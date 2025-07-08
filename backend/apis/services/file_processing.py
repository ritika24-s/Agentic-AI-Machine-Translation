import asyncio
import aiofiles
import uuid
from pathlib import Path
from typing import Dict, Any, List
import logging
from datetime import datetime

from fastapi import UploadFile, HTTPException
import PyPDF2
import docx


logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Class for handling document upload and processing for translation"""
    
    def __init__(self):
        # base path for data
        self.base_path = Path("Data/files/")
        self.base_path.mkdir(exist_ok=True)
        
        # Create upload directory if it doesn't exist
        self.upload_dir = self.base_path + "uploads"
        self.upload_dir.mkdir(exist_ok=True)
        
        # Create processed directory if it doesn't exist
        self.processed_dir = self.base_path + "processed"
        self.processed_dir.mkdir(exist_ok=True)
        
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.allowed_types = {
            "application/pdf": ".pdf",
            "text/plain": ".txt",
            "application/msword": ".doc",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx"
        }
    
    async def process_upload(
        self, 
        file: UploadFile, 
        source_language: str, 
        target_language: str
    ) -> Dict[str, Any]:
        """Process uploaded document and extract text for translation"""
        
        # Validate file
        await self._validate_file(file)
        
        # Generate task ID
        task_id = str(uuid.uuid4())
        
        # Save uploaded file
        file_path = await self._save_upload(file, task_id)
        
        try:
            # Extract text based on file type
            extracted_text = await self._extract_text(file_path, file.content_type)
            
            # Split text into chunks if large document
            text_chunks = self._chunk_text(extracted_text)
            
            return {
                "task_id": task_id,
                "filename": file.filename,
                "file_type": file.content_type,
                "file_size": file.size,
                "text_chunks": text_chunks,
                "total_chunks": len(text_chunks),
                "source_language": source_language,
                "target_language": target_language,
                "status": "ready_for_translation",
                "created_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            # Clean up on error
            file_path.unlink(missing_ok=True)
            raise HTTPException(status_code=400, detail=f"Failed to process document: {str(e)}")
    
    async def _validate_file(self, file: UploadFile):
        """Validate uploaded file type and size"""
        # Check file size
        if file.size > self.max_file_size:
            raise HTTPException(
                status_code=413,
                detail=f"File size {file.size} exceeds maximum {self.max_file_size} bytes"
            )
        
        # Check file type
        if file.content_type not in self.allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file.content_type} not supported. Allowed: {list(self.allowed_types.keys())}"
            )
    
    async def _save_upload(self, file: UploadFile, task_id: str) -> Path:
        """Save uploaded file to disk"""
        
        file_extension = self.allowed_types[file.content_type]
        file_path = self.upload_dir / f"{task_id}{file_extension}"
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        return file_path
    
    async def _extract_text(self, file_path: Path, content_type: str) -> str:
        """Extract text from different document types"""
        
        if content_type == "application/pdf":
            return await self._extract_pdf_text(file_path)
        elif content_type == "text/plain":
            return await self._extract_txt_text(file_path)
        elif content_type in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            return await self._extract_docx_text(file_path)
        else:
            raise ValueError(f"Unsupported content type: {content_type}")
    
    async def _extract_pdf_text(self, file_path: Path) -> str:
        """Extract text from PDF file"""
        
        def extract_sync():
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        
        return await asyncio.to_thread(extract_sync)
    
    async def _extract_txt_text(self, file_path: Path) -> str:
        """Extract text from TXT file"""
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            return await f.read()
    
    async def _extract_docx_text(self, file_path: Path) -> str:
        """Extract text from DOCX file"""
        def extract_sync():
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        
        return await asyncio.to_thread(extract_sync)
    
    def _chunk_text(self, text: str, max_chunk_size: int = 3000) -> List[str]:
        """Split large text into manageable chunks for translation"""
        
        # Simple sentence-based chunking
        sentences = text.split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < max_chunk_size:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks

# Global processor instance
document_processor = DocumentProcessor()