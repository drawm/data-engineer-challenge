from entities.User import User
from processors.event_processor import EventProcessor
from storage import Storage

class UserProcessor(EventProcessor):
    """
    A simple `if` will do for this challenge, but a full schema validation would be better
    """

    def validate_schema(self, data: dict) -> bool:
        return data['metadata'] and data['payload']

    def process(self, data: dict) -> bool:
        print('processing user event')
        user = User(data['payload'], data['metadata'])
        storage = Storage()

        # During user creation, don't override existing users
        if storage.user.get_by_id(user.id):
            return False

        storage.user.insert(user)

        return True
