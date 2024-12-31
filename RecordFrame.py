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


class RecordFrame(TK.Frame):
    """
    Inheritance of tkinter.frame. The recording page(frame) of Application.

    Attributes:
        controller : TK.Tk
            the Tk of frames, which means Application at here.
        parent : TK.Frame
            the contain of frame in Application.

    Method:
        camera_update():
            Update the tkImage label, which display the camera view on this frame.
        set_button():
            Set button on screen to keyboard. Be called when show this frame.

    """

    field_index: int
    field_id: int
    pool_index: int
    pool_id: int

    def __init__(self, parent, controller):

        # 初始化Frame
        TK.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.recording = False
        self.rec_len = 5
        self.field_index = 0
        self.field_id = self.controller.setting["field_ids"][self.field_index]
        self.pool_index = 0
        self.pool_id = self.controller.setting["pool_ids"][self.field_index][self.pool_index]

        # 繪製頁面
        page_name_label = TK.Label(self, text="錄製介面").place(relx=0.0, y=controller.title_y, relwidth=1.0)

        # 繪製左側資訊欄
        line_sapcing = 40
        font_size = 15
        field_text_label = TK.Label(self, text="現在場域: ", font=("Arial", font_size))
        field_text_label.place(x=5, y=line_sapcing * 1)
        self.field_label = TK.Label(self, text="Nan", font=("Arial", font_size))
        self.field_label.place(relx=0.0, y=line_sapcing * 2, relwidth=0.3)
        field_next_button = TK.Button(self, text=">", command=self.next_field, font=("Arial", font_size))
        field_next_button.place(relx=0.2, y=line_sapcing * 2, height=line_sapcing, relwidth=0.1)
        field_last_button = TK.Button(self, text="<", command=self.last_field, font=("Arial", font_size))
        field_last_button.place(relx=0.0, y=line_sapcing * 2, height=line_sapcing, relwidth=0.1)
        pool_text_label = TK.Label(self, text="現在池號: ", font=("Arial", font_size))
        pool_text_label.place(x=5, y=line_sapcing * 3)
        self.pool_label = TK.Label(self, text="Nan", font=("Arial", font_size))
        self.pool_label.place(relx=0.0, y=line_sapcing * 4, relwidth=0.3)
        pool_next_button = TK.Button(self, text=">", command=self.next_pool, font=("Arial", font_size))
        pool_next_button.place(relx=0.2, y=line_sapcing * 4, height=line_sapcing, relwidth=0.1)
        pool_last_button = TK.Button(self, text="<", command=self.last_pool, font=("Arial", font_size))
        pool_last_button.place(relx=0.0, y=line_sapcing * 4, height=line_sapcing, relwidth=0.1)
        len_text_label = TK.Label(self, text="錄製長度: ", font=("Arial", font_size))
        len_text_label.place(x=5, y=line_sapcing * 5)

        def Selection():
            self.rec_len = var.get()
            print("chouse rec_len" + str(self.rec_len))

        var = TK.IntVar()
        var.set(5)
        sec = [5, 30, 60, 120]
        self.rec_len_buttons = {}
        for index, val in enumerate(sec):
            self.rec_len_buttons[val] = TK.Radiobutton(self,
                                                       text=str(val) + "秒",
                                                       variable=var,
                                                       value=val,
                                                       command=Selection,
                                                       font=("Arial", font_size))
            self.rec_len_buttons[val].place(x=5, y=line_sapcing * (index + 6))

        # 繪製攝影機視窗
        self.camera_label = TK.Label(self)
        self.camera_label.place(relx=0.3, y=20, relwidth=0.7)
        # 3/16開始寫這邊吧 要完成檢視功能跟場域選擇

        # 繪製按鈕
        self.button_1 = TK.Button(self, text="開始錄製", command=lambda: self.start_rec(), font=("Arial", font_size))
        self.button_1.place(relx=0.0, rely=controller.button_rely, relheight=controller.button_relheight, relwidth=0.2)
        self.button_2 = TK.Button(self, text="錄製紀錄", command=lambda: controller.show_frame("view"), font=("Arial", font_size))
        self.button_2.place(relx=0.2, rely=controller.button_rely, relheight=controller.button_relheight, relwidth=0.2)
        self.button_5 = TK.Button(self, text="回首頁", command=lambda: controller.show_frame("init"), font=("Arial", font_size))
        self.button_5.place(relx=0.8, rely=controller.button_rely, relheight=controller.button_relheight, relwidth=0.2)

    def __del__(self):
        print("close cap")
        self.cap.close()

    def open_frame(self):
        print("open RecordFrame")

        self.update_info()

        # open zed
        init = sl.InitParameters()
        init.camera_resolution = sl.RESOLUTION.HD720
        init.camera_fps = 30
        self.cam = sl.Camera()
        if not self.cam.is_opened():
            print("Opening ZED Camera...")
        status = self.cam.open(init)
        if status != sl.ERROR_CODE.SUCCESS:
            print(repr(status))
            self.controller.write_log("ZED open fail!!!")
        self.runtime = sl.RuntimeParameters()
        self.mat = sl.Mat()

        def print_camera_information(cam):
            print("Resolution: {0}, {1}.".format(round(cam.get_camera_information().camera_resolution.width, 2),
                                                 cam.get_camera_information().camera_resolution.height))
            print("Camera FPS: {0}.".format(cam.get_camera_information().camera_fps))
            print("Firmware: {0}.".format(cam.get_camera_information().camera_firmware_version))
            print("Serial number: {0}.\n".format(cam.get_camera_information().serial_number))

        print_camera_information(self.cam)

        # grab and update tkImage

        if not self.recording:
            self.grab_frame()

    def close_frame(self):
        print("close RecordFrame")
        # close zed
        if not self.recording:
            self.cam.close()
            print("ZED close")
        pass

    def start_rec(self):
        self.button_1['state'] = TK.DISABLED
        self.button_1['text'] = "錄影中"
        print(f"start record {self.rec_len} sec")
        self.controller.write_log(f"start record {self.rec_len} sec")

        vid = sl.ERROR_CODE.FAILURE
        time_now = time.localtime()
        filepath = Path("svo_files") / time.strftime(str(self.field_id) + '_' + str(self.pool_id) + "_%Y-%m-%d-%H-%M-%S.svo", time_now)
        self.controller.records.add_record(time_now, self.field_id, self.pool_id, filepath)
        self.controller.records.save_to_json()
        self.recording = True
        self.controller.after(int(self.rec_len * 1000), self.stop_rec)
        print("set rec_param")
        record_param = sl.RecordingParameters(str(filepath), sl.SVO_COMPRESSION_MODE.H264)
        print("enable_recording")
        vid = self.cam.enable_recording(record_param)
        print(repr(vid))

    def grab_frame(self):
        err = self.cam.grab(self.runtime)
        self.cam.retrieve_image(self.mat, sl.VIEW.LEFT)
        image_ocvL = cv2.cvtColor(self.mat.get_data(), cv2.COLOR_BGR2RGB)
        imgL = Image.fromarray(image_ocvL)
        imgL = imgL.resize((854, 480))
        new_img = ImageTk.PhotoImage(imgL)
        self.camera_label.configure(image=new_img)
        self.camera_label.image = new_img
        if self.controller.frame_now == "record" or self.recording:
            self.controller.after(1, self.grab_frame)
        else:
            self.cam.close()
            print("ZED close")

    def stop_rec(self):
        print("Recording finished.")
        self.recording = False
        self.cam.disable_recording()
        self.button_1['state'] = TK.NORMAL
        self.button_1['text'] = "開始錄製"
        self.controller.write_log("Recording Finished")
        if self.controller.setting["upload_when_recording"]:
            self.controller.records.upload_newest()
            if self.controller.setting["delete_after_upload"]:
                self.controller.records.delete_uploaded()
        # 3/17 from here, to finish the upload after record, and slove the socket jam problem

    def camera_update(self):
        if not self.recording:
            pass
        self.camera_label.after(30, self.camera_update)
        # print("camera_update end")

    def update_info(self):
        self.field_label['text'] = str(self.controller.setting["field_names"][self.field_index])
        self.pool_label['text'] = str(self.controller.setting["pool_names"][self.field_index][self.pool_index])
        pass

    def last_field(self):
        self.field_index -= 1
        self.field_index %= len(self.controller.setting["field_ids"])
        self.field_id = self.controller.setting["field_ids"][self.field_index]
        self.pool_index = 0
        self.pool_id = self.controller.setting["pool_ids"][self.field_index][self.pool_index]
        self.update_info()
        pass

    def next_field(self):
        self.field_index += 1
        self.field_index %= len(self.controller.setting["field_ids"])
        self.field_id = self.controller.setting["field_ids"][self.field_index]
        self.pool_index = 0
        self.pool_id = self.controller.setting["pool_ids"][self.field_index][self.pool_index]
        self.update_info()
        pass

    def last_pool(self):
        self.pool_index -= 1
        self.pool_index %= len(self.controller.setting["pool_ids"][self.field_index])
        self.pool_id = self.controller.setting["pool_ids"][self.field_index][self.pool_index]
        self.update_info()
        pass

    def next_pool(self):
        self.pool_index += 1
        self.pool_index %= len(self.controller.setting["pool_ids"][self.field_index])
        self.pool_id = self.controller.setting["pool_ids"][self.field_index][self.pool_index]
        self.update_info()
        pass