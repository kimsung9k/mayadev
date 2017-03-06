import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaMPx as mpx
import volumeHairTool.functions as fnc
import math



def setGrp( targetObject, grpName ):
    
    surfObj = cmds.listConnections( targetObject+'.message', s=0, d=1 )[0]
    surfObjGrp = cmds.listRelatives( surfObj, p=1 )[0]
    
    if not cmds.attributeQuery( grpName, node=surfObjGrp, ex=1 ):
        cmds.addAttr( surfObjGrp, ln=grpName, at='message' )
    
    grpCons = cmds.listConnections( surfObjGrp+'.'+grpName )

    if not grpCons:
        grp = cmds.createNode( 'transform', n=surfObjGrp+'_'+grpName )
        cmds.connectAttr( grp+'.message', surfObjGrp+'.'+grpName )
    else:
        grp = grpCons[0]
    
    if cmds.listRelatives( targetObject, p=1 ) != [grp]:
        cmds.parent( targetObject, grp )
    


def getSurfaceCenterCurve( surfaceObj, meshObj, parentNode=None ):
    
    surface = cmds.listRelatives( surfaceObj, s=1 )[0]
    mesh = cmds.listRelatives( meshObj, s=1 )[0]
    
    fnSurface = om.MFnNurbsSurface( fnc.getMObject( surface ) )
    surfaceMatrix = fnc.getMMatrixFromMtxList( cmds.getAttr( surface+'.wm' ) )
        
    degreeU = fnSurface.degreeU()
    numU = fnSurface.numCVsInU()
    numV = fnSurface.numCVsInV()
    
    cvPoints = []
    cvMPoints = om.MPointArray()
    cvMPoints.setLength( numU )
    
    for i in range( numU ):
        bbox = om.MBoundingBox()
        point = om.MPoint()
        for j in range( numV ):
            fnSurface.getCV( i, j, point )
            bbox.expand( point )
        minPoint = om.MVector( bbox.min() )
        maxPoint = om.MVector( bbox.max() )
        cPoint = om.MPoint(( minPoint + maxPoint )/2)*surfaceMatrix
        cvPoints.append( [cPoint.x,cPoint.y,cPoint.z] )
        cvMPoints.set( cPoint, i )
    
    surfaceObject = cmds.listRelatives( surface, p=1 )[0] 
    returnCurve = cmds.curve( p=cvPoints, d=degreeU )
    returnCurveShape = cmds.listRelatives( returnCurve, s=1 )[0]
    
    origShape = fnc.getOrigShape( returnCurveShape )
    closestParam = getClosestParam( origShape, mesh )
    
    detachCurve = cmds.createNode( 'detachCurve', n=returnCurve+'_detach' )
    cmds.setAttr( detachCurve+'.parameter[0]', closestParam )
    rebuildCurve = cmds.createNode( 'rebuildCurve', n=returnCurve+'._rebuild' )
    cmds.connectAttr( origShape+'.degree', rebuildCurve+'.degree' )
    cmds.connectAttr( origShape+'.spans', rebuildCurve+'.spans' )
    
    cmds.connectAttr( origShape+'.local', detachCurve+'.inputCurve' )
    cmds.connectAttr( detachCurve+'.outputCurve[1]', rebuildCurve+'.inputCurve' )
    cmds.connectAttr( rebuildCurve+'.outputCurve', returnCurveShape+'.create', f=1 )
    
    if not cmds.attributeQuery( 'centerCurve', node=surfaceObject, ex=1 ):
        cmds.addAttr( surfaceObject, ln='centerCurve', at='message' )
    cons = cmds.listConnections( surfaceObject+'.centerCurve', s=1, d=0 )
    
    if not cons:
        cmds.connectAttr( returnCurve+'.message', surfaceObject+'.centerCurve' )
        returnCurve = cmds.rename( returnCurve, surfaceObject+'_cCurve' )
    else:
        cmds.delete( returnCurve )
        returnCurve = cons[0]
    
    
    if parentNode:
        parents = cmds.listRelatives( returnCurve, p=1 )
        if parents:
            if not parentNode in parents:
                cmds.parent( returnCurve, parentNode )
        else:
            cmds.parent( returnCurve, parentNode )
    
    if cmds.nodeType( returnCurve ) != 'transform':
        return cmds.listRelatives( returnCurve, p=1 )[0]
    else:
        return returnCurve



def getClosestParam( curveShape, meshShape ):

    curveMatrix = fnc.getMMatrixFromMtxList( cmds.getAttr( curveShape+'.wm' ) )
    #curveMatrixInv = curveMatrix.inverse()
    meshMatrix  = fnc.getMMatrixFromMtxList( cmds.getAttr( meshShape+'.wm' ) )
    meshMatrixInv = meshMatrix.inverse()
    
    fnCurve = om.MFnNurbsCurve( fnc.getMObject( curveShape ) )
    fnMesh = om.MFnMesh( fnc.getMObject( meshShape ) )
    
    minParam = fnCurve.findParamFromLength( 0.0 )
    maxParam = fnCurve.findParamFromLength( fnCurve.length() )
    paramRate = (maxParam-minParam)/fnCurve.numSpans()
    
    paramPoint = om.MPoint()
    point = om.MPoint()
    normal = om.MVector()
    
    returnParam = maxParam
    searchNum = 0
    
    while searchNum < 60:
        
        if returnParam < minParam:
            returnParam = minParam
            break
        
        fnCurve.getPointAtParam( returnParam, paramPoint )
        paramPoint *= curveMatrix*meshMatrixInv
        fnMesh.getClosestPointAndNormal( paramPoint, point, normal )
        
        if paramPoint.distanceTo( point ) < 0.001:
            break
        
        pointV = om.MVector( paramPoint - point )  
        
        if paramRate > 0:
            if pointV * normal > 0:
                paramRate *= -0.5
        else:
            if pointV * normal < 0:
                paramRate *= -0.5
                
        returnParam += paramRate
        
        searchNum+=1
        
    return returnParam



