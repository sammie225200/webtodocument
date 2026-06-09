from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from .services.document_parser import DocumentParser
from .services.mistral_service import MistralService
from .models import ConvertResponse
import tempfile
import os

router = APIRouter()
mistral_service = MistralService()

@router.post("/convert", response_model=ConvertResponse)
async def convert_document(
    file: UploadFile = File(...),
    style: str = "modern"
):
    """Upload a document and convert it to a website"""
    
    # Validate file type
    allowed_types = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain"
    ]
    
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: PDF, DOCX, TXT"
        )
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Parse document text
        document_text = await DocumentParser.parse_file(file_content, file.content_type)
        
        if not document_text or len(document_text.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="No text content found in document"
            )
        
        # Generate website using Mistral
        result = await mistral_service.generate_website(document_text, style)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return ConvertResponse(
            success=True,
            html=result["html"],
            document_length=len(document_text),
            tokens_used=result.get("tokens_used", 0)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@router.get("/health")
async def health_check():
    return {"status": "healthy"}

@router.post("/validate-api-key")
async def validate_api_key(api_key: str):
    """Test if API key is valid (optional endpoint)"""
    try:
        test_client = OpenAI(
            base_url="https://api.mistral.ai/v1",
            api_key=api_key
        )
        # Simple test call
        return {"valid": True}
    except:
        return {"valid": False, "error": "Invalid API key"}