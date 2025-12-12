"""Run the games module."""

from game import ResultEnum
from utils import get_game, print_game_options

print_game_options()
game = get_game()

game.setup_game()

while game.continue_playing:
    game.reset()
    game.start_playing()

    while game.result == ResultEnum.incomplete:
        game.play_round()

    game.output_result()
    game.update_win_loss_tally()
    game.ask_play_again()

game.output_final_tally()
