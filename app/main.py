from fastapi import FastAPI

app = FastAPI(title="Backend API")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"status": 123}
