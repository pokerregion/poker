import jsonpickle
from jsonpickle.handlers import BaseHandler

from poker import Card, Combo
from poker.handhistory import _BaseStreet, _BaseHandHistory, _Player


@jsonpickle.handlers.register(Card, base=True)
class CardHandler(BaseHandler):

    def flatten(self, obj, data):
        data = {'rank': obj.rank.val, 'suit': obj.suit.name}
        return data

    def restore(self, obj):
        raise NotImplementedError


@jsonpickle.handlers.register(Combo, base=True)
class ComboHandler(BaseHandler):

    def flatten(self, obj, data):
        data = {'1': self.context.flatten(obj.first, reset=False), '2': self.context.flatten(obj.second, reset=False)}
        return data

    def restore(self, obj):
        raise NotImplementedError


@jsonpickle.handlers.register(_Player, base=True)
class PlayerHandler(BaseHandler):

    def flatten(self, obj, data):
        data = {'name': obj.name, 'stack': float(obj.stack), 'seat': obj.seat}
        if obj.combo is not None:
            data['hand'] = self.context.flatten(obj.combo, reset=False)
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
        data['bb'] = float(obj.bb)
        data['sb'] = float(obj.sb)
        data['button'] = self.context.flatten(obj.button, reset=False)
        if obj.currency is not None:
            data['currency'] = str(obj.currency)
        data['timestamp'] = str(obj.date)
        #fixme: need to get moneytype
        #if obj.extra is not None:
        #    data.update(obj.extra)

        return data

    def restore(self, obj):
        raise NotImplementedError


class JsonEncoder:

    def __init__(self):
        jsonpickle.handlers.register(CardHandler)
        jsonpickle.handlers.register(StreetHandler)
        jsonpickle.handlers.register(HandHistoryHandler)
        jsonpickle.handlers.register(PlayerHandler)

    def encode(self, obj):
        return jsonpickle.encode(obj)
