from tkinter import *
from multiprocessing import Process, Queue

from SetupPanel import *
from ControlPanel import *
from Base.IMainWindow import IMainWindow

import BotService.Worker as bs
from BotService.Worker import worker


class MainWindow(IMainWindow):

    def __init__(self) -> None:

        self.root = Tk()
        self.root.geometry("680x400")
        self.root.wm_title("Battle Bot Controller")
        self.root.resizable(False, False)

        self.root.columnconfigure(0, weight=1)

        self.init_all()

    def init_all(self) -> None:
        self.init_top_panel()
        self.init_bottom_panel()
        self.init_process()

    def init_top_panel(self) -> None:
        self.top_panel = ttk.Frame(self.root)
        self.top_panel.grid(row=0, column=0, sticky=tk.EW, padx=5, pady=5)
        self.top_panel.columnconfigure(0, weight=1)

        self.control_panel = ControlPanel(self, self.top_panel)


    def init_bottom_panel(self) -> None:
        self.bottom_panel = ttk.Frame(self.root)
        self.bottom_panel.grid(row=1, column=0, sticky=tk.EW, padx=5, pady=5)
        self.bottom_panel.columnconfigure(0, weight=1)

        self.setup_panel = SetupPanel(self, self.bottom_panel)

    def init_process(self) -> None:
        self.rec_q = Queue()
        self.trn_q = Queue()
        self.bot_service = Process(target=worker, args=(self.trn_q, self.rec_q, ))

        self.bot_ip = ''

    def start(self) -> None:
        self.bot_service.start()
        self.root.mainloop()
        self.trn_q.put(bs.End())
        self.bot_service.join()
