from blind_auction import get_highest_bidder


def test_get_highest_bidder():
    assert get_highest_bidder({"James": 10, "Lily": 100, "Harry": 52}) == ("Lily", 100)
