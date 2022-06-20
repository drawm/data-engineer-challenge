from typing import Dict

from etl.extractor import extract_events
from etl.processors.card import CardProcessor
from etl.processors.event_processor import EventProcessor
from etl.processors.user import UserProcessor

event_processors: Dict[str, EventProcessor] = {
    'card': CardProcessor(),
    'user': UserProcessor(),
}

# TODO: Add a way to process new events (loop / watch)
extract_events(event_processors)
