from maya import OpenMaya, OpenMayaUI, cmds
import pymel.core
import math, copy
import os
import math
from sgMaya import sgModel
from sgMaya.sgPlugin.sgCppPlug_modelingTool.format import BoundingBox



if not cmds.pluginInfo( 'matrixNodes', q=1, l=1 ):
    cmds.loadPlugin( 'matrixNodes' )



def makeFolder( pathName ):
    
    if os.path.exists( pathName ):return None
    os.makedirs( pathName )
    return pathName




def makeFile( filePath ):
    if os.path.exists( filePath ): return None
    filePath = filePath.replace( "\\", "/" )
    splits = filePath.split( '/' )
    folder = '/'.join( splits[:-1] )
    makeFolder( folder )
    f = open( filePath, "w" )
    f.close()



def getPymelObject( inputObj ):
    
    return pymel.core.ls( inputObj )[0]



def getVectorList():
    
    return [ [1,0,0], [0,1,0], [0,0,1], [-1,0,0], [0,-1,0], [0,0,-1] ]




def getOptionValue( keyName, returnValue, **options ):
    
    if options.has_key( keyName ):
        returnValue = options[ keyName ]
    return returnValue




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
    target = pymel.core.ls( inputTarget )[0]
    mObject = OpenMaya.MObject()
    selList = OpenMaya.MSelectionList()
    selList.add( target.name() )
    selList.getDependNode( 0, mObject )
    return mObject




def getDagPath( inputTarget ):
    target = pymel.core.ls( inputTarget )[0]
    dagPath = OpenMaya.MDagPath()
    selList = OpenMaya.MSelectionList()
    selList.add( target.name() )
    try:
        selList.getDagPath( 0, dagPath )
        return dagPath
    except:
        return None




def getDefaultMatrix():
    return [1,0,0,0, 0,1,0,0, 0,0,1,0 ,0,0,0,1]




def getDigitStrs( inputStr ):
    
    digitStr = ''
    digitStrs = []
    
    for i in range( len( inputStr ) ):
        if inputStr[i].isdigit():
            digitStr += inputStr[i]
        else:
            if digitStr:
                digitStrs.append( digitStr )
            digitStr = ''
    
    if digitStr:
        digitStrs.append( digitStr )
        
    return digitStrs



def listToMatrix( mtxList ):
    if type( mtxList ) == OpenMaya.MMatrix:
        return mtxList
    matrix = OpenMaya.MMatrix()
    if type( mtxList ) == list:
        resultMtxList = mtxList
    else:
        resultMtxList = []
        for i in range( 4 ):
            for j in range( 4 ):
                resultMtxList.append( mtxList[i][j] )
    
    OpenMaya.MScriptUtil.createMatrixFromList( resultMtxList, matrix )
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
    if type( mtxList[0] ) == list:
        resultMtxList = reduce( lambda x, y : x + y, mtxList )
    else:
        resultMtxList = mtxList
    OpenMaya.MScriptUtil.createMatrixFromList( resultMtxList, matrix )
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




def getMirrorMatrix( mtxValue ):

    if type( mtxValue ) == list:
        mtxList = mtxValue
    else:
        mtxList = matrixToList( mtxValue )
        
    mtxList[1]  *= -1
    mtxList[2]  *= -1
    mtxList[5]  *= -1
    mtxList[6]  *= -1
    mtxList[9]  *= -1
    mtxList[10]  *= -1
    mtxList[12] *= -1
    
    return listToMatrix( mtxList )




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




def matrixOutput( inputNode, **options ):
    
    node = pymel.core.ls( inputNode )[0]
    nodeType = node.nodeType()
    
    isLocal = False
    if options.has_key( 'local' ):
        isLocal = True
    
    if nodeType in ['composeMatrix', 'inverseMatrix']:
        return node.attr( 'outputMatrix' )
    elif nodeType in ['multMatrix', 'wtAddMatrix', 'addMatrix']:
        return node.attr( 'matrixSum' )
    elif nodeType in ['fourByFourMatrix']:
        return node.attr( 'output' )
    elif nodeType in ['transform', 'joint']:
        if isLocal:
            return node.attr( 'm' )
        else:
            return node.attr( 'wm' )




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




def makeChild( inputTarget, typ='null', **options ):
    
    if typ == 'joint':
        childObject = pymel.core.createNode( 'joint',**options )
    elif typ == 'locator':
        childObject = pymel.core.spaceLocator( **options )
    else:
        childObject = pymel.core.createNode( 'transform', **options )
    
    target = pymel.core.ls( inputTarget )[0]
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
    



def separateParentConnection( inputNode, attrName ):
    
    node = pymel.core.ls( inputNode )[0]
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
    if attrInfo.type in [ 'double' ]:
        nodeAttr.setRange( attrInfo.range )
    if attrInfo.channelBox:
        nodeAttr.showInChannelBox(True)
    if attrInfo.keyable:
        nodeAttr.setKeyable(True)
    if attrInfo.lock:
        nodeAttr.set( lock=1 )





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
    if srcAttr.type() in [ 'double' ]:
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
    
    pymel.core.xform( dst, ws=1, matrix= src.wm.get() )
    
    children = src.listRelatives( c=1, type='transform' )
    for child in children:
        child.setParent( dst )
    return dst




def makeCurveFromObjects( *sels, **options ):
    
    sels = list( sels )
    for i in range( len( sels ) ):
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
        cmds.addAttr( trNode, ln='parameter', min=0, max=10, dv=(eachParamValue * i + addParamValue)*10 )
        cmds.setAttr( trNode + '.parameter', e=1, k=1 )
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
        cmds.setAttr( multDouble + '.input2', 0.1 )
        cmds.connectAttr( trNode + '.parameter', multDouble + '.input1' )
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





def createNearestPointOnCurveObject( inputPointObj, inputCurve ):
    
    pointObj = pymel.core.ls( inputPointObj )[0]
    curve    = pymel.core.ls( inputCurve )[0]
    
    nearPointOnCurve = pymel.core.createNode( 'nearestPointOnCurve' )
    pointOnCurveInfo = pymel.core.createNode( 'pointOnCurveInfo' )

    curve.getShape().worldSpace >> nearPointOnCurve.inputCurve
    curve.getShape().worldSpace >> pointOnCurveInfo.inputCurve
    dcmp = getDecomposeMatrix( pointObj.wm )
    dcmp.ot >> nearPointOnCurve.inPosition
    nearPointOnCurve.parameter >> pointOnCurveInfo.parameter
    
    tangent = getMVector( pointOnCurveInfo.tangent.get() ) * getMMatrix( pointObj.wm.get() )
    dirIndex = getDirectionIndex( tangent )
    
    args = [ None for i in range( 4 ) ]
    upTrans = [0,0,0]
    upTrans[ ( dirIndex + 1 )%3 ] = 1
    vectorNodeUp = pymel.core.createNode( 'vectorProduct' )
    vectorNodeUp.input1.set( upTrans )
    vectorNodeUp.op.set( 3 )
    inputPointObj.wm >> vectorNodeUp.matrix
    
    vectorNodeCross = getCrossVectorNode( pointOnCurveInfo, vectorNodeUp )
    vectorNodeUp = getCrossVectorNode( vectorNodeCross, pointOnCurveInfo )
    
    args[ dirIndex % 3 ] = pointOnCurveInfo.tangent
    args[ (dirIndex+1) % 3 ] = vectorNodeUp.output
    args[ (dirIndex+2) % 3 ] = vectorNodeCross.output 
    args[ 3 ] = nearPointOnCurve.position
    
    newTr = pymel.core.createNode( 'transform' )
    fbf = getFbfMatrix( *args )
    dcmp = getLocalDecomposeMatrix( fbf.o, newTr.pim )
    dcmp.ot >> newTr.t
    dcmp.outputRotate >> newTr.r
    newTr.dh.set( 1 )
    return newTr




def createDetachCurve( pointObjects, curve ):
    
    if curve.nodeType() == 'transform':
        curveParent = curve.getParent()
    else:
        curveParent = curve.getParent().getParent()
    
    curveShape = getShape( curve )
    detachNode = pymel.core.createNode( 'detachCurve' )
    curveShape.local >> detachNode.inputCurve
    
    for i in range( len( pointObjects ) ):
        pointObject = pointObjects[i]
        
        detachPoint = getLocalDecomposeMatrix( pointObject.wm, curve.wim )
        nearPointCurveNode = pymel.core.createNode( 'nearestPointOnCurve' )
        
        curveShape.local >> nearPointCurveNode.inputCurve
        detachPoint.ot >> nearPointCurveNode.inPosition
        nearPointCurveNode.parameter >> detachNode.parameter[i]
    
    for i in range( len( pointObjects )+1 ):
        newCurveShape = pymel.core.createNode( 'nurbsCurve' )
        detachNode.outputCurve[i] >> newCurveShape.create
        newCurve = newCurveShape.getParent()
        newCurve.setParent( curveParent )





def setWire( targetGeos, wireCurve, wireCurveBase=None ):
    
    if not wireCurveBase:
        wireCurveBase = pymel.core.duplicate( wireCurve )[0]
    
    wire = pymel.core.deformer( targetGeos, type='wire' )[0]
    
    wireCurveShape = getShape( wireCurve )
    wireCurveShapeBase = getShape( wireCurveBase )
    
    wireCurveShape.worldSpace >> wire.deformedWire[0]
    wireCurveShapeBase.worldSpace >> wire.baseWire[0]
    wire.dropoffDistance[0].set( 1000 )
    
    return wire
    




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

    return [ pymel.core.ls( meshName + '.e[%d]' % i )[0] for i in orderedEdgeIndices ]





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
        srcCons = filter( lambda x : x.longName() in ['message', 'outColor'], engine.listConnections( s=1, d=0, p=1 ) )
        if not srcCons: continue
        pymel.core.hyperShade( objects = srcCons[0].node() )
        selObjs = pymel.core.ls( sl=1 )
        print "sel Objs : ", selObjs
        targetObjs = []
        for selObj in selObjs:
            if selObj.node() != firstShape: continue
            if selObj.find( '.' ) != -1:
                targetObjs.append( second+'.'+ selObj.split( '.' )[-1] )
            else:
                targetObjs.append( secondShape.name() )
        if not targetObjs: continue        
        for targetObj in targetObjs:
            cmds.sets( targetObj, e=1, forceElement=engine.name() )
            copyObjAndEngines.append( [targetObj, engine.name()] )
    return copyObjAndEngines



def getTranslateFromMatrix( mtxValue ):
    
    return matrixToList( getMMatrix( mtxValue ) )[12:-1]



def getRotateFromMatrix( mtxValue ):
    
    trMtx = OpenMaya.MTransformationMatrix( getMMatrix( mtxValue ) )
    rotVector = trMtx.eulerRotation().asVector()
    
    return [math.degrees(rotVector.x), math.degrees(rotVector.y), math.degrees(rotVector.z)]


def getScaleFromMatrix( mtxValue ):
    
    trMtx = OpenMaya.MTransformationMatrix( getMMatrix( mtxValue ) )
    
    util = OpenMaya.MScriptUtil()
    util.createFromDouble(0.0, 0.0, 0.0)
    ptr = util.asDoublePtr()
    trMtx.getScale(ptr, OpenMaya.MSpace.kObject)
    
    scaleX = util.getDoubleArrayItem(ptr, 0)
    scaleY = util.getDoubleArrayItem(ptr, 1)
    scaleZ = util.getDoubleArrayItem(ptr, 2)
    
    return [scaleX, scaleY, scaleZ]


def getShearFromMatrix( mtxValue ):
    
    trMtx = OpenMaya.MTransformationMatrix( getMMatrix( mtxValue ) )
    
    util = OpenMaya.MScriptUtil()
    util.createFromDouble(0.0, 0.0, 0.0)
    ptr = util.asDoublePtr()
    trMtx.getShear(ptr, OpenMaya.MSpace.kObject)
    
    shearXY = util.getDoubleArrayItem(ptr, 0)
    shearXZ = util.getDoubleArrayItem(ptr, 1)
    shearYZ = util.getDoubleArrayItem(ptr, 2)
    
    return [shearXY, shearXZ, shearYZ]


def getTransformFromMatrix( mtxValue ):
    
    trMtx = OpenMaya.MTransformationMatrix( getMMatrix( mtxValue ) )
    
    util = OpenMaya.MScriptUtil()
    util.createFromDouble(0.0, 0.0, 0.0)
    ptr = util.asDoublePtr()
    trans = trMtx.getTranslation( OpenMaya.MSpace.kWorld )
    
    rotVector = trMtx.eulerRotation().asVector()
    rotX, rotY, rotZ = [math.degrees(rotVector.x), math.degrees(rotVector.y), math.degrees(rotVector.z)]
    
    trMtx.getScale(ptr, OpenMaya.MSpace.kObject)
    scaleX = util.getDoubleArrayItem(ptr, 0)
    scaleY = util.getDoubleArrayItem(ptr, 1)
    scaleZ = util.getDoubleArrayItem(ptr, 2)
    
    trMtx.getShear(ptr, OpenMaya.MSpace.kObject)
    shearXY = util.getDoubleArrayItem(ptr, 0)
    shearXZ = util.getDoubleArrayItem(ptr, 1)
    shearYZ = util.getDoubleArrayItem(ptr, 2)
    
    return [trans.x, trans.y, trans.z, rotX, rotY, rotZ, scaleX, scaleY, scaleZ, shearXY, shearXZ, shearYZ]

    
def freezeJoint( inputJnt ):
    
    jnt = pymel.core.ls( inputJnt )[0]
    jntChildren = jnt.listRelatives( c=1, ad=1, type='joint' )
    if not jntChildren: jntChildren = []
    jntChildren.append( jnt )
    
    if jnt.r.listConnections( s=1, d=0 ): return
    if jnt.rx.listConnections( s=1, d=0 ): return
    if jnt.ry.listConnections( s=1, d=0 ): return
    if jnt.rz.listConnections( s=1, d=0 ): return
    
    for jnt in jntChildren:
        mtxJnt = pymel.core.xform( jnt, q=1, os=1, matrix=1 )
        rotValue = getRotateFromMatrix( mtxJnt )
        jnt.jo.set( rotValue )
        jnt.r.set( 0,0,0 )
        jnt.rotateAxis.set( 0,0,0 )



def blendTwoMatrixConnect( inputFirst, inputSecond, inputThird, **options ):
    
    connectTrans = True
    connectRotate = True
    connectScale = True
    connectShear = True
    
    if options.has_key( 'ct' ):
        connectTrans = options['ct']
    if options.has_key( 'cr' ):
        connectRotate = options['cr']
    if options.has_key( 'cs' ):
        connectScale = options['cs']
    if options.has_key( 'csh' ):
        connectShear = options['csh']
    
    first  = pymel.core.ls( inputFirst )[0]
    second = pymel.core.ls( inputSecond )[0]
    third  = pymel.core.ls( inputThird )[0]
    
    third.addAttr( 'blend', min=0, max=1, k=1, dv=0.5 )
    
    if options.has_key( 'local' ):
        wtAddMtx = pymel.core.createNode( 'wtAddMatrix' )
        dcmp = pymel.core.createNode( 'decomposeMatrix' )
        revNode = pymel.core.createNode( 'reverse' )
        third.blend >> revNode.inputX
        first.m >> wtAddMtx.i[0].m
        second.m >> wtAddMtx.i[1].m
        revNode.outputX >> wtAddMtx.i[0].w
        third.blend >> wtAddMtx.i[1].w
        wtAddMtx.matrixSum >> dcmp.imat
    else:
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
    if connectScale:
        dcmp.outputScale >> third.s
    if connectShear:
        dcmp.outputShear >> third.sh



def makeTranslateSquash( inputTarget ):
    
    target = pymel.core.ls( inputTarget )[0]
    
    txValue = cmds.getAttr( target + '.tx' )
    tyValue = cmds.getAttr( target + '.ty' )
    tzValue = cmds.getAttr( target + '.tz' )
    
    directionIndex = getDirectionIndex( [txValue, tyValue, tzValue ] )
    axis = ['x', 'y', 'z' ][directionIndex%3]
    
    if not pymel.core.attributeQuery( 'origDist', node=target, ex=1 ):
        target.addAttr( 'origDist' )
        target.origDist.set( cb=1 )
    if not pymel.core.attributeQuery( 'cuDist', node=target, ex=1 ):
        target.addAttr( 'cuDist' )
        target.cuDist.set( cb=1 )
    if not pymel.core.attributeQuery( 'squashValue', node=target, ex=1 ):
        target.addAttr( 'squashValue', k=1, min=0, max=1 )
    
    otherAxis = ['x','y','z']
    otherAxis.remove( axis )
    
    distNode = pymel.core.createNode( 'distanceBetween' )
    target.attr( 't' + axis.lower() ) >>  distNode.point1X
    
    target.origDist.set( distNode.distance.get() )
    distNode.distance >> target.cuDist
    
    multNode = pymel.core.createNode( 'multiplyDivide' )
    powNode = pymel.core.createNode( 'multiplyDivide' )
    multNode.op.set( 2 )
    powNode.op.set( 3 )
    target.origDist >> multNode.input1X
    target.cuDist >> multNode.input2X
    multNode.outputX >> powNode.input1X
    powNode.input2X.set( 0.5 )
    
    scaleNode = pymel.core.createNode( 'multiplyDivide' )
    scaleNode.op.set( 2 )
    target.cuDist >> scaleNode.input1X
    target.origDist >> scaleNode.input2X
    
    for attr in otherAxis:
        blendNode = pymel.core.createNode( 'blendTwoAttr' )
        blendNode.input[0].set( 1 )
        powNode.outputX >> blendNode.input[1]
        target.squashValue >> blendNode.ab
        blendNode.output >> target.attr( 's' + attr )
    
    scaleNode.outputX >> target.attr( 's' + axis )


    
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



def setAngleReverse( rigedNode ):
    srcList = getSourceList( rigedNode, [] )
    for src in srcList:
        src = pymel.core.ls( src )[0]
        if src.nodeType() == 'angleBetween':
            vector1Value = src.vector1.get()
            src.vector1.set( -vector1Value[0],-vector1Value[1],-vector1Value[2])

    

def addMiddleJoint( inputJnt, **options ):
    
    jnt = pymel.core.ls( inputJnt )[0]
    jntC = jnt.listRelatives( c=1, f=1 )[0]
    middleTransJnt = addMiddleTranslateJoint( jntC, **options )
    cmds.setAttr( middleTransJnt + '.transMult', 0 )
    
    compose = pymel.core.createNode( 'composeMatrix' )
    inverse = pymel.core.createNode( 'inverseMatrix' )
    addMtx  = pymel.core.createNode( 'addMatrix' )
    dcmp    = pymel.core.createNode( 'decomposeMatrix' )
    
    jnt.matrix >> inverse.inputMatrix
    compose.outputMatrix >> addMtx.matrixIn[0]
    inverse.outputMatrix >> addMtx.matrixIn[1]
    addMtx.matrixSum >> dcmp.imat
    
    dcmp.outputRotate >> middleTransJnt.rotate
    
    middleTransJnt.radius.set( cmds.getAttr( jnt + '.radius' ) * 1.5 )
    return pymel.core.ls( middleTransJnt )[0]




def getConstrainMatrix( inputFirst, inputTarget ):
    first = pymel.core.ls( inputFirst )[0]
    target = pymel.core.ls( inputTarget )[0]
    mm = pymel.core.createNode( 'multMatrix' )
    first.wm >> mm.i[0]
    target.pim >> mm.i[1]
    return mm



def insertMatrix( inputTargetAttr, inputMM ):

    targetAttr = pymel.core.ls( inputTargetAttr )[0]
    mm = pymel.core.ls( inputMM )[0]
    
    cons = mm.i.listConnections( s=1, d=0, p=1, c=1 )    
    srcAttrs = []
    dstIndices = []
    for i in range( len( cons ) ):
        origCon, srcCon = cons[i]
        srcAttrs.append( srcCon )
        dstIndices.append( origCon.index()+1 )
        srcCon // origCon
    
    targetAttr >> mm.i[0]
    for i in range( len( srcAttrs ) ):
        srcAttrs[i] >> mm.i[dstIndices[i]]



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
    dcmp = getDecomposeMatrix( mm.matrixSum )
    cmds.connectAttr( dcmp + '.os', target + '.s', f=1 )



def constrain_parent( first, target, **options ):
    
    mo = False
    if options.has_key( 'mo' ):
        mo = options['mo']
    
    mm = getConstrainMatrix( first, target )
    dcmp = getDecomposeMatrix( mm.matrixSum )
    
    if mo:
        localMtx = getMMatrix( target.wm ) * getMMatrix( first.wim )
        trValue = getTranslateFromMatrix( localMtx )
        rotValue = getRotateFromMatrix( localMtx )
        scaleValue = getScaleFromMatrix( localMtx )
        shearValue = getShearFromMatrix( localMtx )
        compose = pymel.core.createNode( 'composeMatrix' )
        compose.it.set( trValue )
        compose.ir.set( rotValue )
        compose.inputScale.set( scaleValue )
        compose.ish.set( shearValue )
        insertMatrix( compose.outputMatrix, mm )
    
    cmds.connectAttr( dcmp + '.ot',  target + '.t', f=1 )
    cmds.connectAttr( dcmp + '.or',  target + '.r', f=1 )




def constrain_all( first, target ):
    
    mm = getConstrainMatrix( first, target )
    dcmp = getDecomposeMatrix( mm.matrixSum )
    cmds.connectAttr( dcmp + '.ot',  target + '.t', f=1 )
    cmds.connectAttr( dcmp + '.or',  target + '.r', f=1 )
    cmds.connectAttr( dcmp + '.os',  target + '.s', f=1 )
    cmds.connectAttr( dcmp + '.osh',  target + '.sh', f=1 )



def getOffsetNode( target, base ):
    
    offsetNode = pymel.core.createNode( 'composeMatrix' )
    matValue = getMMatrix( target.wm ) * getMMatrix( base.wim )
    offsetNode.it.set( getTranslateFromMatrix( matValue ) )
    offsetNode.ir.set( getRotateFromMatrix( matValue ) )
    offsetNode.inputScale.set( getScaleFromMatrix( matValue ) )
    offsetNode.ish.set( getShearFromMatrix( matValue ) )
    return offsetNode



def constrain( *inputs, **options ):
    
    srcs   = inputs[:-1]
    target = inputs[-1]
    
    atToChild = False
    mo = False
    ct = True
    cr = True
    cs = False
    csh = False
    
    atToChild = getOptionValue( 'atToChild', atToChild, **options )
    mo = getOptionValue( 'mo', mo, **options )
    ct = getOptionValue( 'ct', ct, **options )
    cr = getOptionValue( 'cr', cr, **options )
    cs = getOptionValue( 'cs', cs, **options )
    csh = getOptionValue( 'csh', csh, **options )
    
    if len( srcs ) == 1:
        mm = getLocalMatrix( srcs[0].wm, target.pim )
        if mo: 
            offsetNode = getOffsetNode( target, srcs[0] )
            insertMatrix( offsetNode.outputMatrix, mm )
    else:
        addNode = pymel.core.createNode( 'plusMinusAverage' )
        conditionNode = pymel.core.createNode( 'condition' )
        addNode.output1D >> conditionNode.firstTerm
        addNode.output1D >> conditionNode.colorIfFalseR
        conditionNode.colorIfTrueR.set( 1 )
        
        wtAddMtx = pymel.core.createNode( 'wtAddMatrix' )
        mm = getLocalMatrix( wtAddMtx.matrixSum, target.pim )
        
        for i in range( len( srcs ) ):
            eachMM = pymel.core.createNode( 'multMatrix' )
            srcs[i].wm >> eachMM.i[0]
            if mo: 
                offsetNode = getOffsetNode( target, srcs[i] )
                insertMatrix( offsetNode.outputMatrix, eachMM )
                
            if atToChild:
                targetChild = target.listRelatives( c=1, type='transform' )
                if targetChild:
                    addAttr( targetChild[0], ln='blend_%d' % i, k=1, min=0, dv=1 )
                    blendAttr = targetChild[0].attr( 'blend_%d' % i )
                else:
                    addAttr( target, ln='blend_%d' % i, k=1, min=0, dv=1 )
                    blendAttr = target.attr( 'blend_%d' % i )
            else:
                addAttr( target, ln='blend_%d' % i, k=1, min=0, dv=1 )
                blendAttr = target.attr( 'blend_%d' % i )
            blendAttr >> addNode.input1D[i]
            divNode = pymel.core.createNode( 'multiplyDivide' ); divNode.op.set( 2 )
            blendAttr >> divNode.input1X
            conditionNode.outColorR >> divNode.input2X
            
            eachMM.o >> wtAddMtx.i[i].m
            divNode.outputX >> wtAddMtx.i[i].w
    resultDcmp = getDecomposeMatrix( mm.o )
    
    if ct  : resultDcmp.ot >> target.t
    if cr  : resultDcmp.outputRotate >> target.r
    if cs  : resultDcmp.os >> target.s
    if csh : resultDcmp.osh >> target.sh
            



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



def freezeByParent( inputTarget, evt=0 ):
    
    target = pymel.core.ls( inputTarget )[0]
    
    pTarget = target.getParent()
    if not pTarget: return None
    pymel.core.xform( pTarget, ws=1, matrix = target.wm.get() )
    try:cmds.xform( target, ws=1, matrix= pTarget.wm.get() )
    except:pass



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
    node = fullAttr.node().name()
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
    
    animCurve = cmds.createNode( animCurveType )
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
    
    tempTr = pymel.core.createNode( 'transform' )
    oTarget = getMObject( tempTr )
    
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

    setIndexColor( tempTr.getShape(), getIndexColor( shape ) )
    pymel.core.parent( tempTr.getShape(), transform, shape=1, add=1 )
    pymel.core.delete( tempTr )



def reverseShape( inputShape ):
    
    shape = pymel.core.ls( inputShape )[0]
    
    oShape = getMObject( shape )
    points = OpenMaya.MPointArray()
    
    if shape.type() == 'mesh':
        fnMesh = OpenMaya.MFnMesh( oShape )
        fnMesh.getPoints( points )
        for i in range( points.length() ):
            points.set( points[i] * -1, i )
        fnMesh.setPoints( points )
    elif shape.type() == 'nurbsCurve':
        fnCurve = OpenMaya.MFnNurbsCurve( oShape )
        fnCurve.getCVs( points )
        for i in range( points.length() ):
            points.set( points[i] * -1, i )
        fnCurve.setCVs( points )
    elif shape.type() == 'nurbsSurface':
        oSurface = getMObject( shape )
        fnNurbsSurface = OpenMaya.MFnNurbsSurface( oSurface )
        for i in range( points.length() ):
            points.set( points[i] * -1, i )
        fnNurbsSurface.getCVs( points )
    




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
    ioShape = targetTr.listRelatives( s=1 )[-1]
    return ioShape



def setPntsZero( targetMesh ):
    shapes = pymel.core.ls( targetMesh )[0].listRelatives( s=1 )
    for shape in shapes:
        if shape.attr( 'io' ).get(): continue
        if shape.nodeType() == 'mesh':
            fnMesh = OpenMaya.MFnMesh( getMObject( shape.name() ) )
            numVertices = fnMesh.numVertices()
            
            meshName = shape.name()
            for i in range( numVertices ):
                cmds.setAttr( meshName + '.pnts[%d]' % i, 0,0,0 )
        elif shape.nodeType() == 'nurbsCurve':
            fnNurbsCurve = OpenMaya.MFnNurbsCurve( getMObject(shape.name()) )
            numCVs = fnNurbsCurve.numCVs()
            
            curveName = shape.name()
            for i in range( numCVs ):
                cmds.setAttr( curveName + '.controlPoints[%d]' % i, 0,0,0 )



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
    
    crvShape.addAttr( 'shape_tx', dv=0 ); jnt.shape_tx.set( e=1, cb=1 )
    crvShape.addAttr( 'shape_ty', dv=0); jnt.shape_ty.set( e=1, cb=1 )
    crvShape.addAttr( 'shape_tz', dv=0); jnt.shape_tz.set( e=1, cb=1 )
    crvShape.addAttr( 'shape_rx', dv=0, at='doubleAngle' ); jnt.shape_rx.set( e=1, cb=1 )
    crvShape.addAttr( 'shape_ry', dv=0, at='doubleAngle' ); jnt.shape_ry.set( e=1, cb=1 )
    crvShape.addAttr( 'shape_rz', dv=0, at='doubleAngle' ); jnt.shape_rz.set( e=1, cb=1 )
    crvShape.addAttr( 'shape_sx', dv=1 ); jnt.shape_sx.set( e=1, cb=1 )
    crvShape.addAttr( 'shape_sy', dv=1 ); jnt.shape_sy.set( e=1, cb=1 )
    crvShape.addAttr( 'shape_sz', dv=1 ); jnt.shape_sz.set( e=1, cb=1 )
    crvShape.addAttr( 'scaleMult', dv=defaultScaleMult, min=0 ); jnt.scaleMult.set( e=1, cb=1 )
    composeMatrix = pymel.core.createNode( 'composeMatrix' )
    composeMatrix2 = pymel.core.createNode( 'composeMatrix' )
    multMatrix = pymel.core.createNode( 'multMatrix' )
    composeMatrix.outputMatrix >> multMatrix.i[0]
    composeMatrix2.outputMatrix >> multMatrix.i[1]
    crvShape.shape_tx >> composeMatrix.inputTranslateX
    crvShape.shape_ty >> composeMatrix.inputTranslateY
    crvShape.shape_tz >> composeMatrix.inputTranslateZ
    crvShape.shape_rx >> composeMatrix.inputRotateX
    crvShape.shape_ry >> composeMatrix.inputRotateY
    crvShape.shape_rz >> composeMatrix.inputRotateZ
    crvShape.shape_sx >> composeMatrix.inputScaleX
    crvShape.shape_sy >> composeMatrix.inputScaleY
    crvShape.shape_sz >> composeMatrix.inputScaleZ
    crvShape.scaleMult >> composeMatrix2.inputScaleX
    crvShape.scaleMult >> composeMatrix2.inputScaleY
    crvShape.scaleMult >> composeMatrix2.inputScaleZ
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
        cmds.select( geoShape.name() )
        cmds.DeleteHistory()
        origShape = addIOShape( geoShape )
        
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