def getSurfaceUpObject( curveObj, meshObj ):
    
    meshShape = cmds.listRelatives( meshObj, s=1 )[0]
    curveShape = cmds.listRelatives( curveObj, s=1 )[0]
    
    curveObj = cmds.listRelatives( curveShape, p=1 )[0]
    surfObj = cmds.listConnections( curveObj+'.message' )[0]
    
    if not cmds.attributeQuery( 'upObject', node=surfObj, ex=1 ):
        cmds.addAttr( surfObj, ln='upObject', at='message' )
    
    cons = cmds.listConnections( surfObj+'.upObject' )
    
    upObjExists = False
    if not cons:
        node = cmds.createNode( 'matrixFromPolygon', n=surfObj+'_mtxFromPoly' )
        dcmpNode = cmds.createNode( 'multMatrixDecompose', n=surfObj+'_upMtxDcmp' )
        trNodeGrp = cmds.createNode( 'transform', n=surfObj+'_upObject_GRP' )
        baseTrNodeGrp = cmds.createNode( 'transform', n=surfObj+'_baseUpObject_GRP' )
        
        trNode = cmds.createNode( 'transform', n=surfObj+'_upObject' )
        baseTrNode = cmds.createNode( 'transform', n=surfObj+'_baseUpObject' )
        #cmds.setAttr( trNode+'.dh', 1 )
        cmds.parent( trNode, trNodeGrp )
        cmds.parent( baseTrNode, baseTrNodeGrp )
        cmds.connectAttr( trNode+'.r', baseTrNode+'.r' )
        
        cmds.connectAttr( meshShape+'.outMesh', node+'.inputMesh' )
        cmds.connectAttr( meshShape+'.wm', node+'.inputMeshMatrix' )
        cmds.connectAttr( node+'.outputMatrix', dcmpNode+'.i[0]' )
        cmds.connectAttr( trNodeGrp+'.pim', dcmpNode+'.i[1]' )
        cmds.connectAttr( dcmpNode+'.ot', trNodeGrp+'.t' )
        cmds.connectAttr( dcmpNode+'.or', trNodeGrp+'.r' )
        
        cmds.connectAttr( trNodeGrp+'.message', surfObj+'.upObject' )
    else:
        trNodeGrp = cons[0]
        trNode = cmds.listRelatives( trNodeGrp, c=1 )[0]
        baseTrNode = cmds.listConnections( trNode+'.r', d=1, s=0 )[0]
        baseTrNodeGrp = cmds.listRelatives( baseTrNode, p=1 )[0]
        mtxDcmp = cmds.listConnections( trNodeGrp, s=1, d=0 )[0]
        node = cmds.listConnections( mtxDcmp+'.i[0]' )[0]
        
        upObjExists = True
    
    curveMatrix = om.MMatrix()
    meshMatrix = om.MMatrix()
    
    curveMtx = cmds.getAttr( curveShape+'.wm' )
    meshMtx = cmds.getAttr( meshShape+'.wm' )
    
    om.MScriptUtil.createMatrixFromList( curveMtx, curveMatrix )
    om.MScriptUtil.createMatrixFromList( meshMtx, meshMatrix )
    
    fnCurve = om.MFnNurbsCurve( fnc.getMObject( curveShape ) )
    fnMesh  = om.MFnMesh( fnc.getMObject( meshShape ) )
    
    minParam = fnCurve.findParamFromLength( 0 )
    
    pivPoint = om.MPoint()
    fnCurve.getPointAtParam( minParam, pivPoint )
    pivPoint *= curveMatrix * meshMatrix.inverse()
    
    closeMeshNode = cmds.createNode( 'closestPointOnMesh' )
    cmds.connectAttr( meshShape+'.outMesh', closeMeshNode+'.inMesh' )
    cmds.setAttr( closeMeshNode+'.inPosition', pivPoint.x, pivPoint.y, pivPoint.z )
    
    faceIndex = cmds.getAttr( closeMeshNode+'.closestFaceIndex' )
    cmds.delete( closeMeshNode )
    
    verties = om.MIntArray()
    fnMesh.getPolygonVertices( faceIndex, verties )
    points = om.MPointArray()
    points.setLength( verties.length() )
    
    for i in range( points.length() ):
        index = verties[i]
        fnMesh.getPoint( index, points[i] )
    
    vPoint = points[0]
    cPoint = points[1]
    uPoint = points[2]
    
    vVector = vPoint - cPoint
    uVector = uPoint - cPoint
    
    vLength = vVector.length()
    uLength = uVector.length()
    
    nVector = uVector^vVector
    nVector = nVector.normal()*( vLength + uLength )/2.0
    
    mtxList = [ nVector.x, nVector.y, nVector.z, 0,
                uVector.x, uVector.y, uVector.z, 0,
                vVector.x, vVector.y, vVector.z, 0,
                cPoint.x , cPoint.y , cPoint.z , 1 ]
    mtx = om.MMatrix()
    
    om.MScriptUtil.createMatrixFromList( mtxList, mtx )
    pivVector = pivPoint - cPoint
    
    pivVector*=mtx.inverse()
    
    uValue = pivVector.y
    vValue = pivVector.z
    
    cmds.setAttr( node+'.polygonIndex', faceIndex )
    cmds.setAttr( node+'.u', uValue )
    cmds.setAttr( node+'.v', vValue )
    
    if not upObjExists:
        mtx = cmds.getAttr( trNode+'.wm' )
        aimV = om.MVector( *mtx[:3] )
        upV  = om.MVector( 0,1,0 )
        projAimV = aimV*(upV*aimV)/(aimV.length()**2)
        upV = upV - projAimV
        
        aimV.normalize()
        upV.normalize()
        byNormal = upV^aimV
        
        mtx = [ aimV.x, aimV.y, aimV.z, 0, 
                byNormal.x, byNormal.y, byNormal.z, 0,
                upV.x, upV.y, upV.z, 0,
                mtx[12], mtx[13], mtx[14], 1 ]
        
        cmds.xform( trNode, ws=1, matrix=mtx )
        
    trans = cmds.getAttr( trNodeGrp+'.t' )[0]
    rotate = cmds.getAttr( trNodeGrp+'.r' )[0]
    
    cmds.setAttr( baseTrNodeGrp+'.t', *trans )
    cmds.setAttr( baseTrNodeGrp+'.r', *rotate )
    
    return trNode, baseTrNode
   
    

