from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QScrollArea, QProgressDialog
)
from PyQt5.QtCore import Qt
from keyframe_worker import KeyframeWorker
from looping_clip import LoopingClip

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QScrollArea

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QScrollArea, QFileDialog, QHBoxLayout, QLabel
)
from utils import get_keyframe_timestamps


class VideoLooperApp(QWidget):
    def __init__(self):
        super().__init__()

        self.global_scale = 1.0
        self.clips = []

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.container = QWidget()
        self.vbox = QVBoxLayout(self.container)
        self.scroll_area.setWidget(self.container)

        self.btn_load = QPushButton("Load Video")
        self.btn_scale_up = QPushButton("Scale Up All")
        self.btn_scale_down = QPushButton("Scale Down All")

        self.btn_load.clicked.connect(self.load_video)
        self.btn_scale_up.clicked.connect(self.scale_up_all)
        self.btn_scale_down.clicked.connect(self.scale_down_all)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.btn_load)
        buttons_layout.addWidget(self.btn_scale_down)
        buttons_layout.addWidget(self.btn_scale_up)

        main_layout = QVBoxLayout()
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.scroll_area)

        self.setLayout(main_layout)
        self.setWindowTitle("Video Looper")
        
        self.scroll_area.verticalScrollBar().valueChanged.connect(self.update_visible_clips)
        self.scroll_area.horizontalScrollBar().valueChanged.connect(self.update_visible_clips)

    def update_visible_clips(self):
        viewport = self.scroll_area.viewport()
        visible_rect = QRect(0, 0, viewport.width(), viewport.height())

        for clip in self.clips:
            # Map clip geometry to viewport coordinates
            clip_rect = clip.geometry()
            clip_pos_in_viewport = self.container.mapTo(viewport, clip.pos())
            clip_rect_mapped = QRect(clip_pos_in_viewport, clip_rect.size())

            # Check if clip_rect_mapped intersects visible_rect
            if clip_rect_mapped.intersects(visible_rect):
                if not clip.timer.isActive():
                    clip.timer.start()
            else:
                if clip.timer.isActive():
                    clip.timer.stop()

    def load_video(self):
        video_path, _ = QFileDialog.getOpenFileName(self, "Select Video File")
        if not video_path:
            return

        # Clear existing clips
        for clip in self.clips:
            clip.timer.stop()
            clip.setParent(None)
        self.clips.clear()

        timestamps = get_keyframe_timestamps(video_path)
        if not timestamps:
            QLabel("No keyframes found or error reading video.", self).show()
            return

        for i in range(len(timestamps) - 1):
            start = timestamps[i]
            end = timestamps[i + 1]
            clip = LoopingClip(video_path, start, end)
            clip.set_scale(self.global_scale)
            self.clips.append(clip)
            self.vbox.addWidget(clip)

    def scale_up_all(self):
        self.global_scale *= 1.25
        if self.global_scale > 5.0:
            self.global_scale = 5.0
        for clip in self.clips:
            clip.set_scale(self.global_scale)

    def scale_down_all(self):
        self.global_scale /= 1.25
        if self.global_scale < 0.1:
            self.global_scale = 0.1
        for clip in self.clips:
            clip.set_scale(self.global_scale)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoLooperApp()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())