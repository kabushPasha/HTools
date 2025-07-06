from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QImage
import cv2

class LoopingClip(QWidget):
    def __init__(self, video_path, start_time, end_time):
        super().__init__()
        self.cap = cv2.VideoCapture(video_path)
        self.start_time = start_time
        self.end_time = end_time

        self.cap.set(cv2.CAP_PROP_POS_MSEC, self.start_time * 1000)

        self.scale_factor = 1.0  # default scale

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1000 // 30)

    def set_scale(self, scale_factor):
        self.scale_factor = scale_factor

    def update_frame(self):
        current_pos = self.cap.get(cv2.CAP_PROP_POS_MSEC)
        if current_pos > self.end_time * 1000:
            self.cap.set(cv2.CAP_PROP_POS_MSEC, self.start_time * 1000)

        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_MSEC, self.start_time * 1000)
            return

        h, w = frame.shape[:2]

        new_w = int(w * self.scale_factor)
        new_h = int(h * self.scale_factor)

        resized_frame = cv2.resize(frame, (new_w, new_h))
        rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
        img = QImage(rgb_frame.data, new_w, new_h, rgb_frame.strides[0], QImage.Format_RGB888)

        self.label.setPixmap(QPixmap.fromImage(img))
        self.label.resize(new_w, new_h)
        self.resize(new_w, new_h)

    def resizeEvent(self, event):
        super().resizeEvent(event)
