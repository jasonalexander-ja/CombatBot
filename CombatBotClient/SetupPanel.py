from typing import List, Union, Any
from enum import Enum
import time

import tkinter as tk
from tkinter import ttk

from serial.tools import list_ports
import serial

from Base.IMainWindow import IMainWindow

import BotService.Worker as bs
from BotService.Messaging import RtnMessage


SERIAL_WAIT_PERIOD = 0.3


def get_comports() -> List[str]:
    ports: List[str] = []
    for p in list_ports.comports():
        ports.append(p.device)
    return ports


class MsgSeverity(Enum):
    INFO = 1
    SUCCESS = 0
    WARNING = -1
    ERROR = -2


def write_serial(
    ser: serial.Serial, 
    msg: bytes, 
    wait: bool = False
) -> None:
    if wait:
        time.sleep(SERIAL_WAIT_PERIOD)
    ser.write(msg)


def write_serial_response(
    ser: serial.Serial, 
    msg: bytes, 
    wait: bool = False
) -> bytes:
    if wait:
        time.sleep(SERIAL_WAIT_PERIOD)
    ser.write(msg)
    return ser.readline()[:-2]


class SetupPanel:
    root: IMainWindow

    def verify_port(self) -> bool:
        port = self.selected_port.get()
        try:
            with serial.Serial(port, 115200, timeout=5) as ser:
                time.sleep(SERIAL_WAIT_PERIOD)
                ser.write(b'STAT\n')
                # ESP32 Likes to send random crap over Serial
                # So we need to sift through that 
                response = ser.readline()
                while response != b'\r\n' and response != b'':
                    if response.startswith(b'SETUP\r\n'):
                        return True
                    response = ser.readline()
                return False
        except:
            return False
    
    def fetch_network_info(self, ser: serial.Serial) -> None:
        ssid = write_serial_response(ser, b'GET_SSID\n', True)
        self.set_ssid.set(ssid.decode("utf-8"))
        
        password = write_serial_response(ser, b'GET_PSWD\n', True)
        self.set_pswd.set(password.decode("utf-8"))
        
        self.setup_disabled(False)
        self.change_msg("Port verified ", MsgSeverity.SUCCESS)

    def verify_port_get_info(self) -> None:
        if not self.verify_port():
            self.change_msg("Selected port did not respond as expected ", MsgSeverity.WARNING)
            return
        port = self.selected_port.get()
        try:
            with serial.Serial(port, 115200, timeout=5) as ser:
                self.fetch_network_info(ser)
        except:
            self.change_msg(
                "Failed to get information from the bot at this port ",
                MsgSeverity.WARNING
            )
    
    def set_network_details(self) -> None:
        port = self.selected_port.get()
        ssid = self.set_ssid.get()
        pswd = self.set_pswd.get()
        try:
            with serial.Serial(port, 115200, timeout=5) as ser:
                write_serial(ser, f"SET_SSID\n{ssid}\n".encode(), True)

                write_serial(ser, f"SET_PSWD\n{pswd}\n".encode(), True)
                self.change_msg("Network details updated ", MsgSeverity.SUCCESS)
        except:
            self.change_msg("Failed to communicate with the bot ", MsgSeverity.WARNING)
    
    def connect(self) -> bool:
        port = self.selected_port.get()
        with serial.Serial(port, 115200, timeout=15) as ser:
            response = write_serial_response(ser, b'CONNECT\n', True)
            if response != b'CONNECTED':
                self.change_msg("Error connecting to network ", MsgSeverity.WARNING)
                return False
            bot_ip = ser.readline().decode("utf-8")[:-2]
            self.root.bot_ip = bot_ip
            self.setup_disabled(True)
            self.change_msg(f"Connected at {self.root.bot_ip}", MsgSeverity.SUCCESS)
            return True

    def try_connect(self) -> None:
        try:
            if not self.connect():
                return
        except:
            self.change_msg("Failed to communicate with bot ", MsgSeverity.WARNING)
            return
        try:
            self.root.trn_q.put(bs.ConnectTo(self.root.bot_ip))
            response = self.root.rec_q.get()
            if response != RtnMessage.SUCESS:
                raise
        except:
            self.change_msg(
                f"Failed to connect to bot on given ip {self.root.bot_ip} ", 
                MsgSeverity.WARNING
            )
    
    def setup_disabled(self, disabled: bool) -> None:
        state = tk.DISABLED if disabled else tk.NORMAL
        show = "*" if disabled else ""

        self.ssid_field.config(state=state)
        self.upload_button.config(state=state)
        self.connect_button.config(state=state)
        self.pswd_field.config(state=state, show=show)

    def __init__(self, root: Any, frame: Union[ttk.Frame, tk.Frame]) -> None:
        self.root = root
        self.root_frame = frame

        self.main = tk.LabelFrame(self.root_frame, text='Setup')
        self.main.grid(row=0, column=0, sticky=tk.EW, padx=5)
        for i in range(0, 3):
            self.main.columnconfigure(i, weight=1)
        self.add_ui_elems()

    def add_ui_elems(self) -> None:
        self.add_setup_msg()
        self.add_port_selector()
        self.add_ssid_entry()
        self.add_password_entry()
        self.add_action_buttons()

    def add_setup_msg(self) -> None:
        self.setup_msg = tk.StringVar()
        self.setup_msg.set("Select a port and verify")
        self.setup_msg_label = tk.Entry(
            self.main, 
            textvariable=self.setup_msg,
            state='disabled',
            disabledbackground='#242424',
            disabledforeground='#206fe6'
        )
        self.setup_msg_label.grid(
            row=0, 
            column=0, 
            columnspan=3, 
            sticky=tk.W, 
            padx=10
        )

    def add_port_selector(self) -> None:
        self.port_frame = ttk.Frame(self.main)
        self.port_frame.grid(column=0, row=1, padx=10, pady=7, sticky=tk.W)

        self.port_label = ttk.Label(self.port_frame, text="Port")
        self.port_label.grid(column=0, row=0, sticky=tk.W)
        
        self.selected_port = tk.StringVar()
        self.port_cb = ttk.Combobox(self.port_frame, textvariable=self.selected_port)

        self.port_cb.config(values=get_comports())
        self.port_cb['state'] = 'readonly'
        self.port_cb.grid(column=0, row=1, sticky=tk.W)

    def add_ssid_entry(self) -> None:
        self.ssid_frame = ttk.Frame(self.main)
        self.ssid_frame.grid(column=1, row=1, padx=10, pady=7)

        self.ssid_label = ttk.Label(self.ssid_frame, text="SSID")
        self.ssid_label.grid(column=0, row=0, sticky=tk.W)
        
        self.set_ssid = tk.StringVar()
        self.ssid_field = ttk.Entry(self.ssid_frame, textvariable=self.set_ssid)
        self.ssid_field.config(state=tk.DISABLED)
        self.ssid_field.grid(column=0, row=1, sticky=tk.W)

    def add_password_entry(self) -> None:
        self.pswd_frame = ttk.Frame(self.main)
        self.pswd_frame.grid(column=2, row=1, padx=10, pady=7)

        self.password_label = ttk.Label(self.pswd_frame, text="Password")
        self.password_label.grid(column=0, row=0, sticky=tk.W)
        
        self.set_pswd = tk.StringVar()
        self.pswd_field = ttk.Entry(self.pswd_frame, textvariable=self.set_pswd)
        self.pswd_field.config(state=tk.DISABLED)
        self.pswd_field.grid(column=0, row=1, sticky=tk.W)


    def add_action_buttons(self) -> None:
        self.action_frame = ttk.Frame(self.main)
        self.action_frame.grid(column=0, row=2, columnspan=3)
        for i in range(4):
            self.action_frame.columnconfigure(i, weight=1)
        self.init_buttons()
    
    def init_buttons(self) -> None:
        self.init_refresh_button()
        self.init_verify_button()
        self.init_upload_button()
        self.init_connect_button()

    def init_refresh_button(self) -> None:
        self.refresh_button = ttk.Button(
            self.action_frame, 
            text="Refresh Ports", 
            command=lambda: self.port_cb.config(values=get_comports())
        )
        self.refresh_button.grid(column=0, row=0, sticky=tk.E)

    def init_verify_button(self) -> None:
        self.verify_button = ttk.Button(
            self.action_frame, 
            text="Verify Port",
            command=lambda: self.verify_port_get_info()
        )
        self.verify_button.grid(column=1, row=0, sticky=tk.E)

    def init_upload_button(self) -> None:
        self.upload_button = ttk.Button(
            self.action_frame, 
            text="Update Network Details",
            command=lambda: self.set_network_details(),
            state=tk.DISABLED
        )
        self.upload_button.grid(column=2, row=0, sticky=tk.E)

    def init_connect_button(self) -> None:
        self.connect_button = ttk.Button(
            self.action_frame, 
            text="Connect",
            command=lambda: self.try_connect(),
            state=tk.DISABLED
        )
        self.connect_button.grid(column=3, row=0, sticky=tk.E)
    
    def change_msg(self, msg: str, severity: MsgSeverity = MsgSeverity.INFO) -> None:
        color = ''
        if severity == MsgSeverity.INFO:
            color = '#206fe6'
        if severity == MsgSeverity.SUCCESS:
            color = 'green'
        if severity == MsgSeverity.WARNING:
            color = 'yellow'
        if severity == MsgSeverity.ERROR:
            color = 'red'
        self.setup_msg.set(msg)
        self.setup_msg_label.config(disabledforeground=color)
