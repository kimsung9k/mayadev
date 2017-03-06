import maya.cmds as cmds
import maya.OpenMaya as om
import math



def getAimIndex( aimTarget, constTarget ):

    firstPos = om.MPoint( *cmds.xform( aimTarget, q=1, ws=1, t=1 ) )
    secondPos = om.MPoint( *cmds.xform( constTarget, q=1, ws=1, t=1 ) )
    
    secondMatrix = cmds.getAttr( constTarget+'.wm' )
    
    axis1 = om.MVector( *secondMatrix[:3] )
    axis2 = om.MVector( *secondMatrix[4:7] )
    axis3 = om.MVector( *secondMatrix[8:11] )
    
    aimVector = firstPos - secondPos
    vectorList = [ axis1, axis2, axis3 ]
    
    maxDot = 0
    aimIndex = 0
    
    for i in range( len( vectorList ) ):
        dotValue = vectorList[i] * aimVector
        if math.fabs( dotValue ) > math.fabs( maxDot ):
            maxDot = dotValue
            aimIndex = i
            if dotValue < 0: aimIndex += 3
    return aimIndex




def getLookAtMtx( aimTarget, constTarget, aimIndex = None ):
    
    firstPos = om.MPoint( *cmds.xform( aimTarget, q=1, ws=1, t=1 ) )
    secondPos = om.MPoint( *cmds.xform( constTarget, q=1, ws=1, t=1 ) )
    
    secondMatrix = cmds.getAttr( constTarget+'.wm' )
    
    axis1 = om.MVector( *secondMatrix[:3] )
    axis2 = om.MVector( *secondMatrix[4:7] )
    axis3 = om.MVector( *secondMatrix[8:11] )
    
    aimVector = firstPos - secondPos
    vectorList = [ axis1, axis2, axis3 ]
    
    if aimIndex == None:
        maxDot = 0
        aimIndex = 0
        
        for i in range( len( vectorList ) ):
            dotValue = vectorList[i] * aimVector
            if math.fabs( dotValue ) > math.fabs( maxDot ):
                maxDot = dotValue
                aimIndex = i
        if maxDot < 0:
            vectorList[ aimIndex ] = -aimVector
        else:
            vectorList[ aimIndex ] = aimVector
    elif aimIndex > 2:
        vectorList[ aimIndex%3 ] = -aimVector
    else:
        vectorList[ aimIndex%3 ] = aimVector

    aimIndex    = aimIndex % 3
    secondIndex = ( aimIndex + 1 )%3
    thirdIndex  = ( secondIndex + 1 )%3
    
    vectorList[ thirdIndex ]  = vectorList[ aimIndex ] ^ vectorList[ secondIndex ]
    vectorList[ secondIndex ] = vectorList[ thirdIndex ] ^ vectorList[ aimIndex ]
    
    for i in range( 3 ):
        vectorList[i].normalize()
    
    mtx = [ 1,0,0,0, 
            0,1,0,0, 
            0,0,1,0, 
            0,0,0,1 ]

    for i in [ aimIndex, secondIndex, thirdIndex ]:
        mtx[ i*4 + 0 ] = vectorList[ i ].x
        mtx[ i*4 + 1 ] = vectorList[ i ].y
        mtx[ i*4 + 2 ] = vectorList[ i ].z
    
    return mtx




def lookAt( aimTarget, constTarget, axisIndex=None ):
    
    import sgBFunction_convert
    mtx = sgBFunction_convert.convertMatrixToMMatrix( getLookAtMtx( aimTarget, constTarget, axisIndex ) )
    
    trMtx = om.MTransformationMatrix( mtx )
    vRot = trMtx.eulerRotation().asVector()
    rot = [ math.degrees( vRot.x ), math.degrees( vRot.y ), math.degrees( vRot.z ) ]
    
    cmds.xform( constTarget, ws=1, ro=rot )