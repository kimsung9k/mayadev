from sgModules.sgcommands import *
import pymel.core


class AutoFacialRig:
    
    VowelGroupName = 'Vowel_Shapes'
    LipGroupName = 'Lip_Shapes'
    JawGroupName = 'Jaw_Shapes'
    MouthGroupName = 'Mouth_Shapes'
    CheckGroupName = 'Check_Shapes'
    EyeGroupName = 'Eye_Shapes'
    BrowGroupName = 'Brow_Shapes'
    NoseGroupName = 'Nose_Shapes'
    
    def __init__(self, facialGrp, target ):
        
        facialGrp = pymel.core.ls( facialGrp )[0]
        
        facialChildren = facialGrp.listRelatives( c=1, type='transform' )
        
        self.VowelGrp = None
        self.LipGrp   = None
        self.JawGrp   = None
        self.MouthGrp = None
        self.CheckGrp = None
        self.EyeGrp   = None
        self.BrowGrp = None
        self.NoseGrp  = None
        self.target = pymel.core.ls( target )[0]
        
        for facialChild in facialChildren:
            if facialChild == AutoFacialRig.VowelGroupName:
                self.VowelGrp = facialChild
            elif facialChild == AutoFacialRig.LipGroupName:
                self.LipGrp = facialChild
            elif facialChild == AutoFacialRig.JawGroupName:
                self.JawGrp = facialChild
            elif facialChild == AutoFacialRig.MouthGroupName:
                self.MouthGrp = facialChild
            elif facialChild == AutoFacialRig.CheckGroupName:
                self.CheckGrp = facialChild
            elif facialChild == AutoFacialRig.EyeGroupName:
                self.EyeGrp = facialChild
            elif facialChild == AutoFacialRig.BrowGroupName:
                self.BrowGrp = facialChild
            elif facialChild == AutoFacialRig.NoseGroupName:
                self.NoseGrp = facialChild
        
        '''
        print self.VowelGrp
        print self.LipGrp
        print self.JawGrp
        print self.MouthGrp
        print self.CheckGrp
        print self.EyeGrp
        print self.BrowGrp
        print self.NoseGrp
        '''


    def createMouth(self):
        
        if not self.MouthGrp: return None
        
        mouthShapes = self.MouthGrp.listRelatives( c=1, type='transform' )
        
        mouthBlend = pymel.core.blendShape( mouthShapes, self.target, n='bl_' + self.MouthGrp )[0]
        print mouthBlend
        
        


class DeformedJointFromVertices:
    
    def __init__(self):
        
        pass
    
    
    
    def createMatrixCube( self, vtxName ):

        follicle = self.getFollicleFromVertex(vtxName)
        mtxObj, cubeObj = createFourByFourMatrixCube( follicle )
        return mtxObj, cubeObj, follicle
    
    
    def getFollicleFromVertex( self, vtxName ):
        
        vtx = pymel.core.ls( vtxName )[0]
        meshShape = vtx.plugNode()
        meshObj = meshShape.getParent()
        
        if not cmds.attributeQuery( 'follicles', node=meshObj.name(), ex=1 ):
            mAttr = OpenMaya.MFnMessageAttribute()
            mAttr.create( "follicles", "follicles" )
            mAttr.setArray( True )
            oNode = getMObject( meshObj.name() )
            oAttr = mAttr.object()
            dgMod = OpenMaya.MDGModifier()
            dgMod.addAttribute( oNode, oAttr )
            dgMod.doIt()
        
        cons = meshObj.follicles[vtx.index()].listConnections( s=1, d=0 )
        if cons: return cons[0].name()
        
        follicleNode = createFollicleOnVertex( vtxName )
        cmds.connectAttr( follicleNode + '.message', meshObj + '.follicles[%d]' % vtx.index() ) 
        return follicleNode





