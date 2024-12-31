#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import tkinter as TK
import time
from PIL import Image, ImageTk
import cv2
from pathlib import Path
import json


class InitFrame(TK.Frame):
    """
    Inheritance of tkinter.frame. The first page(frame) of Application.

    Attributes:
        controller : TK.Tk
            the Tk of frames, which means Application at here.
        parent : TK.Frame
            the contain of frame in Application.

    Method:
        update_clock():
            Update the clock label on this frame.
        set_button():
            Set button on screen to keyboard. Be called when show this frame.

    """

    def __init__(self, parent, controller):
        """
        Constructs all the necessary attributes for Application and open the camera.

        Args:
            parents : tkinter.Frame
                The frame to grid.
            controller : tkinter.Tk
                The Tk to work.
        """

        # 初始化Frame
        TK.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        # 繪製頁面
        line_sapcing = 40
        font_size = 15

        page_name_label = TK.Label(self, text="首頁").place(relx=0.0, y=controller.title_y, relwidth=1.0)

        self.device_name_label = TK.Label(self, text=controller.setting["device_name"], font=('Helvetica', 23))
        self.device_name_label.place(relx=0.0, rely=0.3, relwidth=1.0)
        self.clock_label = TK.Label(self, text="0000-00-00 00:00:00", font=('Helvetica', 16))
        self.clock_label.place(relx=0.0, rely=0.5, relwidth=1.0)
        self.update_clock()

        self.button_1 = TK.Button(self, text="開始錄製作業", command=lambda: controller.show_frame("record"), font=("Arial", font_size))
        self.button_1.place(relx=0.0, rely=controller.button_rely, relheight=controller.button_relheight, relwidth=0.2)
        self.button_2 = TK.Button(self, text="顯示系統紀錄", command=lambda: controller.show_frame("log"), font=("Arial", font_size))
        self.button_2.place(relx=0.2, rely=controller.button_rely, relheight=controller.button_relheight, relwidth=0.2)
        self.button_3 = TK.Button(self, text="系統設定", command=lambda: controller.show_frame("setting"), font=("Arial", font_size))
        self.button_3.place(relx=0.4, rely=controller.button_rely, relheight=controller.button_relheight, relwidth=0.2)
        self.button_4 = TK.Button(self, text="錄製紀錄", command=lambda: controller.show_frame("view"), font=("Arial", font_size))
        self.button_4.place(relx=0.6, rely=controller.button_rely, relheight=controller.button_relheight, relwidth=0.2)
        self.button_5 = TK.Button(self, text="結束系統", command=controller.end_app, font=("Arial", font_size))
        self.button_5.place(relx=0.8, rely=controller.button_rely, relheight=controller.button_relheight, relwidth=0.2)
        pass

    def open_frame(self):
        """
        abcd

        Args:
            None

        Returns:
            None
        """
        print("open InitFrame")
        self.update_clock()
        pass

    def close_frame(self):
        """
        """
        print("close InitFrame")
        pass

    def update_clock(self):
        """
        Update the time text in init frame.

        Args:
            None

        Returns:
            None
        """

        # print("update_clock")
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        self.clock_label.configure(text=now)
        if self.controller.frame_now == "init":
            self.controller.after(1000, self.update_clock)
