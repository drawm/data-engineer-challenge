from entities.Card import Card
from processors.event_processor import EventProcessor
from storage import Storage


# def _new_card(old_card: Card, new_card: Card, storage=Storage()):
#     if old_card.metadata.event_at > new_card.metadata.event_at:
#         # Event is out of date, don't process it
#         pass
#
#     storage.card.insert(new_card)
#     return False

def _update_card(old_card: Card, new_card: Card, storage=Storage()):
    if old_card.metadata.event_at > new_card.metadata.event_at:
        # Event is out of date, don't process it
        return False

    storage.card.update(new_card)
    return False


class CardProcessor(EventProcessor):
    """
    A simple `if` will do for this challenge, but a full schema validation would be better
    """

    def validate_schema(self, data: dict) -> bool:
        return data['metadata'] and data.get('payload').get('user_id')

    def process(self, data: dict) -> bool:
        print('processing card event')
        card = Card(data['payload'], data['metadata'])
        storage = Storage()

        # During card creation, don't override existing card
        current_card = storage.card.get_by_id(card.id)

        # No card in db, just push the one you have
        if not current_card:
            return storage.card.insert(card)

        return _update_card(current_card, card, storage)

        # return _new_card(current_card, card, storage)