class AddInfluenceOnlyOneCloseVertex:
    
    def __init__(self):
        
        pass
    
    
    def addInfluceneAndSetWeight(self, jnt, mesh ):
        
        mesh = pymel.core.ls( mesh )[0]
        if mesh.type() == 'mesh':
            meshShape = mesh
        else:
            meshShape = mesh.getShape()
        
        hists = meshShape.history( pdo=1 )
        targetSkinNode = None
        for hist in hists:
            if hist.type() == 'skinCluster':
                targetSkinNode = hist
                break
        if not targetSkinNode: return None
        
        try:cmds.skinCluster( targetSkinNode.name(), e=1, ug=1, dr=4, ps=0, ns=10, lw=True, wt=0, ai=jnt )
        except:pass
        closeIndex = getClosestVertexIndex( cmds.xform( jnt, q=1, ws=1, t=1 )[:3], mesh.name() )
        
        fnNode = OpenMaya.MFnDependencyNode( getMObject( targetSkinNode.name() ) )
        wlPlug = fnNode.findPlug( 'weightList' )[ closeIndex ].child(0)
        
        for i in range( wlPlug.numElements() ):
            cmds.removeMultiInstance( wlPlug[0].name() )
        
        jnt = pymel.core.ls( jnt )[0]
        skinCons = jnt.wm.listConnections( type='skinCluster', p=1 )
        for skinCon in skinCons:
            node = skinCon.node()
            jntIndex = skinCon.index()
            if node.name() != targetSkinNode.name(): continue
            cmds.setAttr( wlPlug.name() + '[%d]' % jntIndex, 1 )
        
    
    
class DuplicateBlendShapeByCtl:
    
    def __init__(self, ctls, srcMesh, dstMesh ):
        
        def getBlendShapeDestConnections( attr ):
            destAttrs = attr.listConnections( s=0, d=1, p=1 )
            compairAttrs = []
            for destAttr in destAttrs:
                if cmds.attributeQuery( 'wm', node=destAttr.node().name(), ex=1 ): continue
                compairAttrs.append( destAttr )
            
            blendConnections = []
            for compairAttr in compairAttrs:
                if compairAttr.node().type() == 'blendShape':
                    blendConnections.append( [attr,compairAttr] )
                else:
                    outputAttrs = compairAttr.node().listAttr( o=1 )
                    for outputAttr in outputAttrs:
                        try:blendConnections += getBlendShapeDestConnections( outputAttr )
                        except:pass
            return blendConnections
        
        def addBlendShape( mesh, targetMesh ):
            hists = targetMesh.history( pdo=1 )
            blendShapeNode = None
            for hist in hists:
                if hist.type() == 'blendShape':
                    blendShapeNode = hist
            if not blendShapeNode:
                blendShapeNode = pymel.core.blendShape( mesh, targetMesh )[0]
                return blendShapeNode.weight[0]
            else:
                currentIndex = blendShapeNode.weight.numElements()
                pymel.core.blendShape( blendShapeNode, e=1, t=[blendShapeNode.getBaseObjects()[0], currentIndex, mesh, 1] )
                return blendShapeNode.weight[currentIndex]  
        
        
        for ctl in ctls:
            attrs = ctl.listAttr( k=1 )
            for attr in attrs:
                if attr.isLocked(): continue
                blendCons = getBlendShapeDestConnections( attr )
                srcAttrNames = []
                for srcAttr, dstAttr in blendCons:
                    if srcAttr.name() in srcAttrNames: continue
                    srcAttrNames.append( srcAttr.name() )
                    srcAttr // dstAttr
                    dstAttr.set( 1 )
                    duMesh = pymel.core.duplicate( srcMesh, n= srcMesh.name() + '_' + attr.attrName() )[0]
                    pymel.core.parent( duMesh, w=1 )
                    srcAttr >> dstAttr
                    print "dest mesh : ", dstMesh
                    blendShapeAttr = addBlendShape( duMesh, dstMesh )
                    print "blend shape attr : ", blendShapeAttr
                    
                    srcAttr >> blendShapeAttr
    



def sortObjsByPosition( objs ):
    def getPointFromObject( obj ):
        point = OpenMaya.MPoint( *cmds.xform( obj, q=1, ws=1, t=1 ) )
        return point
    firstPoint = getPointFromObject( objs[0] )
    secondPoint = getPointFromObject( objs[1] )
    firstVector = secondPoint - firstPoint
 
    sortedObjs = [ objs[0], objs[1] ]
    for i in range( 2, len( objs ) ):
        pointTarget = getPointFromObject( objs[i] )
        inserted = False
        for j in range( len( sortedObjs ) ):
            pointSorted = getPointFromObject( sortedObjs[j] )
            cuVector = pointTarget - pointSorted
            if cuVector * firstVector > 0: continue
            sortedObjs.insert( j, objs[i] )
            inserted = True
            break
        if not inserted: 
            sortedObjs.append( objs[i] )
    return sortedObjs




