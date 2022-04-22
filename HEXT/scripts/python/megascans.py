from glob import glob
    
    
    
def AssetFolder(mega_folder, asset_id):
    folder = glob(mega_folder + "Downloaded/3d/*" +  asset_id)[0]    
    return folder


def HighFile(asset_folder, asset_id):
    file = glob(asset_folder + "/*" + asset_id + "_High.fbx")[0]
    return file
    
def Get3DAssets(mega_folder):
    return glob(mega_folder + "Downloaded/3d/*")
