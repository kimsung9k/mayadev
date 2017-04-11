import maya.OpenMaya as om
import maya.cmds as cmds


def createRivetLineAuto( selObjects, rivetType='joint' ):

    import sgBFunction_mesh
    shapeName, indices = sgBFunction_mesh.getMeshAndIndicesPoints( selObjects )
    
    rivetObjs = []
    for meshVtxIndex in indices:
        
        meshVertex = shapeName+'.vtx[%d]'% meshVtxIndex
        
        selectNum = meshVtxIndex
        edges = cmds.polyListComponentConversion( meshVertex, toEdge=1 )
        vts   = cmds.polyListComponentConversion( edges, toVertex=1 )
        vts   = cmds.ls( vts, fl=1 )
        
        targetNums = []
        for vtx in vts:
            num = int( vtx.split( '[' )[-1].replace( ']', '' ) )
            targetNums.append( num )
        
        targetNums.remove( selectNum )
        
        aimIndices = []
        upIndices  = []
        for num in targetNums:
            if num in indices:
                aimIndices.append( num )
            else:
                upIndices.append( num )    
        
        rivetObject = sgBFunction_mesh.createMeshRivet( shapeName, selectNum, [selectNum], [selectNum], [selectNum], [selectNum], 0, 1, rivetType )
        rivetObjs.append( rivetObject )
        
        rivetNode = cmds.listConnections( rivetObject+'.t' )[0]
        
        if len( aimIndices ) == 2:
            cmds.setAttr( rivetNode+'.aimPivIndices[0]', aimIndices[0] )
            cmds.setAttr( rivetNode+'.aimIndices[0]', aimIndices[1] )
        elif len( aimIndices ) == 1:
            cmds.setAttr( rivetNode+'.aimIndices[0]', aimIndices[0] )
        
        if len( upIndices ) == 2:
            cmds.setAttr( rivetNode+'.upPivIndices[0]', upIndices[0] )
            cmds.setAttr( rivetNode+'.upIndices[0]', upIndices[1] )
        elif len( upIndices ) == 1:
            cmds.setAttr( rivetNode+'.upIndices[0]', upIndices[0] )
    
    return cmds.group( rivetObjs )




def createFollicleOnVertices( vertices ):
    
    import sgBFunction_dag
    import sgBFunction_mesh
    
    vertices = cmds.ls( vertices, fl=1 )
    
    for vertex in vertices:
        
        vtxPos = cmds.xform( vertex, q=1, ws=1, t=1 )
        mesh = vertex.split( '.' )[0]
        meshShape = sgBFunction_dag.getShape( mesh )
        u, v = sgBFunction_mesh.getUVAtPoint( vtxPos, mesh )
        
        follicleNode = cmds.createNode( 'follicle' )
        follicle = cmds.listRelatives( follicleNode, p=1, f=1 )[0]
        
        cmds.connectAttr( meshShape+'.outMesh', follicleNode+'.inputMesh' )
        cmds.connectAttr( meshShape+'.wm', follicleNode+'.inputWorldMatrix' )
        
        cmds.setAttr( follicleNode+'.parameterU', u )
        cmds.setAttr( follicleNode+'.parameterV', v )
        
        cmds.connectAttr( follicleNode+'.outTranslate', follicle+'.t' )
        cmds.connectAttr( follicleNode+'.outRotate', follicle+'.r' )



def createCurveFromSelVertices():
    
    import sgBModel_data
    import sgBFunction_base
    import sgBFunction_dag
    
    sgBFunction_base.autoLoadPlugin( 'sgRigAddition' )
    
    vertices = sgBModel_data.orderedVertices
    
    def getMeshAndIndices( vertices ):
        meshName = sgBFunction_dag.getShape( vertices[0].split( '.' )[0] )
        indices = []
        for vtx in vertices:
            vtxName = vtx.split( '.' )[1]
            
            index = int( vtxName.split( '[' )[-1].replace( ']', '' ) )
            indices.append( index )
        return meshName, indices
    
    def createCurve( mesh, indices ):
        cons = cmds.listConnections( mesh+'.outMesh', type='sgVerticeToCurve', d=1, s=0 )
        if not cons:
            vtsToCrv = cmds.createNode( 'sgVerticeToCurve'  )
            cmds.connectAttr( mesh+'.outMesh', vtsToCrv+'.inputMesh' )
            cmds.connectAttr( mesh+'.wm', vtsToCrv+'.inputMeshMatrix' )
            targetIndex = 0
        else:
            vtsToCrv = cons[0]
            cons = cmds.listConnections( vtsToCrv+'.outputCurve', p=1, c=1 )
            outputs = cons[::2]
            targetIndex = int( outputs[-1].split( '[' )[-1].replace( ']', '' ) ) + 1
        
        crv = cmds.createNode( 'nurbsCurve' )
        crvObj = cmds.listRelatives( crv, p=1, f=1 )[0]
        cmds.connectAttr( vtsToCrv+'.outputCurve[%d]' % targetIndex, crv+'.create' )
        cmds.connectAttr( crvObj+'.wim', vtsToCrv+'.input[%d].pim' % targetIndex, f=1 )
        attrs = cmds.ls( vtsToCrv+'.input[%d].verticeIds[*]' % targetIndex )
        for attr in attrs:
            cmds.removeMultiInstance( attr )
        for i in range( len( indices ) ):
            if indices[i] == 0: indices[i] = -1
            cmds.setAttr( vtsToCrv+'.input[%d].verticeIds[%d]' % (targetIndex,i), indices[i] )

    mesh, indices = getMeshAndIndices( vertices )
    createCurve( mesh, indices )



