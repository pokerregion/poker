import jsonpickle
from jsonpickle.handlers import BaseHandler

from poker import Card, Combo
from poker.handhistory import _BaseStreet, _BaseHandHistory, _Player, _PlayerAction


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
        data.clear()
        data = {'name': obj.name, 'stack': float(obj.stack), 'seat': obj.seat}
        if obj.combo is not None:
            data['hand'] = self.context.flatten(obj.combo, reset=False)
        return data

    def restore(self, obj):
        raise NotImplementedError


@jsonpickle.handlers.register(_PlayerAction, base=True)
class PlayerActionsHandler(BaseHandler):

    def flatten(self, obj, data):
        data = {}
        data['name'] = obj.name
        data['action'] = obj.action.name
        if obj.amount is not None:
            data['amount'] = float(obj.amount)
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
        data['timestamp'] = str(obj.date)
        data['id'] = int(obj.ident)
        data['tablename'] = obj.table_name
        data['bb'] = float(obj.bb)
        data['sb'] = float(obj.sb)
        data['game'] = str(obj.game)
        data['gametype'] = str(obj.game_type)
        data['limit'] = str(obj.limit)
        data['max-players'] = obj.max_players
        data['hero'] = obj.hero.name
        data['button'] = obj.button.name
        data['showdown'] = str(obj.show_down)
        if obj.total_pot is not None:
            data['total_pot'] = float(obj.total_pot)
        if obj.rake is not None:
            data['rake'] = float(obj.rake)
        if obj.tournament_ident is not None:
            data['tournament-id'] = int(obj.tournament_ident)
        if obj.tournament_level is not None:
            data['tournament-level'] = str(obj.tournament_level)
        if obj.currency is not None:
            data['currency'] = str(obj.currency)
        if obj.extra is not None and obj.extra.get('money_type') is not None:
            data['moneytype'] = str(obj.extra.get('money_type'))
        data['players'] = [self.context.flatten(player, reset=True) for player in obj.players]
        data['preflop'] = {'actions': obj.preflop_actions}

        if obj.flop is not None:
            flop = {}
            if obj.flop.actions is not None:
                flop['actions'] = [self.context.flatten(action, reset=True) for action in obj.flop.actions]
            flop['cards'] = [self.context.flatten(card, reset=True) for card in obj.flop.cards]
            flop['flushdraw'] = obj.flop.has_flushdraw
            flop['gutshot'] = obj.flop.has_gutshot
            flop['paired'] = obj.flop.has_pair
            flop['straightdraw'] = obj.flop.has_straightdraw
            flop['monotone'] = obj.flop.is_monotone
            flop['triplet'] = obj.flop.is_triplet
            data['flop'] = flop

        if obj.turn is not None:
            turn = {}
            turn['card'] = self.context.flatten(obj.turn, reset=True)
            if obj.turn_actions is not None:
                turn['actions'] = obj.turn_actions
            data['turn'] = turn

        if obj.river is not None:
            river = {}
            river['card'] = self.context.flatten(obj.river, reset=True)
            if obj.river_actions is not None:
                river['actions'] = obj.river_actions
            data['river'] = river

        if obj.board is not None:
            board_ = [self.context.flatten(card, reset=True) for card in obj.board]
            data['board'] = board_
        data['winners'] = obj.winners
        return data

    def restore(self, obj):
        raise NotImplementedError


class JsonEncoder:

    def encode(self, obj):
        return jsonpickle.encode(obj)