class FurBall_furOutJntSetting:
    
    def __init__(self):
        
        pass
    
    @staticmethod
    def getDistanceNodeFromTwoObjs( target1, target2 ):
    
        pmTarget1 = pymel.core.ls( target1 )[0]
        pmTarget2 = pymel.core.ls( target2 )[0]
        
        distNode = pymel.core.createNode( 'distanceBetween' )
        pmTarget1.t >> distNode.point1
        pmTarget2.t >> distNode.point2
        
        distNode.addAttr( 'origDist', dv= distNode.distance.get() )
        
        return distNode.name(), 'origDist'
    
    
    @staticmethod
    def createFromEdges( baseTransform, edges  ):
        
        loopCurves = []
        for edge in edges:
            loopCurve = FurBall_furOutJntSetting.createLoopCurve( edge )
            loopCurves.append(loopCurve )
            FurBall_furOutJntSetting.setWorldGeometryToLocalGeometry( loopCurve, baseTransform )
        
        pointsList = []
        for loopCurve in loopCurves:
            points = FurBall_furOutJntSetting.createFourPoints( loopCurve )
            pointsList.append( points )
        centers = []
        for points in pointsList:
            center = FurBall_furOutJntSetting.createCenterPoint( points )
            centers.append( center )
        
        curve = FurBall_furOutJntSetting.createCenterLineCurve( *centers )
        origAttrName, currentAttrName = addCurveDistanceInfo(curve)
        scaleNode = cmds.createNode( 'multiplyDivide' )
        cmds.setAttr( scaleNode + '.op', 2 )
        
        print curve + '.' + currentAttrName
        #print cmds.ls( curve + '.' + currentAttrName )
        
        cmds.connectAttr( curve + '.' + currentAttrName, scaleNode + '.input1X' )
        cmds.connectAttr( curve + '.' + origAttrName, scaleNode + '.input2X' )
        
        jntCenters = [ cmds.createNode( 'joint' ) for i in range( 3 ) ]
        
        for i in range( len(edges) ):
            constrain_point( centers[i], jntCenters[i] )
            tangentNode = cmds.tangentConstraint( curve, jntCenters[i], aim=[0,1,0], u=[1,0,0], wut='vector' )[0]
            upNode1 = pointsList[i][0]
            upNode2 = pointsList[i][2]
            dcmp1 = getDecomposeMatrix( upNode1 )
            dcmp2 = getDecomposeMatrix( upNode2 )
            upVectorNode = cmds.createNode( 'plusMinusAverage' )
            cmds.setAttr( upVectorNode + '.operation', 2 )
            cmds.connectAttr( dcmp1 + '.ot', upVectorNode+'.input3D[0]' )
            cmds.connectAttr( dcmp2 + '.ot', upVectorNode+'.input3D[1]' )
            cmds.connectAttr( upVectorNode + '.output3D', tangentNode + '.worldUpVector' )
            cmds.connectAttr( scaleNode + '.outputX', jntCenters[i] + '.sy' )
            
            distNode1, origAttrName1 = FurBall_furOutJntSetting.getDistanceNodeFromTwoObjs( pointsList[i][0], pointsList[i][2] )
            distNode2, origAttrName2 = FurBall_furOutJntSetting.getDistanceNodeFromTwoObjs( pointsList[i][1], pointsList[i][3] )
        
            scaleXNode = cmds.createNode( 'multiplyDivide' )
            scaleZNode = cmds.createNode( 'multiplyDivide' )
            cmds.setAttr( scaleXNode + '.op', 2 )
            cmds.setAttr( scaleZNode + '.op', 2 )
            cmds.connectAttr( distNode1 + '.distance', scaleXNode + '.input1X' )
            cmds.connectAttr( distNode1 + '.' + origAttrName1, scaleXNode + '.input2X' )
            cmds.connectAttr( distNode2 + '.distance', scaleZNode + '.input1X' )
            cmds.connectAttr( distNode2 + '.' + origAttrName2, scaleZNode + '.input2X' )
            
            cmds.connectAttr( scaleXNode + '.outputX', jntCenters[i] + '.sx' )
            cmds.connectAttr( scaleZNode + '.outputX', jntCenters[i] + '.sz' )
        
        cmds.parent( loopCurves , centers, jntCenters, curve, pointsList[0], pointsList[1], pointsList[2], baseTransform )
    
    
    @staticmethod
    def setWorldGeometryToLocalGeometry( geo, mtxTarget ):
        
        print "%s to %s" %( geo, mtxTarget )
        
        shapes = cmds.listRelatives( geo, c=1, ad=1, type='shape', f=1 )
        
        trs = []
        for shape in shapes:
            transform = cmds.listRelatives( shape, p=1, f=1 )[0]
            trs.append( transform )
        
        trs = list( set( trs ) )
        
        for tr in trs:
            shape = cmds.listRelatives( tr, s=1, f=1 )[0]
            trGeo = cmds.createNode( 'transformGeometry' )
            
            if cmds.nodeType( shape ) == 'nurbsCurve':
                cons = cmds.listConnections( shape + '.create', s=1, d=0, p=1, c=1 )
                if not cons: continue
                cmds.connectAttr( cons[1], trGeo + '.inputGeometry' )
                cmds.connectAttr( trGeo + '.outputGeometry', shape + '.create', f=1 )
                cmds.connectAttr( mtxTarget + '.wim', trGeo + '.transform' )
    
    
    
    @staticmethod
    def createLoopCurve( edge1 ):
        
        cmds.select( edge1 )
        cmds.SelectEdgeLoopSp()
        curve1 = cmds.polyToCurve( form=2, degree=3 )[0]
        return curve1

    
    @staticmethod
    def createFourPoints( curve1 ):
        
        curveShape = cmds.listRelatives( curve1, s=1, f=1 )[0]        
        numPoints = 4
        
        fourPoints = []
        for i in range( numPoints ):
            trNode = cmds.createNode( 'transform' )
            cmds.setAttr( trNode + '.dh', 1 )
            curveInfo = cmds.createNode( 'pointOnCurveInfo' )
            cmds.connectAttr( curveShape + '.local', curveInfo + '.inputCurve' )
            cmds.setAttr( curveInfo + '.top', 1 )
            cmds.setAttr( curveInfo + '.parameter', i / float( numPoints ) )
            cmds.connectAttr( curveInfo + '.position', trNode + '.t' )
            fourPoints.append( trNode )
        return fourPoints

    
    @staticmethod
    def createCenterPoint( trObjects ):
        
        averageNode = cmds.createNode( 'plusMinusAverage' )
        cmds.setAttr( averageNode + '.op', 3 )
        
        centerNode = cmds.createNode( 'transform' )
        cmds.setAttr( centerNode + '.dh', 1 )
        for i in range( len( trObjects ) ):
            cmds.connectAttr( trObjects[i] + '.t', averageNode + '.input3D[%d]' % i )
        cmds.connectAttr( averageNode + '.output3D', centerNode + '.t' )
        return centerNode


    @staticmethod
    def createCenterLineCurve( node1, node2, node3 ):
        
        point1 = OpenMaya.MVector( *cmds.xform( node1, q=1, ws=1, t=1 ) )
        point2 = OpenMaya.MVector( *cmds.xform( node2, q=1, ws=1, t=1 ) )
        point3 = OpenMaya.MVector( *cmds.xform( node3, q=1, ws=1, t=1 ) )
        v1 = point2 - point1
        v2 = point3 - point2
        
        sortedNodes = []
        if v1 * v2 > 0:
            sortedNodes = [ node1, node2, node3 ]
        else:
            if v1.length() < v2.length():
                sortedNodes = [ node3, node1, node2 ]
            else:
                sortedNodes = [ node1, node3, node2 ]
        
        return makeCurveFromSelection( sortedNodes, d=2 )
        
        
        