def addFixedWeightJointToVertices( inputVertices ):
    
    vertices = pymel.core.ls( inputVertices, fl=1 )
    
    mesh = vertices[0].node()
    for vertex in vertices:
        if vertex.node() != mesh:
            cmds.error( "There is multiple mesh vertices" )
    
    skinNode = getNodeFromHistory( mesh, 'skinCluster' )
    if not skinNode: return None
    skinNode = skinNode[0]
    
    maxIndex = max( [ skinNode.matrix[i].index() for i in range( skinNode.matrix.numElements() ) ] )
    nextIndex = maxIndex + 1
    
    bbc = getCenter( vertices )
    jnt = pymel.core.createNode( 'joint' )
    jnt.t.set( bbc )
    
    jnt.wm >> skinNode.matrix[ nextIndex ]
    skinNode.bindPreMatrix[ nextIndex ].set( jnt.wim.get() )
    
    for vertex in vertices:
        weightPlug = getWeightPlugFromSkinedVertex( vertex )
        for i in range( len( weightPlug ) ):
            pymel.core.removeMultiInstance( weightPlug[i] )
        weightPlug[0].array()[ nextIndex ].set( 1 )
    return jnt




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

    


def edgeLoopWeightHammer( inputSelEdges ):
    
    selEdges = pymel.core.ls( inputSelEdges, sl=1, fl=1 )
    
    for edge in selEdges:
        vertices = pymel.core.ls( pymel.core.polyListComponentConversion( edge, tv=1 ), fl=1 )
        vtxIndex = int( vertices[0].split( '[' )[-1].replace( ']', '' ) )
        
        meshShape = edge.node()
        skinNodes = getNodeFromHistory( meshShape, 'skinCluster' )
        if not skinNodes: continue
        
        fnSkinNode = OpenMaya.MFnDependencyNode( getMObject( skinNodes[0] ) )
        plugWeightList = fnSkinNode.findPlug('weightList')
        weightsPlug = plugWeightList[vtxIndex].child(0)
        
        indicesAndValues = []
        for i in range( weightsPlug.numElements() ):
            influenceIndex = weightsPlug[i].logicalIndex()
            value = weightsPlug[i].asFloat()
            indicesAndValues.append( [influenceIndex,value] )
        
        pymel.core.select( edge )
        cmds.SelectEdgeLoopSp()
        edges = pymel.core.ls( sl=1, fl=1 )
        vertices = pymel.core.ls( pymel.core.polyListComponentConversion( edges, tv=1 ), fl=1 )
        for vtx in vertices:
            vtxIndex = vtx.index()
            eachWeightsPlug = plugWeightList[ vtxIndex ].child(0)
            for i in range( eachWeightsPlug.numElements() ):
                cmds.removeMultiInstance( eachWeightsPlug[0].name() )
            for influenceIndex, value in indicesAndValues:
                cmds.setAttr( skinNodes[0] + '.weightList[%d].weights[%d]' % (vtxIndex, influenceIndex), value )
    
    pymel.core.select( selEdges )




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
    



def edgeStartAndEndWeightHammer( inputEdges, power=1.0 ):
    
    inputEdges = [ pymel.core.ls( inputEdge )[0] for inputEdge in inputEdges ]
    inputEdgeIndices = [ inputEdge.index() for inputEdge in inputEdges ]
    
    startEdge = None
    for inputEdge in inputEdges:
        indices = [ index for index in inputEdge.connectedEdges().indices() if index in inputEdgeIndices ]
        if len( indices ) != 1: continue
        startEdge = inputEdge
        break

    orderedEdges = [ startEdge ]
    for i in range( len( inputEdges )-1 ):
        connectedEdges = orderedEdges[-1].connectedEdges()
        for connectedEdge in connectedEdges:
            if not connectedEdge in inputEdges: continue
            if connectedEdge in orderedEdges: continue
            orderedEdges.append( connectedEdge )
            break
    
    orderedInputIndices = [ orderedEdge.index() for orderedEdge in orderedEdges ]
    
    mesh = inputEdges[0].node()
    srcMeshs = getNodeFromHistory( mesh, 'mesh' )
    skinNode = getNodeFromHistory( mesh, 'skinCluster' )[0]
    
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
    
    for startPlug in startPlugs:
        print "start plug : ", startPlug, startPlug.get()
    
    for endPlug in endPlugs:
        print "end plug : ", endPlug, endPlug.get()
    
    def getPoweredWeight( weightValue, powerValue ):
        value = weightValue * 2 -1
        negativeMult = 1.0
        if value < 0: negativeMult = -1.0
        value *= negativeMult
        poweredValue = float( value ) ** 1.0/powerValue
        return (poweredValue*negativeMult+ 1)/2
        
    
    for i in range( 1, len( orderedVtxIndices )-1 ):
        currentDist = reduce( lambda x, y : x+y, distList[:i] )
        targetVtx = mesh + '.vtx[%d]' % orderedVtxIndices[i]
        targetPlugs = getWeightPlugFromSkinedVertex(targetVtx)
        weightValue = currentDist/allDist
        revValue    = 1.0 - weightValue
        
        poweredWeightValue = getPoweredWeight( weightValue, power )
        poweredRevValue = getPoweredWeight( revValue, power )
        
        weightValue = poweredWeightValue/(poweredWeightValue+poweredRevValue)
        revValue = poweredRevValue/(poweredWeightValue+poweredRevValue)
        
        targetPlugArray = targetPlugs[0].array()
        
        for element in targetPlugArray.elements():
            pymel.core.removeMultiInstance( skinNode + '.' + element )
        
        existIndices = []
        for startPlug in startPlugs:
            plugIndex = startPlug.index()
            targetPlugArray[plugIndex].set( revValue * startPlug.get() )
            existIndices.append( plugIndex )
        
        for endPlug in endPlugs:
            plugIndex = endPlug.index()
            if plugIndex in existIndices:
                targetPlugArray[plugIndex].set( targetPlugArray[plugIndex].get() + weightValue * endPlug.get() )
            else:
                targetPlugArray[plugIndex].set( weightValue * endPlug.get() )
    
    pymel.core.skinCluster( skinNode, e=1, nw=1 )

        


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





def attachJointLineToCurve( topJoint, curve ):
    
    childrenJnts = topJoint.listRelatives( c=1, ad=1 )
    childrenJnts.append( topJoint )    
    childrenJnts.reverse()    
    topJnt = childrenJnts[0]
    endJnt = childrenJnts[-1]
    pymel.core.ikHandle( sj=topJnt, ee=endJnt, curve=curve, sol='ikSplineSolver', ccv=False, pcv=False )

    curveInfos = []
    for i in range( len( childrenJnts ) ):
        paramValue = getClosestParamAtPoint( childrenJnts[i], curve )
        curveInfo = pymel.core.createNode( 'pointOnCurveInfo' )
        curveShape = curve.getShape()
        curveShape.local >> curveInfo.inputCurve
        curveInfo.parameter.set( paramValue )
        curveInfos.append( curveInfo )
    
    for i in range( len( childrenJnts )-1 ):
        distNode = pymel.core.createNode( 'distanceBetween' )
        curveInfos[i].position >> distNode.point1
        curveInfos[i+1].position >> distNode.point2
        directionIndex = getDirectionIndex( childrenJnts[i+1].t.get() )
        attr = ['tx', 'ty', 'tz'][ directionIndex % 3 ]
        if directionIndex >= 3:
            multMinus = pymel.core.createNode( 'multDoubleLinear' )
            distNode.distance >> multMinus.input1
            multMinus.input2.set( -1 )
            multMinus.output >> childrenJnts[i+1].attr( attr )
        else:
            distNode.distance >> childrenJnts[i+1].attr( attr )



    

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



def getEachObjectComponents( targets ):
    
    pymel.core.select( targets )
    
    mSelList = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList( mSelList )
    
    def getNameFromDagPath( dagPath ):
        fnNode = OpenMaya.MFnDagNode( dagPath )
        return fnNode.partialPathName()
    
    returnTargets = []
    for i in range( mSelList.length() ):
        mDagPath = OpenMaya.MDagPath()
        mObject  = OpenMaya.MObject()
        mSelList.getDagPath( i, mDagPath, mObject )

        mIntArrU = OpenMaya.MIntArray()
        mIntArrV = OpenMaya.MIntArray()
        mIntArrW = OpenMaya.MIntArray()
        
        dagName = getNameFromDagPath( mDagPath )
        
        compStringList = []
        if not mObject.isNull():
            if mDagPath.apiType() == OpenMaya.MFn.kNurbsCurve:
                component = OpenMaya.MFnSingleIndexedComponent( mObject )
                component.getElements( mIntArrU )
                for i in range( mIntArrU.length() ):
                    compName = '%s.cv[%d]' %( dagName, mIntArrU[i] )
                    compStringList.append( compName )
            elif mDagPath.apiType() == OpenMaya.MFn.kNurbsSurface:
                component = OpenMaya.MFnDoubleIndexedComponent( mObject )
                component.getElements( mIntArrU, mIntArrV )
                fnSurface = OpenMaya.MFnNurbsSurface( mDagPath )
                for i in range( mIntArrV.length() ):
                    for j in range( mIntArrU.length() ):
                        compName = '%s.cv[%d]' %( dagName, mIntArrU[j] + mIntArrV[i]*fnSurface.numCVsInV() )
                        compStringList.append( compName ) 
            elif mDagPath.apiType() == OpenMaya.MFn.kLattice:
                component = OpenMaya.MFnTripleIndexedComponent( mObject )
                component.getElements( mIntArrU, mIntArrV, mIntArrW )
            elif mObject.apiType() == OpenMaya.MFn.kMeshVertComponent:
                component = OpenMaya.MFnSingleIndexedComponent( mObject )
                component.getElements( mIntArrU )
                for i in range( mIntArrU.length() ):
                    compName = '%s.vtx[%d]' %( dagName, mIntArrU[i] )
                    compStringList.append( compName )
            elif mObject.apiType() == OpenMaya.MFn.kMeshEdgeComponent:
                component = OpenMaya.MFnSingleIndexedComponent( mObject )
                component.getElements( mIntArrU )
                for i in range( mIntArrU.length() ):
                    compName = '%s.e[%d]' %( dagName, mIntArrU[i] )
                    compStringList.append( compName )
            elif mObject.apiType() == OpenMaya.MFn.kMeshPolygonComponent:
                component = OpenMaya.MFnSingleIndexedComponent( mObject )
                component.getElements( mIntArrU )
                for i in range( mIntArrU.length() ):
                    compName = '%s.f[%d]' %( dagName, mIntArrU[i] )
                    compStringList.append( compName )
        returnTargets.append( compStringList )
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
    trNodes = []
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
        trNodes.append( trNode )
    return trNodes




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
    
    return curve



def getDistanceNodeBetwwenTwoObjs( inputFirst, inputSecond ):
    
    first = pymel.core.ls( inputFirst )[0]
    second = pymel.core.ls( inputSecond )[0]
    
    distNode = pymel.core.createNode( 'distanceBetween' )
    
    first.wm >> distNode.attr( 'inMatrix1' )
    second.wm >> distNode.attr( 'inMatrix2' )
    
    return distNode
    



def getDivideNodeFromTwoNodeOutput( inputNumeratorNode, inputDenominatorNode ):
    
    numeratorNode = pymel.core.ls( inputNumeratorNode )[0]
    denominatorNode = pymel.core.ls( inputDenominatorNode )[0]
    
    divNode = pymel.core.createNode( 'multiplyDivide' )
    divNode.op.set( 2 )
    
    scalarOutput( numeratorNode ) >> divNode.input1X
    scalarOutput( denominatorNode ) >> divNode.input2X
    return divNode




def getSortedEdgesInSameRing( inputEdges ):
    
    edges = [ pymel.core.ls( inputEdge )[0].name() for inputEdge in inputEdges ]
    edgeRings = [ i.name() for i in getOrderedEdgeRings( edges[0] ) ]
    
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
    
    def getDistanceNodeFromTwoObjs( target1, target2 ):
    
        pmTarget1 = pymel.core.ls( target1 )[0]
        pmTarget2 = pymel.core.ls( target2 )[0]
        
        distNode = pymel.core.createNode( 'distanceBetween' )
        pmTarget1.t >> distNode.point1
        pmTarget2.t >> distNode.point2
        
        distNode.addAttr( 'origDist', dv= distNode.distance.get() )
        
        return distNode.name(), 'origDist'
    
    loopCurves = []
        
    for edge in edges:
        loopCurve = createLoopCurve( edge )
        loopCurves.append( loopCurve )
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
        tangentNode = cmds.tangentConstraint( curve.name(), jntCenters[i], aim=[0,1,0], u=[1,0,0], wut='vector' )[0]
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
    
    cmds.parent( loopCurves, centers, jntCenters, curve.name(), allPoints, baseTransform )
    
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





def getOutputGeometryAttr( inputGeo ):
    
    geoShape = getShape( inputGeo )
    if geoShape.nodeType() == 'mesh':
        return geoShape.attr( 'outMesh' )
    elif geoShape.nodeType() in ['nurbsCurve', 'nurbsSurface']:
        return geoShape.attr( 'local' )


def getInputGeometryAttr( inputGeo ):
    
    geoShape = getShape( inputGeo )
    if geoShape.nodeType() == 'mesh':
        return geoShape.attr( 'inMesh' )
    elif geoShape.nodeType() in ['nurbsCurve', 'nurbsSurface']:
        return geoShape.attr( 'create' )




def makeCloneObject( inputTarget, **options  ):
    
    target = pymel.core.ls( inputTarget )[0]
    
    op_cloneAttrName = 'iscloneObj'
    op_shapeOn       = False
    op_connectionOn  = False
    op_searchSymmetry = False
    
    if options.has_key( 'cloneAttrName' ):
        op_cloneAttrName = options['cloneAttrName']
        cloneLabel = op_cloneAttrName
    if options.has_key( 'shapeOn' ):
        op_shapeOn = options['shapeOn']
    if options.has_key( 'connectionOn' ):
        op_connectionOn = options['connectionOn']
    if options.has_key( 'searchSymmetry' ):
        op_searchSymmetry = options['searchSymmetry']
    cloneLabel = op_cloneAttrName

    targets = target.getAllParents()
    targets.insert( 0, target )
    
    def getSourceConnection( src, trg ):
        src = pymel.core.ls( src )[0]
        trg = pymel.core.ls( trg )[0]
        cons = src.listConnections( s=1, d=0, p=1, c=1 )
    
        if not cons: return None
    
        for destCon, srcCon in cons:
            srcCon = srcCon.name()
            destCon = destCon.name().replace( src.name(), trg.name() )
            if cmds.nodeType( src ) == 'joint' and cmds.nodeType( trg ) =='transform':
                destCon = destCon.replace( 'jointOrient', 'rotate' )
            if not cmds.ls( destCon ): continue
            if not cmds.isConnected( srcCon, destCon ):
                cmds.connectAttr( srcCon, destCon, f=1 )

    targetClones = []
    for cuTarget in targets:
        if not pymel.core.attributeQuery( op_cloneAttrName, node=cuTarget, ex=1 ):
            cuTarget.addAttr( op_cloneAttrName, at='message' )
        cloneConnection = cuTarget.attr( op_cloneAttrName ).listConnections(s=1, d=0 )
        symmetryTargetStr = None
        if op_searchSymmetry:
            symmetryTargetStr = getOtherSideStr(cuTarget.name())
            if pymel.core.objExists( symmetryTargetStr ):
                cloneConnection = [pymel.core.ls( symmetryTargetStr )[0]]
        if not cloneConnection:
            targetClone = pymel.core.createNode( cuTarget.nodeType(), n= cuTarget.split( '|' )[-1]+ '_' + cloneLabel )
            targetClone.message >> cuTarget.attr( op_cloneAttrName )
            
            if op_shapeOn:
                cuTargetShape = cuTarget.getShape()
                if cuTargetShape:
                    oCuShape = getMObject( cuTargetShape )
                    oTargetClone = getMObject( targetClone )
                    if cuTargetShape.nodeType() == 'mesh':
                        OpenMaya.MFnMesh().copy( oCuShape, oTargetClone )
                    elif cuTargetShape.nodeType() == 'nurbsCurve':
                        OpenMaya.MFnNurbsCurve().copy( oCuShape, oTargetClone )
                    
            if op_connectionOn:
                getSourceConnection( cuTarget, targetClone )
                cuTargetShape    = cuTarget.getShape()
                targetCloneShape = targetClone.getShape()
                
                if cuTargetShape and targetCloneShape:
                    getOutputGeometryAttr( cuTargetShape ) >> getInputGeometryAttr( targetCloneShape )
                    copyShader( cuTargetShape, targetCloneShape )
                
                if not pymel.core.isConnected( cuTarget.t, targetClone.t ):
                    cuTarget.t >> targetClone.t
                if not pymel.core.isConnected( cuTarget.r, targetClone.r ):
                    cuTarget.r >> targetClone.r
                if not pymel.core.isConnected( cuTarget.s, targetClone.s ):
                    cuTarget.s >> targetClone.s
                if not pymel.core.isConnected( cuTarget.sh, targetClone.sh ):
                    cuTarget.sh >> targetClone.sh

            udAttrs = cmds.listAttr( cuTarget.name(), ud=1 )
            for attr in udAttrs:
                try:copyAttribute( cuTarget, targetClone, attr )
                except:pass
            targetClones.append( targetClone )
        else:
            targetClone = cloneConnection[0]
            targetClones.append( targetClone )
            break
    
    cuTargets = targets[:len( targetClones )]
    for i in range( len( targetClones ) ):
        if len( targetClones ) > i+1:
            targetClones[i].setParent( targetClones[i+1] )
        
        selRp  = pymel.core.xform( cuTargets[i], q=1, os=1, rp=1 )
        selSp  = pymel.core.xform( cuTargets[i], q=1, os=1, sp=1 )
        pymel.core.xform( targetClones[i], os=1, rp=selRp )
        pymel.core.xform( targetClones[i], os=1, sp=selSp )
        
        
        if not targetClones[i].t.listConnections(): targetClones[i].t.set( cuTargets[i].t.get() )
        if not targetClones[i].r.listConnections(): targetClones[i].r.set( cuTargets[i].r.get() )
        if not targetClones[i].s.listConnections(): targetClones[i].s.set( cuTargets[i].s.get() )
        if not targetClones[i].sh.listConnections(): targetClones[i].sh.set( cuTargets[i].sh.get() )
        if not targetClones[i].rotatePivot.listConnections(): targetClones[i].rotatePivot.set( cuTargets[i].rotatePivot.get() )
        if not targetClones[i].scalePivot.listConnections(): targetClones[i].scalePivot.set( cuTargets[i].scalePivot.get() )
        if not targetClones[i].rotatePivotTranslate.listConnections(): targetClones[i].rotatePivotTranslate.set( cuTargets[i].rotatePivotTranslate.get() )
        if not targetClones[i].scalePivotTranslate.listConnections(): targetClones[i].scalePivotTranslate.set( cuTargets[i].scalePivotTranslate.get() )
    
    return targetClones[0]



def makeCloneObjectGroup( inputGroup, **options  ):
    
    childTransforms = pymel.core.ls( inputGroup )[0].listRelatives( c=1, ad=1, type='transform' )
    childTransforms.append( inputGroup )
    
    for tr in childTransforms:
        cloneTr = makeCloneObject( tr, **options )
    
    return cloneTr




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





def getOutputMatrixAttribute( node ):
    targetAttr = None
    if node.nodeType() == 'transform':
        targetAttr = node.worldMatrix
    elif node.nodeType() in ['multMatrix', 'wtAddMatrix', 'addMatrix']:
        targetAttr = node.matrixSum
    elif node.nodeType() in ['composeMatrix', 'transposeMatrix', 'inverseMatrix']:
        targetAttr = node.outputMatrix
    
    return targetAttr




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
    




def makeSubCtl( inputCtl, cloneName = 'subCtl' ):
    
    ctl = pymel.core.ls( inputCtl )[0]
    cloneCtl = makeCloneObject( ctl, cloneAttrName=cloneName, shapeOn=1 )
    cloneCtl.rename( ctl.shortName() )
    ctl.rename( 'sub_' + ctl.shortName().split( '|' )[-1] )
    
    udAttrs = cmds.listAttr( ctl.name(), ud=1 )
    keyAttrs = cmds.listAttr( ctl.name(), k=1 )
    
    for udAttr in udAttrs:
        try:copyAttribute( ctl, cloneCtl, udAttr )
        except:pass
        
    connectAttrs = list( set( udAttrs + keyAttrs ) )
    for attr in connectAttrs:
        try:cloneCtl.attr( attr ) >> ctl.attr( attr )
        except:pass
    
    ctlP = ctl.getParent()
    cloneCtlP = cloneCtl.getParent()
    
    ctlP.t >> cloneCtlP.t
    ctlP.r >> cloneCtlP.r
    ctlP.s >> cloneCtlP.s
    ctlP.v >> cloneCtlP.v
    
    setIndexColor( cloneCtl, getIndexColor( ctl ) )
    setIndexColor( cloneCtl.getShape(), getIndexColor( ctl.getShape() ) )
    
    



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
        srcAttr = shapeNode.local
        dstAttr = pymel.core.ls( fnCurve.name() + '.create' )[0]
    elif shapeNode.nodeType() == 'nurbsSurface':
        oShape = OpenMaya.MFnNurbsCurve().copy( oShape, oTransform )
        fnSurface = OpenMaya.MFnNurbsSurface( oShape )
        srcAttr = shapeNode.local
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





def setAttrCurrentAsDefault( inputTarget ):
    
    target = pymel.core.ls( inputTarget )[0]
    attrs  = pymel.core.listAttr( target, ud=1, k=1 )
    if not attrs: attrs = []
    cbAttrs = pymel.core.listAttr( target, ud=1, cb=1 )
    if not cbAttrs: cbAttrs = []
    attrs += cbAttrs
    
    for attr in attrs:
        value = target.attr( attr ).get()
        cmds.addAttr( target + '.' + attr, e=1, dv=value )





def getVerticesFromEdge( fnMesh, edgeNum ):

    util = OpenMaya.MScriptUtil()
    util.createFromList( [0,0], 2 )
    int2Ptr = util.asInt2Ptr()
    fnMesh.getEdgeVertices( edgeNum, int2Ptr )
    first = OpenMaya.MScriptUtil.getInt2ArrayItem( int2Ptr, 0, 0 )
    second = OpenMaya.MScriptUtil.getInt2ArrayItem( int2Ptr, 0, 1 )
    return first, second





def getConnectedVertices( inputVtx ):
    vtx = pymel.core.ls( inputVtx )[0]
    mesh = vtx.node()
    vtxIndex = vtx.index()
    itMeshVtx = OpenMaya.MItMeshVertex( getDagPath(mesh))
    
    util = OpenMaya.MScriptUtil()
    util.createFromInt(0)
    ptrInt = util.asIntPtr()
    itMeshVtx.setIndex( vtxIndex, ptrInt )
    indices = OpenMaya.MIntArray()
    itMeshVtx.getConnectedVertices( indices )
    return [ pymel.core.ls( mesh + '.vtx[%d]' % indices[i] )[0] for i in range( indices.length() ) ]
    




def getPointOnCurveFromMeshVertex( inputVtx ):
    vtx = pymel.core.ls( inputVtx )[0]
    
    mesh = vtx.node()
    vtxIndex = vtx.index()
    
    targetEdgeCurveNode = None
    if pymel.core.attributeQuery( 'curveInfo_%d' % vtxIndex, node=mesh, ex=1 ):
        cons = mesh.attr('curveInfo_%d' % vtxIndex).listConnections( s=1, d=0 )
        if cons: return cons[0]
    
    paramValue = 0.0
    if pymel.core.attributeQuery( 'edgeToCurve_%d' % vtxIndex, node=mesh, ex=1 ):
        edgeCurveNodes = mesh.attr('edgeToCurve_%d' % vtxIndex).listConnections( s=1, d=0, type='polyEdgeToCurve' )
        for edgeCurveNode in edgeCurveNodes:
            fnNode = OpenMaya.MFnDependencyNode( getMObject(edgeCurveNode.name()))
            plugInputComponts = fnNode.findPlug( 'inputComponents' )
            compData = OpenMaya.MFnComponentListData( plugInputComponts.asMObject() )
            for i in range( compData.length() ):
                singleComp = OpenMaya.MFnSingleIndexedComponent( compData[i] )
                indices = OpenMaya.MIntArray()
                singleComp.getElements( indices )
                for j in range( indices.length() ):
                    if vtxIndex == indices[j]:
                        targetEdgeCurveNode = edgeCurveNode
                        if i == 1: paramValue = 1.0
                if targetEdgeCurveNode: break
    
    if not targetEdgeCurveNode:
        dagMesh = getDagPath( mesh )
        itMeshVtx = OpenMaya.MItMeshVertex( dagMesh )
        prevIndex = getIntPtr()
        itMeshVtx.setIndex( vtxIndex, prevIndex )
        edgeIndices = OpenMaya.MIntArray()
        itMeshVtx.getConnectedEdges( edgeIndices )
        createdTransform, polyToCurveNode = pymel.core.polyToCurve( mesh + '.e[%d]' % edgeIndices[0], form=2, degree=1 )
        targetEdgeCurveNode = pymel.core.ls( polyToCurveNode )[0]
        
        fnNode = OpenMaya.MFnDependencyNode( getMObject(targetEdgeCurveNode.name()))
        plugInputComponts = fnNode.findPlug( 'inputComponents' )
        compData = OpenMaya.MFnComponentListData( plugInputComponts.asMObject() )

        for i in range( compData.length() ):
            singleComp = OpenMaya.MFnSingleIndexedComponent( compData[i] )
            indices = OpenMaya.MIntArray()
            singleComp.getElements( indices )
            if indices[0] == vtxIndex and i == 1:
                paramValue = 1.0
            addAttr( mesh, ln='edgeToCurve_%d' % indices[0], at='message' )
            targetEdgeCurveNode.message >> mesh.attr( 'edgeToCurve_%d' % indices[0] )
            
    
    curveInfo = pymel.core.createNode( 'pointOnCurveInfo' )
    targetEdgeCurveNode.outputcurve >> curveInfo.inputCurve
    curveInfo.parameter.set( paramValue )
    try:pymel.core.delete( createdTransform )
    except:pass
    
    addAttr( mesh, ln='curveInfo_%d' % vtxIndex, at='message' )
    curveInfo.message >> mesh.attr('curveInfo_%d' % vtxIndex)
    
    return curveInfo
    



def getPivotLocalMatrix( inputTarget ):
    
    target = pymel.core.ls( inputTarget )[0]
    rp = pymel.core.getAttr( target + '.rotatePivot' )
    rpMtx = listToMatrix( [1,0,0,0, 0,1,0,0, 0,0,1,0 , rp[0], rp[1], rp[2], 1 ] )
    
    return rpMtx



def getPivotWorldMatrix( inputTarget ):
    
    target = pymel.core.ls( inputTarget )[0]
    rp = pymel.core.getAttr( target + '.rotatePivot' )
    rpMtx = listToMatrix( [1,0,0,0, 0,1,0,0, 0,0,1,0 , rp[0], rp[1], rp[2], 1 ] )
    mtx = listToMatrix( cmds.getAttr( target + '.wm' ) )
    
    return rpMtx * mtx





def getWorldPosition( inputTarget ):
    
    pos = pymel.core.xform( inputTarget, q=1, ws=1, t=1 )
    return OpenMaya.MPoint( *pos )





def getWorldMatrix( inputTarget ):
    
    target = pymel.core.ls( inputTarget )[0]
    return listToMatrix( cmds.getAttr( target + '.wm' ) )




