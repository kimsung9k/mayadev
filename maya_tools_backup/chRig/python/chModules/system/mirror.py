import maya.cmds as cmds
import maya.OpenMaya as om
import basicfunc

defaultVectorList = [ [1,0,0],  [0,1,0], [0,0,1] ]
defaultMtxList = [ 1,0,0,0,  0,1,0,0, 0,0,1,0, 0,0,0,1 ]

def mirrorVector( targetVector, mirrorBaseVector ):
    P = targetVector
    Q = mirrorBaseVector
    
    projP_Q = Q*(P*Q/(Q.length()**2))
    
    mirV = P - projP_Q*2
    return mirV

def mirrorMatrix( targetMatrix, mirrorBaseVetor, *skipIndexList ):
    mv = mirrorBaseVetor
    M = targetMatrix
    
    X = om.MVector( M(0,0),  M(0,1),  M(0,2) )
    Y = om.MVector( M(1,0),  M(1,1),  M(1,2) )
    Z = om.MVector( M(2,0),  M(2,1),  M(2,2) )
    P = om.MVector( M(3,0),  M(3,1),  M(3,2) )
    
    revList = [-1,-1,-1]
    for skipIndex in skipIndexList:
        revList[skipIndex] *= -1
    
    X = mirrorVector( X, mv )*revList[0]
    Y = mirrorVector( Y, mv )*revList[1]
    Z = mirrorVector( Z, mv )*revList[2]
    P = mirrorVector( P, mv )
    
    MList = [ X.x, X.y, X.z, 0, Y.x, Y.y, Y.z, 0, Z.x, Z.y, Z.z, 0, P.x, P.y, P.z, 1 ]
    
    MMtx = om.MMatrix()
    
    om.MScriptUtil.createMatrixFromList( MList, MMtx )
    
    return MMtx

def positionMirror( base, target, typ='mirror' ):
    trs0 = cmds.getAttr( base+'.t' )[0]
    trs1 = cmds.getAttr( target+'.t' )[0]
    
    basicfunc.trySetAttrs( target,
                          ['tx', -trs0[0]], ['ty', trs0[1]], ['tz', trs0[2]] )
    
    if typ == 'flip':
        basicfunc.trySetAttrs( base,
                          ['tx', -trs1[0]], ['ty', trs1[1]], ['tz', trs1[2]] )

def objectMirror( base, target, typ='mirror' ):
    trs = cmds.getAttr( base+'.t' )[0]
    rot = cmds.getAttr( base+'.r' )[0]
    
    trsTarget = cmds.getAttr( target+'.t' )[0]
    rotTarget = cmds.getAttr( target+'.r' )[0]
    
    basicfunc.trySetAttrs( target, 
                           ['tx', -trs[0]], ['ty', -trs[1]],['tz', -trs[2] ],
                           ['rx',  rot[0]], ['ry',  rot[1]],['rz',  rot[2] ] )
    
    if typ == 'flip':
        basicfunc.trySetAttrs( base,
                               ['tx', -trsTarget[0]], ['ty', -trsTarget[1]],['tz', -trsTarget[2] ],
                               ['rx',  rotTarget[0]], ['ry',  rotTarget[1]],['rz',  rotTarget[2] ] )
    
def mMatrixObjectMirror( target ):
    mtxList = [ target(0,0),  target(0,1),  target(0,2),  target(0,3),
                target(1,0),  target(1,1),  target(1,2),  target(1,3),
                target(2,0),  target(2,1),  target(2,2),  target(2,3),
                -target(3,0), -target(3,1), -target(3,2), target(3,3) ]
    
    om.MScriptUtil.createMatrixFromList( mtxList, target )
    return target