def createCurveFromSelVertices_mirror( targetCurve ):
    
    import sgBFunction_dag
    
    def getMeshAndIndices( targetCurve ):
        curveShape = sgBFunction_dag.getShape( targetCurve )
        
        inputNode = curveShape
        crvToPointNode = None
        mtxFromVtxNode = None
        num = 0
        while True:
            num += 1
            if num >= 100: break
            cons = cmds.listConnections( inputNode, s=1, d=0, p=1, c=1 )
            if not cons: return None
            outputCon = cons[1]
            node = outputCon.split( '.' )[0]
            targetNodeType = cmds.nodeType( node )
            if targetNodeType == 'sgCurveFromPoints':
                crvToPointNode = node
                inputNode = node
                continue
            if targetNodeType == 'sgMatrixFromVertices':
                mtxFromVtxNode = node
                break
            inputNode = node

        mesh = cmds.listConnections( mtxFromVtxNode+'.inputMesh', s=1, d=0 )[0]
        
        print "crvToPointNode : ", crvToPointNode
        fnNode = om.MFnDependencyNode( sgBFunction_dag.getMObject( crvToPointNode ) )
        plugInputs = fnNode.findPlug( 'input' )
        
        indices = []
        for i in range( plugInputs.numElements() ):
            connections = om.MPlugArray()
            plugInputPoint = plugInputs[i].child( 1 )
            plugInputPoint.connectedTo( connections, True, False )
            indices.append( connections[0].logicalIndex() )
        
        return mesh, indices
        
    
    def createCurve( mesh, indices ):
        
        vtsToCrv = cmds.createNode( 'sgMatrixFromVertices'  )
        pointToCrv = cmds.createNode( 'sgCurveFromPoints' )
        crv = cmds.createNode( 'nurbsCurve' )
        
        cmds.connectAttr( pointToCrv+'.outputCurve', crv+'.create' )
        
        cmds.connectAttr( mesh+'.outMesh', vtsToCrv+'.inputMesh' )
        cmds.connectAttr( mesh+'.wm', vtsToCrv+'.inputMeshMatrix' )
        
        for i in range( len( indices ) ):
            cmds.setAttr( vtsToCrv+'.verticeId[%d]' % indices[i], indices[i] )
            cmds.connectAttr( vtsToCrv+'.outputTranslate[%d]' % indices[i], pointToCrv+'.input[%d].inputPoint' % i )
        
        return crv, pointToCrv
    
    mesh, indices = getMeshAndIndices( targetCurve )
    mesh = sgBFunction_dag.getShape( mesh )

    dagPathMesh = sgBFunction_dag.getMDagPath( mesh )
    
    intersector = om.MMeshIntersector()
    intersector.create( dagPathMesh.node() )
    
    meshMtx = dagPathMesh.inclusiveMatrix()
    meshMtxInv = dagPathMesh.inclusiveMatrixInverse()
    fnMesh = om.MFnMesh( dagPathMesh )
    
    pArr = om.MPointArray()
    fnMesh.getPoints( pArr )
    
    targetIndices = []
    pointOnMesh = om.MPointOnMesh()
    for index in indices:
        worldPoint = pArr[ index ] * meshMtx
        mirrorPoint = om.MPoint( -worldPoint.x, worldPoint.y, worldPoint.z )*meshMtxInv
        intersector.getClosestPoint( mirrorPoint, pointOnMesh )
        fIndex = pointOnMesh.faceIndex()
        
        vtxIndices = om.MIntArray()
        fnMesh.getPolygonVertices( fIndex, vtxIndices )
        
        closeDist = 1000000.0
        closeIndex = vtxIndices[0]
        for vtxIndex in vtxIndices:
            point = pArr[ vtxIndex ]
            dist = point.distanceTo( mirrorPoint )
            if dist < closeDist:
                closeDist = dist
                closeIndex = vtxIndex
        
        targetIndices.append( closeIndex )
    
    node = sgBFunction_dag.getNodeFromHistory( targetCurve, 'sgCurveFromPoints' )[0]
    createType = cmds.getAttr( node + '.createType' )
    degrees    = cmds.getAttr( node+'.degrees' )
    
    createdCrv, createdNode = createCurve( mesh, targetIndices )
    cmds.setAttr( createdNode + '.createType', createType )
    cmds.setAttr( createdNode + '.degrees',    degrees )



