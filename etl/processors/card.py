from etl.processors.event_processor import EventProcessor


class Card(EventProcessor):
    def validate_schema(self, data: dict) -> bool:
        return False

    def process(self, data: dict) -> bool:
        return False
