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
        collection = database.collection("user")
        uid = auth.verify_id_token(self.request.id_token)["uid"]
        collection.add(
            {
                "id": uid,
                "name": self.request.name,
                "profileImageUrl": self.request.profile_image_url,
                "notificationTokens": []
            },
            uid
        )

        return {}
