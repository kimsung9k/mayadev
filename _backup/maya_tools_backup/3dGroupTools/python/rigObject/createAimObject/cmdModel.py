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



def lookAt( aimTarget, constTarget ):
    
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
    
    if maxDot < 0:
        vectorList[ aimIndex ] = -aimVector;
    else:
        vectorList[ aimIndex ] = aimVector;
    
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
    
    import sgBFunction_convert
    trMtx = om.MTransformationMatrix( sgBFunction_convert.convertMatrixToMMatrix( mtx ) )
    rotValue = trMtx.eulerRotation().asVector()
    rot = [ math.degrees( rotValue.x ), math.degrees( rotValue.y ), math.degrees( rotValue.z ) ]
    
    cmds.xform( constTarget, ws=1, ro=rot )
    
    return aimIndex

    
    
def uiCmd_createAimObject( axisIndex, inverseAim, displayAxis, worldPosition, autoAxis=True, lookAt=False, *args ):
    
    def createAimObject( first, second, third, worldPosition=True ):
    
        aimObjectMatrix = cmds.createNode( 'aimObjectMatrix' )
        cmds.connectAttr( first+'.wm', aimObjectMatrix+'.targetMatrix' )
        cmds.connectAttr( second+'.wm', aimObjectMatrix+'.baseMatrix' )
        
        if third:
            aimObject = third
        else:
            aimObject = cmds.createNode( 'transform' )
        
        if cmds.nodeType( aimObject ) == 'joint':
            try: cmds.setAttr( aimObject+'.jo', 0,0,0 )
            except:pass
        cmds.connectAttr( aimObjectMatrix+'.outRotate', aimObject+'.r' )
        
        if not third: cmds.parent( aimObject, second )
        cmds.setAttr( aimObject+'.t', 0,0,0 )
        
        if worldPosition:
            cmds.setAttr( aimObjectMatrix+'.worldSpaceOutput', 1 )
            cmds.connectAttr( aimObject+'.pim', aimObjectMatrix+'.parentInverseMatrix' )
            cmds.connectAttr( aimObjectMatrix+'.outTranslate', aimObject+'.t' )
        
        return aimObject, aimObjectMatrix
    
    sels = cmds.ls( sl=1 )
    
    aimTarget = sels[0]
    constTarget  = sels[1]
    
    
    
    thirdName = constTarget.split( '|' )[-1]
    second = cmds.createNode( 'transform', n=thirdName + '_upObject' )
    thirdP = cmds.listRelatives( thirdName, p=1, f=1 )
    if thirdP:
        second = cmds.parent( second, thirdP[0] )[0]
    cmds.xform( second, ws=1, matrix= cmds.getAttr( constTarget+'.wm' ) )
    
    aimObject, aimObjectMatrix = createAimObject( aimTarget, second, constTarget )
    
    cmds.setAttr( aimObjectMatrix+'.aimAxis', axisIndex )
    cmds.setAttr( aimObjectMatrix+'.inverseAim', inverseAim )
    cmds.setAttr( aimObject+'.dla', displayAxis )
    cmds.setAttr( aimObject+'.dh', displayAxis )