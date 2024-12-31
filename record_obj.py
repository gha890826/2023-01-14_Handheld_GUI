#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import json
import time
import os
from pathlib import Path
from client import send
import mysql.connector
from mysql.connector import errorcode


class Record:
    """
    A class to record a recor.

    ...

    Attributes:
        rec_time: time.localtime
            The time of this record.
        field_id: int
            The fidld id of this record.
        pool_id: int
            The pool id of this record.
        svo_path: pathlib.Path
            The .svo file path of record.
        uploaded: bool
            Has the .svo file been uploaded. Init value is False.
        deleted: bool
            Has the .svo file in this mechine been deleted. Init value is False.

    Methods:
        get_json():
            Get the json part of this record.
        upload():
            Upload .svo file.
        delete_svo():
            Delete .svo file.
    """

    def __init__(self,
                 rec_time: time.localtime,
                 field_id: int,
                 pool_id: int,
                 svo_path: Path,
                 uploaded: bool = False,
                 deleted: bool = False):
        """
        Construct all the necessary attributes of this object.

        Args:
            rec_time: time.localtime
                The time of this record.
            field_id: int
                The fidld id of this record.
            pool_id: int
                The pool id of this record.
            svo_path: pathlib.Path
                The .svo file path of record.
            uploaded: bool
                Has the .svo file been uploaded? Default is False.
            deleted
                Has the .svo file in this machine been deleted? Default is False.

        Return:
            None.
        """
        self.rec_time = rec_time
        self.field_id = field_id
        self.pool_id = pool_id
        self.svo_path = svo_path
        self.uploaded = uploaded
        self.deleted = deleted
        pass

    def __str__(self) -> None:
        """
        Return the string of obj.

        Args:
            None.

        Return:
            None.
        """
        return f"rec_time: {time.strftime('%Y-%m-%d %H:%M:%S',self.rec_time)}, field_id: {self.field_id}, pool_id: {self.pool_id}, svo_path: {self.svo_path}, uploaded: {self.uploaded}, deleted: {self.deleted}"

    def get_json(self) -> dict:
        """
        Get the json part of this record.

        Args:
            None.

        Return:
            None.
        """
        myjson_dic = {
            "rec_time": self.rec_time,
            "field_id": self.field_id,
            "pool_id": self.pool_id,
            "svo_path": os.fspath(self.svo_path),
            "uploaded": self.uploaded,
            "deleted": self.deleted
        }
        return myjson_dic
        pass

    def upload(self) -> bool:
        """
        Upload .svo file.

        Args:
            None.

        Return:
            None.
        """

        if not self.uploaded:
            try:
                # ===== svo opload =====
                send(str(self.svo_path))

                # ===== sql write =====
                # set link
                cnx = mysql.connector.connect(user=USER,
                                              password=PASSWORD,
                                              host=HOST,
                                              port='3306',
                                              database=DATABASE)  # 設定連線字串
                # open link
                mycursor = cnx.cursor()  # 開啟連線
                print("開啟連線成功")
                # start writing
                sql = "INSERT INTO ai_fish.camera_record (field_id, pool_id, device_type, record_time, file_name) VALUES (%s, %s, %s, %s, %s)"
                val = (self.field_id, self.pool_id, 1, time.strftime(
                    '%Y-%m-%d %H:%M:%S', self.rec_time), self.svo_path.name)
                print("變數成功", val)
                mycursor.execute(sql, val)
                print("加入成功")
                cnx.commit()
                print("送出成功")
                # ===== set self.uploaded =====
                self.uploaded = True
            except Exception as e:
                print(f"upload {self.svo_path} fail: ", e)
                return False
        return True
        pass

    def delete_svo(self) -> None:
        """
        Delete .svo file.

        Args:
            None.

        Return:
            None.
        """
        if not self.deleted:
            print(f"刪除檔案{self.svo_path}")
            try:
                if self.svo_path.exists():
                    self.svo_path.unlink()
                self.deleted = True
            except:
                print(f"delete {self.svo_path} fail")
        pass


