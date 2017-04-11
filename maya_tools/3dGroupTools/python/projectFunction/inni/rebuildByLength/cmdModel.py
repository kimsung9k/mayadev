import maya.cmds as cmds


def rebuildByLength( rate ):
    
    sels = cmds.ls( sl=1 )
    
    info = cmds.createNode( 'curveInfo' )
    for sel in sels:
        if cmds.nodeType( sel ) == 'transform':
            sel = cmds.listRelatives( sel, s=1 )[0]
        
        
        if not cmds.isConnected( sel+'.local', info+'.inputCurve' ):
            cmds.connectAttr( sel+'.local', info+'.inputCurve', f=1 )
        length = cmds.getAttr( info+'.arcLength' )
        cmds.rebuildCurve( sel, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=0, kt=0, s=length*rate, tol=0.01 )
    
    cmds.delete( info )
    
    cmds.select( sels )