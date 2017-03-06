import maya.cmds as cmds
import maya.OpenMaya as om


def getLoftSurfaceFromSelCurves( sels, close=False ):
    
    import sgBFunction_dag
    
    poses = []
    
    for sel in sels:
        pos = om.MPoint( *cmds.xform( sel+'.cv[0]', q=1, ws=1, t=1 ) )
        poses.append( pos )
    
    targetIndices = [ 0 ]
    
    nextIndex = 0
    for i in range( len( poses ) ):
        minDist = 100000.0
        minDistIndex = nextIndex
        for j in range( 1, len( poses ) ):
            if nextIndex == j: continue
            if j in targetIndices: continue
            dist = poses[nextIndex].distanceTo( poses[j] )
            if dist < minDist:
                minDist = dist
                minDistIndex = j
        nextIndex = minDistIndex
        if minDistIndex in targetIndices: continue
        targetIndices.append( minDistIndex )
    
    cmds.select( d=1 )
    for i in targetIndices:
        cmds.select( sels[i], add=1 )
    
    sels = cmds.ls( sl=1 )
    allSpans = 0
    for sel in sels:
        selShape = sgBFunction_dag.getShape( sel )
        allSpans += cmds.getAttr( selShape+'.spans' )
    
    eachSpan = int( allSpans / len( sels ) )
    
    for sel in sels:
        cmds.rebuildCurve( sel, ch=0, s=eachSpan )
    
    loftNode = cmds.createNode( 'loft' )
    cmds.setAttr( loftNode+'.close', close )
    reverseNode = cmds.createNode( 'reverseSurface' )
    cmds.setAttr( reverseNode+'.direction', 3 )
    for i in range( len( sels ) ):
        sel = sels[i]
        selShape= sgBFunction_dag.getShape( sel )
        cmds.connectAttr( selShape+'.worldSpace', loftNode+'.inputCurve[%d]' % i )
    
    cmds.connectAttr( loftNode+'.outputSurface', reverseNode+'.inputSurface' )
    surf = cmds.createNode( 'nurbsSurface' )
    cmds.connectAttr( reverseNode+'.outputSurface', surf+'.create' )
    surfaceObj = cmds.listRelatives( surf, p=1, f=1 )[0]
    cmds.sets( surfaceObj, e=1, forceElement='initialShadingGroup' )
    
    return surfaceObj
    
    



def createInCurve( surface, numCurve, paramRand=0.3, offsetRand=0.15, centerOffset = 0.5 ):
    
    import random
    import sgBFunction_dag
    import sgBFunction_base
    
    sgBFunction_base.autoLoadPlugin("HSBVC.mll")
    
    node = cmds.createNode( 'volumeCurvesOnSurface' )
    cmds.connectAttr( surface+'.wm', node+'.inputMatrix' )
    surfaceShape = sgBFunction_dag.getShape( surface )
    cmds.connectAttr( surfaceShape+'.local', node+'.inputSurface' )
    
    minValue, maxValue = cmds.getAttr( surfaceShape+'.minMaxRangeV' )[0]
    
    if numCurve in [1,2,3]:
        paramRate = ( maxValue-minValue )/numCurve
    else:
        paramRate = ( maxValue-minValue )/(numCurve-1)
    
    outputCurves = cmds.listConnections( node+'.outputCurve' )
    
    if outputCurves:
        lenOutputCurves = len( outputCurves )
        
        if lenOutputCurves > numCurve:
            cmds.delete( outputCurves[numCurve-lenOutputCurves:] )
    
    if not numCurve:
        return None
    
    curves = []
    for i in range( numCurve ):
        addOffsetParam = random.uniform( -paramRate/2*paramRand, paramRate/2*paramRand )
        addOffsetCenter = random.uniform( -offsetRand, offsetRand )
        
        outputCurveCon = cmds.listConnections( node+'.outputCurve[%d]' % i )
        
        if not outputCurveCon:
            crvNode = cmds.createNode( 'nurbsCurve' )
            crvObj = cmds.listRelatives( crvNode, p=1 )[0]
            cmds.connectAttr( node+'.outputCurve[%d]' % i, crvNode+'.create' )
            cmds.addAttr( crvObj, ln='paramRate', dv= paramRate*i + addOffsetParam + paramRate*0.5 )
            cmds.setAttr( crvObj+'.paramRate', e=1, k=1 )
            cmds.addAttr( crvObj, ln='centerRate', dv= centerOffset+addOffsetCenter )
            cmds.setAttr( crvObj+'.centerRate', e=1, k=1 )
            cmds.connectAttr( crvObj+'.paramRate', node+'.curveInfo[%d].paramRate' % i )
            cmds.connectAttr( crvObj+'.centerRate', node+'.curveInfo[%d].centerRate' % i )
        else:
            crvObj = outputCurveCon[0]
            cmds.setAttr( crvObj+'.paramRate', paramRate*i + addOffsetParam + paramRate*0.5  )
            cmds.setAttr( crvObj+'.centerRate', centerOffset+addOffsetCenter  )
        crvObj = cmds.rename( crvObj, surface+'_curve_%d' % i )
        curves.append( crvObj )
        
        if i == numCurve -1:
            if not numCurve in [2,3]:
                cmds.setAttr( crvObj+'.centerRate', 0 )
    
    outputLen = numCurve
    for i in range( outputLen ):
        outputCons = cmds.listConnections( node+'.outputCurve[%d]' % i )
        if not outputCons:
            cmds.removeMultiInstance( '%s[%d]' %( node+'.outputCurve', i ) )
            cmds.removeMultiInstance( '%s[%d]' %( node+'.curveInfo', i ) )
    
    return curves


def getSurfaceInfo_worldSpace( surf ):
    
    import sgBFunction_dag
    surfShape = sgBFunction_dag.getShape( surf )
    
    cons = cmds.listConnections( surfShape+'.worldSpace', d=1, s=0 )
    
    if not cons:
        info = cmds.createNode( 'surfaceInfo' )
        cmds.connectAttr( surfShape+'.worldSpace[0]', info+'.inputSurface' )
        return info
    else:
        return cons[0]



def getSurfaceInfo_localSpace( surf ):
    
    import sgBFunction_dag
    surfShape = sgBFunction_dag.getShape( surf )
    
    cons = cmds.listConnections( surfShape+'.local', d=1, s=0 )
    
    if not cons:
        info = cmds.createNode( 'surfaceInfo' )
        cmds.connectAttr( surfShape+'.local', info+'.inputSurface' )
        return info
    else:
        return cons[0]