def createRivetBasedOnSkinWeights( selectedObjs ):
    
    import sgModelMesh
    import sgModelDag
    import sgModelSkinCluster
    import sgModelConvert
    
    def getJointMultMatrix( jnt, mtxBindPre ):
        cons = cmds.listConnections( jnt+'.wm', type='multMatrix' )

        if cons:
            for con in cons:
                if cmds.attributeQuery( 'skinWeightInfluenceMatrix', node=con, ex=1 ):
                    if mtxBindPre == cmds.getAttr( con+'.i[0]' ):
                        return con
        
        mmtxNode = cmds.createNode( 'multMatrix' )
        cmds.setAttr( mmtxNode+'.i[0]', mtxBindPre, type='matrix' )
        cmds.connectAttr( jnt+'.wm', mmtxNode+'.i[1]' )
        
        cmds.addAttr( mmtxNode, ln='skinWeightInfluenceMatrix', at='message' )
        
        return mmtxNode


    mesh, vtxIndices = sgModelMesh.getMeshAndIndicesPoints( selectedObjs )
    
    skinClusterNode = sgModelDag.getNodeFromHistory( mesh, 'skinCluster' )
    if not skinClusterNode: return None
    skinClusterNode = skinClusterNode[0]
    
    influenceAndWeightList, phygicalMap = sgModelSkinCluster.getInfluenceAndWeightList( mesh, vtxIndices )
    
    meshMatrix = sgModelDag.getDagPath( mesh ).inclusiveMatrix()
    meshPoints = sgModelMesh.getLocalPoints( mesh )
    plugMatrix = sgModelSkinCluster.getPlugMatrix( mesh )
    plugBindPre = sgModelSkinCluster.getPlugBindPre( mesh )
    
    BB = om.MBoundingBox()
    
    wtAddMtx = cmds.createNode( 'wtAddMatrix' )
    mtxPlugIndidcesAndWeights = {}
    allWeights = 0.0
    for i in vtxIndices:
        influenceList, weights = influenceAndWeightList[ phygicalMap[i] ]
        
        for j in range( len( influenceList ) ):
            mtxPlugIndex = influenceList[j]
            if mtxPlugIndex in mtxPlugIndidcesAndWeights.keys():
                mtxPlugIndidcesAndWeights[mtxPlugIndex] += weights[j]
            else:
                mtxPlugIndidcesAndWeights.update( {mtxPlugIndex:weights[j]} )
            allWeights += weights[j]
        BB.expand( meshPoints[i] )
    worldPoint = BB.center()*meshMatrix
    
    items = mtxPlugIndidcesAndWeights.items()
    for i in range( len( items ) ):
        influence, weight = items[i]
        
        plugMatrixElement = plugMatrix.elementByLogicalIndex( influence )
        plugBindPreElement = plugBindPre.elementByLogicalIndex( influence )
        
        jnt = cmds.listConnections( plugMatrixElement.name(), s=1, d=0, type='joint' )[0]
        mtxBindPre = cmds.getAttr( plugBindPreElement.name() )
        mmtxNode = getJointMultMatrix( jnt, mtxBindPre )
        cmds.connectAttr( mmtxNode+'.o', wtAddMtx+'.i[%d].m' % i )
        cmds.setAttr( wtAddMtx+'.i[%d].w' % i, weight/allWeights )
    
    origObj = cmds.createNode( 'transform', n='OrigObject' )
    destObj = cmds.createNode( 'transform', n='destObject' )
    cmds.setAttr( destObj+'.dh' , 1 )
    cmds.setAttr( destObj+'.dla', 1 )
    mmNode = cmds.createNode( 'multMatrix' )
    dcmp = cmds.createNode( 'decomposeMatrix' )
    mtxWtAdd = cmds.getAttr( wtAddMtx+'.o' )
    
    cmds.connectAttr( origObj+'.wm', mmNode+'.i[0]' )
    cmds.connectAttr( wtAddMtx+'.o', mmNode+'.i[1]' )
    cmds.connectAttr( destObj+'.pim', mmNode+'.i[2]' )
    
    cmds.connectAttr( mmNode+'.o', dcmp+'.imat' )
    
    cmds.connectAttr( dcmp+'.ot', destObj+'.t' )
    cmds.connectAttr( dcmp+'.or', destObj+'.r' )
    
    mmtxWtAdd = sgModelConvert.convertMatrixToMMatrix( mtxWtAdd )
    worldPoint *= mmtxWtAdd.inverse()
    cmds.setAttr( origObj+'.t', worldPoint.x, worldPoint.y, worldPoint.z )



