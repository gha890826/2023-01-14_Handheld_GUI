#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import socket
import tqdm
import os


def send(filename="./svo_files/test.svo", host="*", port=5001, BUFFER_SIZE=4096):
    SEPARATOR = "<SEPARATOR>"
    # get the file size
    filesize = os.path.getsize(filename)

    # create the client socket
    s = socket.socket()

    print(f"[+] Connecting to {host}:{port}")
    s.settimeout(10)
    s.connect((host, port))
    print("[+] Connected.")

    # send the filename and filesize
    s.send(f"{filename}{SEPARATOR}{filesize}".encode("utf-8"))

    # start sending the file
    progress = tqdm.tqdm(range(
        filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in
            # busy networks
            s.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))
    # close the socket
    s.close()


if __name__ == "__main__":
    send(host="192.168.50.188")
