from __future__ import print_function
from os import path
import cv2
import time
import base64
from imutils.video import WebcamVideoStream
import imutils


FACE_PATH = path.join(
    path.dirname(path.abspath(__file__)), 'data',
    'haarcascade_frontalface_default.xml')
SMILE_PATH = path.join(
    path.dirname(path.abspath(__file__)), 'data', 'haarcascade_smile.xml')


class Detector(object):
    def __init__(self):
        self.camera = WebcamVideoStream(src=0).start()
        self.face_cascade = cv2.CascadeClassifier(FACE_PATH)
        self.smile_cascade = cv2.CascadeClassifier(SMILE_PATH)
        self.cache = {'faces': None, 'smiles': None, 'hit_count': 0}

        # Configurable arguments
        self.camera_width = 500
        self.face_rect = {'color': (255, 255, 0), 'thickness': 3}
        self.smile_rect = {'color': (0, 255, 0), 'thickness': 2}
        self.face_opts = {'scaleFactor': 1.05, 'minNeighbors': 12}
        self.smile_opts = {'scaleFactor': 1.6, 'minNeighbors': 22}
        self.output_img_size = {'width': 400, 'height': 300}
        self.brightness_threshold = 30  # stop face detection if brightness below this value
        self.cache_ttl = 2  # keep cache in number of frames

    def __del__(self):
        self.camera.stop()

    def process_frame(self, output_fmt=None):
        assert output_fmt in ['raw', 'jpeg', 'png']
        face_num = 0
        smile_num = 0

        frame = self.camera.read()
        frame = imutils.resize(frame, width=self.camera_width)
        frame = cv2.flip(frame, 1)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = gray.mean()

        if brightness < self.brightness_threshold:
            return (self.encode_frame(frame, output_fmt), face_num, smile_num)

        faces = self._get_faces(gray)

        for (f_x, f_y, f_w, f_h) in faces:
            face_num += 1
            cv2.rectangle(frame, (f_x, f_y), (f_x + f_w, f_y + f_h),
                          self.face_rect['color'], self.face_rect['thickness'])
            roi_gray = gray[f_y:f_y + f_h, f_x:f_x + f_w]
            roi_color = frame[f_y:f_y + f_h, f_x:f_x + f_w]

            smiles = self._get_smiles(roi_gray, f_w, f_h)

            for (s_x, s_y, s_w, s_h) in smiles:
                smile_num += 1
                cv2.rectangle(roi_color, (s_x, s_y), (s_x + s_w, s_y + s_h),
                              self.smile_rect['color'],
                              self.smile_rect['thickness'])
        output_frame = cv2.resize(
            frame,
            (self.output_img_size['width'], self.output_img_size['height']))

        return (self.encode_frame(output_frame, output_fmt), face_num, smile_num)

    def encode_frame(self, frame, output_fmt):
        if output_fmt != 'raw':
            cnt = cv2.imencode('.' + output_fmt, frame)[1]
            frame = base64.encodestring(cnt).decode('ascii')
        return frame

    def _get_faces(self, frame_gray):
        self._check_cache()
        if self.cache['faces'] is None:
            faces = self.face_cascade.detectMultiScale(
                frame_gray,
                scaleFactor=self.face_opts['scaleFactor'],
                minNeighbors=self.face_opts['minNeighbors'])
            self.cache['faces'] = faces
        return self.cache['faces']

    def _get_smiles(self, face_gray, face_width, face_height):
        if self.cache['smiles'] is None:
            smiles = self.smile_cascade.detectMultiScale(
                face_gray,
                scaleFactor=self.smile_opts['scaleFactor'],
                minNeighbors=self.smile_opts['minNeighbors'],
                minSize=(face_width / 4, face_height / 8))
            self.cache['smiles'] = smiles
        return self.cache['smiles']

    def _check_cache(self):
        if self.cache['hit_count'] > self.cache_ttl:
            self.cache['faces'] = None
            self.cache['smiles'] = None
            self.cache['hit_count'] = 0
        else:
            self.cache['hit_count'] += 1


if __name__ == "__main__":
    detector = Detector()
    t1 = time.time()
    count = 0
    while True:
        frame, face_num, smile_num = detector.process_frame('raw')
        print(face_num, smile_num)
        cv2.imshow('Smile Detector', frame)
        c = cv2.waitKey(100)  # wait 100ms
        if c == 27:  # Esc key to stop
            break
        t2 = time.time()
        count += 1
        if (t2 - t1) > 5.0:
            print("FPS is %d" % (int(count/5)))
            count = 0
            t1 = time.time()
    cv2.destroyAllWindows()
