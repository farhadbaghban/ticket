from fastapi import FastAPI
import uvicorn

from db.engine import Base, engine

app = FastAPI()
Base.metadata.create_all(engine)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
