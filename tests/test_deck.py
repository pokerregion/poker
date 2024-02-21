from poker import Card, Deck


def test_initial_state():
    deck = Deck()
    assert len(deck) == 52
    assert deck._drawn == []
    assert deck._cards == list(Card)


def test_draw():
    deck = Deck()
    card = deck.draw()
    assert len(deck) == 51
    assert card not in deck._cards
    assert deck._drawn == [card]


def test_shuffle():
    deck = Deck()
    deck2 = Deck()
    assert deck._cards == deck2._cards

    deck3 = Deck()
    deck3.shuffle()
    assert deck._cards != deck3._cards
    assert deck2._cards != deck3._cards
