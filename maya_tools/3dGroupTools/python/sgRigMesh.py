import maya.cmds as cmds
import sgModelDag


def createMeshInstersectPointObject( sourcePointObject, destPointObject, mesh ):
    
    meshShape = sgModelDag.getShape( mesh )
    
    dcmpSrc = cmds.createNode( 'decomposeMatrix' )
    dcmpDst = cmds.createNode( 'decomposeMatrix' )
    intersectNode = cmds.createNode( 'sgMeshIntersect' )
    
    cmds.connectAttr( sourcePointObject+'.wm', dcmpSrc+'.imat' )
    cmds.connectAttr( destPointObject  +'.wm', dcmpDst+'.imat' )
    
    cmds.connectAttr( mesh+'.wm', intersectNode+'.inputMeshMatrix' )
    cmds.connectAttr( meshShape+'.outMesh', intersectNode+'.inputMesh' )
    cmds.connectAttr( dcmpSrc+'.ot', intersectNode+'.pointSource' )
    cmds.connectAttr( dcmpDst+'.ot', intersectNode+'.pointDest' )

    trObj = cmds.createNode( 'transform' )
    cmds.setAttr( trObj+'.dh', 1 )
    
    crv = cmds.curve( p=[[0,0,0],[0,0,0]], d=1 )
    cmds.setAttr( crv+'.template', 1 )
    crvShape = cmds.listRelatives( crv, s=1 )[0]
    mmdcSource = cmds.createNode( 'sgMultMatrixDecompose' )
    mmdcDest   = cmds.createNode( 'sgMultMatrixDecompose' )
    cmds.connectAttr( sourcePointObject+'.wm', mmdcSource+'.i[0]' )
    cmds.connectAttr( destPointObject+'.wm',   mmdcDest+'.i[0]' )
    cmds.connectAttr( crv+'.wim', mmdcSource+'.i[1]' )
    cmds.connectAttr( crv+'.wim', mmdcDest+'.i[1]' )
    cmds.connectAttr( mmdcSource+'.ot', crvShape+'.controlPoints[0]' )
    cmds.connectAttr( mmdcDest+'.ot',   crvShape+'.controlPoints[1]' )
    
    cmds.connectAttr( trObj+'.pim', intersectNode+'.pim' )
    cmds.connectAttr( intersectNode+'.outPoint', trObj+'.t' )
    
    return trObj, crv




def setOrigNormalSoft( target ):
    
    ioMeshs = sgModelDag.getIntermediateObjects( target )
    
    for ioMesh in ioMeshs:
        mesh = cmds.createNode( 'mesh' )
        meshObj = sgModelDag.getTransform( mesh )
        cmds.connectAttr( ioMesh+'.outMesh', mesh+'.inMesh' )
        cmds.refresh()
        cmds.disconnectAttr( ioMesh+'.outMesh', mesh+'.inMesh' )
        cmds.polyNormalPerVertex( mesh, ufn=1 )
        cmds.polySoftEdge( mesh, a=180, ch=1 )
        cmds.connectAttr( mesh+'.outMesh', ioMesh+'.inMesh' )
        cmds.refresh()
        cmds.disconnectAttr( mesh+'.outMesh', ioMesh+'.inMesh' )
        cmds.delete( meshObj )



def setMultiObjectCombine( models ):
    
    first = models[0]
    others = models[1:]
    
    firstOrigShape = sgModelDag.getOrigShape( first )

    for other in others:
        if not cmds.objExists( other ): continue
        otherOrigShape = sgModelDag.getOrigShape( other )
        if firstOrigShape == otherOrigShape: continue
        if cmds.isConnected( firstOrigShape+'.outMesh', otherOrigShape+'.inMesh' ): continue
        cmds.connectAttr( firstOrigShape+'.outMesh', otherOrigShape+'.inMesh', f=1 )



def cleanMesh():
    sels = cmds.ls( type='mesh' )
    
    targets = []
    
    for sel in sels:
        if cmds.getAttr( sel+'.io' ): continue
        selObj = cmds.listRelatives( sel, p=1 )[0]
        targets.append( selObj )
    
    cmds.select( targets )


mc_selectOrigMesh = """import maya.cmds as cmds
import sgModelDag
sels = cmds.ls( sl=1 )

origMeshs = []

for sel in sels:
    shape = sgModelDag.getShape( sel )
    if cmds.nodeType( shape ) != 'mesh':
        continue
    origMesh = sgModelDag.getOrigShape( sel )
    origMeshs.append( origMesh )

if origMeshs:cmds.select( origMeshs )"""


mc_setOrigNormalSoft = """import maya.cmds as cmds
import sgRigMesh
sels = cmds.ls( sl=1 )
for sel in sels:
    sgRigMesh.setOrigNormalSoft( sel )
"""


mc_cleanMesh = """import sgRigMesh
sgRigMesh.cleanMesh()
"""