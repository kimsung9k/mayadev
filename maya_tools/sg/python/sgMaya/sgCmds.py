import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import pymel.core
import math, copy
import os
import math
from sgMaya import sgModel


def getIntPtr( intValue = 0 ):
    util = OpenMaya.MScriptUtil()
    util.createFromInt(intValue)
    return util.asIntPtr()




def getDoublePtr( doubleValue=0 ):
    util = OpenMaya.MScriptUtil()
    util.createFromDouble( doubleValue )
    return util.asDoublePtr()



def getDoubleFromDoublePtr( ptr ):
    return OpenMaya.MScriptUtil.getDouble( ptr )



def getInt2Ptr():
    util = OpenMaya.MScriptUtil()
    util.createFromList([0,0],2)
    return util.asInt2Ptr()




def getListFromInt2Ptr( ptr ):
    util = OpenMaya.MScriptUtil()
    v1 = util.getInt2ArrayItem( ptr, 0, 0 )
    v2 = util.getInt2ArrayItem( ptr, 0, 1 )
    return [v1, v2]




def getFloat2Ptr():
    util = OpenMaya.MScriptUtil()
    util.createFromList( [0,0], 2 )
    return util.asFloat2Ptr()



def getMObject( inputTarget ):
    mObject = OpenMaya.MObject()
    selList = OpenMaya.MSelectionList()
    selList.add( pymel.core.ls( inputTarget )[0].name() )
    selList.getDependNode( 0, mObject )
    return mObject



def getDagPath( inputTarget ):
    dagPath = OpenMaya.MDagPath()
    selList = OpenMaya.MSelectionList()
    selList.add( pymel.core.ls( inputTarget )[0].name() )
    try:
        selList.getDagPath( 0, dagPath )
        return dagPath
    except:
        return None




def getDefaultMatrix():
    return [1,0,0,0, 0,1,0,0, 0,0,1,0 ,0,0,0,1]




def listToMatrix( mtxList ):
    if type( mtxList ) == OpenMaya.MMatrix:
        return mtxList
    matrix = OpenMaya.MMatrix()
    OpenMaya.MScriptUtil.createMatrixFromList( mtxList, matrix  )
    return matrix



def matrixToList( matrix ):
    if type( matrix ) == list:
        return matrix
    mtxList = range( 16 )
    for i in range( 4 ):
        for j in range( 4 ):
            mtxList[ i * 4 + j ] = matrix( i, j )
    return mtxList



def getMatrixFromList( mtxList ):
    if type( mtxList ) == OpenMaya.MMatrix:
        return mtxList
    matrix = OpenMaya.MMatrix()
    OpenMaya.MScriptUtil.createMatrixFromList( mtxList, matrix  )
    return matrix



def getListFromMatrix( matrix ):
    if type( matrix ) == list:
        return matrix
    mtxList = range( 16 )
    for i in range( 4 ):
        for j in range( 4 ):
            mtxList[ i * 4 + j ] = matrix( i, j )
    return mtxList



def getSymmetryMatrix( matrix, directionIndex ):
    
    matrixList = getListFromMatrix( matrix )
    
    for i in range( 3 ):
        matrixList[ i*4 + directionIndex+1 ] *= -1
        matrixList[ i*4 + directionIndex+2 ] *= -1
    matrixList[ 3*4 + directionIndex ] *= -1
    
    return getMatrixFromList( matrixList )



def createLocalMatrix( matrixAttr, inverseMatrixAttr ):
    matrixAttr = pymel.core.ls( matrixAttr )[0]
    inverseMatrixAttr = pymel.core.ls( inverseMatrixAttr )[0]
    multMatrixNode = pymel.core.createNode( 'multMatrix' )
    matrixAttr >> multMatrixNode.i[0]
    inverseMatrixAttr >> multMatrixNode.i[1]
    return multMatrixNode




def rotateToMatrix( rotation ):
    
    rotX = math.radians( rotation[0] )
    rotY = math.radians( rotation[1] )
    rotZ = math.radians( rotation[2] )
    
    trMtx = OpenMaya.MTransformationMatrix()
    trMtx.rotateTo( OpenMaya.MEulerRotation( OpenMaya.MVector(rotX, rotY, rotZ) ) )
    return trMtx.asMatrix()



def addAttr( target, **options ):
    
    items = options.items()
    
    attrName = ''
    channelBox = False
    keyable = False
    for key, value in items:
        if key in ['ln', 'longName']:
            attrName = value
        elif key in ['cb', 'channelBox']:
            channelBox = True
            options.pop( key )
        elif key in ['k', 'keyable']:
            keyable = True 
            options.pop( key )
    
    if pymel.core.attributeQuery( attrName, node=target, ex=1 ): return None
    
    pymel.core.addAttr( target, **options )
    
    if channelBox:
        pymel.core.setAttr( target+'.'+attrName, e=1, cb=1 )
    elif keyable:
        pymel.core.setAttr( target+'.'+attrName, e=1, k=1 )



def getLocalMatrix( matrixAttr, inverseMatrixAttr ):
    
    matrixAttr = pymel.core.ls( matrixAttr )[0]
    inverseMatrixAttr = pymel.core.ls( inverseMatrixAttr )[0]
    multMatrixNodes = matrixAttr.listConnections( d=1, s=0, type='multMatrix' )
    for multMatrixNode in multMatrixNodes:
        firstAttr = multMatrixNode.i[0].listConnections( s=1, d=0, p=1 )
        secondAttr = multMatrixNode.i[1].listConnections( s=1, d=0, p=1 )
        thirdConnection = multMatrixNode.i[2].listConnections( s=1, d=0 )
        
        if not firstAttr or not secondAttr or thirdConnection: continue
        
        firstEqual = firstAttr[0] == matrixAttr
        secondEqual = secondAttr[0] == inverseMatrixAttr
        
        if firstEqual and secondEqual:
            pymel.core.select( multMatrixNode )
            return multMatrixNode
    return createLocalMatrix( matrixAttr, inverseMatrixAttr )




def getDecomposeMatrix( matrixAttr ):
    
    matrixAttr = pymel.core.ls( matrixAttr )[0]
    cons = matrixAttr.listConnections( s=0, d=1, type='decomposeMatrix' )
    if cons: 
        pymel.core.select( cons[0] )
        return cons[0]
    decomposeMatrix = pymel.core.createNode( 'decomposeMatrix' )
    matrixAttr >> decomposeMatrix.imat
    return decomposeMatrix



def getLocalDecomposeMatrix( matrixAttr, matrixAttrInv ):
    return getDecomposeMatrix( getLocalMatrix( matrixAttr, matrixAttrInv ).matrixSum )



def makeChild( target, typ='null', **options ):
    
    if typ == 'joint':
        childObject = pymel.core.createNode( 'joint',**options )
    elif typ == 'locator':
        childObject = pymel.core.spaceLocator( **options )
    else:
        childObject = pymel.core.createNode( 'transform', **options )
    
    target = pymel.core.ls( target )[0]
    childObject.setParent( target )
    childObject.setMatrix( getDefaultMatrix() )
    return childObject


def printMatrix( inputMatrix ):
    
    mtxValue = getMatrixFromList( inputMatrix )
    for i in range( 4 ):
        print "%5.3f, %5.3f, %5.3f, %5.3f" %( mtxValue(i,0), mtxValue(i,1), mtxValue(i,2), mtxValue(i,3) )
    print




def editShapeByMatrix( inputShapeNode, inputMatrix ):
    shapeNode = pymel.core.ls( inputShapeNode )[0]
    if shapeNode.nodeType() == 'nurbsCurve':
        components = pymel.core.ls( shapeNode + '.cv[*]', fl=1 )
    elif shapeNode.nodeType() == 'mesh':
        components = pymel.core.ls( shapeNode + '.vtx[*]', fl=1 )
    
    matrix = getMatrixFromList( inputMatrix )
    
    for component in components:
        cuPos = pymel.core.xform( component, q=1, os=1, t=1 )
        afterPos = OpenMaya.MPoint( *cuPos ) * matrix
        pymel.core.move( afterPos[0], afterPos[1], afterPos[2], component, os=1 )
    



def separateParentConnection( node, attrName ):
    
    if not type( node ) in [ str, unicode ]:
        node = node.name()
    parentAttr = cmds.attributeQuery( attrName, node=node, listParent=1 )
    
    if parentAttr:
        cons = cmds.listConnections( node+'.'+parentAttr[0], s=1, d=0, p=1, c=1 )
        if cons:
            srcAttr = cons[1]
            srcNode, srcParentAttr = srcAttr.split( '.' )
            if cmds.nodeType( srcNode ) == 'unitConversion':
                origCons = cmds.listConnections( srcNode + '.input', s=1, d=0, p=1, c=1 )
                origSrcNode, origSrcParentAttr = origCons[1].split( '.' )
                srcAttrs = cmds.attributeQuery( origSrcParentAttr, node=origSrcNode, listChildren=1 )
                srcNode = origSrcNode
            else:
                srcAttrs = cmds.attributeQuery( srcParentAttr, node=srcNode, listChildren=1 )
            dstAttrs = cmds.attributeQuery( parentAttr[0], node=node,    listChildren=1 )
            for i in range( len( srcAttrs ) ):
                if cmds.connectAttr( srcNode+'.'+srcAttrs[i], node+'.'+dstAttrs[i] ): continue
                cmds.connectAttr( srcNode+'.'+srcAttrs[i], node+'.'+dstAttrs[i], f=1 )
            cmds.disconnectAttr( cons[1], cons[0] )




def convertMultDoubleConnection( inputAttr ):
    
    attr = pymel.core.ls( inputAttr )[0]
    attrName = attr.shortName()
    newAttrName = 'mult_' + attrName
    node = attr.node()
    
    if not attr.isChild() and attr.numChildren() == 3:
        attrs = []
        for child in attr.children():
            attr = convertMultDoubleConnection( child )
            attrs.append( attr )
        return attrs
    else:
        addAttr( node, ln=newAttrName, cb=1, dv=1 )
        
        multDouble = cmds.createNode( 'multDoubleLinear' )
        separateParentConnection( node, attrName )

        cons = attr.listConnections( s=1, d=0, p=1, c=1 )
        if not cons: return None
        cmds.connectAttr( cons[0][1].name(), multDouble+'.input1' )
        cmds.connectAttr( node+'.'+newAttrName, multDouble + '.input2' )
        cmds.connectAttr( multDouble + '.output', node+'.'+attrName, f=1 )
        return node.attr( newAttrName )
    




def addOptionAttribute( inputTarget, enumName = "Options" ):
    
    target = pymel.core.ls( inputTarget )[0]
    
    barString = '____'
    while pymel.core.attributeQuery( barString, node=target, ex=1 ):
        barString += '_'
    
    target.addAttr( barString,  at="enum", en="%s:" % enumName )
    target.attr( barString ).set( e=1, cb=1 )





def copyAttribute( inputSrc, inputDst, attrName ):
    
    src = pymel.core.ls( inputSrc )[0]
    dst = pymel.core.ls( inputDst )[0]
    
    srcAttr = src.attr( attrName )
    defaultList = pymel.core.attributeQuery( attrName, node=src, ld=1 )
    
    try:
        if srcAttr.type() == 'enum':
            enumNames = pymel.core.attributeQuery( attrName, node=inputSrc, le=1 )
            enumStr = ':'.join( enumNames ) + ':'
            addAttr( dst, ln= srcAttr.longName(), sn= srcAttr.shortName(), at=srcAttr.type(), en=enumStr, dv=defaultList[0] )
        else:
            addAttr( dst, ln= srcAttr.longName(), sn= srcAttr.shortName(), at=srcAttr.type(), dv=defaultList[0] )
    except:
        try:
            addAttr( dst, ln= srcAttr.longName(), sn= srcAttr.shortName(), dt=srcAttr.type(), dv=defaultList[0] )
        except:
            pass

    dstAttr = dst.attr( attrName )
    if srcAttr.isnumeric():
        dstAttr.setRange( srcAttr.getRange() )
    if srcAttr.isInChannelBox():
        dstAttr.showInChannelBox(True)
    if srcAttr.isKeyable():
        dstAttr.setKeyable(True)
    
    try:dstAttr.set( srcAttr.get() )
    except:pass




