from typing import Tuple, List, Dict
import socket as sc
import time

from .Messaging import *


MoveData = List[Tuple[List[int], int]]
Animations = Dict[str, List[Tuple[List[int], int]]]


MOVE_DATA: Dict[str, List[Tuple[List[int], int]]] = {
    "FORWARD": [
        ([90, 0, 0, 0, 0, 0, 0, 0], 1),
        ([0, 0, 0, 0, 0, 0, 0, 0], 1)
    ],
    "BACKWARDS": [
        ([90, 0, 0, 0, 0, 0, 0, 0], 1),
        ([0, 0, 0, 0, 0, 0, 0, 0], 1)
    ],
    "LEFT": [
        ([90, 0, 0, 0, 0, 0, 0, 0], 1),
        ([0, 0, 0, 0, 0, 0, 0, 0], 1)
    ],
    "RIGHT": [
        ([90, 0, 0, 0, 0, 0, 0, 0], 1),
        ([0, 0, 0, 0, 0, 0, 0, 0], 1)
    ]
}


def move(step: int, move: str, socket: sc.socket) -> None:
    moves = MOVE_DATA[move]
    if step >= len(moves):
        return
    (step_data, delay) = moves[step]
    socket.send(bytes(step_data))
    time.sleep(delay)



def forward(step: int, socket: sc.socket) -> None:
    move(step, "FORWARD", socket)


def backwards(step: int, socket: sc.socket) -> None:
    move(step, "BACKWARDS", socket)


def left(step: int, socket: sc.socket) -> None:
    move(step, "LEFT", socket)


def right(step: int, socket: sc.socket) -> None:
    move(step, "RIGHT", socket)
