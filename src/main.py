import json
import os
import uvicorn
from fastapi import FastAPI, HTTPException, Form, Body
from googleapiclient.model import BaseModel
from starlette.responses import RedirectResponse

from request_parser import *
from response import *
from core import *
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register")
async def req_register(data: dict):
    try:
        request = RegisterRequest(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    response = RegisterResponse(request)
    return response.process()


@app.post("/new_post/text")
async def req_new_post_text(data: dict):
    try:
        request = NewPostTextRequest(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    response = NewPostTextResponse(request)
    return response.process()


@app.post("/new_post/image")
async def req_new_post_image(data: str=Form(...), image: UploadFile = File(...)):
    data = json.loads(data)
    try:
        request = NewPostImageRequest(data, image)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    response = NewPostImageResponse(request)
    return response.process()


@app.post("/vote/text")
async def req_vote_text(data: dict):
    try:
        request = VoteTextRequest(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    response = VoteTextResponse(request)
    return response.process()


@app.post("/vote/image")
async def req_vote_text(data: dict):
    try:
        request = VoteImageRequest(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    response = VoteImageResponse(request)
    return response.process()


@app.post("/register_notification")
async def req_register_notification(data: dict):
    try:
        request = RegisterNotificationRequest(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    response = RegisterNotificationResponse(request)
    return response.process()


@app.post("/recommendation")
async def req_recommendation(data: dict):
    try:
        request = RecommendationRequest(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    response = RecommendationResponse(request)
    return response.process()


@app.get("/")
async def root():
    return RedirectResponse("http://alex-xu.site:8000/")


if __name__ == '__main__':
    # respond = RegisterResponse(request)
    print(
        "#" * 10 + "\n" + \
        os.getcwd() + "\n" + \
        "#" * 10
    )

    uvicorn.run(app, host="0.0.0.0", port=8080)
    ...
