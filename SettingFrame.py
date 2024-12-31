#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import tkinter as TK
import time
from PIL import Image, ImageTk
import cv2
from pathlib import Path
import json


class SettingFrame(TK.Frame):
    """
    Inheritance of tkinter.frame. The setting page(frame) of Application, which can set options of app.

    Attributes:
        controller : TK.Tk
            the Tk of frames, which means Application at here.
        parent : TK.Frame
            the contain of frame in Application.

    Method:
        set_button():
            Set button on screen to keyboard. Be called when show this frame.

    """

    def __init__(self, parent, controller):

        # 初始化Frame
        TK.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        # 繪製頁面
        # 繪製標題
        page_name_label = TK.Label(self, text="系統設定").place(relx=0.0, y=controller.title_y, relwidth=1.0)

        # 繪製檢查格
        line_sapcing = 50
        font_size=30
        self.checkboxes = {}
        self.checkboxes["upload_when_recording"] = TK.BooleanVar()
        Cb = TK.Checkbutton(self, text="錄影結束後上傳", variable=self.checkboxes["upload_when_recording"], font=("Arial", font_size))
        Cb.place(relx=0.0, y=line_sapcing * 2, relwidth=1.0)
        self.checkboxes["delete_after_upload"] = TK.BooleanVar()
        Cb = TK.Checkbutton(self, text="上傳後刪除本地檔案", variable=self.checkboxes["delete_after_upload"], font=("Arial", font_size))
        Cb.place(relx=0.0, y=line_sapcing * 3, relwidth=1.0)

        # 繪製按鈕
        font_size = 15
        self.button_4 = TK.Button(self, text="回復預設", command=self.set_to_default, font=("Arial", font_size))
        self.button_4.place(relx=0.6, rely=controller.button_rely, relheight=controller.button_relheight, relwidth=0.2)
        self.button_5 = TK.Button(self, text="回首頁", command=lambda: controller.show_frame("init"), font=("Arial", font_size))
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
        self.checkboxes["upload_when_recording"].set(self.controller.setting["upload_when_recording"])
        self.checkboxes["delete_after_upload"].set(self.controller.setting["delete_after_upload"])
        print("open SettingFrame")
        pass

    def close_frame(self):
        """
        """
        self.controller.setting["upload_when_recording"] = self.checkboxes["upload_when_recording"].get()
        self.controller.setting["delete_after_upload"] = self.checkboxes["delete_after_upload"].get()
        print(f"after get_chosen: {self.controller.setting}")
        self.controller.save_setting()
        print("close SettingFrame")
        pass

    def get_chosen(self):
        # controller.setting[]=0
        for box in self.checkboxes.values():
            print(box.get())
        pass

    def set_to_default(self):
        self.checkboxes["upload_when_recording"].set(False)
        self.checkboxes["delete_after_upload"].set(False)
        pass