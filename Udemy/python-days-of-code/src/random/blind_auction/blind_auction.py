"""Day 9. Define functions to perform a blind auction."""

from art import logo


def print_start():
    """Print the welcome message."""
    print(logo)
    print("\nWelcome to the secret auction program!\n")


def take_turn():
    """Take a turn bidding."""
    name = get_name()
    bid = get_bid()
    return {name: bid}


def get_name():
    """Ask user for their name."""
    return input("What is your name? ")


def get_bid():
    """Get the bid from a user."""
    bid = "-1"  # default value to ask for input
    while not bid.isdigit() or int(bid) < 0:
        bid = input("What is your bid? $")

    return int(bid)


def get_highest_bidder(bids: dict[str:int]) -> tuple[str, int]:
    """Determine the highest bid."""
    max_bid = -1
    max_bidder = ""
    for key, value in bids.items():
        if value > max_bid:
            max_bid = value
            max_bidder = key

    return (max_bidder, max_bid)
