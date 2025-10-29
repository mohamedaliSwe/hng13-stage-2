"""Contains the app configurations"""

from fastapi import FastAPI
from src.routes import countries
from src.models.db import init_db


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


app.include_router(countries.router)


if __name__ == "__main__":
    import uvicorn

    port = int(config("PORT", 8000))
    uvicorn.run("src.app:app", host="0.0.0.0", port=port)