def replaceObject( inputSrc, inputDst ):
    
    src = pymel.core.ls( inputSrc )[0]
    dst = pymel.core.ls( inputDst )[0]
    
    attrs = src.listAttr( ud=1 )
    for attr in attrs:
        copyAttribute( src, dst, attr.longName() )
    
    srcCons = src.listConnections( s=1, d=0, p=1, c=1 )
    dstCons = src.listConnections( s=0, d=1, p=1, c=1 )
    
    dst.setParent( src.getParent() )
    
    for origCon, srcCon in srcCons:
        srcCon >> dst.attr( origCon.attrName() )
    for origCon, dstCon in dstCons:
        dst.attr( origCon.attrName() ) >> dstCon
    
    children = src.listRelatives( c=1, type='transform' )
    for child in children:
        child.setParent( dst )
    return dst




def makeCurveFromObjects( *sels, **options ):
    
    sels = list( sels )
    for i in range( len( sels ) ):
        print sels[i]
        sels[i] = pymel.core.ls( sels[i] )[0]

    poses = []
    for sel in sels:
        pose = pymel.core.xform( sel, q=1, ws=1, t=1 )[:3]
        poses.append( pose )
    curve = pymel.core.ls( cmds.curve( p=poses, **options ) )[0]
    curveShape = curve.getShape()
    
    for i in range( len( sels ) ):
        dcmp = pymel.core.createNode( 'decomposeMatrix' )
        vp   = pymel.core.createNode( 'vectorProduct' ); vp.setAttr( 'op', 4 )
        sels[i].wm >> dcmp.imat
        dcmp.ot >> vp.input1
        curve.wim >> vp.matrix
        vp.output >> curveShape.controlPoints[i]
    
    return curve



def createPointOnCurve( inputCurve, numPoints, **options ):

    eachParamValue = 1.0
    if numPoints == 1:
        addParamValue = 0.5
    else:
        addParamValue = 0.0
        eachParamValue = 1.0/(numPoints-1)
    
    curve = pymel.core.ls( inputCurve )[0]
    curveShape = curve.getShape()

    nodeType = 'transform'
    if options.has_key( 'nodeType' ):
        nodeType = options['nodeType']
    vector = None
    if options.has_key( 'vector' ):
        vector = options['vector']
    
    returnObjs = []
    for i in range( numPoints ):
        curveInfo = cmds.createNode( 'pointOnCurveInfo' )
        cmds.connectAttr( curveShape + '.worldSpace', curveInfo+'.inputCurve' )
        cmds.setAttr( curveInfo + '.top', 1 )
        trNode = cmds.createNode( nodeType )
        cmds.addAttr( trNode, ln='param', min=0, max=100, dv=(eachParamValue * i + addParamValue)*100 )
        cmds.setAttr( trNode + '.param', e=1, k=1 )
        if cmds.nodeType( trNode ) == 'transform':
            cmds.setAttr( trNode + '.dh', 1 )
        compose = cmds.createNode( 'composeMatrix' )
        multMtx = cmds.createNode( 'multMatrix' )
        dcmp = cmds.createNode( 'decomposeMatrix' )
        cmds.connectAttr( curveInfo + '.position', compose + '.it' )
        cmds.connectAttr( compose + '.outputMatrix', multMtx + '.i[0]' )
        cmds.connectAttr( trNode + '.pim', multMtx + '.i[1]' )
        cmds.connectAttr( multMtx + '.o', dcmp + '.imat' )
        cmds.connectAttr( dcmp + '.ot', trNode + '.t' )
        multDouble = cmds.createNode( 'multDoubleLinear' )
        cmds.setAttr( multDouble + '.input2', 0.01 )
        cmds.connectAttr( trNode + '.param', multDouble + '.input1' )
        cmds.connectAttr( multDouble + '.output', curveInfo + '.parameter' )
        
        if vector:
            curveInfo = pymel.core.ls( curveInfo )[0]
            angleNode = pymel.core.createNode( 'angleBetween' )
            vectorNode = pymel.core.createNode( 'vectorProduct' )
            trNode = pymel.core.ls( trNode )[0]
            vectorNode.operation.set(3)
            valueX = vector[0]
            valueY = vector[1]
            valueZ = vector[2]
            angleNode.vector1X.set( valueX )
            angleNode.vector1Y.set( valueY )
            angleNode.vector1Z.set( valueZ )
            curveInfo.tangent >> vectorNode.input1
            trNode.pim >> vectorNode.matrix
            vectorNode.output >> angleNode.vector2
            angleNode.euler >> trNode.r
        returnObjs.append( pymel.core.ls( trNode )[0] )

    return returnObjs



def getOrderedEdgeRings( inputTargetEdge ):
    
    targetEdge = pymel.core.ls( inputTargetEdge )[0].name()
    
    cmds.select( targetEdge )
    cmds.SelectEdgeRingSp()
    ringEdges = [ edge.name() for edge in pymel.core.ls( sl=1, fl=1 ) ]
    oppasitEdges = []
    
    meshName = targetEdge.split( '.' )[0]
    dagPathMesh = getDagPath( meshName )
    itEdgeMesh = OpenMaya.MItMeshEdge( dagPathMesh )
    itPolygon  = OpenMaya.MItMeshPolygon( dagPathMesh )
    
    util = OpenMaya.MScriptUtil()
    util.createFromInt( 0 )
    prevIndex = util.asIntPtr()
    
    startEdgeIndex = None
    for edge in ringEdges:
        edgeIndex = int( edge.split( '[' )[-1].replace( ']', '' ) )
        itEdgeMesh.setIndex( edgeIndex, prevIndex )
        connectedFaces = OpenMaya.MIntArray()
        connectedEdges = OpenMaya.MIntArray()
        itEdgeMesh.getConnectedFaces( connectedFaces )
        itEdgeMesh.getConnectedEdges( connectedEdges )
        
        resultEdgeIndices = []
        for i in range( connectedFaces.length() ):
            edgesFromFace = OpenMaya.MIntArray()
            itPolygon.setIndex( connectedFaces[i], prevIndex )
            itPolygon.getEdges( edgesFromFace )
            for j in range( edgesFromFace.length() ):
                if edgesFromFace[j] == edgeIndex: continue
                exists = False
                for k in range( connectedEdges.length() ):
                    if edgesFromFace[j] == connectedEdges[k]: 
                        exists=True
                        break
                if exists: continue
                resultEdgeIndices.append( edgesFromFace[j] )
        if len( resultEdgeIndices ) == 1:
            startEdgeIndex = edgeIndex
            break

    maxLoopNum = 1000
    loopIndex = 0
    
    orderedEdgeIndices = [ startEdgeIndex ]
    currentIndex = startEdgeIndex
    while True:
        itEdgeMesh.setIndex( currentIndex, prevIndex )
        connectedFaces = OpenMaya.MIntArray()
        connectedEdges = OpenMaya.MIntArray()
        itEdgeMesh.getConnectedFaces( connectedFaces )
        itEdgeMesh.getConnectedEdges( connectedEdges )
        
        resultEdgeIndices = []
        for i in range( connectedFaces.length() ):
            edgesFromFace = OpenMaya.MIntArray()
            itPolygon.setIndex( connectedFaces[i], prevIndex )
            itPolygon.getEdges( edgesFromFace )
            for j in range( edgesFromFace.length() ):
                if edgesFromFace[j] == edgeIndex: continue
                exists = False
                for k in range( connectedEdges.length() ):
                    if edgesFromFace[j] == connectedEdges[k]: 
                        exists=True
                        break
                if exists: continue
                resultEdgeIndices.append( edgesFromFace[j] )
                
        nextEdgeIndex = None
        for resultEdgeIndex in resultEdgeIndices:
            if resultEdgeIndex in orderedEdgeIndices: continue
            nextEdgeIndex = resultEdgeIndex
            break
        if not nextEdgeIndex: break
        currentIndex = nextEdgeIndex
        orderedEdgeIndices.append( nextEdgeIndex )
        
        loopIndex+=1
        if loopIndex > maxLoopNum: break

    return [ meshName + '.e[%d]' % i for i in orderedEdgeIndices ]




def getNumVertices( inputNode ):
    
    node = pymel.core.ls( inputNode )[0]
    nodeShape = None
    if node.type() == 'transform':
        nodeShape = node.getShape()
    else:
        nodeShape = node
    if not nodeShape: return 0
    dagPath = getDagPath( nodeShape )
    fnMesh = OpenMaya.MFnMesh( dagPath )
    return fnMesh.numVertices()




def getCurrentVisibleShapes( inputTarget ):
    
    target = pymel.core.ls( inputTarget )[0]
    shapes = target.listRelatives( s=1 )
    return [ shape for shape in shapes if not shape.io.get() ]




def getShadingEngines( inputTarget ):
    
    target = pymel.core.ls( inputTarget )[0]
    if target.nodeType() == 'transform':
        shape = getCurrentVisibleShapes( inputTarget )[0]
    else:
        shape = target
    return shape.listConnections( s=0, d=1, type='shadingEngine' )




def copyShader( inputFirst, inputSecond ):
    first = pymel.core.ls( inputFirst )[0]
    second = pymel.core.ls( inputSecond )[0]
    if not pymel.core.objExists( first ): return None
    if not pymel.core.objExists( second ): return None
    
    try:firstShape = first.getShape()
    except:firstShape = first
    try:secondShape = second.getShape()
    except:secondShape = second
    engines = firstShape.listConnections( type='shadingEngine' )
    if not engines: return None
    
    engines = list( set( engines ) )
    
    copyObjAndEngines = []
    for engine in engines:
        shaders = engine.surfaceShader.listConnections( s=1, d=0 )
        if not shaders: continue
        shader = shaders[0]
        pymel.core.hyperShade( objects = shader )
        selObjs = pymel.core.ls( sl=1 )
        
        targetObjs = []
        for selObj in selObjs:
            if selObj.find( '.' ) != -1:
                if selObj.node() == firstShape:
                    targetObjs.append( second+'.'+ selObj.split( '.' )[-1] )
            elif selObj.name() == firstShape.name():
                targetObjs.append( secondShape.name() )

        if not targetObjs: continue
        for targetObj in targetObjs:
            cmds.sets( targetObj, e=1, forceElement=engine.name() )
            copyObjAndEngines.append( [targetObj, engine.name()] )
    return copyObjAndEngines
    


def getTranslateFromMatrix( mtxValue ):
    
    if type( mtxValue ) != list:
        mtxList = matrixToList( mtxValue )
    else:
        mtxList = mtxValue
    
    return mtxList[12:-1]



def getRotateFromMatrix( mtxValue ):
    
    if type( mtxValue ) == list:
        mtxValue = listToMatrix( mtxValue )
    
    trMtx = OpenMaya.MTransformationMatrix( mtxValue )
    rotVector = trMtx.eulerRotation().asVector()
    
    return [math.degrees(rotVector.x), math.degrees(rotVector.y), math.degrees(rotVector.z)]


    
def freezeJoint( inputJnt ):
    
    jnt = pymel.core.ls( inputJnt )[0]
    jntChildren = jnt.listRelatives( c=1, ad=1, type='joint' )
    if not jntChildren: jntChildren = []
    jntChildren.append( jnt )
    
    for jnt in jntChildren:
        mtxJnt = pymel.core.xform( jnt, q=1, os=1, matrix=1 )
        rotValue = getRotateFromMatrix( mtxJnt )
        jnt.jo.set( rotValue )
        jnt.r.set( 0,0,0 )
        jnt.rotateAxis.set( 0,0,0 )



def blendTwoMatrixConnect( inputFirst, inputSecond, inputThird, **options ):
    
    connectTrans = True
    connectRotate = True
    
    if options.has_key( 'ct' ):
        connectTrans = options['ct']
    if options.has_key( 'cr' ):
        connectRotate = options['cr']
    
    first  = pymel.core.ls( inputFirst )[0]
    second = pymel.core.ls( inputSecond )[0]
    third  = pymel.core.ls( inputThird )[0]
    
    third.addAttr( 'blend', min=0, max=1, k=1, dv=0.5 )
    
    wtAddMtx = pymel.core.createNode( 'wtAddMatrix' )
    multMtx = pymel.core.createNode( 'multMatrix' )
    dcmp = pymel.core.createNode( 'decomposeMatrix' )
    revNode = pymel.core.createNode( 'reverse' )
    third.blend >> revNode.inputX
    
    first.wm >> wtAddMtx.i[0].m
    second.wm >> wtAddMtx.i[1].m
    revNode.outputX >> wtAddMtx.i[0].w
    third.blend >> wtAddMtx.i[1].w
    
    wtAddMtx.matrixSum >> multMtx.i[0]
    third.pim >> multMtx.i[1]
    
    multMtx.matrixSum >> dcmp.imat
    
    if connectTrans:
        dcmp.ot >> third.t
    if connectRotate:
        dcmp.outputRotate >> third.r



    