def createFollicle( trObj, meshObj ):
    
    import sgBFunction_mesh
    import sgBFunction_dag
    
    trObjPos = cmds.xform( trObj, q=1, ws=1, t=1 )
    u, v = sgBFunction_mesh.getUVAtPoint( trObjPos, meshObj )
    
    follicle = cmds.createNode( 'follicle' )
    follicleObj = sgBFunction_dag.getTransform( follicle )
    cmds.connectAttr( follicle+'.ot', follicleObj+'.t' )
    cmds.connectAttr( follicle+'.or', follicleObj+'.r' )
    
    meshShape = sgBFunction_dag.getShape( meshObj )
    cmds.connectAttr( meshShape+'.outMesh', follicle+'.inputMesh' )
    cmds.setAttr( follicle+'.parameterU', u )
    cmds.setAttr( follicle+'.parameterV', v )
    
    return follicleObj




def createClosestFollicle( trObj, meshObj ):
    
    import sgBFunction_mesh
    import sgBFunction_dag
    
    trObjPos = cmds.xform( trObj, q=1, ws=1, t=1 )
    u, v = sgBFunction_mesh.getUVAtPoint( trObjPos, meshObj )
    
    follicle = cmds.createNode( 'follicle' )
    follicleObj = sgBFunction_dag.getTransform( follicle )
    cmds.connectAttr( follicle+'.ot', follicleObj+'.t' )
    cmds.connectAttr( follicle+'.or', follicleObj+'.r' )
    
    meshShape = sgBFunction_dag.getShape( meshObj )
    cmds.connectAttr( meshShape+'.outMesh', follicle+'.inputMesh' )
    cmds.setAttr( follicle+'.parameterU', u )
    cmds.setAttr( follicle+'.parameterV', v )
    
    return follicleObj




def createFollicleFromVertex( vertices ):
    
    import sgCFnc_dag
    import sgBFunction_mesh
    import sgBFunction_dag
    
    cmds.select( vertices )
    
    pathAndComps = sgCFnc_dag.getMDagPathAndComponent()
    
    for mDagPath, mIntArrU, mIntArrV, mIntArrW in pathAndComps:
    
        fnMesh = om.MFnMesh( mDagPath )
        meshShape   = fnMesh.name()
        meshObj= sgBFunction_dag.getTransform( meshShape )
        
        for i in range( len( mIntArrU ) ):
            index = mIntArrU[i]
            pos = cmds.xform( meshShape+'.vtx[%d]' % index, q=1, ws=1, t=1 )
        
            u, v = sgBFunction_mesh.getUVAtPoint( pos, meshObj )
        
            follicle = cmds.createNode( 'follicle' )
            follicleObj = sgBFunction_dag.getTransform( follicle )
            cmds.connectAttr( follicle+'.ot', follicleObj+'.t' )
            cmds.connectAttr( follicle+'.or', follicleObj+'.r' )
            
            cmds.connectAttr( meshShape+'.outMesh', follicle+'.inputMesh' )
            cmds.connectAttr( meshShape+'.wm', follicle+'.inputWorldMatrix' )
            cmds.setAttr( follicle+'.parameterU', u )
            cmds.setAttr( follicle+'.parameterV', v )
            cmds.setAttr( follicleObj+'.inheritsTransform', 0 )




