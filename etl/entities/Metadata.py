class Metadata():
    def __init__(self, data):
        self.type = 'user'
        self.event_at = data['event_at']
        self.event_id = data['event_id']

