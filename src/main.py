from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from src.api.v1.bucket.get_all_buckets import router as get_bucket_router

app = FastAPI(title="local-ml-testing", description="Api to handle lambdas and ML interactions")
app.include_router(get_bucket_router)

@app.exception_handler(Exception)
async def default_exception_handler(request: Request, e: Exception):
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={e.__class__.__name__: str(e)})

@app.get("/")
def read_root():
    return {
        "app": "Local Machine Learning Flow",
        "endpoints": ["/bucket/get-all-buckets"]
    }