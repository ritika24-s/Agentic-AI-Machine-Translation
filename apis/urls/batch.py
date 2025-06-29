from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List
import asyncio
import logging
from datetime import datetime

from app.models.requests import BatchTranslationRequest
from app.models.responses import BatchTranslationResponse, BatchResult
from app.services.translation_service import TranslationService
from app.services.cache_service import CacheService
from app.api.deps import get_translation_service, get_cache_service, generate_request_id

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/translate/batch",
    response_model=BatchTranslationResponse,
    status_code=200,
    summary="Batch translate multiple texts",
    description="Process multiple translations simultaneously with intelligent load balancing"
)
async def batch_translate(
    request: BatchTranslationRequest,
    background_tasks: BackgroundTasks,
    translation_service: TranslationService = Depends(get_translation_service),
    cache_service: CacheService = Depends(get_cache_service),
    batch_id: str = Depends(generate_request_id)
) -> BatchTranslationResponse:
    """
    Batch translation endpoint with concurrent processing
    """
    try:
        logger.info(f"Batch translation request: {batch_id}, {len(request.texts)} texts")
        
        # Validate batch size
        if len(request.texts) > 50:  # Configurable limit
            raise HTTPException(
                status_code=400,
                detail="Batch size exceeds maximum limit of 50 texts"
            )
        
        # Check for cached results
        cached_results = []
        texts_to_process = []
        
        for i, text in enumerate(request.texts):
            cached = await cache_service.get_translation(
                text=text,
                source_language=request.source_language,
                target_language=request.target_language
            )
            
            if cached:
                cached_results.append(BatchResult(
                    index=i,
                    source_text=text,
                    translation=cached["translation"],
                    status="completed",
                    quality_score=cached.get("quality_metrics", {}).get("overall_score", 0.0),
                    processing_time=0.0,
                    cached=True
                ))
            else:
                texts_to_process.append((i, text))
        
        # Process uncached texts
        if texts_to_process:
            if len(texts_to_process) > 10:  # Process large batches in background
                # Store batch status
                await cache_service.set_batch_status(
                    batch_id=batch_id,
                    status="processing",
                    total_count=len(request.texts),
                    completed_count=len(cached_results)
                )
                
                background_tasks.add_task(
                    process_batch_async,
                    batch_id,
                    texts_to_process,
                    request,
                    translation_service,
                    cache_service
                )
                
                return BatchTranslationResponse(
                    batch_id=batch_id,
                    status="processing",
                    total_count=len(request.texts),
                    completed_count=len(cached_results),
                    results=cached_results,
                    message="Large batch processing in background. Check status for updates.",
                    timestamp=datetime.now()
                )
            
            # Process small batches immediately
            processing_results = await process_texts_concurrently(
                texts_to_process,
                request,
                translation_service,
                cache_service
            )
            cached_results.extend(processing_results)
        
        # Sort results by index
        all_results = sorted(cached_results, key=lambda x: x.index)
        success_count = len([r for r in all_results if r.status == "completed"])
        
        return BatchTranslationResponse(
            batch_id=batch_id,
            status="completed",
            total_count=len(request.texts),
            completed_count=len(all_results),
            success_count=success_count,
            results=all_results,
            timestamp=datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch translation failed: {e}")
        raise HTTPException(status_code=500, detail="Batch translation failed")


async def process_texts_concurrently(
    texts_to_process: List[tuple],
    request: BatchTranslationRequest,
    translation_service: TranslationService,
    cache_service: CacheService
) -> List[BatchResult]:
    """
    Process multiple texts concurrently with rate limiting
    """
    semaphore = asyncio.Semaphore(5)  # Limit concurrent translations
    
    async def process_single_text(index_text_pair):
        index, text = index_text_pair
        async with semaphore:
            try:
                start_time = datetime.now()
                
                result = await translation_service.translate(
                    text=text,
                    source_language=request.source_language,
                    target_language=request.target_language,
                    request_id=f"batch_{index}"
                )
                
                processing_time = (datetime.now() - start_time).total_seconds()
                
                # Cache individual result
                await cache_service.cache_translation(
                    text=text,
                    source_language=request.source_language,
                    target_language=request.target_language,
                    result=result
                )
                
                return BatchResult(
                    index=index,
                    source_text=text,
                    translation=result.translation,
                    status="completed",
                    quality_score=result.quality_metrics.get("overall_score", 0.0),
                    processing_time=processing_time,
                    cached=False
                )
                
            except Exception as e:
                logger.error(f"Failed to process text at index {index}: {e}")
                return BatchResult(
                    index=index,
                    source_text=text,
                    status="failed",
                    error_message=str(e),
                    processing_time=0.0,
                    cached=False
                )
    
    # Process all texts concurrently
    tasks = [process_single_text(item) for item in texts_to_process]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Handle any exceptions
    processed_results = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            index, text = texts_to_process[i]
            processed_results.append(BatchResult(
                index=index,
                source_text=text,
                status="failed",
                error_message=str(result),
                processing_time=0.0,
                cached=False
            ))
        else:
            processed_results.append(result)
    
    return processed_results


async def process_batch_async(
    batch_id: str,
    texts_to_process: List[tuple],
    request: BatchTranslationRequest,
    translation_service: TranslationService,
    cache_service: CacheService
):
    """
    Background task for large batch processing
    """
    try:
        results = await process_texts_concurrently(
            texts_to_process,
            request,
            translation_service,
            cache_service
        )
        
        # Store final batch results
        await cache_service.set_batch_results(batch_id, results)
        await cache_service.set_batch_status(
            batch_id=batch_id,
            status="completed",
            total_count=len(texts_to_process),
            completed_count=len(results)
        )
        
    except Exception as e:
        logger.error(f"Background batch processing failed for {batch_id}: {e}")
        await cache_service.set_batch_status(
            batch_id=batch_id,
            status="failed",
            error=str(e)
        )


@router.get(
    "/translate/batch/status/{batch_id}",
    summary="Get batch translation status",
    description="Check the status of a batch translation request"
)
async def get_batch_status(
    batch_id: str,
    cache_service: CacheService = Depends(get_cache_service)
):
    """
    Get batch translation status and progress
    """
    try:
        status_data = await cache_service.get_batch_status(batch_id)
        
        if not status_data:
            raise HTTPException(
                status_code=404,
                detail=f"Batch request {batch_id} not found"
            )
        
        return {
            "batch_id": batch_id,
            "status": status_data.get("status"),
            "total_count": status_data.get("total_count", 0),
            "completed_count": status_data.get("completed_count", 0),
            "progress_percentage": (status_data.get("completed_count", 0) / 
                                  max(status_data.get("total_count", 1), 1)) * 100,
            "error_message": status_data.get("error"),
            "timestamp": datetime.now()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch status check failed for {batch_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve batch status")

