import maya.OpenMaya as om
import maya.cmds as cmds


def getSrcCurve( targetCurve ):
    
    if cmds.nodeType( targetCurve ) == 'transform':
        targetCurve = cmds.listRelatives( targetCurve, s=1 )[0]
    
    duCrv = cmds.duplicate( targetCurve )[0]
    duCrvShape= cmds.listRelatives( duCrv, s=1 )[0]
    duCrvShape = cmds.rename( duCrvShape, targetCurve+'Orig' )
    cmds.connectAttr( duCrvShape+'.local', targetCurve+'.create' )
    targetObj = cmds.listRelatives( targetCurve, p=1 )[0]
    cmds.parent( duCrvShape, targetObj, add=1, shape=1 )
    cmds.delete( duCrv )
    cmds.setAttr( duCrvShape+'.io', 1 )
    return duCrvShape



def setObjectToAimMatrix( target, curve, aimIndex=0 ):
    
    startPoint = cmds.xform( curve+'.cv[0]', q=1, ws=1, t=1 )
    nextPoint  = cmds.xform( curve+'.cv[1]', q=1, ws=1, t=1 )
    
    aimIndex   = (aimIndex+3) % 3
    upIndex    = (aimIndex+4) % 3
    crossIndex = (aimIndex+5) % 3
    
    lAim = [nextPoint[0] - startPoint[0],nextPoint[1] - startPoint[1], nextPoint[2] - startPoint[2]]
    lUp = [0,0,0]
    lUp[ aimIndex ] = -lAim[ upIndex ]
    lUp[ upIndex ]  = lAim[ aimIndex ]
    vAim = om.MVector( *lAim )
    vUp  = om.MVector( *lUp )
    vCross = vAim^vUp
    vUp = vCross ^ vAim
    
    vAim.normalize()
    vUp.normalize()
    vCross.normalize()
    
    mtx = [ int(i%5 == 0) for i in range( 16 ) ]
    
    mtx[ aimIndex*4 + 0 ] = vAim.x
    mtx[ aimIndex*4 + 1 ] = vAim.y
    mtx[ aimIndex*4 + 2 ] = vAim.z
    
    mtx[ upIndex*4 + 0 ] = vUp.x
    mtx[ upIndex*4 + 1 ] = vUp.y
    mtx[ upIndex*4 + 2 ] = vUp.z
    
    mtx[ crossIndex*4 + 0 ] = vCross.x
    mtx[ crossIndex*4 + 1 ] = vCross.y
    mtx[ crossIndex*4 + 2 ] = vCross.z
    
    mtx[ 3*4 + 0 ] = startPoint[0]
    mtx[ 3*4 + 1 ] = startPoint[1]
    mtx[ 3*4 + 2 ] = startPoint[2]
    
    cmds.xform( target, ws=1, matrix=mtx )
    

def createAimMatrixToWobbleCurve( curve ):
    
    hists = cmds.listHistory( curve, pdo=1 )
    sgWobbleCurves = []
    for hist in hists:
        if cmds.nodeType( hist ) == 'sgWobbleCurve':
            sgWobbleCurves.append( hist )
    
    aimMtxObjs = []
    for sgWobbleCurve in sgWobbleCurves:
        if cmds.listConnections( sgWobbleCurve+'.aimMatrix' ):
            continue
        aimMtxObj = cmds.createNode( 'transform' )
        cmds.setAttr( aimMtxObj+'.dh',1 )
        cmds.setAttr( aimMtxObj+'.dla', 1 )
        cmds.connectAttr( aimMtxObj+'.m', sgWobbleCurve+'.aimMatrix' )
        cmds.connectAttr( curve+'.m', sgWobbleCurve+'.inputCurveMatrix' )
        setObjectToAimMatrix( aimMtxObj, curve )
        aimMtxObjs.append( aimMtxObj )
    return aimMtxObjs



def setSgWobbleCurve():
    
    sels = cmds.ls( sl=1 )
    
    aimObjMtx = []
    sgWobbleCurves = []
    for sel in sels:
        '''
        hists = cmds.listHistory( sel )
        
        sgWobbleCurveExists = False
        for hist in hists:
            if cmds.nodeType( hist ) == 'sgWobbleCurve':
                sgWobbleCurveExists = True
                break'''
        
        if cmds.nodeType( sel ) == 'transform':
            selShapes = cmds.listRelatives( sel, s=1 )
            if not selShapes: continue
            selShape = selShapes[0]
        
        srcCons = cmds.listConnections( selShape+'.create', s=1, d=0, p=1, c=1 )
        srcAttr = None
        if not srcCons:
            srcAttr = getSrcCurve( selShape ) + '.local'
        else:
            srcAttr = srcCons[1]
        
        sgWobbleCurve = cmds.createNode( 'sgWobbleCurve' )
        sgWobbleCurves.append( sgWobbleCurve )
        cmds.connectAttr( srcAttr, sgWobbleCurve+'.inputCurve' )
        cmds.connectAttr( sgWobbleCurve+'.outputCurve', selShape+'.create', f=1 )
        cmds.connectAttr( 'time1.outTime', sgWobbleCurve+'.time' )
        
        cmds.setAttr( sgWobbleCurve+'.waves[0].rate1', 60 )
        cmds.setAttr( sgWobbleCurve+'.waveOptions[0].waveLength', 2 )
        cmds.setAttr( sgWobbleCurve+'.waveOptions[0].timeMult', -0.2 )
        cmds.setAttr( sgWobbleCurve+'.fallOff[1].fallOff_Position', 1.0 )
        cmds.setAttr( sgWobbleCurve+'.fallOff[1].fallOff_FloatValue', 1.0 )
        cmds.setAttr( sgWobbleCurve+'.fallOff[2].fallOff_Position', 1 )
        cmds.setAttr( sgWobbleCurve+'.fallOff[2].fallOff_FloatValue', 1 )
        
        aimMtxObjs = createAimMatrixToWobbleCurve( sel )
        selP = cmds.listRelatives( sel, p=1 )
        if selP: cmds.parent( aimMtxObjs, selP[0] )
        aimObjMtx += aimMtxObjs 
    
    cmds.select( aimObjMtx )
    
    return sels, sgWobbleCurves, aimObjMtx