def getUVAtPoint( point, inputMesh ):
    
    if type( point ) in [ type([]), type(()) ]:
        point = OpenMaya.MPoint( *point )
    mesh = pymel.core.ls( inputMesh )[0]
    
    meshShape = mesh.name()
    fnMesh = OpenMaya.MFnMesh( getDagPath( meshShape ) )
    
    util = OpenMaya.MScriptUtil()
    util.createFromList( [0.0,0.0], 2 )
    uvPoint = util.asFloat2Ptr()
    fnMesh.getUVAtPoint( point, uvPoint, OpenMaya.MSpace.kWorld )
    u = OpenMaya.MScriptUtil.getFloat2ArrayItem( uvPoint, 0, 0 )
    v = OpenMaya.MScriptUtil.getFloat2ArrayItem( uvPoint, 0, 1 )
    
    return u, v




def getSourceConnection( inputTrg, inputSrc ):

    src = pymel.core.ls( inputSrc )[0].name()
    trg = pymel.core.ls( inputTrg )[0].name()
    cons = cmds.listConnections( src, s=1, d=0, p=1, c=1 )

    if not cons: return None

    srcCons  = cons[1::2]
    destCons = cons[::2]

    for i in range( len( srcCons ) ):
        srcCon = srcCons[i]
        destCon = destCons[i].replace( src, trg )

        if cmds.nodeType( src ) == 'joint' and cmds.nodeType( trg ) =='transform':
            destCon = destCon.replace( 'jointOrient', 'rotate' )

        if not cmds.ls( destCon ): continue

        if not cmds.isConnected( srcCon, destCon ):
            cmds.connectAttr( srcCon, destCon, f=1 )




def getCenter( inputSels ):
    if not inputSels: return None
    
    def chunks(l, n):
        for i in xrange(0, len(l), n):
            yield l[i:i+n]
    
    sels = pymel.core.ls( inputSels, fl=1 )
    
    bb = OpenMaya.MBoundingBox()
    for sel in sels:
        posList = list( chunks( pymel.core.xform( sel, q=1, ws=1, t=1 ), 3 ) )
        for pos in posList:
            pos = OpenMaya.MPoint( *pos )
            bb.expand( pos )
    return bb.center()





def putObject( inputPutTarget, typ='null' ):
    
    if not inputPutTarget:
        putTarget = None
    else:
        putTarget = pymel.core.ls( inputPutTarget, fl=1 )
        if len( putTarget ) == 1:
            putTarget = pymel.core.ls( inputPutTarget )[0]
    
    if typ == 'locator':
        newObj = pymel.core.spaceLocator()
    elif typ == 'null':
        newObj = pymel.core.createNode( 'transform' )
        pymel.core.setAttr( newObj + '.dh', 1 )
    else:
        newObj = pymel.core.createNode( typ )
    
    if putTarget:
        if type( putTarget ) in [list, tuple]:
            center = getCenter( putTarget )
            pymel.core.move( center.x, center.y, center.z, newObj, ws=1 )
        elif not putTarget.nodeType() in ['transform', 'joint']:
            center = getCenter( putTarget )
            pymel.core.move( center.x, center.y, center.z, newObj, ws=1 )
        else:
            mtx = matrixToList( getPivotWorldMatrix( putTarget ) )
            pymel.core.xform( newObj, ws=1, matrix= mtx )
    return newObj





def getLookAtAngleNode( inputLookTarget, inputRotTarget, **options ):

    def createLookAtMatrix( lookTarget, rotTarget ):
        mm = pymel.core.createNode( 'multMatrix' )
        compose = pymel.core.createNode( 'composeMatrix' )
        mm2 = pymel.core.createNode( 'multMatrix' )
        invMtx = pymel.core.createNode( 'inverseMatrix' )
        
        lookTarget.wm >> mm.i[0]
        rotTarget.t >> compose.it
        compose.outputMatrix >> mm2.i[0]
        rotTarget.pm >> mm2.i[1]
        mm2.matrixSum >> invMtx.inputMatrix
        invMtx.outputMatrix >> mm.i[1]
        return mm
    
    if options.has_key( 'direction' ) and options['direction']:
        direction = options['direction']
    else:
        direction = [1,0,0]
    
    lookTarget = pymel.core.ls( inputLookTarget )[0]
    rotTarget = pymel.core.ls( inputRotTarget )[0]
    
    dcmpLookAt = getDecomposeMatrix( createLookAtMatrix( lookTarget, rotTarget ).matrixSum )
    
    abnodes = dcmpLookAt.listConnections( type='angleBetween' )
    if not abnodes:
        node = cmds.createNode( 'angleBetween' )
        cmds.setAttr( node + ".v1", *direction )
        cmds.connectAttr( dcmpLookAt + '.ot', node + '.v2' )
    else:
        node = abnodes[0]
    return node




def lookAtConnect( inputLookTarget, inputRotTarget, **options ):
    
    if options.has_key( 'direction' ) and options['direction']:
        direction = options['direction']
    else:
        direction = None
    
    lookTarget = pymel.core.ls( inputLookTarget )[0]
    rotTarget  = pymel.core.ls( inputRotTarget )[0]
    
    if inputRotTarget:
        pRotTarget = rotTarget.getParent()
        if pRotTarget:
            wim = listToMatrix( pRotTarget.wim.get() )
        else:
            wim = OpenMaya.MMatrix()
        pos = OpenMaya.MPoint( *pymel.core.xform( lookTarget, q=1, ws=1, t=1 ) )
        directionIndex = getDirectionIndex( pos*wim )
        direction = [[1,0,0], [0,1,0], [0,0,1],[-1,0,0], [0,-1,0], [0,0,-1]][directionIndex]
    
    node = getLookAtAngleNode( lookTarget, rotTarget, direction=direction )
    cmds.connectAttr( node + '.euler', rotTarget + '.r' )




def makeLookAtChild( inputLookTarget, inputLookBase, **options ):
    
    lookTarget = pymel.core.ls( inputLookTarget )[0]
    lookBase   = pymel.core.ls( inputLookBase )[0]
    
    lookAtChild = pymel.core.createNode( 'transform' )
    lookAtChild.setParent( lookBase )
    lookAtConnect( lookTarget, lookAtChild, **options )
    lookAtChild.t.set( 0,0,0 )
    return lookAtChild





def getClosestPointSkinWeightDict( inputPoint, mesh ):

    if type( inputPoint ) != type( OpenMaya.MPoint() ):
        point = OpenMaya.MPoint( *inputPoint )
    else:
        point = inputPoint
    
    dagPath = getDagPath( mesh )
    meshMtx = dagPath.inclusiveMatrix()
    localPoint = point * meshMtx.inverse()
    intersector = OpenMaya.MMeshIntersector()
    intersector.create( dagPath.node() )
    
    pointOnMesh = OpenMaya.MPointOnMesh()
    intersector.getClosestPoint( localPoint, pointOnMesh )
    closeFaceIndex = pointOnMesh.faceIndex()
    
    fnMesh = OpenMaya.MFnMesh( dagPath )
    vtxIds = OpenMaya.MIntArray()
    fnMesh.getPolygonVertices( closeFaceIndex, vtxIds )
    
    points = OpenMaya.MPointArray()
    fnMesh.getPoints( points )
    
    plugsList = []
    distanceList = []
    distSum = 0
    for i in range( vtxIds.length() ):
        targetPoint = points[vtxIds[i]]
        dist = localPoint.distanceTo( targetPoint )
        plugs = getWeightPlugFromSkinedVertex( mesh + '.vtx[%d]' % vtxIds[i] )
        distanceList.append( dist )
        plugsList.append( plugs )
        distSum += dist
    
    weightDict = {}
    for i in range( len( distanceList ) ):
        weightValue = ( distSum - distanceList[i] )/( distSum * (vtxIds.length()-1) )
        for plug in plugsList[i]:
            if not weightDict.has_key( plug.index() ):
                weightDict.update( {plug.index():plug.get() * weightValue} )
            else:
                weightDict[ plug.index() ] += (plug.get() * weightValue)

    return weightDict




def bindTransformBySkinedMesh( inputTransform, inputSkinedMesh ):
    
    tr   = pymel.core.ls( inputTransform )[0]
    mesh = pymel.core.ls( inputSkinedMesh )[0]
    if mesh.nodeType() == 'transform':
        mesh = mesh.getShape()
    
    pos = pymel.core.xform( tr, q=1, ws=1, t=1 )
    weightDict = getClosestPointSkinWeightDict( pos, mesh )
    
    skinNodes = getNodeFromHistory( mesh, 'skinCluster' )
    if not skinNodes: return None
    skinNode = skinNodes[0]
    
    plugMatrix = OpenMaya.MFnDependencyNode( getMObject( skinNode ) ).findPlug( 'matrix' )
    
    wtAddMatrix = pymel.core.createNode( 'wtAddMatrix' )
    
    index = 0
    for key, value in weightDict.items():
        cons = pymel.core.listConnections( plugMatrix[ key ].name(), s=1, d=0, p=1 )
        eachMultMatrix = pymel.core.createNode( 'multMatrix' )
        eachMultMatrix.i[0].set( cons[0].node().wim.get() )
        cons[0] >> eachMultMatrix.i[1]
        eachMultMatrix.matrixSum >> wtAddMatrix.i[index].m
        wtAddMatrix.i[index].w.set( value )
        index +=1
    
    multMatrix  = pymel.core.createNode( 'multMatrix' )
    dcmp = pymel.core.createNode( 'decomposeMatrix' )
    multMatrix.matrixSum >> dcmp.imat
    
    multMatrix.i[0].set( tr.wm.get() )
    wtAddMatrix.o >> multMatrix.i[1]
    tr.pim >> multMatrix.i[2]
    
    dcmp.ot >> tr.t
    dcmp.outputRotate >> tr.r
    dcmp.os >> tr.s




def createFollicleOnClosestPoint( inputTargetObj, inputMesh ):
        
    targetObj = pymel.core.ls( inputTargetObj )[0]
    mesh = pymel.core.ls( inputMesh )[0]
        
    meshShape = getShape( mesh )
    u, v = getUVAtPoint( pymel.core.xform( targetObj, q=1, ws=1, t=1 ), mesh )
    
    follicleNode = pymel.core.createNode( 'follicle' )
    follicle = follicleNode.getParent()
    
    meshShape.outMesh >> follicleNode.inputMesh
    meshShape.wm >> follicleNode.inputWorldMatrix
    
    follicleNode.parameterU.set( u )
    follicleNode.parameterV.set( v )
    
    follicleNode.outTranslate >> follicle.t
    follicleNode.outRotate >> follicle.r




def fixFollicleLocalToWorld( inputFollicle ):
    
    follicle = pymel.core.ls( inputFollicle )[0]
    if follicle.nodeType() == 'transform':
        follicle = follicle.getShape()
        follicleTr = follicle.getParent()
    else:
        follicle = follicle
        follicleTr = follicle.getParent()
    
    if follicle.outTranslate.listConnections( s=0, d=1, type='composeMatrix' ): return None
    composeMatrix = pymel.core.createNode( 'composeMatrix' )
    follicle.outTranslate >> composeMatrix.it
    follicle.outRotate >> composeMatrix.ir
    
    dcmp = getLocalDecomposeMatrix( composeMatrix.outputMatrix, follicleTr.pim )
    dcmp.ot >> follicleTr.t
    dcmp.outputRotate >> follicleTr.r





def createFollicleOnVertex( vertexName, ct= True, cr= True, **options ):
    
    vtx = pymel.core.ls( vertexName )[0]
    vtxPos = pymel.core.xform( vtx, q=1, ws=1, t=1 )
    meshShape = vtx.node()
    u, v = getUVAtPoint( vtxPos, meshShape )
    
    follicleNode = pymel.core.createNode( 'follicle' )
    follicle = follicleNode.getParent()
    
    meshShape.outMesh >> follicleNode.inputMesh
    meshShape.wm >> follicleNode.inputWorldMatrix

    follicleNode.parameterU.set( u )
    follicleNode.parameterV.set( v )
    
    if options.has_key( 'local' ) and options['local']:
        follicleNode.outTranslate >> follicle.t
        follicleNode.outRotate >> follicle.r
    else:
        compose = pymel.core.createNode( 'composeMatrix' )
        mm = pymel.core.createNode( 'multMatrix' )
        dcmp = pymel.core.createNode( 'decomposeMatrix' )
        compose.outputMatrix >> mm.i[0]
        follicle.pim >> mm.i[1]
        mm.matrixSum >> dcmp.imat
        if ct: 
            follicleNode.outTranslate >> compose.it
            dcmp.ot >> follicle.t
        if cr:
            follicleNode.outRotate >> compose.ir
            dcmp.outputRotate >> follicle.r    
    return follicle




def bindTransformToMesh( inputTransform, inputMesh, **options ):

    connectTrans = True
    connectRotate = True
    
    if options.has_key( 'ct' ):
        connectTrans = options['ct']
    if options.has_key( 'cr' ):
        connectRotate = options['cr']

    tr = pymel.core.ls( inputTransform )[0]
    mesh = pymel.core.ls( inputMesh )[0]
    
    u, v = getUVAtPoint( pymel.core.xform( tr, q=1, ws=1, t=1 ), mesh )
    follicle = pymel.core.createNode( 'follicle' )
    follicle.parameterU.set( u )
    follicle.parameterV.set( v )
    
    meshShape = getShape( mesh )
    meshShape.outMesh >> follicle.inputMesh
    meshShape.worldMatrix >> follicle.inputWorldMatrix
    
    follicleTr = follicle.getParent()
    offsetTr = pymel.core.createNode( 'transform' )
    offsetTr.setParent( follicleTr )
    
    if connectTrans: follicle.outTranslate >> follicleTr.t
    if connectRotate : follicle.outRotate >> follicleTr.r
    
    pymel.core.xform( offsetTr, ws=1, matrix=tr.wm.get() )
    constrain( offsetTr, tr )




def getOtherSideStr( inputStr ):
    
    leftList = [ '_L_', '_LU_', '_LD_', '_LF_', '_LB_', '_LUF_', '_LUB_' ]
    rightList = [ '_R_', '_RU_', '_RD_', '_RF_', '_RB_', '_RUF_', '_RUB_' ]
    
    for i in range( len( leftList ) ):
        if inputStr.find( leftList[i] ) != -1:
            return inputStr.replace( leftList[i], rightList[i] )

    return  inputStr


    
    
def mirrorControllerShape( inputTarget ):

    target = pymel.core.ls( inputTarget )[0]
    targetName = target.shortName()
    othersideName = getOtherSideStr( targetName )

    cvs = cmds.ls( target + '.cv[*]', fl=1 )
    poses = []
    for cv in cvs:
        cvPoint = cmds.xform( cv, q=1, os=1, t=1 )
        poses.append( cvPoint )
    otherCVs = cmds.ls( target.replace( targetName, othersideName ) + '.cv[*]', fl=1 )
    for i in range( len( otherCVs ) ):
        cmds.move( -poses[i][0], -poses[i][1], -poses[i][2], otherCVs[i], os=1 )




def assignToLayeredTexture( inputTextureNode, inputLayredNode, **options ):
    
    textureNode = pymel.core.ls( inputTextureNode )[0]
    layeredTexture = pymel.core.ls( inputLayredNode )[0]
    
    index = None
    blendMode = None
    if options.has_key( 'index' ):
        index = options['index']
    if options.has_key( 'blendMode' ):
        blendMode = options['blendMode']

    if index == None:
        fnNode = OpenMaya.MFnDependencyNode( getMObject( layeredTexture ) )
        inputsPlug = fnNode.findPlug( 'inputs' )
        if inputsPlug.numElements():
            logicalIndex = inputsPlug[ inputsPlug.numElements()-1 ].logicalIndex()
        else:
            logicalIndex = -1
        index = logicalIndex + 1

    print 
    textureNode.outColor >> layeredTexture.attr( 'inputs' )[ index ].color
    textureNode.outAlpha >> layeredTexture.attr( 'inputs' )[ index ].alpha
    
    if blendMode != None:
        layeredTexture.attr( 'inputs' )[ index ].blendMode.set( blendMode )



def constrain_pointToParent( src, inputTarget ):
    target = pymel.core.ls( inputTarget )[0]
    constrain_point( src, target.getParent() )



def constrain_rotateToParent( src, inputTarget ):
    target = pymel.core.ls( inputTarget )[0]
    constrain_rotate( src, target.getParent() )



def constrain_scaleToParent( src, inputTarget ):
    target = pymel.core.ls( inputTarget )[0]
    constrain_scale( src, target.getParent() )



def constrain_parentToParent( src, inputTarget ):
    target = pymel.core.ls( inputTarget )[0]
    constrain_all( src, target.getParent() )


def constrain_allToParent( src, inputTarget ):
    target = pymel.core.ls( inputTarget )[0]
    constrain_all( src, target.getParent() )




def getDistance( inputNode ):
    node = pymel.core.ls( inputNode )[0]
    distNode = pymel.core.createNode( 'distanceBetween' )
    if node.nodeType() in ['transform', 'joint' ]:
        node.t >> distNode.point1
    if node.nodeType() == "decomposeMatrix":
        node.outputTranslate >> distNode.point1
    elif node.nodeType() in ['composeMatrix', 'transposeMatrix', 'inverseMatrix','multMatrix', 'wtAddMatrix', 'addMatrix']:
        getOutputMatrixAttribute(node) >> distNode.matrix1
    return distNode



def replaceConnection( *args ):
    
    first = pymel.core.ls( args[0] )[0] 
    second = pymel.core.ls( args[1] )[0] 
    target = pymel.core.ls( args[2] )[0]
    
    cons = target.listConnections( s=1, d=0, p=1, c=1 )
    for origCon, srcCon in cons:
        con = srcCon
        attr = srcCon.longName()
        if con.node() != first: continue
        second.attr( attr ) >> origCon



def scalarOutput( inputNode ):
    
    node = pymel.core.ls( inputNode )[0]
    nodeType = node.nodeType()
    
    if nodeType == 'distanceBetween':
        return node.attr( 'distance' )




def vectorOutput( inputNode ):
    
    node = pymel.core.ls( inputNode )[0]
    nodeType = node.nodeType()
    
    if nodeType == "decomposeMatrix":
        return node.attr( 'ot' )
    if nodeType == "vectorProduct":
        return node.attr( "output" )
    if nodeType == "closestPointOnMesh":
        return node.attr( "normal" )
    if nodeType == "plusMinusAverage":
        return node.attr( "output3D" )
    if nodeType == 'pointOnCurveInfo':
        return node.attr( "tangent" )
    else:
        return node
        

    

def getCrossVectorNode( first, second ):
    
    crossVector = pymel.core.createNode( 'vectorProduct' )
    crossVector.attr( 'op' ).set( 2 )
    
    firstVector = vectorOutput( first )
    if firstVector:
        firstVector >> crossVector.attr( 'input1' )
    secondVector = vectorOutput( second )
    if secondVector:
        secondVector >> crossVector.attr( 'input2' )
    
    return crossVector



def getFbfMatrix( *args ):
    
    xAttrs = vectorOutput( args[0] ).children()
    yAttrs = vectorOutput( args[1] ).children()
    zAttrs = vectorOutput( args[2] ).children()
    
    fbfMtx = pymel.core.createNode( 'fourByFourMatrix' )
    xAttrs[0] >> fbfMtx.attr('in00')
    xAttrs[1] >> fbfMtx.attr('in01')
    xAttrs[2] >> fbfMtx.attr('in02')
    yAttrs[0] >> fbfMtx.attr('in10')
    yAttrs[1] >> fbfMtx.attr('in11')
    yAttrs[2] >> fbfMtx.attr('in12')
    zAttrs[0] >> fbfMtx.attr('in20')
    zAttrs[1] >> fbfMtx.attr('in21')
    zAttrs[2] >> fbfMtx.attr('in22')
    if len( args ) == 4:
        pAttr = vectorOutput( args[3] ).children()
        pAttr[0] >> fbfMtx.attr( 'in30' )
        pAttr[1] >> fbfMtx.attr( 'in31' )
        pAttr[2] >> fbfMtx.attr( 'in32' )
    
    return fbfMtx



def addIkScaleAndSlide( inputIkCtl, inputIkJntTop ):
    
    ikCtl = pymel.core.ls( inputIkCtl )[0]
    ikJntTop = pymel.core.ls( inputIkJntTop )[0]
    
    ikJntGrp    = ikJntTop.getParent()
    ikJntMiddle = ikJntTop.listRelatives( c=1, type='transform' )[0]
    ikJntEnd    = ikJntMiddle.listRelatives( c=1, type='transform' )[0]
    
    upperCon = ikJntMiddle.tx.listConnections( s=1, d=0, p=1 )
    lowerCon = ikJntEnd.tx.listConnections( s=1, d=0, p=1 )
    
    if upperCon:
        upperCon = upperCon[0]
    else:
        addDoubleNode = pymel.core.createNode( 'addDoubleLinear' ); addDoubleNode.setAttr( 'input1', ikJntMiddle.tx.get() )
        upperCon = addDoubleNode.output
    if lowerCon:
        lowerCon = lowerCon[0]
    else:
        addDoubleNode = pymel.core.createNode( 'addDoubleLinear' ); addDoubleNode.setAttr( 'input1', ikJntEnd.tx.get() )
        lowerCon = addDoubleNode.output

    addOptionAttribute( ikCtl, 'scaleIk' )
    ikCtl.addAttr( 'addScale',   min=-1, max=1, k=1 )
    ikCtl.addAttr( 'slideScale', min=-1, max=1, k=1 )
    ikCtl.addAttr( 'stretch', min=0, max=1, k=1 )
    
    powNode = pymel.core.createNode( 'multiplyDivide' ); powNode.setAttr( 'op', 3 )
    addUpper = pymel.core.createNode( 'addDoubleLinear' )
    addLower = pymel.core.createNode( 'addDoubleLinear' )
    lowerReverse = pymel.core.createNode( 'multDoubleLinear' ); lowerReverse.setAttr( 'input2', -1 )
    
    multUpper = pymel.core.createNode( 'multDoubleLinear' )
    multLower = pymel.core.createNode( 'multDoubleLinear' )
    
    powNode.input1X.set( 2 )
    ikCtl.addScale >> powNode.input2X
    powNode.outputX >> addUpper.input1
    powNode.outputX >> addLower.input1
    ikCtl.slideScale >> addUpper.input2
    ikCtl.slideScale >> lowerReverse.input1
    lowerReverse.output >> addLower.input2
    addUpper.output >> multUpper.input2
    addLower.output >> multLower.input2
    
    upperCon >> multUpper.input1
    lowerCon >> multLower.input1
    
    multUpper.output >> ikJntMiddle.tx
    multLower.output >> ikJntEnd.tx

    distTarget = ikCtl.name().replace( 'Ctl_IkLeg', 'FootIkJnt_Toe' ).replace( '02', '_end' )
    if cmds.objExists( distTarget ):
        distIk = getDistance( getLocalDecomposeMatrix( distTarget + '.wm', ikJntGrp + '.wim' ) )
    else:
        distIk = getDistance( getLocalDecomposeMatrix( ikCtl + '.wm', ikJntGrp + '.wim' ) )
    
    cuUpperAndLowerAdd = pymel.core.createNode( 'addDoubleLinear' )
    cuUpperAndLowerDist = pymel.core.createNode( 'distanceBetween' )
    multUpper.output >> cuUpperAndLowerAdd.input1
    multLower.output >> cuUpperAndLowerAdd.input2
    cuUpperAndLowerAdd.output >> cuUpperAndLowerDist.point1X
    
    distCondition = pymel.core.createNode( 'condition' )
    distIk.distance >> distCondition.firstTerm
    cuUpperAndLowerDist.distance >> distCondition.secondTerm
    distCondition.op.set( 2 )
    
    distRate = pymel.core.createNode( 'multiplyDivide' )
    distRate.op.set( 2 )
    distIk.distance >> distRate.input1X
    cuUpperAndLowerDist.distance >> distRate.input2X
    
    stretchedUpper = pymel.core.createNode( 'multDoubleLinear' )
    stretchedLower = pymel.core.createNode( 'multDoubleLinear' )
    
    multUpper.output >> stretchedUpper.input1
    multLower.output >> stretchedLower.input1
    distRate.outputX >> stretchedUpper.input2
    distRate.outputX >> stretchedLower.input2
    
    blendNodeUpper = pymel.core.createNode( 'blendTwoAttr' )
    blendNodeLower = pymel.core.createNode( 'blendTwoAttr' )
    ikCtl.stretch >> blendNodeUpper.ab
    ikCtl.stretch >> blendNodeLower.ab
    
    multUpper.output >> blendNodeUpper.input[0]
    multLower.output >> blendNodeLower.input[0]
    stretchedUpper.output >> blendNodeUpper.input[1]
    stretchedLower.output >> blendNodeLower.input[1]
    
    blendNodeUpper.output >> distCondition.colorIfTrueR
    blendNodeLower.output >> distCondition.colorIfTrueG
    multUpper.output >> distCondition.colorIfFalseR
    multLower.output >> distCondition.colorIfFalseG
    
    distCondition.outColorR >> ikJntMiddle.tx
    distCondition.outColorG >> ikJntEnd.tx



def followIk( inputIkCtl, inputParents ):
    
    ikCtl = pymel.core.ls( inputIkCtl )[0]
    
    trList = []
    nameList = []
    for inputParent in inputParents:
        targetParent = pymel.core.ls( inputParent )[0]
        ikPos = ikCtl.getParent().wm.get()
        tr = pymel.core.createNode( 'transform', n='F' + targetParent + '_for_' + inputIkCtl )
        tr.setParent( targetParent )
        trList.append( tr )
        nameList.append( targetParent.name() )
        pymel.core.xform( tr, ws=1, matrix= ikPos )
    
    blendMatrix = pymel.core.createNode( 'wtAddMatrix' )
    trList[0].wm >> blendMatrix.i[0].m
    
    sumWeight = pymel.core.createNode( 'plusMinusAverage' )
    rangeNode = pymel.core.createNode( 'setRange' )
    revNode   = pymel.core.createNode( 'reverse' )
    sumWeight.output1D >> rangeNode.valueX; rangeNode.maxX.set( 1 ); rangeNode.oldMaxX.set( 1 )
    rangeNode.outValueX >> revNode.inputX
    revNode.outputX >> blendMatrix.i[0].w
    
    divSumNode = pymel.core.createNode( 'condition' )
    divSumNode.secondTerm.set( 1 ); divSumNode.operation.set( 2 ); divSumNode.colorIfFalseR.set( 1 )
    sumWeight.output1D >> divSumNode.firstTerm
    sumWeight.output1D >> divSumNode.colorIfTrueR
    divSumAttr = divSumNode.outColorR

    addOptionAttribute( ikCtl, 'followOptions' )

    wIndex = 1
    for i in range( 1, len( trList ) ):
        cuPointer = trList[i]
        cuPointer.wm >> blendMatrix.i[i].m
        
        try:ikCtl.addAttr( nameList[i], k=1, min=0, max=1, dv=0 )
        except:pass
        divWeight = pymel.core.createNode( 'multiplyDivide' ); divWeight.op.set( 2 )
        ikCtl.attr( nameList[i] ) >> divWeight.input1X
        divSumAttr >> divWeight.input2X
        divWeight.outputX >> blendMatrix.i[wIndex].w
        
        ikCtl.attr( nameList[i] ) >> sumWeight.input1D[ wIndex-1 ]
        wIndex += 1
    
    multMtx = pymel.core.createNode( 'multMatrix' )
    dcmp = pymel.core.createNode( 'decomposeMatrix' )
    blendMatrix.matrixSum >> multMtx.i[0]
    ikCtl.getParent().pim >> multMtx.i[1]
    multMtx.matrixSum >> dcmp.imat
    
    dcmp.ot >> ikCtl.getParent().t
    dcmp.outputRotate >> ikCtl.getParent().r
        
        

def createWorldGeometry( inputTarget ):
    
    target = pymel.core.ls( inputTarget )[0]
    if target.nodeType() == 'transform':
        targetShape = target.getShape()
    else:
        targetShape = target
    
    outputAttr = None
    inputAttr = None
    if targetShape.nodeType() == 'mesh':
        outputAttr = targetShape.outMesh
        inputAttr = pymel.core.createNode( 'mesh' ).inMesh
    elif targetShape.nodeType() in ['nurbsCurve', 'nurbsSurface']:
        outputAttr = targetShape.local
        inputAttr = pymel.core.createNode( targetShape.nodeType() ).create
    else:
        cmds.error( "%s is not edit able" % target.name() )
    
    trGeo = pymel.core.createNode( 'transformGeometry' )
    outputAttr >> trGeo.inputGeometry
    target.wm >> trGeo.transform
    trGeo.outputGeometry >> inputAttr
    
    copyShader( target, inputAttr.node().getParent() )
    inputAttr.node().getParent().rename( target.nodeName() + '_worldGeo' )
    
    return inputAttr.node()




