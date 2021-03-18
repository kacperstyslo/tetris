from typing import List

import numpy as np


class TetrisFigures:
    """
    This class is responsible for generating and delivering figures to other objects.
    """

    def __init__(self) -> None:
        self.figures: list = []

    def __call__(self) -> List[np.ndarray]:
        return list(self.tetris_figure_factory())

    def tetris_figure_factory(self) -> List[np.ndarray]:
        """
        Generating all shapes figures.
        """
        self.figures.append(np.array([(1, 1, 1, 1)]))
        self.figures.append(np.array([(1, 0, 0), (1, 0, 0), (1, 1, 0)]))
        self.figures.append(np.array([(0, 1, 0), (0, 1, 0), (1, 1, 0)]))
        self.figures.append(np.array([(0, 1, 0), (1, 1, 0), (1, 0, 0)]))
        self.figures.append(np.array([(1, 1, 0), (1, 1, 0)]))
        return self.figures
