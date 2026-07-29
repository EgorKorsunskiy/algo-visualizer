from fastapi import FastAPI

from api.routers import evaluator


app = FastAPI()

app.include_router(evaluator.router)


@app.get("/")
async def root() -> str:
    return "ping"
