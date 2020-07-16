import jsonpickle
from jsonpickle.handlers import BaseHandler

from poker import Card
from poker.handhistory import _BaseStreet, _BaseHandHistory


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
        if obj.actions is not None:
            data['actions'] = [self.context.flatten(action, reset=False) for action in obj.actions]
        if obj.cards is not None:
            data['cards'] = [self.context.flatten(x, reset=False) for x in obj.cards]
        return data

    def restore(self, obj):
        raise NotImplementedError

@jsonpickle.handlers.register(_BaseHandHistory, base=True)
class HandHistoryHandler(BaseHandler):

    def flatten(self, obj, data):
        data = {}
        # TODO: implement all the toplevel objects of handhistory
        data['board'] = [self.context.flatten(x, reset=False) for x in obj.board]
        return data

    def restore(self, obj):
        raise NotImplementedError

class JsonEncoder:

    def __init__(self):
        jsonpickle.handlers.register(CardHandler)
        jsonpickle.handlers.register(StreetHandler)
        jsonpickle.handlers.register(HandHistoryHandler)

    def encode(self, obj):
        return jsonpickle.encode(obj)
