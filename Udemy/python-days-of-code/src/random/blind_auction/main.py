"""Run a blind auction."""

import platform
from os import system

from blind_auction import (
    get_highest_bidder,
    print_start,
    take_turn,
)

print_start()

bids = {}

keep_bidding = True
while keep_bidding:
    bids.update(take_turn())

    more_bidders = input("Are there any other bidders? 'Y' or 'N' ").lower()
    if more_bidders == "n":
        keep_bidding = False

    if platform.system() == "Windows":
        system("cls")
    else:
        system("clear")

max_bidder, max_bid = get_highest_bidder(bids)
print(f"The winner is {max_bidder} with a bid of ${max_bid}.\n\n")