def addMiddleTranslateJoint( inputJnt, **options ):
    
    jnt = pymel.core.ls(inputJnt)[0]
    pJnt = jnt.getParent()
    
    pymel.core.select( pJnt )
    try:
        radiusValue = pymel.core.getAttr( pJnt + '.radius' ) * 1.5
    except:
        radiusValue = 1
    
    options.update( {'radius':radiusValue})
    newJnt = pymel.core.joint( **options )
    newJnt.addAttr( 'transMult', dv=0.5, k=1 )
    
    multNode = pymel.core.createNode( 'multiplyDivide' )
    cmds.connectAttr( jnt + '.t', multNode + '.input1' )
    cmds.connectAttr( newJnt + '.transMult', multNode + '.input2X' )
    cmds.connectAttr( newJnt + '.transMult', multNode + '.input2Y' )
    cmds.connectAttr( newJnt + '.transMult', multNode + '.input2Z' )
    cmds.connectAttr( multNode + '.output', newJnt + '.t' )
    return newJnt
    
    

def addMiddleJoint( inputJnt, **options ):
    
    jnt = pymel.core.ls( inputJnt )[0].name()
    jntC = cmds.listRelatives( jnt, c=1, f=1 )[0]
    middleTransJnt = addMiddleTranslateJoint( jntC, **options ).name()
    cmds.setAttr( middleTransJnt + '.transMult', 0 )
    
    compose = cmds.createNode( 'composeMatrix' )
    inverse = cmds.createNode( 'inverseMatrix' )
    addMtx = cmds.createNode( 'addMatrix' )
    dcmp = cmds.createNode( 'decomposeMatrix' )
    
    cmds.connectAttr( jnt + '.matrix', inverse+ '.inputMatrix' )
    cmds.connectAttr( compose + '.outputMatrix', addMtx + '.matrixIn[0]' )
    cmds.connectAttr( inverse + '.outputMatrix', addMtx + '.matrixIn[1]' )
    cmds.connectAttr( addMtx + '.matrixSum', dcmp + '.imat' )
    
    cmds.connectAttr( dcmp + '.or', middleTransJnt + '.r' )
    
    cmds.setAttr( middleTransJnt + '.radius', cmds.getAttr( jnt + '.radius' ) * 1.5 )
    return pymel.core.ls( middleTransJnt )[0]




def getConstrainMatrix( inputFirst, inputTarget ):
    first = pymel.core.ls( inputFirst )[0]
    target = pymel.core.ls( inputTarget )[0]
    mm = pymel.core.createNode( 'multMatrix' )
    first.wm >> mm.i[0]
    target.pim >> mm.i[1]
    return mm



def constrain_point( first, target ):
    
    mm = getConstrainMatrix( first, target )
    dcmp = getDecomposeMatrix( mm.matrixSum )
    cmds.connectAttr( dcmp + '.ot', target + '.t', f=1 )



def constrain_rotate( first, target ):
    
    mm = getConstrainMatrix( first, target )
    dcmp = getDecomposeMatrix( mm.matrixSum )
    cmds.connectAttr( dcmp + '.or', target + '.r', f=1 )



def constrain_scale( first, target ):
    
    mm = getConstrainMatrix( first, target )
    dcmp = getDecomposeMatrix( mm )
    cmds.connectAttr( dcmp + '.os', target + '.s', f=1 )




def constrain_parent( first, target ):
    
    mm = getConstrainMatrix( first, target )
    dcmp = getDecomposeMatrix( mm.matrixSum )
    cmds.connectAttr( dcmp + '.ot',  target + '.t', f=1 )
    cmds.connectAttr( dcmp + '.or',  target + '.r', f=1 )


def constrain_all( first, target ):
    
    mm = getConstrainMatrix( first, target )
    dcmp = getDecomposeMatrix( mm.matrixSum )
    cmds.connectAttr( dcmp + '.ot',  target + '.t', f=1 )
    cmds.connectAttr( dcmp + '.or',  target + '.r', f=1 )
    cmds.connectAttr( dcmp + '.os',  target + '.s', f=1 )
    cmds.connectAttr( dcmp + '.osh',  target + '.sh', f=1 )



def makeParent( inputSel, **options ):
    
    sel = pymel.core.ls( inputSel )[0]
    if not options.has_key( 'n' ) and not options.has_key( 'name' ):
        options.update( {'n':'P'+ sel.shortName()} )
    selP = sel.getParent()
    transform = pymel.core.createNode( 'transform', **options )
    if selP: pymel.core.parent( transform, selP )
    pymel.core.xform( transform, ws=1, matrix= sel.wm.get() )
    pymel.core.parent( sel, transform )
    pymel.core.xform( sel, os=1, matrix= getDefaultMatrix() )
    return transform




def addMultDoubleLinearConnection( inputAttr ):
    
    fullAttr = pymel.core.ls( inputAttr )[0]
    newAttrName = 'mult_' + fullAttr.attrName()
    
    node = pymel.core.ls( fullAttr.node() )[0]
    separateParentConnection( node, fullAttr.attrName() )
    
    addAttr( node, ln=newAttrName, cb=1, dv=1 )
    multDouble = pymel.core.createNode( 'multDoubleLinear' )
    
    cons = cmds.listConnections( node + '.' + fullAttr.attrName(), s=1, d=0, p=1, c=1 )
    if not cons: return None
    cmds.connectAttr( cons[1], multDouble+'.input1' )
    cmds.connectAttr( node+'.'+newAttrName, multDouble + '.input2' )
    cmds.connectAttr( multDouble + '.output', node+'.'+fullAttr.attrName(), f=1 )
    return pymel.core.ls( node.attr( newAttrName ) )[0]



def addAnimCurveConnection( inputAttr ):
    
    fullAttr = pymel.core.ls( inputAttr )[0]
    node = fullAttr.node()
    attr = fullAttr.attrName()
    separateParentConnection( node, attr )
          
    cons = cmds.listConnections( node+'.'+attr, s=1, d=0, p=1, c=1 )
    if not cons: return None
    if cmds.nodeType( cons[1].split( '.' )[0] ) == 'unitConversion':
        srcCon = cmds.listConnections( cons[1].split( '.' )[0], s=1, d=0, p=1 )
        if srcCon:
            cons[1] = srcCon[0]
    
    attrType = cmds.attributeQuery( attr, node= node, attributeType=1 )
    
    if attrType == 'doubleLinear':
        animCurveType= 'animCurveUL'
    elif attrType == 'doubleAngle':
        animCurveType = 'animCurveUA'
    else:
        animCurveType = 'animCurveUU'
    
    animCurve = pymel.core.createNode( animCurveType )
    cmds.connectAttr( cons[1], animCurve+'.input' )
    cmds.connectAttr( animCurve+'.output', cons[0], f=1 )
    
    cmds.setKeyframe( animCurve, f= -1, v= -1 )
    cmds.setKeyframe( animCurve, f=  0, v=  0 )
    cmds.setKeyframe( animCurve, f=  1, v=  1 )
    
    cmds.setAttr( animCurve + ".postInfinity", 1 )
    cmds.setAttr( animCurve + ".preInfinity", 1 )
    
    pymel.core.selectKey( animCurve )
    cmds.keyTangent( itt='spline', ott='spline' )
    return animCurve



def copyShapeToTransform( inputShape, inputTransform ):
    
    shape = pymel.core.ls( inputShape )[0]
    transform = pymel.core.ls( inputTransform )[0]
    
    oTarget = getMObject( transform )
    if shape.type() == 'mesh':
        oMesh = getMObject( shape )
        fnMesh = OpenMaya.MFnMesh( oMesh )
        fnMesh.copy( oMesh, oTarget )
    elif shape.type() == 'nurbsCurve':
        oCurve = getMObject( shape )
        fnCurve = OpenMaya.MFnNurbsCurve( oCurve )
        fnCurve.copy( oCurve, oTarget )
    elif shape.type() == 'nurbsSurface':
        oSurface = getMObject( shape )
        fnSurface = OpenMaya.MFnNurbsSurface( oSurface )
        fnSurface.copy( oSurface, oTarget )



def addIOShape( inputShape ):
    
    shape = pymel.core.ls( inputShape )[0]
    
    if shape.type() == 'transform':
        targetShape = shape.getShape()
    else:
        targetShape = shape
    
    targetTr    = targetShape.getParent()
    newShapeTr = pymel.core.createNode( 'transform' )
    copyShapeToTransform( targetShape, newShapeTr )
    ioShape = newShapeTr.getShape()
    ioShape.attr( 'io' ).set( 1 )
    pymel.core.parent( ioShape, targetTr, add=1, shape=1 )
    pymel.core.delete( newShapeTr )
    return targetTr.listRelatives( s=1 )[-1]



def makeController( pointList, defaultScaleMult = 1, **options ):
    
    newPointList = copy.deepcopy( pointList )
    
    options.update( {'p':newPointList, 'd':1} )
    
    typ = 'transform'
    if options.has_key( 'typ' ):
        typ = options.pop( 'typ' )
    
    mp = False
    if options.has_key( 'makeParent' ):
        mp = options.pop('makeParent')
    
    colorIndex = -1
    if options.has_key( 'colorIndex' ):
        colorIndex = options.pop('colorIndex')
    
    crv = pymel.core.curve( **options )
    crvShape = crv.getShape()
    
    if options.has_key( 'n' ):
        name = options['n']
    elif options.has_key( 'name' ):
        name = options['name']
    else:
        name = None
    
    jnt = pymel.core.ls( cmds.createNode( typ ) )[0]
    pJnt = None
    
    if mp:
        pJnt = pymel.core.ls( makeParent( jnt ) )[0]
    
    if name:
        jnt.rename( name )
        if pJnt:
            pJnt.rename( 'P' + name )

    pymel.core.parent( crvShape, jnt, add=1, shape=1 )
    pymel.core.delete( crv )
    crvShape = jnt.getShape()
    
    ioShape = addIOShape( jnt )
    ioShape = pymel.core.ls( ioShape )[0]
    
    jnt.addAttr( 'shape_tx', dv=0 ); jnt.shape_tx.set( e=1, cb=1 )
    jnt.addAttr( 'shape_ty', dv=0); jnt.shape_ty.set( e=1, cb=1 )
    jnt.addAttr( 'shape_tz', dv=0); jnt.shape_tz.set( e=1, cb=1 )
    jnt.addAttr( 'shape_rx', dv=0, at='doubleAngle' ); jnt.shape_rx.set( e=1, cb=1 )
    jnt.addAttr( 'shape_ry', dv=0, at='doubleAngle' ); jnt.shape_ry.set( e=1, cb=1 )
    jnt.addAttr( 'shape_rz', dv=0, at='doubleAngle' ); jnt.shape_rz.set( e=1, cb=1 )
    jnt.addAttr( 'shape_sx', dv=1 ); jnt.shape_sx.set( e=1, cb=1 )
    jnt.addAttr( 'shape_sy', dv=1 ); jnt.shape_sy.set( e=1, cb=1 )
    jnt.addAttr( 'shape_sz', dv=1 ); jnt.shape_sz.set( e=1, cb=1 )
    jnt.addAttr( 'scaleMult', dv=defaultScaleMult, min=0 ); jnt.scaleMult.set( e=1, cb=1 )
    composeMatrix = pymel.core.createNode( 'composeMatrix' )
    composeMatrix2 = pymel.core.createNode( 'composeMatrix' )
    multMatrix = pymel.core.createNode( 'multMatrix' )
    composeMatrix.outputMatrix >> multMatrix.i[0]
    composeMatrix2.outputMatrix >> multMatrix.i[1]
    jnt.shape_tx >> composeMatrix.inputTranslateX
    jnt.shape_ty >> composeMatrix.inputTranslateY
    jnt.shape_tz >> composeMatrix.inputTranslateZ
    jnt.shape_rx >> composeMatrix.inputRotateX
    jnt.shape_ry >> composeMatrix.inputRotateY
    jnt.shape_rz >> composeMatrix.inputRotateZ
    jnt.shape_sx >> composeMatrix.inputScaleX
    jnt.shape_sy >> composeMatrix.inputScaleY
    jnt.shape_sz >> composeMatrix.inputScaleZ
    jnt.scaleMult >> composeMatrix2.inputScaleX
    jnt.scaleMult >> composeMatrix2.inputScaleY
    jnt.scaleMult >> composeMatrix2.inputScaleZ
    trGeo = pymel.core.createNode( 'transformGeometry' )
    try:jnt.attr( 'radius' ).set( 0 )
    except:pass
    
    ioShape.local >> trGeo.inputGeometry
    multMatrix.matrixSum >> trGeo.transform
    
    trGeo.outputGeometry >> crvShape.create
    
    if colorIndex != -1:
        shape = jnt.getShape().name()
        cmds.setAttr( shape + '.overrideEnabled', 1 )
        cmds.setAttr( shape + '.overrideColor', colorIndex )

    return jnt