def createRivetOnSurfacePoint( surfacePoint, firstDirection='u' ):
    
    import sgBFunction_dag
    import sgBFunction_attribute
    
    if firstDirection.lower() == 'u':
        fString = 'U'
        sString = 'V'
    else:
        fString = 'V'
        sString = 'U'

    surfaceName, uv = surfacePoint.split( '.uv' )
    
    surfaceName = sgBFunction_dag.getShape( surfaceName )
    
    uvSplits = uv.split( '][' )
    
    uValue = float( uvSplits[0].replace( '[', '' ) )
    vValue = float( uvSplits[1].replace( ']', '' ) )
    
    pointOnSurf = cmds.createNode( 'pointOnSurfaceInfo' )
    vectorNode  = cmds.createNode( 'vectorProduct' )
    fbfNode     = cmds.createNode( 'fourByFourMatrix' )
    mmdcNode    = cmds.createNode( 'multMatrixDecompose' )
    rivetNode   = cmds.createNode( 'transform' )
    
    cmds.setAttr( pointOnSurf+'.u', uValue )
    cmds.setAttr( pointOnSurf+'.v', vValue )
    cmds.setAttr( vectorNode+'.operation', 2 )
    cmds.setAttr( rivetNode+'.dla',1 )
    cmds.setAttr( rivetNode+'.dh', 1 )
    
    cmds.connectAttr( surfaceName +'.worldSpace[0]', pointOnSurf+'.inputSurface' )
    cmds.connectAttr( pointOnSurf+'.tangent%s' % fString, vectorNode+'.input1' )
    cmds.connectAttr( pointOnSurf+'.tangent%s' % sString, vectorNode+'.input2' )
    
    cmds.connectAttr( pointOnSurf+'.tangent%sx' % fString, fbfNode+'.i00' )
    cmds.connectAttr( pointOnSurf+'.tangent%sy' % fString, fbfNode+'.i01' )
    cmds.connectAttr( pointOnSurf+'.tangent%sz' % fString, fbfNode+'.i02' )
    cmds.connectAttr( pointOnSurf+'.tangent%sx' % sString, fbfNode+'.i10' )
    cmds.connectAttr( pointOnSurf+'.tangent%sy' % sString, fbfNode+'.i11' )
    cmds.connectAttr( pointOnSurf+'.tangent%sz' % sString, fbfNode+'.i12' )
    cmds.connectAttr( vectorNode+'.outputX', fbfNode+'.i20' )
    cmds.connectAttr( vectorNode+'.outputY', fbfNode+'.i21' )
    cmds.connectAttr( vectorNode+'.outputZ', fbfNode+'.i22' )
    cmds.connectAttr( pointOnSurf+'.positionX', fbfNode+'.i30' )
    cmds.connectAttr( pointOnSurf+'.positionY', fbfNode+'.i31' )
    cmds.connectAttr( pointOnSurf+'.positionZ', fbfNode+'.i32' )
    
    cmds.connectAttr( fbfNode+'.output', mmdcNode+'.i[0]' )
    cmds.connectAttr( rivetNode+'.pim',  mmdcNode+'.i[1]' )
    cmds.connectAttr( mmdcNode+'.ot',  rivetNode+'.t' )
    cmds.connectAttr( mmdcNode+'.or',  rivetNode+'.r' )
    
    sgBFunction_attribute.addAttr( rivetNode, ln='paramU', min=0, dv=uValue, k=1 )
    sgBFunction_attribute.addAttr( rivetNode, ln='paramV', min=0, dv=vValue, k=1 )
    
    cmds.connectAttr( rivetNode+'.paramU', pointOnSurf+'.u' )
    cmds.connectAttr( rivetNode+'.paramV', pointOnSurf+'.v' )




def createRivetFromVertex( targetVertices, connectMatrix=False ):
    
    import sgBFunction_base
    sgBFunction_base.autoLoadPlugin( 'sgRigAddition' )
    
    def getNodeFromMesh( mesh, isFirst=True ):
    
        import sgBFunction_dag
        
        if cmds.objectType( mesh ) == 'transform':
            mesh = sgBFunction_dag.getShape( mesh )
        
        cons = cmds.listConnections( mesh+'.wm', type='sgMatrixFromVertices' )
        if cons: return cons[0]
        
        node = cmds.createNode( 'sgMatrixFromVertices' )
        cmds.connectAttr( mesh+'.outMesh', node+'.inputMesh' )
        cmds.connectAttr( mesh+'.wm', node+'.inputMeshMatrix' )
        
        return node


    import sgCFnc_dag
    cmds.select( targetVertices )
    
    pathAndComps = sgCFnc_dag.getMDagPathAndComponent()
    
    for mDagPath, mIntArrU, mIntArrV, mIntArrW in pathAndComps:
    
        fnMesh = om.MFnMesh( mDagPath )
        mesh   = fnMesh.name()
        
        node = getNodeFromMesh( mesh )
        
        if connectMatrix:
            for i in range( len( mIntArrU ) ):
                index = mIntArrU[i]
                cmds.setAttr( node+'.verticeId[%d]' % index, index )
                
                tr = cmds.createNode( 'transform', n= mesh+'_vtxPoint_%d' % index )
                mmdc = cmds.createNode( 'multMatrixDecompose' )
                cmds.setAttr( tr+'.dh', 1 )
                cmds.connectAttr( node+'.outputMatrix[%d]' % index, mmdc+'.i[0]' )
                cmds.connectAttr( tr+'.pim', mmdc+'.i[1]' )
                cmds.connectAttr( mmdc+'.ot', tr+'.t' )
        else:
            for i in range( len( mIntArrU ) ):
                index = mIntArrU[i]
                cmds.setAttr( node+'.verticeId[%d]' % index, index )
                
                tr = cmds.createNode( 'transform', n= mesh+'_vtxPoint_%d' % index )
                cmds.setAttr( tr+'.dh', 1 )
                cmds.setAttr( tr+'.inheritsTransform', 0 )
                cmds.connectAttr( node+'.outputTranslate[%d]' % index, tr+'.t' )




