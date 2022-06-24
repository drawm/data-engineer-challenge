from etl.entities.User import User
from etl.processors.event_processor import EventProcessor
from etl.storage import Storage

class UserProcessor(EventProcessor):
    """
    A simple `if` will do for this challenge, but a full schema validation would be better
    """

    def validate_schema(self, data: dict) -> bool:
        if data['metadata'] and data['payload']:
            return True

        return False

    def process(self, data: dict) -> bool:
        print('processing user event')
        user = User(data)
        storage = Storage()

        if storage.user.get_by_id(user.id):
            return False

        storage.user.insert(user)

        return True
