import maya.cmds as cmds
import maya.OpenMaya as om
import copy


class CtlInfo:
    centerGrp = ''
    leftCtls = []
    rightCtls = []
    
    zRotMirrorTargetNames = ['wing_big', '_st_' ]
    xTransMirrorTargetNames = ['up_wing']


def loadRelativeCtls( ikCtl ):
    
    if ikCtl.find( 'L_wrist_CTL' ) != -1:
        ns = ikCtl.replace( 'L_wrist_CTL', '' )
        CtlInfo.leftCtls = cmds.ls( ns+'L_*_CTL', type='transform' )
        CtlInfo.rightCtls = cmds.ls( ns+'R_*_CTL', type='transform' )
        CtlInfo.leftCtls += cmds.ls( ns+'L_*_st_JNT', type='joint' )
        CtlInfo.rightCtls += cmds.ls( ns+'R_*_st_JNT', type='joint' )
    elif ikCtl.find( 'R_wrist_CTL' ) != -1:
        ns = ikCtl.replace( 'R_wrist_CTL', '' )
        CtlInfo.leftCtls = cmds.ls( ns+'L_*_CTL', type='transform' )
        CtlInfo.rightCtls = cmds.ls( ns+'R_*_CTL', type='transform' )
        CtlInfo.leftCtls += cmds.ls( ns+'L_*_st_JNT', type='joint' )
        CtlInfo.rightCtls += cmds.ls( ns+'R_*_st_JNT', type='joint' )

    for ctl in CtlInfo.leftCtls:
        if ctl.find( 'wing_all_CTL' ) != -1:
            CtlInfo.leftCtls.remove( ctl )
    for ctl in CtlInfo.rightCtls:
        if ctl.find( 'wing_all_CTL' ) != -1:
            CtlInfo.rightCtls.remove( ctl )

    CtlInfo.centerGrp = ns + 'all_CTL'
    


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
        otherTarget = target.replace( 'L_', 'R_' )
    elif target in CtlInfo.rightCtls:
        otherTarget = target.replace( 'R_', 'L_' )
    if not otherTarget: return None
    
    isTransMirror = False
    isZRotMirror    = False
    for transMirrorName in CtlInfo.xTransMirrorTargetNames:
        if target.find( transMirrorName ) != -1:
            isTransMirror = True
    for zRotMirror in CtlInfo.zRotMirrorTargetNames:
        if target.find( zRotMirror ) != -1 and target.find( 'wing_big4_CTL' ) == -1:
            isZRotMirror = True
    
    if isTransMirror:
        trValue = cmds.getAttr( target + '.t' )[0]
        cmds.setAttr( otherTarget+'.t', -trValue[0], trValue[1], trValue[2] )
    elif isZRotMirror:
        rotValue = cmds.getAttr( target + '.r' )[0]
        cmds.setAttr( otherTarget + '.r', -rotValue[0], -rotValue[1], rotValue[2] )
    else:
        keys = cmds.listAttr( target, k=1 )
        for key in keys:
            value = cmds.getAttr( target+'.'+key )
            cmds.setAttr( otherTarget + '.' + key, value )

    listAttr = cmds.listAttr( target, ud=1, k=1 )
    if not listAttr: return None
    for attr in listAttr:
        cmds.setAttr( otherTarget+'.'+attr, cmds.getAttr( target+'.'+attr ) )
    
    
    
def setMirrorObject( fromList, toList ):
    
    for i in range( len( fromList ) ):
        fromCtl = fromList[i]
        toCtl = toList[i]
        
        isTransMirror = False
        isZRotMirror    = False
        for transMirrorName in CtlInfo.xTransMirrorTargetNames:
            if fromCtl.find( transMirrorName ) != -1:
                isTransMirror = True
        for zRotMirror in CtlInfo.zRotMirrorTargetNames:
            if fromCtl.find( zRotMirror ) != -1 and fromCtl.find( 'wing_big4_CTL' ) == -1:
                isZRotMirror = True
        
        try:
            if isTransMirror:
                trValue = cmds.getAttr( fromCtl + '.t' )[0]
                cmds.setAttr( toCtl+'.t', -trValue[0], trValue[1], trValue[2] )
            elif isZRotMirror:
                rotValue = cmds.getAttr( fromCtl + '.r' )[0]
                cmds.setAttr( toCtl + '.r', -rotValue[0], -rotValue[1], rotValue[2] )
            else:
                keys = cmds.listAttr( fromCtl, k=1 )
                for key in keys:
                    value = cmds.getAttr( fromCtl+'.'+key )
                    cmds.setAttr( toCtl + '.' + key, value )
        except: pass
        
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
        otherTarget = target.replace( 'L_', 'R_' )
    elif target in CtlInfo.rightCtls:
        otherTarget = target.replace( 'R_', 'L_' )
    if not otherTarget: return None
    
    isTransMirror = False
    isZRotMirror    = False
    for transMirrorName in CtlInfo.xTransMirrorTargetNames:
        if target.find( transMirrorName ) != -1:
            isTransMirror = True
    for zRotMirror in CtlInfo.zRotMirrorTargetNames:
        if target.find( zRotMirror ) != -1 and target.find( 'wing_big4_CTL' ) == -1:
            isZRotMirror = True
    
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
            if attr.find( 'scale' ) != -1:
                value = values[i]
                ia = inAngles[i]
                oa = outAngles[i]
            elif attr.find( 'translate' ) != -1:
                if isTransMirror and attr[-1] in ['Y','Z']:
                    value = values[i]
                    ia = inAngles[i]
                    oa = outAngles[i]
                else:
                    value = -values[i]
                    ia = -inAngles[i]
                    oa = -outAngles[i]
            else:
                if isZRotMirror and attr[-1] in [ 'X', 'Y' ]:
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
        toCtl   = toList[i]
        
        isTransMirror = False
        isZRotMirror    = False
        for transMirrorName in CtlInfo.xTransMirrorTargetNames:
            if fromCtl.find( transMirrorName ) != -1:
                isTransMirror = True
        for zRotMirror in CtlInfo.zRotMirrorTargetNames:
            if fromCtl.find( zRotMirror ) != -1 and fromCtl.find( 'wing_big4_CTL' ) == -1:
                isZRotMirror = True
        
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
                if attr.find( 'scale' ) != -1:
                    value = values[i]
                    ia = inAngles[i]
                    oa = outAngles[i]
                elif attr.find( 'translate' ) != -1:
                    if isTransMirror and attr[-1] == ['Y','Z']:
                        value = values[i]
                        ia = inAngles[i]
                        oa = outAngles[i]
                    else:
                        value = -values[i]
                        ia = -inAngles[i]
                        oa = -outAngles[i]
                else:
                    if isZRotMirror and attr[-1] in [ 'X', 'Y' ]:
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