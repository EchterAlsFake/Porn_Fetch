"""
This is for Android, you don't need this file
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class ErrorLog(BaseModel):
    message: str


app = FastAPI()


@app.post("/error-log/")
def receive_error_log(error_log: ErrorLog):
    print(f"Received error: {error_log.message}")
    return {"detail": "Error log received"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
