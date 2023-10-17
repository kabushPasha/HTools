import kivy
kivy.require('1.9.1') # the kivy version required

# import the kivy modules/widgets
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.button import Button
from kivy.uix.video import Video
from kivy.uix.progressbar import ProgressBar

import glob
import os,sys

from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

# An App running a video file
class MyVideo(Video):
	def setApp(self, App):
		self.app = App
		self.preview = "./black.png"

	def on_touch_up(self, touch):
		if touch.is_touch:
			if self.collide_point(*touch.pos):	
				print(self.source)
				self.unload()
				self.preview = "./black.png"
				
				# REMOVE
				if touch.button == 'right':
					print("RIGHT")					
					if os.path.basename(self.source) != "black.png":
						os.remove(self.source)
					
						
				
				if self.app.vods:
					self.source = self.app.vods.pop()
				else:
					self.source = "black.png"

					

class MyVideoApp(App):
	def build(self):
		self.layout = GridLayout(cols=2)
		self.n_videos = 2
		self.players = []	
		
		self.src_folder = sys.argv[1]
		
		self.vods = sorted(glob.glob( self.src_folder + "/*.mp4"),reverse=True)
		
		
		for i in range(0,self.n_videos):
			# break if we're out of vods
			if self.vods == [] :
				break
			
			player = MyVideo(source= self.vods.pop() ,  state='play', options={'allow_stretch': True,'eos': 'loop'}, volume=0)
			player.setApp(self)
			self.players += [player]	
			self.layout.add_widget(widget=player)
		
		
		pb = ProgressBar(max=1000)
		pb.value = 750
		self.layout.add_widget(widget=pb)
		
		return (self.layout)


 

# Start the Video App
if __name__ == '__main__':
	MyVideoApp().run()