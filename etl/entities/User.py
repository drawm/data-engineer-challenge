import json

from entities.Metadata import Metadata


class User:
    def __init__(self, payload, metadata):
        self.json_metadata = json.dumps(metadata)
        self.metadata = Metadata(metadata)
        self.id = payload['id']
        self.name = payload['name']
        self.address = payload['address']
        self.job = payload['job']
        self.score = payload['score']

