import maya.cmds as cmds



def isNode( target ):
    
    return cmds.objExists( target )



def isTransformNode( target ):
    
    if not isNode( target ): return False
    if cmds.nodeType( target ) in ["joint", "transform"]: return True
    return False



def isShapeNode( target ):
    
    if not isNode( target ): return False
    if cmds.ls( target, s=1 ): return True
    return False



def isMesh( target ):
    
    if not isNode( target ): return False
    return cmds.nodeType( target ) == "mesh"


def isJoint( target ):
    return cmds.nodeType( target ) == 'joint'



def isDefault( transformNode ):
    
    import math
    
    trValues = cmds.getAttr( transformNode + '.t' )[0]
    for trValue in trValues:
        if math.fabs( trValue ) > 0.0001: return False
    rotValues = cmds.getAttr( transformNode + '.r' )[0]
    for rotValue in rotValues:
        if math.fabs( rotValue ) > 0.0001: return False
    scaleValues = cmds.getAttr( transformNode + '.s' )[0]
    for scaleValue in scaleValues:
        if math.fabs( scaleValue ) > 1.0001 or math.fabs( scaleValue ) < 0.9999: return False
    shearValues = cmds.getAttr( transformNode + '.sh' )[0]
    for shearValue in shearValues:
        if math.fabs( shearValue ) > 0.0001: return False
    
    return True
    
    