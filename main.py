#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import sys
import tkinter as TK
import time
from PIL import Image, ImageTk
import cv2
from pathlib import Path
import json

if os.name == "posix":
    sys.path.append('/home/cheng/Desktop/2023-01-14_Handheld_GUI')
from record_obj import Records
from InitFrame import InitFrame
from SettingFrame import SettingFrame
from LogFrame import LogFrame
from ViewFrame import ViewFrame
from RecordFrame import RecordFrame

class Application(TK.Tk):
    """
    A class to build main application. Inheritance of tkinter.Tk.
    Need instanced before calling .mainloop().
    example:
    app = Application()
    app.mainloop()

    ...

    Attributes:
        frame_names : dic
            the index and name of frames
        title_name : str
            title of the app window
        fullscreen : bool
            set the display mode(fullscreen)

    Methods:
        show_frame(cont):
            Show the certain frame in frames[].
        end_app():
            Ene entire application.
    """

    # 設定參數
    log: list
    setting_path: Path
    setting: dict

    # 顯示參數
    title_name: str
    frame_names = {
        "init": "首頁",
        "record": "錄製介面",
        "log": "系統紀錄",
        "setting": "系統設定",
        "check": "確認頁面",
        "view": "錄製紀錄"
    }
    frame_now = "init"
    button_rely = 0.8
    button_relheight = 0.2
    title_y = 1

    def __init__(self, title_text="手持式裝置", fullscreen=True):
        """
        Constructs all the necessary attributes for Application.

        Args:
            title_text : str, optional
                name of the application window.(default is "手持式裝置")
            fullscreen : bool, optional
                family name of the person.(default is False)
        """

        # 準備資料
        self.setting_path = Path("setting.json")
        self.get_setting()
        self.records = Records()
        self.field_id_now = self.setting["field_ids"][0]
        self.field_index_now = 0
        self.pool_id_now = self.setting["pool_ids"][0][0]
        self.pool_index_now = 0

        # 處理畫面
        TK.Tk.__init__(self)

        self.title_name = title_text
        if fullscreen:
            self.attributes('-fullscreen', True)
            print("fullscreen")
        else:
            self.geometry("540x360")

        container = TK.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.frames["init"] = InitFrame(container, self)
        self.frames["record"] = RecordFrame(container, self)
        self.frames["view"] = ViewFrame(container, self)
        self.frames["log"] = LogFrame(container, self)
        self.frames["setting"] = SettingFrame(container, self)

        for f in self.frames.values():
            f.grid(row=0, column=0, sticky="nsew")

        self.show_frame("init")
        pass

    def __del__(self):
        # 可能會有問題，不知道TK.quit()會不會呼叫__del__
        self.end_app()
        print("OBJ Application has been end")

    def show_frame(self, cont):
        """
        Bring the frame to the top of conatiner.

        Args:
            cont : str
                the index of frame to bring in frames[]
        """
        try:
            self.frames[self.frame_now].close_frame()
            if cont in self.frame_names:
                title_text = self.title_name + " - " + self.frame_names[cont]
            else:
                title_text = self.title_name
            self.title(title_text)
            # print(self.frames)
            self.frame_now = cont
            self.frames[cont].tkraise()
            self.frames[cont].open_frame()
        except Exception as e:
            print(e)
            print("frame switch err")
        

    def get_setting(self):
        """
        Get settings from setting.json.

        Args:
            None.

        Returns:
            None.
        """
        self.write_log("read setting")
        with open(self.setting_path, encoding="utf8") as f:
            self.setting = json.load(f)
        pass

    def save_setting(self):
        """
        Write settings to setting.json.

        Args:
            None.

        Returns:
            None.
        """
        self.write_log("save setting")
        with open(self.setting_path, "w", encoding="utf8") as f:
            json.dump(self.setting, f, indent=4, ensure_ascii=False)
        pass

    def write_log(self, log_str):
        """
        Write string to log.txt.

        Args:
            Texting for log.

        Returns:
            None.
        """
        with open('log.txt', 'a',encoding='utf-8') as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + log_str + '\r\n')
        pass

    def end_app(self, event=None):
        self.write_log("close system")
        print("program closing by main")
        try:
            self.frames[self.frame_now].close_frame()
        except Exception as e:
            print(e)
            print("frame close err")
            self.write_log("err when closing page")
        self.quit()


if __name__ == "__main__":
    intest=True
    app = Application("手持式裝置", fullscreen=True)
    app.mainloop()
    if os.name == "posix" and not intest:
        os.system("shutdown now -h")
    os._exit(0)
