import maya.api.OpenMaya as openMaya
import maya.OpenMaya as om
import maya.cmds as cmds




def getMatrixFromPlugMatrix( plugMatrix ):
    
    mObj = plugMatrix.asMObject()
    mtxData = openMaya.MFnMatrixData()
    mtxData.create( mObj )
    return mtxData.matrix()





def getMPointFromMMatrix( mmtx ):
    
    return openMaya.MPoint( mmtx(3,0), mmtx(3,1), mmtx(3,2) )





def getDefaultMatrix():
    
    return [ i%5 == 0 for i in range( 16 ) ]





def getValueFromDict( argDict, *dictKeys ):
    
    items = argDict.items()
    
    for item in items:
        if item[0] in dictKeys: return item[1]
    
    return None




def getArragnedList( inputList ):
    
    if not type( inputList ) in [ type([]), type(()) ]:
        inputList = [inputList]
    
    arrangedList = []
    for inputs in inputList:
        if type( inputs ) in [ type([]), type(()) ]:
            arrangedList += getArragnedList( inputs )
        else:
            arrangedList.append( inputs )
    
    return arrangedList




def getCurrentUnitFrameRate():
    
    timeUnitDict = { 'game':15, 'film':24, 'pal':25, 'ntsc':30, 'show':48, 'palf':50, 'ntscf':60 }
    currentTimeUnit = cmds.currentUnit( q=1, time=1 )
    
    return float( timeUnitDict[ currentTimeUnit ] )




def getSortIndicesByPosition( positionList ):
    
    addNumPositionList = []
    
    for i in range( len( positionList ) ):
        addNumPositionList.append( [positionList[i], i] )
    
    addNumPositionList.sort()
    
    indices = []
    for position, index in addNumPositionList:
        indices.append( index )
    
    return indices




def surfaceColorAtPoint( surfaceNode, position ):
    
    import sgBFunction_dag
    
    def getCloseNode( surfaceNode ):
        closeNode = cmds.listConnections( surfaceNode+'.worldSpace', type='closestPointOnSurface' )
        if closeNode: return closeNode[0]
        closeNode = cmds.createNode( 'closestPointOnSurface' )
        cmds.connectAttr( surfaceNode+'.worldSpace', closeNode+'.inputSurface' )
        return closeNode
    
    surfaceNode = sgBFunction_dag.getShape( surfaceNode )
    closeNode = getCloseNode( surfaceNode )
    cmds.setAttr( closeNode+'.inPosition', *position )
    
    shadingEngines = sgBFunction_dag.getShadingEngines( surfaceNode )
    if not shadingEngines: return None
    
    shader = cmds.listConnections( shadingEngines[0]+'.surfaceShader', s=1, d=0 )
    texture = cmds.listConnections( shader[0]+'.color', s=1, d=0 )
    
    if not texture: return None
    
    uValue = cmds.getAttr( closeNode+'.parameterU' )
    vValue = cmds.getAttr( closeNode+'.parameterV' )
    
    return cmds.colorAtPoint( texture[0], u=uValue, v=vValue )



def getVectorFromMatrixByAngle( mtx, angle, aimIndex=0 ):
    
    import math
    
    if type( mtx ) == type( [] ):
        mtxTemp = om.MMatrix()
        om.MScriptUtil.createMatrixFromList( mtx, mtxTemp )
        mtx = mtxTemp
    
    upIndex = ( aimIndex + 1 ) % 3
    crossIndex = ( aimIndex + 2 ) % 3
    
    vX = om.MVector( mtx[ upIndex ] )
    vY = om.MVector( mtx[ crossIndex ] )
    
    vAngle = vX * math.cos( angle ) + vY * math.sin( angle )

    return vAngle



def getMirrorMatrix_world( sideMatrix, centerMatrix ):
    
    mSideMatrix = om.MMatrix()
    mCenterMatrix = om.MMatrix()
    
    om.MScriptUtil.createMatrixFromList( sideMatrix, mSideMatrix )
    om.MScriptUtil.createMatrixFromList( centerMatrix, mCenterMatrix )
    
    mLocalMatrix = mSideMatrix*mCenterMatrix.inverse()
    mMirrorMatrix = om.MMatrix()
    
    mtxList = getDefaultMatrix()
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
    
    worldMatrixList = getDefaultMatrix()
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


def getMirrorMatrix_local( sideMatrix ):
    
    import copy
    mirrorMatrix = copy.copy( sideMatrix )
    
    mirrorMatrix[12] *= -1
    mirrorMatrix[13] *= -1
    mirrorMatrix[14] *= -1
    
    return mirrorMatrix



def getOtherSideString( first ):
    
    firstName = first.split( '|' )[-1]
    if firstName.find( '_L_' ) != -1:
        return firstName.replace( '_L_', '_R_' )
    else:
        return firstName.replace( '_R_', '_L_' )


