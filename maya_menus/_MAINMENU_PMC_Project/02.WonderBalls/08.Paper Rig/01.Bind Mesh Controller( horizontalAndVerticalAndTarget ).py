from sgMaya import sgCmds
import pymel.core

def getDigitNumFromName( name ):
    firstLocalName = name.split( '|' )[-1]
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
    if not digitIndices: return None
    return int( name[ digitIndices[0]: digitIndices[1]+1 ] )

sels = pymel.core.ls( sl=1 )

vertical = None
horizontal = None
target = None
for sel in sels:
    bb = pymel.core.exactWorldBoundingBox( sel.getShape() )
    xDist = bb[3] - bb[0]
    zDist = bb[5] - bb[2]
    
    print sel, xDist, zDist
    
    if xDist * 2 < zDist:
        vertical = sel
    elif zDist * 2 < xDist:
        horizontal = sel
    else:
        target = sel

indexFirst = getDigitNumFromName( vertical.name() )
indexSecond = getDigitNumFromName( horizontal.name() )
target.rename( 'Ctl_dt_%02d_%02d' %( indexFirst,indexSecond ) )


def setVerticalAndHorizontalControledCtl( verticalCtl, horizontalCtl, targetCtl ):
    
    pTargetCtl     = targetCtl.getParent()
    pivTargetCtl   = pTargetCtl.getParent()
    
    def getPivotCtl( targetCtl ):
        if not pymel.core.objExists( 'Piv' + target.nodeName() ):
            targetPivot = sgCmds.makeParent( target.getParent() )
            targetPivot.rename( 'Piv' + target.nodeName() )
        else:
            targetPivot = target.getParent().getParent()
        return targetPivot
    
    def getMultMatrix( targetCtl, baseCtl ):    
        mm = pymel.core.createNode( 'multMatrix' )
        pivotCtl = getPivotCtl( targetCtl )
        pivotCtl.wm >> mm.i[0]
        baseCtl.pim >> mm.i[1]
        baseCtl.wm >> mm.i[2]
        pivotCtl.wim >> mm.i[3]
        return mm
    
    mmVertical = getMultMatrix( pivTargetCtl, verticalCtl )
    mmHorizontal = getMultMatrix( pivTargetCtl, horizontalCtl )
    addMtx = pymel.core.createNode( 'addMatrix' )
    dcmpVertical = sgCmds.getDecomposeMatrix( mmVertical.o )
    dcmpHorizontal = sgCmds.getDecomposeMatrix( mmHorizontal.o )
    
    transAdd = pymel.core.createNode( 'plusMinusAverage' )
    scaleAdd = pymel.core.createNode( 'plusMinusAverage' )
    scaleAdd.op.set( 3 )
    
    rotAddMtx = pymel.core.createNode( 'addMatrix' )
    rotDcmp   = sgCmds.getDecomposeMatrix( rotAddMtx.matrixSum )
    
    dcmpVertical.ot >> transAdd.input3D[0]
    dcmpHorizontal.ot >> transAdd.input3D[1]
    dcmpVertical.os >> scaleAdd.input3D[0]
    dcmpHorizontal.os >> scaleAdd.input3D[1]
    mmVertical.o >> rotAddMtx.matrixIn[0]
    mmHorizontal.o >> rotAddMtx.matrixIn[1]

    transAdd.output3D >> pTargetCtl.t
    scaleAdd.output3D >> pTargetCtl.s
    rotDcmp.outputRotate >> pTargetCtl.r

setVerticalAndHorizontalControledCtl( vertical, horizontal, target )