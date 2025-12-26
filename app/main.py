from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Deep Learning")

@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "Hello World"}