import jsonpickle
from jsonpickle.handlers import BaseHandler

from poker import Card, Combo
from poker.handhistory import _BaseStreet, _BaseHandHistory, _Player


#TODO: Create test case!!

@jsonpickle.handlers.register(Card, base=True)
class CardHandler(BaseHandler):

    def flatten(self, obj, data):
        data = {}
        data['rank'] = obj.rank.val
        data['suit'] = obj.suit.name
        return data

    def restore(self, obj):
        raise NotImplementedError


@jsonpickle.handlers.register(Combo, base=True)
class ComboHandler(BaseHandler):

    def flatten(self, obj, data):
        data = {}
        data['1'] = self.context.flatten(obj.first, reset=False)
        data['2'] = self.context.flatten(obj.second, reset=False)
        return data

    def restore(self, obj):
        raise NotImplementedError


@jsonpickle.handlers.register(_Player, base=True)
class PlayerHandler(BaseHandler):

    def flatten(self, obj, data):
        data = {}
        # TODO: implement player encoding
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