class AddControlerToCurve:

    def __init__( self, upMatrixNode, curveObject, surfaceObject, controlNum, offset = 0.5 ):
        
        baseUpMatrixNode = cmds.listConnections( upMatrixNode+'.r', s=0, d=1 )[0]
        
        curveShape = fnc.getShapeFromObject( curveObject, 'nurbsCurve' )
        
        splineMatrixNode = self.getSplineMatrixNode( curveObject, upMatrixNode, baseUpMatrixNode )
        clusterControlNode = self.getClusterControlNode( curveObject, baseUpMatrixNode )

        cons = cmds.listConnections( clusterControlNode+'.bindPreMatrix' )
        
        
        if cons:
            beforeInvMatrix = cons[-1]
            startNum = len( cons )
            
            if startNum == controlNum:
                matrixCons = cmds.listConnections( clusterControlNode+'.matrix' )
                
                for dCtl in matrixCons:
                    
                    index = matrixCons.index( dCtl )
                    
                    dCtlGrp = cmds.listRelatives( dCtl, p=1 )[0]
                    ctlGrp = cmds.listRelatives( dCtlGrp, p=1 )[0]
                    ctl = cmds.listRelatives( ctlGrp, c=1 )[1]
                    cmds.setAttr( ctl+'.parameter', float( index )/(controlNum-1) )
                    
                    cmds.setAttr( dCtl+'.t', 0,0,0 )
                    cmds.setAttr( dCtl+'.r', 0,0,0 )
                    cmds.setAttr( dCtl+'.s', 1,1,1 )
                    
                    cmds.setAttr( ctl+'.t', 0,0,0 )
                    cmds.setAttr( ctl+'.r', 0,0,0 )
                    cmds.setAttr( ctl+'.s', 1,1,1 )
                    
                    upMatrixNode = ctl
                    
                self.updateNodes( splineMatrixNode, clusterControlNode, None )
                return None
            elif startNum > controlNum:
                matrixCons = cmds.listConnections( clusterControlNode+'.matrix' )
                
                for dCtl in matrixCons:
                    
                    index = matrixCons.index( dCtl )
                    
                    dCtlGrp = cmds.listRelatives( dCtl, p=1 )[0]
                    ctlGrp = cmds.listRelatives( dCtlGrp, p=1 )[0]
                    ctl = cmds.listRelatives( ctlGrp, c=1 )[1]
                    
                    if index == controlNum:
                        cmds.delete( ctlGrp, cons[controlNum:] )
                        break
                    
                    cmds.setAttr( ctl+'.parameter', float( index )/(controlNum-1) )
                
                self.updateNodes( splineMatrixNode, clusterControlNode, None )
                return None
            else:
                matrixCons = cmds.listConnections( clusterControlNode+'.matrix' )
                
                for dCtl in matrixCons:
                    
                    index = matrixCons.index( dCtl )
                    
                    dCtlGrp = cmds.listRelatives( dCtl, p=1 )[0]
                    ctlGrp = cmds.listRelatives( dCtlGrp, p=1 )[0]
                    ctl = cmds.listRelatives( ctlGrp, c=1 )[1]
                    cmds.setAttr( ctl+'.parameter', float( index )/(controlNum-1) )
                    
                    cmds.setAttr( dCtl+'.t', 0,0,0 )
                    cmds.setAttr( dCtl+'.r', 0,0,0 )
                    cmds.setAttr( dCtl+'.s', 1,1,1 )
                    
                    cmds.setAttr( ctl+'.t', 0,0,0 )
                    cmds.setAttr( ctl+'.r', 0,0,0 )
                    cmds.setAttr( ctl+'.s', 1,1,1 )
                    
                    upMatrixNode = ctl
            
        else:
            beforeInvMatrix = None
            startNum = 0
            
        
        ctlGroups = []
        for i in range( startNum, controlNum ):
            dcMtx = cmds.createNode( 'multMatrixDecompose', n=curveObject+'_%d_ctlDcMtx' % i )
            cmds.connectAttr( splineMatrixNode+'.outputMatrix[%d]' % i, dcMtx+'.i[0]' )
            
            if i == 0:
                cmds.connectAttr( upMatrixNode+'.wim', dcMtx+'.i[1]' )
            else:
                if not cmds.isConnected( splineMatrixNode+'.outputMatrix[%d]' % (i-1), beforeInvMatrix+'.inputMatrix' ):
                    cmds.connectAttr( splineMatrixNode+'.outputMatrix[%d]' % (i-1), beforeInvMatrix+'.inputMatrix' )
                cmds.connectAttr( beforeInvMatrix+'.outputMatrix', dcMtx+'.i[1]')
                if not cmds.isConnected( beforeInvMatrix+'.outputMatrix', clusterControlNode+'.bindPreMatrix[%d]' % (i-1) ):
                    cmds.connectAttr( beforeInvMatrix+'.outputMatrix', clusterControlNode+'.bindPreMatrix[%d]' % (i-1) )
        
            defaultParamValue = i/( controlNum-1.0)+0.001
            
            dCtlNode, ctlNode, ctlGrp = self.getControlerFromSurfaceObject( curveObject+'_%d_CTL' % i, curveObject, surfaceObject, splineMatrixNode, defaultParamValue, i, offset )
            ctlGroups.append( (dCtlNode, ctlNode, ctlGrp) )
            
            cmds.parent( ctlGrp, upMatrixNode )
            cmds.connectAttr( dcMtx+'.ot', ctlGrp+'.t' )
            cmds.connectAttr( dcMtx+'.or', ctlGrp+'.r' )
            
            upMatrixNode = ctlNode
            cmds.connectAttr( dCtlNode+'.wm', clusterControlNode+'.matrix[%d]' % i )
            
            beforeInvMatrix = cmds.createNode( 'inverseMatrix', n=curveObject+'_%d_ctlInvMtx' % i )
            
        cmds.connectAttr( splineMatrixNode+'.outputMatrix[%d]' % i, beforeInvMatrix+'.inputMatrix' )
        cmds.connectAttr( beforeInvMatrix+'.outputMatrix', clusterControlNode+'.bindPreMatrix[%d]' % i )
        if not cmds.isConnected( clusterControlNode+'.outputCurve', curveShape+'.create' ):
            cmds.connectAttr( clusterControlNode+'.outputCurve', curveShape+'.create', f=1 )
        
        '''
        for i in range( startNum, controlNum ):
            dCtl, ctl, ctlGrp = ctlGroups[i-startNum]
            self.addSurfaceEditControl( clusterControlSurfNode, dCtl, ctlGrp, i )
            
        self.updateNodes( splineMatrixNode, clusterControlNode, clusterControlSurfNode )
        '''
            
    
    def updateNodes(self, splineMatrixNode, clusterControlNode, clusterControlSurfNode ):
        
        fnc.clearArrayElement( splineMatrixNode+'.parameter')
        fnc.clearArrayElement( clusterControlNode+'.matrix')
        fnc.clearArrayElement( clusterControlNode+'.bindPreMatrix')
        if clusterControlSurfNode:
            fnc.clearArrayElement( clusterControlSurfNode+'.upMatrix' )
            fnc.clearArrayElement( clusterControlSurfNode+'.baseUpMatrix' )
        
        cmds.setAttr( clusterControlNode+'.update', True )
        cmds.refresh()
        cmds.setAttr( clusterControlNode+'.update', False )


    def addSurfaceEditControl(self, clusterControlSurfNode, ctlNode, ctlGrp, index ):
        
        ctlMtxNode = cmds.listConnections( ctlGrp, type='multMatrixDecompose', s=1, d=0 )[0]
        sourceMtxAttr = cmds.listConnections( ctlMtxNode+'.matrixIn[0]', p=1, c=1 )[1]
        
        if not cmds.listConnections( clusterControlSurfNode+'.baseUpMatrix[%d]' % index ):
            cmds.connectAttr( sourceMtxAttr, clusterControlSurfNode+'.baseUpMatrix[%d]' % index )
        if not cmds.listConnections( clusterControlSurfNode+'.upMatrix[%d]' % index ):
            cmds.connectAttr( ctlNode+'.wm', clusterControlSurfNode+'.upMatrix[%d]' % index )


    def getClusterControledSurfNode(self, surfaceObject, curveObject, clusterControlNode ):
        
        surfShape = cmds.listRelatives( surfaceObject, s=1 )[0]
        surfSourceCon = cmds.listConnections( surfShape+'.create' )
        if not surfSourceCon:
            fnc.getOrigShape( surfShape )
        surfSourceAttr = cmds.listConnections( surfShape+'.create', p=1, c=1 )[1]
        sourceNode = surfSourceAttr.split( '.' )[0]
        
        curveShape = fnc.getShapeFromObject( curveObject, 'nurbsCurve' )
        
        hists = cmds.listHistory( curveShape, pdo=1 )
        for hist in hists:
            if cmds.nodeType( hist ) == 'rebuildCurve':
                curveSourceAttr = hist+'.outputCurve'
        
        if cmds.nodeType( sourceNode ) == 'clusterControledSurface':
            if not cmds.listConnections( sourceNode+'.inputOrigCurve' ):
                cmds.connectAttr( curveSourceAttr, sourceNode+'.inputOrigCurve' )
            if not cmds.listConnections( sourceNode+'.inputCurve' ):
                cmds.connectAttr( curveShape+'.local', sourceNode+'.inputCurve' )
            if not cmds.listConnections( sourceNode+'.inputOrigCurveMatrix' ):
                cmds.connectAttr( curveObject+'.wm', sourceNode+'.inputOrigCurveMatrix' )
            if not cmds.listConnections( sourceNode+'.inputCurveMatrix' ):
                cmds.connectAttr( curveObject+'.wm', sourceNode+'.inputCurveMatrix' )
            return sourceNode
        
        node = cmds.createNode( 'clusterControledSurface' )
        
        cmds.connectAttr( curveSourceAttr, node+'.inputOrigCurve' )
        cmds.connectAttr( curveShape+'.local', node+'.inputCurve' )
        cmds.connectAttr( curveObject+'.wm', node+'.inputOrigCurveMatrix' )
        cmds.connectAttr( curveObject+'.wm', node+'.inputCurveMatrix' )
        cmds.connectAttr( clusterControlNode+'.weightChanged', node+'.checkPoint', f=1 )
        
        
        cmds.connectAttr( surfSourceAttr, node+'.inputSurface' )
        cmds.connectAttr( surfaceObject+'.wm', node+'.inputSurfaceMatrix' )
        cmds.connectAttr( node+'.outputSurface', surfShape+'.create', f=1 )
        
        return node
    
    
    def getSplineMatrixNode(self, curveObject, upMatrixNode, baseUpMatrixNode ):
        
        upMatrixGrp = cmds.listRelatives( upMatrixNode, p=1 )[0]
        baseUpMatrixGrp = cmds.listRelatives( baseUpMatrixNode, p=1 )[0]
        
        hists = cmds.listHistory( curveObject )
        for hist in hists:
            if cmds.nodeType( hist ) == 'detachCurve':
                detachNode = hist
        destCons   = cmds.listConnections( curveObject+'.wm', s=0, d=1, type='splineMatrix' )
        if destCons:
            return destCons[0]
        
        splineMatrixNode = cmds.createNode( 'splineMatrix', n=curveObject+'_splineMatrix' )
        trGeo = cmds.createNode( 'transformGeometry', n=curveObject+'_trGeo' )
        mtx = cmds.createNode( 'multMatrixDecompose', n=curveObject+'_trMtxDcmp' )
        cmds.connectAttr( upMatrixNode+'.wm', splineMatrixNode+'.topMatrix' )
        cmds.connectAttr( detachNode+'.outputCurve[1]', splineMatrixNode+'.inputCurve' )
        cmds.connectAttr( curveObject+'.wm', splineMatrixNode+'.inputCurveMatrix' )
        
        return splineMatrixNode


    def getClusterControlNode( self, curveObject, baseUpObject ):
        
        curveShapes = cmds.listRelatives( curveObject, s=1 )
        
        for shape in curveShapes:
            if cmds.getAttr( shape+'.io' ) == 0:
                curveShape = shape
                break
        
        sourceCons = cmds.listConnections( curveShape+'.create', s=1, d=0, p=1, c=1 )

        sourceNode = sourceCons[1].split( '.' )[0]
        if cmds.nodeType( sourceNode ) == 'clusterControledCurve':
            return sourceNode
        
        clusterControlNode = cmds.createNode( 'clusterControledCurve', n=curveObject+'_clusterControl' )

        cmds.connectAttr( sourceCons[1], clusterControlNode+'.inputCurve' )
        cmds.connectAttr( curveObject+'.wm', clusterControlNode+'.inputCurveMatrix' )
        cmds.connectAttr( baseUpObject+'.wm', clusterControlNode+'.dumyMatrix' )
        
        return clusterControlNode


    def getControlerFromSurfaceObject(self, controlerName, curveObject, surfaceObject, splineMatrixNode, defaultParamValue, index, offset ):
        
        ctlNode = cmds.curve( p=[(0,0,0),(0,0,0)], degree=1, n=controlerName )
        
        dCtlNode = cmds.group( em=1, n= controlerName.replace( 'CTL', 'dCTL' ) )

        #cmds.setAttr( dCtlNode+'.dh', 1 )
        dCtlNodeGrp = cmds.group( dCtlNode, n= dCtlNode+'_GRP' )
        
        cmds.addAttr( ctlNode, ln='parameter', min=0, max=1, dv=defaultParamValue )
        cmds.setAttr( ctlNode+'.parameter', e=1, k=1 )
        cmds.connectAttr( ctlNode+'.parameter', splineMatrixNode+'.parameter[%d]' % index )
        ctlGrp  = cmds.group( dCtlNodeGrp, ctlNode, n= ctlNode+'_GRP' )
        ctlNodeShape = cmds.listRelatives( ctlNode, s=1 )[0]
        cmds.connectAttr( ctlNode+'.t', dCtlNodeGrp+'.t' )
        
        curveShape = cmds.listRelatives( curveObject, s=1 )[0]
        surfaceShape = cmds.listRelatives( surfaceObject, s=1 )[0]
        cons = cmds.listConnections( surfaceShape+'.worldSpace', s=0, d=1, type='offsetSurface' )
        
        if cons:
            offsetSurface = cons[0]
        else:
            offsetSurface = cmds.createNode( 'offsetSurface', n=surfaceObject+'_offsetSurf' )
            cmds.connectAttr( surfaceShape+'.worldSpace', offsetSurface+'.inputSurface' )
            cmds.setAttr( offsetSurface+'.distance', offset )
            
        curveOnSurf = cmds.createNode( 'curveFromSurfaceIso', n= controlerName.replace( 'CTL', 'curveOnSurf' ) )
        cmds.setAttr( curveOnSurf+'.isoparmDirection', 1 )
        cmds.setAttr( curveOnSurf+'.relativeValue', 1 )
        
        for hist in cmds.listHistory( curveObject ):
            if cmds.nodeType( hist ) == 'detachCurve':
                detachCurve = hist
                break
            else:
                detachCurve = None
                
        if not detachCurve:
            return None
                
        paramRange = cmds.createNode( 'setRange', n=controlerName.replace( 'CTL', 'paramRange' ) )
        paramDiv = cmds.createNode( 'multiplyDivide', n=controlerName.replace( 'CTL', 'paramDiv' ) )
        cmds.setAttr( paramDiv+'.op', 2 )
        cmds.setAttr( paramRange+'.oldMaxX', 1 )
        cmds.connectAttr( detachCurve+'.parameter[0]', paramRange+'.minX' )
        cmds.connectAttr( surfaceShape+'.spansU', paramRange+'.maxX' )
        cmds.connectAttr( paramRange+'.outValueX', paramDiv+'.input1X' )
        cmds.connectAttr( surfaceShape+'.spansU', paramDiv+'.input2X' )
        cmds.connectAttr( ctlNode+'.parameter', paramRange+'.valueX' )
        
        cmds.connectAttr( paramDiv+'.outputX', curveOnSurf+'.isoparmValue' )
        trGeo  = cmds.createNode( 'transformGeometry', n= controlerName.replace( 'CTL', 'trGeo' ) )
        cmds.connectAttr( offsetSurface+'.outputSurface', curveOnSurf+'.inputSurface' )
        cmds.connectAttr( curveOnSurf+'.outputCurve', trGeo+'.inputGeometry' )
        cmds.connectAttr( trGeo+'.outputGeometry', ctlNodeShape+'.create' )
        cmds.connectAttr( ctlNode+'.wim', trGeo+'.transform' )
        
        return dCtlNode, ctlNode, ctlGrp
    
        

