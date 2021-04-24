import firebase_admin
import os
import dotenv
from google.cloud import firestore
from firebase_admin import auth, storage

dotenv.load_dotenv()
firebase_admin.initialize_app(options={
    'storageBucket': 'decide4me-pegasis.appspot.com'
})
database: firestore.Client = firestore.Client()
bucket = storage.bucket()


def open_file(path: "list[str]", name: str):
    path = ''
    for node in path:
        path += node + "/"
        try:
            os.mkdir(path)
        except FileExistsError:
            pass
    return open(path+name, 'wb'), path+name


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
