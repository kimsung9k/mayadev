import maya.cmds as cmds
from sgMaya import sgCmds
sels = cmds.ls( sl=1 )

def setMatrixPreventChildren( target, moveTarget ):
    targetChildren = cmds.listRelatives( target, c=1, type='transform', f=1 )
    if not targetChildren: targetChildren = []
    poses = []
    for targetChild in targetChildren:
        pose = cmds.xform( targetChild, q=1, ws=1, matrix=1 )
        poses.append( pose )
    
    cmds.xform( target, ws=1, matrix= cmds.getAttr( moveTarget + '.wm' ) )
    
    for i in range( len( targetChildren ) ):
        cmds.xform( targetChildren[i], ws=1, matrix= poses[i] )

for sel in sels[:-1]:
    if sgCmds.getShape( sel ):
        sgCmds.setGeometryMatrixToTarget( sel, sels[-1] )
    setMatrixPreventChildren( sel, sels[-1] )