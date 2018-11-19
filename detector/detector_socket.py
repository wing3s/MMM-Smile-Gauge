import socket
import json
from time import sleep
from detector import Detector

SOCKET_PATH = "/tmp/node-python-socket"
MSG_SEPARATOR = "\r"
FRAME_WAIT = 100  # ms

if __name__ == "__main__":
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(SOCKET_PATH)
    detector = Detector()
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

    client.close()