def objPMirror( base, target, baseP, targetP, typ= 'mirror' ):
    baseMatrix = basicfunc.getMMatrix( base, ws=1 )
    basePMatrix = basicfunc.getMMatrix( baseP, ws=1 )
    targetMatrix = basicfunc.getMMatrix( target, ws=1 )
    targetPMatrix = basicfunc.getMMatrix( targetP, ws=1 )
    
    baseLocalMtx = baseMatrix*basePMatrix.inverse()
    targetLocalMtx = targetMatrix*targetPMatrix.inverse()
    
    baseMirrorMtx = mMatrixObjectMirror( baseLocalMtx )
    targetMirrorMtx = mMatrixObjectMirror( targetLocalMtx )
    
    if typ == 'mirror':
        mtxForTarget = baseMirrorMtx*targetPMatrix
        basicfunc.setMMatrix( target, mtxForTarget, ws=1 )
        if cmds.nodeType( target ) == 'joint':
            basicfunc.setRotate_keepJointOrient( mtxForTarget, target )
    else:
        mtxForTarget = baseMirrorMtx*targetPMatrix
        mtxForBase   = targetMirrorMtx*basePMatrix
        basicfunc.setMMatrix( target, mtxForTarget, ws=1 )
        basicfunc.setMMatrix( base,   mtxForBase, ws=1 )
        if cmds.nodeType( target ) == 'joint':
            basicfunc.setRotate_keepJointOrient( mtxForTarget, target )
            basicfunc.setRotate_keepJointOrient( mtxForBase, base )
            
def axisMirror( base, target, spaceObj, mirrorBaseVector, typ= 'mirror' ):
    mbv = om.MVector( *mirrorBaseVector )
    
    baseMatrix = basicfunc.getMMatrix( base, ws=1 )
    targetMatrix = basicfunc.getMMatrix( target, ws=1 )
    spaceMatrix = basicfunc.getMMatrix( spaceObj, ws=1 )
    
    baseLocalMtx = baseMatrix*spaceMatrix.inverse()
    targetLocalMtx = targetMatrix*spaceMatrix.inverse()
    
    baseMirrorMtx = mirrorMatrix( baseLocalMtx, mbv )
    targetMirrorMtx = mirrorMatrix( targetLocalMtx, mbv )
    
    if typ == 'mirror':
        mtxForTarget = baseMirrorMtx*spaceMatrix
        basicfunc.setMMatrix( target, mtxForTarget, ws=1 )
        if cmds.nodeType( target ) == 'joint':
            basicfunc.setRotate_keepJointOrient( mtxForTarget, target )
    else:
        mtxForTarget = baseMirrorMtx*spaceMatrix
        mtxForBase   = targetMirrorMtx*spaceMatrix
        basicfunc.setMMatrix( target, mtxForTarget, ws=1 )
        basicfunc.setMMatrix( base,   mtxForBase, ws=1 )
        if cmds.nodeType( target ) == 'joint':
            basicfunc.setRotate_keepJointOrient( mtxForTarget, target )
            basicfunc.setRotate_keepJointOrient( mtxForBase, base )
    
def centerMirror( target, spaceObj, axisIndex, typ='mirror' ):
    mirrorBaseVector = defaultVectorList[ axisIndex ]
    mbv = om.MVector( *mirrorBaseVector )
    
    targetMatrix = basicfunc.getMMatrix( target, ws=1 )
    spaceMatrix = basicfunc.getMMatrix( spaceObj, ws=1 )
    
    targetLocalMtx = targetMatrix*spaceMatrix.inverse()
    
    skipList = [0,1,2]
    skipList.remove( axisIndex )
    targetMirrorMtx = mirrorMatrix( targetLocalMtx, mbv, *skipList )
    
    if typ == 'mirror':
        sumMtx = targetMirrorMtx+targetLocalMtx
        mtxForTarget = (sumMtx*0.5)*spaceMatrix
    else:
        mtxForTarget = targetMirrorMtx*spaceMatrix
    
    basicfunc.setRotMMatrix( target, mtxForTarget, ws=1 )  
    basicfunc.setTrMMatrix( target, mtxForTarget, ws=1 )
        
def getOtherSide( target ):
    if target.find( '_L_' ) != -1:
        return target.replace( '_L_', '_R_' )
    elif target.find( '_R_' ) != -1:
        return target.replace( '_R_', '_L_' )