def getDynamicCurve( surfaceObject ):
    
    centerCurveObj = cmds.listConnections( surfaceObject+'.centerCurve' )[0]
    centerCurveShape = fnc.getShapeFromObject( centerCurveObj )
        
    rebuildCons = cmds.listConnections( centerCurveShape, s=0, d=1, type='rebuildCurve' )
    
    if not rebuildCons:
        dRebuild = cmds.createNode( 'rebuildCurve', n=centerCurveShape.replace( 'cCurveShahpe', 'degreeRebuild' ) )
        cmds.connectAttr( centerCurveShape+'.local', dRebuild+'.inputCurve' )
        cmds.setAttr( dRebuild+'.degree', 1 )
        cmds.setAttr( dRebuild+'.keepControlPoints', 1 )
        cmds.setAttr( dRebuild+'.keepTangents', 0 )
        cmds.setAttr( dRebuild+'.keepRange', 0 )
    else:
        dRebuild = rebuildCons[0]
        
    oneDCurveCons = cmds.listConnections( dRebuild, s=0, d=1, type='nurbsCurve' )
    
    if not oneDCurveCons:
        oneDCurveShape = cmds.createNode( 'nurbsCurve', n=centerCurveShape.replace( 'cCurveShape', 'c1DegreeShape' ) )
        oneDCurveObj = cmds.listRelatives( oneDCurveShape, p=1 )[0]
        cmds.parent( oneDCurveShape, centerCurveObj, add=1, shape=1 )
        cmds.delete( oneDCurveObj )
        cmds.connectAttr( dRebuild+'.outputCurve', oneDCurveShape+'.create' )
        cmds.setAttr( oneDCurveShape+'.io', 1 )
    else:
        oneDCurveShape = cmds.listRelatives( oneDCurveCons[0], s=1 )
    
    follicleCons = cmds.listConnections( oneDCurveShape, s=0, d=1, type='follicle' )
    
    if not follicleCons:
        follicle = cmds.createNode( 'follicle', n=centerCurveShape.replace( 'cCurveShape', 'follicle' ) )
        cmds.connectAttr( oneDCurveShape+'.local', follicle+'.startPosition' )
        cmds.connectAttr( oneDCurveShape+'.worldMatrix', follicle+'.startPositionMatrix' )
        cmds.connectAttr( centerCurveShape+'.degree', follicle+'.degree' )
        cmds.setAttr( follicle+'.startDirection', 1 )
    else:
        follicle = cmds.listRelatives( follicleCons[0], s=1 )[0]
    
    follicleObj = cmds.listRelatives( follicle, p=1 )[0]
    if not cmds.attributeQuery( 'follicle',node=surfaceObject, ex=1 ):
        cmds.addAttr( surfaceObject, ln='follicle', at='message' )
    if not cmds.isConnected( follicleObj+'.message', surfaceObject+'.follicle' ):
        cmds.connectAttr( follicleObj+'.message', surfaceObject+'.follicle' )
        
    surfObjGrp = cmds.listRelatives( surfaceObject, p=1 )[0]
    hairSystemCons = cmds.listConnections( surfObjGrp, type='hairSystem' )
    
    if not hairSystemCons:
        hairSystem = cmds.createNode( 'hairSystem', n=centerCurveShape.replace( 'cCurveShape', 'hairSystem' ) )
        
        if not cmds.attributeQuery( 'hairSystem', node = surfObjGrp, ex=1 ):
            cmds.addAttr( surfObjGrp, ln='hairSystem', at='message' )
        
        if not cmds.isConnected( hairSystem+'.message', surfObjGrp+'.hairSystem' ):
            cmds.connectAttr( hairSystem+'.message', surfObjGrp+'.hairSystem' )
        cmds.setAttr( hairSystem+'.active', 1 )
        
        nucleus = cmds.createNode( 'nucleus' )
        cmds.connectAttr( nucleus+'.outputObjects[0]', hairSystem+'.nextState' )
        cmds.connectAttr( nucleus+'.startFrame', hairSystem+'.startFrame' )
        cmds.connectAttr( hairSystem+'.currentState', nucleus+'.inputActive[0]' )
        cmds.connectAttr( hairSystem+'.startState', nucleus+'.inputActiveStart[0]' )
        
        cmds.connectAttr( 'time1.outTime', hairSystem+'.currentTime' )
        cmds.connectAttr( 'time1.outTime', nucleus+'.currentTime' )
    else:
        hairSystem = cmds.listRelatives( hairSystemCons[0], s=1 )[0]
    
    fnc.clearArrayElement( hairSystem+'.inputHair' )
    currentIndex = fnc.getLastIndex( hairSystem+'.inputHair' )+1
    
    if not cmds.listConnections( follicle+'.outHair', type='hairSystem' ):
        cmds.connectAttr( follicle+'.outHair', hairSystem+'.inputHair[%d]' % currentIndex )
        cmds.connectAttr( hairSystem+'.outputHair[%d]' % currentIndex , follicle+'.currentPosition' )
        currentShape = cmds.createNode( 'nurbsCurve', n=centerCurveShape.replace( 'cCurveShape', 'currentShape' )  )
        cmds.connectAttr( follicle+'.outCurve', currentShape+'.create' )
        currentObj = cmds.listRelatives( currentShape, p=1 )[0]
    else:
        currentObj = cmds.listConnections( follicle+'.outCurve' )[0]
    
    if not cmds.attributeQuery( 'currentCurve',node=surfaceObject, ex=1 ):
            cmds.addAttr( surfaceObject, ln='currentCurve', at='message' )
    if not cmds.isConnected( currentObj+'.message', surfaceObject+'.currentCurve' ):
        cmds.connectAttr( currentObj+'.message', surfaceObject+'.currentCurve' )
        
    return currentObj, follicleObj



