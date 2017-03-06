import maya.cmds as cmds
import maya.OpenMaya as om
import copy


class CtlInfo:
    centerGrp = ''
    leftCtls = []
    rightCtls = []


def loadRelativeCtls( ikCtl ):
    
    if ikCtl.find( 'CtlIk_Wing_L1_02' ) != -1:
        ns = ikCtl.replace( 'CtlIk_Wing_L1_02', '' )
        CtlInfo.leftCtls = cmds.ls( ns+'Ctl*_Wing*L1_*', type='transform' )
        CtlInfo.leftCtls += cmds.ls( ns+'Ctl_Collar_L_00', type='transform' )
        CtlInfo.rightCtls = cmds.ls( ns+'Ctl*_Wing*R1_*', type='transform' )
        CtlInfo.rightCtls += cmds.ls( ns+'Ctl_Collar_R_00', type='transform' )
    elif ikCtl.find( 'CtlIk_Wing_R1_02' ) != -1:
        ns = ikCtl.replace( 'CtlIk_Wing_R1_02', '' )
        CtlInfo.leftCtls = cmds.ls( ns+'Ctl*_Wing*L1_*', type='transform' )
        CtlInfo.leftCtls += cmds.ls( ns+'Ctl_Collar_L_00', type='transform' )
        CtlInfo.rightCtls = cmds.ls( ns+'Ctl*_Wing*R1_*', type='transform' )
        CtlInfo.rightCtls += cmds.ls( ns+'Ctl_Collar_R_00', type='transform' )
        
    CtlInfo.centerGrp = ns + 'MirrorBaseCtl_C_Chest'
    


def getMirrorMatrix_world( sideMatrix, centerMatrix ):
    
    mSideMatrix = om.MMatrix()
    mCenterMatrix = om.MMatrix()
    
    om.MScriptUtil.createMatrixFromList( sideMatrix, mSideMatrix )
    om.MScriptUtil.createMatrixFromList( centerMatrix, mCenterMatrix )
    
    mLocalMatrix = mSideMatrix*mCenterMatrix.inverse()
    mMirrorMatrix = om.MMatrix()
    
    mtxList = [ 0 for i in range( 16 ) ]
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
    
    worldMatrixList = [ 0 for i in range( 16 ) ]
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
    
    mirrorMatrix = copy.copy( sideMatrix )
    
    mirrorMatrix[12] *= -1
    mirrorMatrix[13] *= -1
    mirrorMatrix[14] *= -1
    
    return mirrorMatrix



def setMirrorObjectOnce( target ):
    
    otherTarget = ''
    if target in CtlInfo.leftCtls:
        otherTarget = target.replace( '_L1_', '_R1_' )
    elif target in CtlInfo.rightCtls:
        otherTarget = target.replace( '_R1_', '_L1_' )
    if not otherTarget: return None
        
    targetMtx = cmds.getAttr( target+'.m' )
    mirrorMtx = getMirrorMatrix_local( targetMtx )
    
    cmds.xform( otherTarget, os=1, matrix=mirrorMtx )
    
    
    
def setMirrorObject( fromList, toList ):
    
    for i in range( len( fromList ) ):
        fromCtl = fromList[i]
        toCtl = toList[i]
        
        targetMtx = cmds.getAttr( fromCtl+'.m' )
        mirrorMtx = getMirrorMatrix_local( targetMtx )
        
        cmds.xform( toCtl, os=1, matrix=mirrorMtx )
        listAttr = cmds.listAttr( fromCtl, ud=1, k=1 )
        if not listAttr: continue
        for attr in listAttr:
            cmds.setAttr( toCtl+'.'+attr, cmds.getAttr( fromCtl+'.'+attr ) )
                
        
def setMirrorObjectLtoR():
    
    setMirrorObject( CtlInfo.leftCtls, CtlInfo.rightCtls )


def setMirrorObjectRtoL():
    
    setMirrorObject( CtlInfo.rightCtls, CtlInfo.leftCtls )



