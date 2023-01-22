from PIL import Image
import math,time,os

def image_grid(imgs):
	cols = math.ceil(pow(len(imgs),0.5))
	rows = cols

	w, h = imgs[0].size
	grid = Image.new('RGB', size=(cols*w, rows*h))
	grid_w, grid_h = grid.size
	
	for i, img in enumerate(imgs):
		grid.paste(img, box=(i%cols*w, i//cols*h))
	return grid
	
	
def saveImages(images,prompt = "",out_folder = "S:\Temp\ML\SD"):
	i = 0 
	for image in images:
		i += 1
		image.save(out_folder + "IMAGE__" + str(time.time()) +f"__iter_{i}" + "__PROMPT__" +  prompt.replace(" ","_")  +".png")
		
	# Save and open grid
	grid = image_grid(images)
	grid_path = out_folder + "GRID__" + str(time.time()) + "__PROMPT__" +  prompt.replace(" ","_").replace(",","_")  +".png"
	grid.save(grid_path)
	os.system(grid_path)

