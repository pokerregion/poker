import jsonpickle
from jsonpickle.handlers import BaseHandler
from poker.handhistory import IStreet

from poker import Card

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

CardHandler.handles(Card)

@jsonpickle.handlers.register(IStreet, base=True)
class StreetHandler(BaseHandler):

    def flatten(self, obj, data):
        data = {}
        #Todo: implement like this
        if obj.cards is not None:
            cards = [self.context.flatten(x, reset=False) for x in obj.cards]
            data['cards'] = cards
        return data

    def restore(self, obj):
        raise NotImplementedError