def createWorldGeometryGroup( inputGrp ):

    geos = [ target for target in pymel.core.listRelatives( inputGrp, c=1, ad=1, type='transform' ) if target.getShape() ]
    worldGeos = []
    
    for geo in geos:
        worldGeo = createWorldGeometry( geo )
        worldGeos.append( worldGeo )
    
    grp = pymel.core.group( em=1 )
    pymel.core.parent( worldGeos, grp )
    grp.rename( pymel.core.ls( inputGrp )[0].nodeName() + '_worldGeo' )
    return grp
        


    
    
def createWorldGeometryNoneDeform( inputTarget ):
    
    target = pymel.core.ls( inputTarget )[0]
    if target.nodeType() == 'transform':
        targetShape = target.getShape()
    else:
        targetShape = target
    
    outputAttr = None
    inputAttr = None
    if targetShape.nodeType() == 'mesh':
        outputAttr = targetShape.outMesh
        inputAttr = pymel.core.createNode( 'mesh' ).inMesh
    elif targetShape.nodeType() in ['nurbsCurve', 'nurbsSurface']:
        outputAttr = targetShape.local
        inputAttr = pymel.core.createNode( targetShape.nodeType() ).create
    else:
        cmds.error( "%s is not edit able" % target.name() )
    
    outputAttr >> inputAttr
    newObject = inputAttr.node().getParent()
    dcmp = pymel.core.createNode( 'decomposeMatrix' )
    target.wm >> dcmp.imat
    dcmp.ot >> newObject.t
    dcmp.outputRotate >> newObject.r
    dcmp.os >> newObject.s
    dcmp.osh >> newObject.sh
    
    copyShader( target, newObject )
    
    return newObject
    



def setTranslateDefault( inputTarget ):
    
    target = pymel.core.ls( inputTarget )[0]
    attrs = ['tx', 'ty', 'tz']
    for attr in attrs:
        dv = pymel.core.attributeQuery( attr, node= target, ld=1 )[0]
        try:target.attr( attr ).set( dv )
        except:pass
        
    

def setRotateDefault( inputTarget ):
    
    target = pymel.core.ls( inputTarget )[0]
    attrs = ['rx', 'ry', 'rz']
    for attr in attrs:
        dv = pymel.core.attributeQuery( attr, node= target, ld=1 )[0]
        try:target.attr( attr ).set( dv )
        except:pass



def setScaleDefault( inputTarget ):
    
    target = pymel.core.ls( inputTarget )[0]
    attrs = ['sx', 'sy', 'sz']
    for attr in attrs:
        dv = pymel.core.attributeQuery( attr, node= target, ld=1 )[0]
        try:target.attr( attr ).set( dv )
        except:pass



def setAllDefault( inputTarget ):
    
    target = pymel.core.ls( inputTarget )[0]
    attrs = cmds.listAttr( target.name(), k=1 )
    for attr in attrs:
        dv = pymel.core.attributeQuery( attr, node= target, ld=1 )[0]
        try:target.attr( attr ).set( dv )
        except:pass





def getClosestParamAtPoint( inputTargetObj, inputCurve ):
    
    targetObj = pymel.core.ls( inputTargetObj )[0]
    curve = pymel.core.ls( inputCurve )[0]
    
    if curve.nodeType() == 'transform':
        crvShape = curve.getShape()
    else:
        crvShape = curve
    
    dagPathTarget = getDagPath( targetObj )
    mtxTarget = dagPathTarget.inclusiveMatrix()
    dagPathCurve  = getDagPath( crvShape )
    mtxCurve  = dagPathCurve.inclusiveMatrix()
    
    pointTarget = OpenMaya.MPoint( mtxTarget[3] )
    pointTarget *= mtxCurve.inverse()
    
    fnCurve = OpenMaya.MFnNurbsCurve( getDagPath( crvShape ) )
    
    util = OpenMaya.MScriptUtil()
    util.createFromDouble( 0.0 )
    ptrDouble = util.asDoublePtr()
    fnCurve.closestPoint( pointTarget, 0, ptrDouble )
    
    paramValue = OpenMaya.MScriptUtil().getDouble( ptrDouble )
    return paramValue




def attachToCurve( inputTargetObj, inputCurve ):
    
    targetObj = pymel.core.ls( inputTargetObj )[0]
    curve = pymel.core.ls( inputCurve )[0]
    
    if curve.nodeType() == 'transform':
        crvShape = curve.getShape()
    else:
        crvShape = curve
    
    param = getClosestParamAtPoint( targetObj, curve )
    curveInfo = pymel.core.createNode( 'pointOnCurveInfo' )
    
    crvShape.ws >> curveInfo.inputCurve
    addAttr( inputTargetObj, ln='param', min=crvShape.minValue.get(), max=crvShape.maxValue.get(), dv=param, k=1 )
    inputTargetObj.attr( 'param' ) >> curveInfo.parameter
    
    vectorNode = pymel.core.createNode( 'vectorProduct' )
    vectorNode.op.set( 4 )
    curveInfo.position >> vectorNode.input1
    targetObj.pim >> vectorNode.matrix
    vectorNode.output >> targetObj.t
    


def getPointAtParam( inputCurveObj, paramValue ):
    
    curveObj = pymel.core.ls( inputCurveObj )[0]
    if curveObj.nodeType() == 'nurbsCurve':
        curveShape = curveObj
    else:
        curveShape = curveObj.getShape()
    
    fnCurve = OpenMaya.MFnNurbsCurve( getDagPath( curveShape ) )
    point = OpenMaya.MPoint()
    fnCurve.getPointAtParam( paramValue, point, OpenMaya.MSpace.kWorld )
    return [ point.x, point.y, point.z ]



def getTangetAtParam( inputCurveObj, paramValue ):
    
    curveObj = pymel.core.ls( inputCurveObj )[0]
    if curveObj.nodeType() == 'nurbsCurve':
        curveShape = curveObj
    else:
        curveShape = curveObj.getShape()
    
    fnCurve = OpenMaya.MFnNurbsCurve( getDagPath( curveShape ) )
    tangent = fnCurve.tangent( paramValue, OpenMaya.MSpace.kWorld )
    return [ tangent.x, tangent.y, tangent.z ]
    
    


def getNormalAtPoint( inputMesh, inputPoint ):
    
    if type( inputPoint ) in [ list, tuple ]:
        point = OpenMaya.MPoint( *inputPoint )
    else:
        point = inputPoint
    
    mesh = pymel.core.ls( inputMesh )[0]
    if mesh.nodeType() == 'transform':
        meshShape = mesh.getShape()
    else:
        meshShape = mesh
    
    dagPath = getDagPath( meshShape.name() )
    intersector = OpenMaya.MMeshIntersector()
    intersector.create( getMObject( meshShape ) )
    
    pointOnMesh = OpenMaya.MPointOnMesh()
    intersector.getClosestPoint( point * dagPath.inclusiveMatrixInverse(), pointOnMesh )
    normal = OpenMaya.MVector( pointOnMesh.getNormal() ) * dagPath.inclusiveMatrix()
    
    return [ normal.x, normal.y, normal.z ]




def lookAt( inputAimTarget, inputRotTarget, baseDir=None, **options ):
    
    aimTarget = pymel.core.ls( inputAimTarget )[0]
    rotTarget = pymel.core.ls( inputRotTarget )[0]
    
    rotWorldMatrix = listToMatrix( pymel.core.xform( rotTarget, q=1, ws=1, matrix=1 ) )
    aimWorldMatrix = listToMatrix( pymel.core.xform( aimTarget, q=1, ws=1, matrix=1 ) )
    localAimTarget = aimWorldMatrix * rotWorldMatrix.inverse()
    localAimPos    = OpenMaya.MPoint( localAimTarget[3] )
    direction = OpenMaya.MVector( localAimPos ).normal()
    
    directionIndex = getDirectionIndex( direction )
    
    if not baseDir:
        baseDir = [[1,0,0], [0,1,0], [0,0,1], [-1,0,0], [0,-1,0], [0,0,-1]][directionIndex]
    
    baseDir = OpenMaya.MVector( *baseDir )
    direction = OpenMaya.MVector( *direction )
    localAngle = baseDir.rotateTo( direction ).asMatrix()
    
    rotResultMatrix = localAngle * rotWorldMatrix
    trRotMatrix = OpenMaya.MTransformationMatrix( rotResultMatrix )
    rotVector = trRotMatrix.eulerRotation().asVector()
    
    options.update( {'ws':1, 'pcp':1} )
    pymel.core.rotate( inputRotTarget, math.degrees( rotVector.x ), math.degrees( rotVector.y ), math.degrees( rotVector.z ), **options )



def setOrientByChild( inputTargetJnt, evt=0 ):
    
    targetJnt = pymel.core.ls( inputTargetJnt )[0]
    children = pymel.core.listRelatives( targetJnt, c=1, f=1 )
    if not children: return None
    childrenMats = []
    for child in children:
        childrenMats.append( cmds.getAttr( child + '.wm' ) )
    lookAt( targetJnt, children[0] )
    for i in range( len(children) ):
        cmds.xform( children[i], ws=1, matrix= childrenMats[i] )
    
    
    
    

def createJointLineOnEdge( edges, numJoint, **options ):
    
    reverseOrder = False
    if options.has_key( 'reverseOrder' ):
        reverseOrder = options['reverseOrder']
    print "reverseOrder :", reverseOrder
    

    pymel.core.select( edges )
    curve = pymel.core.ls( pymel.core.polyToCurve( form=2, degree=3 )[0] )[0]
    curveShape = curve.getShape()
    maxValue = curveShape.maxValue.get()
    eachParam = maxValue / numJoint
    
    targetMeshShape = pymel.core.ls( edges[0] )[0].node()
    targetMesh = targetMeshShape.getParent()
    
    matricies = []
    meshIntersector = OpenMaya.MMeshIntersector()
    meshIntersector.create( getMObject( targetMeshShape ) )
    
    for i in range( numJoint+1 ):
        point   = getPointAtParam( curve, i*eachParam )
        tangent = getTangetAtParam( curve, i*eachParam )
        normal  = OpenMaya.MVector( *getNormalAtPoint( targetMesh, point ) )
        if reverseOrder:
            tangent = [ value * -1 for value in tangent ]
        vTangent = OpenMaya.MVector( *tangent )
        vNormal = OpenMaya.MVector( *normal )
        vBNormal = vTangent ^ vNormal
        vANormal = vBNormal ^ vTangent
        vTangent.normalize()
        vANormal.normalize()
        vBNormal.normalize()
        matrix = [ vTangent.x, vTangent.y, vTangent.z, 0,
          vANormal.x, vANormal.y, vANormal.z, 0, 
          vBNormal.x, vBNormal.y, vBNormal.z, 0,
          point[0], point[1], point[2], 1 ]
        matricies.append( matrix )
    
    if reverseOrder:
        matricies.reverse()
    
    pymel.core.select( d=1 )
    trNodes = []
    for matrix in matricies:
        trNode = pymel.core.joint()
        pymel.core.xform( trNode, ws=1, matrix=matrix )
        trNodes.append( trNode )
    
    pymel.core.delete( curve )
    
    return trNodes



def getIndexColor( inputDagNode ):
    
    dagNode = pymel.core.ls( inputDagNode )[0]
    return dagNode.overrideColor.get()





def setIndexColor( inputDagNode, index ):
    
    dagNode = pymel.core.ls( inputDagNode )[0]
    dagNode.overrideEnabled.set( 1 )
    dagNode.overrideColor.set( index )
    



def createFkControl( topJoint, controllerSize = 1,  pinExists = False ):

    selChildren = topJoint.listRelatives( c=1, ad=1 )
    selH = selChildren + [topJoint]
    selH.reverse()
    
    beforeCtl = None
    ctls = []
    pinCtls = []
    for i in range( len( selH ) ):    
        target = selH[i]
        ctlTarget = makeController( sgModel.Controller.circlePoints, controllerSize, makeParent=1 )
        ctlTarget.shape_rz.set( 90 )
        ctlP = ctlTarget.getParent()
        pymel.core.xform( ctlP, ws=1, matrix=target.wm.get() )
        if beforeCtl:
            ctlTarget.getParent().setParent( beforeCtl )
        beforeCtl = ctlTarget
        
        if pinExists:
            ctlPin = makeController( sgModel.Controller.pinPoints, controllerSize * 1.2, makeParent=1 )
            ctlPin.shape_ry.set( 90 )
            ctlPinP = ctlPin.getParent()
            ctlPinP.setParent( ctlTarget )
            setTransformDefault( ctlPinP )
            pinCtls.append( ctlPin )
        else:
            pinCtls.append( None )
        ctls.append( ctlTarget )
    
    for i in range( len( selH )-1 ):
        directionIndex = getDirectionIndex( selH[i+1].t.get() )
        vectorList = [[1,0,0], [0,1,0], [0,0,1], [-1,0,0], [0,-1,0], [0,0,-1]]
        aim = vectorList[ directionIndex ]
        up  = vectorList[ (directionIndex + 1)%6 ]
        aimObj = ctls[i+1]
        upObj = ctls[i]
        if pinCtls[i]:
            upObj = pinCtls[i]
        if pinCtls[i+1]:
            aimObj = pinCtls[i+1]
        pymel.core.aimConstraint( aimObj, selH[i], aim=aim, u=up, wu=up, wut='objectrotation', wuo=upObj )
        
        blendTwoMatrixConnect( ctls[i], ctls[i].getParent(), pinCtls[i].getParent(), ct=0, cr=1, cs=0, csh=0 )
        
        constrain_point( upObj, selH[i] )
    constrain_parent( ctls[-1], selH[-1] )
    
    for i in range( len( selH ) ):
        dcmp = selH[i].listConnections( s=1, d=0, type='decomposeMatrix' )[0]
        dcmp.os >> selH[i].s
        selH[i].attr( 'segmentScaleCompensate' ).set( 1 )
    
    return ctls, pinCtls

    
    
def createFkControlJoint( inputTopFk ):
    
    topFk = pymel.core.ls( inputTopFk )[0]
    children = topFk.listRelatives( c=1, ad=1, type='transform' )
    children.append( topFk )
    children.reverse()
    
    isFirst = True
    beforeJoint = None
    
    topFkP = topFk.getParent()
    targets = []
    joints = []
    for child in children:
        if not child.getShape(): continue
        childP = child.getParent()
        childPVec = OpenMaya.MVector( *childP.t.get() )
        if childPVec.length() == 0: continue
        
        if isFirst:
            if topFkP: pymel.core.select( topFkP )
            else:pymel.core.select( d=1 )
            newJoint = pymel.core.joint()
            isFirst = False
        else:
            pymel.core.select( beforeJoint )
            newJoint = pymel.core.joint()
        
        pymel.core.xform( newJoint, ws=1, matrix=childP.wm.get() )
        newJoint.rename( 'cj_' + childP )
        
        targets.append( childP )
        joints.append( newJoint )
        
        beforeJoint = newJoint
    
    for i in range( len( targets ) ):
        if i == 0:
            constrain_parent( joints[i], targets[i] )
        else:
            dcmp = pymel.core.createNode( 'decomposeMatrix' )
            joints[i].m >> dcmp.imat
            dcmp.ot >> targets[i].t
            dcmp.outputRotate >> targets[i].r
        joints[i].jo.set( joints[i].r.get() )
        joints[i].r.set( 0,0,0 )
    
    return joints



def buildCurveFromSylinderEdge( inputEdge ):
    
    edgeRings = getOrderedEdgeRings( inputEdge )
    
    curvePoints = []
    for i in range( len( edgeRings ) ):
        pymel.core.select( edgeRings[i] )
        cmds.SelectEdgeLoopSp()
        loopEdges = pymel.core.ls( sl=1 )
        poses = pymel.core.xform( loopEdges, q=1, ws=1, t=1 )
        
        bb = OpenMaya.MBoundingBox()
        for i in range( 0, len( poses ), 3 ):
            sepPose = [poses[i],poses[i+1],poses[i+2]]
            bb.expand( OpenMaya.MPoint( *sepPose ) )
        
        center = bb.center()
        curvePoints.append( [center.x, center.y, center.z] )
    
    curve = pymel.core.curve( p=curvePoints )
    return curve




def getCurveLength( inputCurve ):
    
    curve = pymel.core.ls( inputCurve )[0]
    if curve.nodeType() == 'transform':
        curveShape = curve.getShape()
    else:
        curveShape = curve
    
    fnCurve = OpenMaya.MFnNurbsCurve( getDagPath( curveShape ) )
    localCVs = OpenMaya.MPointArray()
    worldCVs = OpenMaya.MPointArray()
    fnCurve.getCVs( localCVs )
    fnCurve.getCVs( worldCVs, OpenMaya.MSpace.kWorld )
    fnCurve.setCVs( worldCVs )
    length = fnCurve.length()
    fnCurve.setCVs( localCVs )
    return length



def getCurveLocalLength( inputCurve ):
    
    curve = pymel.core.ls( inputCurve )[0]
    if curve.nodeType() == 'transform':
        curveShape = curve.getShape()
    else:
        curveShape = curve
    
    fnCurve = OpenMaya.MFnNurbsCurve( getDagPath( curveShape ) )
    length = fnCurve.length()
    return length
    
    
def getCurveMinParam( inputCurve ):
    
    curve = pymel.core.ls( inputCurve )[0]
    if curve.nodeType() == 'transform':
        curveShape = curve.getShape()
    else:
        curveShape = curve
    return curveShape.minValue.get()



def getCurveMaxParam( inputCurve ):
    
    curve = pymel.core.ls( inputCurve )[0]
    if curve.nodeType() == 'transform':
        curveShape = curve.getShape()
    else:
        curveShape = curve
    return curveShape.maxValue.get()

    


def createRivetFromMeshVertices( components ):
    sels = pymel.core.ls( pymel.core.polyListComponentConversion( components, tv=1 ), fl=1 )
    average = pymel.core.createNode( 'plusMinusAverage' )
    pointer = pymel.core.createNode( 'transform' )
    pointer.dh.set( 1 )
    average.op.set(3)
    for i in range( len( sels )-1 ):
        pointOnCurve = getPointOnCurveFromMeshVertex( sels[i] )
        pointOnCurve.position >> average.input3D[i]
    compose = pymel.core.createNode( 'composeMatrix' )
    mm = pymel.core.createNode( 'multMatrix' )
    dcmp = pymel.core.createNode( 'decomposeMatrix' )
    
    average.output3D >> compose.it
    compose.outputMatrix >> mm.i[0]
    pointer.pim >> mm.i[1]
    mm.o >> dcmp.imat
    dcmp.ot >> pointer.t
    return pointer



def setCenter( inputSel ):
    
    sel = pymel.core.ls( inputSel )
    matList = sel.wm.get()
    mat = listToMatrix(matList)
    
    maxXIndex = 0
    maxXValue = 0
    
    minXIndex = 1
    minXValue = 100000000.0
    
    for i in range( 3 ):
        v = OpenMaya.MVector( mat[i] )
        if math.fabs( v.x ) > maxXValue:
            maxXValue = math.fabs( v.x )
            maxXIndex = i
        if math.fabs( v.x ) < minXValue:
            minXValue = math.fabs( v.x )
            minXIndex = i
    
    minVector = OpenMaya.MVector( mat[minXIndex] )
    maxVector = OpenMaya.MVector( mat[maxXIndex] )
    
    maxVector.y = 0
    maxVector.z = 0
    minVector.x = 0
    
    maxVector.normalize()
    minVector.normalize()
    otherVector = maxVector ^ minVector
    
    if (maxXIndex + 1) % 3 != minXIndex:
        otherVector *= -1
    
    allIndices = [0,1,2]
    allIndices.remove( minXIndex )
    allIndices.remove( maxXIndex )
    
    otherIndex = allIndices[0]
    
    newMatList = copy.copy( matList )
    
    newMatList[ minXIndex * 4 + 0 ] = minVector.x
    newMatList[ minXIndex * 4 + 1 ] = minVector.y
    newMatList[ minXIndex * 4 + 2 ] = minVector.z
    
    newMatList[ maxXIndex * 4 + 0 ] = maxVector.x
    newMatList[ maxXIndex * 4 + 1 ] = maxVector.y
    newMatList[ maxXIndex * 4 + 2 ] = maxVector.z
    
    newMatList[ otherIndex * 4 + 0 ] = otherVector.x
    newMatList[ otherIndex * 4 + 1 ] = otherVector.y
    newMatList[ otherIndex * 4 + 2 ] = otherVector.z
    
    newMatList[3*4] = 0
    
    newMat = listToMatrix( newMatList )
    
    trMat = OpenMaya.MTransformationMatrix( newMat )
    trans = trMat.getTranslation( OpenMaya.MSpace.kWorld )
    rot   = trMat.eulerRotation().asVector()
    
    pymel.core.move( trans.x, trans.y, trans.z, sel, ws=1 )
    pymel.core.rotate( math.degrees(rot.x), math.degrees(rot.y), math.degrees(rot.z), sel, ws=1 )




def connectBindPreMatrix( inputJoint, inputBindPreObj, inputTargetMesh ):
    
    joint = pymel.core.ls( inputJoint )[0]
    bindPreObj = pymel.core.ls( inputBindPreObj )[0]
    targetMesh = pymel.core.ls( inputTargetMesh )[0]
    
    skinNodes = getNodeFromHistory( targetMesh, 'skinCluster' )
    
    if not skinNodes: return None
    
    cons = cmds.listConnections( joint+'.wm', type='skinCluster', p=1, c=1 )
    
    for con in cons[1::2]:
        skinCluster = con.split( '.' )[0]
        if skinCluster != skinNodes[0]: continue
        
        index = int( con.split( '[' )[-1].replace( ']', '' ) )
        if not cmds.isConnected( bindPreObj+'.wim', skinCluster+'.bindPreMatrix[%d]' % index ):
            cmds.connectAttr( bindPreObj+'.wim', skinCluster+'.bindPreMatrix[%d]' % index, f=1 )



def getOrigMesh( shape ):
    for hist in pymel.core.listHistory( shape ):
        if hist.nodeType() != 'mesh': continue
        if not cmds.getAttr( hist + '.io' ): continue
        if not hist.outMesh.listConnections() and not hist.worldMesh.listConnections(): continue 
        return hist




def getShape( inputTarget ):
    
    target = pymel.core.ls( inputTarget )[0]
    if target.nodeType() == 'transform':
        return target.getShape()
    else:
        return target



def outMeshToInMesh( inputSrcMesh, inputDstMesh ):
    
    srcMeshShape = getShape( inputSrcMesh )
    dstMeshShape = getShape( inputDstMesh )
    
    dstOrigMeshShape = getOrigMesh( dstMeshShape )
    
    if dstOrigMeshShape:
        srcMeshShape.outMesh >> dstOrigMeshShape.inMesh
    else:
        srcMeshShape.outMesh >> dstMeshShape.inMesh
    
    
    
    

def transformGeometryControl( inputController, inputMesh ):
    
    controller = pymel.core.ls( inputController )[0]
    mesh = pymel.core.ls( inputMesh )[0]
    meshShape = getShape( mesh )
    
    mm = pymel.core.createNode( 'multMatrix' )
    trGeo = pymel.core.createNode( 'transformGeometry' )
    origMesh = addIOShape( mesh )
    srcCon = meshShape.inMesh.listConnections( s=1, d=0, p=1 )
    srcAttr = origMesh.attr( 'inMesh' )
    if srcCon:
        srcAttr = srcCon[0]

    mesh.wm >> mm.i[0]
    controller.pim >> mm.i[1]
    controller.wm >> mm.i[2]
    mesh.wim >> mm.i[3]
    
    srcAttr >> trGeo.inputGeometry
    mm.o >> trGeo.transform
    
    trGeo.outputGeometry >> meshShape.inMesh
    
    fnMesh = OpenMaya.MFnMesh( getMObject( meshShape.name() ) )
    numVertices = fnMesh.numVertices()
    
    meshName = meshShape.name()
    for i in range( numVertices ):
        cmds.setAttr( meshName + '.pnts[%d]' % i, 0,0,0 )




def createBlendTwoMatrixNode( inputFirstAttr, inputSecondAttr ):
    
    firstAttr  = pymel.core.ls( inputFirstAttr )[0]
    secondAttr = pymel.core.ls( inputSecondAttr )[0]
    
    wtAddMtx = pymel.core.createNode( 'wtAddMatrix' )
    addAttr( wtAddMtx, ln='blend', min=0, max=1, dv=0.5, k=1 )
    
    revNode  = pymel.core.createNode( 'reverse' )

    firstAttr >> wtAddMtx.i[0].m
    secondAttr >> wtAddMtx.i[1].m
    
    wtAddMtx.blend >> revNode.inputX
    revNode.outputX >> wtAddMtx.i[0].w
    wtAddMtx.blend >> wtAddMtx.i[1].w
    
    return wtAddMtx



def getBlendTwoMatrixNode( inputFirst, inputSecond, **options ):

    first = pymel.core.ls( inputFirst )[0]
    second = pymel.core.ls( inputSecond )[0]

    local = False
    if options.has_key('local') and options['local']:
        local = True
    
    firstAttr  = matrixOutput( inputFirst, **options )
    secondAttr = matrixOutput( inputSecond, **options )
    
    firstConnected = firstAttr.listConnections( type='wtAddMatrix', p=1 )
    
    if firstConnected:
        cons = firstConnected[0].node().i[1].m.listConnections( s=1, d=0 )
        if cons and cons[0] == second:
            pymel.core.select( firstConnected[0].node() )
            return firstConnected[0].node()

    wtAddMtx = createBlendTwoMatrixNode( firstAttr, secondAttr )
    pymel.core.select( wtAddMtx )
    return wtAddMtx



def createFollicleOnSurface( inputSurface, paramU=0.5, paramV=0.5 ):
    
    surface = pymel.core.ls( inputSurface )[0]
    surfaceShape = getShape( surface )
    
    follicleNode = pymel.core.createNode( 'follicle' )
    follicleTr = follicleNode.getParent()
    
    surfaceShape.worldMatrix >> follicleNode.inputWorldMatrix
    surfaceShape.local >> follicleNode.inputSurface
    
    compose = pymel.core.createNode( 'composeMatrix' )
    mm = pymel.core.createNode( 'multMatrix' )
    dcmp = pymel.core.createNode( 'decomposeMatrix' )
    
    follicleNode.outTranslate >> compose.it
    follicleNode.outRotate >> compose.ir
    compose.outputMatrix >> mm.i[0]
    follicleTr.pim >> mm.i[1]
    mm.o >> dcmp.imat
    dcmp.outputTranslate >> follicleTr.t
    dcmp.outputRotate    >> follicleTr.r
    follicleNode.attr( 'parameterU' ).set( paramU )
    follicleNode.attr( 'parameterV' ).set( paramV )




