from typing import Union
from uuid import uuid4
from fastapi import FastAPI
from loguru import logger
from time import sleep

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/tests")
def read_root():
    return {"Hello": "World"}

@app.get("/tests1")
def read_root():
    return {"Hello": "World"}

@app.get("/tests2")
def read_root():
    return {"Hello": "World"}

@app.get("/tests3")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/load")
async def run_load_test():
    request_id = str(uuid4())
    logger.info(f"Starting request {request_id}")
    sleep(2)
    logger.info(f"Finished request {request_id}")
    return "Ok"

import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False, log_level="debug")
                #workers=1, limit_concurrency=1, limit_max_requests=1)