def setDynamicSurface( surfaceObject, centerCurveObj, currentCurveObj, upObject, baseUpObject ):
    
    surfShape = fnc.getShapeFromObject( surfaceObject )
    
    if cmds.listConnections( surfShape, s=1, d=0, type='simulatedCurveControledSurface' ):
        return None
    
    rebuildSurface = cmds.listConnections( surfShape, s=1, d=0, type='rebuildSurface' )[0]
    centerShape = fnc.getShapeFromObject( centerCurveObj )
    currentShape = fnc.getShapeFromObject( currentCurveObj )
    
    hists = cmds.listHistory( centerShape, pdo=1 )
    
    for hist in hists:
        if cmds.nodeType( hist ) == 'rebuildCurve':
            rebuildCurve = hist
            break
    
    nodeCons = cmds.listConnections( surfShape+'.create', type='simulatedCurveControledSurface' )
    
    if not nodeCons:
        node = cmds.createNode( 'simulatedCurveControledSurface', n=surfaceObject+'_simulateSurface' )
    else:
        node = nodeCons[0]
    
    if not cmds.isConnected( surfShape+'.wm', node+'.baseSurfaceMatrix' ):
        cmds.connectAttr( surfShape+'.wm', node+'.baseSurfaceMatrix',f=1 )  
    if not cmds.isConnected( rebuildSurface+'.outputSurface', node+'.baseSurface' ):
        cmds.connectAttr( rebuildSurface+'.outputSurface', node+'.baseSurface',f=1 )
    if not cmds.isConnected( rebuildCurve+'.outputCurve', node+'.baseCurve' ):
        cmds.connectAttr( rebuildCurve+'.outputCurve', node+'.baseCurve',f=1 )
    if not cmds.isConnected( currentShape+'.local', node+'.moveCurve' ):
        cmds.connectAttr( currentShape+'.local', node+'.moveCurve',f=1 )
    if not cmds.isConnected( baseUpObject+'.worldMatrix', node+'.baseUpMatrix' ):
        cmds.connectAttr( baseUpObject+'.worldMatrix', node+'.baseUpMatrix',f=1 )
    if not cmds.isConnected( upObject+'.worldMatrix', node+'.moveUpMatrix' ):
        cmds.connectAttr( upObject+'.worldMatrix', node+'.moveUpMatrix',f=1 )
    if not cmds.isConnected( node+'.outputSurface', surfShape+'.create' ):
        cmds.connectAttr( node+'.outputSurface', surfShape+'.create',f=1 )
    if not cmds.isConnected( 'time1.outTime', node+'.currentTime' ):
        cmds.connectAttr( 'time1.outTime', node+'.currentTime' )
        
    for attr in ['tx','ty','tz','rx','ry','rz','sx','sy','sz']:
        cmds.setAttr( surfaceObject+'.'+attr, e=1, lock=1 )

        
        