def createRivetFromVertex_mirror( rivetObj ):
    
    import sgBFunction_dag
    import sgBFunction_base
    import sgBFunction_convert
    
    sgBFunction_base.autoLoadPlugin( 'sgRigAddition' )
    
    def getNodeFromMesh( mesh, isFirst=True ):
        
        if cmds.objectType( mesh ) == 'transform':
            mesh = sgBFunction_dag.getShape( mesh )
        
        cons = cmds.listConnections( mesh+'.wm', type='sgMatrixFromVertices' )
        if cons: return cons[0]
        
        node = cmds.createNode( 'sgMatrixFromVertices' )
        cmds.connectAttr( mesh+'.outMesh', node+'.inputMesh' )
        cmds.connectAttr( mesh+'.wm', node+'.inputMeshMatrix' )
        
        return node


    cons = cmds.listConnections( rivetObj, s=1, d=0, type='sgMatrixFromVertices', p=1, c=1 )
    if not cons: return None
    
    node, attr = cons[1].split( '.' )
    vtxNum = int( attr.split( '[' )[1].replace( ']', '' ) )
    
    mesh = cmds.listConnections( node, s=1, d=0, type='mesh', shapes=1 )
    if not mesh: return None
    
    mesh = mesh[0]
    
    fnMesh = om.MFnMesh( sgBFunction_dag.getMDagPath( mesh ) )
    intersector = om.MMeshIntersector()
    intersector.create( fnMesh.object() )
    
    pointArr = om.MPointArray()
    fnMesh.getPoints( pointArr )
    pointMirror = om.MPoint( -pointArr[ vtxNum ].x, pointArr[ vtxNum ].y, pointArr[ vtxNum ].z )
    
    pointOnMesh = om.MPointOnMesh()
    intersector.getClosestPoint( pointMirror, pointOnMesh )
    
    faceIndex = pointOnMesh.faceIndex()
    vertices = om.MIntArray()
    fnMesh.getPolygonVertices( faceIndex, vertices )
    
    closeIndex = 0
    closeDist = 1000000.0
    for i in range( vertices.length() ):
        dist = pointArr[ vertices[i] ].distanceTo( pointMirror )
        if closeDist > dist:
            closeDist = dist
            closeIndex = vertices[i]
    
    cmds.setAttr( node+'.verticeId[%d]' % closeIndex, closeIndex )
    
    rivetObjName = rivetObj.split( '|' )[-1]
    rivetObjName = rivetObjName.replace( str( vtxNum ), str( closeIndex ) )
    newObject = cmds.createNode( 'transform', n= sgBFunction_convert.convertSide( rivetObjName ) )
    cmds.setAttr( newObject+'.dh', 1 )
    cmds.setAttr( newObject+'.inheritsTransform', 0 )
    
    cmds.connectAttr( node+'.outputTranslate[%d]' % closeIndex, newObject+'.t' )
        
    
    




