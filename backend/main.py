from fastapi import FastAPI

# Create FastAPI application
app = FastAPI(title="Survey Generator API")

@app.get("/")
def read_root():
    """Root endpoint - just to test the API is working"""
    return {"message": "Hello World! Survey Generator API is running"}




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
