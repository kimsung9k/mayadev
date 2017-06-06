import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import pymel.core
import math, copy
import os
import math


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
    
    if type( inputTarget ) in [str, unicode]:
        target = inputTarget
    else:
        target = inputTarget.name()
    
    mObject = OpenMaya.MObject()
    selList = OpenMaya.MSelectionList()
    selList.add( target )
    selList.getDependNode( 0, mObject )
    return mObject



def getDagPath( inputTarget ):
    
    if type( inputTarget ) in [str, unicode]:
        target = inputTarget
    else:
        target = inputTarget.name()
    
    dagPath = OpenMaya.MDagPath()
    selList = OpenMaya.MSelectionList()
    selList.add( target )
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



def separateParentConnection( node, attrName ):
    
    if not type( node ) in [ str, unicode ]:
        node = node.name()
    parentAttr = cmds.attributeQuery( attrName, node=node, listParent=1 )
    
    if parentAttr:
        cons = cmds.listConnections( node+'.'+parentAttr[0], s=1, d=0, p=1, c=1 )
        if cons:
            cmds.disconnectAttr( cons[1], cons[0] )
            srcAttr = cons[1]
            srcNode, srcParentAttr = srcAttr.split( '.' )
            srcAttrs = cmds.attributeQuery( srcParentAttr, node=srcNode, listChildren=1 )
            dstAttrs = cmds.attributeQuery( parentAttr[0], node=node,    listChildren=1 )
            for i in range( len( srcAttrs ) ):
                if cmds.connectAttr( srcNode+'.'+srcAttrs[i], node+'.'+dstAttrs[i] ): continue
                cmds.connectAttr( srcNode+'.'+srcAttrs[i], node+'.'+dstAttrs[i], f=1 )


    
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



def getOrderedEdgeRings( targetEdge ):
    cmds.select( targetEdge )
    cmds.SelectEdgeRingSp()
    ringEdges = cmds.ls( sl=1, fl=1 )
    oppasitEdges = []
    
    meshName = targetEdge.split( '.' )[0]
    dagPathMesh = getDagPath( meshName )
    itEdgeMesh = OpenMaya.MItMeshEdge( dagPathMesh )
    itPolygon  = OpenMaya.MItMeshPolygon( dagPathMesh )
    
    util = OpenMaya.MScriptUtil()
    util.createFromInt( 0 )
    prevIndex = util.asIntPtr()
    
    for edge in ringEdges:
        edgeIndex = int( edge.split( '[' )[-1].replace( ']', '' ) )
        itEdgeMesh.setIndex( edgeIndex, prevIndex )
        faces = OpenMaya.MIntArray()
        connectedEdges = OpenMaya.MIntArray()
        itEdgeMesh.getConnectedFaces( faces )
        itEdgeMesh.getConnectedEdges( connectedEdges )
        
        resultEdges = []
        for i in range( faces.length() ):
            edgesFromFace = OpenMaya.MIntArray()
            itPolygon.setIndex( faces[i], prevIndex )
            itPolygon.getEdges( edgesFromFace )
            for j in range( edgesFromFace.length() ):
                if edgesFromFace[j] == edgeIndex: continue
                exists = False
                for k in range( connectedEdges.length() ):
                    if edgesFromFace[j] == connectedEdges[k]: 
                        exists=True
                        break
                if exists: continue
                resultEdges.append( meshName + '.e[%d]' % edgesFromFace[j] )
        oppasitEdges.append( resultEdges )

    for i in range( len( ringEdges ) ):
        if len( oppasitEdges[i] ) == 1:
            break
    
    nextIndex = ringEdges.index( oppasitEdges[i][0] )
    orderedEdges = [ ringEdges[i], ringEdges[ nextIndex ] ]
    
    startNum = 0
    while len( oppasitEdges[ nextIndex ]  )== 2:
        edges = oppasitEdges[ nextIndex ]
        exists = False
        for edge in edges:
            if not edge in orderedEdges:
                orderedEdges.append( edge )
                exists = True
                break
        if not exists: break
        nextIndex = ringEdges.index( edge )
        startNum += 1
    
    return orderedEdges



def getNumVertices( inputNode ):
    
    node = pymel.core.ls( inputNode )[0]
    nodeShape = None
    if node.type() == 'transform':
        nodeShape = node.getShape()
    else:
        nodeShape = node
    dagPath = getDagPath( nodeShape )
    fnMesh = OpenMaya.MFnMesh( dagPath )
    return fnMesh.numVertices()




def copyShader( first, second ):
    
    if not cmds.objExists( first ): return None
    if not cmds.objExists( second ): return None
    
    firstShape = cmds.listRelatives( first, s=1, f=1 )[0]
    secondShape = cmds.listRelatives( second, s=1, f=1 )[0]
    engines = cmds.listConnections( firstShape, type='shadingEngine' )
    if not engines: return None
    
    engines = list( set( engines ) )
    
    for engine in engines:
        shaders = cmds.listConnections( engine+'.surfaceShader', s=1, d=0 )
        if not shaders: continue
        shader = shaders[0]
        cmds.hyperShade( objects = shader )
        selObjs = cmds.ls( sl=1, l=1 )
        
        targetObjs = []
        for selObj in selObjs:
            if selObj.find( '.' ) != -1:
                trNode, components = selObj.split( '.' )
                if trNode == first:
                    targetObjs.append( second+'.'+components )
            elif selObj == firstShape:
                targetObjs.append( secondShape )
        
        if not targetObjs: continue
        
        for targetObj in targetObjs:
            cmds.sets( targetObj, e=1, forceElement=engine )
    


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
        connectTrans = options['cr']
    
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
