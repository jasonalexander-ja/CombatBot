from typing import Union, Any

import tkinter as tk
from tkinter import ttk

from sqlalchemy import column

from Base.IMainWindow import IMainWindow
from BotService import Worker as bs

from BotService.Messaging import RtnMessage


class ControlPanel:
    root: IMainWindow

    def send_msg(self, msg: bs.IMessage) -> None:
        if self.root.trn_q.empty():
            self.root.trn_q.put(msg)

    def forward(self) -> None:
        self.send_msg(bs.Move.FORWARD)
    
    def left(self) -> None:
        self.send_msg(bs.Move.LEFT)

    def right(self) -> None:
        self.send_msg(bs.Move.RIGHT)

    def backwards(self) -> None:
        self.send_msg(bs.Move.BACKWARDS)
    
    def released(self) -> None:
        self.send_msg(bs.Pause())
    
    def key_pressed(self, args: Any) -> None:
        key: str = args.char
        key = key.capitalize()
        if key == 'W':
            self.forward()
        elif key == 'A':
            self.left()
        elif key == 'D':
            self.right()
        elif key == 'S':
            self.backwards()
        elif key == ' ':
            self.released()
        
    def key_released(self, args: Any) -> None:
        self.released()

    def __init__(self, root: IMainWindow, frame: Union[ttk.Frame, tk.Frame]) -> None:
        self.root = root
        self.root_frame = frame
        
        self.root.root.bind('<KeyPress>', lambda a: self.key_pressed(a))
        self.root.root.bind('<KeyRelease>', lambda a: self.key_released(a))

        self.init_frames()
        self.init_buttons()

    def init_frames(self) -> None:
        self.main = ttk.Frame(self.root_frame)
        self.main.grid(row=0, column=0, sticky=tk.EW, padx=5)
        for i in range(0, 3):
            self.main.columnconfigure(i, weight=1)
        
        self.button_base = ttk.Frame(self.main)
        self.button_base.grid(row=0, column=0, columnspan=3)
        for i in range(3):
            self.button_base.columnconfigure(i, weight=3)
    
    def init_buttons(self) -> None:
        self.init_forward_button()
        self.init_left_button()
        self.init_right_button()
        self.init_back_button()
        self.init_helper_text()
        
    def init_forward_button(self) -> None:
        self.forward_button = ttk.Button(self.main, text="↑")
        self.forward_button.grid(
            row=0,
            column=0,
            columnspan=3,
            ipady=1
        )

    def init_left_button(self) -> None:
        self.left_button = ttk.Button(self.main, text="←")
        self.left_button.grid(
            row=1,
            column=0,
            sticky=tk.E,
            ipady=1
        )

    def init_right_button(self) -> None:
        self.right_button = ttk.Button(self.main, text="→")
        self.right_button.grid(
            row=1,
            column=2,
            sticky=tk.W,
            ipady=1
        )

    def init_back_button(self) -> None:
        self.back_button = ttk.Button(self.main, text="↓")
        self.back_button.grid(
            row=2,
            column=0,
            columnspan=3,
            ipady=1
        )
    
    def init_helper_text(self) -> None:
        text = "Use; W: forward, S: backwards, A: left, D: Right"
        self.helper_text = ttk.Label(self.main, text=text)
        self.helper_text.grid(
            row=3,
            column=0,
            columnspan=3,
            ipady=1
        )
