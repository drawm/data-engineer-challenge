import os
from typing import Dict

from config import Config
import json

from processors.event_processor import EventProcessor

config = Config(os.environ)


def __load_json_file(path: str):
    io_handle = open(path, "r")
    json_data = json.load(io_handle)
    io_handle.close()
    return json_data


def __mark_file(file_path: str, event_type: str, file_name: str, mark: str):
    destination_dir = os.path.join(config.DIR_LOCATION, mark, event_type)
    destination_path = os.path.join(destination_dir, file_name)

    os.makedirs(destination_dir, exist_ok=True)
    os.replace(file_path, destination_path)
    return destination_path


def __mark_as_processing(file_path: str, event_type: str, file_name: str) -> str:
    return __mark_file(file_path, event_type, file_name, 'processing')


def __mark_as_invalid(file_path: str, event_type: str, file_name: str) -> str:
    return __mark_file(file_path, event_type, file_name, 'invalid')


def __mark_as_completed(file_path: str, event_type: str, file_name: str) -> str:
    return __mark_file(file_path, event_type, file_name, 'completed')

"""
Extract event out of the file system and pass them to the right processor based on its metadata
"""
def extract_events(event_processors: Dict[str, EventProcessor]):
    for event_dir in os.scandir(os.path.join(config.DIR_LOCATION, 'inbox')):
        if event_dir.is_dir():
            for event_file in os.scandir(event_dir.path):
                if event_file.is_file() and event_file.name.endswith('.json'):
                    event_file_path = event_file.path
                    event = __load_json_file(event_file_path)
                    event_type = event['metadata']['type']
                    print("==> Processing event type '%s'" % event_type)

                    # TODO: Move to /processing/{event_type}/
                    event_file_path = __mark_as_processing(event_file_path, event_type, event_file.name)

                    processor = event_processors[event_type]
                    if not processor:
                        print('Unprocessable event type "%s"' % event_type)
                        __mark_as_invalid(event_file_path, event_type, event_file.name)
                        pass

                    if processor.validate_schema(event):
                        success = processor.process(event)
                        if success:
                            __mark_as_completed(event_file_path, event_type, event_file.name)
                    else:
                        print('Event is invalid "%s"' % event)
                        __mark_as_invalid(event_file_path, event_type, event_file.name)
