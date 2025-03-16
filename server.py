"""
This is for Android, you don't need this file
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class ErrorLog(BaseModel):
    message: str


app = FastAPI()


@app.post("/log")
def receive_error_log(error_log: ErrorLog):
    print(f"Received log: {error_log.message}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
