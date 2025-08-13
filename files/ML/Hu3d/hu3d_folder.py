import os,glob
import torch
from PIL import Image


from hy3dgen.rembg import BackgroundRemover
from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline, FaceReducer, FloaterRemover, DegenerateFaceRemover

from mmgp import offload

from hy3dgen.texgen import Hunyuan3DPaintPipeline
#model_path = 'tencent/Hunyuan3D-2'
#texgen_worker = Hunyuan3DPaintPipeline.from_pretrained(model_path)
#i23d_worker = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(model_path)

# Uses Local Files only
model_path = 'tencent/Hunyuan3D-2'
texgen_worker = Hunyuan3DPaintPipeline.from_pretrained(model_path, local_files_only=True)
i23d_worker = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(model_path, local_files_only=True)


pipe = offload.extract_models("i23d_worker", i23d_worker)
pipe.update(  offload.extract_models( "texgen_worker", texgen_worker))

kwargs = {}
kwargs["pinnedMemory"] = "i23d_worker/model"
offload.profile(pipe, profile_no = 3, verboseLevel = int(1), **kwargs)
  

def image_to_3d(image_path='assets/demo.png'):
	rembg = BackgroundRemover()
	

	image = Image.open(image_path)
	#image = image.resize((1024, 1024))

	if image.mode == 'RGB':
		image = rembg(image)

	print("Processing Mesh")
	mesh = i23d_worker(image=image, num_inference_steps=30, mc_algo='mc',
					generator=torch.manual_seed(2025))[0]
	print("MESH GENERATED")
	mesh = FloaterRemover()(mesh)
	mesh = DegenerateFaceRemover()(mesh)
	mesh = FaceReducer()(mesh)
	#mesh.export("out/" + os.path.basename(image_path) + 'mesh.glb')
	#print("MESH EXPORTED")
	#mesh.export( image_path + '.glb',include_normals=True)
	
	
	print("Pipeline loaded, Texturing")
	textured_mesh = texgen_worker(mesh, image)
	print("Exporting Mesh")
	#textured_mesh.export( "out/" + os.path.basename(image_path) + '.glb',include_normals=True)
	textured_mesh.export( image_path + '.glb',include_normals=True)
	
	
	


if __name__ == '__main__':
	#image_to_3d()
	print("CONVERTING FOLDER:")
	print(os.environ["SRC_DIR"])
	print("IMAGES:")
	
	images = glob.glob(os.environ["SRC_DIR"] + "/*.jpg")
	images += glob.glob(os.environ["SRC_DIR"] + "/*.png")
	for img in images:
		print(img)
		if os.path.isfile(img + '.glb'):
			print("Already converted,skippong: ", img)
		else:
			image_to_3d(image_path = img)
		
		

	