def getNodeFromHistory( target, nodeType ):
    
    pmTarget = pymel.core.ls( target )[0]
    hists = pmTarget.history()
    targetNodes = []
    for hist in hists:
        if hist.type() == nodeType:
            targetNodes.append( hist )
    return targetNodes




def setGeometryMatrixToTarget( inputGeo, inputMatrixTarget ):
    
    geo = pymel.core.ls( inputGeo )[0]
    matrixTarget = pymel.core.ls( inputMatrixTarget )[0]
    geoShapes = geo.listRelatives( s=1 )
    
    geoMatrix    = listToMatrix( pymel.core.xform( geo, q=1, ws=1, matrix=1 ) )
    targetMatrix = listToMatrix( pymel.core.xform( matrixTarget, q=1, ws=1, matrix=1 ) )
    
    for shape in geoShapes:
        if shape.attr( 'io' ).get():
            pymel.core.delete( shape )
    
    geoShapes = geo.listRelatives( s=1 )
    
    for geoShape in geoShapes:
        cmds.select( geoShape.name() )
        cmds.CreateCluster()
        shapeHists = cmds.listHistory( geoShape.name() )
        origShape = None
        cluster = None
        for hist in shapeHists:
            if cmds.nodeType( hist ) == 'cluster':
                cluster = hist
            if not cmds.nodeType( hist ) in ['mesh','nurbsCurve', 'nurbsSurface']: continue
            if not cmds.getAttr( hist + '.io' ): continue
            origShape = pymel.core.ls( hist )[0]
            break
        
        outputAttr = None
        inputAttr = None
        
        if origShape.type() == 'mesh':
            outputAttr = 'outMesh'
            inputAttr = 'inMesh'
        elif origShape.type() == 'nurbsCurve':
            outputAttr = 'local'
            inputAttr = 'create'
        
        trGeo = pymel.core.createNode( 'transformGeometry' )
        origShape.attr( outputAttr ) >> trGeo.inputGeometry
        trGeo.outputGeometry >> geoShape.attr( inputAttr )
        trGeo.transform.set( matrixToList(geoMatrix * targetMatrix.inverse()), type='matrix' )
        cmds.select( geoShape.name() )
        cmds.DeleteHistory()
    
    pymel.core.xform( geo, ws=1, matrix= matrixTarget.wm.get() )




def setMeshPoints( srcShape, dstShape ):
    
    fnSrc = OpenMaya.MFnMesh( getDagPath( srcShape ) )
    fnDst = OpenMaya.MFnMesh( getDagPath( dstShape ) )
    
    srcPoints = OpenMaya.MPointArray()
    fnSrc.getPoints( srcPoints )
    fnDst.setPoints( srcPoints )
    



def autoCopyWeight( *args ):
    
    first = pymel.core.ls( args[0] )[0].name()
    second = pymel.core.ls( args[1] )[0].name()
    
    hists = cmds.listHistory( first, pdo=1 )
    
    skinNode = None
    for hist in hists:
        if cmds.nodeType( hist ) == 'skinCluster':
            skinNode = hist
    
    if not skinNode: return None
    
    targetSkinNode = None
    targetHists = cmds.listHistory( second, pdo=1 )
    if targetHists:
        for hist in targetHists:
            if cmds.nodeType( hist ) == 'skinCluster':
                targetSkinNode = hist

    if not targetSkinNode:
        bindObjs = cmds.listConnections( skinNode+'.matrix', s=1, d=0, type='joint' )
        bindObjs.append( second )
        cmds.skinCluster( bindObjs, tsb=1 )
    
    cmds.copySkinWeights( first, second, noMirror=True, surfaceAssociation='closestPoint', influenceAssociation ='oneToOne' )

    


def copyWeightToSpecifyObjects( inputSrcMesh, inputDstMesh, inputSrcJnt, inputDstJnt ):
    
    srcJnt = pymel.core.ls( inputSrcJnt )[0]
    dstJnt = pymel.core.ls( inputDstJnt )[0]
    
    srcMesh = pymel.core.ls( inputSrcMesh )[0]
    trgMesh = pymel.core.ls( inputDstMesh )[0]
    
    srcSkin = getNodeFromHistory( srcMesh, 'skinCluster' )[0]
    dstSkin = getNodeFromHistory( trgMesh, 'skinCluster' )[0]
    
    srcMtxIndex = None
    for con in srcJnt.listConnections( type='skinCluster', p=1 ):
        if con.node().name() != srcSkin.name(): continue
        if con.longName().find( 'matrix' ) == -1: continue
        srcMtxIndex = con.index()
    if not srcMtxIndex: return None
    
    dstMtxIndex = None
    for con in dstJnt.listConnections( type='skinCluster', p=1 ):
        if con.node().name() != dstSkin.name(): continue
        if con.longName().find( 'matrix' ) == -1: continue
        dstMtxIndex = con.index()
    
    if not dstMtxIndex: return None
    
    vtxWeightsMap = {}
    for i in range( srcSkin.weightList.numElements() ):
        weightsPlug = srcSkin.weightList[i].getChildren()[0]
        for j in range( weightsPlug.numElements() ):
            if weightsPlug[j].logicalIndex() != srcMtxIndex: continue
            weightValue = weightsPlug[j].get()
            if not weightValue: continue
            vtxWeightsMap.update( { i: weightValue } )
    
    for i, value in vtxWeightsMap.items():
        weightsPlug = dstSkin.weightList[i].getChildren()[0]
        multValue = 1.0-value
        origValue = 0
        for element in weightsPlug.elements():
            origValue += cmds.getAttr( dstSkin + '.' + element )
            cmds.setAttr( dstSkin + '.' + element, cmds.getAttr( dstSkin + '.' + element ) * multValue )

        weightsPlug[dstMtxIndex].set( weightsPlug[dstMtxIndex].get() + value )



def copyWeightToSmoothedMesh( inputSrcMesh, inputSmoothedMesh, keepSrcVtx=False ):

    from maya import mel

    srcMesh      = pymel.core.ls( inputSrcMesh )[0]    
    smoothedMesh = pymel.core.ls( inputSmoothedMesh )[0]
    
    autoCopyWeight( srcMesh, smoothedMesh )
    
    srcShape = cmds.listRelatives( srcMesh.name(), s=1, f=1 )[0]
    targetShape = cmds.listRelatives( smoothedMesh.name(), s=1, f=1 )[0]
    srcSkinCluster = getNodeFromHistory( srcMesh, 'skinCluster')[0]
    targetSkinCluster = getNodeFromHistory( smoothedMesh, 'skinCluster' )[0]
    
    dagPathSrc = getDagPath( srcShape )
    dagPathTrg = getDagPath( targetShape )
    fnMeshSrc    = OpenMaya.MFnMesh( dagPathSrc )
    fnMeshTarget = OpenMaya.MFnMesh( dagPathTrg )
    fnSkinClusterSrc    = OpenMaya.MFnDependencyNode( getMObject( srcSkinCluster ) )
    fnSkinClusterTarget = OpenMaya.MFnDependencyNode( getMObject( targetSkinCluster ) )
    
    numVerticesSrc    = fnMeshSrc.numVertices()
    numVerticesTarget = fnMeshTarget.numVertices()
    
    matrixPlugSrc     = fnSkinClusterSrc.findPlug( 'matrix' )
    matrixPlugTarget  = fnSkinClusterTarget.findPlug( 'matrix' )
    weightListPlugSrc = fnSkinClusterSrc.findPlug( 'weightList' )
    weightListPlugTrg = fnSkinClusterTarget.findPlug( 'weightList' )
    
    dictSrcJointElementIndices = {}
    dictTrgJointElementIndices = {}
    srcJntList = []
    trgJntList = []
    for i in range( matrixPlugSrc.numElements() ):
        srcJnt = cmds.listConnections( matrixPlugSrc[i].name(), s=1, d=0 )[0]
        trgJnt = cmds.listConnections( matrixPlugTarget[i].name(), s=1, d=0 )[0]
        srcJntList.append( srcJnt )
        trgJntList.append( trgJnt )
        dictSrcJointElementIndices.update( {srcJnt:matrixPlugSrc[i].logicalIndex()} )
        dictTrgJointElementIndices.update( {trgJnt:matrixPlugTarget[i].logicalIndex()} )
    
    srcToTrgMap = {}
    for i in range( matrixPlugSrc.numElements() ):
        srcIndex = dictSrcJointElementIndices[ srcJntList[i] ]
        trgIndex = dictTrgJointElementIndices[ trgJntList[i] ]
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
    fnMesh    = OpenMaya.MFnMesh( dagPathTrg )
    weightListPlug = fnSkinClusterTarget.findPlug( 'weightList' )
    
    util = OpenMaya.MScriptUtil()
    util.createFromInt( 0 )
    prevIndex = util.asIntPtr()
    
    twoVtxIndices = []
    fourVtxIndices = []
    
    for i in range( numVerticesSrc, numVerticesTarget ):
        itMeshTrg.setIndex( i, prevIndex )
        faceIndicesConnected = OpenMaya.MIntArray()
        itMeshTrg.getConnectedFaces( faceIndicesConnected )
        srcVtxIndices = []
        for j in range( faceIndicesConnected.length() ):
            vtxIndices = OpenMaya.MIntArray()
            fnMesh.getPolygonVertices( faceIndicesConnected[j], vtxIndices )
            for k in range( vtxIndices.length() ):
                if vtxIndices[k] >= numVerticesSrc: continue
                if vtxIndices[k] in srcVtxIndices: continue
                srcVtxIndices.append( vtxIndices[k] )    
        
        weightsPlug = weightListPlug[i].child(0)
        for j in range( weightsPlug.numElements() ):
            cmds.removeMultiInstance( weightsPlug[0].name() )
        
        logicalMap = {}
        numSample = len( srcVtxIndices )
        
        if numSample == 2:
            twoVtxIndices.append( i )
        if numSample == 4:
            fourVtxIndices.append( i )
        
        for srcVtxIndex in srcVtxIndices:
            srcWeightsPlug = weightListPlug[srcVtxIndex].child(0)
            for j in range( srcWeightsPlug.numElements() ):
                logicalIndex = srcWeightsPlug[j].logicalIndex()
                value = srcWeightsPlug[j].asFloat() 
                if not logicalMap.has_key( logicalIndex ):
                    logicalMap.update( {logicalIndex:0})
                logicalMap[logicalIndex] += value/numSample

        for key, value in logicalMap.items():
            weightPlug = weightsPlug.elementByLogicalIndex( key )
            weightPlug.setFloat( value )
    
    if not keepSrcVtx:
        for i in range( numVerticesSrc ):
            itMeshTrg.setIndex( i, prevIndex )
            vtxIndicesConnected = OpenMaya.MIntArray()
            itMeshTrg.getConnectedVertices(vtxIndicesConnected)
            weightsPlug = weightListPlug[i].child(0)
            weightsMap = {}
            for j in range( weightsPlug.numElements() ):
                weightsMap.update( {weightsPlug[j].logicalIndex():weightsPlug[j].asFloat()*0.125} )
            
            multValue = 0.875/vtxIndicesConnected.length()
            for j in range( vtxIndicesConnected.length() ):
                connectedWeightsPlug = weightListPlug[vtxIndicesConnected[j]].child(0)
                for k in range( connectedWeightsPlug.numElements() ):
                    logicalIndex = connectedWeightsPlug[k].logicalIndex()
                    value = connectedWeightsPlug[k].asFloat()
                    if not weightsMap.has_key( logicalIndex ):
                        weightsMap.update( {logicalIndex:0})
                    weightsMap[logicalIndex] += (value *multValue)
            for key, value in weightsMap.items():
                weightsPlug.elementByLogicalIndex( key ).setFloat( value )
    
    for i in twoVtxIndices:
        itMeshTrg.setIndex( i, prevIndex )
        vtxIndicesConnected = OpenMaya.MIntArray()
        itMeshTrg.getConnectedVertices(vtxIndicesConnected)
        weightsPlug = weightListPlug[i].child(0)
        weightsMap = {}
        for j in range( weightsPlug.numElements() ):
            weightsMap.update( {weightsPlug[j].logicalIndex():weightsPlug[j].asFloat()*0.5} )
        
        multValue = 0.5/vtxIndicesConnected.length()
        for j in range( vtxIndicesConnected.length() ):
            connectedWeightsPlug = weightListPlug[vtxIndicesConnected[j]].child(0)
            for k in range( connectedWeightsPlug.numElements() ):
                logicalIndex = connectedWeightsPlug[k].logicalIndex()
                value = connectedWeightsPlug[k].asFloat()
                if not weightsMap.has_key( logicalIndex ):
                    weightsMap.update( {logicalIndex:0})
                weightsMap[logicalIndex] += (value *multValue)
        for key, value in weightsMap.items():
            weightsPlug.elementByLogicalIndex( key ).setFloat( value )
    



