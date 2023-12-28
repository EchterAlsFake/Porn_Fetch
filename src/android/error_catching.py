"""
This is a simple server used to catch errors. Debugging on Android isn't really easy, because I can't just use
the Android Studio for debugging Python code :D

So that's why the main application will report errors locally to my server.

(Of course only when developing. The final release won't contain this)
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