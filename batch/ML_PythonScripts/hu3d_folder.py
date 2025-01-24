import os,glob
import torch
from PIL import Image


from hy3dgen.rembg import BackgroundRemover
from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline, FaceReducer, FloaterRemover, DegenerateFaceRemover
from hy3dgen.text2image import HunyuanDiTPipeline


def image_to_3d(image_path='assets/demo.png'):
    rembg = BackgroundRemover()
    model_path = 'tencent/Hunyuan3D-2'

    image = Image.open(image_path)
    image = image.resize((1024, 1024))

    if image.mode == 'RGB':
        image = rembg(image)

    pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(model_path)

    mesh = pipeline(image=image, num_inference_steps=30, mc_algo='mc',
                    generator=torch.manual_seed(2025))[0]
    mesh = FloaterRemover()(mesh)
    mesh = DegenerateFaceRemover()(mesh)
    mesh = FaceReducer()(mesh)
    #mesh.export('mesh.glb')

    try:
        from hy3dgen.texgen import Hunyuan3DPaintPipeline
        pipeline = Hunyuan3DPaintPipeline.from_pretrained(model_path)
        mesh = pipeline(mesh, image=image)
        mesh.export( image_path + '.glb')
    except Exception as e:
        print(e)
        print('Please try to install requirements by following README.md')

if __name__ == '__main__':
    #image_to_3d()
	print("CONVERTING FOLDER:")
	print(os.environ["SRC_DIR"])
	print("IMAGES:")
	
	images = glob.glob(os.environ["SRC_DIR"] + "/*.jpg")
	images += glob.glob(os.environ["SRC_DIR"] + "/*.png")
	for img in images:
		print(img)
		image_to_3d(image_path = img)
		
		
	
	
