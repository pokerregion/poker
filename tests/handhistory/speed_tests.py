from timeit import timeit, repeat


results, single_results = [], []
for handnr in range(1, 5):
    #print "HAND%s Single run:" % handnr,
    single_results.append(timeit('PokerStarsHandHistory(HAND%s)' % handnr,
                   number=100000,
                   setup="from handhistory import PokerStarsHandHistory; from stars_hands import HAND%s" % handnr))

    #print "HAND%s repeated run:" % handnr,
    results.extend(repeat('PokerStarsHandHistory(HAND%s)' % handnr,
                   repeat=3,
                   number=100000,
                   setup="from handhistory import PokerStarsHandHistory; from stars_hands import HAND%s" % handnr))

print "Single results average: %s" % (sum(single_results) / len(single_results))
print "Repeated results average: %s" % (sum(results) / len(results))
