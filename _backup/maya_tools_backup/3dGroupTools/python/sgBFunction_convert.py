import maya.OpenMaya as om


def convertSide( targetName ):
    
    if targetName.find( '_L_' ) != -1:
        return targetName.replace( '_L_', '_R_' )
    elif targetName.find( '_R_' ) != -1:
        return targetName.replace( '_R_', '_L_' )
    else:
        return targetName + '_otherSide'




def singleToList( singleObj ):
    
    if not type( singleObj ) in [ type([]), type(()) ]:
        return [singleObj]
    return singleObj




def convertMPoint( inputValue ):
    
    if type( inputValue ) in [ type([]), type(()) ]:
        return om.MPoint( *inputValue )
    elif type( inputValue ) == type( om.MVector() ):
        return om.MPoint( inputValue )
    elif type( inputValue ) == type( om.MPoint() ):
        return inputValue
    else:
        return None



def convertMVector( inputValue ):
    
    if type( inputValue ) in [ type([]), type(()) ]:
        return om.MVector( *inputValue )
    elif type( inputValue ) == type( om.MPoint() ):
        return om.MVector( inputValue )
    elif type( inputValue ) == type( om.MVector() ):
        return inputValue
    else:
        return None



def convertMMatrixToMatrix( mMatrix ):
    
    import sgBModel_data
    matrix = sgBModel_data.defaultMatrix
    
    for i in range( 4 ):
        for j in range( 4 ):
            matrix[ i*4 + j ] = mMatrix( i, j )
    
    return matrix




def convertMatrixToMMatrix( matrix ):
    
    import maya.OpenMaya as om
    mMatrix = om.MMatrix()
    om.MScriptUtil.createMatrixFromList( matrix, mMatrix )
    return mMatrix




def mirrorMatrix( sideMatrix, centerMatrix=None ):
    
    import maya.OpenMaya as om
    import sgBModel_data
    
    mSideMatrix = om.MMatrix()
    mCenterMatrix = om.MMatrix()
    
    om.MScriptUtil.createMatrixFromList( sideMatrix, mSideMatrix )
    if centerMatrix : om.MScriptUtil.createMatrixFromList( centerMatrix, mCenterMatrix )
    
    mLocalMatrix = mSideMatrix*mCenterMatrix.inverse()
    mMirrorMatrix = om.MMatrix()
    
    mtxList = sgBModel_data.defaultMatrix
    mtxList[0]  =  mLocalMatrix(0,0)
    mtxList[1]  = -mLocalMatrix(0,1)
    mtxList[2]  = -mLocalMatrix(0,2)
    mtxList[3]  =  0.0
    
    mtxList[4]  =  mLocalMatrix(1,0)
    mtxList[5]  = -mLocalMatrix(1,1)
    mtxList[6]  = -mLocalMatrix(1,2)
    mtxList[7]  =  0.0
    
    mtxList[8]  =  mLocalMatrix(2,0)
    mtxList[9]  = -mLocalMatrix(2,1)
    mtxList[10] = -mLocalMatrix(2,2)
    mtxList[11] =  0.0
    
    mtxList[12] = -mLocalMatrix(3,0)
    mtxList[13] =  mLocalMatrix(3,1)
    mtxList[14] =  mLocalMatrix(3,2)
    mtxList[15] =  1.0
    
    om.MScriptUtil.createMatrixFromList( mtxList, mMirrorMatrix )
    
    mWorldMatrix = mMirrorMatrix*mCenterMatrix
    
    worldMatrixList = sgBModel_data.defaultMatrix
    worldMatrixList[0]  =  mWorldMatrix(0,0)
    worldMatrixList[1]  =  mWorldMatrix(0,1)
    worldMatrixList[2]  =  mWorldMatrix(0,2)
    worldMatrixList[3]  =  0.0
    
    worldMatrixList[4]  =  mWorldMatrix(1,0)
    worldMatrixList[5]  =  mWorldMatrix(1,1)
    worldMatrixList[6]  =  mWorldMatrix(1,2)
    worldMatrixList[7]  =  0.0
    
    worldMatrixList[8]  =  mWorldMatrix(2,0)
    worldMatrixList[9]  =  mWorldMatrix(2,1)
    worldMatrixList[10] =  mWorldMatrix(2,2)
    worldMatrixList[11] =  0.0
    
    worldMatrixList[12] =  mWorldMatrix(3,0)
    worldMatrixList[13] =  mWorldMatrix(3,1)
    worldMatrixList[14] =  mWorldMatrix(3,2)
    worldMatrixList[15] =  1.0
    
    return worldMatrixList