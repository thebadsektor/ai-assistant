import uvicorn

# Run backend and frontend with hot reload
if __name__ == "__main__":
    uvicorn.run("backend.src.main:app",
                host="0.0.0.0",
                port=8000,
                log_level="info",
                reload=True)