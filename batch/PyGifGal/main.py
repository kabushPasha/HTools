import sys
from PyQt5.QtWidgets import QApplication
from video_looper_app import VideoLooperApp

def main():
    app = QApplication(sys.argv)
    window = VideoLooperApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
