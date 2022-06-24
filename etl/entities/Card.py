import json

from entities.Metadata import Metadata


class Card:
    def __init__(self, payload, metadata):
        self.json_metadata = json.dumps(metadata)
        self.metadata = Metadata(metadata)
        self.id = payload['id']
        self.user_id = payload['user_id']
        self.created_by_name = payload['created_by_name']
        self.updated_at = payload['updated_at']
        self.created_at = payload['created_at']
        self.active = payload['active']
