"""
Start the Money Cortex backend server.
Run from the backend folder:  python run.py
Then open http://127.0.0.1:8000 in your browser for the app.
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
