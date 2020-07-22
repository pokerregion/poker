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
        data['timestamp'] = str(obj.date)
        data['id'] = int(obj.ident)
        data['tablename'] = obj.table_name
        data['bb'] = float(obj.bb)
        data['sb'] = float(obj.sb)
        data['game'] = str(obj.game)
        data['gametype'] = str(obj.game_type)
        data['limit'] = str(obj.limit)
        data['max-players'] = obj.max_players
        data['hero'] = self.context.flatten(obj.hero, reset=False)
        data['button'] = self.context.flatten(obj.button, reset=False)
        if obj.rake is not None:
            data['rake'] = float(obj.rake)
        if obj.tournament_ident is not None:
            data['tournament-id'] = int(obj.tournament_ident)
        if obj.tournament_level is not None:
            data['tournament-level'] = str(obj.tournament_level)
        # todo: players

        if obj.currency is not None:
            data['currency'] = str(obj.currency)
        if obj.extra is not None and obj.extra.get('money_type') is not None:
            data['moneytype'] = str(obj.extra.get('money_type'))

        #todo preflop actions
        #todo: flop
        #todo: turn
        #todo: turn_actions
        #todo: river
        #todo: river_actions
        #todo: showdown (bool)
        data['board'] = [self.context.flatten(x, reset=False) for x in obj.board]
        #todo winners
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
