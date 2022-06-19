from etl.processors.event_processor import EventProcessor

UserDict = Dict(str: Dict[])

class User(EventProcessor):
    """
    A simple `if` will do for this challenge, but a full schema validation would be better
    """
    def validate_schema(self, data: dict) -> bool:
        if data['metadata'] and data['payload']:
            return True

        return False

    def process(self, data: dict) -> bool:
        return False
