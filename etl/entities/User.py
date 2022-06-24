from etl.entities.Metadata import Metadata


class User():
    def __init__(self, data):
        self.metadata = Metadata(data['metadata'])
        self.id = data['payload']['id']
        self.name = data['payload']['name']
        self.address = data['payload']['address']
        self.job = data['payload']['job']
        self.score = data['payload']['score']