def createCurveFromSelPoints():
    
    import sgBFunction_base
    import sgBModel_data
    import sgBFunction_curve
    import sgBFunction_surface
    import sgBFunction_mesh
    import sgBFunction_dag

    sgBFunction_base.autoLoadPlugin( 'sgRigAddition' )
    
    def getPointAttributeFromObject( obj ):
        import sgCFnc_dag
        if obj.find( '.' ) == -1: return None
        cmds.select( obj )
        mDagPath, mIntArrU, mIntArrV, mIntArrW = sgCFnc_dag.getMDagPathAndComponent()[0]
        dagNode = om.MFnDagNode( mDagPath )
        
        if not len( mIntArrU ): return None
        nodeName = dagNode.fullPathName()
        
        if cmds.nodeType( dagNode.fullPathName() ) == 'nurbsCurve':
            curveInfo = sgBFunction_curve.getCurveInfo_worldSpace( nodeName )
            return curveInfo+'.controlPoints[%d]' % mIntArrU[0]
        elif cmds.nodeType( nodeName ) == 'nurbsSurface':
            surfInfo  = sgBFunction_surface.getSurfaceInfo_worldSpace( nodeName )
            spanV = cmds.getAttr( nodeName + '.spansV' )
            degreeV = cmds.getAttr( nodeName + '.degreeV' )
            vLength = spanV + degreeV
            index = mIntArrU[0] * vLength + mIntArrV[0]
            return surfInfo+'.controlPoints[%d]' % index
        elif cmds.nodeType( nodeName ) == 'mesh':
            return sgBFunction_mesh.getPointAttrFromVertex( obj )


    def getMatrixAttributeFromObject( obj ):
        if obj.find( '.' ) != -1: return None
        cmds.select( obj )
        return obj+'.wm'

    import copy
    selObjs = copy.copy( sgBModel_data.orderedObjects )
    
    node  = cmds.createNode( 'sgCurveFromPoints' )
    curve = cmds.createNode( 'nurbsCurve' )
    cmds.connectAttr( node+'.outputCurve', curve+'.create' )
    
    cmds.setAttr( node + '.createType', 1 )
    cmds.setAttr( node + '.degrees', 2 )
    
    for i in range( len( selObjs ) ):
        pointAttr = getPointAttributeFromObject( selObjs[i] )
        mtxAttr   = getMatrixAttributeFromObject( selObjs[i] )

        if pointAttr:
            cmds.connectAttr( pointAttr, node+'.input[%d].inputPoint' % i )
        else:
            cmds.connectAttr( mtxAttr, node+'.input[%d].inputMatrix' % i )
    
    return sgBFunction_dag.getTransform( curve )



def createRivetFromCurves( curves ):
    
    import sgBFunction_dag
    
    loft = cmds.createNode( 'loft' )
    info = cmds.createNode( 'pointOnSurfaceInfo' )
    fbfm = cmds.createNode( 'fourByFourMatrix' )
    mmdc = cmds.createNode( 'multMatrixDecompose' )
    null = cmds.createNode( 'transform' )
    vp   = cmds.createNode( 'vectorProduct' )
    
    surfShape = cmds.createNode( 'nurbsSurface' )
    surfObj   = sgBFunction_dag.getTransform( surfShape )
    
    for i in range( len( curves ) ):
        curve = curves[i]
        shape = sgBFunction_dag.getShape( curve )
        
        srcCons = cmds.listConnections( shape + '.create', p=1, c=1 )
        if not srcCons:
            cmds.connectAttr( shape+'.local', loft+'.inputCurve[%d]' % i )
        else:
            cmds.connectAttr( srcCons[1], loft+'.inputCurve[%d]' % i )
    
    cmds.setAttr( vp+'.operation', 2 )
    cmds.setAttr( info+'.top', 1 )
    cmds.setAttr( info+'.u', 0.5 )
    cmds.setAttr( info+'.v', 0.5 )
    
    cmds.connectAttr( loft + '.outputSurface', info+'.inputSurface' )
    cmds.connectAttr( loft + '.outputSurface', surfShape+'.create' )
    
    cmds.connectAttr( info+'.nnx', fbfm+'.i00' )
    cmds.connectAttr( info+'.nny', fbfm+'.i01' )
    cmds.connectAttr( info+'.nnz', fbfm+'.i02' )
    
    cmds.connectAttr( info+'.nvx', fbfm+'.i10' )
    cmds.connectAttr( info+'.nvy', fbfm+'.i11' )
    cmds.connectAttr( info+'.nvz', fbfm+'.i12' )
    
    cmds.connectAttr( info+'.nnx', vp+'.input1X' )
    cmds.connectAttr( info+'.nny', vp+'.input1Y' )
    cmds.connectAttr( info+'.nnz', vp+'.input1Z' )
    
    cmds.connectAttr( info+'.nvx', vp+'.input2X' )
    cmds.connectAttr( info+'.nvy', vp+'.input2Y' )
    cmds.connectAttr( info+'.nvz', vp+'.input2Z' )
    
    cmds.connectAttr( vp+'.outputX', fbfm+'.i20' )
    cmds.connectAttr( vp+'.outputY', fbfm+'.i21' )
    cmds.connectAttr( vp+'.outputZ', fbfm+'.i22' )
    
    cmds.connectAttr( info+'.px', fbfm+'.i30' )
    cmds.connectAttr( info+'.py', fbfm+'.i31' )
    cmds.connectAttr( info+'.pz', fbfm+'.i32' )
    
    cmds.connectAttr( fbfm+'.output', mmdc+'.i[0]' )
    cmds.connectAttr( null+'.pim',   mmdc+'.i[1]' )
    
    cmds.connectAttr( mmdc+'.ot', null+'.t' )
    cmds.connectAttr( mmdc+'.or', null+'.r' )
    
    cmds.addAttr( null, ln='parameterU', min=0, max=1, dv=0.5 )
    cmds.setAttr( null+'.parameterU', e=1, k=1 )
    cmds.addAttr( null, ln='parameterV', min=0, max=1, dv=0.5 )
    cmds.setAttr( null+'.parameterV', e=1, k=1 )
    
    cmds.connectAttr( null+'.parameterU', info+'.u' )
    cmds.connectAttr( null+'.parameterV', info+'.v' )
    cmds.setAttr( null+'.dh', 1 )
    
    cmds.select( null )
    return null, surfObj



