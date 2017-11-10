from sgModules import sgcommands
import maya.cmds as cmds
import pymel.core

sels = cmds.ls( sl=1 )
for sel in sels:
    pymelSel = pymel.core.ls( sel )[0]
    pymelSel.rotatePivot.set( 0,0,0 )
    pymelSel.scalePivot.set( 0,0,0 )
    pymelSel.rotatePivotTranslate.set( 0,0,0 )
    pymelSel.scalePivotTranslate.set( 0,0,0 )
    
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