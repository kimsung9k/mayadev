import maya.cmds as cmds
import maya.OpenMaya as om
import functions.apiSimple as apiSimple


class matrixInfo:
    
    def __init__(self, dagNode=None ):
        
        self.name = dagNode
        if not dagNode:
            self.matrix = om.MMatrix()
        else:
            self.matrix = apiSimple.getMMatrixFromDagNode( dagNode )



def setAimMatrix( parentInfo, childInfo, targetInfo, aimIndex=0, upIndex=1 ):
    
    pMtx = parentInfo.matrix
    cMtx = childInfo.matrix
    tMtx = targetInfo.matrix
    
    upVector = om.MVector( pMtx( upIndex, 0 ), pMtx( upIndex, 1 ), pMtx( upIndex, 2 ) )
    aimVector = om.MVector( cMtx( 3,0 ) - tMtx( 3,0 ), cMtx( 3,1 ) - tMtx( 3,1 ), cMtx( 3,2 ) - tMtx( 3,2 ) )
    
    if ( upIndex - aimIndex + 3 ) % 3 == 1:
        crossVector = aimVector ^ upVector
    else:
        crossVector = upVector ^ aimVector
    
    upVector = crossVector ^ aimVector
    
    aimVector.normalize()
    upVector.normalize()
    crossVector.normalize()
    
    crossIndex = 3 - upIndex - aimIndex
    
    mtx = [ [0,0,0,0] for i in range( 4 ) ]
    
    mtx[aimIndex]   = [aimVector.x, aimVector.y, aimVector.z, 0 ]
    mtx[upIndex]    = [upVector.x,  upVector.y,  upVector.z, 0 ]
    mtx[crossIndex] = [crossVector.x, crossVector.y, crossVector.z, 0 ]
    
    wm = cmds.getAttr( targetInfo.name+'.wm' )
    
    for i in range( 3 ):
        for j in range( 3 ):
            wm[ i*4 + j ] = mtx[i][j]
    
    childMtx = cmds.getAttr( childInfo.name+'.wm' )
    cmds.xform( targetInfo.name, ws=1, matrix=wm )
    cmds.xform( childInfo.name, ws=1, matrix=childMtx )


def setOrientJointRelatives( topJnt, aimIndex=0, upIndex=1 ):
    
    childJnts = cmds.listRelatives( topJnt, c=1, ad=1 )
    childJnts.append( topJnt )
    childJnts.reverse()
    
    setAimMatrix( matrixInfo( childJnts[0] ), matrixInfo( childJnts[1] ), matrixInfo( childJnts[0] ), aimIndex, upIndex )
    for i in range( len( childJnts )-2 ):
        setAimMatrix( matrixInfo(childJnts[i]), matrixInfo( childJnts[i+2] ), matrixInfo( childJnts[i+1] ), aimIndex, upIndex )
        