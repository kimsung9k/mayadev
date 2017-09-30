import maya.cmds as cmds
from sgModules import sgcommands

sels = cmds.ls( sl=1 )

for i in range( len( sels ) -1 ):
    sels[i] = cmds.parent( sels[i], sels[i+1] )[0]
    if cmds.nodeType( sels[i] ) == 'joint':
        sgJoint = sgcommands.convertSg( sels[i] )
        mtx = sgJoint.wm.get()
        cmds.setAttr( sels[i] + '.jo', 0,0,0 )
        sgJoint.xform( ws=1, matrix= mtx )
        