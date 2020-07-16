import jsonpickle
from jsonpickle.handlers import BaseHandler

from poker import Card
from poker.handhistory import _BaseStreet


#TODO: Create test case!!

@jsonpickle.handlers.register(Card, base=True)
class CardHandler(BaseHandler):

    def flatten(self, obj, data):
        print(obj.__getattribute__('suit'))
        data = {}
        data['rank'] = obj.rank.val
        data['suit'] = obj.suit.name
        return data

    def restore(self, obj):
        raise NotImplementedError

@jsonpickle.handlers.register(_BaseStreet, base=True)
class StreetHandler(BaseHandler):

    def flatten(self, obj, data):
        data = {}
        if obj.cards is not None:
            cards = [self.context.flatten(x, reset=False) for x in obj.cards]
            data['cards'] = cards
        return data

    def restore(self, obj):
        raise NotImplementedError


class JsonEncoder:

    def __init__(self):
        jsonpickle.handlers.register(CardHandler)
        jsonpickle.handlers.register(StreetHandler)

    def encode(self, obj):
        return jsonpickle.encode(obj)
