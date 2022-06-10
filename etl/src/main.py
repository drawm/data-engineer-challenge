import os
import json

DIR_LOCATION = os.environ.get('EVENT_DIR')
if DIR_LOCATION is None:
    DIR_LOCATION = '/app/events/'

print("DIR_LOCATION = %s" % DIR_LOCATION)
print("Starting ETL")

def load_json_file(path):
    io_handle = open(path, "r")
    json_data = json.load(io_handle)
    io_handle.close()
    return json_data

def print_dict(dict):
    for key, value in dict.items():
        print(key, ":", value)



for event_dir in os.scandir(DIR_LOCATION):
    if event_dir.is_dir():
        print("==> Processing event type '%s'" % event_dir.name)
        for event_file in os.scandir(event_dir.path):
            if event_file.is_file() and event_file.name.endswith('.json'):
                print("===> Parsing file '% s'" % event_file.path)
                event = load_json_file(event_file.path)
                print_dict(event)
