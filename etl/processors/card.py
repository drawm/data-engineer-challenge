from etl.processors.event_processor import EventProcessor


class CardProcessor(EventProcessor):
    """
    A simple `if data['payload']['user_id']` will do for this challenge, but a full schema validation would be better
    """
    def validate_schema(self, data: dict) -> bool:
        if data['metadata'] and data['payload'] and data.get('payload').get('user_id'):
            return True
        return False

    def process(self, data: dict) -> bool:
        return False
