from os import path
import base64
import cv2
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

        # Configurable arguments
        self.camera_width = 500
        self.face_rect = {'color': (255, 255, 0), 'thickness': 3}
        self.smile_rect = {'color': (0, 255, 0), 'thickness': 2}
        self.face_opts = {'scaleFactor': 1.05, 'minNeighbors': 12}
        self.smile_opts = {'scaleFactor': 1.6, 'minNeighbors': 22}
        self.output_img_size = {'width': 400, 'height': 300}
        self.brightness_threshold = 20  # stop face detection if brightness below this value

    def __del__(self):
        self.camera.stop()

    def process_frame(self, output_fmt=None):
        assert output_fmt in ['raw', 'jpeg', 'png']
        face_num = 0
        smile_num = 0

        frame = self.camera.read()
        frame = imutils.resize(frame, width=self.camera_width)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = gray.mean()

        if brightness < self.brightness_threshold:
            return (frame, face_num, smile_num)

        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=self.face_opts['scaleFactor'],
            minNeighbors=self.face_opts['minNeighbors'])

        for (f_x, f_y, f_w, f_h) in faces:
            face_num += 1
            cv2.rectangle(frame, (f_x, f_y), (f_x + f_w, f_y + f_h),
                          self.face_rect['color'], self.face_rect['thickness'])
            roi_gray = gray[f_y:f_y + f_h, f_x:f_x + f_w]
            roi_color = frame[f_y:f_y + f_h, f_x:f_x + f_w]

            smiles = self.smile_cascade.detectMultiScale(
                roi_gray,
                scaleFactor=self.smile_opts['scaleFactor'],
                minNeighbors=self.smile_opts['minNeighbors'],
                minSize=(f_w / 4, f_h / 8))

            for (s_x, s_y, s_w, s_h) in smiles:
                smile_num += 1
                cv2.rectangle(roi_color, (s_x, s_y), (s_x + s_w, s_y + s_h),
                              self.smile_rect['color'],
                              self.smile_rect['thickness'])
        output_frame = cv2.resize(
            frame,
            (self.output_img_size['width'], self.output_img_size['height']))

        if output_fmt != 'raw':
            cnt = cv2.imencode('.' + output_fmt, output_frame)[1]
            output_frame = base64.encodestring(cnt).decode('ascii')
        return (output_frame, face_num, smile_num)


if __name__ == "__main__":
    detector = Detector()
    while True:
        frame, face_num, smile_num = detector.process_frame('raw')
        print(face_num, smile_num)
        cv2.imshow('Smile Detector', frame)
        c = cv2.waitKey(100)  # wait 100ms
        if c == 27:  # Esc key to stop
            break
    cv2.destroyAllWindows()