def edgeStartAndEndWeightHammer( inputEdges, weightPercent=1.0 ):
    
    inputEdgeIndices = [ pymel.core.ls( inputEdge )[0].index() for inputEdge in inputEdges ]
    orderedIndices = getOrderedEdgeLoopIndices( inputEdges[0] )
    
    orderedInputIndices = []
    for orderedIndex in orderedIndices:
        if not orderedIndex in inputEdgeIndices: continue
        orderedInputIndices.append( orderedIndex )
    
    mesh = pymel.core.ls( inputEdges[0] )[0].node()
    srcMeshs = getNodeFromHistory( mesh, 'mesh' )
    
    origMesh = copy.copy( mesh )
    for srcMesh in srcMeshs:
        if mesh.name() == srcMesh.name(): continue
        if mesh.numVertices() != srcMesh.numVertices(): continue
        origMesh = srcMesh
    
    orderedVtxIndices = []
    dagPath = getDagPath( origMesh )
    fnMesh = OpenMaya.MFnMesh( dagPath )
    
    for orderedIndex in orderedInputIndices:
        util = OpenMaya.MScriptUtil()
        util.createFromList([0,0],2)
        int2Ptr = util.asInt2Ptr()
        
        fnMesh.getEdgeVertices( orderedIndex, int2Ptr )
        appendTargets = []
        for vtxIndex in [util.getInt2ArrayItem( int2Ptr, 0, i ) for i in range(2) ]:
            appendTargets.append( vtxIndex )
        if len( orderedVtxIndices ) == 2:
            if orderedVtxIndices[0] in appendTargets:
                orderedVtxIndices.reverse()
        for appendTarget in appendTargets:
            if appendTarget in orderedVtxIndices: continue
            orderedVtxIndices.append( appendTarget )
    
    distList = []
    allDist = 0
    for i in range( len( orderedVtxIndices ) -1 ):
        firstPoint =  OpenMaya.MPoint( *pymel.core.xform( origMesh + '.vtx[%d]' % orderedVtxIndices[i], q=1, ws=1, t=1 )[:3] )
        secondPoint = OpenMaya.MPoint( *pymel.core.xform( origMesh + '.vtx[%d]' % orderedVtxIndices[i+1], q=1, ws=1, t=1 )[:3] )
        dist = firstPoint.distanceTo( secondPoint )
        distList.append( dist )
        allDist += dist
    
    startVtx = mesh + '.vtx[%d]' % orderedVtxIndices[0]
    endVtx   = mesh + '.vtx[%d]' % orderedVtxIndices[-1]
    
    startPlugs = getWeightPlugFromSkinedVertex(startVtx)
    endPlugs   = getWeightPlugFromSkinedVertex(endVtx)
    
    for i in range( 1, len( orderedVtxIndices )-1 ):
        currentDist = reduce( lambda x, y : x+y, distList[:i] )
        targetVtx = mesh + '.vtx[%d]' % orderedVtxIndices[i]
        targetPlugs = getWeightPlugFromSkinedVertex(targetVtx)
        weightValue = currentDist/allDist
        revValue    = 1.0 - weightValue
        
        targetPlugArray = targetPlugs[0].array()
        
        valueKeep = 1.0 - weightPercent
        existsIndices = []
        for targetPlug in targetPlugs:
            targetPlug.set( valueKeep * targetPlug.get() )
            existsIndices.append( targetPlug.index() )
        
        for startPlug in startPlugs:
            startIndex = startPlug.index()
            if startIndex in existsIndices:
                targetPlugArray[startIndex].set( targetPlugArray[startIndex].get() + revValue * startPlug.get() * weightPercent )
            else:
                targetPlugArray[startIndex].set( revValue * startPlug.get() * weightPercent )
                existsIndices.append( startIndex )
        
        for endPlug in endPlugs:
            endIndex = endPlug.index()
            if endIndex in existsIndices:
                targetPlugArray[endIndex].set( targetPlugArray[endIndex].get() + weightValue * endPlug.get()* weightPercent )
            else:
                targetPlugArray[endIndex].set( weightValue * endPlug.get() * weightPercent )

        


def createFourByFourMatrixCube( inputTarget ):
    
    target = pymel.core.ls( inputTarget )[0]
    
    curvePoses = [ [1,0,0], [0,1,0], [0,0,1], [0,0,0] ]
    newCurve = pymel.core.curve( p=curvePoses, d=1 )
    ioShape = addIOShape( newCurve )
    
    compose = pymel.core.createNode( 'composeMatrix' )
    trGeo = pymel.core.createNode( 'transformGeometry' )
    compose.outputMatrix >> trGeo.transform
    ioShape.local >> trGeo.inputGeometry
    addAttr( newCurve, ln='size', min=0, dv=1, cb=1 )
    newCurve.size >> compose.isx
    newCurve.size >> compose.isy
    newCurve.size >> compose.isz
    trGeo.outputGeometry >> newCurve.getShape().create
    curveWorldGeo = pymel.core.createNode( 'transformGeometry' )
    newCurve.getShape().local >> curveWorldGeo.inputGeometry
    newCurve.m >> curveWorldGeo.transform
    
    newTrs = []
    for i in range( 4 ):
        curveInfo = pymel.core.createNode( 'pointOnCurveInfo' )
        curveWorldGeo.outputGeometry >> curveInfo.inputCurve
        curveInfo.parameter.set( i )
        newTr = pymel.core.createNode( 'transform' )
        curveInfo.position >> newTr.t
        newTrs.append( newTr )
    
    newCurve.size >> newTrs[-1].sx
    newCurve.size >> newTrs[-1].sy
    newCurve.size >> newTrs[-1].sz
    
    dcmpX = getLocalDecomposeMatrix( newTrs[0].wm, newTrs[-1].wim )
    dcmpY = getLocalDecomposeMatrix( newTrs[1].wm, newTrs[-1].wim )
    dcmpZ = getLocalDecomposeMatrix( newTrs[2].wm, newTrs[-1].wim )
    
    fbf = pymel.core.createNode( 'fourByFourMatrix' )
    mm  = pymel.core.createNode( 'multMatrix' )
    fbfDcmp = pymel.core.createNode( 'decomposeMatrix' )
    dcmpX.otx >> fbf.in00
    dcmpX.oty >> fbf.in01
    dcmpX.otz >> fbf.in02
    dcmpY.otx >> fbf.in10
    dcmpY.oty >> fbf.in11
    dcmpY.otz >> fbf.in12
    dcmpZ.otx >> fbf.in20
    dcmpZ.oty >> fbf.in21
    dcmpZ.otz >> fbf.in22
    newTrs[-1].tx >> fbf.in30
    newTrs[-1].ty >> fbf.in31
    newTrs[-1].tz >> fbf.in32
    fbf.output >> mm.i[0]
    mm.matrixSum >> fbfDcmp.imat
    
    newGrp = pymel.core.group( em=1 )
    pymel.core.parent( newCurve, newTrs, newGrp )
    
    newGrp.wm >> mm.i[1]
    
    resultTr = pymel.core.createNode( 'transform', n= 'Result' )
    resultTr.dh.set( 1 )
    resultTr.pim >> mm.i[2]
    
    fbfDcmp.outputTranslate >> resultTr.t
    fbfDcmp.outputRotate >> resultTr.r
    fbfDcmp.outputScale >> resultTr.s
    fbfDcmp.outputShear >> resultTr.sh
    
    pymel.core.xform( newGrp, ws=1, matrix= target.wm.get() )
    
    return resultTr, newGrp




def getDirectionIndex( inputVector ):
    
    import math
    
    if type( inputVector ) in [ list, tuple ]:
        normalInput = OpenMaya.MVector(*inputVector).normal()
    else:
        normalInput = OpenMaya.MVector(inputVector).normal()
    
    xVector = OpenMaya.MVector( 1,0,0 )
    yVector = OpenMaya.MVector( 0,1,0 )
    zVector = OpenMaya.MVector( 0,0,1 )
    
    xdot = xVector * normalInput
    ydot = yVector * normalInput
    zdot = zVector * normalInput
    
    xabs = math.fabs( xdot )
    yabs = math.fabs( ydot )
    zabs = math.fabs( zdot )
    
    dotList = [xdot, ydot, zdot]
    
    dotIndex = 0
    if xabs < yabs:
        dotIndex = 1
        if yabs < zabs:
            dotIndex = 2
    elif xabs < zabs:
        dotIndex = 2
        
    if dotList[ dotIndex ] < 0:
        dotIndex += 3
    
    return dotIndex




def getCurveInfo( inputCurveAttr ):
        
    curveAttr = pymel.core.ls( inputCurveAttr )[0]
    consCurveInfo = curveAttr.listConnections( s=0, d=1, type='curveInfo' )
    if consCurveInfo:
        curveInfo = consCurveInfo[0]
    else:
        curveInfo = pymel.core.createNode( 'curveInfo' )
        curveAttr >> curveInfo.inputCurve
    return curveInfo


    

def connectCurveScale( inputCurveOrigAttr, inputCurveCurrentAttr, inputTargetJnt ):

    curveOrigAttr = pymel.core.ls( inputCurveOrigAttr )[0]
    curveCurrentAttr = pymel.core.ls( inputCurveCurrentAttr )[0]
    targetJnt = pymel.core.ls( inputTargetJnt )[0]

    curveOrigInfo    = getCurveInfo( curveOrigAttr )
    curveCurrentInfo = getCurveInfo( curveCurrentAttr )
    def getCurveDistanceNode( curveOrigInfo, curveCurrentInfo ):
        divNode = curveOrigInfo.arcLength.listConnections( type='multiplyDivide' )
        if divNode:
            if pymel.core.isConnected( curveCurrentInfo.arcLength, divNode[0].input1X ):
                return divNode[0]
        divNode = pymel.core.createNode( 'multiplyDivide' )
        curveCurrentInfo.arcLength >> divNode.input1X
        curveOrigInfo.arcLength >> divNode.input2X
        divNode.op.set( 2 )
        return divNode
    divNode = getCurveDistanceNode( curveOrigInfo, curveCurrentInfo )
    
    curveDagPath = getDagPath( inputCurveCurrentAttr.node().name() )
    fnCurve = OpenMaya.MFnNurbsCurve( curveDagPath )
    
    targetWorldPoint = OpenMaya.MPoint( *pymel.core.xform( targetJnt, q=1, ws=1, t=1 ) )
    targetLocalPoint = targetWorldPoint * curveDagPath.inclusiveMatrixInverse()
    
    util = OpenMaya.MScriptUtil()
    util.createFromDouble( 0.0 )
    ptrDouble = util.asDoublePtr()
    fnCurve.getParamAtPoint( targetLocalPoint, ptrDouble, 10000.0 )
    tangent = fnCurve.tangent( util.getDouble(ptrDouble) )
    
    axisName = ['X','Y','Z'][(getDirectionIndex( tangent )+3)%3]
    
    divNode.outputX >> targetJnt.attr( 'scale%s' % axisName )
    
        
    

