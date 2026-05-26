from fastapi import FastAPI
import os

app = FastAPI(title="Backend API")


@app.get("/")
def read_root():
    return {"status": "ok"}
