import hou

ocl_types = { "vector":2, "float":1, "vector4":3, "int":0, "menu":0 ,"bool":0}
ocl_val_types = {  "vector":"v3", "float":"f", "vector4":"v4", "int":"int", "menu":"int" ,"bool":"int"}
ocl_kernel_types = { "vector":"float3", "float":"float", "vector4":"float4", "int":"int", "menu":"int" ,"bool":"int"}

# Split OCL Kernel code
def split_ocl_code(code,kernel_name):
    kernel_split = f"kernel void {kernel_name}("
    [before_kernel,code] = code.split(kernel_split)
    [parms,code] =  code.split(")",1)
    [kernel_function,after_kernel_function] = code.split("}",1)
    return [before_kernel,kernel_split,parms,kernel_function,after_kernel_function]

def join_ocl_code(blocks):
    return blocks[0] + blocks[1] + blocks[2] + ")" + blocks[3] + "}" + blocks[4]

def get_ocl_node_code(n):
    kernel_name = n.parm("kernelname").eval()
    code = n.parm("kernelcode").eval()    
    code = split_ocl_code(code,kernel_name)
    return code
    
# Add OCL Parameter Based on Type
def add_ocl_kernel_parm(n,type,name):
    code = get_ocl_node_code(n)
    code[2] = code[2][0:-1]
    new_parm = f"{ocl_kernel_types[type]} {name}"
    code[2] += f",\n\t\t {new_parm}\n"
    
    code = join_ocl_code(code)
    n.parm("kernelcode").set(code)
    
# Basic User panel code
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
    add_ocl_kernel_parm(n,type,name)
    
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
      
        if type in ["noise","vnoise"]:
            add_OCL_Noise(n,name,type)
            
        else:
            # create parm
            user_parm = create_OCL_user_parm(n,name,type,val,noise_name)
            if not name in bindings:
                add_OCL_parm(n,type,name,user_parm)    

# Basic Noise
def add_OCL_Noise(n,noise_name,type):  
    if type == "noise":
        noise_dict = """float amp 1
                float freq 1
                vector4 freqmult 1
                vector4 offset 0
                float rough 0.5
                int octaves 9"""  
    if type == "vnoise":
        noise_dict = """bool invert 0
            float iso 0
            float cut 2
            float amp 1
            float freq 1
            vector freqmult 1
            vector offset 0
            int seed 0
            menu shape f1,f1-f2,seed"""    
    
    # CreateNoiseFolder
    ptg = n.parmTemplateGroup()
    noise_folder = hou.FolderParmTemplate(noise_name,noise_name,folder_type = hou.folderType.Simple)
    ptg.appendToFolder(ptg.find("Parameters"),noise_folder)
    n.setParmTemplateGroup(ptg)
    # Add Parms
    process_OCL_Lines(noise_dict.splitlines(),n ,noise_name)  
    
    # Add Function Line
    name = noise_name
    if type == "noise":
        func_str = f"\n    float3 {name} = Noise3(vp,{name}_amp,{name}_freq*{name}_freqmult,{name}_rough,{name}_octaves,{name}_offset);\n"
    if type == "vnoise":
        func_str = f"\n    float {name} ={name}_amp * min((1 - 2*{name}_invert) * ({name}_iso + LZ_Voronoi_all((vp+{name}_offset)*{name}_freq*{name}_freqmult,{name}_seed,{name}_shape)),{name}_cut);\n"
        func_str += f"    float {name}_outseed = LZ_Voronoi_all((vp+{name}_offset)*{name}_freq*{name}_freqmult,{name}_seed,2);\n"
    add_OCL_codeline_safe(n,func_str)
    
# Add OCL NOISE function
def add_OCL_codeline(n,codeline):
    code = get_ocl_node_code(n)  
    code[3] += codeline    
    code = join_ocl_code(code)
    n.parm("kernelcode").set(code)
    
def add_OCL_codeline_safe(n,codeline):
    if not codeline in n.parm("kernelcode").eval():
        add_OCL_codeline(n,codeline)

def AddUserInterface(n):
    ptg = n.parmTemplateGroup()    
    folder = hou.FolderParmTemplate('User','User',folder_type = hou.folderType.Tabs )       
    first_folder = ptg.entryAtIndices([0])
    ptg.insertBefore(first_folder,folder)

    hou_parm_template = hou.StringParmTemplate("parms", "Parms", 1, default_value=(["//vector offset 1,2,3\n//float iso 0\n//bool invert 1\n//menu shape sphere,plane,caves\n//noise n0 1\n//noise n1 1\n//vnoise vn0 1\n\n  "]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.Regular, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal)
    hou_parm_template.setScriptCallbackLanguage(hou.scriptLanguage.Python)
    hou_parm_template.setTags({"editor": "1", "editorlang": "vex", "editorlines": "5-20", "script_action": "import lzocl\nlzocl.process_OclLinesParm( kwargs['parmtuple'] )\n", "script_callback_language": "python"})
    ptg.appendToFolder('User',hou_parm_template)

    Parms_folder = hou.FolderParmTemplate('Parameters','Parameters',folder_type = hou.folderType.Simple )       
    ptg.appendToFolder('User',Parms_folder)

    n.setParmTemplateGroup(ptg)


def basicSurfaceOcl(n):
    n.parm("stdswitcher1").set(1)
    n.parm("usecode").set(1)
    n.parm("kernelcode").set('#include <gxnoise.h>\n#include "interpolate.h" \n#include <random.h>\n#include <LZ_noises.h>\nfloat lerpConstant( constant float * in, int size, float pos);\n\nkernel void kernelName( \n                 int stride_x, \n                 int stride_y, \n                 int stride_z, \n                 int stride_offset, \n                 int res_x, \n                 int res_y, \n                 int res_z, \n                 float voxelsize_x, \n                 float voxelsize_y, \n                 float voxelsize_z, \n                 float16 xformtoworld, \n                 global float * surface \n)\n{\n    // GET idx\n    int x = get_global_id(0);\n    int y = get_global_id(1);\n    int z = get_global_id(2);\n    int idx = stride_offset + stride_x*x + stride_y*y + stride_z*z;\n    \n    // Get world position (without rotations though)  voxel_position\n    float3 vp = (float3)(x*voxelsize_x,y*voxelsize_y,z*voxelsize_z);     \n    vp += xformtoworld.hi.hi.xyz;                         \n\n    \n    \n}\n')
    n.parm("kerneloptions").set('-I $HEXT/ocl')
    n.parm("runover").set(1)
    n.parm("stdswitcher_child_1").set(1)
    n.parm("bindings1_name").set('surface')
    n.parm("bindings1_type").set(6)
    n.parm("bindings1_volume").set('surface')
    n.parm("bindings1_forcealign").set(0)
    n.parm("bindings1_resolution").set(1)
    n.parm("bindings1_voxelsize").set(1)
    n.parm("bindings1_xformtoworld").set(1)
    n.parm("bindings1_writeable").set(1)
    n.parm("bindings1_ramp2pos").set(1.0)
    n.parm("bindings1_ramp2value").set(1.0)
    AddUserInterface(n)