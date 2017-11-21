from sgMaya import sgCmds
import maya.cmds as cmds

sels = cmds.ls( sl=1 )
for sel in sels:
    cmds.select( sel )
    cmds.DeleteHistory()
    pivMtx = sgCmds.getPivotLocalMatrix( sel )
    worldMtx = sgCmds.listToMatrix( cmds.getAttr( sel + '.wm' ) )
    worldPivMtx = pivMtx * worldMtx
    tempTr = cmds.createNode( 'transform' )
    cmds.xform( tempTr, ws=1, matrix=sgCmds.matrixToList( worldPivMtx ) )
    sgCmds.setGeometryMatrixToTarget( sel, tempTr )
    cmds.delete( tempTr )
cmds.select( sels )
cmds.DeleteHistory()

for sel in sels:
    selShape = cmds.listRelatives( sel, s=1, f=1 )[0]
    engine = cmds.listConnections( selShape, type='shadingEngine' )
    if not engine: continue
    cmds.sets( sel, e=1, forceElement = engine[0] )