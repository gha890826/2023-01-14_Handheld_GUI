#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import tkinter as TK
import time
from PIL import Image, ImageTk
import cv2
from pathlib import Path
import json
import pyzed.sl as sl
from record_obj import Records


class LogFrame(TK.Frame):
    """
    Inheritance of tkinter.frame. The log page(frame) of Application, which can view log history.

    Attributes:
        controller : TK.Tk
            the Tk of frames, which means Application at here.
        parent : TK.Frame
            the contain of frame in Application.

    Method:
        set_button():
            Set button on screen to keyboard. Be called when show this frame.

    """
    log_in_line: list

    def __init__(self, parent, controller):

        # 初始化Frame
        TK.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.log_in_line = []

        # 繪製頁面

        line_sapcing = 40
        font_size = 15
        
        page_name_label = TK.Label(self, text="系統紀錄").place(relx=0.0, y=controller.title_y, relwidth=1.0)

        sb = TK.Scrollbar(self)
        sb.place(relx=0.9, y=20, relheight=0.7, relwidth=0.1)
        self.lb = TK.Listbox(self, yscrollcommand=sb.set)
        for i in self.log_in_line:
            self.lb.insert("end", i)
        self.lb.place(relx=0.0, y=20, relheight=0.7, relwidth=0.9)
        sb.config(command=self.lb.yview)

        button_3 = TK.Button(self, text="重新整理", command=self.reload, font=("Arial", font_size))
        button_3.place(relx=0.4, rely=controller.button_rely, relheight=controller.button_relheight, relwidth=0.2)
        button_5 = TK.Button(self, text="回首頁", command=lambda: self.controller.show_frame("init"), font=("Arial", font_size))
        button_5.place(relx=0.8, rely=controller.button_rely, relheight=controller.button_relheight, relwidth=0.2)
        pass

    def open_frame(self):
        print("open LogFrame")
        self.reload()
        pass

    def close_frame(self):
        """
        """
        print("close LogFrame")
        pass

    def read_log(self):
        """
        Read log from log.txt and save to self.log[] by 10 log in one page(subarray).

        Args:
            None.

        Returns:
            None.
        """
        self.controller.write_log("讀取log")
        with open('log.txt', 'r', encoding='utf-8') as f:
            self.log_in_line = []
            for line in f:
                self.log_in_line.append(line)

    def reload(self):
        """
        Reload log
        """
        self.read_log()
        self.lb.delete(0, TK.END)
        for i in self.log_in_line:
            self.lb.insert("end", i)