def createRiggedCurve( *ctls ):
    
    firstCtl = pymel.core.ls( ctls[0] )[0]
    firstCtlNext = pymel.core.ls( ctls[1] )[0]
    lastCtlBefore = pymel.core.ls( ctls[-2] )[0]
    lastCtl = pymel.core.ls( ctls[-1] )[0]
    
    addAttr( firstCtl, ln='frontMult', cb=1, dv=0.3 )
    addAttr( lastCtl, ln='backMult', cb=1, dv=0.3 )
    
    firstPointerGrp = pymel.core.createNode( 'transform' )
    firstPointer1 = makeChild( firstPointerGrp )
    firstPointer2 = makeChild( firstPointerGrp )
    firstPointerGrp.setParent( firstCtl )
    setTransformDefault( firstPointerGrp )
    
    lastPointerGrp = pymel.core.createNode( 'transform' )
    lastPointer1 = makeChild( lastPointerGrp )
    lastPointer2 = makeChild( lastPointerGrp )
    lastPointerGrp.setParent( lastCtl )
    setTransformDefault( lastPointerGrp )
    
    dcmpFirst = getLocalDecomposeMatrix( firstCtlNext.wm, firstCtl.wim )
    distFirst = getDistance( dcmpFirst )
    dcmpLast = getLocalDecomposeMatrix( lastCtlBefore.wm, lastCtl.wim ) 
    distLast = getDistance( dcmpLast )
    
    firstDirIndex = getDirectionIndex( dcmpFirst.ot.get() )
    firstReverseMult = -1 if firstDirIndex >= 3 else 1
    firstTargetAttr = ['tx','ty','tz'][firstDirIndex%3]
    lastDirIndex = getDirectionIndex( dcmpLast.ot.get() )
    lastReverseMult = -1 if lastDirIndex >= 3 else 1
    lastTargetAttr  = ['tx','ty','tz'][lastDirIndex%3]
    
    firstReverseMultNode = pymel.core.createNode( 'multDoubleLinear' );firstReverseMultNode.setAttr( 'input2', firstReverseMult )
    lastReverseMultNode = pymel.core.createNode( 'multDoubleLinear' );lastReverseMultNode.setAttr( 'input2', lastReverseMult )
    firstReverseMultNode1 = pymel.core.createNode( 'multDoubleLinear' );firstReverseMultNode1.setAttr( 'input2', firstReverseMult )
    lastReverseMultNode1 = pymel.core.createNode( 'multDoubleLinear' );lastReverseMultNode1.setAttr( 'input2', lastReverseMult )
    multFirstPointer1 = pymel.core.createNode( 'multDoubleLinear' );multFirstPointer1.setAttr( 'input2',  0.05 )
    multFirstPointer2 = pymel.core.createNode( 'multDoubleLinear' );multFirstPointer2.setAttr( 'input2',  0.3 )
    multLastPointer1 = pymel.core.createNode( 'multDoubleLinear' );multLastPointer1.setAttr( 'input2',  0.05 )
    multLastPointer2 = pymel.core.createNode( 'multDoubleLinear' );multLastPointer2.setAttr( 'input2',  0.3 )
    firstCtl.frontMult >> firstReverseMultNode.input1
    firstReverseMultNode.output >> multFirstPointer2.input2
    lastCtl.backMult >> lastReverseMultNode.input1
    lastReverseMultNode.output >> multLastPointer2.input2
    
    firstReverseMultNode.output >> firstReverseMultNode1.input1
    lastReverseMultNode.output >> lastReverseMultNode1.input1
    firstReverseMultNode1.input2.set( 0.15 )
    lastReverseMultNode1.input2.set( 0.15 )
    
    distFirst.distance >> multFirstPointer1.input1
    firstReverseMultNode1.output >> multFirstPointer1.input2
    distFirst.distance >> multFirstPointer2.input1
    multFirstPointer1.output >> firstPointer1.attr( firstTargetAttr )
    multFirstPointer2.output >> firstPointer2.attr( lastTargetAttr )
    
    distLast.distance >> multLastPointer1.input1
    lastReverseMultNode1.output >> multLastPointer1.input2
    distLast.distance >> multLastPointer2.input1
    multLastPointer1.output >> lastPointer1.attr( firstTargetAttr )
    multLastPointer2.output >> lastPointer2.attr( lastTargetAttr )
    
    pointerList = [firstPointerGrp, firstPointer1, firstPointer2, lastPointer2, lastPointer1, lastPointerGrp]
    
    for i in range( 1, len( ctls )-1 ):
        beforeCtl = ctls[i-1]
        ctl = ctls[i]
        nextCtl = ctls[i+1]
        
        ctlPointerGrp = makeChild( ctl )
        ctlPointer1 = makeChild( ctlPointerGrp )
        ctlPointer2 = makeChild( ctlPointerGrp )
        
        dcmpBefore = getLocalDecomposeMatrix( beforeCtl.wm, ctl.wim )
        distBefore = getDistance( dcmpBefore )
        dcmpAfter  = getLocalDecomposeMatrix( nextCtl.wm, ctl.wim )
        distAfter  = getDistance( dcmpAfter )
        
        dirIndexB = getDirectionIndex( dcmpBefore.ot.get() )
        reverseMultB = -1 if dirIndexB >= 3 else 1
        targetAttrB = ['tx','ty','tz'][dirIndexB%3]
        dirindexA = getDirectionIndex( dcmpAfter.ot.get() )
        reverseMultA = -1 if dirindexA >= 3 else 1
        targetAttrA = ['tx','ty','tz'][dirindexA%3]
        
        addAttr( ctl, ln='beforeMult', dv=0.3, cb=1 )
        addAttr( ctl, ln='afterMult', dv=0.3, cb=1 )
        multBefore = pymel.core.createNode( 'multDoubleLinear' );multBefore.setAttr( 'input2', reverseMultB )
        multAfter  = pymel.core.createNode( 'multDoubleLinear' );multAfter.setAttr( 'input2', reverseMultA )
        ctl.beforeMult >> multBefore.input1
        ctl.afterMult  >> multAfter.input1
        
        multBeforePointer = pymel.core.createNode( 'multDoubleLinear' );multBeforePointer.setAttr( 'input2',  0.3 * reverseMultB )
        multAfterPointer  = pymel.core.createNode( 'multDoubleLinear' );multAfterPointer.setAttr( 'input2',  0.3 * reverseMultA )
        
        distBefore.distance >> multBeforePointer.input1
        distAfter.distance >> multAfterPointer.input1
        multBefore.output >> multBeforePointer.input2
        multAfter.output >> multAfterPointer.input2
        
        multBeforePointer.output >> ctlPointer1.attr( targetAttrB )
        multAfterPointer.output >> ctlPointer2.attr( targetAttrA )
        
        pointerList.insert( -3, ctlPointer1 )
        pointerList.insert( -3, ctlPointer2 )

    return makeCurveFromSelection( *pointerList )


    


def createSquashBend( geos, **options ):
        
    if not type( geos ) in [ list, tuple ]:
        geos = [geos]
        
    geos = [ pymel.core.ls( geo )[0] for geo in geos ]
    
    allbb = OpenMaya.MBoundingBox()
    for geo in geos:
        bb = cmds.exactWorldBoundingBox( geo.name() )
        
        if math.fabs( bb[0] ) > 1000000: continue
        
        bbmin = bb[:3]
        bbmax = bb[3:]
        pointer00 = OpenMaya.MPoint( *bbmin )
        pointer01 = OpenMaya.MPoint( *bbmax )
        allbb.expand( pointer00 )
        allbb.expand( pointer01 )
    
    bbmin = allbb.min()
    bbmax = allbb.max()
    center = allbb.center()
    
    upperPoint = [ center.x, bbmax.y, center.z ]
    lowerPoint = [ center.x, bbmin.y, center.z ]
    
    bbSize = max( bbmax.x-bbmin.x, bbmax.z-bbmin.z )
    
    dist = OpenMaya.MPoint( *upperPoint ).distanceTo( OpenMaya.MPoint( *lowerPoint ) )
    squashBase = pymel.core.createNode( 'transform', n='sauashBase' ); squashBase.setAttr( 't', lowerPoint )
    upperCtl = makeController( sgModel.Controller.trianglePoints, dist*0.2 )
    upperCtl.setAttr( 'shape_ty', 1 );upperCtl.setAttr( 'shape_rz', 180 )
    pUpperCtl = makeParent( upperCtl )
    lowerCtl = makeController( sgModel.Controller.trianglePoints, dist*0.2 )
    lowerCtl.setAttr( 'shape_ty', -1 )
    pLowerCtl = makeParent( lowerCtl )
    upperCtl.rename( 'Ctl_SquashUpper' )
    lowerCtl.rename( 'Ctl_SquashLower' )
    pUpperCtl.t.set( upperPoint )
    pLowerCtl.t.set( lowerPoint )
    
    setIndexColor( upperCtl, 14 )
    setIndexColor( lowerCtl, 14 )
    
    pymel.core.parent( pUpperCtl, squashBase )
    pymel.core.parent( pLowerCtl, squashBase )
    
    squashCenter = makeChild( squashBase ); squashCenter.rename( 'squashCenter' )
    blendMtxNode = createBlendTwoMatrixNode( upperCtl.wm, lowerCtl.wm )
    multMtx = pymel.core.createNode( 'multMatrix' )
    blendMtxNode.matrixSum >> multMtx.i[0]
    squashCenter.attr( 'pim' ) >> multMtx.i[1]
    dcmpBlend = getDecomposeMatrix( multMtx.o )
    squashCenter.tx.set( pUpperCtl.tx.get() )
    squashCenter.tz.set( pUpperCtl.tz.get() )
    dcmpBlend.oty >> squashCenter.ty
    
    rigedCurve = createRiggedCurve( lowerCtl, upperCtl )
    cmds.setAttr( rigedCurve + '.v' , 0 )
    upperFirstChild = upperCtl.listRelatives( c=1, type='transform' )[0]
    lowerFirstChild = lowerCtl.listRelatives( c=1, type='transform' )[0]
    pymel.core.parent( rigedCurve, squashBase )
    
    lookAtUpper = makeChild( upperCtl ); lookAtUpper.rename( 'lookAtObj_' + upperCtl.name() )
    lookAtLower = makeChild( lowerCtl ); lookAtLower.rename( 'lookAtObj_' + lowerCtl.name() )
    lookAtConnect( squashCenter, lookAtUpper )
    lookAtConnect( squashCenter, lookAtLower )
    
    multLookAtUpper = pymel.core.createNode( 'multiplyDivide' )
    multLookAtLower = pymel.core.createNode( 'multiplyDivide' )
    
    lookAtUpper.r >> multLookAtUpper.input1
    lookAtLower.r >> multLookAtLower.input1
    addOptionAttribute( upperCtl )
    addOptionAttribute( lowerCtl )
    addAttr( upperCtl, ln='autoOrient', min=0, max=1, dv=1, k=1 )
    addAttr( lowerCtl, ln='autoOrient', min=0, max=1, dv=1, k=1 )
    upperCtl.autoOrient >> multLookAtUpper.input2X
    upperCtl.autoOrient >> multLookAtUpper.input2Y
    upperCtl.autoOrient >> multLookAtUpper.input2Z
    lowerCtl.autoOrient >> multLookAtLower.input2X
    lowerCtl.autoOrient >> multLookAtLower.input2Y
    lowerCtl.autoOrient >> multLookAtLower.input2Z
    
    multLookAtUpper.output >> upperFirstChild.r
    multLookAtLower.output >> lowerFirstChild.r
    
    rebuildCurve, rebuildNode = pymel.core.rebuildCurve( rigedCurve, ch=1, rpo=0, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=3, d=3, tol=0.01 )
    rebuildCurve = pymel.core.parent( rebuildCurve, squashBase )
    rebuildCurve[0].v.set( 0 )
    
    numDiv = 4
    if options.has_key( 'numDiv' ):
        numDiv = options['numDiv']
    
    eachParam = 10.0 / (numDiv-1)
    targetNodes = []
    circleTrs = []
    for i in range( numDiv ):
        targetNode = createPointOnCurve( rebuildCurve, 1, local=1 )[0]
        cmds.setAttr( targetNode + '.dh', 0 )
        cmds.setAttr( targetNode + '.parameter', eachParam * i )
        targetNode = cmds.parent( targetNode.name(), squashBase.name() )[0]
        targetNodes.append( targetNode )
        circle, circleNode = cmds.circle( normal=[0,1,0], radius=bbSize/1.8 )
        circle = cmds.parent( circle, targetNode )[0]
        cmds.setAttr( circle + '.t', 0,0,0 )
        cmds.setAttr( circle + '.r', 0,0,0 )
        circleTrs.append( circle )
    
    cmds.tangentConstraint( rebuildCurve, targetNodes[0], aim=[0,1,0], u=[0,0,1], wu=[0,0,1], wut='objectrotation', wuo=lookAtLower.name() )[0]
    cmds.tangentConstraint( rebuildCurve, targetNodes[-1], aim=[0,1,0], u=[0,0,1], wu=[0,0,1], wut='objectrotation', wuo=lookAtUpper.name() )[0]
    
    eachParam = 1.0/(numDiv-1)
    for i in range( 1, numDiv-1 ):
        blendNode = createBlendTwoMatrixNode( lookAtLower.wm, lookAtUpper.wm )
        cmds.setAttr( blendNode + '.blend', eachParam * i )
        tangentNode = cmds.tangentConstraint( rebuildCurve, targetNodes[i], aim=[0,1,0], u=[0,0,1], wu=[0,0,1], wut='objectrotation')[0]
        cmds.connectAttr( blendNode+ '.matrixSum', tangentNode + '.worldUpMatrix' )
    pass
    
    for i in range( len( targetNodes ) ):
        targetNodes[i] = cmds.rename( targetNodes[i], 'Ctl_Squash_dt_%02d' % i )
        setIndexColor( targetNodes[i], 18 )
    
    pymel.core.select( geos )
    ffd, ffdLattice, ffdLatticeBase = pymel.core.lattice( geos,  divisions=[2, numDiv, 2], objectCentered=True, ldv=[2,numDiv+1,2] )
    pymel.core.parent( ffdLattice, ffdLatticeBase, squashBase )
    
    #cmds.setAttr( ffdLattice + '.inheritsTransform', 0 )
    cmds.setAttr( ffdLattice + '.v', 0 )
    
    for i in range( numDiv ):
        cmds.select( ffdLattice + '.pt[0:1][%d][0]' % i, ffdLattice + '.pt[0:1][%d][1]' % i )
        cluster, clusterHandle = cmds.cluster()
        clusterHandle = cmds.parent( clusterHandle, circleTrs[i] )[0]
        cmds.setAttr( clusterHandle + '.v', 0 )
    
    distNode = cmds.createNode( 'distanceBetween' )
    cmds.connectAttr( pUpperCtl.name() + '.wm', distNode + '.inMatrix1' )
    cmds.connectAttr( pLowerCtl.name() + '.wm', distNode + '.inMatrix2' )
    curveInfoNode = cmds.createNode( 'curveInfo' )
    cmds.connectAttr( rigedCurve + '.worldSpace', curveInfoNode + '.inputCurve' )
    squashDiv = cmds.createNode( 'multiplyDivide' ); cmds.setAttr( squashDiv + '.op', 2 )
    squashPow = cmds.createNode( 'multiplyDivide' ); cmds.setAttr( squashPow + '.op', 3 )
    cmds.connectAttr( distNode + '.distance', squashDiv + '.input1X' )
    cmds.connectAttr( curveInfoNode + '.arcLength', squashDiv + '.input2X' )
    cmds.connectAttr( squashDiv  + '.outputX', squashPow + '.input1X' )
    cmds.setAttr( squashPow + '.input2X', 0.5 )
    
    
    addAttr( upperCtl, ln='squash', min=0, dv=1, k=1 )
    addAttr( upperCtl, ln='showDetail', min=0, max=1, cb=1, at='long' )
    eachParam = 1.0/(numDiv-1)
    for i in range( numDiv ):
        cmds.addAttr( circleTrs[i], ln='squashMult', min=0, dv=1 - 4*( i * eachParam - 0.5 )**2, k=1 )
        multNode1 = cmds.createNode( 'multDoubleLinear' )
        cmds.connectAttr( upperCtl + '.squash', multNode1 + '.input1' )
        cmds.connectAttr( circleTrs[i] + '.squashMult', multNode1 + '.input2' )
        
        blendNode = cmds.createNode( 'blendTwoAttr' )
        cmds.setAttr( blendNode + '.input[0]', 1 )
        cmds.connectAttr( squashPow + '.outputX', blendNode + '.input[1]' )
        
        cmds.connectAttr( multNode1 + '.output', blendNode + '.ab' )
        cmds.connectAttr( blendNode + '.output', targetNodes[i] + '.sx' )
        cmds.connectAttr( blendNode + '.output', targetNodes[i] + '.sz' )
        
        cmds.connectAttr( upperCtl.name() + '.showDetail', targetNodes[i] + '.v' )
    
    cmds.setAttr( ffdLattice + '.inheritsTransform', 0 )
    setMatrixToTarget( listToMatrix(cmds.getAttr( ffdLatticeBase + '.wm' )), ffdLattice )



def copyDeformer( inputSrc, *inputTrgs ):
    
    source = pymel.core.ls( inputSrc )[0]
    targets = [ pymel.core.ls( inputTrg )[0] for inputTrg in inputTrgs ]
    
    hists = pymel.core.listHistory( source, pdo=1 )
    hists.reverse()
    
    for hist in hists:
        if pymel.core.nodeType( hist ) == 'nonLinear':
            for target in targets:
                pymel.core.nonLinear( hist, e=1, geometry=target )
        elif pymel.core.nodeType( hist ) == 'wire':
            for target in targets:
                pymel.core.wire( hist, e=1, geometry=target )
        elif pymel.core.nodeType( hist ) == 'ffd':
            for target in targets:
                pymel.core.lattice( hist, e=1, geometry=target )
        elif pymel.core.nodeType( hist ) == 'skinCluster':
            for target in targets:
                autoCopyWeight( source, target )




def getMPoint( inputSrc ):
    
    if type( inputSrc ) in [ type( OpenMaya.MVector() ), type( OpenMaya.MPoint() ) ]:
        return OpenMaya.MPoint( inputSrc )
    elif type( inputSrc ) == list:
        return OpenMaya.MPoint( *inputSrc )
    return OpenMaya.MPoint( *pymel.core.xform( inputSrc, q=1, ws=1, t=1 ) )



def getMVector( inputSrc ):
    
    if type( inputSrc ) in [ type( OpenMaya.MVector() ), type( OpenMaya.MPoint() ) ]:
        return OpenMaya.MVector( inputSrc )
    elif type( inputSrc ) == list:
        return OpenMaya.MVector( *inputSrc )
    elif type( inputSrc ) == pymel.core.datatypes.Vector:
        return OpenMaya.MVector( inputSrc.x, inputSrc.y, inputSrc.z )
    return OpenMaya.MVector( *pymel.core.xform( inputSrc, q=1, ws=1, t=1 ) )
    



def getMMatrix( inputAttr ):
    
    if type( inputAttr ) == pymel.core.general.Attribute:
        attr = pymel.core.ls( inputAttr )[0]
        return listToMatrix( cmds.getAttr( attr.name() ) )
    elif type( inputAttr ) == pymel.core.datatypes.Matrix:
        return listToMatrix( inputAttr )
    else:
        return inputAttr





def tangentContraint( inputCurve, inputUpObject, inputTarget ):

    curve    = pymel.core.ls( inputCurve )[0]
    upObject = pymel.core.ls( inputUpObject )[0]
    target = pymel.core.ls( inputTarget )[0]
    
    nearPointOnCurve = pymel.core.createNode( 'nearestPointOnCurve' )
    pointOnCurveInfo = pymel.core.createNode( 'pointOnCurveInfo' )

    curve.getShape().worldSpace >> nearPointOnCurve.inputCurve
    curve.getShape().worldSpace >> pointOnCurveInfo.inputCurve
    compose = pymel.core.createNode( 'composeMatrix' )
    inputTarget.t >> compose.it
    mm = pymel.core.createNode( 'multMatrix' )
    compose.outputMatrix >> mm.i[0]
    target.pm >> mm.i[1]
    dcmp = getDecomposeMatrix( mm.o )
    dcmp.ot >> nearPointOnCurve.inPosition
    nearPointOnCurve.parameter >> pointOnCurveInfo.parameter
    
    tangent = getMVector( pointOnCurveInfo.tangent.get() ) * getMMatrix( target.wm.get() ).inverse()
    dirIndex = getDirectionIndex( tangent )
    
    args = [ None for i in range( 4 ) ]
    upTrans = [0,0,0]
    upTrans[ ( dirIndex + 1 )%3 ] = 1
    vectorNodeUp = pymel.core.createNode( 'vectorProduct' )
    vectorNodeUp.input1.set( upTrans )
    vectorNodeUp.op.set( 3 )
    upObject.wm >> vectorNodeUp.matrix
    
    vectorNodeCross = getCrossVectorNode( pointOnCurveInfo, vectorNodeUp )
    vectorNodeUp = getCrossVectorNode( vectorNodeCross, pointOnCurveInfo )
    
    args[ dirIndex % 3 ] = pointOnCurveInfo.tangent
    args[ (dirIndex+1) % 3 ] = vectorNodeUp.output
    args[ (dirIndex+2) % 3 ] = vectorNodeCross.output 
    args[ 3 ] = nearPointOnCurve.position
    
    fbf = getFbfMatrix( *args )
    dcmp = getLocalDecomposeMatrix( fbf.o, target.pim )
    dcmp.outputRotate >> target.r




def getMultMatrix( *matrixAttrList ):
    
    mm = pymel.core.createNode( 'multMatrix' )
    for i in range( len( matrixAttrList ) ):
        pymel.core.connectAttr( matrixAttrList[i], mm.i[i] )
    return mm




def getLookAtChildMatrixAttr( lookTargetMatrix, baseMatrix, baseVector ):

    baseInverse = pymel.core.createNode( 'inverseMatrix' )
    baseMatrix >> baseInverse.inputMatrix
    dcmp = getDecomposeMatrix( getMultMatrix( lookTargetMatrix, baseInverse.outputMatrix ).matrixSum )
    angleNode = pymel.core.createNode( 'angleBetween' )

    lookTargetMVector = OpenMaya.MVector( *dcmp.ot.get() )
    baseMVector       = OpenMaya.MVector( *baseVector )

    if lookTargetMVector * baseMVector < 0:
        baseVector = [ -value for value in baseVector ]

    angleNode.vector1.set( baseVector )
    dcmp.ot >> angleNode.vector2

    compose = pymel.core.createNode( 'composeMatrix' )
    angleNode.euler >> compose.ir

    mm = pymel.core.createNode( 'multMatrix' )
    compose.outputMatrix >> mm.i[0]
    baseMatrix >> mm.i[1]

    return mm.matrixSum




def tangentContraintByGroup( inputCurve, inputTargets, inputUpObjects, aimDirection ):
    
    curve = pymel.core.ls( inputCurve )[0]
    targets = [ pymel.core.ls( inputTarget )[0] for inputTarget in inputTargets ]
    upObjects = [ pymel.core.ls( inputUpObject )[0] for inputUpObject in inputUpObjects ]
    
    def getWorldTangentAttr( tangentAttr ):
        srcCons = tangentAttr.node().inputCurve.listConnections( s=1, d=0, p=1 )
        if not srcCons: return None
        
        spaceType = 'world'
        if srcCons[0].longName() == 'local':
            spaceType = 'local'
        elif srcCons[0].longName() == 'world':
            spaceType = 'world'
        
        if spaceType == 'local':
            vectorNode = pymel.core.createNode( 'vectorProduct' )
            vectorNode.op.set( 3 )
            pointOnCurveInfoNode.tangent >> vectorNode.input1
            srcCons[0].node().wm >> vectorNode.matrix
            return vectorNode.output
        else:
            return pointOnCurveInfoNode.tangent
    
    
    def getPointOnCurveInfo( curve, target ):
        
        curveShape = curve.getShape()
        
        pointOnCurveInfos = getNodeFromHistory( target, 'pointOnCurveInfo' )
        
        if pointOnCurveInfos:
            for pointOnCurveInfo in pointOnCurveInfos:
                cons = pointOnCurveInfo.listConnections( s=1, d=0, shapes=1 )
                if curve.getShape() in cons:
                    return pointOnCurveInfo 

        compose =  pymel.core.createNode( 'composeMatrix' )
        mm = pymel.core.createNode( 'multMatrix' )
        dcmp = pymel.core.createNode( 'decomposeMatrix' )
        mm.o >> dcmp.imat
        target.t >> compose.it
        compose.outputMatrix >> mm.i[0]
        target.pm >> mm.i[1]
        curveShape.pim >> mm.i[2]
        pointOnCurveInfo = pymel.core.createNode( 'pointOnCurveInfo' )
        nearCurve = pymel.core.createNode( 'nearestPointOnCurve' )
        curveShape.local >> pointOnCurveInfo.inputCurve
        curveShape.local >> nearCurve.inputCurve
        dcmp.ot >> nearCurve.inPosition
        nearCurve.parameter >> pointOnCurveInfo.parameter        
        return pointOnCurveInfo
    
    
    def twoUpObjectAndParam( target, upObjects ):
        
        if len( upObjects ) == 1:
            firstUpObject  = upObjects[0]
            secondUpObject = upObjects[0]
        else:
            firstUpObject  = upObjects[0]
            secondUpObject = upObjects[1]
        
        targetParam = getClosestParamAtPoint( target, curve )
        
        betweenParam = 1
        for i in range( len( upObjects )-1 ):
            firstUpObject = upObjects[i]
            secondUpObject = upObjects[i+1]
            
            firstUpParam = getClosestParamAtPoint( firstUpObject, curve )
            secondUpParam = getClosestParamAtPoint( secondUpObject, curve )
            
            multParamDirection = 1
            if firstUpParam > secondUpParam:
                multParamDirection = -1
            
            if multParamDirection * ( targetParam - firstUpParam ) < 0:
                betweenParam = 0
                break
            elif multParamDirection * ( targetParam - secondUpParam ) < 0:
                betweenParam = ( targetParam - firstUpParam ) / ( secondUpParam - firstUpParam )
                break
            else:
                continue
                
        return firstUpObject, secondUpObject, betweenParam
    
    
    def getLocalTangentAngleNodeFromBlendMtxNode( curve, blendMtx ):
        
        aimVectorNode = pymel.core.createNode( 'vectorProduct' )
        aimVectorNode.op.set( 3 )
        worldTangentAttr = getWorldTangentAttr( pointOnCurveInfoNode.tangent )
        multDirectionTangentNode = pymel.core.createNode( 'multiplyDivide' )
        
        worldTangentAttr >> multDirectionTangentNode.input1
        multDirectionTangentNode.input2.set( 1, 1, 1 )
        multDirectionTangentNode.output >> aimVectorNode.input1
        invMtxNode.outputMatrix >> aimVectorNode.matrix
        
        if OpenMaya.MVector( *baseAimVector[:3] ) * OpenMaya.MVector( *(worldTangentAttr.get()) ) < 0:
            multDirectionTangentNode.input2.set( -1, -1, -1 )
        
        angleNode = pymel.core.createNode( 'angleBetween' )
        angleNode.vector1.set( aimDirection )
        aimVectorNode.output >> angleNode.vector2
        return angleNode
        
        
    
    for target in targets:
        pointOnCurveInfoNode = getPointOnCurveInfo( curve, target )
        
        firstUpObject, secondUpObject, betweenParam = twoUpObjectAndParam( target, upObjects )
        
        firstAimVector  = copy.copy( aimDirection )
        secondAimVector = copy.copy( aimDirection )
        
        firstUpMatrixAttr  = getLookAtChildMatrixAttr( secondUpObject.wm, firstUpObject.wm, firstAimVector )
        secondUpMatrixAttr = getLookAtChildMatrixAttr( firstUpObject.wm, secondUpObject.wm, secondAimVector )
        
        blendMtxNode = createBlendTwoMatrixNode( firstUpMatrixAttr, secondUpMatrixAttr )
        blendMtxNode.blend.set( betweenParam )
        
        invMtxNode = pymel.core.createNode( 'inverseMatrix' )
        blendMtxNode.matrixSum >> invMtxNode.inputMatrix
        baseAimVector = blendMtxNode.matrixSum.get()[ getDirectionIndex( aimDirection ) % 3 ]
        
        angleNode = getLocalTangentAngleNodeFromBlendMtxNode( curve, blendMtxNode )
        
        composeRot = pymel.core.createNode( 'composeMatrix' )
        angleNode.euler >> composeRot.ir
        
        mmResult = pymel.core.createNode( 'multMatrix' )
        composeRot.outputMatrix >> mmResult.i[0]
        blendMtxNode.matrixSum >> mmResult.i[1]
        target.pim >> mmResult.i[2]
        
        dcmp = getDecomposeMatrix( mmResult.o )
        dcmp.outputRotate >> target.r
    


def curveBaseScaleConnectByGroup( inputCurve, inputTargets, inputUpObjects ):
    
    curve = pymel.core.ls( inputCurve )[0]
    targets = [ pymel.core.ls( inputTarget )[0] for inputTarget in inputTargets ]
    upObjects = [ pymel.core.ls( inputUpObject )[0] for inputUpObject in inputUpObjects ]
    
    
    def twoUpObjectAndParam( target, upObjects, curve ):
        
        if len( upObjects ) == 1:
            firstUpObject  = upObjects[0]
            secondUpObject = upObjects[0]
        else:
            firstUpObject  = upObjects[0]
            secondUpObject = upObjects[1]
        
        targetParam = getClosestParamAtPoint( target, curve )
        
        betweenParam = 1
        for i in range( len( upObjects )-1 ):
            firstUpObject = upObjects[i]
            secondUpObject = upObjects[i+1]
            firstUpParam = getClosestParamAtPoint( firstUpObject, curve )
            secondUpParam = getClosestParamAtPoint( secondUpObject, curve )
            multParamDirection = 1
            if firstUpParam > secondUpParam:
                multParamDirection = -1
            if multParamDirection * ( targetParam - firstUpParam ) < 0:
                betweenParam = 0
                break
            elif multParamDirection * ( targetParam - secondUpParam ) < 0:
                betweenParam = ( targetParam - firstUpParam ) / ( secondUpParam - firstUpParam )
                break
            else:
                continue
        return firstUpObject, secondUpObject, betweenParam

    for target in targets:
        firstUpObject, secondUpObject, betweenParam = twoUpObjectAndParam( target, upObjects, curve )
        
        blendColors = pymel.core.createNode( 'blendColors' )
        firstUpObject.scale >> blendColors.color2
        secondUpObject.scale >> blendColors.color1
        blendColors.output >> target.scale 
        blendColors.blender.set( betweenParam )
        
        





def aimConstraint( inputAim, inputUp, inputTarget ):
    
    aim = pymel.core.ls( inputAim )[0]
    up  = pymel.core.ls( inputUp )[0]
    target = pymel.core.ls( inputTarget )[0]
    direction = ( getMVector( aim ) - getMVector( target ) ) * getMMatrix( target.wim )
    aimIndex = getDirectionIndex( direction )
    upIndex = (aimIndex+1) % 3
    vectorList = [ [1,0,0], [0,1,0], [0,0,1], [-1,0,0], [0,-1,0], [0,0,-1] ]
    aimVector = vectorList[ aimIndex ]
    upVector = vectorList[ upIndex ]
    pymel.core.aimConstraint( aim, target, aim=aimVector, u=upVector, wu=upVector, wut='objectrotation', wuo=up )



