from __future__ import print_function
import json
import time
import socket
from time import sleep
from detector import Detector

SOCKET_PATH = "/tmp/node-python-socket"
MSG_SEPARATOR = "\r"
FRAME_WAIT = 90  # ms

if __name__ == "__main__":
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(SOCKET_PATH)
    detector = Detector()
    t1 = time.time()
    frame_count = 0
    while True:
        frame, face_num, smile_num = detector.process_frame('jpeg')
        msg = json.dumps({
            'frame': frame,
            'face_num': face_num,
            'smile_num': smile_num
        })
        client.send(msg)
        client.send(MSG_SEPARATOR)
        sleep(FRAME_WAIT / 1000)

        t2 = time.time()
        frame_count += 1
        if (t2 - t1) > 10.0:
            print("FPS is %d" % (int(frame_count/10)))
            frame_count = 0
            t1 = time.time()

    client.close()
