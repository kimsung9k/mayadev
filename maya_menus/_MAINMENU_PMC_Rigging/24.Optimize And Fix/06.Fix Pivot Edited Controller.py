from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )
transformAttrs = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz' ]

def chunks(l, n):
    returnList = []
    for i in xrange(0, len(l), n):
        returnList.append( l[i:i+n] )
    return returnList

for sel in sels:
    children = sel.listRelatives( c=1, type='transform' )
    childrenMatrix = []
    for child in children:
        childMtx = child.wm.get()
        for attr in transformAttrs:
            child.setAttr( attr, e=1, lock=0, k=1 )
        childrenMatrix.append( childMtx )
    
    shapes = sel.listRelatives( s=1 )
    curveShapes = []
    curvePoints = []
    for shape in shapes:
        if shape.nodeType() == 'nurbsCurve':
            curveShapes.append( shape )
            curvePoints.append( chunks( cmds.xform( shape + '.cv[*]', q=1, ws=1, t=1 ), 3 ) )            
    
    worldPivotMatrix = sgCmds.getPivotLocalMatrix( sel ) * sgCmds.getWorldMatrix( sel )
    pymel.core.xform( sel, ws=1, matrix= sgCmds.matrixToList( worldPivotMatrix ) )
    
    for i in range( len( children ) ):
        pymel.core.xform( children[i], ws=1, matrix=childrenMatrix[i] )
    
    for i in range( len( curveShapes ) ):
        cvs = cmds.ls( curveShapes[i] + '.cv[*]', fl=1 )
        for j in range( len( cvs ) ):
            cmds.xform( cvs[j], ws=1, t=curvePoints[i][j] )
    
    selP = sel.getParent()
    if selP:
        for attr in transformAttrs:
            selP.setAttr( attr, e=1, lock=0, k=1 )
    
    sgCmds.freezeByParent( sel )