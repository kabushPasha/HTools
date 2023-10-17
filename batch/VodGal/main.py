# Add arguments:
# 4 - loads 4 pictures
# s - enables save mode - images would only be moved but not deleted
# k - keeps the file on the same place, does not move to picked folder
# r - loads random item

# KEYBOARD SHORTCUTS:
# d - delete all images
# s - save all images

import kivy
kivy.require('1.9.1') # the kivy version required

# import the kivy modules/widgets
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.button import Button
from kivy.uix.video import Video
from kivy.uix.progressbar import ProgressBar
from functools import partial
   
from kivy.core.window import Window

import glob
import os,sys
import random

from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
# 3840x2160 * 1.5
Window.size = (0.25*3840/1.5, 0.25*2160/1.5)
Window.top = 30 + 3*0.25*2160/1.5 - 70
Window.left = 3 * 0.25*3840/1.5

# An App running a video file
class MyVideo(Video):
	def setApp(self, App,_pb):
		self.app = App
		self.preview = "./black.png"
		self.pb = _pb
		
	def deleteCurrent(self):
		self.clearCurrent()
			
		if not self.app.save_mode:
			if os.path.basename(self.source) != "black.png":
				os.remove(self.source)				
				
		self.loadNew()
		
	def saveCurrent(self):
		self.clearCurrent()
	
		if not self.app.keep_mode:
			print("move to folder")
			src_path = self.source
			dest_path = os.path.dirname(src_path) + "/picked/" + os.path.basename(src_path)
			if not os.path.isdir(os.path.dirname(dest_path)): os.mkdir(os.path.dirname(dest_path))
			os.rename(src_path, dest_path)
			
		self.loadNew()

	def clearCurrent(self):
		self.unload()
		self.preview = "./black.png"
	
	def loadNew(self):	
		if self.app.vods:
			self.source = self.app.vods.pop()
		else:
			self.source = "black.png"
		
	def on_touch_up(self, touch):
		if touch.is_touch:
			if self.collide_point(*touch.pos):	
				if touch.button == 'right':
					self.deleteCurrent()			
				else:
					self.saveCurrent()
				

class MyVideoApp(App):
	def build(self):
		# bind keyboard
		Window.bind(on_key_down=self.key_action)

		self.layout = GridLayout(cols=2)
		self.n_videos = 1 
		self.players = []
		self.title = 'DELETE MODE'
		self.save_mode = False
		self.keep_mode = "k" in sys.argv
				
		self.src_folder = sys.argv[1]
		# If we have an argument then load multiple
		if "4" in sys.argv: self.n_videos = 4
		# switch to save mode if s in args
		if "s" in sys.argv:
			self.title = 'SAVE MODE'
			self.save_mode = True
	
		self.vods = sorted(glob.glob( self.src_folder + "/*.mp4"),reverse=True)
		# shuffle if we're random
		if "r" in sys.argv: random.shuffle(self.vods)
		
		
		for i in range(0,self.n_videos):
			# break if we're out of vods
			if self.vods == [] :
				break
						
			subLayout = BoxLayout(orientation='vertical')
			
			player = MyVideo(source= self.vods.pop() ,  state='play', options={'allow_stretch': True,'eos': 'loop'}, volume=0,size_hint=(1, 0.99))
			pb = ProgressBar(max=1000,size_hint_y=None , height = 2 )
			player.setApp(self,pb)
			self.players += [player]	
			
			
			subLayout.add_widget(widget=player)					
			subLayout.add_widget(widget=pb)	
			
			
			def on_position_change(instance, value):
				instance.pb.value = 1000*instance.position/instance.duration

			player.bind(position=partial(on_position_change))

						
			self.layout.add_widget(widget=subLayout)
			
		return (self.layout)

	def key_action(self, *args):
		if args[3] == 'd':
			for player in self.players:
				player.deleteCurrent()
		
 

# Start the Video App
if __name__ == '__main__':
	MyVideoApp().run()
	

			