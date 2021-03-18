import numpy as np


class TetrisMoveFigures:
    """
    A class that contains all the methods responsible for moving figures.
    """

    def __init__(self, board) -> None:
        self.tetris_board_properties = board

    def detected_collision(self, refreshed_tetris_objects) -> bool:
        self.tetris_board_properties.overlay_of_play_field = np.zeros(
            self.tetris_board_properties.play_field.shape
        )
        self.tetris_board_properties.overlay_of_play_field[
            refreshed_tetris_objects.position[0] : refreshed_tetris_objects.position[0]
            + refreshed_tetris_objects.random_figure.shape[0],
            refreshed_tetris_objects.position[1] : refreshed_tetris_objects.position[1]
            + refreshed_tetris_objects.random_figure.shape[1],
        ] = refreshed_tetris_objects.random_figure
        return (
            np.count_nonzero(
                self.tetris_board_properties.overlay_of_play_field
                * self.tetris_board_properties.play_field
            )
        ) > 0

    def left(self, refreshed_tetris_objects) -> bool:
        if (refreshed_tetris_objects.position[1] - 1) < 0:
            return False
        else:
            self.tetris_board_properties.overlay_of_play_field = np.zeros(
                self.tetris_board_properties.play_field.shape
            )
            self.tetris_board_properties.overlay_of_play_field[
                refreshed_tetris_objects.position[0] : refreshed_tetris_objects.position[0]
                + refreshed_tetris_objects.random_figure.shape[0],
                refreshed_tetris_objects.position[1]
                - 1 : refreshed_tetris_objects.position[1]
                - 1
                + refreshed_tetris_objects.random_figure.shape[1],
            ] = refreshed_tetris_objects.random_figure
            return (
                np.count_nonzero(
                    self.tetris_board_properties.overlay_of_play_field
                    * self.tetris_board_properties.play_field
                )
            ) == 0

    def right(self, refreshed_tetris_objects) -> bool:
        if (
            refreshed_tetris_objects.position[1]
            + 1
            + refreshed_tetris_objects.random_figure.shape[1]
        ) > self.tetris_board_properties.board_width:
            return False
        else:
            self.tetris_board_properties.overlay_of_play_field = np.zeros(
                self.tetris_board_properties.play_field.shape
            )
            self.tetris_board_properties.overlay_of_play_field[
                refreshed_tetris_objects.position[0] : refreshed_tetris_objects.position[0]
                + refreshed_tetris_objects.random_figure.shape[0],
                refreshed_tetris_objects.position[1]
                + 1 : refreshed_tetris_objects.position[1]
                + 1
                + refreshed_tetris_objects.random_figure.shape[1],
            ] = refreshed_tetris_objects.random_figure
            return (
                np.count_nonzero(
                    self.tetris_board_properties.overlay_of_play_field
                    * self.tetris_board_properties.play_field
                )
            ) == 0

    def down(self, refreshed_tetris_objects) -> bool:
        if (
            refreshed_tetris_objects.position[0]
            + 1
            + refreshed_tetris_objects.random_figure.shape[0]
        ) > self.tetris_board_properties.board_depth:
            return False
        else:
            self.tetris_board_properties.overlay_of_play_field = np.zeros(
                (self.tetris_board_properties.board_depth, self.tetris_board_properties.board_width)
            )
            self.tetris_board_properties.overlay_of_play_field[
                refreshed_tetris_objects.position[0]
                + 1 : refreshed_tetris_objects.position[0]
                + 1
                + refreshed_tetris_objects.random_figure.shape[0],
                refreshed_tetris_objects.position[1] : refreshed_tetris_objects.position[1]
                + refreshed_tetris_objects.random_figure.shape[1],
            ] = refreshed_tetris_objects.random_figure
            return (
                np.count_nonzero(
                    self.tetris_board_properties.overlay_of_play_field
                    * self.tetris_board_properties.play_field
                )
            ) == 0

    def up(self, refreshed_tetris_objects) -> bool:
        rot_mat = np.rot90(refreshed_tetris_objects.random_figure)
        if (
            (refreshed_tetris_objects.position[0] + rot_mat.shape[0])
            > self.tetris_board_properties.board_depth
        ) or (
            (refreshed_tetris_objects.position[1] + rot_mat.shape[1])
            > self.tetris_board_properties.board_width
        ):
            return False
        else:
            self.tetris_board_properties.overlay_of_play_field = np.zeros(
                (self.tetris_board_properties.board_depth, self.tetris_board_properties.board_width)
            )
            self.tetris_board_properties.overlay_of_play_field[
                refreshed_tetris_objects.position[0] : refreshed_tetris_objects.position[0]
                + rot_mat.shape[0],
                refreshed_tetris_objects.position[1] : refreshed_tetris_objects.position[1]
                + rot_mat.shape[1],
            ] = rot_mat
            return (
                np.count_nonzero(
                    self.tetris_board_properties.overlay_of_play_field
                    * self.tetris_board_properties.play_field
                )
            ) == 0
