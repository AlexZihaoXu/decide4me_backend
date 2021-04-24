from fastapi import File, UploadFile

from core import Data


class BaseRequest:
    def __init__(self, data: dict):
        data = self.data = Data(data)
        self.id_token: str = data['idToken']


class RecommendationRequest(BaseRequest):

    def __init__(self, data: dict):
        super().__init__(data)
        data = self.data

        self.start: int = data.get("start", int)
        self.length: int = data.get("length", int)
        self.refreshID: str = data.get("string", str)


class RegisterRequest(BaseRequest):

    def __init__(self, data: dict):
        super().__init__(data)
        data = self.data
        self.profile_image_url: str = data.get("profileImageUrl", str)
        self.name: str = data.get("name", str)


class NewPostRequest(BaseRequest):

    def __init__(self, data: dict):
        super().__init__(data)
        data = self.data
        self.title: str = self.data.get("title", str)
        self.description: str = self.data.get("description", str)
        self.target_votes: int = self.data.get("targetVotes", int)


class NewPostTextRequest(NewPostRequest):
    def __init__(self, data: dict):
        super().__init__(data)
        self.choices: "list[str]" = self.data.get("choices", list)


class NewPostImageRequest(NewPostRequest):
    def __init__(self, data: dict, file: UploadFile = File(...)):
        super().__init__(data)
        data = self.data
        self.image: UploadFile = file
