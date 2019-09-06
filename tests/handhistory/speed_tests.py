from timeit import timeit, repeat


results, single_results = [], []
for handnr in range(1, 5):
    #print "HAND{} Single run:".format(handnr),
    single_results.append(
        timeit('PokerStarsHandHistory(HAND{})'.format(handnr), number=100000,
               setup="from handhistory import PokerStarsHandHistory; "
                     "from stars_hands import HAND{}".format(handnr))
    )
    #print "HAND{} repeated run:".format(handnr),
    results.extend(repeat('PokerStarsHandHistory(HAND{})'.format(handnr), repeat=3, number=100000,
                   setup="from handhistory import PokerStarsHandHistory; "
                         "from stars_hands import HAND{}".format(handnr))
    )

print("Single results average: {}".format(sum(single_results) / len(single_results)))
print("Repeated results average: {}".format(sum(results) / len(results)))
