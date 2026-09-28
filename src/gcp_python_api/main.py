from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/greet/{name}")
async def greet(name: str) -> dict[str, str]:
    return {"message": f"Hello, {name}!"}