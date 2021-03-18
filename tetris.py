#!/usr/bin/env python3

import os
import time
import curses
import random
from queue import Queue
from threading import Thread, Timer

import numpy as np

from tetris_figures import TetrisFigures
from tetris_board import TetrisBoard
from tetris_move_figures import TetrisMoveFigures


class Tetris:
    """
    This class stores the main game logic.
    """

    def __init__(self) -> None:
        self.tetris_board_properties = TetrisBoard()
        self.move_figure = TetrisMoveFigures(self.tetris_board_properties)
        self.position: list = [0, int(self.tetris_board_properties.board_width / 2) - 1]
        self.random_figure: np.array = random.choice(TetrisFigures().__call__())
        self.full_lines: list = []
        self.pressed_key_dict: dict = {
            65: "a",
            97: "A",
            68: "d",
            100: "D",
            83: "s",
            115: "S",
            87: "w",
            119: "W",
        }
        self.q: Queue = Queue()
        self.exit_game: bool = False

    def __call__(self) -> None:
        if os.name == "nt":
            curses.wrapper(lambda _: time.sleep(0.1))
            curses.wrapper(self.main_tetris)
        quit()

    def main_tetris(self, tetris_main_window) -> None:
        """
        Method with the main logic of the game.
        """
        tetris_main_window.clear()
        tetris_main_window.nodelay(1)
        curses.curs_set(0)
        last_position_of_the_playing_field: bool = False
        refreshed_tetris_objects = Tetris()
        falling_objects_thread = Thread(target=self.falling_objects, args=[self.q])
        falling_objects_thread.start()

        while True:
            self.draw_points_and_figures(
                refreshed_tetris_objects=refreshed_tetris_objects,
                tetris_main_window=tetris_main_window,
            )
            if self.full_lines:
                time.sleep(1)
                self.iterating_over_full_lines(tetris_main_window)

            pressed_key = tetris_main_window.getch()
            if pressed_key == 27 or pressed_key == 81 or pressed_key == 113:
                self.exit_game = True
                break
            self.call_correct_method_for_figure_movement(
                refreshed_tetris_objects=refreshed_tetris_objects,
                pressed_key=pressed_key,
                last_position_of_the_playing_field=last_position_of_the_playing_field,
            )

            if not self.q.empty():
                self.q.get()
                if self.move_figure.down(refreshed_tetris_objects):
                    refreshed_tetris_objects.position[0] += 1
                else:
                    last_position_of_the_playing_field = True

            if last_position_of_the_playing_field:
                print("\a")
                tm = Timer(
                    1.5,
                    self.clear_window,
                    args=[tetris_main_window, 5 + self.tetris_board_properties.board_depth + 1],
                )
                tm.start()
                last_position_of_the_playing_field = False
                self.tetris_board_properties.play_field = np.logical_or(
                    self.tetris_board_properties.play_field,
                    self.tetris_board_properties.overlay_of_play_field,
                )
                refreshed_tetris_objects = Tetris()
                if self.move_figure.detected_collision(refreshed_tetris_objects):
                    self.exit_game = True
                    break
                tetris_main_window.refresh()

    def iterating_over_full_lines(self, tetris_main_window) -> None:
        for i in self.full_lines:
            before = self.tetris_board_properties.play_field[0:i]
            after = self.tetris_board_properties.play_field[
                i + 1 : self.tetris_board_properties.board_width
            ]
            self.tetris_board_properties.play_field = np.append(
                np.zeros((1, self.tetris_board_properties.board_width)), before, axis=0
            )
            self.tetris_board_properties.play_field = np.append(
                self.tetris_board_properties.play_field, after, axis=0
            )
            tetris_main_window.move(i + 5, 0)
            tetris_main_window.clrtoeol()

    def draw_points_and_figures(self, refreshed_tetris_objects, tetris_main_window) -> None:
        """
        Drawing points and shape on the board.
        """
        self.tetris_board_properties.overlay_of_play_field[
            refreshed_tetris_objects.position[0] : refreshed_tetris_objects.position[0]
            + refreshed_tetris_objects.random_figure.shape[0],
            refreshed_tetris_objects.position[1] : refreshed_tetris_objects.position[1]
            + refreshed_tetris_objects.random_figure.shape[1],
        ] = refreshed_tetris_objects.random_figure
        for i in range(0, self.tetris_board_properties.board_depth):
            if (
                np.count_nonzero(self.tetris_board_properties.play_field[i])
                == self.tetris_board_properties.board_width
            ):
                tetris_main_window.addstr(
                    i + self.tetris_board_properties.top_padding,
                    self.tetris_board_properties.left_padding - 3,
                    ">>>>|" + ("*" * self.tetris_board_properties.board_width) + "|<<<<",
                )
                self.full_lines.append(i)
            else:
                tetris_main_window.addch(
                    i + self.tetris_board_properties.top_padding,
                    self.tetris_board_properties.left_padding,
                    ord("*"),
                )
                for j in range(0, self.tetris_board_properties.board_width):
                    tetris_main_window.addch(
                        i + self.tetris_board_properties.top_padding,
                        self.tetris_board_properties.left_padding + 1 + j,
                        ord("*")
                        if self.tetris_board_properties.play_field[i, j]
                        + self.tetris_board_properties.overlay_of_play_field[i, j]
                        else ord(" "),
                    )
                tetris_main_window.addstr(
                    i + self.tetris_board_properties.top_padding,
                    self.tetris_board_properties.left_padding
                    + 1
                    + self.tetris_board_properties.board_width,
                    "* ",
                )
            tetris_main_window.addstr(
                self.tetris_board_properties.board_depth + self.tetris_board_properties.top_padding,
                self.tetris_board_properties.left_padding,
                ("*" * (self.tetris_board_properties.board_width + 2)),
            )
        tetris_main_window.refresh()

    def call_correct_method_for_figure_movement(self, **kwargs) -> None:
        """
        When the user presses one of the figure control keys, this method will select the
        appropriate function.
        """
        refreshed_tetris_objects = kwargs["refreshed_tetris_objects"]
        pressed_key = kwargs["pressed_key"]
        if (
            self.pressed_key_dict.get(pressed_key) == "a"
            or self.pressed_key_dict.get(pressed_key) == "A"
        ):
            if self.move_figure.left(refreshed_tetris_objects):
                refreshed_tetris_objects.position[1] -= 1
        elif (
            self.pressed_key_dict.get(pressed_key) == "d"
            or self.pressed_key_dict.get(pressed_key) == "D"
        ):
            if self.move_figure.right(refreshed_tetris_objects):
                refreshed_tetris_objects.position[1] += 1
        elif (
            self.pressed_key_dict.get(pressed_key) == "s"
            or self.pressed_key_dict.get(pressed_key) == "S"
        ):
            if self.move_figure.down(refreshed_tetris_objects):
                refreshed_tetris_objects.random_figure = np.rot90(
                    refreshed_tetris_objects.random_figure, -1
                )
        elif (
            self.pressed_key_dict.get(pressed_key) == "w"
            or self.pressed_key_dict.get(pressed_key) == "W"
        ):
            if self.move_figure.up(refreshed_tetris_objects):
                refreshed_tetris_objects.random_figure = np.rot90(
                    refreshed_tetris_objects.random_figure
                )

    @staticmethod
    def clear_window(tetris_main_window, position: int) -> None:
        tetris_main_window.move(position, 0)
        tetris_main_window.clrtoeol()

    @staticmethod
    def say_goodbye() -> None:
        print("Goodbye!")
        quit()

    def falling_objects(self, q: Queue) -> None:
        """
        The method responsible for falling shapes.
        """
        while True:
            if self.exit_game:
                self.say_goodbye()
            time.sleep(0.25)
            q.put(True)


if __name__ == "__main__":
    Tetris().__call__()
