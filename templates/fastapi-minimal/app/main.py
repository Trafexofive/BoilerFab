from fastapi import FastAPI


app = FastAPI(title="{{PROJECT_NAME}}", version="1.0.0")


@app.get("/")
async def root():
    return {"message": "Welcome to {{PROJECT_NAME}}!", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}