import maya.cmds as cmds


def goToTarget( first, second ):
    
    tr = cmds.xform( second, q=1, ws=1, piv=1 )[:3]
    ro = cmds.xform( second, q=1, ws=1, ro =1 )[:3]
    
    cmds.move( tr[0], tr[1], tr[2], first, ws=1 )
    cmds.rotate( ro[0], ro[1], ro[2], first, ws=1 )
    
    
    
    
def goToTargetPosition( first, second ):
    
    tr = cmds.xform( second, q=1, ws=1, piv=1 )[:3]
    cmds.move( tr[0], tr[1], tr[2], first, ws=1 )
    
    
    
def goToTargetOrient( first, second ):
    
    ro = cmds.xform( second, q=1, ws=1, ro=1 )[:3]
    cmds.rotate( ro[0], ro[1], ro[2], second, ws=1 )
    
    
    
    
def uiCmd_goToTarget( *args ):
    
    selections = cmds.ls( sl=1, tr=1 )
    
    last = selections[-1]
    
    for selection in selections[:-1]:
        goToTarget( selection, last )
        
        
        
def uiCmd_goToTargetPosition( *args ):
    
    selections = cmds.ls( sl=1, tr=1 )
    
    last = selections[-1]
    
    for selection in selections[:-1]:
        goToTargetPosition( selection, last )
        
        
        
def uiCmd_goToTargetOrient( *args ):
    
    selections = cmds.ls( sl=1, tr=1 )
    
    last = selections[-1]
    
    for selection in selections[:-1]:
        goToTargetOrient( selection, last )