import pymel.core
from sgMaya import sgCmds

def getPointers( centerPoint, endPoint ):
    
    middlePoint = [ (centerPoint[i] + endPoint[i])/2.0 for i in range( 3 ) ]
    
    centerPointer = pymel.core.createNode( 'transform' )
    endPointer = pymel.core.createNode( 'transform' )
    middlePointer = pymel.core.createNode( 'transform' )
    centerPointer.dh.set( 1 )
    endPointer.dh.set( 1 )
    middlePointer.dh.set( 1 )
    
    centerPointer.t.set( centerPoint )
    endPointer.t.set( endPoint )
    middlePointer.t.set( middlePoint )
    
    staticMiddle = pymel.core.duplicate( middlePointer )[0]
    moveMiddle   = pymel.core.duplicate( middlePointer )[0]
    
    pymel.core.parent( moveMiddle, endPointer, centerPointer )
    
    sgCmds.blendTwoMatrixConnect( moveMiddle, staticMiddle, middlePointer, ct=1 )
    return centerPointer, middlePointer, endPointer, staticMiddle, moveMiddle


sels = pymel.core.ls( sl=1 )

for mainCtl in sels:
    
    bb = pymel.core.exactWorldBoundingBox( mainCtl.getShape() )
    
    mainCtlPos = pymel.core.xform( mainCtl, q=1, ws=1, t=1 )
    
    minPoint = [ bb[0], 0, mainCtlPos[2] ]
    centerPoint = mainCtlPos
    maxPoint = [ bb[3], 0, mainCtlPos[2] ]
    
    minCenter, minMiddle, minEnd, minStatic, minMove = getPointers( centerPoint, minPoint )
    maxCenter, maxMiddle, maxEnd, maxStatic, maxMove = getPointers( centerPoint, maxPoint )
    
    sgCmds.addOptionAttribute( mainCtl )
    sgCmds.addAttr( mainCtl, ln='bendMin', k=1 )
    sgCmds.addAttr( mainCtl, ln='bendMax', k=1 )
    sgCmds.addAttr( mainCtl, ln='bendMinRounding', k=1, min=0, max=10, dv=10 )
    sgCmds.addAttr( mainCtl, ln='bendMaxRounding', k=1, min=0, max=10, dv=10 )

    multMax  = pymel.core.createNode( 'multDoubleLinear' )
    multMin  = pymel.core.createNode( 'multDoubleLinear' )
    multMaxRounging  = pymel.core.createNode( 'multDoubleLinear' )
    multMinRounging  = pymel.core.createNode( 'multDoubleLinear' )
    
    mainCtl.attr( 'bendMin' ) >> multMin.input1
    multMin.input2.set( -1 )
    multMin.output >> minCenter.rz
    
    mainCtl.attr( 'bendMax' ) >> multMax.input1
    multMax.input2.set( 1 )
    multMax.output >> maxCenter.rz
    
    mainCtl.attr( 'bendMinRounding' ) >> multMinRounging.input1
    multMinRounging.input2.set( .1 )
    multMinRounging.output >> minMiddle.blend
    
    mainCtl.attr( 'bendMaxRounding' ) >> multMaxRounging.input1
    multMaxRounging.input2.set( .1 )
    multMaxRounging.output >> maxMiddle.blend
    
    
    grp = pymel.core.createNode( 'transform' )
    pymel.core.xform( grp, ws=1, matrix=mainCtl.wm.get() )
    pymel.core.parent( minCenter, minMiddle, minStatic, grp )
    pymel.core.parent( maxCenter, maxMiddle, maxStatic, grp )
    
    curve = sgCmds.makeCurveFromSelection( minEnd, minMiddle, minCenter, maxMiddle, maxEnd )
    curve.setParent( grp )
    