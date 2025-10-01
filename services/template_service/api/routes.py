"""
API routes for the FastAPI Template Service
"""
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from typing import List, Dict, Any
from ..models.schemas import TemplateInfo, TemplateMetadata, TemplateRegistrationRequest, GenerateRequest
from ..utils.template_service import (
    get_available_templates, 
    generate_project_zip, 
    get_template_detail,
    register_template,
    validate_parameters
)
from ..utils.auth import verify_api_key, require_api_key


router = APIRouter()


@router.get("/", response_model=dict)
async def root(request: Request):
    if not verify_api_key(request):
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return {"message": "FastAPI Template Service", "status": "running"}


@router.get("/health", response_model=dict)
async def health(request: Request):
    if not verify_api_key(request):
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return {"status": "healthy"}


@router.get("/api/v1/templates", response_model=List[TemplateInfo])
async def list_templates(request: Request):
    """List all available templates"""
    if not verify_api_key(request):
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return get_available_templates()


@router.get("/api/v1/templates/{template_name}", response_model=TemplateMetadata)
async def get_template(template_name: str, request: Request):
    """Get detailed information about a specific template"""
    if not verify_api_key(request):
        raise HTTPException(status_code=401, detail="Invalid API Key")
    try:
        return get_template_detail(template_name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Template '{template_name}' not found")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/v1/templates", status_code=201)
async def create_template(request: TemplateRegistrationRequest, http_request: Request):
    """Register a new template in the system"""
    if not verify_api_key(http_request):
        raise HTTPException(status_code=401, detail="Invalid API Key")
    try:
        success = register_template(request)
        if success:
            return {"message": f"Template '{request.name}' registered successfully", "name": request.name}
        else:
            raise HTTPException(status_code=500, detail="Failed to register template")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registering template: {str(e)}")


@router.post("/api/v1/templates/{template_name}/validate-parameters")
async def validate_template_parameters(template_name: str, parameters: Dict[str, Any], http_request: Request):
    """Validate parameters against a template's requirements"""
    if not verify_api_key(http_request):
        raise HTTPException(status_code=401, detail="Invalid API Key")
    try:
        validated_params = validate_parameters(template_name, parameters)
        return {
            "valid": True,
            "parameters": validated_params,
            "message": "Parameters are valid for the template"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Template '{template_name}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating parameters: {str(e)}")


@router.post("/api/v1/generate")
async def generate_project(request: GenerateRequest, http_request: Request):
    """Generate a project from a template and return as zip file"""
    if not verify_api_key(http_request):
        raise HTTPException(status_code=401, detail="Invalid API Key")
    try:
        zip_buffer = generate_project_zip(
            request.template_name,
            request.project_name,
            request.parameters
        )
        
        # Return the zip file as a streaming response
        return StreamingResponse(
            iter([zip_buffer.getvalue()]),
            media_type="application/zip",
            headers={
                "Content-Disposition": f"attachment; filename={request.project_name}.zip"
            }
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating project: {str(e)}")