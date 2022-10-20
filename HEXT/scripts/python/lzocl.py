import hou

ocl_types = { "vector":2, "float":1, "vector4":3, "int":0, "menu":0 ,"bool":0}
ocl_val_types = {  "vector":"v3", "float":"f", "vector4":"v4", "int":"int", "menu":"int" ,"bool":"int"}

def process_OclLinesParm(parm):    
    parms_string = parm.eval()[0]
    process_OCL_Lines(parms_string.splitlines(),parm.node())


def get_OCL_bindings(n):
    parms = []
    n_bindings = n.parm("bindings").eval()
    for binding in range(0,n_bindings):
        parms += [n.parm(f"bindings{binding+1}_name").eval()]
    return parms
    
def add_OCL_parm(n,type,name,user_parm):
    bindings = n.parm("bindings")
    i =  bindings.eval() + 1
    bindings.set(i)
    n.parm(f"bindings{i}_name").set(name)
    type_id = ocl_types[type]
    n.parm(f"bindings{i}_type").set(type_id)
    
    value_string = f"bindings{i}_{ocl_val_types[type]}val"
    (n.parm(value_string) or n.parmTuple(value_string)).set(user_parm)

   
def create_OCL_user_parm(n,name,type,val,noise_name=""):
    parm = n.parm(name) or n.parmTuple(name)
    if parm is None:
        ptg = n.parmTemplateGroup()
        
        if type == "vector":
            pt = hou.FloatParmTemplate(name,name,3,default_value = val)
        elif type == "vector4":
            pt = hou.FloatParmTemplate(name,name,4,default_value = val)
        elif type == "float":
            pt = hou.FloatParmTemplate(name,name,1,default_value = val)
        elif type == "int":
            pt = hou.IntParmTemplate(name,name,1,default_value = [int(x) for x in val ])
        elif type == "bool":
            pt = hou.ToggleParmTemplate(name,name,default_value = bool(val[0]) )  
        elif type == "menu":
            print(val)
            menu_items = tuple([str(i) for i in range(0,len(val))])
            menu_labels = tuple(val)
            pt = hou.IntParmTemplate(name,name,1,default_value = (0,),menu_items=val,menu_labels=val)            
        
        parent_folder = "Parameters"
        if noise_name != "" : parent_folder = noise_name
        ptg.appendToFolder(ptg.find(parent_folder),pt)    
        n.setParmTemplateGroup(ptg)  
    return n.parm(name) or n.parmTuple(name)
   
def process_OCL_Lines(lines, n , noise_name=""):  
    bindings = get_OCL_bindings(n)
    for line in lines: 
        if line.startswith("//") : continue                     # remove comments
        line = line.strip()
        if not line : continue
        [type,name,val] = line.split(" ")
        if noise_name: name = noise_name + "_" + name
        val = val.split(",")
        if type != "menu": val = [float(x) for x in val]        # Convert to floats
      
        if type == "noise":
            add_OCL_Noise(n,name)
        else:
            # create parm
            user_parm = create_OCL_user_parm(n,name,type,val,noise_name)
            if not name in bindings:
                add_OCL_parm(n,type,name,user_parm)    

def add_OCL_Noise(n,noise_name):    
    noise_dict = """float amp 1
            float freq 1
            vector4 freqmult 1
            vector4 offset 0
            float rough 0.5
            int octaves 9"""    
    
    # CreateNoiseFolder
    ptg = n.parmTemplateGroup()
    noise_folder = hou.FolderParmTemplate(noise_name,noise_name,folder_type = hou.folderType.Simple)
    ptg.appendToFolder(ptg.find("Parameters"),noise_folder)
    n.setParmTemplateGroup(ptg)
    # Add Parms
    process_OCL_Lines(noise_dict.splitlines(),n ,noise_name)       



def AddUserInterface(n):
    ptg = n.parmTemplateGroup()    
    folder = hou.FolderParmTemplate('User','User',folder_type = hou.folderType.Tabs )       
    first_folder = ptg.entryAtIndices([0])
    ptg.insertBefore(first_folder,folder)

    hou_parm_template = hou.StringParmTemplate("parms", "Parms", 1, default_value=(["//vector offset 1,2,3\n//float scale 5\n//bool invert 1\n//menu shape sphere,plane,caves\n//noise noise1 1\n//noise noise2 1\n\n  "]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.Regular, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal)
    hou_parm_template.setScriptCallbackLanguage(hou.scriptLanguage.Python)
    hou_parm_template.setTags({"editor": "1", "editorlang": "vex", "editorlines": "5-20", "script_action": "import lzocl\nlzocl.process_OclLinesParm( kwargs['parmtuple'] )\n", "script_callback_language": "python"})
    ptg.appendToFolder('User',hou_parm_template)

    Parms_folder = hou.FolderParmTemplate('Parameters','Parameters',folder_type = hou.folderType.Simple )       
    ptg.appendToFolder('User',Parms_folder)

    n.setParmTemplateGroup(ptg)
