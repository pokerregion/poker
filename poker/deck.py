import secrets

from .card import Card


class Deck:
    def __init__(self):
        self._cards = list(Card)
        self._drawn = []

    def shuffle(self):
        """Shuffles the deck."""
        # Algorithm taken from the Python standard library 3.12 Random.shuffle,
        # which is based on the Fisher-Yates shuffle.
        for i in range(len(self._cards) - 1, 0, -1):
            # pick an element in cards[:i+1] with which to exchange cards[i]
            j = secrets.randbelow(i + 1)
            self._cards[i], self._cards[j] = self._cards[j], self._cards[i]

    def __len__(self):
        return len(self._cards)

    def draw(self):
        """Draws a card from the top of the deck."""
        card = self._cards.pop()
        self._drawn.append(card)
        return card
