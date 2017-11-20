import pymel.core
from sgMaya import sgCmds
from maya import cmds
import ntpath, os


def renameSelOrder( sels ):
    firstName = sels[0].name()
    firstLocalName = firstName.split( '|' )[-1]
    
    digitIndices = []
    for i in range( len( firstLocalName ) ):
        if firstLocalName[i].isdigit():
            if len( digitIndices ):
                if i == digitIndices[-1]+1:
                    digitIndices.append( i )
                else:
                    digitIndices = [i]
            else:
                digitIndices.append( i )
    
    if digitIndices:
        sepNameFront = firstLocalName[:digitIndices[0]]
        sepNameBack  = firstLocalName[digitIndices[-1]+1:]
        
        numFormat = "%0" + str(len( digitIndices )) + "d"
        
        startNum = int( firstLocalName[digitIndices[0]:digitIndices[-1]+1] )
        fullNameFormat = sepNameFront + numFormat + sepNameBack
    else:
        startNum = 0
        fullNameFormat = firstName.split( '|' )[-1] + '%02d'
        
    for sel in sels:
        sel.rename( fullNameFormat % startNum )
        startNum += 1
        

def getBoundingBoxDistStr( sel ):
    
    bbMin = sel.getShape().boundingBoxMin.get()
    bbMax = sel.getShape().boundingBoxMax.get()
    
    minPoint = OpenMaya.MPoint( *bbMin )
    maxPoint = OpenMaya.MPoint( *bbMax )
    
    dist = minPoint.distanceTo( maxPoint )
    distStr = ('%.3f' % dist ).replace( '.', '_' )
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
    
    renameSelOrder( sels )
    
    for sel in sels:
        selShape = sel.getShape()
        numVertices = selShape.numVertices()
        bbStr = getBoundingBoxDistStr( sel )
        keyStr = 'mesh_%d_%s' %( numVertices, bbStr )
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

