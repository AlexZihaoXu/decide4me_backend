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
        result_image_path = generate_token() + "_" + self.request.image.filename
        converting_image_path = generate_token() + "_" + self.request.image.filename

        fp, converting_path = open_file(["cache", "images"], converting_image_path)
        fp.write(self.request.image.file.read())
        fp.close()

        image = pygame.image.load(converting_path)
        os.remove(converting_path)

        max_len = 1024
        w, h = image.get_size()
        max_side = max(w, h)
        rate = 1.0 if max_side < max_len else max_len/max_side

        if rate != 1.0:
            image = pygame.transform.smoothscale(image, (int(w*rate), int(h*rate)))
        make_dirs(["cache", "images"])
        pygame.image.save(image, "cache/images/"+result_image_path)

        blob = bucket.blob(
            "images/" + result_image_path
        )

        blob.upload_from_filename("cache/images/"+result_image_path)
        os.remove("cache/images/"+result_image_path)

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
                "text": None,
                "image": {
                    "imageUrl": blob.public_url,
                    "choices": []
                }
            }
        )

        return {}