def keyCopyObjectOnce( target, start, end ):
    
    otherTarget = ''
    if target in CtlInfo.leftCtls:
        otherTarget = target.replace( '_L1_', '_R1_' )
    elif target in CtlInfo.rightCtls:
        otherTarget = target.replace( '_R1_', '_L1_' )
    if not otherTarget: return None
    
    attrs = cmds.listAttr( target, k=1 )

    for attr in attrs:
        times = cmds.keyframe( target+'.'+attr, q=1, t=(start,end), tc=1 )
        if not times: continue
        
        values = cmds.keyframe( target+'.'+attr, q=1, t=(start,end), vc=1 )
        keyLocks = cmds.keyTangent( target+'.'+attr, q=1, t=(start,end), lock=1 )
        inAngles = cmds.keyTangent( target+'.'+attr, q=1, t=(start,end), ia=1 )
        outAngles = cmds.keyTangent( target+'.'+attr, q=1, t=(start,end), oa=1 )

        cmds.cutKey( otherTarget+'.'+attr, t=(start+0.01, end-0.01) )
        
        for i in range( len( times ) ):
            if attr.find( 'translate' ) != -1:
                value = -values[i]
                ia = -inAngles[i]
                oa = -outAngles[i]
            else:
                value = values[i]
                ia = inAngles[i]
                oa = outAngles[i]
            cmds.setKeyframe( otherTarget+'.'+attr, t=times[i], v=value )
            cmds.keyTangent( otherTarget+'.'+attr, e=1, t=(times[i],times[i]), lock=0 )
            cmds.keyTangent( otherTarget+'.'+attr, e=1, t=(times[i],times[i]), ia=ia )
            cmds.keyTangent( otherTarget+'.'+attr, e=1, t=(times[i],times[i]), oa=oa )
            cmds.keyTangent( otherTarget+'.'+attr, e=1, t=(times[i],times[i]), lock=keyLocks[i] )
            
            
def keyCopyObjects( fromList, toList, start, end ):
    
    for i in range( len( fromList ) ):
        fromCtl = fromList[i]
        toCtl = toList[i]
        
        targetMtx = cmds.getAttr( fromCtl+'.m' )
        mirrorMtx = getMirrorMatrix_local( targetMtx )
        
        listAttr = cmds.listAttr( fromCtl, k=1 )
        if not listAttr: continue
        for attr in listAttr:
            times = cmds.keyframe( fromCtl+'.'+attr, q=1, t=(start,end), tc=1 )
            if not times: continue
            
            values = cmds.keyframe( fromCtl+'.'+attr, q=1, t=(start,end), vc=1 )
            keyLocks = cmds.keyTangent( fromCtl+'.'+attr, q=1, t=(start,end), lock=1 )
            inAngles = cmds.keyTangent( fromCtl+'.'+attr, q=1, t=(start,end), ia=1 )
            outAngles = cmds.keyTangent( fromCtl+'.'+attr, q=1, t=(start,end), oa=1 )
    
            cmds.cutKey( toCtl+'.'+attr, t=(start+0.01, end-0.01) )
            for i in range( len( times ) ):
                if attr.find( 'translate' ) != -1:
                    value = -values[i]
                    ia = -inAngles[i]
                    oa = -outAngles[i]
                else:
                    value = values[i]
                    ia = inAngles[i]
                    oa = outAngles[i]
                cmds.setKeyframe( toCtl+'.'+attr, t=times[i], v=value )
                cmds.keyTangent( toCtl+'.'+attr, e=1, t=(times[i],times[i]), lock=0 )
                cmds.keyTangent( toCtl+'.'+attr, e=1, t=(times[i],times[i]), ia=ia )
                cmds.keyTangent( toCtl+'.'+attr, e=1, t=(times[i],times[i]), oa=oa )
                cmds.keyTangent( toCtl+'.'+attr, e=1, t=(times[i],times[i]), lock=keyLocks[i] )
                
                
                
def keyCopyObjectLtoR( start, end ):
    
    keyCopyObjects( CtlInfo.leftCtls, CtlInfo.rightCtls, start, end )


def keyCopyObjectRtoL( start, end ):
    
    keyCopyObjects( CtlInfo.rightCtls, CtlInfo.leftCtls, start, end )