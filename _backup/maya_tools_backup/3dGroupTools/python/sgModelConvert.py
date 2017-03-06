import maya.cmds as cmds
import maya.OpenMaya as om

import sgModelData
import sgModelDg
import sgModelDag


def convertMIntArrayFromList( lIntArr ):
    
    intArr = om.MIntArray()
    intArr.setLength( len( lIntArr ) )
    
    for i in range( len( lIntArr ) ):
        intArr[i] = lIntArr[i]
    return intArr



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
    
    matrix = sgModelData.getDefaultMatrix()
    
    for i in range( 4 ):
        for j in range( 4 ):
            matrix[ i*4 + j ] = mMatrix( i, j )
    
    return matrix




def convertMatrixToMMatrix( matrix ):
    
    mMatrix = om.MMatrix()
    om.MScriptUtil.createMatrixFromList( matrix, mMatrix )
    return mMatrix




def convertMVectorFromPointList( pointList ):
    
    return om.MVector( *pointList[:3] )




def convertMFnDependencyNodes( nodeNames ):
    
    fnNodes = []
    for nodeName in nodeNames:
        fnNode = om.MFnDependencyNode( sgModelDg.getMObject( nodeName ) )
        fnNodes.append( fnNode )
    return fnNodes



def convertMFnDagNodes( nodeNames ):
    
    dagNodes = []
    for nodeName in nodeNames:
        dagNode = om.MFnDagNode( sgModelDag.getDagPath( nodeName ) )
        dagNodes.append( dagNode )
    return dagNodes



def convertFullPathName( nodeName ):
    
    return cmds.ls( nodeName, l=1 )[0]



def convertFullPathNames( nodeNames ):
    
    fullPathNames = []
    for name in nodeNames:
        fullPathNames.append( cmds.ls( name, l=1 )[0] )
    return fullPathNames