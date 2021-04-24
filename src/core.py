import firebase_admin
import dotenv
from google.cloud import firestore
from firebase_admin import auth

dotenv.load_dotenv()
firebase_admin.initialize_app(options={
    'storageBucket': 'decide4me-pegasis.appspot.com'
})
database: firestore.Client = firestore.Client()


class Data:
    def __init__(self, data: dict):
        self.data = data

    def get(self, key, _type: type = None):
        if key in self.data:
            if _type and (type(self.data[key]) != _type):
                raise KeyError(f"""Wrong type of key: {str(key)} | Type: {type(self.data[key])} | Expected: {_type}""")
            return self.data[key]
        raise KeyError("Missing field: " + str(key))

    def __getitem__(self, item):
        return self.get(item)
