"""
{{PROJECT_NAME}} - Example Application
Customize this file for your specific application needs
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="{{PROJECT_NAME}}",
    description="Application with universal Docker Compose Makefile",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to {{PROJECT_NAME}}!",
        "status": "running",
        "makefile": "Use 'make help' for available commands"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "{{PROJECT_NAME}}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)