from timeit import timeit, repeat


results, single_results = [], []
for handnr in range(1, 5):
    single_results.append(
        timeit(
            f"PokerStarsHandHistory(HAND{handnr})",
            number=100000,
            setup="from poker.room.pokerstars import PokerStarsHandHistory; "
            f"from tests.handhistory.stars_hands import HAND{handnr}",
        )
    )
    results.extend(
        repeat(
            f"PokerStarsHandHistory(HAND{handnr})",
            repeat=3,
            number=100000,
            setup="from poker.room.pokerstars import PokerStarsHandHistory; "
            f"from tests.handhistory.stars_hands import HAND{handnr}",
        )
    )

print("Single results average:", sum(single_results) / len(single_results))
print("Repeated results average:", sum(results) / len(results))
