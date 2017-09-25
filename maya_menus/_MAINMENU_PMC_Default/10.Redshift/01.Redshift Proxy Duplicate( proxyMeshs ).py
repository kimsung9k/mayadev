import pymel.core
from sgMaya import sgCmds

sels = pymel.core.ls( sl=1 )

for sel in sels:
    proxyMesh = sgCmds.getNodeFromHistory( sel, 'RedshiftProxyMesh' )
    if not proxyMesh: continue
    
    mesh = pymel.core.createNode( 'mesh' )
    meshObj = mesh.getParent()
    meshObj.rename( sel )
    proxyMesh[0].outMesh >> mesh.inMesh
    
    selP = sel.getParent()
    if selP:
        meshObj.setParent( selP )
    pymel.core.xform( meshObj, ws=1, matrix=sel.wm.get() )