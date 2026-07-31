from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.middlewares.add_response_headers import addResponseHeadersMiddleware
from api.routers import evaluator


app = FastAPI()

app.include_router(evaluator.router)

origins = ["http://localhost:3000"]

addResponseHeadersMiddleware(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> str:
    return "ping"
