from timeit import timeit, repeat


for handnr in range(1, 5):
    print "HAND%s Single run:" % handnr,
    print timeit('PokerStarsHand(HAND%s)' % handnr,
                 number=10000,
                 setup="from handparser import PokerStarsHand; from test_data import HAND%s" % handnr)

    print "HAND%s repeated run:" % handnr,
    print repeat('PokerStarsHand(HAND%s)' % handnr,
                 repeat=5,
                 number=10000,
                 setup="from handparser import PokerStarsHand; from test_data import HAND%s" % handnr)

