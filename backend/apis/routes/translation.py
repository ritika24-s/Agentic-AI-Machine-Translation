from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import logging
from datetime import datetime
import asyncio

from apis.models.requests import TranslationRequest, BatchTranslationRequest
from apis.models.responses import TranslationResponse, BatchTranslationResponse, ErrorResponse, SupportedLanguagesResponse
from apis.utils.dependencies import get_translation_service, generate_request_id


# Create router instance
router = APIRouter(prefix="/api/v1", tags=["translation"])
logger = logging.getLogger(__name__)


@router.post(
    "/translate",
    response_model=TranslationResponse,
    status_code=200,
    summary="Translate text using multi-agent AI system",
    description="Translates text with better quality through specialized agent collaboration"
)
async def translate_text(
    request: TranslationRequest,
    # Dependency injection for translation service
    translation_service = Depends(get_translation_service),
    request_id: str = Depends(generate_request_id)
) -> TranslationResponse:
    """
    Main translation endpoint with intelligent agent routing
    
    This endpoint orchestrates your 5 AI agents:
    1. Intelligence Router - Analyzes text complexity
    2. Context Manager - Manages conversation context
    3. Translation Specialist - Performs translation
    4. Quality Guardian - Reviews quality
    5. Results Synthesizer - Finalizes output
    """
    try:
        from apis.services.translation import agent_service
        from apis.services.websocket import manager
        
        logger.info(f"Translation request received: {request_id}")
        start_time = datetime.now()
        
        # Execute workflow with WebSocket updates
        result = await agent_service.execute_translation_workflow(
            {
                "text": request.text,
                "source_language": request.source_language,
                "target_language": request.target_language,
                "context": request.context,
                "request_id": request_id
            },
            websocket_manager=manager
        )
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Build response matching frontend expectations
        return TranslationResponse(
            request_id=request_id,
            translated_text=result["translated_text"],
            source_language=result.get("detected_language", request.source_language),
            target_language=request.target_language,
            confidence_score=result.get("confidence_score", 0.9),
            agent_activities=result.get("agent_activities", []),
            quality_metrics=result.get("quality_metrics", {}),
            processing_time=processing_time,
            complexity=result.get("complexity", "simple")
        )
        
    except Exception as e:
        logger.error(f"Translation failed for request {request_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Translation failed: {str(e)}"
        )


@router.post("/translate/batch", response_model=BatchTranslationResponse)
async def batch_translate(
    request: BatchTranslationRequest,
    background_tasks: BackgroundTasks,
    translation_service = Depends(get_translation_service),
    batch_id: str = Depends(generate_request_id)
):
    """
    Batch translation with concurrent processing
    
    Processes multiple texts simultaneously using asyncio for better performance
    """
    try:
        if len(request.texts) > 50:
            raise HTTPException(status_code=400, detail="Batch size limit exceeded")
        
        start_time = datetime.now()
        
        # Create translation tasks for concurrent processing
        async def translate_single(text: str, index: int):
            single_request = TranslationRequest(
                text=text,
                source_language=request.source_language,
                target_language=request.target_language,
                context=request.context
            )
            
            return await translate_text(single_request, translation_service, f"{batch_id}-{index}")
        
        # Process all translations concurrently
        tasks = [translate_single(text, i) for i, text in enumerate(request.texts)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Separate successful and failed translations
        successful_results = []
        failed_count = 0
        
        for result in results:
            if isinstance(result, Exception):
                failed_count += 1
                logger.error(f"Batch translation failed: {result}")
            else:
                successful_results.append(result)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return BatchTranslationResponse(
            batch_id=batch_id,
            total_items=len(request.texts),
            completed_items=len(successful_results),
            failed_items=failed_count,
            results=successful_results,
            overall_processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Batch translation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/languages", response_model=SupportedLanguagesResponse)
async def get_supported_languages():
    """Get all supported language pairs with quality metrics"""
    
    # This would typically come from agent configuration
    language_pairs = [
        {"source": "en", "target": "es", "quality_score": 0.95, "agent_preference": "specialist"},
        {"source": "en", "target": "fr", "quality_score": 0.92, "agent_preference": "specialist"},
        {"source": "en", "target": "de", "quality_score": 0.89, "agent_preference": "general"},
        # Add more based on agents' capabilities
    ]
    
    return SupportedLanguagesResponse(
        languages=language_pairs,
        total_pairs=len(language_pairs)
    )


@router.get("/translate/status/{request_id}")
async def get_translation_status(request_id: str):
    """Get current status of a translation request"""
    from apis.services.translation import agent_service
    
    status = agent_service.get_translation_status(request_id)
    
    if status["status"] == "not_found":
        raise HTTPException(status_code=404, detail="Translation request not found")
    
    return status


@router.delete("/translate/{request_id}")
async def cancel_translation(request_id: str):
    """Cancel an ongoing translation"""
    from apis.services.translation import agent_service
    
    success = await agent_service.cancel_translation(request_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Translation request not found")
    
    return {"message": "Translation cancelled", "request_id": request_id}