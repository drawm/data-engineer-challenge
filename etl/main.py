import time
from typing import Dict

from extractor import extract_events
from processors.card import CardProcessor
from processors.event_processor import EventProcessor
from processors.user import UserProcessor

event_processors: Dict[str, EventProcessor] = {
    'card': CardProcessor(),
    'user': UserProcessor(),
}

# TODO: Add a way to process new events (loop / watch)
delay = 2
while True:
    print('Starting extraction now!')
    extract_events(event_processors)
    print('Extraction completed, waiting for %s seconds...' % delay)
    time.sleep(delay)
