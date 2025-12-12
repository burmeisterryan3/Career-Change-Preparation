from hangman import Hangman

continue_playing = "y"
print_logo = True

while continue_playing == "y":
    h = Hangman(print_logo)

    while not h.game_over():
        h.take_turn()

    h.print_final_game_status()

    continue_playing = input("Want to play again? Type 'y' or 'n'\n")
    if continue_playing == "y":
        print("\nRematch accepted! ... You're going down.")
        print_logo = False
