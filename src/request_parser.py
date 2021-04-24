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
