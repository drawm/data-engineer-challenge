from etl.processors.event_processor import EventProcessor
from etl.storage import Storage


class Metadata():
    def __init__(self, data):
        self.type = 'user'
        self.event_at = data['event_at']
        self.event_id = data['event_id']


class User():
    def __init__(self, data):
        self.metadata = Metadata(data['metadata'])
        self.id = data['payload']['id']
        self.name = data['payload']['name']
        self.address = data['payload']['address']
        self.job = data['payload']['job']
        self.score = data['payload']['score']


class UserProcessor(EventProcessor):
    """
    A simple `if` will do for this challenge, but a full schema validation would be better
    """

    def validate_schema(self, data: dict) -> bool:
        if data['metadata'] and data['payload']:
            return True

        return False

    def process(self, data: dict) -> bool:
        try:
            user = User(data)
            storage = Storage()

            if storage.user.get_by_id(user.id):
                return False

            storage.user.insert(user)
        except (Exception) as error:
            print(error)

        return True
