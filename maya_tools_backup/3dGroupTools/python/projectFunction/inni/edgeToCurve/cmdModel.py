import maya.cmds as cmds

def createCurveFromEdge( value, degree=3 ):
    
    print "degree : ", degree
    sels = cmds.ls( sl=1 )
    if not sels: return None
    
    if cmds.nodeType( sels[0] ) == 'transform':
        sels[0] = cmds.listRelatives( sels[0], s=1 )[0]
    if cmds.nodeType( sels[0] ) == 'nurbsCurve':
        if not value: return None
        cmds.rebuildCurve( sels[0], ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=0, kt=0, s=value, tol=0.01 )
    else:
        curveObject, node = cmds.polyToCurve( form=0, degree=degree )
        crvShape= cmds.listRelatives( curveObject, s=1 )[0]
        cmds.setAttr( crvShape+'.dispCV', 1 )
        if value:
            cmds.rebuildCurve( curveObject, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=0, kt=0, s=value, tol=0.01 )
        
    


def cvOnOff():
    
    sels = cmds.ls( sl=1 )
    for sel in sels:
        if cmds.nodeType( sel ) == 'transform':
            selShape = cmds.listRelatives( sel, s=1 )[0]
        else:
            selShape = sel
        if cmds.getAttr( selShape+'.dispCV'):
            cmds.setAttr( selShape+'.dispCV', 0 )
        else:
            cmds.setAttr( selShape+'.dispCV', 1 )