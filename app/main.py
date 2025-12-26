from fastapi import FastAPI

app = FastAPI(title="Deep Learning")

@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "Hello World"}