def createFollicleFromSurfacePoint( surfacePoint ):
    
    import sgBFunction_dag
    surfaceNode, noneArrangeStr = surfacePoint.split( '.uv[' )
    uvStrs = noneArrangeStr.replace( ']', '' ).split( '[' )
    
    uv = [ float( uvStrs[0] ), float( uvStrs[1] ) ]
    
    surfaceNode = sgBFunction_dag.getShape( surfaceNode )
    
    minMaxRangeU = cmds.getAttr( surfaceNode+'.minMaxRangeU' )[0]
    minMaxRangeV = cmds.getAttr( surfaceNode+'.minMaxRangeV' )[0]
    
    divRateU = minMaxRangeU[1] - minMaxRangeU[0]
    divRateV = minMaxRangeV[1] - minMaxRangeV[0]
    
    follicleNode = cmds.createNode( 'follicle' )
    cmds.setAttr( follicleNode+'.parameterU', uv[0]/divRateU )
    cmds.setAttr( follicleNode+'.parameterV', uv[1]/divRateV )
    cmds.connectAttr( surfaceNode+'.local', follicleNode+'.inputSurface' )
    cmds.connectAttr( surfaceNode+'.wm', follicleNode+'.inputWorldMatrix' )
    
    follicleObj = sgBFunction_dag.getTransform( follicleNode )
    cmds.setAttr( follicleObj+'.inheritsTransform', 0 )
    cmds.connectAttr( follicleNode+'.outTranslate', follicleObj+'.t' )
    cmds.connectAttr( follicleNode+'.outRotate', follicleObj+'.r' )
    
    return follicleObj



def createClosestPointObjectOnCurve( target, curve, attach=False ):
    
    import sgBFunction_dag
    import sgBFunction_curve
    import sgBFunction_attribute
    
    crvShape = sgBFunction_dag.getShape( curve )
    
    crvMin, crvMax = cmds.getAttr( crvShape + '.minMaxValue' )[0]
    
    tr = cmds.createNode( 'transform' )
    cmds.setAttr( tr + '.dh', 1 )
    
    sgBFunction_attribute.addAttr( tr, ln='param', min=crvMin, max=crvMax, k=1 )
    
    
    if attach:
        nearInfo = cmds.createNode( 'nearestPointOnCurve' )
        dcmp = cmds.createNode( 'decomposeMatrix' )
        cmds.connectAttr( crvShape + '.worldSpace', nearInfo + '.inputCurve' )
        cmds.connectAttr( target + '.wm', dcmp + '.imat' )
        cmds.connectAttr( dcmp + '.ot', nearInfo + '.inPosition' )
        
        vectorProduct = cmds.createNode( 'vectorProduct' )
        cmds.setAttr( vectorProduct + '.operation', 4 )
        
        cmds.connectAttr( nearInfo+'.position', vectorProduct+'.input1' )
        cmds.connectAttr( tr+'.pim', vectorProduct + '.matrix' )
        cmds.connectAttr( vectorProduct + '.output', tr+'.t' )
        
    else:
        pointOnCurve = cmds.createNode( 'pointOnCurveInfo' )
        cmds.connectAttr( crvShape + '.worldSpace', pointOnCurve + '.inputCurve' )    
        vectorProduct = cmds.createNode( 'vectorProduct' )
        cmds.setAttr( vectorProduct + '.operation', 4 )
    
        cmds.connectAttr( pointOnCurve+'.position', vectorProduct+'.input1' )
        cmds.connectAttr( tr+'.pim', vectorProduct + '.matrix' )
        cmds.connectAttr( vectorProduct + '.output', tr+'.t' )
    
        parameter = sgBFunction_curve.getClosestParameter( target, curve )
        cmds.setAttr( tr + '.param', parameter )
        cmds.connectAttr( tr + '.param', pointOnCurve + '.parameter' )
    
    return tr