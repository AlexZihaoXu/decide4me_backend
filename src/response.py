import random
import pygame

from request_parser import *
from core import *


class BaseResponse:

    def __init__(self, request: BaseRequest):
        self.request: BaseRequest = request

    def process(self) -> dict:
        raise NotImplemented("Method process not implemented!")


class RegisterResponse(BaseResponse):

    def __init__(self, request: RegisterRequest):
        super().__init__(request)
        self.request: RegisterRequest = self.request

    def process(self) -> dict:
        collection = database.collection("users")
        uid = auth.verify_id_token(self.request.id_token)["uid"]
        import google.api_core.exceptions
        content = {
            "id": uid,
            "name": self.request.name,
            "profileImageUrl": self.request.profile_image_url,
            "notificationTokens": []
        }
        try:
            collection.add(
                content,
                uid
            )
        except google.api_core.exceptions.AlreadyExists:
            collection.document(uid).update(
                content
            )
        return {}


class NewPostTextResponse(BaseResponse):
    def __init__(self, request: NewPostTextRequest):
        super().__init__(request)
        self.request: NewPostTextRequest = request

    def process(self) -> dict:

        collection = database.collection("posts")
        uid = auth.verify_id_token(self.request.id_token)["uid"]

        collection.add(
            {
                "userId": uid,
                "title": self.request.title,
                "description": self.request.description,
                "time": firestore.SERVER_TIMESTAMP,
                "views": 0,
                "targetVotes": self.request.target_votes,
                "text": {
                    "choices": [
                        {
                            "text": choice,
                            "vote": 0
                        }
                        for choice in self.request.choices
                    ]
                },
                "image": None
            }
        )

        return {}


class NewPostImageResponse(BaseResponse):
    def __init__(self, request: BaseRequest):
        super().__init__(request)
        self.request: NewPostImageRequest = self.request

    def process(self) -> dict:
        image_id = ''.join(
            [
                chr(
                    random.randint(97, 123) if random.randint(0, 2) else
                    random.randint(65, 91)
                )
                for i in range(64)
            ]
        )

        fp, path = open_file(["cache", "image"], image_id)
        fp.write(self.request.image.file.read())
        fp.close()

        blob = bucket.blob(
            "images/"+image_id
        )

        blob.upload_from_filename(path)

        os.remove(path)

        collection = database.collection("posts")
        uid = 'ovo'  # auth.verify_id_token(self.request.id_token)["uid"]

        collection.add(
            {
                "userId": uid,
                "title": self.request.title,
                "description": self.request.description,
                "time": firestore.SERVER_TIMESTAMP,
                "views": 0,
                "targetVotes": self.request.target_votes,
                "text": None,
                "image": {
                    "imageUrl": blob.public_url,
                    "choices": []
                }
            }
        )

        return {}
