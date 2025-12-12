"""Play blackjack."""

from blackjack import Blackjack

continue_playing = "y"
while continue_playing == "y":
    game = Blackjack()

    if not game.user_dealt_21():
        take_turn = True
        while take_turn:
            take_turn = game.take_turn()

    game.play_dealer_hand()
    game.output_result()

    continue_playing = input("\n\nWould you like to play again? 'y' or 'n'? ")
    while continue_playing not in ["y", "n"]:
        continue_playing = input(
            "Invalid input! Would you like to play again? 'y' or 'n'? "
        )
