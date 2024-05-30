import uvicorn

from fastapi import FastAPI

from db.engine import Base, engine

app = FastAPI()


async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.add_event_handler("startup", startup)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
