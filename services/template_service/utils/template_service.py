"""
Template service utilities and business logic
"""
from pathlib import Path
import shutil
import tempfile
import zipfile
import io
import json
from typing import List, Dict, Any
from datetime import datetime
from ..models.schemas import TemplateInfo, TemplateMetadata, TemplateRegistrationRequest
from ..config.settings import settings


def get_available_templates() -> List[TemplateInfo]:
    """Get all available templates from the templates directory"""
    templates_dir = Path(settings.templates_dir)
    if not templates_dir.exists():
        templates_dir.mkdir(parents=True, exist_ok=True)
    
    templates = []
    for template_dir in templates_dir.iterdir():
        if template_dir.is_dir():
            # Look for template metadata
            metadata_file = template_dir / "metadata.json"
            if metadata_file.exists():
                try:
                    metadata = json.loads(metadata_file.read_text())
                    # Count parameters if they exist in metadata
                    param_count = len(metadata.get("parameters", []))
                    templates.append(TemplateInfo(
                        name=template_dir.name,
                        description=metadata.get("description", "No description"),
                        version=metadata.get("version", "1.0.0"),
                        author=metadata.get("author"),
                        tags=metadata.get("tags", []),
                        parameter_count=param_count
                    ))
                except json.JSONDecodeError:
                    templates.append(TemplateInfo(
                        name=template_dir.name,
                        description="Invalid metadata.json",
                        version="1.0.0",
                        parameter_count=0
                    ))
            else:
                templates.append(TemplateInfo(
                    name=template_dir.name,
                    description="No description",
                    version="1.0.0",
                    parameter_count=0
                ))
    
    return templates


def validate_parameters(template_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Validate parameters against template requirements"""
    template_metadata = get_template_detail(template_name)
    validated_params = parameters.copy()
    
    for param_def in template_metadata.parameters:
        param_name = param_def.name
        param_type = param_def.type
        required = param_def.required
        default = param_def.default
        
        # Check if required parameter is missing
        if required and param_name not in validated_params:
            if default is not None:
                validated_params[param_name] = default
            else:
                raise ValueError(f"Required parameter '{param_name}' is missing")
        
        # If parameter was provided, validate its type
        if param_name in validated_params:
            value = validated_params[param_name]
            if param_type == 'string':
                if not isinstance(value, str):
                    validated_params[param_name] = str(value)
            elif param_type == 'integer':
                try:
                    validated_params[param_name] = int(value)
                except ValueError:
                    raise ValueError(f"Parameter '{param_name}' must be an integer")
            elif param_type == 'boolean':
                if isinstance(value, str):
                    validated_params[param_name] = value.lower() in ('true', '1', 'yes', 'on')
                else:
                    validated_params[param_name] = bool(value)
            elif param_type == 'float':
                try:
                    validated_params[param_name] = float(value)
                except ValueError:
                    raise ValueError(f"Parameter '{param_name}' must be a float")
    
    # Check for any parameters that aren't defined in the template
    allowed_params = {param.name for param in template_metadata.parameters}
    for param_name in validated_params:
        if param_name not in allowed_params:
            # For now, we'll allow extra parameters, but in a real implementation
            # you might want to restrict to only defined parameters
            pass
    
    return validated_params


def get_template_detail(template_name: str) -> TemplateMetadata:
    """Get detailed information about a specific template"""
    templates_dir = Path(settings.templates_dir)
    template_path = templates_dir / template_name
    
    if not template_path.exists():
        raise FileNotFoundError(f"Template '{template_name}' not found")
    
    # Look for template metadata
    metadata_file = template_path / "metadata.json"
    if metadata_file.exists():
        try:
            metadata = json.loads(metadata_file.read_text())
            return TemplateMetadata(**metadata)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid metadata.json for template '{template_name}'")
    else:
        # Create basic metadata from directory
        return TemplateMetadata(
            name=template_name,
            description="No description",
            version="1.0.0",
            created_at=datetime.now()
        )


def register_template(request: TemplateRegistrationRequest) -> bool:
    """Register a new template in the system"""
    templates_dir = Path(settings.templates_dir)
    template_path = templates_dir / request.name
    
    # Check if template already exists
    if template_path.exists():
        raise ValueError(f"Template '{request.name}' already exists")
    
    # Create template directory
    template_path.mkdir(parents=True, exist_ok=True)
    
    # Save metadata
    metadata = {
        "name": request.name,
        "description": request.description,
        "version": request.version,
        "author": request.author,
        "license": request.license,
        "tags": request.tags,
        "parameters": [param.dict() for param in request.parameters],
        "created_at": datetime.now().isoformat()
    }
    
    with open(template_path / "metadata.json", 'w') as f:
        json.dump(metadata, f, indent=2)
    
    # Create basic template structure
    app_dir = template_path / "app"
    app_dir.mkdir(exist_ok=True)
    
    with open(app_dir / "main.py", 'w') as f:
        f.write(f'''from fastapi import FastAPI

app = FastAPI(title="{{{{PROJECT_NAME}}}}", version="{request.version}")

@app.get("/")
async def root():
    return {{"message": "Welcome to {{{{PROJECT_NAME}}}}!", "status": "running"}}

@app.get("/health")
async def health():
    return {{"status": "healthy"}}
''')
    
    with open(template_path / "README.md", 'w') as f:
        f.write(f'''# {{{{PROJECT_NAME}}}}

A project generated from the {request.name} template.

## Description
{request.description}

## Author
{request.author or "Unknown"}
''')
    
    with open(template_path / "requirements.txt", 'w') as f:
        f.write("fastapi>=0.104.1\nuvicorn[standard]>=0.24.0\npydantic>=2.0.0\n")
    
    return True


def customize_project(project_path: Path, project_name: str, parameters: Dict[str, Any]):
    """Apply project-specific customizations"""
    # Replace common placeholders in files
    for file_path in project_path.rglob('*'):
        if file_path.is_file() and file_path.suffix in ['.py', '.md', '.txt', '.yml', '.yaml', '.json', '.toml', '.Dockerfile', '.dockerfile', '.cfg', '.conf', '.ini']:
            try:
                content = file_path.read_text()
                # Replace placeholders
                content = content.replace('{{PROJECT_NAME}}', project_name)
                content = content.replace('{{SERVICE_NAME}}', project_name)
                
                # Apply additional parameters
                for key, value in parameters.items():
                    content = content.replace(f'{{{{{key}}}}}', str(value))
                
                file_path.write_text(content)
            except UnicodeDecodeError:
                # Skip binary files
                continue


def generate_project_zip(template_name: str, project_name: str, parameters: Dict[str, Any]) -> io.BytesIO:
    """Generate a project from a template and return as zip buffer"""
    templates_dir = Path(settings.templates_dir)
    template_path = templates_dir / template_name
    
    if not template_path.exists():
        raise FileNotFoundError(f"Template '{template_name}' not found")
    
    # Validate parameters against template requirements
    validated_parameters = validate_parameters(template_name, parameters)
    
    # Create a temporary directory for the project
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_project_path = Path(temp_dir) / project_name
        
        # Copy template files to temp directory
        shutil.copytree(template_path, temp_project_path, dirs_exist_ok=True)
        
        # Apply parameters to template files
        customize_project(temp_project_path, project_name, validated_parameters)
        
        # Create a zip file of the generated project
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_path in temp_project_path.rglob('*'):
                if file_path.is_file():
                    # Calculate relative path from project directory
                    rel_path = file_path.relative_to(temp_project_path)
                    zip_file.write(file_path, rel_path)
        
        zip_buffer.seek(0)
        return zip_buffer