class SetInfluenceOnlySelJoint:
    
    def __init__(self):
        
        pass
    
    
    def setWeightBySelection( self ):
        
        targets = getMDagPathAndComponent()
        
        jnts = []
        mesh = None

        fnMesh = OpenMaya.MFnMesh()        
        faceCompIndices = OpenMaya.MIntArray()
        for dagPath, compU, compV, compW in targets:
            nodeName = OpenMaya.MFnDagNode( dagPath ).partialPathName()
            if compU:
                mesh = pymel.core.ls( nodeName )[0]
                faceCompIndices = compU
                fnMesh.setObject( dagPath )
            else:
                jnts.append( pymel.core.ls( nodeName )[0] )

        skinNode = None
        for hist in mesh.history( pdo=1 ):
            if hist.type() == 'skinCluster':
                skinNode = hist
                break
        if not skinNode: return None

        influenceIndices = []
        for jnt in jnts:
            cons = jnt.wm.listConnections( type='skinCluster', p=1 )
            for con in cons:
                if skinNode.name() != con.node().name(): continue
                influenceIndices.append( con.index() )

        allVertices = []
        for i in range( faceCompIndices.length() ):
            allVertices.append( faceCompIndices[i] )
            
        allVertices = list( set( allVertices ) )
        
        fnSkinNode = OpenMaya.MFnDependencyNode( getMObject( skinNode.name() ) )
        plugWeightList = fnSkinNode.findPlug( 'weightList' )
        
        for vtxIndex in allVertices:
            plugWeights = plugWeightList[ vtxIndex ].child( 0 )
            
            allWeights = 0
            removeTargets = []
            for i in range( plugWeights.numElements() ):
                if plugWeights[i].logicalIndex() in influenceIndices:
                    allWeights += plugWeights[i].asFloat()
                else:
                    removeTargets.append( plugWeights[i].name() )
            
            for removeTarget in removeTargets:
                cmds.removeMultiInstance( removeTarget )

            for i in range( plugWeights.numElements() ):
                plugName = plugWeights[i].name()
                cuValue = plugWeights[i].asFloat()
                cmds.setAttr( plugName, cuValue / allWeights )
        
        

