import maya.cmds as cmds
import maya.OpenMaya as OpenMaya



def matrixFromList( mtxList ):
    
    matrix = OpenMaya.MMatrix();
    OpenMaya.MScriptUtil.createMatrixFromList( mtxList, matrix )
    return matrix




def MIntArray( target ):
    OpenMaya.MObject()
    if type( target ) == type( OpenMaya.MIntArray() ):
        return target
    if type( target ) in [ type( () ), type( [] ) ]:
        intArr = OpenMaya.MIntArray()
        intArr.setLength( len( target ) )
        for i in range( intArr.length() ):
            intArr.set( target[i], i )
        return intArr
    return OpenMaya.MIntArray()




def matrixToList( matrix ):
    mtxList = range( 16 )
    for i in range( 4 ):
        for j in range( 4 ):
            mtxList[ i * 4 + j ] = matrix( i, j )
    return mtxList




def rotateToMatrix( rotation ):
    
    import math
    rotX = math.radians( rotation[0] )
    rotY = math.radians( rotation[1] )
    rotZ = math.radians( rotation[2] )
    
    trMtx = OpenMaya.MTransformationMatrix()
    trMtx.rotateTo( OpenMaya.MEulerRotation( OpenMaya.MVector(rotX, rotY, rotZ) ) )
    return trMtx.asMatrix()




def listToMatrix( mtxList ):
    matrix = OpenMaya.MMatrix()
    OpenMaya.MScriptUtil.createMatrixFromList( mtxList, matrix  )
    return matrix



def singleToList( target ):
    
    if type( target ) in ( type(()), type([]) ): return target
    else: return [target]




def sideString( string ):
    
    import copy
    converted = copy.copy( string )
    if string.find( '_L_' ) != -1:
        converted = string.replace( '_L_', '_R_' )
    elif string.find( '_R_' ) != -1:
        converted = string.replace( '_R_', '_L_' )
    return converted




