from fastapi import FastAPI

app = FastAPI(title="Backend API")


@app.get("/")
def read_root():
    return {"status": "ok"}
