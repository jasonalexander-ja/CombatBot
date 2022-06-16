from enum import Enum


class IMessage:
    pass


class End(IMessage):
    def __init__(self) -> None:
        super().__init__()


class ConnectTo(IMessage):
    ip: str

    def __init__(self, ip: str) -> None:
        self.ip = ip


class Move(IMessage, Enum):
    FORWARD = 0
    BACKWARDS = 1
    LEFT = 2
    RIGHT = 3


class Pause(IMessage):
    def __init__(self) -> None:
        super().__init__()


class RtnMessage(Enum):
    SUCESS = 0
    CONNECT_FAILED = -1
    COMMAND_SEND_FAILED = -1