def duplicateBlendShapeByCtl(ctls, inputSrcMesh ):
    
    srcMesh = pymel.core.ls( inputSrcMesh )[0]
    
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
    
    
    duMeshs = []
    for inputCtl in ctls:
        ctl = pymel.core.ls( inputCtl )[0]
        attrs = ctl.listAttr( k=1 )
        for attr in attrs:
            #print "attr : ", attr
            if attr.isLocked(): continue
            blendCons = getBlendShapeDestConnections( attr )
            srcAttrNames = []
            for srcAttr, dstAttr in blendCons:
                attrName = cmds.ls( dstAttr.name() )[0].split( '.' )[-1]
                if srcAttr.name() in srcAttrNames: continue
                srcAttrNames.append( srcAttr.name() )
                dstAttr.set( 1 )
                duMesh = pymel.core.duplicate( srcMesh, n= srcMesh.name() + '_' + attrName )[0]
                duMeshs.append( duMesh )
                duMesh.setParent( w=1 )
                dstAttr.set( 0 )
    return duMeshs



def getMDagPathAndComponent():
    
    mSelList = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList( mSelList )
    
    returnTargets = []
    for i in range( mSelList.length() ):
        mDagPath = OpenMaya.MDagPath()
        mObject  = OpenMaya.MObject()
        
        mSelList.getDagPath( i, mDagPath, mObject )
        
        mIntArrU = OpenMaya.MIntArray()
        mIntArrV = OpenMaya.MIntArray()
        mIntArrW = OpenMaya.MIntArray()
        
        if not mObject.isNull():
            if mDagPath.apiType() == OpenMaya.MFn.kNurbsCurve:
                component = OpenMaya.MFnSingleIndexedComponent( mObject )
                component.getElements( mIntArrU )
            elif mDagPath.apiType() == OpenMaya.MFn.kNurbsSurface:
                component = OpenMaya.MFnDoubleIndexedComponent( mObject )
                component.getElements( mIntArrU, mIntArrV )
            elif mDagPath.apiType() == OpenMaya.MFn.kLattice:
                component = OpenMaya.MFnTripleIndexedComponent( mObject )
                component.getElements( mIntArrU, mIntArrV, mIntArrW )
            elif mObject.apiType() == OpenMaya.MFn.kMeshVertComponent:
                component = OpenMaya.MFnSingleIndexedComponent( mObject )
                component.getElements( mIntArrU )
            elif mObject.apiType() == OpenMaya.MFn.kMeshEdgeComponent:
                mfnMesh = OpenMaya.MFnMesh( mDagPath )
                component = OpenMaya.MFnSingleIndexedComponent( mObject )
                mIntArr = OpenMaya.MIntArray()
                component.getElements( mIntArr )
                mIntArrU.setLength( mIntArr.length() * 2 )
                util = OpenMaya.MScriptUtil()
                util.createFromList([0,0],2)
                ptrEdgeToVtxIndex = util.asInt2Ptr()
                for i in range( mIntArr.length() ):
                    mfnMesh.getEdgeVertices( mIntArr[i], ptrEdgeToVtxIndex )
                    index1 = util.getInt2ArrayItem( ptrEdgeToVtxIndex, 0, 0 )
                    index2 = util.getInt2ArrayItem( ptrEdgeToVtxIndex, 0, 1 )
                    mIntArrU[i*2  ] = index1
                    mIntArrU[i*2+1] = index2 
            elif mObject.apiType() == OpenMaya.MFn.kMeshPolygonComponent:
                mfnMesh = OpenMaya.MFnMesh( mDagPath )
                component = OpenMaya.MFnSingleIndexedComponent( mObject )
                mIntArr = OpenMaya.MIntArray()
                component.getElements( mIntArr )
                mIntArrEach = OpenMaya.MIntArray()
                for i in range( mIntArr.length() ):
                    mfnMesh.getPolygonVertices( mIntArr[i], mIntArrEach )
                    for i in range( mIntArrEach.length() ):
                        mIntArrU.append( mIntArrEach[i] )
        
        returnTargets.append( [mDagPath, list( set( mIntArrU ) ), list( set( mIntArrV ) ), list( set( mIntArrW ) )] )
    
    return returnTargets




def setInfluenceOnlySelJoint():
        
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





def getClosestVertexIndex( position, mesh ):
    
    if type( position ) in [tuple, list]:
        pos = OpenMaya.MPoint( *position )
    else:
        pos = OpenMaya.MPoint( position )
    
    if cmds.nodeType( mesh ) == 'transform':
        meshShape = cmds.listRelatives( mesh, s=1, f=1 )[0]
    else:
        meshShape = mesh
    
    dagPathMesh = getDagPath( meshShape )
    intersector = OpenMaya.MMeshIntersector()
    intersector.create( dagPathMesh.node() )
    
    meshMatrix = dagPathMesh.inclusiveMatrix()
    localPos = pos * meshMatrix.inverse()
    
    pointOnMesh = OpenMaya.MPointOnMesh()
    intersector.getClosestPoint( localPos, pointOnMesh )
    
    faceIndex = pointOnMesh.faceIndex()
    fnMesh = OpenMaya.MFnMesh( dagPathMesh )
    vtxIndices = OpenMaya.MIntArray()
    fnMesh.getPolygonVertices( faceIndex, vtxIndices )

    points = OpenMaya.MPointArray()
    fnMesh.getPoints( points )
    minDist = 10000000.0
    minDistIndex = vtxIndices[0]
    for i in range( vtxIndices.length() ):
        vtxIndex = vtxIndices[i]
        point = points[ vtxIndex ]
        dist = point.distanceTo( localPos )
        if dist < minDist:
            minDist = dist
            minDistIndex = vtxIndex
    return minDistIndex





def addInfluenceOnlyOneCloseVertex( inputJnt, inputMesh ):
    
    jnt = pymel.core.ls( inputJnt )[0]
    mesh = pymel.core.ls( inputMesh )[0]
    
    try:pymel.core.skinCluster( getNodeFromHistory( mesh, 'skinCluster' )[0], e=1, dr=10, lw=True, wt=0, ai=jnt )
    except:pass
    
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
    closeIndex = getClosestVertexIndex( pymel.core.xform( jnt, q=1, ws=1, t=1 )[:3], mesh.name() )
    
    fnNode = OpenMaya.MFnDependencyNode( getMObject( targetSkinNode.name() ) )
    wlPlug = fnNode.findPlug( 'weightList' )[ closeIndex ].child(0)
    
    for i in range( wlPlug.numElements() ):
        cmds.removeMultiInstance( wlPlug[0].name() )
    
    skinCons = jnt.wm.listConnections( type='skinCluster', p=1 )
    for skinCon in skinCons:
        node = skinCon.node()
        jntIndex = skinCon.index()
        if node.name() != targetSkinNode.name(): continue
        cmds.setAttr( wlPlug.name() + '[%d]' % jntIndex, 1 )
    



def createLoopCurve( edge1 ):
        
    cmds.select( edge1 )
    cmds.SelectEdgeLoopSp()
    curve1 = cmds.polyToCurve( form=2, degree=3 )[0]
    return curve1




def setWorldGeometryToLocalGeometry( geo, mtxTarget ):
        
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




def createPointsFromCurve( curve1, numPoints ):
        
    curveShape = cmds.listRelatives( curve1, s=1, f=1 )[0]        
    fourPoints = []
    for i in range( numPoints ):
        trNode = cmds.createNode( 'transform' )
        cmds.setAttr( trNode + '.dh', 1 )
        curveInfo = cmds.createNode( 'pointOnCurveInfo' )
        animCurve = cmds.createNode( 'animCurveUU' )
        cmds.setKeyframe( animCurve, f=0, v=0 )
        cmds.setKeyframe( animCurve, f=1, v=1 )
        cmds.selectKey( animCurve, add=1, k=1, f=(0.0, 1.0) )
        cmds.keyTangent( animCurve, itt='linear', ott='linear' )
        cmds.setAttr( animCurve + '.preInfinity', 3 )
        cmds.setAttr( animCurve + '.postInfinity', 3 )
        cmds.connectAttr( curveShape + '.local', curveInfo + '.inputCurve' )
        cmds.setAttr( curveInfo + '.top', 1 )
        cmds.addAttr( trNode, ln='parameter', dv=i / float( numPoints ) )
        cmds.setAttr( trNode + '.parameter', e=1, k=1 )
        cmds.connectAttr( trNode + '.parameter', animCurve + '.input' )
        cmds.connectAttr( animCurve + '.output', curveInfo + '.parameter' )
        cmds.connectAttr( curveInfo + '.position', trNode + '.t' )
        fourPoints.append( trNode )
    return fourPoints




def getDistanceNodeFromTwoObjs( target1, target2 ):
    
        pmTarget1 = pymel.core.ls( target1 )[0]
        pmTarget2 = pymel.core.ls( target2 )[0]
        
        distNode = pymel.core.createNode( 'distanceBetween' )
        pmTarget1.t >> distNode.point1
        pmTarget2.t >> distNode.point2
        
        distNode.addAttr( 'origDist', dv= distNode.distance.get() )
        
        return distNode.name(), 'origDist'



def addCurveDistanceInfo( inputCurve ):
    
    NAME_origLength = 'origLength'
    NAME_currentLength = 'currentLength'
    
    curve = pymel.core.ls( inputCurve )[0]
    if curve.type() == 'nurbsCurve':
        curveShape = curve
    else:
        curveShape = curve.getShape()
    
    curve = curveShape.getParent()
    if not pymel.core.attributeQuery( NAME_origLength, node=curve, ex=1 ):curve.addAttr( NAME_origLength )
    pymel.core.setAttr( curve.attr(NAME_origLength), e=1, cb=1 )
    if not pymel.core.attributeQuery( NAME_currentLength, node=curve, ex=1 ):curve.addAttr( NAME_currentLength )
    pymel.core.setAttr( curve.attr(NAME_currentLength), e=1, cb=1 )
    
    curveInfos = curve.attr(NAME_currentLength).listConnections( s=1, d=0, type='curveInfo' )
    if not curve.currentLength.listConnections( s=1, d=0, type='curveInfo' ):
        info = pymel.core.createNode( 'curveInfo' )
        curveShape.local >> info.inputCurve
        info.arcLength >> curve.currentLength
    else:
        info = curveInfos[0]
    
    curve.origLength.set( info.arcLength.get() )
    return NAME_origLength, NAME_currentLength



def makeCurveFromSelection( *inputSels, **options ):
    
    poses = []
    sels = []
    for inputSel in inputSels:
        sels.append( pymel.core.ls( inputSel )[0] )
    for sel in sels:
        pose = pymel.core.xform( sel, q=1, ws=1, t=1 )[:3]
        poses.append( pose )
    curve = pymel.core.curve( p=poses, **options )
    curveShape = curve.getShape()
    
    for i in range( len( sels ) ):
        dcmp = pymel.core.createNode( 'decomposeMatrix' )
        vp   = pymel.core.createNode( 'vectorProduct' )
        vp.setAttr( 'op', 4 )
        sels[i].wm >> dcmp.imat
        dcmp.ot >> vp.input1
        curve.wim >> vp.matrix
        vp.output >> curveShape.attr( 'controlPoints' )[i]
    
    return curve.name()