def removeControler( upObject, centerCurveObj ):
    centerCurveShape = fnc.getShapeFromObject( centerCurveObj )
    
    clusterNode = None
    rebuildNode = None
    
    for hist in cmds.listHistory( centerCurveShape, pdo=1 ):
        if cmds.nodeType( hist ) == 'clusterControledCurve':
            clusterNode = hist
        if cmds.nodeType( hist ) == 'rebuildCurve':
            rebuildNode = hist
    
    if not clusterNode or not rebuildNode: return None
            
    cmds.delete( clusterNode )
    cmds.connectAttr( rebuildNode+'.outputCurve', centerCurveShape+'.create' )
    
    upObjectChildren = cmds.listRelatives( upObject, c=1 )
    cmds.delete( upObjectChildren )



def attachStartCurveToHead( startCurve, upObjectGrp, baseUpObjectGrp ):
    if not cmds.listConnections( startCurve, s=1, d=0, type='multMatrixDecompose' ):
        mtxDcmp = cmds.createNode( 'multMatrixDecompose', n= startCurve+'_mtxDcmp' )
        cmds.connectAttr( baseUpObjectGrp+'.wim', mtxDcmp+'.i[0]' )
        cmds.connectAttr( upObjectGrp+'.wm', mtxDcmp+'.i[1]' )
        cmds.connectAttr( mtxDcmp+'.ot', startCurve+'.t' )
        cmds.connectAttr( mtxDcmp+'.or', startCurve+'.r' )



