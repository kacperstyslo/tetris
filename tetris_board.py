from os import get_terminal_size
from dataclasses import dataclass

import numpy as np


@dataclass
class TetrisBoard:
    """
    This class stores the properties of the playing field.
    """

    board_depth: int = 19
    board_width: int = 18
    top_padding: int = min(5, get_terminal_size().lines - board_depth - 5)
    left_padding: int = min(10, get_terminal_size().columns - (board_width * 3) - 5)
    play_field: np.array = np.zeros((board_depth, board_width))
    overlay_of_play_field: np.array = np.zeros((board_depth, board_width))
