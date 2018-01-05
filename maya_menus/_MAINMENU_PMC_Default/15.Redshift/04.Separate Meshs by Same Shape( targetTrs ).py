import pymel.core
from sgMaya import sgCmds
from maya import cmds, OpenMaya, mel
import ntpath, os


def getBoundingBoxDistStr( sel ):
    
    bbMin = sel.getShape().boundingBoxMin.get()
    bbMax = sel.getShape().boundingBoxMax.get()
    
    minPoint = OpenMaya.MPoint( *bbMin )
    maxPoint = OpenMaya.MPoint( *bbMax )
    
    dist = minPoint.distanceTo( maxPoint )
    startSum = minPoint.x + minPoint.y + minPoint.z
    
    distStr = ( '%.3f' % (dist + startSum) ).replace( '.', '_' )
    return distStr
       

def isVisible( target ):
    allParents = target.getAllParents()
    allParents.append( target )
    for parent in allParents:
        if not parent.v.get(): return False
    return True


targetGrps = pymel.core.ls( sl=1 )

resultGrps = []
otherGrps = []

for targetGrp in targetGrps:
    children = targetGrp.listRelatives( c=1, ad=1, type='transform' )
    sels = []

    for child in children:
        if not child.getShape() or child.getShape().nodeType() != 'mesh' or not isVisible( child ): 
            otherGrps.append( child )
            continue
        sels.append( child )
    
    meshs = {}
    
    for sel in sels:
        selShape = sel.getShape()
        numVertices = selShape.numVertices()
        bbStr = getBoundingBoxDistStr( sel )
        keyStr = targetGrp + '_%d_%s' %( numVertices, bbStr )
        if not meshs.has_key( keyStr ):
            meshs[ keyStr ] = [sel]
        else:
            meshs[ keyStr ].append( sel )
    
    if len( meshs.keys() ) != 1:
        for key in meshs.keys():
            grp = pymel.core.group( em=1, n= key )
            grp.setParent( targetGrp )
            pymel.core.xform( grp, os=1, matrix=[1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1] )
            pymel.core.parent( meshs[key], grp )
            resultGrps.append( grp )

pymel.core.delete( otherGrps )

pymel.core.select( resultGrps )

