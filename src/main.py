
import uvicorn
from fastapi import FastAPI, HTTPException
from googleapiclient.model import BaseModel

from request_parser import *
from response import *
from core import *
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "*"
]

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.post("/register")
async def req_register(_data: dict):
    try:
        request = RegisterRequest(_data)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    response = RegisterResponse(request)
    return response.process()

if __name__ == '__main__':
    # respond = RegisterResponse(request)
    uvicorn.run(api, host="0.0.0.0", port=8080)
    ...