def getDecomposeRotateConnection( inputTarget ):
    
    target = pymel.core.ls( inputTarget )[0]
    
    dcmp = target.listConnections( s=1, d=0, type='decomposeMatrix' )
    if not dcmp: return
    if cmds.isConnected( dcmp[0] + '.or', target + '.r' ): return
    cmds.connectAttr( dcmp[0] + '.or', target + '.r' )



def getDecomposeScaleConnection( inputTarget ):
    
    target = pymel.core.ls( inputTarget )[0]
    
    dcmp = target.listConnections( s=1, d=0, type='decomposeMatrix' )
    if not dcmp: return
    if cmds.isConnected( dcmp[0] + '.os', target + '.s' ): return
    cmds.connectAttr( dcmp[0] + '.os', target + '.s' )



def getDecomposeShearConnection( inputTarget ):
    
    target = pymel.core.ls( inputTarget )[0]
    
    dcmp = target.listConnections( s=1, d=0, type='decomposeMatrix' )
    if not dcmp: return
    if cmds.isConnected( dcmp[0] + '.osh', target + '.sh' ): return
    cmds.connectAttr( dcmp[0] + '.osh', target + '.sh' )




def connectScaleByTranslateDistance( inputDistTarget1, inputDistTarget2, inputTarget, axisIndex ):
    
    distTarget1 = pymel.core.ls( inputDistTarget1 )[0]
    distTarget2 = pymel.core.ls( inputDistTarget2 )[0]
    target = pymel.core.ls( inputTarget )[0]
    targetChild = target.listRelatives( c=1 )[0]
    if not targetChild: return
    
    dcmpPoint1 = getLocalDecomposeMatrix( distTarget1.wm, target.pim )
    dcmpPoint2 = getLocalDecomposeMatrix( distTarget2.wm, target.pim )
    distNode = pymel.core.createNode( 'distanceBetween' )
    dcmpPoint1.ot >> distNode.point1
    dcmpPoint2.ot >> distNode.point2
    
    scaleAttrName = ['sx','sy','sz'][axisIndex]
    
    defaultAttrName = 'distanceDefault'
    addAttr( targetChild, ln=defaultAttrName, cb=1, dv= distNode.distance.get() )

    divNode = pymel.core.createNode( 'multiplyDivide' )
    divNode.op.set( 2 )
    
    distNode.distance >> divNode.input1X
    targetChild.attr( defaultAttrName ) >> divNode.input2X
    
    divNode.outputX >> target.attr( scaleAttrName )




def createLineController( inputTopJoint, **options ):
    
    topJoint = pymel.core.ls( inputTopJoint )[0]
    jointH = topJoint.listRelatives( c=1, ad=1, type='joint' )
    jointH.append( topJoint )
    jointH.reverse()
    
    startJoint = jointH[0]
    endJoint   = jointH[-1]
    
    firstCtl  = makeController( sgModel.Controller.cubePoints, makeParent=1 )
    secondCtl = makeController( sgModel.Controller.cubePoints, makeParent=1 )
    pymel.core.xform( firstCtl.getParent(),  ws=1, matrix=startJoint.wm.get() )
    pymel.core.xform( secondCtl.getParent(), ws=1, matrix=endJoint.wm.get() )
    
    curveFirst   = createRiggedCurve( firstCtl, secondCtl )
    
    middlePoint = createPointOnCurve( curveFirst, 1 )[0]
    blendTwoMatrixConnect( firstCtl, secondCtl, middlePoint, ct=0 )
    
    middleCtl = makeController( sgModel.Controller.spherePoints, makeParent=1 )
    pymel.core.xform( middleCtl.getParent(), ws=1, matrix=middlePoint.wm.get() )
    constrain_point( middlePoint, middleCtl.getParent() )
    tangentContraint( curveFirst, middlePoint, middleCtl.getParent() )
    
    curveSecond = createRiggedCurve( firstCtl, middleCtl, secondCtl )
    
    minValue = curveSecond.getShape().minValue.get()
    maxValue = curveSecond.getShape().maxValue.get()
    
    middleParam = getClosestParamAtPoint( middleCtl, curveSecond )
    eachCtls = []
    allPoints = [middlePoint]
    for i in range( len( jointH ) ):
        closeParam = getClosestParamAtPoint( jointH[i], curveSecond )
        paramAttrValue = ( closeParam - minValue )/maxValue * 10
        eachPointBase = createPointOnCurve( curveSecond, 1 )[0]
        eachPointBase.parameter.set( paramAttrValue )
        allPoints.append( eachPointBase )
        
        if closeParam < middleParam:
            blendTwoMatrixConnect( firstCtl, middleCtl, eachPointBase, ct=0 )
            eachPointBase.blend.set( closeParam/(middleParam - minValue) )
        else:
            blendTwoMatrixConnect( middleCtl, secondCtl, eachPointBase, ct=0 )
            eachPointBase.blend.set( (closeParam-middleParam)/(maxValue - middleParam) )
        
        eachPoint = makeChild( eachPointBase )
        pymel.core.xform( eachPoint, ws=1, matrix=jointH[i].wm.get() )
        
        eachCtl = makeController( sgModel.Controller.planePoints, makeParent=1 )
        if i == len( jointH )-1:
            constrain_all( secondCtl, eachCtl.getParent() )
        else:
            pymel.core.xform( eachCtl.getParent(), ws=1, matrix= eachPoint.wm.get() )
            constrain_point( eachPoint, eachCtl.getParent() )
            tangentContraint( curveSecond, eachPoint, eachCtl.getParent() )
        eachCtls.append( eachCtl )
    
    for i in range( len( eachCtls )-1 ):
        constrain_point( eachCtls[i], jointH[i] )
        aimConstraint( eachCtls[i+1], eachCtls[i], jointH[i] )
        getDecomposeScaleConnection( jointH[i] )
        getDecomposeShearConnection( jointH[i] )
        jointH[i].segmentScaleCompensate.set( 0 )
        separateParentConnection( jointH[i], 'scale' )
        connectScaleByTranslateDistance( eachCtls[i], eachCtls[i+1], jointH[i], 0 )
        
    constrain_parent( eachCtls[i+1], jointH[i+1] )
    
    direction = ( getMVector(eachCtls[1]) - getMVector( jointH[0] ) ) * getMMatrix( jointH[0].wim )
    aimIndex = getDirectionIndex( direction )
    for i in range( len( eachCtls ) ):
        if aimIndex == 0: eachCtls[i].shape_rz.set( 90 )
        elif aimIndex == 2: eachCtls[i].shape_rx.set( 90 )
    
    etcGrp = pymel.core.group( allPoints, curveFirst, curveSecond )
    ctlsGrp = pymel.core.group( firstCtl.getParent(), secondCtl.getParent(), middleCtl.getParent(), [ eachCtl.getParent() for eachCtl in eachCtls ] )
    etcGrp.v.set( 0 )

    return firstCtl, secondCtl, middleCtl, eachCtls, ctlsGrp, etcGrp



def putControllerToGeo( inputTarget, points, multSize = 1.0 ):
    
    def makeParent( target ):
        targetP = pymel.core.createNode( 'transform' )
        pymel.core.xform( targetP, ws=1, matrix= target.wm.get() )
        pymel.core.parent( target, targetP )
        targetP.rename( 'P' + target.shortName() )
        return targetP
    
    target = pymel.core.ls( inputTarget )[0]
    
    if target:
        if type( target ) in [list, tuple] or target.find( '.' ) != -1:
            worldCenter = getCenter( target )
            controllerMatrix = [1,0,0,0, 0,1,0,0, 0,0,1,0, worldCenter.x, worldCenter.y, worldCenter.z, 1 ]
            sizeX = 1
            sizeY = 1
            sizeZ = 1
        else:
            bbmin = target.boundingBoxMin.get()
            bbmax = target.boundingBoxMax.get()
            sizeX = (bbmax[0]-bbmin[0])/2 * multSize
            sizeY = (bbmax[1]-bbmin[1])/2 * multSize
            sizeZ = (bbmax[2]-bbmin[2])/2 * multSize
            controllerMatrix = matrixToList( getPivotWorldMatrix( target ) )
    else:
        controllerMatrix = OpenMaya.MMatrix()

    if sizeX == 0: sizeX = 1
    if sizeY == 0: sizeY = 1
    if sizeZ == 0: sizeZ = 1

    targetCtl = makeController( points )
    targetCtl.shape_sx.set( sizeX )
    targetCtl.shape_sy.set( sizeY )
    targetCtl.shape_sz.set( sizeZ )
    pymel.core.xform( targetCtl, ws=1, matrix=controllerMatrix )
    makeParent( targetCtl )
    
    return targetCtl



def getMatrixFromSelection( sels ):
    
    isTransform = False
    if len( sels ) == 1:
        if sels[0].find( '.' ) == -1:
            if cmds.objExists( sels[0] ) and cmds.nodeType( sels[0] ) in ['mesh', 'transform']:
                isTransform = True
            
    if sels:
        if isTransform:
            return pymel.core.xform( sels[0], q=1, ws=1, matrix=1 )
        else:
            try:
                centerPos = getCenter( sels )
                mtx = [1,0,0,0, 0,1,0,0, 0,0,1,0, centerPos.x, centerPos.y, centerPos.z,1 ]
                return mtx
            except:
                return [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]
    else:
        return [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]



def replaceShape( inputSrc, inputDst ):
    
    src = pymel.core.ls( inputSrc )[0]
    dst = pymel.core.ls( inputDst )[0]
    
    dstShapes = dst.listRelatives( s=1 )
    srcShapes = src.listRelatives( s=1 )
    
    pymel.core.delete( dstShapes )
    for srcShape in srcShapes:
        pymel.core.parent( srcShape, dst, add=1, shape=1 )



def createSliderBase( axis=None ):
    
    axisX = True
    axisY = True
    
    if axis:
        axisX = False
        axisY = False
        if axis == 'x': axisX = True
        elif axis == 'y': axisY = True
        elif axis == 'xy': axisX = True; axisY = True

    baseData = [[-.5,-.5,0],[.5,-.5,0],[.5,.5,0],[-.5,.5,0],[-.5,-.5,0]]
    baseCurve = pymel.core.curve( p=baseData, d=1 )
    baseCurveOrigShape= addIOShape( baseCurve )
    baseCurveShape = baseCurve.getShape()
    
    trGeo = pymel.core.createNode( 'transformGeometry' )
    composeMatrix = pymel.core.createNode( 'composeMatrix' )
    
    if axisX:
        multNodeX = pymel.core.createNode( 'multDoubleLinear' );multNodeX.setAttr( 'input2', 0.5 )
        addNodeX = pymel.core.createNode( 'addDoubleLinear' );addNodeX.setAttr( 'input2', 1 )
        baseCurve.addAttr( 'slideSizeX', min=0 ); baseCurve.attr( 'slideSizeX' ).set( e=1, cb=1 )
        baseCurve.slideSizeX >> multNodeX.input1
        baseCurve.slideSizeX >> addNodeX.input1
        addNodeX.output >> composeMatrix.inputScaleX
        multNodeX.output >> composeMatrix.inputTranslateX
    
    if axisY:
        multNodeY = pymel.core.createNode( 'multDoubleLinear' );multNodeY.setAttr( 'input2', 0.5 )
        addNodeY = pymel.core.createNode( 'addDoubleLinear' );addNodeY.setAttr( 'input2', 1 )
        baseCurve.addAttr( 'slideSizeY', min=0 ); baseCurve.attr( 'slideSizeY' ).set( e=1, cb=1 )
        baseCurve.slideSizeY >> multNodeY.input1
        baseCurve.slideSizeY >> addNodeY.input1
        addNodeY.output >> composeMatrix.inputScaleY
        multNodeY.output >> composeMatrix.inputTranslateY
    
    composeMatrix.outputMatrix >> trGeo.transform
    baseCurveOrigShape.local >> trGeo.inputGeometry
    trGeo.outputGeometry >> baseCurveShape.create

    return baseCurve



def connectControllerAttrToBlendAttr( inputCtl, blendTarget ):

    ctl = pymel.core.ls( inputCtl )[0]
    blendNode = getNodeFromHistory( blendTarget, 'blendShape' )[0]
    
    ctlAttrs = [ pymel.core.ls( ctl + '.' + attr )[0] for attr in cmds.listAttr( ctl.name(), k=1 ) ]
    
    driverAttr = None
    driverAttrValue = None
    for ctlAttr in ctlAttrs:
        if math.fabs( ctlAttr.get() ) < 0.0001: continue
        driverAttr = ctlAttr
        driverAttrValue = driverAttr.get()
        break
    
    blendNodeAttrs = pymel.core.ls( blendNode + '.w[*]' )
    targetAttr = None
    targetAttrValue = None
    for blendNodeAttr in blendNodeAttrs:
        if math.fabs( blendNodeAttr.get() ) < 0.0001: continue
        targetAttr = blendNodeAttr
        targetAttrValue = targetAttr.get()
        break
        
    if driverAttr and targetAttr:
        animNode = pymel.core.createNode( 'animCurveUU' )
        pymel.core.setKeyframe( animNode, f=0, v=0 )
        pymel.core.setKeyframe( animNode, f=driverAttrValue, v=targetAttrValue )
        pymel.core.keyTangent( animNode, itt='linear', ott='linear' )
    
        driverAttr >> animNode.input
        animNode.output >> targetAttr



def getMatrixFromRotate( rotValue ):
    
    trMtx = OpenMaya.MTransformationMatrix()
    radRotValues = [ math.radians(i) for i in rotValue ]
    trMtx.rotateTo( OpenMaya.MEulerRotation( OpenMaya.MVector( *radRotValues ) ) ) 
    return trMtx.asMatrix()



def setMatrixToTarget( mtxValue, inputTarget ):

    mtx = OpenMaya.MMatrix()
    if type( mtxValue ) == list:
        mtx = listToMatrix( mtxValue )
    else:
        mtx = mtxValue
    transMtxList = [1,0,0,0,
                    0,1,0,0,
                    0,0,1,0,
                    mtx(3,0), mtx(3,1), mtx(3,2), 1]
    target = pymel.core.ls( inputTarget )[0]
    
    if target.type() == 'joint':
        joValue = target.jo.get()
        rotMtx = getMatrixFromRotate( joValue )
        parentMtx = listToMatrix( target.pm.get() )
        localRotMtx = mtx * ( rotMtx * parentMtx ).inverse()
        pymel.core.xform( target, ws=1, matrix= transMtxList )
        rotValue = getRotateFromMatrix( localRotMtx )
        target.r.set( rotValue )
    else:
        pymel.core.xform( target, ws=1, matrix= matrixToList( mtx ) )




def setMatrixToGeoGroup( mtx, inputTarget ):
    
    target = pymel.core.ls( inputTarget )[0]
    tr = cmds.createNode( 'transform' )
    setMatrixToTarget( mtx, tr )
    selChildren = cmds.listRelatives( target.name(), c=1, f=1, ad=1, type='transform' )
    if not selChildren: selChildren = []
    selChildren.append( target.name() )
    unParentList = []
    for selChild in selChildren:
        if cmds.listRelatives( selChild, s=1, f=1 ):
            try:selP = cmds.listRelatives( selChild, p=1, f=1 )[0]
            except:selP = None
            try:selChild = cmds.parent( selChild, w=1 )[0]
            except:pass
            setGeometryMatrixToTarget( selChild, tr )
            unParentList.append( [selChild,selP] )
        else:
            setMatrixToTarget( mtx, selChild )
    for child, parent in unParentList:
        if not parent: continue
        cmds.parent( child, parent )
    cmds.delete( tr )




def createDefaultPropRig( propGrp ):
    
    propGrp = pymel.core.ls( propGrp )[0]
    
    def makeParent( target ):
        targetP = pymel.core.createNode( 'transform' )
        pymel.core.xform( targetP, ws=1, matrix= target.wm.get() )
        pymel.core.parent( target, targetP )
        targetP.rename( 'P' + target.shortName() )
        return targetP
    
    worldCtl = pymel.core.ls( makeController( sgModel.Controller.circlePoints ).name() )[0]
    moveCtl  = pymel.core.ls( makeController( sgModel.Controller.crossPoints ).name() )[0]
    rootCtl  = pymel.core.ls( makeController( sgModel.Controller.circlePoints ).name() )[0]
    
    bb = cmds.exactWorldBoundingBox(propGrp.name())
    bbmin = bb[:3]
    bbmax = bb[3:]
    
    bbsize = max( bbmax[0] - bbmin[0], bbmax[2] - bbmin[2] )/2
    
    center     = ( ( bbmin[0] + bbmax[0] )/2, ( bbmin[1] + bbmax[1] )/2, ( bbmin[2] + bbmax[2] )/2 )
    floorPoint = ( ( bbmin[0] + bbmax[0] )/2, bbmin[1], ( bbmin[2] + bbmax[2] )/2 )
    
    worldCtl.t.set( *floorPoint )
    moveCtl.t.set( *floorPoint )
    rootCtl.t.set( *center )
    
    rootCtl.shape_sx.set( bbsize*1.2 )
    rootCtl.shape_sy.set( bbsize*1.2 )
    rootCtl.shape_sz.set( bbsize*1.2 )

    moveCtl.shape_sx.set( bbsize*1.3 )
    moveCtl.shape_sy.set( bbsize*1.3 )
    moveCtl.shape_sz.set( bbsize*1.3 )
    
    worldCtl.shape_sx.set( bbsize*1.5 )
    worldCtl.shape_sy.set( bbsize*1.5 )
    worldCtl.shape_sz.set( bbsize*1.5 )
    
    rootCtl.getShape().setAttr( 'overrideEnabled', 1 )
    rootCtl.getShape().setAttr( 'overrideColor', 29 )
    moveCtl.getShape().setAttr( 'overrideEnabled', 1 )
    moveCtl.getShape().setAttr( 'overrideColor', 20 )
    worldCtl.getShape().setAttr( 'overrideEnabled', 1 )
    worldCtl.getShape().setAttr( 'overrideColor', 17 )
    
    shortName = propGrp.shortName().split( '|' )[-1]
    rootCtl.rename( 'Ctl_%s_Root' % shortName )
    moveCtl.rename( 'Ctl_%s_Move' % shortName )
    worldCtl.rename( 'Ctl_%s_World' % shortName )
    
    pRootCtl = makeParent( rootCtl )
    pMoveCtl = makeParent( moveCtl )
    pWorldCtl = makeParent( worldCtl )
    
    pymel.core.parent( pRootCtl, moveCtl )
    pymel.core.parent( pMoveCtl, worldCtl )

    setMatrixToGeoGroup( rootCtl.wm.get(), propGrp.name() )
    constrain_all( rootCtl, propGrp )



def buildMouthDetailController( detailPointers ):
    
    ptUpper = detailPointers[0]
    ptLeft  = detailPointers[3]
    ptBottom = detailPointers[6]
    ptRight = detailPointers[9]
    
    size = getMPoint( ptLeft ).distanceTo( getMPoint( ptRight ))
    controllerSize = size / 20
    
    ctlUpper = makeController( sgModel.Controller.spherePoints, controllerSize * 1.3, makeParent=1, n= 'Ctl_Mouth_Upper' )
    ctlLeft = makeController( sgModel.Controller.spherePoints, controllerSize * 1.3, makeParent=1, n= 'Ctl_Mouth_Left' )
    ctlBottom = makeController( sgModel.Controller.spherePoints, controllerSize * 1.3, makeParent=1, n= 'Ctl_Mouth_Bottom' )
    ctlRight = makeController( sgModel.Controller.spherePoints, controllerSize * 1.3, makeParent=1, n='Ctl_Mouth_Right' )
    
    pymel.core.xform( ctlUpper.getParent(), ws=1, matrix=ptUpper.wm.get() )
    pymel.core.xform( ctlLeft.getParent(), ws=1, matrix=ptLeft.wm.get() )
    pymel.core.xform( ctlBottom.getParent(), ws=1, matrix=ptBottom.wm.get() )
    pymel.core.xform( ctlRight.getParent(), ws=1, matrix=ptRight.wm.get() )
    
    ctlDts = []
    for i in range( len( detailPointers ) ): 
        ctlDt = makeController( sgModel.Controller.spherePoints, controllerSize * 0.7, makeParent=1, n='Ctl_Mouth_dt_%d' % i )
        pymel.core.xform( ctlDt.getParent(), ws=1, matrix= detailPointers[i].wm.get() )
        ctlDts.append( ctlDt )
    
    constrain( ctlUpper, ctlDts[0].getParent() )
    constrain( ctlUpper, ctlLeft, ctlDts[1].getParent(), mo=1, atToChild=1 )
    constrain( ctlUpper, ctlLeft, ctlDts[2].getParent(), mo=1, atToChild=1 )
    constrain( ctlLeft, ctlDts[3].getParent() )
    constrain( ctlBottom, ctlLeft, ctlDts[4].getParent(), mo=1, atToChild=1 )
    constrain( ctlBottom, ctlLeft, ctlDts[5].getParent(), mo=1, atToChild=1 )
    constrain( ctlBottom, ctlDts[6].getParent() )
    constrain( ctlBottom, ctlRight, ctlDts[7].getParent(), mo=1, atToChild=1 )
    constrain( ctlBottom, ctlRight, ctlDts[8].getParent(), mo=1, atToChild=1 )
    constrain( ctlRight, ctlDts[9].getParent() )
    constrain( ctlUpper, ctlRight, ctlDts[10].getParent(), mo=1, atToChild=1 )
    constrain( ctlUpper, ctlRight, ctlDts[11].getParent(), mo=1, atToChild=1 )
    
    ctlDts[1].blend_0.set( 5 )
    ctlDts[2].blend_0.set( 0.3 )
    ctlDts[4].blend_0.set( 0.3 )
    ctlDts[5].blend_0.set( 5 )
    ctlDts[7].blend_0.set( 5 )
    ctlDts[8].blend_0.set( 0.3 )
    ctlDts[10].blend_0.set( 0.3 )
    ctlDts[11].blend_0.set( 5 )




def setBindPreMatrix( inputJnt, inputBindPre ):

    jnt = pymel.core.ls( inputJnt )[0]
    bindPre = pymel.core.ls( inputBindPre )[0]
    
    targetAttrs = jnt.wm.listConnections( s=0, d=1, type='skinCluster', p=1 )
    if not targetAttrs: return None
    
    for targetAttr in targetAttrs:
        node = targetAttr.node()
        try:index = targetAttr.index()
        except: continue
        bindPre.wim >> node.bindPreMatrix[ index ]
    
    


def paperRig( target, div=[5,2,5] ):
    
    ffd, lattice, latticeBase = pymel.core.lattice( target, divisions=div, objectCentered=True, ldv=[ i+1 for i in div ] )
    
    if math.fabs( lattice.sy.get() ) < 0.0001:
        lattice.sy.set( 1 )
        latticeBase.sy.set( 1 )
    
    bb = pymel.core.exactWorldBoundingBox( target )
    bbmin = OpenMaya.MVector( *bb[:3] )
    bbmax = OpenMaya.MVector( *bb[3:] )
    
    bbc = [ (bbmin[i] + bbmax[i])/2.0 for i in range( 3 ) ]
    
    startPoint = OpenMaya.MVector( bbmin.x, (bbmin.y + bbmax.y)/2, bbmin.z )
    
    xInterval = (bbmax.x - bbmin.x)/(div[0]-1)
    zInterval = (bbmax.z - bbmin.z)/(div[1]-1)
    xSize = (bbmax.x - bbmin.x)
    zSize = (bbmax.z - bbmin.z)
    
    worldCtl = makeController( sgModel.Controller.circlePoints, 1, makeParent=1, n='Ctl_World' )
    moveCtl  = makeController( sgModel.Controller.crossPoints, 1, makeParent=1, n='Ctl_Move' )
    rootCtl = makeController( sgModel.Controller.planePoints, 1, makeParent=1, n='Ctl_Root' )
    pWorldCtl = worldCtl.getParent()
    pMoveCtl  = moveCtl.getParent()
    pRootCtl  = rootCtl.getParent()
    pWorldCtl.t.set( bbc )
    pMoveCtl.t.set( bbc )
    pRootCtl.t.set( bbc )
    worldCtl.scaleMult.set( xSize/2.0*1.6 )
    moveCtl.scaleMult.set( xSize/2.0*1.4 )
    rootCtl.scaleMult.set( xSize/2.0*1.1 )
    
    pMoveCtl.setParent( worldCtl )
    pRootCtl.setParent( moveCtl )
    
    setIndexColor( worldCtl, 17 )
    setIndexColor( moveCtl, 20 )
    setIndexColor( rootCtl, 15 )
    
    joints = []
    ctls   = []
    fkCtls = []
    
    for i in range( div[0] ):
        xValue = startPoint.x + xInterval * i
        yValue = startPoint.y
        fkCtl = makeController( sgModel.Controller.planePoints, 1, makeParent=1, n='Ctl_Fk_%d' % i )
        pFkCtl = fkCtl.getParent()
        pFkCtl.t.set( xValue, yValue, bbc[2] )
        fkCtl.shape_sz.set( zSize/2.0 )
        fkCtl.shape_rz.set( 90 )
        if fkCtls:
            pFkCtl.setParent( fkCtls[-1] )
        fkCtls.append( fkCtl )
        setIndexColor( fkCtl, 23 )
        
        baseCtl = makeController( sgModel.Controller.spherePoints, 1, makeParent=1, n='Ctl_Base_%d' % i )
        setIndexColor( baseCtl, 18 )
        pBaseCtl = baseCtl.getParent()
        pBaseCtl.t.set( xValue, yValue, bbc[2] )
        pBaseCtl.setParent( fkCtl )
        
        eachJnts = []
        eachCtls = []
        for j in range( div[1] ):
            zValue = startPoint.z + zInterval * j
            eachCtl = makeController( sgModel.Controller.spherePoints, .6, makeParent=1, n='Ctl_Each_%d_%d' % ( i, j ) )
            pEachCtl = eachCtl.getParent()
            pEachCtl.t.set( xValue, yValue, zValue )
            jnt = pymel.core.createNode( 'joint' )
            constrain( eachCtl, jnt, ct=1, cr=1, cs=1, csh=1 )
            pEachCtl.setParent( baseCtl )
            eachJnts.append( jnt )
            eachCtls.append( eachCtl )
            setIndexColor( eachCtl, 31 )
        joints.append( eachJnts )
        ctls.append( eachCtls )

    fkCtls[0].getParent().setParent( rootCtl )
    bindJoints = []
    for eachJoints in joints:
        bindJoints += eachJoints

    skinNode = pymel.core.skinCluster( bindJoints, lattice, tsb=1 )
    lattice.wm >> skinNode.geomMatrix
    latticeGrp = pymel.core.group( em=1, n='latticeGrp' ); pymel.core.parent( lattice, latticeBase, latticeGrp )
    bindJntGrp = pymel.core.group( bindJoints, n='bindJnts' )
    
    initObj = pymel.core.createNode( 'transform', n='initObj' )
    pymel.core.xform( initObj, ws=1, t=bbc )
    initBase = pymel.core.createNode( 'transform', n='initBase' )
    pymel.core.xform( initBase, ws=1, matrix= initObj.wm.get() )
    initObj.t >> initBase.t
    initObj.r >> initBase.r
    latticeGrp.setParent( initObj )
    
    bindPres = []
    for eachJoints in joints:
        eachBindPres = []
        for bindJnt in eachJoints:
            bindPre = pymel.core.createNode( 'transform' )
            bindPre.dh.set( 1 )
            pymel.core.xform( bindPre, ws=1, matrix= bindJnt.wm.get() )
            setBindPreMatrix( bindJnt, bindPre )
            eachBindPres.append( bindPre )
        pymel.core.parent( eachBindPres, initBase )
        bindPres.append( eachBindPres )
    
    #bindPre setting
    beforeAverageNode = None
    for i in range( len( joints ) ):
        eachBindPres = bindPres[i]
        eachJoints   = joints[i]
        eachCtls     = ctls[i]
        fkCtl        = fkCtls[i]
        
        bindPreControls = []
        for eachBindPre in eachBindPres:
            bindPreControl = pymel.core.createNode( 'transform' )
            pymel.core.xform( bindPreControl, ws=1, matrix=eachBindPre.wm.get() )
            bindPreControl.setParent( initObj )
            constrain( bindPreControl, eachBindPre )
            bindPreControls.append( bindPreControl )
        
        averageNode = pymel.core.createNode( 'plusMinusAverage' )
        averageNode.op.set( 3 )
        eachBindPres[0].t >> averageNode.input3D[0]
        eachBindPres[-1].t >> averageNode.input3D[1]
        
        if not beforeAverageNode:
            averageNode.output3D >> fkCtl.getParent().t
        else:
            minusNode = pymel.core.createNode( 'plusMinusAverage' )
            minusNode.op.set( 2 )
            averageNode.output3D >> minusNode.input3D[0]
            beforeAverageNode.output3D >> minusNode.input3D[1]
            minusNode.output3D >> fkCtl.getParent().t
        
        beforeAverageNode = averageNode
        
        for i in range( len( eachBindPres ) ):
            minusNode = pymel.core.createNode( 'plusMinusAverage' )
            minusNode.op.set( 2 )
            eachBindPres[i].t >> minusNode.input3D[0]
            averageNode.output3D >> minusNode.input3D[1]
            minusNode.output3D >> eachCtls[i].getParent().t
        
    constrain( initObj, pWorldCtl )
    
    #shapeSetting
    for i in range( len( joints ) ):
        eachBindPres = bindPres[i]
        fkCtl        = fkCtls[i]
        minusNode = pymel.core.createNode( 'plusMinusAverage' ); minusNode.op.set( 2 )
        multHalf = pymel.core.createNode( 'multDoubleLinear' )
        eachBindPres[-1].t  >> minusNode.input3D[0]
        eachBindPres[0].t >> minusNode.input3D[1]
        minusNode.output3Dz >> multHalf.input1
        multHalf.input2.set( 0.5 )
        multHalf.output >> fkCtl.shape_sz
    
    bindJntGrp.v.set( 0 )
    initObj.v.set( 0 )
    initBase.v.set( 0 )
    lattice.v.set( 0 )
    latticeBase.v.set( 0 )
    
    for targetCtl in [ rootCtl, moveCtl, worldCtl ]:
        initObj.sx >> targetCtl.shape_sx
        initObj.sy >> targetCtl.shape_sy
        initObj.sz >> targetCtl.shape_sz
    
    pymel.core.group( target, pWorldCtl, bindJntGrp, initObj, initBase, n='SET' )