def getSortedEdgesInSameRing( inputEdges ):
    
    edges = [ pymel.core.ls( inputEdge )[0].name() for inputEdge in inputEdges ]
    edgeRings = getOrderedEdgeRings( edges[0] )
    
    orderedEdges = {}
    for edge in edges:
        if edge in edgeRings:
            orderedEdges.update( { edgeRings.index(edge):edge } )
    
    def sortCmp( input1, input2 ):
        return cmp( input1[0], input2[0] )
    
    items = orderedEdges.items()
    items.sort( sortCmp )
    return [ value for index, value in items ]



def setTransformDefault( inputTarget ):
    target = pymel.core.ls( inputTarget )[0]
    attrs = ['tx','ty','tz','rx','ry','rz','sx','sy','sz']
    values = [0,0,0,0,0,0,1,1,1]
    for i in range( len( attrs ) ):
        try:cmds.setAttr( target + '.' + attrs[i], values[i] )
        except:pass



def rigWithEdgeRing( inputEdges, inputBaseTransform, degree=2 ):
    
    edges = getSortedEdgesInSameRing( inputEdges )
    baseTransform = pymel.core.ls( inputBaseTransform )[0].name()
    
    def createCenterPoint( trObjects ):
        
        averageNode = cmds.createNode( 'plusMinusAverage' )
        cmds.setAttr( averageNode + '.op', 3 )
        
        centerNode = cmds.createNode( 'transform' )
        cmds.setAttr( centerNode + '.dh', 1 )
        for i in range( len( trObjects ) ):
            cmds.connectAttr( trObjects[i] + '.t', averageNode + '.input3D[%d]' % i )
        cmds.connectAttr( averageNode + '.output3D', centerNode + '.t' )
        return centerNode
    
    loopCurves = []
        
    for edge in edges:
        loopCurve = createLoopCurve( edge )
        loopCurves.append(loopCurve )
        setWorldGeometryToLocalGeometry( loopCurve, baseTransform )
    
    pointsList = []
    #print "loopCurves :", len( loopCurves )
    for loopCurve in loopCurves:
        points = createPointsFromCurve( loopCurve, 4 )
        pointsList.append( points )
    centers = []
    for points in pointsList:
        center = createCenterPoint( points )
        centers.append( center )
    
    curve = makeCurveFromSelection( *centers, d=degree )
    origAttrName, currentAttrName = addCurveDistanceInfo(curve)
    scaleNode = cmds.createNode( 'multiplyDivide' )
    cmds.setAttr( scaleNode + '.op', 2 )
    #print curve + '.' + currentAttrName
    #print cmds.ls( curve + '.' + currentAttrName )
    cmds.connectAttr( curve + '.' + currentAttrName, scaleNode + '.input1X' )
    cmds.connectAttr( curve + '.' + origAttrName, scaleNode + '.input2X' )
    
    jntCenters = []
    for i in range( len( centers ) ):
        pymel.core.select( baseTransform )
        jntCenters.append( cmds.joint() )
    
    for i in range( len(edges) ):
        constrain_point( centers[i], jntCenters[i] )
        tangentNode = cmds.tangentConstraint( curve, jntCenters[i], aim=[0,1,0], u=[1,0,0], wut='vector' )[0]
        upNode1 = pointsList[i][0]
        upNode2 = pointsList[i][2]
        dcmp1 = getDecomposeMatrix( upNode1 + '.wm' )
        dcmp2 = getDecomposeMatrix( upNode2 + '.wm' )
        upVectorNode = cmds.createNode( 'plusMinusAverage' )
        cmds.setAttr( upVectorNode + '.operation', 2 )
        cmds.connectAttr( dcmp1 + '.ot', upVectorNode+'.input3D[0]' )
        cmds.connectAttr( dcmp2 + '.ot', upVectorNode+'.input3D[1]' )
        cmds.connectAttr( upVectorNode + '.output3D', tangentNode + '.worldUpVector' )
        cmds.connectAttr( scaleNode + '.outputX', jntCenters[i] + '.sy' )
        
        distNode1, origAttrName1 = getDistanceNodeFromTwoObjs( pointsList[i][0], pointsList[i][2] )
        distNode2, origAttrName2 = getDistanceNodeFromTwoObjs( pointsList[i][1], pointsList[i][3] )
    
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
    
    allPoints = []
    for points in pointsList:
        allPoints += points
    
    cmds.parent( loopCurves, centers, jntCenters, curve, allPoints, baseTransform )
    
    setTransformDefault( curve )
    for target in loopCurves:
        setTransformDefault( target )
    for target in centers:
        setTransformDefault( target )
    for target in jntCenters:
        setTransformDefault( target )
    for target in allPoints:
        setTransformDefault( target )

    return jntCenters




def getWeightPlugFromSkinedVertex( skinedVtx ):
    
    mesh = skinedVtx.split( '.' )[0]
    vtxId = int( skinedVtx.split( '[' )[-1].replace( ']', '' ) )
    
    skinNode = getNodeFromHistory( mesh, 'skinCluster' )[0]
    fnSkinNode = OpenMaya.MFnDependencyNode( getMObject( skinNode ) )
    
    plugWeights = fnSkinNode.findPlug( 'weightList' )[vtxId].child(0)
    
    weightInfos = []
    for i in range( plugWeights.numElements() ):
        weightInfos.append( pymel.core.ls( plugWeights[i].name() )[0] )
    return weightInfos




def removeSkinWeight( skinedVtx, maxWeight ):
    
    meshName = skinedVtx.split( '.' )[0]
    vtxId = int( skinedVtx.split( 'vtx[' )[-1].replace( ']', '' ) )
    
    skinNode = getNodeFromHistory( meshName, 'skinCluster' )[0]
    fnSkinNode = OpenMaya.MFnDependencyNode( getMObject( skinNode ) )
    
    plugWeights = fnSkinNode.findPlug( 'weightList' )[vtxId].child(0)
    for i in range( plugWeights.numElements() ):
        weight = plugWeights[i].asFloat()
        if weight < maxWeight:
            cmds.setAttr( plugWeights[i].name(), 0 )




def replaceDestinationConnection( *args ):
    
    first = pymel.core.ls( args[0] )[0] 
    second = pymel.core.ls( args[1] )[0] 
    target = pymel.core.ls( args[2] )[0]
    
    cons = target.listConnections( s=1, d=0, p=1, c=1 )
    for dest, src in cons:
        splits = src.split( '.' )
        node = splits[0]
        attr = '.'.join( splits[1:] )
        
        if src.node() != first: continue
        if not pymel.core.attributeQuery( attr, node=second, ex=1 ): continue
        try:
            cmds.connectAttr( second + '.' + attr, dest.name(), f=1 )
        except:
            pass




def getOrderedEdgeLoopIndices( targetEdge ):
    
    pymel.core.select( targetEdge )
    cmds.SelectEdgeLoop()
    
    edges = pymel.core.ls( sl=1, fl=1 )
    edgeIndices = [ edge.index() for edge in edges ]
    
    meshName = targetEdge.split( '.' )[0]
    itEdge = OpenMaya.MItMeshEdge( getDagPath( meshName ) )
    
    def getConnectedEdge( itEdge, edgeIndex, edgeIndices ):
        util = OpenMaya.MScriptUtil()
        util.createFromInt( 0 )
        prevIndex = util.asIntPtr()
        itEdge.setIndex( edgeIndex, prevIndex )
        conEdges = OpenMaya.MIntArray()
        itEdge.getConnectedEdges( conEdges )
        return [ conEdges[i] for i in range( conEdges.length() ) if conEdges[i] in edgeIndices ]
    
    currentIndex = copy.copy( edgeIndices[0] )
    
    orderedList = []
    orderedList.append( currentIndex )
    
    firstConnectedEdges = getConnectedEdge( itEdge, currentIndex, edgeIndices )
    currentIndex = copy.copy( firstConnectedEdges[0] )
    orderedList.append( currentIndex )
    
    while( True ):
        connectedEdges = getConnectedEdge( itEdge, currentIndex, edgeIndices )
        targetEdges = [ connectedEdge for connectedEdge in connectedEdges if not connectedEdge in orderedList ]
        if not targetEdges: break
        orderedList += targetEdges
        currentIndex = copy.copy( targetEdges[0] )
    
    if len( firstConnectedEdges ) >=2:
        currentIndex = copy.copy( firstConnectedEdges[1] )
        orderedList.insert( 0, currentIndex )
        while( True ):
            connectedEdges = getConnectedEdge( itEdge, currentIndex, edgeIndices )
            targetEdges = [ connectedEdge for connectedEdge in connectedEdges if not connectedEdge in orderedList ]
            if not targetEdges: break
            orderedList  = targetEdges + orderedList
            currentIndex = copy.copy( targetEdges[0] )
            
    return orderedList



def connectReverseScaleFromParent( inputTarget ):
    target = pymel.core.ls( inputTarget )[0]
    pTarget = target.getParent()
    multNode = pymel.core.createNode( 'multiplyDivide' )
    multNode.op.set( 2 )
    multNode.input1.set( 1,1,1 )
    pTarget.scale >> multNode.input2
    multNode.output >> target.scale





def keepInfluenceOnlySelComponent( components, jnts ):
    
    vtxList = pymel.core.ls( pymel.core.polyListComponentConversion( components, toVertex=1 ), fl=1 )
    mesh = vtxList[0].node()
    skinNodes = getNodeFromHistory( mesh, 'skinCluster' )
    if not skinNodes: return None
    
    influenceIndices = []
    for jnt in jnts:
        cons = jnt.wm.listConnections( s=0, d=1, type='skinCluster', p=1 )
        for con in cons:
            if not con.node() in skinNodes: continue
            influenceIndices.append( con.index() )
    
    fnSkinNode = OpenMaya.MFnDependencyNode(  )



def makeCloneObject( inputTarget, **options  ):
    
    target = pymel.core.ls( inputTarget )[0]
    
    op_cloneAttrName = 'iscloneObj'
    op_shapeOn       = False
    op_connectionOn  = False
    
    if options.has_key( 'cloneAttrName' ):
        op_cloneAttrName = options['cloneAttrName']
        cloneLabel = op_cloneAttrName
    if options.has_key( 'shapeOn' ):
        op_shapeOn = options['shapeOn']
    if options.has_key( 'connectionOn' ):
        op_connectionOn = options['connectionOn']
    cloneLabel = op_cloneAttrName

    targets = target.getAllParents()
    targets.reverse()
    targets.append( target )
    
    def getSourceConnection( src, trg ):
        src = pymel.core.ls( src )[0]
        trg = pymel.core.ls( trg )[0]
        cons = src.listConnections( s=1, d=0, p=1, c=1 )
    
        if not cons: return None
    
        for destCon, srcCon in cons:
            srcCon = srcCon.name()
            destCon = destCon.name().replace( src, trg )
            if cmds.nodeType( src ) == 'joint' and cmds.nodeType( trg ) =='transform':
                destCon = destCon.replace( 'jointOrient', 'rotate' )
            if not cmds.ls( destCon ): continue
            if not cmds.isConnected( srcCon, destCon ):
                cmds.connectAttr( srcCon, destCon, f=1 )

    targetCloneParent = None
    for cuTarget in targets:
        if not pymel.core.attributeQuery( op_cloneAttrName, node=cuTarget, ex=1 ):
            cuTarget.addAttr( op_cloneAttrName, at='message' )
        cloneConnection = cuTarget.attr( op_cloneAttrName ).listConnections(s=1, d=0 )
        if not cloneConnection:
            targetClone = pymel.core.createNode( 'transform', n= cuTarget.split( '|' )[-1]+ '_' + cloneLabel )
            targetClone.message >> cuTarget.attr( op_cloneAttrName )
            
            if op_shapeOn:
                cuTargetShape = cuTarget.getShape()
                if cuTargetShape:
                    oCuShape = getMObject( cuTargetShape )
                    oTargetClone = getMObject( targetClone )
                    OpenMaya.MFnMesh().copy( oCuShape, oTargetClone )
                    
            if op_connectionOn:
                getSourceConnection( cuTarget, targetClone )
                cuTargetShape    = cuTarget.getShape()
                targetCloneShape = targetClone.getShape()
                
                if cuTargetShape and targetCloneShape:
                    getSourceConnection( cuTargetShape, targetCloneShape )
        else:
            targetClone = cloneConnection[0]
        
        targetCloneParentExpected = targetClone.getParent()
        if targetCloneParent and targetCloneParentExpected != targetCloneParent:
            pymel.core.parent( targetClone, targetCloneParent )

        cuTargetPos = cuTarget.m.get()
        pymel.core.xform( targetClone, os=1, matrix=cuTargetPos )

        targetCloneParent = targetClone
    return targetCloneParent




