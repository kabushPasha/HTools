import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Player")

        self.video_frame = tk.Frame(root)
        self.video_frame.pack()

        self.canvas = tk.Canvas(self.video_frame)
        self.canvas.pack()

        self.play_button = tk.Button(root, text="Play", command=self.play_video)
        self.play_button.pack(pady=10)

        self.pause_button = tk.Button(root, text="Pause", command=self.pause_video)
        self.pause_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_video)
        self.stop_button.pack(pady=10)

        self.video_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video files", "*.mp4;*.avi")])

        self.cap = cv2.VideoCapture(self.video_path)
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.canvas.config(width=self.width, height=self.height)

        self.paused = False
        self.update()

    def play_video(self):
        self.paused = False

    def pause_video(self):
        self.paused = True

    def stop_video(self):
        self.cap.release()
        self.root.destroy()

    def update(self):
        if not self.paused:
            ret, frame = self.cap.read()
            if ret:
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.root.after(10, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    player = VideoPlayer(root)
    root.mainloop()