def makeFreezeGeometry( inputGeo ):
    
    targetGeo = pymel.core.ls( inputGeo )[0]
    targetGeoShape = targetGeo.getShape()
    if not targetGeoShape:
        pymel.core.error( "'%s' is not freeze able geometry" % targetGeo.name() )
        return None

    outputAttrName = None; inputAttrName = None
    if targetGeoShape.nodeType() == 'mesh':
        outputAttrName = 'outMesh'
        inputAttrName  = 'inMesh'
    elif targetGeoShape.nodeType() in ['nurbsCurve', 'nurbsSurface']:
        outputAttrName = 'local'
        inputAttrName = 'create'
    if not outputAttrName: 
        pymel.core.error( "'%s' is not freeze able geometry" % targetGeo.name() )
        return None
        
    duTargetGeo = pymel.core.duplicate( targetGeo )[0]
    duTargetGeo.setParent( w=1 )
    duTargetGeoShape = duTargetGeo.getShape()
    trGeo = pymel.core.createNode( 'transformGeometry' )
    targetGeo.attr( outputAttrName ) >> trGeo.inputGeometry
    targetGeo.wm >> trGeo.transform
    trGeo.outputGeometry >> duTargetGeoShape.attr( inputAttrName )
    
    return duTargetGeo
    
    
    
def getSourceGeometry( inputTarget, inputSource ):
    
    target = pymel.core.ls( inputTarget )[0]
    source = pymel.core.ls( inputSource )[0]
    
    inputAttrName  = None
    
    try:
        targetShape = target.getShape()
    except:
        pymel.core.error( "'%s' has no shape" % target )
    
    try:
        sourceShape = source.getShape()
    except:
        pymel.core.error( "'%s' hat no shape" % source )
    
    if targetShape.nodeType() != sourceShape.nodeType():
        pymel.core.error( "'%s' and '%s' has no same geometry type" %( targetShape, sourceShape ) )
    
    if targetShape.nodeType() == 'mesh':
        inputAttrName = 'inMesh'
    elif targetShape.nodeType() in ['nurbsCurve', 'nurbsSurface']:
        inputAttrName = 'create'
    
    if not inputAttrName:
        pymel.core.error( "'%s' is not connect able geometry" % target.name() )
    
    srcPlug = sourceShape.attr( inputAttrName ).listConnections( s=1, d=0, p=1 )
    if not srcPlug:
        pymel.core.error( "%s has no source connection" % sourceShape )
    
    srcPlug[0] >> targetShape.attr( inputAttrName )



def outShapeToInShape( inputSrc, inputDst ):
    
    src = pymel.core.ls( inputSrc )[0]
    dst = pymel.core.ls( inputDst )[0]
    
    srcShape = getShape( src )
    dstShape = getShape( dst )
    
    outputAttr = None
    inputAttr = None
    if srcShape.nodeType() == 'mesh':
        outputAttr = 'outMesh'
        inputAttr = 'inMesh'
    elif srcShape.nodeType() in ['nurbsCurve','nurbsSurface']:
        outputAttr = 'local'
        inputAttr = 'create'
    srcShape.attr( outputAttr ) >> dstShape.attr( inputAttr )




def constrainToCurve( curve, upObject, target ):
    
    param = getClosestParamAtPoint( target, curve )
    curveInfo = pymel.core.createNode( 'pointOnCurveInfo' )
    
    curveShape = curve.getShape()
    curveShape.worldSpace >> curveInfo.inputCurve
    curveInfo.parameter.set( param )
    
    vectorList = getVectorList()
    vTangentTarget = getMVector( curveInfo.tangent.get() )
    vLocalTangetTarget = vTangentTarget * getMMatrix( target.wim.get() )
    aimIndex = getDirectionIndex( vLocalTangetTarget ) % 3
    vTangentUpObject = getMVector( curveInfo.tangent.get() )
    vLocalTangentUpObject = vTangentUpObject * getMMatrix( target.wim.get() )
    upIndex  = ( getDirectionIndex( vLocalTangentUpObject ) + 1 ) % 3
    
    vectorForUp = pymel.core.createNode( 'vectorProduct' ); vectorForUp.op.set( 3 )
    vectorForUp.input1.set( vectorList[ upIndex ] )
    upObject.wm >> vectorForUp.matrix
    
    vectorNode = getCrossVectorNode( curveInfo, vectorForUp )
    fbfNodes = [None, None, None]
    fbfNodes[ aimIndex % 3 ] = curveInfo
    fbfNodes[ upIndex % 3 ] = vectorForUp
    for i in range( len( fbfNodes ) ):
        if fbfNodes[i]: continue
        fbfNodes[i] = vectorNode
    fbf = getFbfMatrix( *fbfNodes )
    curveInfo.positionX >> fbf.in30
    curveInfo.positionY >> fbf.in31
    curveInfo.positionZ >> fbf.in32
    resultDcmp = getLocalDecomposeMatrix( fbf.output, target.pim )
    
    resultDcmp.ot >> target.t
    resultDcmp.outputRotate >> target.r





def makeInterPointer( inputCtls, alwaysConnected = False ):
    
    ctls = [ pymel.core.ls( inputCtl )[0] for inputCtl in inputCtls ]
    
    interPointers = []
    
    pointerInverseMatrixObjects = []
    
    for ctl in ctls:
        tr = pymel.core.createNode( 'transform', n='invMtxObj_' + ctl.name() )
        tr.setParent( ctl.getParent() )
        ctl.t >> tr.t
        pointerInverseMatrixObjects.append( tr )
        tr.s.set( 1,1,1 )
    
    for i in range( len( ctls )-1 ):
        firstCtl = ctls[i]
        secondCtl = ctls[i+1]
        firstInvObj  = pointerInverseMatrixObjects[i]
        secondInvObj = pointerInverseMatrixObjects[i+1]
        
        interPointer1 = pymel.core.createNode( 'transform' ); interPointer1.dh.set( 1 )
        interPointer2 = pymel.core.createNode( 'transform' ); interPointer2.dh.set( 1 )
        interPointer1.rename( 'startIP_' + firstCtl.shortName() )
        interPointer2.rename( 'endIP_' + secondCtl.shortName() )
        interPointer1.setParent( firstCtl ); setTransformDefault( firstInvObj )
        interPointer2.setParent( secondCtl ); setTransformDefault( secondInvObj )
        localDcmpPointer1 = getLocalDecomposeMatrix( secondInvObj.wm, firstInvObj.wim )
        localDcmpPointer2 = getLocalDecomposeMatrix( firstInvObj.wm,  secondInvObj.wim )
        
        twoInterPointers     = [ interPointer1, interPointer2 ]
        twoLocalDcmpPointers = [ localDcmpPointer1, localDcmpPointer2 ]
        
        for i in range( 2 ):
            setTransformDefault( twoInterPointers[i] )
            interPointers.append( twoInterPointers[i] )
            
            if alwaysConnected:
                multTrans = pymel.core.createNode( 'multiplyDivide' )
                twoLocalDcmpPointers[i].ot >> multTrans.input1
                multTrans.output >> twoInterPointers[i].t
                
                addAttr( twoInterPointers[i], ln='multTransX', dv= 0.25, k=1 )
                addAttr( twoInterPointers[i], ln='multTransY', dv= 0.25, k=1 )
                addAttr( twoInterPointers[i], ln='multTransZ', dv= 0.25, k=1 )
                twoInterPointers[i].attr( 'multTransX' ) >> multTrans.input2X
                twoInterPointers[i].attr( 'multTransY' ) >> multTrans.input2Y
                twoInterPointers[i].attr( 'multTransZ' ) >> multTrans.input2Z
            else:
                origDirection = pymel.core.createNode( 'multiplyDivide' )
                origDirection.input1.set( twoLocalDcmpPointers[i].ot.get() )
                
                distNode     = pymel.core.createNode( 'distanceBetween' ); twoLocalDcmpPointers[i].ot >> distNode.point1;
                origDistNode = pymel.core.createNode( 'distanceBetween' ); origDistNode.point1.set( twoLocalDcmpPointers[i].ot.get() )
                distRateNode = pymel.core.createNode( 'multiplyDivide' )
                distRateNode.op.set( 2 )
                
                distNode.distance     >> distRateNode.input1X
                origDistNode.distance >> distRateNode.input2X
                
                addAttr( twoInterPointers[i], ln='multTransX', dv= 0.25, k=1 )
                addAttr( twoInterPointers[i], ln='multTransY', dv= 0.25, k=1 )
                addAttr( twoInterPointers[i], ln='multTransZ', dv= 0.25, k=1 )
                twoInterPointers[i].attr( 'multTransX' ) >> origDirection.input2X
                twoInterPointers[i].attr( 'multTransY' ) >> origDirection.input2Y
                twoInterPointers[i].attr( 'multTransZ' ) >> origDirection.input2Z
                
                multResult = pymel.core.createNode( 'multiplyDivide' )
                origDirection.output >> multResult.input1
                distRateNode.outputX >> multResult.input2X
                distRateNode.outputX >> multResult.input2Y
                distRateNode.outputX >> multResult.input2Z
                
                multResult.output >> twoInterPointers[i].t
    
    return interPointers




def reverseSelection():
    sels = pymel.core.ls( sl=1 )
    sels.reverse()
    pymel.core.select( sels )    




def tangentContraintByStartAndEndUp( inputCurve, inputStartUp, inputEndUp, inputTargets ):
    
    startUp = pymel.core.ls( inputStartUp )[0]
    endUp   = pymel.core.ls( inputEndUp )[0]
    curve   = pymel.core.ls( inputCurve )[0]
    targets = [ pymel.core.ls( inputTarget )[0] for inputTarget in inputTargets ]
    
    startParam = getClosestParamAtPoint( startUp, curve )
    endParam   = getClosestParamAtPoint( endUp, curve )
    
    for target in targets:
        cuParam = getClosestParamAtPoint( target, curve )
        startWeight = ( cuParam - startParam )/( endParam - startParam )
        if startWeight < 0:
            startWeight = 0
        if startWeight > 1:
            startWeight = 1
        
        endWeight = 1.0 - startWeight
        
        tangent = OpenMaya.MVector( *getTangetAtParam( curve, cuParam ) )
        
        localStartUpTangent = tangent * getMMatrix( startUp.wim )
        localEndUpTangent = tangent * getMMatrix( endUp.wim )
        
        avTangent = localStartUpTangent * startWeight + localEndUpTangent * endWeight

        directionIndex = getDirectionIndex( avTangent )
        aim = getVectorList()[ directionIndex ]
        up  = getVectorList()[ (directionIndex + 1)%6 ]
        
        vectorStart = pymel.core.createNode( 'vectorProduct' ); vectorStart.op.set( 3 )
        vectorEnd = pymel.core.createNode( 'vectorProduct' ); vectorEnd.op.set( 3 )
        vectorStart.input1.set( up )
        vectorEnd.input1.set( up )
        multVectorStart = pymel.core.createNode( 'multiplyDivide' ); multVectorStart.input2.set( [endWeight for i in range(3)] )
        multVectorEnd = pymel.core.createNode( 'multiplyDivide' ); multVectorEnd.input2.set( [startWeight for i in range(3)] )
        vectorStart.output >> multVectorStart.input1
        vectorEnd.output >> multVectorEnd.input1
        
        startUp.wm >> vectorStart.matrix
        endUp.wm >> vectorEnd.matrix
        
        sumVector = pymel.core.createNode( 'plusMinusAverage' )
        multVectorStart.output >> sumVector.input3D[0]
        multVectorEnd.output   >> sumVector.input3D[1]
        
        tangentNode = pymel.core.tangentConstraint( curve, target, aim=aim, u=up, wu=up, wut='vector' )
        sumVector.output3D >> tangentNode.attr( 'worldUpVector' )
        
        
        
        
def createDetachPoints( inputCurve, numPoints=2 ):
    
    if numPoints == 0: return None
    curve = pymel.core.ls( inputCurve )[0]
    curveShape = getShape( curve )
    
    minParam = curveShape.minValue.get()
    maxParam = curveShape.maxValue.get()
    
    eachParam = ( maxParam - minParam ) / ( numPoints + 1 )
    
    detachCurveNode = pymel.core.createNode( 'detachCurve' )
    curveShape.local >> detachCurveNode.inputCurve
    
    for i in range( numPoints ):
        cuParam = minParam + eachParam * ( i + 1 )
        curveInfo = pymel.core.createNode( 'pointOnCurveInfo' )
        curveShape.worldSpace >> curveInfo.inputCurve
        
        pointer = pymel.core.createNode( 'transform' )
        pointer.dh.set( 1 )
        addAttr( pointer, ln='param', min=minParam, max=maxParam, k=1, dv=cuParam )
        
        pointer.attr( 'param' ) >> curveInfo.parameter
        
        vectorNode = pymel.core.createNode( 'vectorProduct' )
        vectorNode.op.set( 4 )
        curveInfo.position >> vectorNode.input1
        pointer.pim >> vectorNode.matrix
        vectorNode.output >> pointer.t
        
        pointer.attr( 'param' ) >> detachCurveNode.parameter[i]
    
    for i in range( numPoints+1 ):
        nurbsCurve = pymel.core.createNode( 'nurbsCurve' )
        detachCurveNode.outputCurve[i] >> nurbsCurve.create
        pymel.core.xform( nurbsCurve.getParent(), ws=1, matrix= curve.wm.get() )
        
        
    
def getClosestTransform( inputBase, inputCompairTargets ):
    
    base = pymel.core.ls( inputBase )[0]
    compairTargets = [ pymel.core.ls( inputCompairTarget )[0] for inputCompairTarget in inputCompairTargets ]
    
    closeIndex = 0
    closeDist = 10000000.0
    
    pointBase = getMPoint( pymel.core.xform( base, q=1, ws=1, t=1 ) )
    for i in range( len( compairTargets ) ):
        pointTarget = getMPoint( pymel.core.xform( compairTargets[i], q=1, ws=1, t=1 ) )
        dist = pointBase.distanceTo( pointTarget )
        if dist < closeDist:
            closeDist = dist
            closeIndex = i
    
    return compairTargets[ closeIndex ]




def setMirrorTransform( inputSrcTr, inputDstTr ):
    
    srcTr = pymel.core.ls( inputSrcTr )[0]
    dstTr = pymel.core.ls( inputDstTr )[0]
    
    mirrorMtx = getMirrorMatrix( getMMatrix(srcTr.wm) )
    
    pymel.core.xform( dstTr, ws=1, matrix=matrixToList( mirrorMtx ) )




def makeMirrorTransform( inputTrTarget ):
    
    trTarget = pymel.core.ls( inputTrTarget )[0]
    mirrorTransform = pymel.core.createNode( trTarget.nodeType() )
    mirrorTransform.rename( getOtherSideStr( trTarget.shortName() ) )
    mirrorTransform.dh.set( trTarget.dh.get() )
    setMirrorTransform( trTarget, mirrorTransform )
    
    for shape in trTarget.listRelatives( s=1 ):
        if shape.io.get(): continue
        copyShapeToTransform( shape, mirrorTransform )
        reverseShape( mirrorTransform.getShape() )
    
    targetParent = trTarget.getParent()
    otherSideParentStr = getOtherSideStr( targetParent.name())
    if pymel.core.objExists( otherSideParentStr ):
        pymel.core.parent( mirrorTransform, otherSideParentStr )
    
    return mirrorTransform





def deleteAttr( node, attr ):
    if not pymel.core.attributeQuery( attr, node=node, ex=1 ): return None
    pymel.core.deleteAttr( node + '.' + attr )




def makeMirrorTransformWithHierarchy( inputTrTarget, cloneAttrName = 'mirrorH' ):
    
    trTarget = pymel.core.ls( inputTrTarget )[0]
    otherSideObjStr = getOtherSideStr( trTarget.name() )
    if pymel.core.objExists( otherSideObjStr ):
        cloneObj = pymel.core.ls( otherSideObjStr )[0]
    else:
        cloneObj = makeCloneObject( inputTrTarget, cloneAttrName = cloneAttrName, searchSymmetry=True )
    cloneParents = cloneObj.getAllParents()
    cloneParents.reverse()
    cloneParents.append( cloneObj )
    
    for cloneParent in cloneParents:
        cons = cloneParent.message.listConnections( s=0, d=1 )
        for con in cons:
            if not pymel.core.attributeQuery( cloneAttrName, node=con, ex=1 ): continue
            srcTarget = con
            cloneParent.rename( getOtherSideStr(srcTarget.shortName()) )
            mirrorMatrix = matrixToList( getMirrorMatrix( getMMatrix( srcTarget.wm ) ) )
            pymel.core.xform( cloneParent, ws=1, matrix=mirrorMatrix )
    try:cloneObj.dh.set( trTarget.dh.get() )
    except:pass
    try:cloneObj.v.set( trTarget.v.get() )
    except:pass
    
    for shape in trTarget.listRelatives( s=1 ):
        if shape.io.get(): continue
        copyShapeToTransform( shape, cloneObj )
        reverseShape( cloneObj.getShape() )



def getSourceList( inputNode, nodeList = [] ):
    
    node = pymel.core.ls( inputNode )[0]
    if node in nodeList: return []
    
    nodeList.append( node )
    if node.nodeType() in ['transform','joint']:
        cons = []
        attrs = ['t', 'r', 's']
        attrs += cmds.listAttr( node.name(), k=1 )
        for attr in attrs:
            cons += node.attr( attr ).listConnections( s=1, d=0, p=1, c=1 )
    else:
        cons = node.listConnections( s=1, d=0, p=1, c=1 )
    srcs = cons[1::2]
    
    returnList = [node]
    for origAttr, srcAttr in cons:
        results = getSourceList( srcAttr.node(), nodeList )
        if not results: continue
        returnList += results
    return returnList



def getNameReplaceList( firstName, secondName ):
    
    splitsFirst = firstName.split( '_' )
    splitsSecond = secondName.split( '_' )
    
    diffIndices = []
    for i in range( len( splitsFirst ) ):
        if splitsFirst[i] != splitsSecond[i]:
            diffIndices.append(i)
    
    replaceStrsList = []
    for diffIndex in diffIndices:
        firstStr = splitsFirst[diffIndex]
        secondStr = splitsSecond[diffIndex]
        
        if diffIndex == 0:
            firstStr = firstStr + '_'
            secondStr = secondStr + '_'
        elif diffIndex == len( splitsFirst ) - 1:
            firstStr = '_' + firstStr
            secondStr = '_' + secondStr
        else:
            firstStr = '_' + firstStr + '_'
            secondStr = '_' + secondStr + '_'
        
        replaceStrsList.append( [firstStr, secondStr] )
    
    return replaceStrsList


def copyChildren( source, target ):
    first = source
    firstName = source.shortName()
    secondName = target.shortName()
    
    replaceStrsList = getNameReplaceList(firstName, secondName)
    
    firstChildren = first.listRelatives( c=1, ad=1, type='transform' )
    firstChildren.reverse()
    
    for firstChild in firstChildren:
        childName = firstChild.shortName()
        for replaceSrc, replaceDst in replaceStrsList:
            childName = childName.replace( replaceSrc, replaceDst )
        parentName = firstChild.getParent().shortName()
        for replaceSrc, replaceDst in replaceStrsList:
            parentName = parentName.replace( replaceSrc, replaceDst )
        if not cmds.objExists( parentName ): continue
        exists = False
        if not cmds.objExists( childName ):
            secondChild = pymel.core.createNode( firstChild.nodeType() ).rename( childName )
        else:
            secondChild = pymel.core.ls( childName )[0]
            exists = True
        try:
            pymel.core.parent( secondChild, parentName )
        except: pass
        if not exists: 
            pymel.core.xform( secondChild, os=1, matrix= firstChild.m.get() )
            secondChild.attr( 'dh' ).set( firstChild.attr( 'dh' ).get() )
            if secondChild.nodeType() == 'joint':
                secondChild.attr( 'radius' ).set( firstChild.attr( 'radius' ).get() )




def copyAndPastRig( inputCopyTarget, inputPastTarget, sourceTransformsDicts, mirrorCopy=False ):
    
    copyTarget = pymel.core.ls( inputCopyTarget )[0]
    pastTarget = pymel.core.ls( inputPastTarget )[0]
    
    newDicts = copy.copy( sourceTransformsDicts )
    newDicts[copyTarget.name()] = pastTarget.name()
    
    copyedAttrName = "copyAndPastRig_copyed"

    def getReplacedNode( sourceNode, sourceTransformsDicts ):
        
        addAttr( sourceNode, ln=copyedAttrName, dt='string' )
        copyedObj = sourceNode.attr( copyedAttrName ).get()
        if copyedObj and cmds.objExists( copyedObj ):
            return pymel.core.ls( copyedObj )[0]
        
        destTarget = None
        if sourceTransformsDicts.has_key( sourceNode.shortName() ):
            destTarget = sourceTransformsDicts[ sourceNode.shortName() ]

        print "dest target : ", destTarget
        if destTarget and cmds.objExists( destTarget ):
            return pymel.core.ls( destTarget )[0]
        
        if pymel.core.attributeQuery( 'worldMatrix', node = sourceNode, ex=1 ):
            return sourceNode
        
        srcCons = sourceNode.listConnections( s=1, d=0, p=1, c=1 )
        dstCons = sourceNode.listConnections( s=0, d=1, p=1, c=1 )
        for origCon, srcCon in srcCons:
            srcCon // origCon
        for origCon, dstCon in dstCons:
            origCon // dstCon
        duObj = sourceNode.duplicate()[0]
        for origCon, srcCon in srcCons:
            srcCon >> origCon
        for origCon, dstCon in dstCons:
            origCon >> dstCon
        if mirrorCopy: reverseVector( duObj )
        sourceNode.attr( copyedAttrName ).set( duObj.name() )
        return duObj

    sourceNodes = getSourceList( copyTarget, [] )
    if not sourceNodes: return None
    
    for sourceNode in sourceNodes:
        replacedSourceNode = getReplacedNode( sourceNode, newDicts )
        if not replacedSourceNode: continue
        
        srcCons = sourceNode.listConnections( s=1, d=0, p=1, c=1 )
        dstCons = sourceNode.listConnections( s=0, d=1, p=1, c=1 )
        srcCons = [[ second, first ] for first, second in srcCons ]
        
        for cons in [ srcCons, dstCons ]:
            for start, dest in cons:
                destNode = dest.node()
                startNode = start.node()
                destAttrName = dest.longName()
                startAttrName = start.longName()
                
                replacedDestNode = getReplacedNode( destNode, newDicts )
                replacedStartNode = getReplacedNode( startNode, newDicts )
                
                if not replacedDestNode or not replacedStartNode: continue
                if not replacedDestNode.attr( destAttrName ).listConnections( s=1, d=0 ):
                    replacedStartNode.attr( startAttrName ) >> replacedDestNode.attr( destAttrName )
    
    targets = pymel.core.ls( '*.' + copyedAttrName )
    for target in targets:
        target.node().deleteAttr( copyedAttrName )



def copyRigH( inputSource, inputTarget, mirrorCopy=False ):
    
    source = pymel.core.ls( inputSource )[0]
    target = pymel.core.ls( inputTarget )[0]
    
    sourceName = source.shortName()
    targetName = target.shortName()
    
    replaceStrList = getNameReplaceList(sourceName, targetName)
    
    #copyChildren( source, target )

    sourceChildren = source.listRelatives( c=1, ad=1, type='transform' )
    sourceChildren.append( source )
    
    def reverseVector( inputNode ):
        node = pymel.core.ls( inputNode )[0]
        if node.nodeType() == 'angleBetween':
            vec1 = node.vector1.get()
            node.vector1.set( -vec1[0], -vec1[1], -vec1[2] )
            vec2 = node.vector2.get()
            node.vector2.set( -vec2[0], -vec2[1], -vec2[2] )


    def getReplacedNode( source, replaceStrList ):
        
        sourceName = source.name()
        for srcStr, dstStr in replaceStrList:
            sourceName = sourceName.replace( srcStr, dstStr )
        if sourceName == source.name():
            sourceName = source.name() + '_rigCopyed'
        else:
            if cmds.objExists( sourceName ):
                return pymel.core.ls( sourceName )[0]
        if cmds.objExists( sourceName ): 
            return pymel.core.ls( sourceName )[0]
        
        if pymel.core.attributeQuery( 'worldMatrix', node = source, ex=1 ):
            return source
        
        srcCons = source.listConnections( s=1, d=0, p=1, c=1 )
        dstCons = source.listConnections( s=0, d=1, p=1, c=1 )
        for origCon, srcCon in srcCons:
            try:srcCon // origCon
            except:pass
        for origCon, dstCon in dstCons:
            try:origCon // dstCon
            except:pass
        try:duObjs = source.duplicate( n=sourceName )
        except:duObjs = [source]
        for origCon, srcCon in srcCons:
            try:srcCon >> origCon
            except:pass
        for origCon, dstCon in dstCons:
            try:origCon >> dstCon
            except:pass
        if mirrorCopy: reverseVector( duObjs[0] )
        return duObjs[0]
    
    for i in range( len( sourceChildren ) ):
        sourceNodes = getSourceList( sourceChildren[i], [] )
        if not sourceNodes: continue
        for sourceNode in sourceNodes:
            replacedSourceNode = getReplacedNode( sourceNode, replaceStrList )
            if not replacedSourceNode: continue
            
            srcCons = sourceNode.listConnections( s=1, d=0, p=1, c=1 )
            dstCons = sourceNode.listConnections( s=0, d=1, p=1, c=1 )
            srcCons = [[ second, first ] for first, second in srcCons ]

            for cons in [ srcCons, dstCons ]:
                for start, dest in cons:
                    destNode = dest.node()
                    startNode = start.node()
                    destAttrName = dest.longName()
                    startAttrName = start.longName()
                    replacedDestNode  = getReplacedNode( destNode, replaceStrList )
                    replacedStartNode = getReplacedNode( startNode, replaceStrList )
                    if not replacedDestNode or not replacedStartNode: continue
                    try:
                        if not replacedDestNode.attr( destAttrName ).listConnections( s=1, d=0 ):
                            replacedStartNode.attr( startAttrName ) >> replacedDestNode.attr( destAttrName )
                    except:pass
    
    duNodes = cmds.ls( '*_rigCopyed' )
    for duNode in duNodes:
        cmds.rename( duNode, duNode.replace( '_rigCopyed', '' ) )





def convertDestinationConnectionsToReverse( inputAttr ):
    
    tagetAttr = pymel.core.ls( inputAttr )[0]
    
    def getReverseOutputAttr( pymelAttr ):
        try: 
            pymelAttr.getChildren()
            mdNodes = pymelAttr.listConnections( s=0, d=1, type='multiplyDivide' )
            targetMdNode = None
            if mdNodes:
                targetMdNodes = [ mdNode for mdNode in mdNodes if list(mdNode.input2.get()) == [-1,-1,-1] ]
                if targetMdNodes: targetMdNode = targetMdNodes[0]
            if not targetMdNode:
                targetMdNode = pymel.core.createNode( 'multiplyDivide' )
                pymelAttr >> targetMdNode.input1
                targetMdNode.input2.set( -1,-1,-1 )
            return targetMdNode.output
        except:
            multNodes = pymelAttr.listConnections( s=0, d=1, type='multDoubleLinear' )
            targetMultNode = None
            if multNodes:
                targetMultNodes = [ multNode for multNode in multNodes if multNode.input2.get() == -1 ]
                if targetMultNodes: targetMultNode = targetMultNodes[0]
            if not targetMultNode:
                targetMultNode = pymel.core.createNode( 'multDoubleLinear' )
                pymelAttr >> targetMultNode.input1
                targetMultNode.input2.set( -1 )
            return targetMultNode.output

    dstAttrs = tagetAttr.listConnections( s=0, d=1, p=1 )
    if not dstAttrs: return None
    reverseOutputAttr = getReverseOutputAttr( tagetAttr )
    targetDstAttrs = [ dstAttr for dstAttr in dstAttrs if dstAttr.node() != reverseOutputAttr.node() ]
    for targetDstAttr in targetDstAttrs:
        reverseOutputAttr >> targetDstAttr



