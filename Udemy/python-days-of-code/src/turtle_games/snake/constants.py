"""Define the constants for the Snake game."""

# Canvas
HEIGHT = 600
WIDTH = 600

# Scoreboard
SCORE_POSITION = (0, 260)
SCORE_MIN_X = -30
SCORE_MAX_X = 30
SCORE_MIN_Y = 260
SCORE_MAX_Y = 280
ALIGNMENT = "center"
FONT = ("Arial", 24, "normal")

# Snake
STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20

# Food
MAX_POS = 280
MIN_POS = -280
LEFT_START_BOUNDARY = -50
RIGHT_START_BOUNDARY = 10
UP_START_BOUNDARY = 20
DOWN_START_BOUNDARY = -20

# Directions
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0
