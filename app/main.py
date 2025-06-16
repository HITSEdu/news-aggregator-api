from fastapi import FastAPI, APIRouter
from fastapi.openapi.docs import get_swagger_ui_html

app = FastAPI()

@app.get("/")
async def get_root():
    return {"message": "hello world"}

@app.get("/docs")
async def get_documentation():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
