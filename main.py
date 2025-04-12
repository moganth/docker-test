from fastapi import FastAPI
import uvicorn
from routes.docker_routes import router as docker_router

app = FastAPI(openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)
app.include_router(docker_router, prefix="/api")

@app.get("/api/home")
async def root():
    return {"message": "API Home"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=1243, reload=True)
