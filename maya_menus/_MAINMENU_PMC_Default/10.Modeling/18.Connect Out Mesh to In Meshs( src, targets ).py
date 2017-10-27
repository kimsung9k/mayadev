import maya.cmds as cmds

def getMObject( target ):
    
    mObject = OpenMaya.MObject()
    selList = OpenMaya.MSelectionList()
    selList.add( target )
    selList.getDependNode( 0, mObject )
    return mObject

sels= cmds.ls( sl=1 )

srcMesh = sels[0]
otherMeshs = sels[1:]

srcMeshShape = cmds.listRelatives( srcMesh, s=1, f=1 )[0]

for otherMesh in otherMeshs:
    otherMeshShape = cmds.listRelatives( otherMesh, s=1, f=1 )[0]
    if cmds.isConnected( srcMeshShape + '.outMesh', otherMeshShape + '.inMesh' ): continue
    cmds.connectAttr( srcMeshShape + '.outMesh', otherMeshShape + '.inMesh' )