def transformGeoSet( upObjectGrp, baseUpObjectGrp, cCurveShape ):
    
    rebuildCurve = ''
    detachCurve  = ''
    
    hists = cmds.listHistory( cCurveShape, pdo=1 )
    
    if not hists:
        return None
    
    for hist in hists:
        if cmds.nodeType( hist ) == 'rebuildCurve':
            rebuildCurve = hist
        elif cmds.nodeType( hist ) == 'detachCurve':
            detachCurve = hist
    
    mtxCons = cmds.listConnections( baseUpObjectGrp+'.wim', type='multMatrix' )
    
    mtxNode = ''
    if mtxCons:
        mtxNode = mtxCons[0]
    else:
        mtxNode = cmds.createNode( 'multMatrix', n= cCurveShape+'_trGeo' )
        cmds.connectAttr( baseUpObjectGrp+'.wim', mtxNode+'.i[0]' )
        cmds.connectAttr( upObjectGrp+'.wm', mtxNode+'.i[1]' )
        
    if detachCurve:
        trGeo = ''
        destCons = cmds.listConnections( detachCurve+'.outputCurve[1]', type='splineMatrix' )
        if destCons:
            for destCon in destCons:
                if cmds.nodeType( destCon ) == 'transformGeometry':
                    trGeo = destCon
        if not trGeo:
            cons = cmds.listConnections( detachCurve+'.outputCurve[1]', type='splineMatrix' )
            
            if cons:
                trGeo = cmds.createNode( 'transformGeometry', n=cCurveShape+'_trGeoDetach' )
                cmds.connectAttr( detachCurve+'.outputCurve[1]', trGeo+'.inputGeometry' )
                cmds.connectAttr( mtxNode+'.matrixSum', trGeo+'.transform' )
                cmds.connectAttr( trGeo+'.outputGeometry', cons[0]+'.inputCurve', f=1 )
        
    if rebuildCurve:
        trGeo = ''
        destCons = cmds.listConnections( rebuildCurve+'.outputCurve', type='clusterControledCurve' )
        if destCons:
            for destCon in destCons:
                if cmds.nodeType( destCon ) == 'transformGeometry':
                    trGeo = destCon
        if not trGeo:
            cons = cmds.listConnections( rebuildCurve+'.outputCurve', type='clusterControledCurve', p=1, c=1 )
            
            if not cons:
                cons = cmds.listConnections( rebuildCurve+'.outputCurve', type='nurbsCurve', p=1, c=1 )
                
            print cons
            
            if cons:
                trGeo = cmds.createNode( 'transformGeometry', n=cCurveShape+'_trGeoRebuild' )
                cmds.connectAttr( rebuildCurve+'.outputCurve', trGeo+'.inputGeometry' )
                cmds.connectAttr( mtxNode+'.matrixSum', trGeo+'.transform' )
                cmds.connectAttr( trGeo+'.outputGeometry', cons[1], f=1 )