class Records:
    """
    Provide the way to save and manage list of record

    Attributes:
        __data: list
            A private list to save record.
        json_path: pathlib.Path
            Path of records.json

    Method:
        data_sort():
            Sort Record in __data[].
        save_to_json():
            Save __data[] to records.json.
        read_from_json():
            Read records from records.json to __data[].
        add_data():
            Add a Record into __data[] by args.
        add_record():
            Add a Record object into __data[].
        upload():
            Upload .svo file which hasn't been uploaded.
        delete_uploaded():
            Delete .svo file which has been uploaded.

    """
    __data: []
    json_path: Path

    def __init__(self, path=Path("records.json"), init_data=[]):
        self.data = init_data
        self.json_path = Path(path)
        if self.json_path.exists():
            self.read_from_json()
        else:
            self.json_path.touch()
        pass

    def __str__(self):
        return f"Has {len(self.data)} Records."

    def __getitem__(self, key):
        return self.data[key]

    def __len__(self):
        return len(self.data)

    def data_sort(self):
        self.data.sort(key=lambda r: r.rec_time)

    def save_to_json(self) -> None:
        myjson = [j.get_json() for j in self.data]
        with open(self.json_path, "w") as f:
            json.dump(myjson, f, indent=4)
        pass

    def read_from_json(self) -> None:
        with open(self.json_path) as f:
            temps = json.load(f)
            for p in temps:
                t = time.localtime(time.mktime(tuple(p["rec_time"])))
                self.add_record(t, p["field_id"], p["pool_id"], Path(
                    p["svo_path"]), p["uploaded"], p["deleted"])
        pass

    def add_record(self,
                   rec_time: time.localtime,
                   field_id: int,
                   pool_id: int,
                   svo_path: Path,
                   uploaded: bool = False,
                   deleted: bool = False) -> None:
        self.add_data(Record(rec_time, field_id, pool_id,
                      svo_path, uploaded, deleted))
        pass

    def add_data(self, new_record: Record) -> None:
        if type(new_record) != Record:
            raise ValueError(f"{Record} wanted, but {type(new_record)} give")
        self.data.append(new_record)
        self.data_sort()
        self.save_to_json()

    def upload_all(self) -> bool:
        for i in self.data:
            time.sleep(2)
            if not i.svo_path.exists():
                print(f"path {i.svo_path} not exists")
                continue
            if not i.upload():
                self.save_to_json()
                return False
        return True

    def upload_newest(self) -> bool:
        return self.upload(len(self.data) - 1)

    def upload(self, index) -> bool:
        if 0 <= index < len(self.data):
            if self.data[index].upload():
                self.save_to_json()
                return True
        return False

    def delete_uploaded(self) -> None:
        index = 0
        while index < len(self.data):
            if self.data[index].uploaded:
                self.pop_record(index)
                continue
            else:
                index += 1
        self.save_to_json()
        pass

    def pop_record(self, index) -> None:
        self.data[index].delete_svo()
        self.data.pop(index)
        self.data_sort()
        self.save_to_json()


def unitest():
    rec1 = Record(time.localtime(time.time()), 1,
                  1, Path('./svo_files/test.svo'))
    rec2 = Record(time.localtime(time.time()), 2,
                  2, Path('./svo_files/test.svo'))
    rec3 = Record(time.localtime(time.time()), 3,
                  3, Path('./svo_files/test.svo'))
    records = Records()
    # records.read_from_json()
    # records.add_data(rec2)
    # try:
    #     records.add_data("test")
    # except:
    #     print("catch")
    # records.add_record(time.localtime(time.time()), 3, 3, Path('./svo_files/test.svo'))
    print(records)
    # records.upload()
    records.delete_uploaded()
    records.save_to_json()
    # print(records[0])
    for rec in records:
        print(rec)


if __name__ == "__main__":
    unitest()
