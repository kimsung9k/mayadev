from sgModules import sgcommands
import maya.cmds as cmds

sels = cmds.ls( sl=1 )
for sel in sels:
    cmds.select( sel )
    cmds.DeleteHistory()
    pivMtx = sgcommands.getPivotMatrix( sel )
    worldMtx = sgcommands.listToMatrix( cmds.getAttr( sel + '.wm' ) )
    worldPivMtx = pivMtx * worldMtx
    tempTr = cmds.createNode( 'transform' )
    cmds.xform( tempTr, ws=1, matrix=sgcommands.matrixToList( worldPivMtx ) )
    sgcommands.setGeometryMatrixToTarget( sel, tempTr )
    cmds.delete( tempTr )
cmds.select( sels )
cmds.DeleteHistory()

for sel in sels:
    selShape = cmds.listRelatives( sel, s=1, f=1 )[0]
    engine = cmds.listConnections( selShape, type='shadingEngine' )
    if not engine: continue
    cmds.sets( sel, e=1, forceElement = engine[0] )