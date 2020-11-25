import hou

def extractBoxTransform(geo):
    # Extrects Box Transforms from the geo
    p = []
    for prim in geo.prims():
        p += [prim.positionAtInterior(0.5,0.5)]
    
    center = (p[4]+p[5]) * 0.5
    dx = (p[1] - p[3]).length()
    dy = (p[5] - p[4]).length()
    dz = (p[2] - p[0]).length()
    size = hou.Vector3(dx,dy,dz)

    yax = (p[5] - p[4]).normalized()
    xax = (p[1] - p[3]).normalized()
    zax = (p[2] - p[0]).normalized()
    m = hou.Matrix3(
    [xax.x(),xax.y(),xax.z(),
    yax.x(),yax.y(),yax.z(),
    zax.x(),zax.y(),zax.z()])
    rotates =  m.extractRotates()
    return [center,size,rotates]

def pointsToBox(pos):
    minx = min(pos[0].x(),pos[1].x())
    maxx = max(pos[0].x(),pos[1].x())
    sx = maxx - minx;
    tx = minx + sx*0.5;
    
    miny = min(pos[0].y(),pos[1].y())
    maxy = max(pos[0].y(),pos[1].y())
    sy = maxy - miny;
    ty = miny + sy*0.5;
    
    minz = min(pos[0].z(),pos[1].z())
    maxz = max(pos[0].z(),pos[1].z())
    sz = maxz - minz;
    tz = minz + sz*0.5;
    return  [hou.Vector3(tx,ty,tz) , hou.Vector3(sx,sy,sz)]

def test():
    print ("tests")
