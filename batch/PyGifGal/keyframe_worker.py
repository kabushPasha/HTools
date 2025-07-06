from PyQt5.QtCore import QThread, pyqtSignal
from utils import get_keyframe_timestamps

class KeyframeWorker(QThread):
    finished = pyqtSignal(list, str)  # timestamps list and video path

    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path

    def run(self):
        timestamps = get_keyframe_timestamps(self.video_path)
        self.finished.emit(timestamps, self.video_path)