def allSet( surfaceShape, meshShape, addControl = False, numControl=5, offset=0.5 ):
    
    surfaceObj = cmds.listRelatives( surfaceShape, p=1 )[0]
    meshObj    = cmds.listRelatives( meshShape, p=1 )[0]
    
    centerCurveObj = getSurfaceCenterCurve( surfaceObj, meshObj )
    upObject, baseUpObject = getSurfaceUpObject( centerCurveObj, meshObj )
    upObjectGrp    = cmds.listRelatives( upObject, p=1 )[0]
    baseUpObjectGrp = cmds.listRelatives( baseUpObject, p=1 )[0]
    
    currentObj, follicleObj = getDynamicCurve( surfaceObj )
    
    if addControl:
        AddControlerToCurve( upObject, centerCurveObj, surfaceObj, numControl, offset )
    else:
        removeControler( upObject, centerCurveObj )
    
    cCurveShape = fnc.getShapeFromObject( centerCurveObj )
    transformGeoSet( upObjectGrp, baseUpObjectGrp, cCurveShape )
    
    setGrp( centerCurveObj, 'cCurveGrp' )
    setGrp( upObjectGrp, 'upObjectGrp' )
    setGrp( currentObj, 'currentGrp' )
    setGrp( follicleObj, 'follicleGrp' )
    
    upObjectGrp_p = cmds.listRelatives( upObjectGrp, p=1 )
    if cmds.listRelatives( baseUpObjectGrp, p=1 ) != upObjectGrp_p:
        cmds.parent( baseUpObjectGrp, upObjectGrp_p[0] )
    
    setDynamicSurface( surfaceObj, centerCurveObj, currentObj, upObject, baseUpObject )