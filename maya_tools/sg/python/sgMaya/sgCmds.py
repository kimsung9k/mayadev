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



def getOrderedEdgeRings( targetEdge ):
    
    targetEdge = pymel.core.ls( targetEdge )[0].name()
    
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
    if not nodeShape: return 0
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



def copyWeightToSmoothedMesh( inputSrcMesh, inputSmoothedMesh ):

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
    
    matrixPlugSrc    = fnSkinClusterSrc.findPlug( 'matrix' )
    matrixPlugTarget = fnSkinClusterTarget.findPlug( 'matrix' )
    weightListPlugSrc    = fnSkinClusterSrc.findPlug( 'weightList' )
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
            vtxnames.append( smoothedMesh + '.vtx[%d]' % i )
            continue
        else:
            othreVtxNames.append( smoothedMesh + '.vtx[%d]' % i )
        
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
        vtxnames.append( smoothedMesh + '.vtx[%d]' % i )

    return smoothedMesh, othreVtxNames
    
        


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
        
        returnTargets.append( [mDagPath, mIntArrU, mIntArrV, mIntArrW] )
    
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
        cmds.connectAttr( curveShape + '.local', curveInfo + '.inputCurve' )
        cmds.setAttr( curveInfo + '.top', 1 )
        cmds.setAttr( curveInfo + '.parameter', i / float( numPoints ) )
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



def rigWithEdgeRing( inputEdges, inputBaseTransform ):
    
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
    print "loopCurves :", len( loopCurves )
    for loopCurve in loopCurves:
        points = createPointsFromCurve( loopCurve, 4 )
        pointsList.append( points )
    centers = []
    for points in pointsList:
        center = createCenterPoint( points )
        centers.append( center )
    
    curve = makeCurveFromSelection( *centers, d=2 )
    origAttrName, currentAttrName = addCurveDistanceInfo(curve)
    scaleNode = cmds.createNode( 'multiplyDivide' )
    cmds.setAttr( scaleNode + '.op', 2 )
    
    print curve + '.' + currentAttrName
    #print cmds.ls( curve + '.' + currentAttrName )
    
    cmds.connectAttr( curve + '.' + currentAttrName, scaleNode + '.input1X' )
    cmds.connectAttr( curve + '.' + origAttrName, scaleNode + '.input2X' )
    
    jntCenters = [ cmds.createNode( 'joint' ) for i in range( len(centers) ) ]
    
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
    
    cmds.parent( loopCurves , centers, jntCenters, curve, allPoints, baseTransform )




def getWeightInfoFromVertex( skinedVtx ):
    
    meshName = skinedVtx.split( '.' )[0]
    vtxId = int( skinedVtx.split( 'vtx[' )[-1].replace( ']', '' ) )
    
    skinNode = getNodeFromHistory( meshName, 'skinCluster' )[0]
    fnSkinNode = OpenMaya.MFnDependencyNode( getMObject( skinNode ) )
    
    plugWeights = fnSkinNode.findPlug( 'weightList' )[vtxId].child(0)
    
    
    weightInfos = []
    for i in range( plugWeights.numElements() ):
        cons = cmds.listConnections( skinNode + '.matrix[%d]' % plugWeights[i].logicalIndex(), s=1, d=0, type='joint')
        weight = plugWeights[i].asFloat()
        if not cons: continue
        weightInfos.append( [cons[0], weight] )
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






