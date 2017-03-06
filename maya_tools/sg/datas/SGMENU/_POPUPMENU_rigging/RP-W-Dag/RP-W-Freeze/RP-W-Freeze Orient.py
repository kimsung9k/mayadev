from sgModules import sgcommands
from maya import OpenMaya

sels = sgcommands.listNodes( sl=1 )
for sel in sels:
    if sel.nodeType() != 'joint': continue
    mtx = sel.matrix.get()
    
    mMatrix = OpenMaya.MMatrix()
    OpenMaya.MScriptUtil.createMatrixFromList( mtx, mMatrix )
    
    trMtx = OpenMaya.MTransformationMatrix( mMatrix )
    rotVector = trMtx.eulerRotation().asVector()
    rot = [ rotVector.x, rotVector.y, rotVector.z ]
    
    try:
        sel.jo.set( 0,0,0 )
        sel.r.set( *rot )
    except:
        pass