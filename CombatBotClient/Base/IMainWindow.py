import tkinter as tk
from multiprocessing import Process, Queue


class IMainWindow:
    root: tk.Tk
    bot_ip: str
    bot_service: Process
    rec_q: Queue
    trn_q: Queue