def getAngleNode( inputVectorAttr, baseVector = None ):
    
    vectorAttr = pymel.core.ls( inputVectorAttr )[0]
    if not baseVector:
        dirIndex = getDirectionIndex( vectorAttr.get() )
        baseVector = getVectorList()[ dirIndex ]
    
    angleNode = pymel.core.createNode( 'angleBetween' )
    angleNode.vector1.set( baseVector )
    vectorAttr >> angleNode.vector2
    
    return angleNode
    


def getLocalAngleNode( inputTr, inputParentTr ):
    
    tr = pymel.core.ls( inputTr )[0]
    parentTr = pymel.core.ls( inputParentTr )[0]
    dcmp = getLocalDecomposeMatrix( tr.wm, parentTr.wim )
    return getAngleNode( dcmp.ot )
    
    
    


def getInnerObjectsOnMesh( transforms, mesh ):
    
    meshShape = getShape( mesh )
    oMesh = getMObject( meshShape )
    
    meshIntersector = OpenMaya.MMeshIntersector()
    meshIntersector.create( oMesh )
    
    meshInverseMatrix = getWorldMatrix( meshShape ).inverse()
    
    pointOnMesh = OpenMaya.MPointOnMesh()
    
    innerObjects = []
    for transform in transforms:
        localPosition = getWorldPosition( transform ) * meshInverseMatrix
        meshIntersector.getClosestPoint( localPosition, pointOnMesh )
        normal = pointOnMesh.getNormal()
        closePos = pointOnMesh.getPoint()
        
        vPos = OpenMaya.MFloatVector( localPosition - OpenMaya.MPoint( closePos ) )
        if vPos * normal < 0:
            innerObjects.append( transform )
    return innerObjects
        
        
        

def setComposeMatrixValueFromTransform( inputTrObject, inputCompose ):
    
    trObject = pymel.core.ls( inputTrObject )[0]
    compose = pymel.core.ls( inputCompose )[0]
    
    values = getTransformFromMatrix( trObject.wm )
    
    compose.it.set( values[:3] )
    compose.ir.set( values[3:6] )
    compose.inputScale.set( values[6:9] )
    compose.inputShear.set( values[9:] )





def getLocalMapFolder():
    
    sceneName = cmds.file( q=1, sceneName=1 )
    sceneFolder = os.path.dirname( sceneName )
    mapfolder = sceneFolder + '/maps'
    makeFolder( mapfolder )
    return mapfolder





def printCurvePoints( crv ):

    crvShape = getShape( crv )
    returnStr = "["
    for i in range( crvShape.numCVs() ):
        returnStr += str( crvShape.controlPoints[i].get() ) + ",\n"
    returnStr = returnStr[:-2] + "]"
    print returnStr



def getParentNameOf( target, searchName ):
    
    longNameTarget = pymel.core.ls( target, l=1 )[0].longName()
    
    splits = longNameTarget.split( '|' )
    
    targetIndex = -1
    for i in range( len( splits ) ):
        if splits[i].find( searchName ) == -1: continue
        targetIndex = i
    if targetIndex == -1: return None
    
    return '|'.join( splits[:targetIndex+1] ) 



def lockParent( inputTarget ):
    
    target = pymel.core.ls( inputTarget )[0].getParent()
    if not target: return None
    keyAttrs = cmds.listAttr( target.name(), k=1 )
    for attr in keyAttrs:
        target.attr( attr ).set( lock=1 )


def unlockParent( inputTarget ):
    
    target = pymel.core.ls( inputTarget )[0].getParent()
    if not target: return None
    keyAttrs = cmds.listAttr( target.name(), k=1 )
    for attr in keyAttrs:
        target.attr( attr ).set( lock=0 )



def renameParent( inputTarget ):
    
    target = pymel.core.ls( inputTarget )[0]
    target.getParent().rename( 'P' + target.nodeName() )



def renameShape( inputTarget ):
    
    target = pymel.core.ls( inputTarget )[0]
    targetShapes = target.listRelatives( s=1 )
    
    if len( targetShapes ) == 1:
        targetShapes[0].rename( target.nodeName() + 'Shape' )
    for i in range( len( targetShapes ) ):
        targetShapes[i].rename( target.nodeName() + 'Shape%02d' % i )




def setAttrDefault( sels, **options ):
    
    attrs = []
    targetIsKeyAttrs = False
    
    if options.has_key( 'attrs' ):
        attrs = options['attrs']
    if options.has_key( 'k' ):
        if options['k']:
            targetIsKeyAttrs = True
    
    for sel in sels:
        if targetIsKeyAttrs:
            keyAttrs = cmds.listAttr( sel, k=1 )
            for attr in keyAttrs:
                defaultValue = cmds.attributeQuery( attr, node=sel, ld=1 )
                try:cmds.setAttr( sel + '.' + attr, defaultValue[0] )
                except:pass
        for attr in attrs:
            defaultValue = cmds.attributeQuery( attr, node=sel, ld=1 )
            try:cmds.setAttr( sel + '.' + attr, defaultValue[0] )
            except:pass


class SliderBase:
    
    def __init__(self):

        pass
    

    def create(self, axis=None, *args ):
    
        axisX = True
        axisY = True
        
        if axis:
            axisX = False
            axisY = False
            if axis == 'x': axisX = True
            elif axis == 'y': axisY = True
            elif axis == 'xy': axisX = True; axisY = True
    
        baseData = [[-.5,-.5,0],[.5,-.5,0],[.5,.5,0],[-.5,.5,0],[-.5,-.5,0]]
        baseCurve = pymel.core.curve( p=baseData, d=1 )
        baseCurveOrigShape=  addIOShape( baseCurve )
        baseCurveShape = baseCurve.getShape()
        
        trGeo = pymel.core.createNode( 'transformGeometry' )
        composeMatrix = pymel.core.createNode( 'composeMatrix' )
        
        if axisX:
            multNodeX = pymel.core.createNode( 'multDoubleLinear' );multNodeX.setAttr( 'input2', 0.5 )
            addNodeX = pymel.core.createNode( 'addDoubleLinear' );addNodeX.setAttr( 'input2', 1 )
            addAttr( baseCurve, ln='slideSizeX', min=0, cb=1 )
            baseCurve.slideSizeX >> multNodeX.input1
            baseCurve.slideSizeX >> addNodeX.input1
            addNodeX.output >> composeMatrix.inputScaleX
            multNodeX.output >> composeMatrix.inputTranslateX
        
        if axisY:
            multNodeY = pymel.core.createNode( 'multDoubleLinear' );multNodeY.setAttr( 'input2', 0.5 )
            addNodeY = pymel.core.createNode( 'addDoubleLinear' );addNodeY.setAttr( 'input2', 1 )
            addAttr( baseCurve, ln='slideSizeY', min=0, cb=1 )
            baseCurve.slideSizeY >> multNodeY.input1
            baseCurve.slideSizeY >> addNodeY.input1
            addNodeY.output >> composeMatrix.inputScaleY
            multNodeY.output >> composeMatrix.inputTranslateY
        
        composeMatrix.outputMatrix >> trGeo.transform
        baseCurveOrigShape.local >> trGeo.inputGeometry
        trGeo.outputGeometry >> baseCurveShape.create

        return baseCurve



def createTextureFileNode( filePath ):
    
    fileNode = pymel.core.shadingNode( "file", asTexture=1 )
    place2d  = pymel.core.shadingNode( "place2dTexture", asUtility=1 )
    
    fileNode.attr( 'fileTextureName' ).set( filePath, type='string' )
    
    place2d.coverage >> fileNode.coverage
    place2d.translateFrame  >> fileNode.translateFrame 
    place2d.rotateFrame  >> fileNode.rotateFrame 
    place2d.mirrorU  >> fileNode.mirrorU 
    place2d.mirrorV  >> fileNode.mirrorV
    place2d.stagger >> fileNode.stagger
    place2d.wrapU >> fileNode.wrapU
    place2d.wrapV >> fileNode.wrapV
    place2d.repeatUV >> fileNode.repeatUV
    place2d.offset >> fileNode.offset
    place2d.rotateUV >> fileNode.rotateUV
    place2d.noiseUV >> fileNode.noiseUV
    place2d.vertexUvOne >> fileNode.vertexUvOne
    place2d.vertexUvTwo >> fileNode.vertexUvTwo
    place2d.vertexUvThree >> fileNode.vertexUvThree
    place2d.vertexCameraOne >> fileNode.vertexCameraOne
    place2d.outUV >> fileNode.uv
    place2d.outUvFilterSize >> fileNode.uvFilterSize
    
    return fileNode.name(), place2d.name()




def getActiveProjectionMatrix():
    
    activeView = OpenMayaUI.M3dView.active3dView()
    dagCam = OpenMaya.MDagPath()
    
    activeView.getCamera( dagCam )
    
    projMtx = OpenMaya.MMatrix()
    activeView.projectionMatrix( projMtx )
    
    width = activeView.portWidth()
    height = activeView.portHeight()
    
    return dagCam.inclusiveMatrixInverse() * projMtx





def createInvertMesh( inputTargetMesh, inputSkinedMesh ):
    
    targetMesh = pymel.core.ls( inputTargetMesh )[0]
    skinedMesh = pymel.core.ls( inputSkinedMesh )[0]
    
    skinClusters = getNodeFromHistory( skinedMesh, 'skinCluster' )
    if not skinClusters: return None
    
    skinCluster = skinClusters[0]
    
    def getWeightList( skinCluster ):
        
        weightList = [ None for i in range( skinCluster.weightList.numElements() ) ]
        for i in range( skinCluster.weightList.numElements() ):
            weightsPlug = skinCluster.weightList[i].children()[0]
            weightsDict = {}
            for j in range( weightsPlug.numElements() ):
                targetElement = weightsPlug.elementByPhysicalIndex( j )
                weightsDict.update( {targetElement.logicalIndex():targetElement.get()} )
                weightList[i] = weightsDict
        return weightList

    def getMatrixList( skinCluster ):
        
        matrixList = {}
        for i in range( skinCluster.matrix.numElements() ):
            matrixPlug = skinCluster.matrix.elementByPhysicalIndex( i )
            matrixList[ matrixPlug.logicalIndex() ] = listToMatrix( matrixPlug.get() )
        return matrixList
    
    def getBindPreList( skinCluster ):
        
        bindPreList = {}
        for i in range( skinCluster.bindPreMatrix.numElements() ):
            bindPrePlug = skinCluster.bindPreMatrix.elementByPhysicalIndex( i )
            bindPreList[ bindPrePlug.logicalIndex() ] = listToMatrix( bindPrePlug.get() )
        return bindPreList

    weightList = getWeightList( skinCluster )
    matrixList = getMatrixList( skinCluster )
    bindPreList = getBindPreList( skinCluster )
    geoMtx = listToMatrix( skinCluster.geomMatrix.get() )
    
    vtxMultMtxList = [ None for i in range( skinCluster.weightList.numElements() ) ]
    for i in range( skinCluster.weightList.numElements() ):
        weightsDict = weightList[i]
        keys = weightsDict.keys()
        jointMultedMtx = reduce( lambda x, y : x + y,  [ bindPreList[mtxIndex] * matrixList[mtxIndex] * weightsDict[ mtxIndex ] for mtxIndex in keys ] )
        vtxMultMtxList[i] = ( geoMtx * jointMultedMtx * geoMtx.inverse() ).inverse()
    
    duTargetMesh = pymel.core.duplicate( targetMesh )[0]
    duTargetMeshShape = duTargetMesh.getShape()
    
    dagPathMesh = getDagPath( duTargetMeshShape )
    fnMesh = OpenMaya.MFnMesh( dagPathMesh )
    origPoints = OpenMaya.MPointArray()
    fnMesh.getPoints( origPoints )
    resultPoints = OpenMaya.MPointArray()
    resultPoints.setLength( origPoints.length() )
    
    for i in range( fnMesh.numVertices() ):
        resultPoints.set( origPoints[i] * vtxMultMtxList[i], i )
    
    fnMesh.setPoints( resultPoints )
        


def makeOffsetBlendMatrixToMovedCtl( inputCtl ):
    
    ctl = pymel.core.ls( inputCtl )[0]
    offsetCtl = makeParent( ctl )
    offsetCtl.rename( 'Offset_' + ctl.nodeName() )
    
    composeDefault = pymel.core.createNode( 'composeMatrix' )
    composeOffset  = pymel.core.createNode( 'composeMatrix' )
    
    composeOffset.it.set( offsetCtl.t.get() )
    composeOffset.ir.set( offsetCtl.r.get() )
    
    blendMatrixNode = createBlendTwoMatrixNode( composeDefault.outputMatrix, composeOffset.outputMatrix )
    
    addAttr( offsetCtl, ln='blend', min=0, max=1, k=1, dv=1 )
    offsetCtl.attr( 'blend' ) >> blendMatrixNode.blend
    
    dcmp = getDecomposeMatrix( blendMatrixNode.matrixSum )
    dcmp.ot >> offsetCtl.t
    dcmp.outputRotate >> offsetCtl.r
    
    


def cutCurve( inputCurve, inputMesh ):
    
    curve = pymel.core.ls( inputCurve )[0].name()
    mesh   = pymel.core.ls( inputMesh )[0].name()
        
    mesh = cmds.listRelatives( mesh, s=1, f=1 )[0]
    fnMesh = OpenMaya.MFnMesh( getDagPath( mesh ) )
    meshIntersector = OpenMaya.MMeshIntersector()
    meshIntersector.create( fnMesh.object() )
    meshMtx  = fnMesh.dagPath().inclusiveMatrix()
    
    curveShape = cmds.listRelatives( curve, s=1, f=1 )[0]
    
    fnCurve = OpenMaya.MFnNurbsCurve( getDagPath( curveShape ) )
    curveMtx = fnCurve.dagPath().inclusiveMatrix()
    
    multMtx = curveMtx * meshMtx.inverse()
    
    numSpans = fnCurve.numSpans()
    degree   = fnCurve.degree()
    
    minParam = fnCurve.findParamFromLength( 0.0 )
    maxParam = fnCurve.findParamFromLength( fnCurve.length() )
    
    eachParam = (maxParam-minParam) / ( numSpans*10-1 )
    
    pointOnMesh = OpenMaya.MPointOnMesh()
    
    pointInCurve = OpenMaya.MPoint();
    pointInMesh = OpenMaya.MPoint();

    closestParam = 0.0;

    for i in range( numSpans*10 ):
        targetParam = eachParam * i + minParam
        fnCurve.getPointAtParam( targetParam, pointInCurve )
        pointInCurve*= multMtx
        meshIntersector.getClosestPoint( pointInCurve, pointOnMesh )
        normal = pointOnMesh.getNormal()
        pointInMesh = OpenMaya.MVector( pointOnMesh.getPoint() )
        
        if OpenMaya.MVector( pointInCurve - pointInMesh ) * OpenMaya.MVector( normal ) > 0:
            closestParam = targetParam
            break
    
    currentParam = targetParam
    
    if closestParam != 0:
        
        pointInCurvePlus = OpenMaya.MPoint()
        pointInCurveMinus = OpenMaya.MPoint()
        pointOnMeshPlus = OpenMaya.MPointOnMesh()
        pointOnMeshMinus = OpenMaya.MPointOnMesh()
        
        for i in range( 10 ):
            currentParamPlus  = currentParam + eachParam
            currentParamMinus = currentParam - eachParam
            
            if currentParamMinus < minParam: currentParamMinus = minParam
            
            fnCurve.getPointAtParam( currentParamPlus, pointInCurvePlus )
            fnCurve.getPointAtParam( currentParamMinus, pointInCurveMinus )
            pointInCurvePlus *= multMtx
            pointInCurveMinus *= multMtx
            meshIntersector.getClosestPoint( pointInCurvePlus, pointOnMeshPlus )
            meshIntersector.getClosestPoint( pointInCurveMinus, pointOnMeshMinus )
            pointInMeshPlus = OpenMaya.MPoint( pointOnMeshPlus.getPoint() )
            pointInMeshMinus = OpenMaya.MPoint( pointOnMeshMinus.getPoint() )
            
            if pointInMeshPlus.distanceTo( pointInCurvePlus ) < pointInMeshMinus.distanceTo( pointInCurveMinus ):
                currentParam = currentParamPlus
            else:
                currentParam = currentParamMinus
            
            if currentParam < minParam:
                currentParam = minParam
            if currentParam > maxParam:
                currentParam  = maxParam
            
            eachParam *= 0.5
    
    detachNode = cmds.createNode( 'detachCurve' )
    cmds.setAttr( detachNode+'.parameter[0]', currentParam )
    
    cutCurve  = cmds.createNode( 'nurbsCurve' )
    cutCurveP = cmds.listRelatives( cutCurve, p=1, f=1 )[0]
    
    cmds.connectAttr( curveShape+'.local', detachNode+'.inputCurve' )
    cmds.connectAttr( detachNode+'.outputCurve[1]', cutCurve+'.create' )
    
    if currentParam < 0.0001:
        fnCurve.getPointAtParam( currentParam, pointInCurve )
        pointInCurve*= multMtx
        meshIntersector.getClosestPoint( pointInCurve, pointOnMesh )
        pointClose = OpenMaya.MPoint( pointOnMesh.getPoint() ) * multMtx.inverse()
        cmds.move( pointClose.x, pointClose.y, pointClose.z, cutCurveP+'.cv[0]', os=1 )
    else:
        cmds.rebuildCurve( cutCurveP, ch=1, rpo=1, rt=0, end=1, kr=2, kcp=0, kep=1, kt=0, s=numSpans, degree=degree, tol=0.01 )

    cmds.DeleteHistory( cutCurveP )
    cmds.xform( cutCurveP, ws=1, matrix = matrixToList( curveMtx ) )

    curveName = curve.split( '|' )[-1]
    cutCurveP = cmds.rename( cutCurveP, curveName+'_cuted' )

    return pymel.core.ls( cutCurveP )[0]



def createControllerByCurveCVs( inputCurve ):

    curve = pymel.core.ls( inputCurve )[0]
    cvs = pymel.core.ls( curve + '.cv[*]', fl=1 )
    numControl = len( cvs )/2
    
    controlInfos = [ {} for i in range( numControl ) ]
    
    startCtlCenterPos = getMVector( pymel.core.xform( cvs[0], q=1, ws=1, t=1 ) )
    startCtlStartPos  = getMVector( pymel.core.xform( cvs[0], q=1, ws=1, t=1 ) )
    startCtlEndPos    = getMVector( pymel.core.xform( cvs[1], q=1, ws=1, t=1 ) )
    
    endCtlCenterPos = getMVector( pymel.core.xform( cvs[-1], q=1, ws=1, t=1 ) )
    endCtlStartPos  = getMVector( pymel.core.xform( cvs[-2], q=1, ws=1, t=1 ) )
    endCtlEndPos    = getMVector( pymel.core.xform( cvs[-1], q=1, ws=1, t=1 ) )
    
    labelCenter = 'centerPos'
    labelStart  = 'startPos'
    labelEnd    = 'endPos'
    
    controlInfos[0][labelCenter] = startCtlCenterPos
    controlInfos[0][labelStart] = startCtlStartPos
    controlInfos[0][labelEnd] = startCtlEndPos
    
    controlInfos[-1][labelCenter] = endCtlCenterPos
    controlInfos[-1][labelStart] = endCtlStartPos
    controlInfos[-1][labelEnd] = endCtlEndPos
    
    for i in range( 2, len( cvs )-2, 2 ):
        controlIndex = (i+1)/2
        startPos  = getMVector( pymel.core.xform( cvs[i], q=1, ws=1, t=1 ) )
        endPos    = getMVector( pymel.core.xform( cvs[i+1],  q=1, ws=1, t=1 ) )
        centerPos = ( startPos + endPos )/2
        controlInfos[ controlIndex ][labelCenter] = centerPos
        controlInfos[ controlIndex ][labelStart] = startPos
        controlInfos[ controlIndex ][labelEnd] = endPos
    
    
    baseMatrix = listToMatrix( getDefaultMatrix() )
    baseVector = None
    
    pointerList = []
    parentCtl = None
    
    ctls = []


    for i in range( len( controlInfos ) ):
        
        controlInfo = controlInfos[i]
        startPos = controlInfo[ labelStart ]
        endPos   = controlInfo[ labelEnd ]
        centerPos = controlInfo[ labelCenter ]
        
        dirVector = ( endPos - startPos ) * baseMatrix.inverse()
        if not baseVector:
            baseVector = getMVector( getVectorList()[ getDirectionIndex( dirVector ) ] )
        
        rotatedMatrix = baseVector.rotateTo( dirVector ).asMatrix() * baseMatrix
        worldRot = getRotateFromMatrix( rotatedMatrix )
        
        ctl = pymel.core.circle( normal=[ baseVector.x, baseVector.y, baseVector.z ] )[0]
        ctl.rename( 'Ctl_%s_%02d' % ( curve.name(), i ) )
        pCtl = makeParent( ctl )
        
        pymel.core.xform( pCtl, ws=1, t = [ centerPos.x, centerPos.y, centerPos.z ] )
        pymel.core.xform( pCtl, ws=1, ro= worldRot )
        
        baseMatrix = rotatedMatrix
        
        pointerStart = pymel.core.createNode( 'transform', n = 'pointer_%s_%02d_start' % ( curve.name(), i ) )
        pointerEnd   = pymel.core.createNode( 'transform', n = 'pointer_%s_%02d_end' % ( curve.name(), i ) )
        
        pointerStart.t.set( startPos.x, startPos.y, startPos.z )
        pointerEnd.t.set( endPos.x, endPos.y, endPos.z )
        pointerStart.setParent( ctl )
        pointerEnd.setParent( ctl )
        
        pointerList += [ pointerStart, pointerEnd ]
        
        if parentCtl:
            pCtl.setParent( parentCtl )
        parentCtl = ctl
        ctls.append( ctl )


    def convertPointersToInterPointer( pointers, ctls ):
        
        for pointer in pointers:
            ctl = pointer.getParent()
            ctlIndex =  ctls.index( ctl )
            
            startCtl = ctls[ ctlIndex-1 if ctlIndex-1 > 0 else 0 ]
            endCtl   = ctls[ ctlIndex+1 if ctlIndex+1 < len(ctls)-1 else len(ctls)-1 ]
            
            startCtlPos = OpenMaya.MPoint( *pymel.core.xform( startCtl, q=1, ws=1, t=1 ) )
            endCtlPos   = OpenMaya.MPoint( *pymel.core.xform( endCtl, q=1, ws=1, t=1 ) )
            pointerPos = OpenMaya.MPoint( *pymel.core.xform( pointer, q=1, ws=1, t=1 ) )
            
            startCtlDist = startCtlPos.distanceTo( pointerPos )
            endCtlDist   = endCtlPos.distanceTo( pointerPos )
            
            if startCtlDist < 0.00001 or endCtlDist < 0.00001: continue
            
            if ctl == startCtl: targetCtl = endCtl
            elif ctl == endCtl : targetCtl = startCtl
            else: targetCtl = startCtl if startCtlDist < endCtlDist else endCtl
            
            dcmp = getDecomposeMatrix( getMultMatrix( targetCtl.wm, ctl.wim ).o )
            origValue = pointer.t.get()
            dcmpValue = dcmp.ot.get()
            multNode = pymel.core.createNode( 'multiplyDivide' )
            dcmp.ot >> multNode.input1
            multNode.input2.set( origValue[0]/dcmpValue[0] if dcmpValue[0] !=0 else 1, origValue[1]/dcmpValue[1] if dcmpValue[1] !=0 else 1, origValue[2]/dcmpValue[2] if dcmpValue[2] !=0 else 1 )
            multNode.output >> pointer.t

    convertPointersToInterPointer( pointerList, ctls )

    newCurve = makeCurveFromObjects( *pointerList )
    getSourceConnection( curve.getShape(), newCurve.getShape() )
    pymel.core.delete( newCurve )
    
    return ctls




def createBoundingBoxCubeConnected( inputGrp ):
    
    grp = pymel.core.ls( inputGrp )[0]
    polyCube = pymel.core.polyCube()[0]
    bbcNode = pymel.core.createNode( 'plusMinusAverage' )
    bbcNode.op.set( 3 )
    
    grp.attr( 'boundingBoxMin' ) >> bbcNode.input3D[0]
    grp.attr( 'boundingBoxMax' ) >> bbcNode.input3D[1]
    bbcNode.output3D >> polyCube.t
    grp.attr( 'boundingBoxSizeX' ) >> polyCube.sx
    grp.attr( 'boundingBoxSizeY' ) >> polyCube.sy
    grp.attr( 'boundingBoxSizeZ' ) >> polyCube.sz
    
    polyCube.rename( grp.nodeName() + '_boundingBoxCube' )
    
    return polyCube
    
    
    


def createSquashBendLatticeRig( meshGrp, latticeDiv = 5 ):
    
    worldGeoGrp = createWorldGeometryGroup( meshGrp )
    bbCube = createBoundingBoxCubeConnected( worldGeoGrp ); bbCube.getShape().v.set( 0 )
    worldGeoGrp.v.set( lock=1 )
    cloneGrp = makeCloneObjectGroup( meshGrp, connectionOn=1, shapeOn=1 )

    ffd, lattice, latticeBase = pymel.core.lattice( cloneGrp,  divisions=[2,latticeDiv,2], objectCentered=True, ldv=[2, latticeDiv+1, 2] )
    pymel.core.parent( lattice, latticeBase, bbCube )
    
    lattice.t.set( 0,0,0 ); lattice.r.set( 0,0,0 ); lattice.s.set( 1,1,1 ); lattice.sh.set( 0,0,0 )
    latticeBase.t.set( 0,0,0 ); latticeBase.r.set( 0,0,0 ); latticeBase.s.set( 1,1,1 ) ; latticeBase.sh.set( 0,0,0 )
    
    bindPrePointers = []
    jnts = []
    bindPreObjs = []
    for i in range( latticeDiv ):
        tr = pymel.core.createNode( 'transform' ); tr.dh.set( 1 )
        tr.setParent( bbCube )
        y = 1.0 / ( latticeDiv-1 ) * i - 0.5
        tr.t.set( 0, y, 0 )
        tr.s.set( 1,1,1 )
        bindPrePointers.append( tr )
    
        circle = pymel.core.circle( radius=0.5, normal=[0,1,0] )
        pCircle = makeParent( circle )
        pCircle.setParent( bbCube )
        
        tr.t >> pCircle.t
        pCircle.s.set( 1,1,1 )
        
        pymel.core.select( circle )
        jnt = pymel.core.joint()
        jnt.radius.set( 0.1 )
        jnts.append( jnt )
        bindPreObjs.append( tr )
        
        jnt.attr( 'drawStyle' ).set( 2 )
    
    pymel.core.skinCluster( jnts, lattice, tsb=1, dr=100 )
    for i in range( len( jnts ) ):
        connectBindPreMatrix( jnts[i], bindPreObjs[i], lattice)
        
    
    
    
def createConnectedGeoFromReferenceGeo( mainGrp ):
    
    duGrp = pymel.core.duplicate( mainGrp )[0]
    pymel.core.refresh()
    duGrpMeshs = [ target for target in duGrp.listRelatives( c=1, ad=1, type='transform' ) if target.getShape() and target.getShape().nodeType() == 'mesh' ]
    for mesh in duGrpMeshs:
        setPntsZero( mesh )
    mainChildren = pymel.core.listRelatives( mainGrp, c=1, ad=1, type='transform' )
    mainChildren.append( mainGrp )
    
    duChildren = pymel.core.listRelatives( duGrp, c=1, ad=1, type='transform' )
    duChildren.append( duGrp )
    
    for i in range( len( mainChildren ) ):
        mainChild = mainChildren[i]
        duChild = duChildren[i]
    
        mainChild.t >> duChild.t
        mainChild.r >> duChild.r
        mainChild.s >> duChild.s
    
        mainChildShape = mainChild.getShape()
        duChildShape = duChild.getShape()
    
        if not mainChildShape: continue
    
        if mainChildShape.nodeType() == 'mesh':
            mainChildShape.outMesh >> duChildShape.inMesh
        elif mainChildShape.nodeType() in ['nurbsCurve', 'nurbsSurface']:
            mainChildShape.local >> duChildShape.create
    
    