def getAttrInfo( inputTargetAttr ):

    inputAttrInfo = sgModel.AttrInfo()

    targetAttr = pymel.core.ls( inputTargetAttr )[0]
    
    inputAttrInfo.shortName = targetAttr.shortName()
    inputAttrInfo.longName  = targetAttr.longName()
    inputAttrInfo.type    = targetAttr.type()
    inputAttrInfo.keyable = targetAttr.isKeyable()
    inputAttrInfo.channelBox = targetAttr.isInChannelBox()
    inputAttrInfo.lock = targetAttr.isLocked()
    inputAttrInfo.range = targetAttr.getRange()
    inputAttrInfo.defaultValue = pymel.core.attributeQuery( inputTargetAttr.attrName(), node=inputTargetAttr.node(), ld=1 )[0]
    
    if targetAttr.type() == 'enum':
        inputAttrInfo.enums = targetAttr.getEnums()
    return inputAttrInfo



def createAttrByAttrInfo( attrInfo, inputNode ):
    
    node = pymel.core.ls( inputNode )[0]
    try:
        addAttr( node, ln= attrInfo.longName, sn= attrInfo.shortName, at=attrInfo.type, en=":", dv=attrInfo.defaultValue )
    except:
        try:addAttr( node, ln= attrInfo.longName, sn= attrInfo.shortName, at=attrInfo.type, dv=attrInfo.defaultValue )
        except:pass
        
    nodeAttr = node.attr( attrInfo.longName )
    if nodeAttr.isnumeric():
        nodeAttr.setRange( attrInfo.range )
    if attrInfo.channelBox:
        nodeAttr.showInChannelBox(True)
    if attrInfo.keyable:
        nodeAttr.setKeyable(True)
    if attrInfo.lock:
        nodeAttr.set( lock=1 )




def renameSelOrder( sels ):

    firstName = sels[0].name()
    firstLocalName = firstName.split( '|' )[-1]
    
    digitIndices = []
    for i in range( len( firstLocalName ) ):
        if firstLocalName[i].isdigit():
            if len( digitIndices ):
                if i == digitIndices[-1]+1:
                    digitIndices.append( i )
                else:
                    digitIndices = [i]
            else:
                digitIndices.append( i )
    
    if digitIndices:
        sepNameFront = firstLocalName[:digitIndices[0]]
        sepNameBack  = firstLocalName[digitIndices[-1]+1:]
        
        numFormat = "%0" + str(len( digitIndices )) + "d"
        
        startNum = int( firstLocalName[digitIndices[0]:digitIndices[-1]+1] )
        fullNameFormat = sepNameFront + numFormat + sepNameBack
    else:
        startNum = 0
        fullNameFormat = firstName.split( '|' )[-1] + '%02d'
        
    for sel in sels:
        sel.rename( fullNameFormat % startNum )
        startNum += 1




def getDefaultAnimCurveUU( floats, values ):

    animCurve = pymel.core.createNode( 'animCurveUU' )
    for i in range( len( floats ) ):
        pymel.core.setKeyframe( animCurve, f=floats[i], v=values[i] )
    pymel.core.keyTangent( animCurve, itt='linear', ott='linear' )
    return animCurve



def getDefaultAnimCurveUA( floats, values ):

    animCurve = pymel.core.createNode( 'animCurveUA' )
    for i in range( len( floats ) ):
        pymel.core.setKeyframe( animCurve, f=floats[i], v=values[i] )
    pymel.core.keyTangent( animCurve, itt='linear', ott='linear' )
    return animCurve




def getMatrixAngleNode( inputTargetObj, directionIndex ):
    
    targetObj = pymel.core.ls( inputTargetObj )[0]
    
    composeMatrix = pymel.core.createNode( 'composeMatrix' )
    targetDirection = [[1,0,0], [0,1,0], [0,0,1]][directionIndex]
    composeMatrix.it.set( targetDirection )
    
    mm = pymel.core.createNode( 'multMatrix' )
    composeMatrix.outputMatrix >> mm.i[0]
    targetObj.m >> mm.i[1]
    dcmp = pymel.core.createNode( 'decomposeMatrix' )
    mm.o >> dcmp.imat
    
    abNode = pymel.core.createNode( 'angleBetween' )
    abNode.vector1.set( targetDirection )
    dcmp.ot >> abNode.vector2
    
    abCompose = pymel.core.createNode( 'composeMatrix' )
    abInverse = pymel.core.createNode( 'inverseMatrix' )
    abNode.euler >> abCompose.inputRotate
    abCompose.outputMatrix >> abInverse.inputMatrix
    
    mm = pymel.core.createNode( 'multMatrix' )
    dcmp = pymel.core.createNode( 'decomposeMatrix' )
    targetObj.m >> mm.i[0]
    abInverse.outputMatrix >> mm.i[1]
    mm.o >> dcmp.imat
    return dcmp
    



def makeSubCtl( inputCtl, inputBase ):
    
    ctl = pymel.core.ls( inputCtl )[0]
    base = pymel.core.ls( inputBase )[0]
    
    ctlP = ctl.getParent()
    duCtlP = pymel.core.duplicate( ctlP )[0]
    duCtl = duCtlP.listRelatives( c=1, f=1 )[0]
    
    ctl.rename( 'sub_' + ctl.nodeName() )
    
    keyAttrs = pymel.core.listAttr( duCtl, k=1 )
    keyAttrs += pymel.core.listAttr( duCtl, cb=1 )
    for attr in keyAttrs:
        duCtl.attr( attr ) >> ctl.attr( attr )
    
    keyAttrsP = pymel.core.listAttr( duCtlP, ud=1, k=1 )
    keyAttrs += pymel.core.listAttr( duCtlP, ud=1, cb=1 )
    for attr in keyAttrsP:
        ctlP.attr( attr ) >> duCtlP.attr( attr )
    
    mm = pymel.core.createNode( 'multMatrix' )
    dcmp = pymel.core.createNode( 'decomposeMatrix' )
    mm.matrixSum >> dcmp.imat
    ctlP.wm >> mm.i[0]
    base.wim >> mm.i[1]
    
    dcmp.ot >> duCtlP.t
    dcmp.outputRotate >> duCtlP.r
    dcmp.os >> duCtlP.s
    
    pymel.core.parent( duCtlP, w=1 )
    
    return duCtlP.name()



def addShapeToTarget( inputShapeNode, inputTransform ):
    
    shapeNode = pymel.core.ls( inputShapeNode )[0]
    transform = pymel.core.ls( inputTransform )[0]
    
    oTransform = getMObject( transform.name() )
    oShape = getMObject( shapeNode.name() )
    
    if shapeNode.nodeType() == 'mesh':
        oShape = OpenMaya.MFnMesh().copy( oShape, oTransform )
        fnMesh = OpenMaya.MFnMesh( oShape )
        srcAttr = shapeNode.outMesh
        dstAttr = pymel.core.ls( fnMesh.name() + '.inMesh' )[0]
    elif shapeNode.nodeType() == 'nurbsCurve':
        oShape = OpenMaya.MFnNurbsCurve().copy( oShape, oTransform )
        fnCurve = OpenMaya.MFnNurbsCurve( oShape )
        srcAttr = shapeNode.outMesh
        dstAttr = pymel.core.ls( fnCurve.name() + '.create' )[0]
    elif shapeNode.nodeType() == 'nurbsSurface':
        oShape = OpenMaya.MFnNurbsCurve().copy( oShape, oTransform )
        fnSurface = OpenMaya.MFnNurbsSurface( oShape )
        srcAttr = shapeNode.outMesh
        dstAttr = pymel.core.ls( fnSurface.name() + '.create' )[0]
    
    trGeo = pymel.core.createNode( 'transformGeometry' )
    srcAttr >> trGeo.inputGeometry
    shapeNode.wm >> trGeo.transform
    trGeo.outputGeometry >> dstAttr
    return dstAttr.node()
    
    



def combineMultiShapes( inputTargetGrps ):
    
    targetShapes = pymel.core.listRelatives( inputTargetGrps, c=1, ad=1, type='shape' )
    
    newTransform = pymel.core.createNode( 'transform' )
    for targetShape in targetShapes:
        addedShape = addShapeToTarget( targetShape, newTransform )
        print targetShape, addedShape
        copyShader( targetShape, addedShape )
    
    try:return pymel.core.polyUnite( newTransform, ch=0, mergeUVSets=1 )[0]
    except: return newTransform





def surfaceColorAtPoint( inputSurfaceNode, position ):
    
    surfaceNode = pymel.core.ls( inputSurfaceNode )[0]
    
    def getCloseNode( surfaceNode ):
        if surfaceNode.nodeType() == 'nurbsSurface':
            closeNode = cmds.listConnections( surfaceNode+'.worldSpace', type='closestPointOnSurface' )
            if closeNode: return pymel.core.ls( closeNode )[0]
            closeNode = cmds.createNode( 'closestPointOnSurface' )
            cmds.connectAttr( surfaceNode+'.worldSpace', closeNode+'.inputSurface' )
            return pymel.core.ls( closeNode )[0]
        elif surfaceNode.nodeType() == 'mesh':
            closeNode = surfaceNode.outMesh.listConnections( type='closestPointOnMesh' )
            if closeNode: return closeNode[0]
            closeNode = pymel.core.createNode( 'closestPointOnMesh' )
            surfaceNode.outMesh >> closeNode.inputMesh
            surfaceNode.worldMatrix >> closeNode.inputMatrix
            return closeNode
    
    closeNode = getCloseNode( surfaceNode )
    closeNode.inPosition.set( position )
    
    shadingEngines = getShadingEngines( surfaceNode )
    if not shadingEngines: return None
    
    shader = shadingEngines[0].surfaceShader.listConnections( s=1, d=0 )
    texture = shader[0].color.listConnections( s=1, d=0 )
    
    if not texture:
        try:return shader.color.get()
        except: return None
    
    uValue = cmds.getAttr( closeNode+'.parameterU' )
    vValue = cmds.getAttr( closeNode+'.parameterV' )
    
    return pymel.core.colorAtPoint( texture[0], u=uValue, v=vValue )
    


def getAverageColorFromSurface( inputSurface ):
    
    surfaceNode = pymel.core.ls( inputSurface )[0]
    
    if surfaceNode.nodeType() == 'transform':
        surfaceNode = getCurrentVisibleShapes( surfaceNode )[0]
    
    if surfaceNode.nodeType() == 'mesh':
        components = pymel.core.ls( surfaceNode + '.vtx[*]', fl=1 )
    elif surfaceNode.nodeType() == 'nurbsSurface':
        components = pymel.core.ls( surfaceNode + '.cv[*]', fl=1 )
    
    for component in components:
        pos = pymel.core.xform( component, q=1, ws=1, t=1 )
        colorValues = surfaceColorAtPoint( surfaceNode, pos )
        print component, colorValues
    
        
        
    
def createBoundingBox( inputTarget ):
    
    target = pymel.core.ls( inputTarget )[0]
    bb = pymel.core.exactWorldBoundingBox( target )    
    bbmin = bb[:3]
    bbmax = bb[-3:]
    points = [[] for i in range(8)]
    points[0] = [bbmin[0], bbmin[1], bbmax[2]]
    points[1] = [bbmax[0], bbmin[1], bbmax[2]]
    points[2] = [bbmin[0], bbmax[1], bbmax[2]]
    points[3] = [bbmax[0], bbmax[1], bbmax[2]]
    points[4] = [bbmin[0], bbmax[1], bbmin[2]]
    points[5] = [bbmax[0], bbmax[1], bbmin[2]]
    points[6] = [bbmin[0], bbmin[1], bbmin[2]]
    points[7] = [bbmax[0], bbmin[1], bbmin[2]]
    
    cube = pymel.core.polyCube( ch=1, o=1, cuv=4, n= target.shortName() + '_boundingBox' )[0]
    for i in range( 8 ):
        pymel.core.move( points[i][0], points[i][1], points[i][2], cube + '.vtx[%d]' % i )
    return cube


    
    