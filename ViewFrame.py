#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import tkinter as TK
from tkinter import messagebox
import time
from PIL import Image, ImageTk
import cv2
from pathlib import Path
import json
import pyzed.sl as sl
from record_obj import Records


class ViewFrame(TK.Frame):
    """
    Inheritance of tkinter.frame. The view page(frame) of Application, which can view

    Attributes:
        controller : TK.Tk
            the Tk of frames, which means Application at here.
        parent : TK.Frame
            the contain of frame in Application.

    Method:
        set_button():
            Set button on screen to keyboard. Be called when show this frame.

    """

    index_now: int
    time_info: TK.Label
    field_info: TK.Label
    pool_info: TK.Label
    uploaded_info: TK.Label
    view_label: TK.Label

    def __init__(self, parent, controller):

        # 初始化Frame
        TK.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        page_name_label = TK.Label(self, text="錄製紀錄").place(relx=0.0, y=controller.title_y, relwidth=1.0)

        # 繪製左側資訊欄
        line_sapcing = 40
        font_size = 15
        time_label = TK.Label(self, text="時間: ", font=("Arial", font_size))
        time_label.place(x=5, y=line_sapcing * 1)
        self.time_info = TK.Label(self, text="Nan", font=("Arial", font_size))
        self.time_info.place(relx=0.0, y=line_sapcing * 2, relwidth=0.3)

        field_label = TK.Label(self, text="場域: ", font=("Arial", font_size))
        field_label.place(x=5, y=line_sapcing * 3)
        self.field_info = TK.Label(self, text="Nan", font=("Arial", font_size))
        self.field_info.place(relx=0.0, y=line_sapcing * 4, relwidth=0.3)

        pool_label = TK.Label(self, text="池號: ", font=("Arial", font_size))
        pool_label.place(x=5, y=line_sapcing * 5)
        self.pool_info = TK.Label(self, text="Nan", font=("Arial", font_size))
        self.pool_info.place(relx=0.0, y=line_sapcing * 6, relwidth=0.3)

        uploaded_label = TK.Label(self, text="上傳完成:")
        uploaded_label.place(x=5, y=line_sapcing * 7)
        self.uploaded_info = TK.Label(self, text="Nan", font=("Arial", font_size))
        self.uploaded_info.place(relx=0.0, y=line_sapcing * 8, relwidth=0.3)

        self.upload_button = TK.Button(self, text="上傳", command=self.upload_now)
        self.upload_button.place(relx=0.0, y=line_sapcing * 9, height=line_sapcing, relwidth=0.3)

        self.del_button = TK.Button(self, text="刪除此筆", command=self.delete_data)
        self.del_button.place(relx=0.0, y=line_sapcing * 11, height=line_sapcing, relwidth=0.3)

        # 繪製右側檢視畫面
        self.view_label = TK.Label(self)
        self.view_label.place(relx=0.3, y=20, relwidth=0.7)

        # 繪製按鈕
        button_1 = TK.Button(self, text="上一筆", command=self.last_data, font=("Arial", font_size))
        button_1.place(relx=0.0, rely=controller.button_rely, relheight=controller.button_relheight, relwidth=0.2)
        button_2 = TK.Button(self, text="下一筆", command=self.next_data, font=("Arial", font_size))
        button_2.place(relx=0.2, rely=controller.button_rely, relheight=controller.button_relheight, relwidth=0.2)
        button_3 = TK.Button(self, text="清除已上傳", command=self.delete_uploaded_data, font=("Arial", font_size))
        button_3.place(relx=0.4, rely=controller.button_rely, relheight=controller.button_relheight, relwidth=0.2)
        button_4 = TK.Button(self, text="上傳全部", command=self.upload_all, font=("Arial", font_size))
        button_4.place(relx=0.6, rely=controller.button_rely, relheight=controller.button_relheight, relwidth=0.2)
        button_5 = TK.Button(self, text="回首頁", command=lambda: controller.show_frame("init"), font=("Arial", font_size))
        button_5.place(relx=0.8, rely=controller.button_rely, relheight=controller.button_relheight, relwidth=0.2)

    def open_frame(self):
        print("open ViewFrame")
        # set data index
        self.index_now = len(self.controller.records) - 1
        self.cam = sl.Camera()
        # load data
        self.load_data()
        # call update view
        self.view_label_update()
        pass

    def close_frame(self):
        print("close ViewFrame")
        # close zed for view
        self.cam.close()
        pass

    def load_data(self):
        # print("load data")
        if len(self.controller.records) == 0:
            self.index_now = -1
            self.time_info['text'] = 'Nan'
            self.field_info['text'] = 'Nan'
            self.pool_info['text'] = 'Nan'
            self.uploaded_info['text'] = 'Nan'
            self.upload_button['state'] = TK.DISABLED
            self.del_button['state'] = TK.DISABLED
            print("no records")
            pass
        else:
            if self.index_now > len(self.controller.records) - 1:
                self.index_now = len(self.controller.records) - 1
            elif self.index_now < 0:
                self.index_now = 0
            print("load index:", self.index_now)
            self.time_info["text"] = time.strftime('%Y-%m-%d %H:%M:%S', self.controller.records[self.index_now].rec_time)
            field_id_loaded_str = str(self.controller.records[self.index_now].field_id)
            self.field_info["text"] = str(self.controller.setting["fidld_name_dict"][field_id_loaded_str])
            pool_id_loaded_str = str(self.controller.records[self.index_now].pool_id)
            self.pool_info["text"] = str(self.controller.setting["pool_name_dict"][pool_id_loaded_str])
            self.uploaded_info["text"] = str(self.controller.records[self.index_now].uploaded)
            if self.controller.records[self.index_now].uploaded:
                self.upload_button['state'] = TK.DISABLED
                self.upload_button['text'] = "已上傳"
            else:
                self.upload_button['state'] = TK.NORMAL
                self.upload_button['text'] = "上傳"
            self.del_button['state'] = TK.NORMAL
            # open zed for data
            self.set_view_camera()
        pass

    def set_view_camera(self):
        print("set view camera")
        if not self.controller.records[self.index_now].svo_path.exists():
            self.runtime = False
            return
        filepath = str(self.controller.records[self.index_now].svo_path)
        input_type = sl.InputType()
        input_type.set_from_svo_file(filepath)
        init = sl.InitParameters(input_t=input_type, svo_real_time_mode=False)
        self.cam.close()
        status = self.cam.open(init)
        if status != sl.ERROR_CODE.SUCCESS:
            print(repr(status))
            exit()
        self.runtime = sl.RuntimeParameters()
        self.mat = sl.Mat()

    def view_label_update(self):
        # print("view update")
        if self.runtime == False:
            # print("no .svo file")
            imgL = Image.open("VIDEO_FILE_MISSING.png")
            imgL = imgL.resize((854, 480))
            new_img = ImageTk.PhotoImage(imgL)
            self.view_label.configure(image=new_img)
            self.view_label.image = new_img
        else:
            err = self.cam.grab(self.runtime)
            if err == sl.ERROR_CODE.SUCCESS:
                # print("grab success")
                self.cam.retrieve_image(self.mat)
                image_ocvL = cv2.cvtColor(self.mat.get_data(), cv2.COLOR_BGR2RGB)
                imgL = Image.fromarray(image_ocvL)
                imgL = imgL.resize((854, 480))
                new_img = ImageTk.PhotoImage(imgL)
                self.view_label.configure(image=new_img)
                self.view_label.image = new_img
            else:
                # print("grab fail")
                pass

        if self.controller.frame_now == "view" and self.index_now != -1:
            self.view_label.after(30, self.view_label_update)
        pass

    def last_data(self):
        print("switch to last data")
        if self.index_now <= 0:
            # print("no last data")
            messagebox.showinfo('通知', '已是第一筆')
            pass
        else:
            self.index_now -= 1
        self.load_data()
        pass

    def next_data(self):
        # print("switch to next data")
        if self.index_now >= len(self.controller.records) - 1:
            # print("no next data")
            messagebox.showinfo('通知', '已是最後一筆')
            pass
        else:
            self.index_now += 1
        self.load_data()
        pass

    def delete_data(self):
        print("call delete data")
        MsgBox = TK.messagebox.askquestion('刪除檔案', '確定要刪除：' + str(self.controller.records[self.index_now].svo_path))
        if MsgBox == 'yes':
            self.controller.write_log("delete file" + str(self.controller.records[self.index_now].svo_path))
            self.controller.records.pop_record(self.index_now)
            self.load_data()
        pass

    def delete_uploaded_data(self):
        print("delete uploaded")
        self.controller.records.delete_uploaded()
        self.load_data()

    def upload_all(self):
        print("upload all")
        if not self.controller.records.upload_all():
            messagebox.showwarning('上傳失敗', '網路連線錯誤\r\n請稍後再試')
        if self.controller.setting["delete_after_upload"]:
            self.controller.records.delete_uploaded()
        self.load_data()

    def upload_now(self):
        print("upload this")
        if not self.controller.records.upload(self.index_now):
            messagebox.showwarning('上傳失敗', '網路連線錯誤\r\n請稍後再試')
        if self.controller.setting["delete_after_upload"]:
            self.controller.records.delete_uploaded()
        self.load_data()