from sgModules import sgcommands

def makeSmoothSkinedCloneMesh( src, cloneAttrName='_smooth' ):
    
    target = sgcommands.makeCloneObject( src, cloneAttrName = cloneAttrName, shapeOn=True )
    cmds.polySmooth( target,  mth=0 ,sdt=2, ovb=1, ofb=3, ofc=0, ost=1, ocr=0, dv=1, bnr=1, c=1, kb=1, ksb=1, khe=0, kt=1, kmb=1, suv=1, peh=0, sl=1, dpe=1, ps=0.1, ro=1, ch=0 )
    sgcommands.autoCopyWeight( src, target )
    
    srcShape = cmds.listRelatives( src, s=1, f=1 )[0]
    targetShape = cmds.listRelatives( target, s=1, f=1 )[0]
    srcSkinCluster = sgcommands.getNodeFromHistory( src, 'skinCluster')[0]
    targetSkinCluster = sgcommands.getNodeFromHistory( target, 'skinCluster' )[0]
    
    dagPathSrc = sgcommands.getDagPath( srcShape )
    dagPathTrg = sgcommands.getDagPath( targetShape )
    fnMeshSrc    = OpenMaya.MFnMesh( dagPathSrc )
    fnMeshTarget = OpenMaya.MFnMesh( dagPathTrg )
    fnSkinClusterSrc    = OpenMaya.MFnDependencyNode( sgcommands.getMObject( srcSkinCluster ) )
    fnSkinClusterTarget = OpenMaya.MFnDependencyNode( sgcommands.getMObject( targetSkinCluster ) )
    
    numVerticesSrc    = fnMeshSrc.numVertices()
    numVerticesTarget = fnMeshTarget.numVertices()
    
    matrixPlugSrc    = fnSkinClusterSrc.findPlug( 'matrix' )
    matrixPlugTarget = fnSkinClusterTarget.findPlug( 'matrix' )
    weightListPlugSrc    = fnSkinClusterSrc.findPlug( 'weightList' )
    weightListPlugTrg = fnSkinClusterTarget.findPlug( 'weightList' )
    
    dictSrcJointElementIndices = {}
    dictTrgJointElementIndices = {}
    srcJntList = []
    for i in range( matrixPlugSrc.numElements() ):
        srcJnt = cmds.listConnections( matrixPlugSrc[i].name(), s=1, d=0 )[0]
        trgJnt = cmds.listConnections( matrixPlugTarget[i].name(), s=1, d=0 )[0]
        srcJntList.append( srcJnt )
        dictSrcJointElementIndices.update( {srcJnt:matrixPlugSrc[i].logicalIndex()} )
        dictTrgJointElementIndices.update( {trgJnt:matrixPlugTarget[i].logicalIndex()} )
    
    srcToTrgMap = {}
    for i in range( matrixPlugSrc.numElements() ):
        srcIndex = dictSrcJointElementIndices[ srcJntList[i] ]
        trgIndex = dictTrgJointElementIndices[ srcJntList[i] ]
        srcToTrgMap.update( {srcIndex:trgIndex} )
    
    for i in range( weightListPlugSrc.numElements() ):
        weightsPlugSrc = weightListPlugSrc[i].child(0)
        weightsPlugTrg = weightListPlugTrg[i].child(0)
        
        for j in range( weightsPlugTrg.numElements() ):
            cmds.removeMultiInstance( weightsPlugTrg[0].name() )
        
        for j in range( weightsPlugSrc.numElements() ):
            srcMatrixIndex = weightsPlugSrc[j].logicalIndex()
            trgMatrixIndex = srcToTrgMap[ srcMatrixIndex ]
            value = weightsPlugSrc[j].asFloat()
            weightsPlugTrg.elementByLogicalIndex( trgMatrixIndex ).setFloat( value )
    
    itMeshTrg = OpenMaya.MItMeshVertex( dagPathTrg )
    
    util = OpenMaya.MScriptUtil()
    util.createFromInt( 0 )
    prevIndex = util.asIntPtr()
    
    vtxnames = []
    othreVtxNames = []
    for i in range( numVerticesSrc, numVerticesTarget ):
        itMeshTrg.setIndex( i, prevIndex )
        vtxIndices = OpenMaya.MIntArray()
        itMeshTrg.getConnectedVertices( vtxIndices )
        targetIndices = []
        for j in range( vtxIndices.length() ):
            if vtxIndices[j] < numVerticesSrc:
                targetIndices.append( vtxIndices[j] )
        if not targetIndices:
            vtxnames.append( target + '.vtx[%d]' % i )
            continue
        else:
            othreVtxNames.append( target + '.vtx[%d]' % i )
        
        averageMatrixIndices = []
        averageValues = []
        for targetIndex in targetIndices:
            weightsPlug = weightListPlugTrg[targetIndex].child(0)
            for j in range( weightsPlug.numElements() ):
                matrixIndex = weightsPlug[j].logicalIndex()
                value = weightsPlug[j].asFloat()
                if matrixIndex in averageMatrixIndices:
                    index = averageMatrixIndices.index( matrixIndex )
                    averageValues[ index ] += value
                else:
                    averageMatrixIndices.append( matrixIndex )
                    averageValues.append( value )
        
        numInfluence = len( averageMatrixIndices )
        for j in range( numInfluence ):
            averageValues[j] /= len(targetIndices)
        
        weightsPlug = weightListPlugTrg[i].child(0)     
        for j in range( weightsPlug.numElements() ):
            cmds.removeMultiInstance( weightsPlug[0].name() )
        
        for j in range( len(averageMatrixIndices) ):
            averageMatrixIndex = averageMatrixIndices[j]
            averageValue = averageValues[j]
            weightsPlug.elementByLogicalIndex( averageMatrixIndex ).setFloat( averageValue )
        
    cmds.select( vtxnames )
    mel.eval( 'weightHammerVerts;' )
    
    for i in range( numVerticesSrc ):
        vtxnames.append( target + '.vtx[%d]' % i )

    return target, othreVtxNames


def getWeightInfoFromVertex( skinedVtx ):
    
    meshName = skinedVtx.split( '.' )[0]
    vtxId = int( skinedVtx.split( 'vtx[' )[-1].replace( ']', '' ) )
    
    skinNode = getNodeFromHistory( meshName, 'skinCluster' )[0]
    fnSkinNode = OpenMaya.MFnDependencyNode( getMObject( skinNode ) )
    
    plugWeights = fnSkinNode.findPlug( 'weightList' )[vtxId].child(0)
    
    for i in range( plugWeights.numElements() ):
        print cmds.listConnections( skinNode + '.matrix[%d]' % plugWeights[i].logicalIndex(), s=1, d=0, type='joint'), plugWeights[i].asFloat()






            
                
                
                
            
            

