import random

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


def make_dirs(path: "list[str]"):
    p = ''
    for node in path:
        p += node + "/"
        try:
            os.mkdir(p)
        except FileExistsError:
            pass
    return p


def get_uid_of(id_token) -> str:
    return auth.verify_id_token(id_token)["uid"]


def open_file(path: "list[str]", name: str, method='wb'):
    path = make_dirs(path)
    return open(path+name, method), path+name


def generate_token() -> str:
    return ''.join(
        [
            chr(
                random.randint(97, 122) if random.randint(0, 1) else
                random.randint(65, 90)
            )
            for i in range(16)
        ]
    )


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
