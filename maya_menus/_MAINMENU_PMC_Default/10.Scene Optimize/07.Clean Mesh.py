import maya.cmds as cmds

def cleanMeshInScene( *args ):

    def cleanMesh( targetObj ):
    
        targetShapes = cmds.listRelatives( targetObj, s=1, f=1 )
        for targetShape in targetShapes:
            if not cmds.getAttr( targetShape+'.io' ): continue
            if cmds.listConnections( targetShape, s=0, d=1 ): continue 
            cmds.delete( targetShape )
            cmds.warning( "%s is deleted" % targetShape )
    
    meshs = cmds.ls( type='mesh' )
    
    meshObjs = []
    for mesh in meshs:
        if cmds.getAttr( mesh+'.io' ): continue
        meshP = cmds.listRelatives( mesh, p=1, f=1 )[0]
        if meshP in meshObjs: continue
        meshObjs.append( meshP ) 
    
    for meshObj in meshObjs:
        cleanMesh( meshObj )

cleanMeshInScene()