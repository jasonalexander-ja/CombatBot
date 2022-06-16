from multiprocessing import Queue
from typing import Union, Optional
import socket as sc
import time

from . import BotController as bc

from .Messaging import *


def connect(info: ConnectTo, out_q: Queue) -> Union[sc.socket, None]:
    try:
        clientSocket = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
        clientSocket.connect((info.ip, 8088))
        out_q.put(RtnMessage.SUCESS)
        return clientSocket
    except:
        out_q.put(RtnMessage.CONNECT_FAILED)
        return None


def handle_movement(
    move: Move, 
    mv_no: int, 
    out_q: Queue, 
    s: Optional[sc.socket]
) -> None:
    if s == None:
        x = 0
        # return
    try:
        if move is Move.FORWARD:
            print(f"Forward {mv_no}") # bc.forward(mv_no, s)
        elif move is Move.BACKWARDS:
            print(f"Backwards {mv_no}")
        elif move is Move.LEFT:
            print(f"Left {mv_no}")
        elif move is Move.RIGHT:
            print(f"Right {mv_no}")
    except:
        out_q.put(RtnMessage.COMMAND_SEND_FAILED)
    time.sleep(0.25)


def worker(in_q: Queue, out_q: Queue) -> None:
    command: Union[IMessage, None] = None
    new_command: Union[IMessage, None] = None
    command_step = 0
    socket: Optional[sc.socket] = None

    while True:
        if not in_q.empty() or command == None or isinstance(new_command, Pause): 
            new_command = in_q.get()
        if isinstance(new_command, Pause):
            continue
        if new_command != command:
            command, command_step = new_command, 0
        if isinstance(command, ConnectTo):
            socket, command = connect(command, out_q), None
        elif isinstance(command, Move):
            handle_movement(command, command_step, out_q, socket)
        elif isinstance(command, End):
            if isinstance(socket, sc.socket):
                socket.close()
            return
        command_step += 1
