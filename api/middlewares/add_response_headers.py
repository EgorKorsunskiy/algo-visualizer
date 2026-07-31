from fastapi import FastAPI, Request, Response


def addResponseHeadersMiddleware(app: FastAPI):
    @app.middleware("http")
    async def addResponseHeaders(request: Request, call_next):
        response: Response = await call_next(request)
        response.headers["Content-Type"] = "application/json"
        return response
