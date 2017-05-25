import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import pymel.core
import math, copy
import os
from sgModules import sgdata
from sgModules.sgobjects import *
from sgModules.sgbase import *



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




def getDirection( inputVector ):
    
    return [ [1,0,0], [0,1,0], [0,0,1], [-1,0,0], [0,-1,0], [0,0,-1] ][getDirectionIndex( inputVector )]


    
    
    
def matrixToList( matrix ):
    if type( matrix ) == list:
        return matrix
    mtxList = range( 16 )
    for i in range( 4 ):
        for j in range( 4 ):
            mtxList[ i * 4 + j ] = matrix( i, j )
    return mtxList



def listToMatrix( mtxList ):
    if type( mtxList ) == OpenMaya.MMatrix:
        return mtxList
    matrix = OpenMaya.MMatrix()
    OpenMaya.MScriptUtil.createMatrixFromList( mtxList, matrix  )
    return matrix





def rotateToMatrix( rotation ):
    
    import math
    rotX = math.radians( rotation[0] )
    rotY = math.radians( rotation[1] )
    rotZ = math.radians( rotation[2] )
    
    trMtx = OpenMaya.MTransformationMatrix()
    trMtx.rotateTo( OpenMaya.MEulerRotation( OpenMaya.MVector(rotX, rotY, rotZ) ) )
    return trMtx.asMatrix()





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





def convertSideString( string ):
    
    import copy
    converted = copy.copy( string )
    if string.find( '_L_' ) != -1:
        converted = string.replace( '_L_', '_R_' )
    elif string.find( '_R_' ) != -1:
        converted = string.replace( '_R_', '_L_' )
    return converted




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




def getOtherSideName( nodeName ):
    
    if nodeName.find( '_L_' ):
        return nodeName.replace( '_L_', '_R_' )
    elif nodeName.find( '_R_' ):
        return nodeName.replace( '_R_', '_L_' )
    return nodeName




def makeFolder( pathName ):
    
    pathName = pathName.replace( '\\', '/' )
    splitPaths = pathName.split( '/' )
    
    cuPath = splitPaths[0]
    
    folderExist = True
    for i in range( 1, len( splitPaths ) ):
        checkPath = cuPath+'/'+splitPaths[i]
        if not os.path.exists( checkPath ):
            os.chdir( cuPath )
            os.mkdir( splitPaths[i] )
            folderExist = False
        cuPath = checkPath
        
    if folderExist: return None
        
    return pathName


def makeFile( filePath ):
    if os.path.exists( filePath ): return None
    filePath = filePath.replace( "\\", "/" )
    splits = filePath.split( '/' )
    folder = '/'.join( splits[:-1] )
    makeFolder( folder )
    f = open( filePath, "w" )
    f.close()



def reloadModules( pythonPath='' ):

    import os, imp, sys
    
    if not pythonPath:
        pythonPath = __file__.split( '\\' )[0]
    
    for root, folders, names in os.walk( pythonPath ):
        root = root.replace( '\\', '/' )
        for name in names:
            try:onlyName, extension = name.split( '.' )
            except:continue
            if extension.lower() != 'py': continue
            
            if name == '__init__.py':
                fileName = root
            else:
                fileName = root + '/' + name
                
            moduleName = fileName.replace( pythonPath, '' ).split( '.' )[0].replace( '/', '.' )[1:]
            moduleEx =False
            try:
                sys.modules[moduleName]
                moduleEx = True
            except:
                pass
            
            if moduleEx:
                try:reload( sys.modules[moduleName] )
                except:pass



def listNodes( *args, **options ):
    
    nodes = cmds.ls( *args, **options )
    
    sgNodes = []
    for node in nodes:
        sgNodes.append( convertSg( node ) )
    
    return sgNodes



def listConnections( *args, **options ):
    
    newArgs = convertArgs( args )
    cons = cmds.listConnections( *newArgs, **options )
    if not cons: return []
    
    sgcons = []
    for con in cons:
        if con.find( '.' ) != -1:
            sgcons.append( SGAttribute( con ) )
        else:
            sgcons.append( SGNode( con ) )
    
    return sgcons




def select( *args, **options ):
    
    allList = []
    for arg in args:
        if type( arg ) in [ list, tuple ]:
            allList += list( arg )
        else:
            allList.append( arg )
    
    for i in range( len( allList ) ):
        allList[i] = convertName( allList[i] )

    cmds.select( *allList, **options )




def getConstrainMatrix( first, target ):
    
    first = convertSg( first )
    target = convertSg( target )
    
    mmFirstAttr = first.wm.listConnections( type='multMatrix', p=1 )
    mmSecondAttr = target.pim.listConnections( type="multMatrix", p=1 )
    
    mm = None
    if mmFirstAttr and mmSecondAttr:
        mmFirstAttr = mmFirstAttr[0]
        mmSecondAttr = mmSecondAttr[0]
        if mmFirstAttr.attrName() in ["matrixIn[0]","i[0]"] and mmSecondAttr.attrName() in ["matrixIn[1]","i[1]"]:
            if mmFirstAttr.nodeName() == mmSecondAttr.nodeName():
                node = mmFirstAttr.node()
                if not node.i[1].listConnections():
                    mm = node
    
    if not mm:
        mm = createNode( 'multMatrix' )
        first.wm >> mm.i[0]
        target.pim >> mm.i[1]
    
    return mm



@convertSg_dec
def constrain_point( first, target ):
    
    mm = getConstrainMatrix( first, target )
    dcmp = getDecomposeMatrix( mm )
    cmds.connectAttr( dcmp + '.ot', target + '.t', f=1 )



@convertSg_dec
def constrain_rotate( first, target ):
    
    mm = getConstrainMatrix( first, target )
    dcmp = getDecomposeMatrix( mm )
    cmds.connectAttr( dcmp + '.or', target + '.r', f=1 )




@convertSg_dec
def constrain_scale( first, target ):
    
    mm = getConstrainMatrix( first, target )
    dcmp = getDecomposeMatrix( mm )
    cmds.connectAttr( dcmp + '.os', target + '.s', f=1 )




@convertSg_dec
def constrain_parent( first, target ):
    
    mm = getConstrainMatrix( first, target )
    dcmp = getDecomposeMatrix( mm )
    cmds.connectAttr( dcmp + '.ot',  target + '.t', f=1 )
    cmds.connectAttr( dcmp + '.or',  target + '.r', f=1 )



@convertSg_dec
def constrain_tangent( curve, upObject, target, **options ):
    
    curveShape = curve.shape()
    pointOnCurve = createNode( 'pointOnCurveInfo' )
    curveShape.attr( 'worldSpace' ) >> pointOnCurve.inputCurve
    nearNode = getNearPointOnCurve( target, curve )
    paramValue = nearNode.parameter.get()
    delete( nearNode )
    
    pointOnCurve.parameter.set( paramValue )
    
    vectorProduct = createNode( 'vectorProduct' ).setAttr( 'operation', 3 ).setAttr( 'input1', 0,1,0 )
    upObject.wm >> vectorProduct.matrix
    
    fbf = createNode( 'fourByFourMatrix' )
    pointOnCurve.tangentX >> fbf.in00
    pointOnCurve.tangentY >> fbf.in01
    pointOnCurve.tangentZ >> fbf.in02
    vectorProduct.outputX >> fbf.in10
    vectorProduct.outputY >> fbf.in11
    vectorProduct.outputZ >> fbf.in12
    mm = createNode( 'multMatrix' )
    fbf.output >> mm.i[0]
    target.pim >> mm.i[1]
    fbfDcmp = getDecomposeMatrix( mm )
    cmds.connectAttr( fbfDcmp + '.or',  target + '.r' )



@convertSg_dec
def constrain_onCurve( curve, upObject, target, **options ):
    
    curveShape = curve.shape()
    pointOnCurve = createNode( 'pointOnCurveInfo' )
    curveShape.attr( 'worldSpace' ) >> pointOnCurve.inputCurve
    nearNode = getNearPointOnCurve( target, curve )
    position = cmds.xform( target.name(), ws=1, q=1, t=1 )[:3]
    nearNode.inPosition.set( position )
    paramValue = nearNode.parameter.get()
    delete( nearNode )
    
    pointOnCurve.parameter.set( paramValue )
    
    vectorProduct = createNode( 'vectorProduct' ).setAttr( 'operation', 3 ).setAttr( 'input1', 0,1,0 )
    upObject.wm >> vectorProduct.matrix
    
    fbf = createNode( 'fourByFourMatrix' )
    pointOnCurve.tangentX >> fbf.in00
    pointOnCurve.tangentY >> fbf.in01
    pointOnCurve.tangentZ >> fbf.in02
    vectorProduct.outputX >> fbf.in10
    vectorProduct.outputY >> fbf.in11
    vectorProduct.outputZ >> fbf.in12
    pointOnCurve.positionX >> fbf.in30
    pointOnCurve.positionY >> fbf.in31
    pointOnCurve.positionZ >> fbf.in32
    mm = createNode( 'multMatrix' )
    fbf.output >> mm.i[0]
    target.pim >> mm.i[1]
    dcmp = createNode( 'decomposeMatrix' )
    mm.o >> dcmp.imat
    dcmp.outputRotate >> target.r
    dcmp.outputTranslate >> target.t
    
    




@convertSg_dec
def constrain_all( first, target ):
    
    mm = getConstrainMatrix( first, target )
    dcmp = getDecomposeMatrix( mm )
    cmds.connectAttr( dcmp + '.ot', target + '.t' )
    cmds.connectAttr( dcmp + '.or', target + '.r' )
    cmds.connectAttr( dcmp + '.os', target + '.s' )
    cmds.connectAttr( dcmp + '.osh', target + '.sh' )
    
    

@convertName_dec
def parent( *args, **options ):
    parentedTargets = cmds.parent( *args, **options )
    for target in parentedTargets:
        if cmds.nodeType( target ) == 'joint':
            freezeJoint( target )
    return convertSg( parentedTargets )



def xform( *args, **options ):
    sgnodeNames = []
    for arg in args:
        sgnodeNames.append( convertSg( arg ).name() )
    return cmds.xform( *sgnodeNames, **options )



def isConnected( *args, **options ):
    srcAttr = SGAttribute( args[0] )
    dstAttr = SGAttribute( args[1] )
    return cmds.isConnected( srcAttr.name(), dstAttr.name(), **options )


@convertSg_dec
def getOutputMatrixAttribute( node ):
    targetAttr = None
    if node.nodeType() == 'transform':
        targetAttr = node.worldMatrix
    elif node.nodeType() in ['multMatrix', 'wtAddMatrix', 'addMatrix']:
        targetAttr = node.matrixSum
    elif node.nodeType() in ['composeMatrix', 'transposeMatrix', 'inverseMatrix']:
        targetAttr = node.outputMatrix
    
    return targetAttr


@convertSg_dec
def getOutputVectorAttribute( node ):
    targetAttr = None
    if node.nodeType() in ["transform", "joint"]:
        targetAttr = node.translate
    elif node.nodeType() in ["decomposeMatrix"]:
        targetAttr = node.outputTranslate
    return targetAttr



@convertSg_dec
def createLocalMatrix( localTarget, parentTarget ):
    
    multMatrixNode = createNode( 'multMatrix' )
    
    localTarget.matrixOutput() >> multMatrixNode.i[0]
    parentTarget.wim >> multMatrixNode.i[1]
    
    return multMatrixNode




@convertSg_dec
def getLocalMatrix( localTarget, parentTarget ):
    
    multMatrixNodes = localTarget.matrixOutput().listConnections( d=1, s=0, type='multMatrix' )
    for multMatrixNode in multMatrixNodes:
        firstAttr = multMatrixNode.i[0].listConnections( s=1, d=0, p=1 )
        secondAttr = multMatrixNode.i[1].listConnections( s=1, d=0, p=1 )
        thirdConnection = multMatrixNode.i[2].listConnections( s=1, d=0 )
        
        if not firstAttr or not secondAttr or thirdConnection: continue
        
        firstEqual = firstAttr[0].node() == localTarget and firstAttr[0].attrName() in ["wm", "worldMatrix"]
        secondEqual = secondAttr[0].node() == parentTarget and secondAttr[0].attrName() in ["wim", "worldInverseMatrix"]
        
        if firstEqual and secondEqual:
            select( multMatrixNode )
            return multMatrixNode
    
    return createLocalMatrix( localTarget, parentTarget )




def getLocalDecomposeMatrix( localTarget, parentTarget ):
    return getDecomposeMatrix( getLocalMatrix( localTarget, parentTarget ) )




@convertSg_dec
def opptimizeConnection( node ):
    
    srcAttrs = listConnections( node, s=1, d=0, p=1 )
    dstAttrs = listConnections( node, s=0, d=1, p=1 )
    
    if len( srcAttrs ) != 1 or len( dstAttrs ) != 1: return None
    
    if not isConnected( srcAttrs[0], dstAttrs[0] ):
        try:
            srcAttrs[0] >> dstAttrs[0]
        except:
            pass



def getConstrainedObject( node, messageName = '' ):
    
    messageAttr = None
    if messageName:
        messageAttr = node.attr( messageName )
        if not messageAttr:
            messageAttr = node.addAttr( ln=messageName, at='message' )
    
    targetNode = None
    if messageAttr:
        connectedNodes = messageAttr.listConnections( s=0, d=1, type='transform' )
        if connectedNodes:
            targetNode = connectedNodes[0]




@convertSg_dec
def getDecomposeMatrix( node ):
    
    if isinstance( node, SGDagNode ):
        outputMatrixAttr = node.worldMatrix
    else:
        outputMatrixAttr = node.matrixOutput()

    if outputMatrixAttr:
        destNodes = outputMatrixAttr.listConnections( s=0, d=1, type='decomposeMatrix' )
        if destNodes: return destNodes[0]
        decomposeMatrixNode = createNode( 'decomposeMatrix' )
        outputMatrixAttr >> decomposeMatrixNode.imat
        return decomposeMatrixNode




@convertSg_dec
def getDistance( node ):
    distNode = createNode( 'distanceBetween' )
    if node.nodeType() in ['transform', 'joint' ]:
        node.t >> distNode.point1
    if node.nodeType() == "decomposeMatrix":
        node.outputTranslate >> distNode.point1
    elif node.nodeType() in ['composeMatrix', 'transposeMatrix', 'inverseMatrix','multMatrix', 'wtAddMatrix', 'addMatrix']:
        getOutputMatrixAttribute(node) >> distNode.matrix1
    return distNode




@convertSg_dec
def createLookAtMatrix( lookTarget, rotTarget ):
    
    mm = createNode( 'multMatrix' )
    compose = createNode( 'composeMatrix' )
    mm2 = createNode( 'multMatrix' )
    invMtx = createNode( 'inverseMatrix' )
    
    lookTarget.wm >> mm.i[0]
    rotTarget.t >> compose.it
    compose.outputMatrix >> mm2.i[0]
    rotTarget.pm >> mm2.i[1]
    mm2.matrixSum >> invMtx.inputMatrix
    invMtx.outputMatrix >> mm.i[1]
    return mm




@convertSg_dec
def getLookAtAngleNode( lookTarget, rotTarget, **options ):

    def getLookAtMatrixNode( lookTarget, rotTarget ):
    
        consLookTarget = lookTarget.wm.listConnections( type="multMatrix", p=1 )
        return createLookAtMatrix( lookTarget, rotTarget )
    
    if options.has_key( 'direction' ) and options['direction']:
        direction = options['direction']
    else:
        direction = [1,0,0]
    
    lookTarget = convertSg( lookTarget )
    rotTarget = convertSg( rotTarget )
    
    dcmpLookAt = getDecomposeMatrix( getLookAtMatrixNode( lookTarget, rotTarget ) )
    
    abnodes = cmds.listConnections( dcmpLookAt.name(), type='angleBetween' )
    if not abnodes:
        node = cmds.createNode( 'angleBetween' )
        cmds.setAttr( node + ".v1", *direction )
        cmds.connectAttr( dcmpLookAt + '.ot', node + '.v2' )
    else:
        node = abnodes[0]
    return node


def lookAtConnect( lookTarget, rotTarget, **options ):
    
    if options.has_key( 'direction' ) and options['direction']:
        direction = options['direction']
    else:
        direction = None
    
    sgLookTarget = convertSg( lookTarget )
    sgRotTarget = convertSg( rotTarget )
    
    if not direction:
        pRotTarget = sgRotTarget.parent()
        if pRotTarget:
            wim = listToMatrix( pRotTarget.wim.get() )
        else:
            wim = OpenMaya.MMatrix()
        pos = OpenMaya.MPoint( *sgLookTarget.xform( q=1, ws=1, t=1 ) )
        directionIndex = getDirectionIndex( pos*wim )
        direction = [[1,0,0], [0,1,0], [0,0,1],[-1,0,0], [0,-1,0], [0,0,-1]][directionIndex]
    
    node = getLookAtAngleNode( lookTarget, rotTarget, direction=direction )
    cmds.connectAttr( node + '.euler', rotTarget + '.r' )




@convertSg_dec
def makeChild( target ):
    trNode = createNode( 'transform' )
    parent( trNode, target )
    trNode.setTransformDefault()
    return trNode



@convertSg_dec
def makeLookAtChild( lookTarget, pRotTarget, **options ):
    rotTarget = makeChild( pRotTarget )
    if options.has_key( 'n' ):
        rotTarget.rename( options['n'] )
    elif options.has_key( 'name' ):
        rotTarget.rename( options['name'] )
    lookAtConnect( lookTarget, rotTarget, **options )
    return rotTarget.name()











@convertSg_dec
def createBlendTwoMatrixNode( first, second, **options ):
    
    wtAddMtx = createNode( 'wtAddMatrix' )
    wtAddMtx.addAttr( ln='blend', min=0, max=1, dv=0.5, k=1 )
    
    revNode  = createNode( 'reverse' )
    
    local = False
    if options.has_key('local') and options['local']:
        local = True
    
    if first.nodeType() == 'multMatrix':
        firstAttr = first.matrixSum
    else:
        if local:
            firstAttr = first.m
        else:
            firstAttr = first.wm
        
    if second.nodeType() == 'multMatrix':
        secondAttr = second.matrixSum
    else:
        if local:
            secondAttr = second.m
        else:
            secondAttr = second.wm

    firstAttr >> wtAddMtx.i[0].m
    secondAttr >> wtAddMtx.i[1].m
    
    wtAddMtx.blend >> revNode.inputX
    revNode.outputX >> wtAddMtx.i[0].w
    wtAddMtx.blend >> wtAddMtx.i[1].w
    
    return wtAddMtx



@convertSg_dec
def getBlendTwoMatrixNode( first, second, **options ):

    local = False
    if options.has_key('local') and options['local']:
        local = True
    
    if first.nodeType() == 'multMatrix':
        firstAttr = first.matrixSum
    else:
        if local:
            firstAttr = first.m
        else:
            firstAttr = first.wm
    
    firstConnected = firstAttr.listConnections( type='wtAddMatrix', p=1 )
    
    if firstConnected:
        cons = firstConnected[0].node().i[1].m.listConnections( s=1, d=0 )
        if cons and cons[0] == second:
            select( firstConnected[0].node() )
            return firstConnected[0].node()

    wtAddMtx = createBlendTwoMatrixNode( first, second, **options )
    select( wtAddMtx )
    return wtAddMtx




@convertSg_dec
def blendTwoMatrix( first, second, target, **options ):
    
    connectBlendTwoMatrix(first, second, target, **options)




@convertSg_dec
def connectBlendTwoMatrix( first, second, target, **options ):

    if options.has_key( 'local' ):
        blendNode = createBlendTwoMatrixNode( first, second, local='local' )
        dcmp = getDecomposeMatrix( blendNode )
    else:
        blendNode = createBlendTwoMatrixNode( first, second )
        mm = createNode( 'multMatrix' )
        blendNode.matrixOutput() >> mm.i[0]
        target.pim >> mm.i[1]
        dcmp = getDecomposeMatrix( mm )
    
    trConnect = False
    roConnect = False
    scaleConnect = False
    
    if options.has_key( 'ct' ):
        trConnect = options['ct']
    if options.has_key( 'cr' ):
        roConnect = options['cr']
    if options.has_key( 'cs' ):
        scaleConnect = options['cs']
    
    if trConnect: cmds.connectAttr( dcmp + '.ot', target + '.t' )
    if roConnect: cmds.connectAttr( dcmp + '.or', target + '.r' )
    if scaleConnect: cmds.connectAttr( dcmp + '.os', target + '.s' )
    
    target.addAttr( ln='blend', min=0, max=1, k=1, dv=0.5 )
    target.blend >> blendNode.blend



@convertSg_dec
def createBlendMatrix( *args, **options ):
    
    constObjs = args[:-1]
    target = args[-1]
    
    isLocal = False
    if options.has_key( 'local' ):
        isLocal = options['local']
    
    wtAddMtx = createNode( 'wtAddMatrix' )
    plusNode = createNode( 'plusMinusAverage' )
    if isLocal :
        outDcmp = getDecomposeMatrix( wtAddMtx )
    else:
        outMM    = createNode( 'multMatrix' )
        wtAddMtx.o >> outMM.i[0]
        target.pim >> outMM.i[1]
        outDcmp = getDecomposeMatrix( outMM )
    
    for i in range( len(constObjs) ):
        constObj = constObjs[i]
        if options.has_key('mo') and options['mo']:
            constChild = constObj.makeChild('_Offset')
            constChild.xform( ws=1, matrix= target.wm.get() )
            constMatrixAttr = constChild.wm
        elif isLocal:
            constMatrixAttr = constObj.m
        else:
            constMatrixAttr = constObj.wm
        
        divNode = createNode( 'multiplyDivide' )
        divNode.op.set( 2 )
        
        target.addAttr( ln='constWeight_%d' % i, k=1, dv=1 )
        target.attr( 'constWeight_%d' % i ) >> plusNode.attr( 'input1D[%d]' % i )
        target.attr( 'constWeight_%d' % i ) >> divNode.attr( 'input1X' )
        plusNode.attr( 'output1D' ) >> divNode.input2X
        
        constMatrixAttr >> wtAddMtx.attr( 'i[%d].m' % i )
        divNode.outputX >> wtAddMtx.attr( 'i[%d].w' % i )
    
    outDcmp.outputRotate >> target.r
   



@convertSg_dec
def addBlendMatrix( *args, **options ):
    
    constObjs = args[:-1]
    target = args[-1]
    
    wtAddMtx = target.getNodeFromHistory( 'wtAddMatrix' )
    averages = target.getNodeFromHistory( 'plusMinusAverage' )
    
    if not averages:
        createBlendMatrix( *args, **options )
        return 0
    
    multNodes = wtAddMtx[0].listConnections( s=1, type='multiplyDivide' )
    length = len( multNodes )
    
    for i in range( len( constObjs ) ):
        cuNumber = length + i
        target.addAttr( ln='constWeight_%d' % cuNumber, k=1 )
        
        divNode = createNode( 'multiplyDivide' ).setAttr( 'op', 2 )
        
        target.attr( 'constWeight_%d' % cuNumber ) >> averages[0].input1D[cuNumber]
        target.attr( 'constWeight_%d' % cuNumber ) >> divNode.input1X
        averages[0].output1D >> divNode.input2X
        
        if options.has_key( 'mo' ) and options['mo']:
            constChild = constObjs[i].makeChild('_Offset')
            constChild.xform( ws=1, matrix= target.wm.get() )
            constAttr = constChild.wm
        else:
            constAttr = constObjs[i].wm
            
        constAttr >> wtAddMtx[0].i[cuNumber].m
        divNode.outputX >> wtAddMtx[0].i[cuNumber].w
    return length


def getAngle( node, axis=[1,0,0] ):
    
    node = convertSg( node )
    
    outputAttr = node.vectorOutput()
    connectedAttrs = outputAttr.listConnections( s=0, d=1, p=1, type='angleBetween' )
    
    conectedindex = None
    for i in range( len( connectedAttrs ) ):
        value = connectedAttrs[i].node().attr( 'vector1' ).get()
        if OpenMaya.MVector(*axis) * OpenMaya.MVector( *value ) > 0.999:
            conectedindex = i
            break
    
    if conectedindex == None:
        angleNode = createNode("angleBetween")
        angleNode.vector1.set( *axis )
        outputAttr >> angleNode.vector2
        return angleNode
    else:
        targetNode = connectedAttrs[conectedindex].node()
        select( targetNode )
        return targetNode



@convertSg_dec
def getFbfMatrix( *args ):
    
    xNode = args[0]
    yNode = args[1]
    zNode = args[2]
    
    if isinstance( xNode, SGAttribute ):
        xAttr = xNode
    else:
        xAttr = xNode.vectorOutput()
    
    if isinstance( yNode, SGAttribute ):
        yAttr = yNode
    else:
        yAttr = yNode.vectorOutput()
    
    if isinstance( zNode, SGAttribute ):
        zAttr = zNode
    else:
        zAttr = zNode.vectorOutput()
    
    fbfMtx = createNode( 'fourByFourMatrix' )
    xAttr[0] >> fbfMtx.attr('in00')
    xAttr[1] >> fbfMtx.attr('in01')
    xAttr[2] >> fbfMtx.attr('in02')
    yAttr[0] >> fbfMtx.attr('in10')
    yAttr[1] >> fbfMtx.attr('in11')
    yAttr[2] >> fbfMtx.attr('in12')
    zAttr[0] >> fbfMtx.attr('in20')
    zAttr[1] >> fbfMtx.attr('in21')
    zAttr[2] >> fbfMtx.attr('in22')
    
    return fbfMtx



@convertSg_dec
def getCrossVectorNode( *args ):
    
    first = args[0]
    second = args[1]
    
    if isinstance( first, SGAttribute ):
        firstAttr = first
    else:
        firstAttr = first.vectorOutput()
    
    if isinstance( second, SGAttribute ):
        secondAttr = second
    else:
        secondAttr = second.vectorOutput()
    
    crossVector = createNode( 'vectorProduct' )
    crossVector.attr( 'op' ).set( 2 )
    
    firstAttr  >> crossVector.attr( 'input1' )
    secondAttr >> crossVector.attr( 'input2' )
    
    return crossVector



@convertSg_dec
def replaceConnection( *args ):
    
    first = args[0] 
    second = args[1] 
    target = args[2]
    
    cons = target.listConnections( s=1, d=0, p=1, c=1 )
    for i in range( 0, len(cons), 2 ):
        con = cons[i+1]
        dest = cons[i]
        
        splits = con.split( '.' )
        node = splits[0]
        attr = '.'.join( splits[1:] )
        
        if con.node() != first: continue 
        cmds.connectAttr( second + '.' + attr, dest.name(), f=1 )



@convertSg_dec
def freezeJoint( joint ):
    
    import math
    mat = listToMatrix( cmds.getAttr( joint + '.m' ) )
    rot = OpenMaya.MTransformationMatrix( mat ).eulerRotation().asVector()
    joint.attr( 'jo' ).set( math.degrees( rot.x ), math.degrees( rot.y ), math.degrees( rot.z ) )
    joint.attr( 'r' ).set( 0,0,0 )
    


@convertSg_dec
def freezeByParent( target ):

    pTarget = target.listRelatives( p=1 )[0]
    xform( pTarget, ws=1, matrix = cmds.getAttr( target + '.wm' ) )
    target.setTransformDefault()
    



@convertSg_dec
def setCenter( sel ):
    
    import math
    import copy
    
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
    
    sel.setPosition( trans.x, trans.y, trans.z, ws=1 )
    sel.setOrient( math.degrees(rot.x), math.degrees(rot.y), math.degrees(rot.z), ws=1 )



@convertSg_dec
def setMirror( sel ):

    matList = sel.wm.get()
    matList[1]  *= -1
    matList[2]  *= -1
    matList[5]  *= -1
    matList[6]  *= -1
    matList[9]  *= -1
    matList[10]  *= -1
    matList[12] *= -1
    sel.xform( ws=1, matrix= matList )




@convertSg_dec
def setSymmetryToOther( src, trg ):
    
    matList = src.wm.get()
    matList[1]  *= -1
    matList[2]  *= -1
    matList[4]  *= -1
    matList[8]  *= -1
    matList[12] *= -1
    
    if trg.nodeType() == 'joint':
        trg.xform( ws=1, matrix = matList )
        worldMatrix = listToMatrix( matList )
        joValue = trg.attr( 'jo' ).get()
        joRadValue = [ math.radians( joValue[0]), math.radians( joValue[1]), math.radians( joValue[2]) ]
        joMtx = OpenMaya.MEulerRotation( OpenMaya.MVector( *joRadValue ) ).asMatrix()
        pMtx = listToMatrix( trg.attr( 'pm' ).get() )
        localRotMtx = worldMatrix * pMtx.inverse() * joMtx.inverse()
        trMtx = OpenMaya.MTransformationMatrix( localRotMtx )
        rotValue = trMtx.eulerRotation().asVector()
        rotDegValue = [ math.degrees( rotValue[0] ), math.degrees( rotValue[1] ), math.degrees( rotValue[2] ) ]
        #print 'rot deg value : ', rotDegValue
        trg.r.set( *rotDegValue )
    else:
        trg.xform( ws=1, matrix= matList )

    



@convertSg_dec
def setMirrorLocal( sel ):

    matList = sel.m.get()
    matList[1]  *= -1
    matList[2]  *= -1
    matList[4]  *= -1
    matList[8]  *= -1
    matList[12] *= -1
    mtx = listToMatrix( matList )
    trMtx = OpenMaya.MTransformationMatrix( mtx )
    rotValue = trMtx.eulerRotation().asVector()
    rotList = [math.degrees(rotValue.x), math.degrees(rotValue.y), math.degrees(rotValue.z)]
    
    if cmds.nodeType( sel.name() ) == 'joint':
        joValue = sel.jo.get()
        joMtx = getMatrixFromRotate( joValue )
        rotMtx = getMatrixFromRotate( rotList )
        localRotMtx = rotMtx * joMtx.inverse()
        rotList = getRotateFromMatrix( localRotMtx )
    
    sel.xform( os=1, ro=rotList )
    sel.tx.set( -sel.tx.get() )





@convertSg_dec
def setCenterMirrorLocal( sel ):

    matList = sel.m.get()
    matList[1]  *= 0
    matList[2]  *= 0
    matList[4]  *= 0
    matList[8]  *= 0
    matList[12] *= 0
    
    xVector = OpenMaya.MVector( matList[0], matList[1], matList[2] )
    yVector = OpenMaya.MVector( matList[4], matList[5], matList[6] )
    xVector.normalize()
    yVector.normalize()
    zVector = xVector ^ yVector
    
    matList[0] = xVector.x; matList[1] = xVector.y; matList[2] = xVector.z
    matList[4] = yVector.x; matList[5] = yVector.y; matList[6] = yVector.z
    matList[8] = zVector.x; matList[9] = zVector.y; matList[10] = zVector.z
    
    mtx = listToMatrix( matList )
    trMtx = OpenMaya.MTransformationMatrix( mtx )
    rotValue = trMtx.eulerRotation().asVector()
    rotList = [math.degrees(rotValue.x), math.degrees(rotValue.y), math.degrees(rotValue.z)]
    
    sel.tx.set( 0 )
    
    if cmds.nodeType( sel.name() ) == 'joint':
        joValue = sel.jo.get()
        joMtx = getMatrixFromRotate( joValue )
        rotMtx = getMatrixFromRotate( rotList )
        localRotMtx = rotMtx * joMtx.inverse()
        rotList = getRotateFromMatrix( localRotMtx )
    
    sel.xform( os=1, ro=rotList )




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




def getTransformFromMatrix( mtxValue ):
    
    printMatrix( listToMatrix(mtxValue) )
    trMtx = OpenMaya.MTransformationMatrix( listToMatrix(mtxValue) )
    rotValue = trMtx.eulerRotation().asVector()
    trValue = trMtx.getTranslation( OpenMaya.MSpace.kObject )
    scriptUtil = OpenMaya.MScriptUtil()
    scriptUtil.createFromList( [1.0,1.0,1.0], 3 )
    doublePtr = scriptUtil.asDoublePtr()
    trMtx.getScale( doublePtr, OpenMaya.MSpace.kTransform )
    sValueX = OpenMaya.MScriptUtil.getDoubleArrayItem( doublePtr, 0 )
    sValueY = OpenMaya.MScriptUtil.getDoubleArrayItem( doublePtr, 1 )
    sValueZ = OpenMaya.MScriptUtil.getDoubleArrayItem( doublePtr, 2 )
    return trValue.x, trValue.y, trValue.z, rotValue.x, rotValue.y, rotValue.z, sValueX, sValueY, sValueZ



def printMatrix( mtxValue ):
    
    for i in range( 4 ):
        print "%5.3f, %5.3f, %5.3f, %5.3f" %( mtxValue(i,0), mtxValue(i,1), mtxValue(i,2), mtxValue(i,3) )
    print



@convertSg_dec
def getLookAtMatrixValue( aimTarget, rotTarget, **options ):
    
    rotWorldMatrix = listToMatrix( rotTarget.wm.get() )
    aimWorldMatrix = listToMatrix( aimTarget.wm.get() )
    localAimTarget = aimWorldMatrix * rotWorldMatrix.inverse()
    localAimPos    = OpenMaya.MPoint( localAimTarget[3] )
    direction = OpenMaya.MVector( localAimPos ).normal()
    
    directionIndex = getDirectionIndex( direction )
    
    baseDir = None
    if options.has_key( 'direction' ):
        baseDir = OpenMaya.MVector( *options[ 'direction' ] ).normal()
    
    if not baseDir:
        baseDir = [[1,0,0], [0,1,0], [0,0,1], [-1,0,0], [0,-1,0], [0,0,-1]][directionIndex]
    
    baseDir = OpenMaya.MVector( *baseDir )
    direction = OpenMaya.MVector( *direction )
    localAngle = baseDir.rotateTo( direction ).asMatrix()
    
    rotResultMatrix = localAngle * rotWorldMatrix
    return rotResultMatrix




def getTranslateFromMatrix( targetMtx ):
    if type( targetMtx ) == list:
        return OpenMaya.MPoint( targetMtx[12], targetMtx[13], targetMtx[14] )
    return [targetMtx( 3, 0 ), targetMtx( 3,1 ), targetMtx( 3,2 )]



def getRotateFromMatrix( mtxValue ):
    
    if type( mtxValue ) == list:
        mtxValue = listToMatrix( mtxValue )
    
    trMtx = OpenMaya.MTransformationMatrix( mtxValue )
    rotVector = trMtx.eulerRotation().asVector()
    
    return [math.degrees(rotVector.x), math.degrees(rotVector.y), math.degrees(rotVector.z)]



def getMatrixFromTranslate( transValue ):
    
    defaultMtx = matrixToList( OpenMaya.MMatrix() )
    defaultMtx[12] = transValue[0]
    defaultMtx[13] = transValue[1]
    defaultMtx[14] = transValue[2]
    return listToMatrix( defaultMtx )



def getMatrixFromRotate( rotValue ):
    
    trMtx = OpenMaya.MTransformationMatrix()
    radRotValues = [ math.radians(i) for i in rotValue ]
    trMtx.rotateTo( OpenMaya.MEulerRotation( OpenMaya.MVector( *radRotValues ) ) ) 
    return trMtx.asMatrix()



def setMatrixTranslate( mtx, *transValue ):
    
    mtxList = matrixToList( mtx )
    mtxList[12] = transValue[0]
    mtxList[13] = transValue[1]
    mtxList[14] = transValue[2]
    return listToMatrix( mtxList )


def setMatrixRotate( mtx, *rotValue ):
    
    mtxList = matrixToList( getMatrixFromRotate( rotValue ) )
    mtxList[12] = mtx(3,0)
    mtxList[13] = mtx(3,1)
    mtxList[14] = mtx(3,2)
    return listToMatrix( mtxList )




@convertSg_dec
def lookAt( aimTarget, rotTarget, baseDir=None, **options ):
    
    rotWorldMatrix = listToMatrix( rotTarget.wm.get() )
    aimWorldMatrix = listToMatrix( aimTarget.wm.get() )
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
    
    options.update( {'ws':1} )
    rotTarget.setOrient( math.degrees( rotVector.x ), math.degrees( rotVector.y ), math.degrees( rotVector.z ), **options )




    

@convertSg_dec
def insertMatrix( target, multMatrixNode ):

    cons = multMatrixNode.listConnections( s=1, d=0, p=1, c=1 )    
    srcAttrs = []
    dstLists = []
    for i in range( 0, len( cons ), 2 ):
        nodeName = cons[i].node().name()
        attrName = cons[i]._attrName
        index    = cons[i]._index
        
        srcAttrs.append( cons[i+1] )
        dstLists.append( [nodeName, attrName, index] )
        
        cons[i+1] // cons[i]
    
    target.matrixOutput() >> multMatrixNode.i[0]
    for i in range( len( srcAttrs ) ):
        srcAttrs[i] >> SGAttribute( dstLists[i][0], dstLists[i][1] + '[%d]' % (dstLists[i][2]+1) )
        

@convertSg_dec
def getSourceConnection( *args ):
    
    targets = args[:-1]
    src = args[-1]
    
    cons = src.listConnections( s=1, d=0, c=1, p=1 )

    srcAttrs = []
    connectedAttrs = []
    
    for i in range( 0, len( cons ), 2 ):
        srcAttrs.append( cons[i+1] )
        connectedAttrs.append( cons[i].attrName() )
    
    for target in targets:
        for i in range( len( connectedAttrs ) ):
            try:
                srcAttrs[i] >> target.attr( connectedAttrs[i] )
            except:
                pass
            


def getAnimCurveValueAtFloatInput( animCurveNode, inputFloat ):
    
    animCurveNode = convertName( animCurveNode )
    
    import maya.OpenMayaAnim as OpenMayaAnim
    
    oAnimCurve = getMObject( animCurveNode )
    fnAnim = OpenMayaAnim.MFnAnimCurve( oAnimCurve )
    doublePtr2 = getDoublePtr()
    fnAnim.evaluate( inputFloat, doublePtr2 )
    
    return getDoubleFromDoublePtr( doublePtr2 )




def getSourceList( node, nodeList = [] ):
    
    node = convertSg( node )
    if node in nodeList: return []
    
    nodeList.append( node )
    if node.nodeType() in sgdata.NodeType.transform:
        cons = []
        attrs = ['t', 'r', 's']
        attrs += cmds.listAttr( node.name(), k=1 )
        for attr in attrs:
            cons += node.attr( attr ).listConnections( s=1, d=0, p=1, c=1 )
    else:
        cons = node.listConnections( s=1, d=0, p=1, c=1 )
    srcs = cons[1::2]
    
    returnList = [node.name()]
    for i in range( len( srcs ) ):
        results = getSourceList( srcs[i].node(), nodeList )
        if not results: continue
        returnList += results
    return returnList



@convertSg_dec
def copyChildren( source, target ):
    first = source
    firstName = source.localName()
    secondName = target.localName()
    
    replaceStrsList = getNameReplaceList(firstName, secondName)
    
    firstChildren = first.listRelatives( c=1, ad=1, type='transform' )
    firstChildren.reverse()
    
    for firstChild in firstChildren:
        childName = firstChild.localName()
        for replaceSrc, replaceDst in replaceStrsList:
            childName = childName.replace( replaceSrc, replaceDst )
        parentName = firstChild.parent().localName()
        for replaceSrc, replaceDst in replaceStrsList:
            parentName = parentName.replace( replaceSrc, replaceDst )
        if not cmds.objExists( parentName ): continue
        exists = False
        if not cmds.objExists( childName ):
            secondChild = createNode( firstChild.nodeType() ).rename( childName )
        else:
            secondChild = SGTransformNode( childName )
            exists = True
        try:
            parent( secondChild, parentName )
        except: pass
        if not exists: 
            secondChild.xform( os=1, matrix= firstChild.m.get() )
            secondChild.attr( 'dh' ).set( firstChild.attr( 'dh' ).get() )
            if secondChild.nodeType() == 'joint':
                secondChild.attr( 'radius' ).set( firstChild.attr( 'radius' ).get() )


@convertSg_dec
def copyRig( source, target ):
    
    sourceName = source.localName()
    targetName = target.localName()
    
    replaceStrList = getNameReplaceList(sourceName, targetName)
    
    copyChildren( source, target )

    sourceChildren = source.listRelatives( c=1, ad=1, type='transform' )
    sourceChildren.append( source )
    
    def getReplacedNode( source, replaceStrList ):
        sourceName = source.name()
        for srcStr, dstStr in replaceStrList:
            sourceName = sourceName.replace( srcStr, dstStr )
        if sourceName == source.name():
            sourceName = source.name() + '_rigCopyed'
        else:
            if cmds.objExists( sourceName ):
                return convertSg( sourceName )
        if cmds.objExists( sourceName ): 
            return convertSg( sourceName )
        
        if source.nodeType() in sgdata.NodeType.transform:
            return None
        try:
            srcCons = source.listConnections( s=1, d=0, p=1, c=1 )
            dstCons = source.listConnections( s=0, d=1, p=1, c=1 )
            for i in range( 0, len( srcCons ), 2 ):
                srcCons[i+1] // srcCons[i]
            for i in range( 0, len( dstCons ), 2 ):
                dstCons[i] // dstCons[i+1]
            duObjs = source.duplicate( n=sourceName )
            for i in range( 0, len( srcCons ), 2 ):
                srcCons[i+1] >> srcCons[i]
            for i in range( 0, len( dstCons ), 2 ):
                dstCons[i] >> dstCons[i+1]
            return duObjs[0]
        except:
            return None
    
    for i in range( len( sourceChildren ) ):
        sourceNodes = getSourceList( sourceChildren[i], [] )
        if not sourceNodes: continue
        for sourceNode in sourceNodes:
            replacedSourceNode = getReplacedNode( sourceNode, replaceStrList )
            if not replacedSourceNode: continue
            
            srcCons = sourceNode.listConnections( s=1, d=0, p=1, c=1 )
            dstCons = sourceNode.listConnections( s=0, d=1, p=1, c=1 )
            dstCons.reverse()
            
            for cons in [ srcCons, dstCons ]:
                for i in range( 0, len( cons ), 2 ):
                    dest  = cons[i]
                    start = cons[i+1]
                    
                    destNode = dest.node()
                    startNode = start.node()
                    destAttrName = dest.attrName()
                    startAttrName = start.attrName()
                    
                    replacedDestNode = getReplacedNode( destNode, replaceStrList )
                    replacedStartNode = getReplacedNode( startNode, replaceStrList )
                    
                    if not replacedDestNode or not replacedStartNode: continue
                    
                    replacedStartNode.attr( startAttrName ) >> replacedDestNode.attr( destAttrName )
    
    duNodes = cmds.ls( '*_rigCopyed' )
    for duNode in duNodes:
        cmds.rename( duNode, duNode.replace( '_rigCopyed', '' ) )

    
    
def setAngleReverse( rigedNode ):
    srcList = getSourceList( rigedNode, [] )
    for src in srcList:
        if src.nodeType() == 'angleBetween':
            vector1Value = src.vector1.get()
            src.vector1.set( -vector1Value[0],-vector1Value[1],-vector1Value[2])




def getSelectedVertices( targetObj=None ):
    
    cmds.select( targetObj )
    selList = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList(selList)
    
    returnTargets = []
    for i in range( selList.length() ):
        dagPath    = OpenMaya.MDagPath()
        oComponent = OpenMaya.MObject()
        
        selList.getDagPath( i, dagPath, oComponent )
        
        if dagPath.node().apiTypeStr() != 'kMesh': continue 
        
        fnMesh = OpenMaya.MFnMesh( dagPath )
        targetVertices = OpenMaya.MIntArray()
        if oComponent.isNull(): continue
        
        singleComp = OpenMaya.MFnSingleIndexedComponent( oComponent )
        elements = OpenMaya.MIntArray()
        singleComp.getElements( elements )
            
        
        if singleComp.componentType() == OpenMaya.MFn.kMeshVertComponent :
            for j in range( elements.length() ):
                targetVertices.append( elements[j] )
        elif singleComp.componentType() == OpenMaya.MFn.kMeshEdgeComponent:
            for j in range( elements.length() ):
                vtxList = getInt2Ptr()
                fnMesh.getEdgeVertices( elements[j], vtxList )
                values = getListFromInt2Ptr(vtxList)
                targetVertices.append( values[0] )
                targetVertices.append( values[1] )
        elif singleComp.componentType() == OpenMaya.MFn.kMeshPolygonComponent:
            for j in range( elements.length() ):
                intArr = OpenMaya.MIntArray()
                fnMesh.getPolygonVertices( elements[j], intArr )
                for k in range( intArr.length() ):
                    targetVertices.append( intArr[k] )
        
        if targetVertices.length():
            returnTargets.append( [dagPath, targetVertices] )
    
    return returnTargets



def getBBC( target ):
    
    bbmin = cmds.getAttr( target + '.boundingBoxMin' )[0]
    bbmax = cmds.getAttr( target + '.boundingBoxMax' )[0]
    
    bbcenter = []
    for i in range( 3 ):
        bbcenter.append( (bbmin[i] + bbmax[i])/2.0 )
    return bbcenter





def getCenter( sels ):
    if not sels: return None
    
    def chunks(l, n):
        for i in xrange(0, len(l), n):
            yield l[i:i+n]
    
    sels = cmds.ls( sels, fl=1 )
    
    bb = OpenMaya.MBoundingBox()
    for sel in sels:
        posList = list( chunks( cmds.xform( sel, q=1, ws=1, t=1 ), 3 ) )
        for pos in posList:
            pos = OpenMaya.MPoint( *pos )
            bb.expand( pos )
    return bb.center()




def putObject( putTarget, typ='joint', putType='' ):
    
    putTarget = cmds.ls( putTarget, fl=1 )
    if len( putTarget ) == 1:
        putTarget = putTarget[0]
    
    if typ == 'locator':
        newObj = cmds.spaceLocator()[0]
    elif typ == 'null':
        newObj = cmds.createNode( 'transform' )
        cmds.setAttr( newObj + '.dh', 1 )
    else:
        newObj = cmds.createNode( typ )
    
    if type( putTarget ) in [list, tuple]:
        center = getCenter( putTarget )
        cmds.move( center.x, center.y, center.z, newObj, ws=1 )
    else:
        try:
            mtx = cmds.getAttr( putTarget + '.wm' )
            cmds.xform( newObj, ws=1, matrix= mtx )
        except:
            pos = getCenter( putTarget )
            cmds.xform( newObj, ws=1, t=[pos.x, pos.y, pos.z] )
    
    return newObj



@convertName_dec
def copyShapeToTransform( shape, target ):
    
    oTarget = getMObject( target )
    if cmds.nodeType( shape ) == 'mesh':
        oMesh = getMObject( shape )
        fnMesh = OpenMaya.MFnMesh( oMesh )
        fnMesh.copy( oMesh, oTarget )
    elif cmds.nodeType( shape ) == 'nurbsCurve':
        oCurve = getMObject( shape )
        fnCurve = OpenMaya.MFnNurbsCurve( oCurve )
        fnCurve.copy( oCurve, oTarget )
    elif cmds.nodeType( shape ) == 'nurbsSurface':
        oSurface = getMObject( shape )
        fnSurface = OpenMaya.MFnNurbsSurface( oSurface )
        fnSurface.copy( oSurface, oTarget )



@convertSg_dec
def addIOShape( target ):
    
    targetTr    = target.transform()
    targetShape = target.shape()
    newShapeTr = createNode( 'transform' )
    copyShapeToTransform( targetShape, newShapeTr )
    newShapeTr.shape().attr( 'io' ).set( 1 )
    newShapeName = newShapeTr.shape().name()
    cmds.parent( newShapeName, targetTr.name(), add=1, shape=1 )
    cmds.delete( newShapeTr.name() )
    return newShapeName
        


def curve( **options ):
    return convertSg( cmds.curve( **options ) )



@convertName_dec
def delete( *args, **options ):
    cmds.delete( *args, **options )



def makeController( pointList, defaultScaleMult = 1, **options ):
    
    import copy
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
        
    
    crv = curve( **options )
    crvShape = crv.shape()
    
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

    parent( crvShape, jnt, add=1, shape=1 )
    delete( crv )
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

    return convertSg( jnt.name() )





@convertSg_dec
def transformGeometryControl( controller, mesh ):
    
    meshShape = mesh.shape()
    mm = createNode( 'multMatrix' )
    trGeo = createNode( 'transformGeometry' )
    origMesh = addIOShape( mesh )
    srcCon = meshShape.inputGeometry().listConnections( s=1, d=0, p=1 )
    srcAttr = origMesh.attr( 'inMesh' )
    if srcCon:
        srcAttr = srcCon[0]
    print srcAttr.name()

    mesh.wm >> mm.i[0]
    controller.pim >> mm.i[1]
    controller.wm >> mm.i[2]
    mesh.wim >> mm.i[3]
    
    srcAttr >> trGeo.inputGeometry
    mm.o >> trGeo.transform
    
    trGeo.outputGeometry >> meshShape.inputGeometry()
    
    fnMesh = OpenMaya.MFnMesh( getMObject( meshShape.name() ) )
    numVertices = fnMesh.numVertices()
    
    meshName = meshShape.name()
    for i in range( numVertices ):
        cmds.setAttr( meshName + '.pnts[%d]' % i, 0,0,0 )
    



def setPntsZero( targetMesh ):
    shapes = convertSg( targetMesh ).listRelatives( s=1 )
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




@convertSg_dec
def updateFollicleConnection( follicleTr ):
    
    transAttr = follicleTr.t.listConnections( s=1, d=0, p=1 )[0]
    rotateAttr = follicleTr.r.listConnections( s=1, d=0, p=1 )[0]
    
    compose = createNode( 'composeMatrix' )
    mm = createNode( 'multMatrix' )
    dcmp = getDecomposeMatrix( mm )
    
    transAttr >> compose.inputTranslate
    rotateAttr >> compose.inputRotate
    
    compose.outputMatrix >> mm.i[0]
    follicleTr.pim >> mm.i[1]
    
    dcmp.ot >> follicleTr.t
    dcmp.outputRotate >> follicleTr.r


@convertSg_dec
def sliderVisibilityConnection( sliderAttr, *meshs, **options ):
    
    offset = 0
    if options.has_key( 'offset' ):
        offset = options[ 'offset' ]
    
    for i in range( len( meshs ) ):
        setRange = createNode( 'setRange' )
        multNode = createNode( 'multDoubleLinear' )
        setRange.oldMinX.set( offset + i-0.5 )
        setRange.oldMaxX.set( offset + i+0.5 )
        setRange.oldMinY.set( offset + i+0.5 )
        setRange.oldMaxY.set( offset + i+1.4999 )
        setRange.maxX.set( 1 )
        setRange.minY.set( 1 )
        sliderAttr >> setRange.valueX
        sliderAttr >> setRange.valueY
        setRange.outValueX >> multNode.input1
        setRange.outValueY >> multNode.input2
        multNode.output >> meshs[i].v
    
    
    
@convertSg_dec
def makeCurveFromSelection( *sels, **options ):
    
    poses = []
    for sel in sels:
        pose = sel.xform( q=1, ws=1, t=1 )[:3]
        poses.append( pose )
    curve = convertSg( cmds.curve( p=poses, **options ) )
    curveShape = curve.shape()
    
    for i in range( len( sels ) ):
        dcmp = createNode( 'decomposeMatrix' )
        vp   = createNode( 'vectorProduct' ).setAttr( 'op', 4 )
        sels[i].wm >> dcmp.imat
        dcmp.ot >> vp.input1
        curve.wim >> vp.matrix
        vp.output >> curveShape.attr( 'controlPoints' )[i]
    
    return curve.name()




class CreateJointOnCurveSet:
    
    def __init__( self ):
        
        self._curveShape = ''
        self._minParam   = 0.0
        self._maxParam   = 1.0
        self._infoNum    = 5
        self._numSpans   = 5
        
        
    def setJointNum( self, num ):
        
        self._infoNum = num
        
        
    def setCurve( self, curveShape ):
        
        self._curveShape = curveShape
        self._minParam = cmds.getAttr( self._curveShape+'.minValue' )
        self._maxParam = cmds.getAttr( self._curveShape+'.maxValue' )
        self._numSpans = cmds.getAttr( self._curveShape+'.spans' )
    
    
    def create(self, distanceNode ):
        
        eachParam = ( self._maxParam - self._minParam )/( self._infoNum - 1 )
        
        eachInfos = []
        
        for i in range( self._infoNum ):
            
            info = cmds.createNode( 'pointOnCurveInfo', n= self._curveShape+'_info%d' % i )
            cmds.connectAttr( self._curveShape+'.local', info+'.inputCurve' )
            cmds.setAttr( info+'.parameter', eachParam*i + self._minParam )
            eachInfos.append( info )
            
        cmds.select( d=1 )
        
        joints = []
        for i in range( self._infoNum ):
            joints.append( cmds.joint(p=[i,0,0]) )
            
        handle, effector = cmds.ikHandle( sj=joints[0], ee=joints[-1], sol='ikSplineSolver', ccv=False, pcv=False, curve=self._curveShape )
        
        distNodes = []
        for i in range( self._infoNum -1 ):
            
            firstInfo = eachInfos[i]
            secondInfo = eachInfos[i+1]
            targetJoint = joints[i+1]
            
            distNode = cmds.createNode( 'distanceBetween' )
            distNodes.append( distNode )
            
            cmds.connectAttr( firstInfo+'.position', distNode+'.point1' )
            cmds.connectAttr( secondInfo+'.position', distNode+'.point2')
            
            if distanceNode:
                cmds.connectAttr( distNode+'.distance', targetJoint+'.tx' )
            else:
                cmds.setAttr( targetJoint+'.tx', cmds.getAttr( distNode+'.distance' ) )
        
        if not distanceNode:
            cmds.delete( distNodes )
        
        return handle, joints
    





def createJointOnCurve( curve, numJoint, distanceNode = True ):
    
    curve = convertSg( curve )
    curveShape = curve.shape()
    
    curveSetInst = CreateJointOnCurveSet()
    curveSetInst.setJointNum( numJoint )
    
    curveSetInst.setCurve( curveShape.name() )
    
    return curveSetInst.create( distanceNode )
    




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
        baseCurve = curve( p=baseData, d=1 )
        baseCurveOrigShape=  convertSg( addIOShape( baseCurve ) )
        baseCurveShape = baseCurve.shape()
        
        trGeo = createNode( 'transformGeometry' )
        composeMatrix = createNode( 'composeMatrix' )
        
        if axisX:
            multNodeX = createNode( 'multDoubleLinear' ).setAttr( 'input2', 0.5 )
            addNodeX = createNode( 'addDoubleLinear' ).setAttr( 'input2', 1 )
            baseCurve.addAttr( ln='slideSizeX', min=0, cb=1 )
            baseCurve.slideSizeX >> multNodeX.input1
            baseCurve.slideSizeX >> addNodeX.input1
            addNodeX.output >> composeMatrix.inputScaleX
            multNodeX.output >> composeMatrix.inputTranslateX
        
        if axisY:
            multNodeY = createNode( 'multDoubleLinear' ).setAttr( 'input2', 0.5 )
            addNodeY = createNode( 'addDoubleLinear' ).setAttr( 'input2', 1 )
            baseCurve.addAttr( ln='slideSizeY', min=0, cb=1 )
            baseCurve.slideSizeY >> multNodeY.input1
            baseCurve.slideSizeY >> addNodeY.input1
            addNodeY.output >> composeMatrix.inputScaleY
            multNodeY.output >> composeMatrix.inputTranslateY
        
        composeMatrix.outputMatrix >> trGeo.transform
        baseCurveOrigShape.outputGeometry() >> trGeo.inputGeometry
        trGeo.outputGeometry >> baseCurveShape.inputGeometry()

        return baseCurve



@convertSg_dec
def makeParent( sel, **options ):
    
    if not options.has_key( 'n' ) and not options.has_key( 'name' ):
        options.update( {'n':'P'+ sel.localName()} )
    
    selP = sel.parent()
    transform = createNode( 'transform', **options )
    if selP: parent( transform, selP )
    transform.xform( ws=1, matrix= sel.wm.get() )
    parent( sel, transform )
    sel.setTransformDefault()
    return transform.name()




def makeParent_pymel( target ):
    
    pymelTarget = pymel.core.ls( target )[0]
    pTarget = pymel.core.createNode( 'transform', n= 'P' + pymelTarget.shortName() )
    pymel.core.xform( pTarget, ws=1, matrix= pymelTarget.wm.get() )
    
    origParent = pymelTarget.getParent()
    pymel.core.parent( pymelTarget, pTarget )
    if origParent: pymel.core.parent( pTarget, origParent )
    



@convertName_dec
def getMatrixFromSelection( *sels ):
    
    isTransform = False
    if len( sels ) == 1:
        if sels[0].find( '.' ) == -1:
            if cmds.objExists( sels[0] ) and cmds.nodeType( sels[0] ) in ['mesh', 'transform']:
                isTransform = True
            
    if sels:
        if isTransform:
            return convertSg( sels[0] ).wm.get()
        else:
            try:
                centerPos = getCenter( sels )
                mtx = [1,0,0,0, 0,1,0,0, 0,0,1,0, centerPos.x, centerPos.y, centerPos.z,1 ]
                return mtx
            except:
                return [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]
    else:
        return [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]










@convertName_dec
def joint( *args, **options ):
    return convertSg( cmds.joint( *args, **options ) )



@convertName_dec
def ikHandle( *args, **options ):
    return convertSg( cmds.ikHandle( *args, **options ) )





@convertName_dec
def autoCopyWeight( *args ):
    
    first = args[0]
    second = args[1]
    
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
    
    



@convertName_dec
def setSkinClusterDefault( *args ):
    
    import sgPlugin
    if not cmds.pluginInfo( 'sgCmdSkinCluster', q=1, l=1 ):
        cmds.loadPlugin( 'sgCmdSkinCluster' )
    cmds.sgCmdSkinClustser( cmds.ls( sl=1 ), d=1 )
    




def separateParentConnection( node, attr ):
    
    parentAttr = cmds.attributeQuery( attr, node=node, listParent=1 )
    
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




@convertName_dec
def addMultDoubleLinearConnection( node, attr ):

    newAttrName = 'mult_' + attr
    
    print "node, attr : ", node, attr
    
    convertSg( node ).addAttr( ln=newAttrName, cb=1, dv=1 )
    multDouble = cmds.createNode( 'multDoubleLinear' )
    
    separateParentConnection( node, attr )
    
    cons = cmds.listConnections( node + '.' + attr, s=1, d=0, p=1, c=1 )
    cmds.connectAttr( cons[1], multDouble+'.input1' )
    cmds.connectAttr( node+'.'+newAttrName, multDouble + '.input2' )
    cmds.connectAttr( multDouble + '.output', node+'.'+attr, f=1 )
    return convertSg( multDouble )



@convertName_dec
def addAnimCurveConnection( node, attr ):
    
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
    
    cmds.selectKey( animCurve )
    cmds.keyTangent( itt='spline', ott='spline' )
    return convertSg( animCurve )




@convertName_dec
def getOrigShape( shape ):
    for hist in cmds.listHistory( shape ):
        if cmds.nodeType( hist ) != 'mesh': continue
        if not cmds.getAttr( hist + '.io' ): continue
        return convertSg( hist )




def createPointOnCurve( inputCurve, **options ):
    
    curve = pymel.core.ls( inputCurve )[0]
    curveShape = curve.getShape()
    pointInfoNode = pymel.core.createNode( 'pointOnCurveInfo' )
    trNode = pymel.core.createNode( 'transform' )
    trNode.dh.set( 1 )
    
    
    local = False
    if options.has_key( 'local' ):
        local = options[ 'local' ]
    
    if local:
        curveShape.attr( 'local' ) >> pointInfoNode.inputCurve
        pointInfoNode.position >> trNode.t
    else:
        curveShape.attr( 'worldSpace' ) >> pointInfoNode.inputCurve
        composeNode = pymel.core.createNode( 'composeMatrix' )
        mm = pymel.core.createNode( 'multMatrix' )
        dcmp = pymel.core.createNode( 'decomposeMatrix' )
        
        pointInfoNode.position >> composeNode.inputTranslate
        composeNode.outputMatrix >> mm.i[0]
        trNode.pim >> mm.i[1]
        mm.matrixSum >> dcmp.imat
        
        dcmp.ot >> trNode.t
    
    trNode.addAttr( 'parameter', k=1, 
                    min=curveShape.attr( 'minValue' ).get(), max=curveShape.attr( 'maxValue' ).get() )
    trNode.parameter >> pointInfoNode.parameter
    return trNode.name()



@convertSg_dec
def getParents( target, **options ):
    
    firstTarget=None 
    parents = []
    
    if options.has_key( 'firstTarget' ):
        firstTarget = options['firstTarget']
    if options.has_key('parents' ):
        parents = options['parents']
    
    if not firstTarget:
        firstTarget = target
        parents = []

    ps = target.listRelatives( p=1 )
    if not ps: return parents
    parents.insert( 0, ps[0] )
    
    return getParents( ps[0], firstTarget=firstTarget, parents=parents )



class DataPtr:
    
    def __init__(self):
        
        self.defaultIgnore = []
        self.reverseAttrs = []
        
        self.leftPrefix  = []
        self.rightPrefix = []
        self.data = []



class MirrorInfo:
    
    prefix = 'mi_'
    mirrorTypeAttr = 'mirrorType'
    
    def __init__(self, nodeName ):
        
        nodeName = convertName( nodeName )
        if nodeName[ :len( MirrorInfo.prefix ) ] == MirrorInfo.prefix:    
            mirrorInfo = nodeName
        else:
            mirrorInfo = MirrorInfo.prefix + nodeName
        
        if not cmds.objExists( mirrorInfo ):
            mirrorInfo = cmds.createNode( 'transform', n=mirrorInfo )
            cmds.setAttr( mirrorInfo + '.dh', 1 )
            
        self.mirrorInfo = convertSg( mirrorInfo )
        pivMatrix = convertSg( nodeName ).getPivotMatrix() * convertSg( nodeName ).getWorldMatrix()
        self.mirrorInfo.xform( ws=1, matrix=pivMatrix.getList() )

    
    def origName(self):
        return self.mirrorInfo.localName()[ len( MirrorInfo.prefix ): ]


    def name(self):
        return self.mirrorInfo.name()


    def parent(self):
        mirrorInfoParent = self.mirrorInfo.parent()
        if not mirrorInfoParent:
            return None
        return MirrorInfo( mirrorInfoParent )


    def setParent( self, nodeName ):
        
        parentInst = MirrorInfo( nodeName )
        origParents = self.mirrorInfo.parent()
        if not origParents or origParents.name() != parentInst.mirrorInfo.name():
            parent( self.mirrorInfo, parentInst.mirrorInfo )
    

    def getOtherSide(self, leftPrefixList, rightPrefixList ):
        
        orig = self.mirrorInfo.name()[len( MirrorInfo.prefix ):]
        otherSideOrig = copy.copy( orig )
        for i in range( len( leftPrefixList ) ):
            leftPrefix  = leftPrefixList[i]
            rightPrefix = rightPrefixList[i]
            if orig.find( leftPrefix ) != -1:
                otherSideOrig = orig.replace( leftPrefix, rightPrefix )
            elif orig.find( rightPrefix ) != -1:
                otherSideOrig = orig.replace( rightPrefix, leftPrefix )
            if otherSideOrig:
                break
        
        if not otherSideOrig or not cmds.objExists( otherSideOrig ): return None
        return MirrorInfo( otherSideOrig )
    
    
    def setMirrorType(self, mirrorTypeName ):
        
        self.mirrorInfo.addAttr( ln= MirrorInfo.mirrorTypeAttr, cb=1, at='enum', en=mirrorTypeName + ':' )
    
    
    def getMirrorType(self):
        
        if cmds.attributeQuery( MirrorInfo.mirrorTypeAttr, node = self.mirrorInfo.name(), ex=1 ):
            return cmds.attributeQuery( MirrorInfo.mirrorTypeAttr, node=self.mirrorInfo.name(),le=1 )[0]
        else:
            return 'center'
    
    
        


def getDataPtrFromMirrorInfo( rootMirrorInfo, leftPrefixList, rightPrefixList ):
    
    origRoot = rootMirrorInfo[len(MirrorInfo.prefix):]
    parents = getParents( origRoot )
    rootMirrorInfo = convertSg( rootMirrorInfo )
    children = rootMirrorInfo.listRelatives( c=1, ad=1, type='transform' )
    dataPtrInst = DataPtr()
    dataPtrInst.leftPrefix = leftPrefixList
    dataPtrInst.rightPrefix = rightPrefixList
    for child in children:
        info = MirrorInfo( child )
        otherSide = info.getOtherSide( leftPrefixList, rightPrefixList )
        parent = info.parent()
        dataPtrInst.data.append( [info.origName(), parent.origName(), otherSide.origName(), info.getMirrorType()] )
    return dataPtrInst



def getPivotMatrix( target ):
    piv = OpenMaya.MPoint( *cmds.getAttr( target + '.rotatePivot' )[0] )
    mtxList = matrixToList( OpenMaya.MMatrix() )
    mtxList[ 12 ] = piv.x
    mtxList[ 13 ] = piv.y
    mtxList[ 14 ] = piv.z
    return listToMatrix( mtxList )





class SymmetryControl:

    def __init__(self, name, dataPtr ):
        self.__name = name
        self.__origName = self.__name.split( ':' )[-1]
        self.__namespace = ':'.join( self.__name.split( ':' )[:-1] )
        self.sgtransform = convertSg( self.__name )
        self.dataPtr = dataPtr
    
    
    def fullName(self, origName ):
        return self.__namespace + ':' + origName


    def parent(self):
        for origName, pOrigName, otherSide, mirrorType in self.dataPtr.data:
            if origName != self.__origName: continue
            if not pOrigName: return self
            return [ SymmetryControl( self.fullName( i ), self.dataPtr ) for i in pOrigName.split( ',' ) ]
    
    
    def side(self):
        for leftPrefix in self.dataPtr.leftPrefix:
            if leftPrefix == self.__origName[:len( leftPrefix ) ]:
                return 'left'
        for rightPrefix in self.dataPtr.rightPrefix:
            if rightPrefix == self.__origName[:len( rightPrefix ) ]:
                return 'right'
        return 'center'
    
    
    def otherSide(self):
        for origName, pOrigName, otherSide, mirrorType in self.dataPtr.data:
            if origName != self.__origName:continue
            if not otherSide: return self
            return SymmetryControl( self.fullName( otherSide ), self.dataPtr )


    def mirrorType(self):
        for origName, pOrigName, otherSide, mirrorType in self.dataPtr.data:
            if origName != self.__origName:continue
            return mirrorType.split( ',' )


    def name(self):
        return self.sgtransform.name()


    def setMatrixByMirrorType( self, mirrorTypes, srcLocalMtx ):
        attrs  = ['tx', 'ty', 'tz','rx', 'ry', 'rz']
        revs = [1,1,1,1,1,1]
        values = [0,0,0,0,0,0]
        for mirrorType in mirrorTypes[1:]:
            for attr in attrs:
                mirrorAttr, rev, value= mirrorType.split( '_' )
                if mirrorAttr != attr: continue
                if rev == 'r': revs[ attrs.index( attr ) ] *= -1
                values[ attrs.index( attr ) ] = float( value )

        trans = srcLocalMtx.getTranslate()
        rots  = srcLocalMtx.getRotate()
        trans.x *= revs[0]
        trans.y *= revs[1]
        trans.z *= revs[2]
        rots.x *= revs[3]
        rots.y *= revs[4]
        rots.z *= revs[5]
        srcLocalMtx.setTranslate( trans )
        srcLocalMtx.setRotate( rots )
        transAddValues = values[:3]
        rotAddValues = values[3:]
        srcLocalMtx.translateOutside( *transAddValues )
        srcLocalMtx.rotateInside( *rotAddValues )
        return srcLocalMtx


    def getCtlData(self, source ):
        
        sourceParent = source.parent()
        if not source.parent(): return None
        
        sgtrans = source.sgtransform
        udAttrs = sgtrans.listAttr( k=1, ud=1 )
        udAttrValues = []
        for attr in udAttrs:
            if attr in self.dataPtr.reverseAttrs:
                udAttrValues.append( -sgtrans.attr( attr ).get() )
            else:
                udAttrValues.append( sgtrans.attr( attr ).get() )
        transformAttrs = ['tx','ty','tz','rx','ry','rz','sx','sy','sz']
        transformAttrValues = []
        for attr in transformAttrs:
            transformAttrValues.append( sgtrans.attr( attr ).get() )
        worldMatrix = sgtrans.getWorldMatrix()
        pivMatrix   = sourceParent[0].sgtransform.getPivotMatrix() * sourceParent[0].sgtransform.getWorldMatrix()
        return udAttrs, udAttrValues, transformAttrs, transformAttrValues, worldMatrix * pivMatrix.inverse()
    
    
    def setCtlData(self, source, target, ctlData, typ='mirror' ):

        if not ctlData: return None

        mirrorTypes = source.mirrorType()
        udAttrs, udAttrValues, transformAttrs, transformValues, localMatrix = ctlData
        
        trg = target.sgtransform
        for i in range( len( udAttrs ) ):
            try:
                trg.attr( udAttrs[i] ).set( udAttrValues[i] )
            except:pass
        for i in range( len( transformAttrs ) ):
            try:trg.attr( transformAttrs[i] ).set( transformValues[i] )
            except:pass
        
        if 'none' in mirrorTypes: return None

        if 'local' in mirrorTypes:
            trg.tx.set( -trg.tx.get() )
            trg.ty.set( -trg.ty.get() )
            trg.tz.set( -trg.tz.get() )
        
        if 'txm' in mirrorTypes:
            trg.tx.set( -trg.tx.get() )
        if 'tym' in mirrorTypes:
            trg.ty.set( -trg.ty.get() )
        if 'tzm' in mirrorTypes:
            trg.tz.set( -trg.tz.get() )
        if 'rxm' in mirrorTypes:
            trg.rx.set( -trg.rx.get() )
        if 'rym' in mirrorTypes:
            trg.ry.set( -trg.ry.get() )
        if 'rzm' in mirrorTypes:
            trg.rz.set( -trg.rz.get() )

        if 'matrix' in mirrorTypes:
            srcLocalMtx = self.setMatrixByMirrorType( mirrorTypes, localMatrix )
            dstMatrix = srcLocalMtx * target.parent()[0].sgtransform.getPivotMatrix() * target.parent()[0].sgtransform.getWorldMatrix()

            rotList = dstMatrix.getRotate().getList()
            for i in range( len( rotList ) ):
                rotList[i] = math.degrees(rotList[i])
            target.sgtransform.xform( ws=1, t= dstMatrix.getTranslate().getList() )
            target.sgtransform.xform( ws=1, ro= rotList )
        
        if 'center' in mirrorTypes:
            if typ == 'flip':
                setMirrorLocal( target.sgtransform )
            elif typ == 'mirror':
                setCenterMirrorLocal( target.sgtransform )
        
    
    def isMirrorAble(self):
        
        for origName, pOrigName, otherSide, mirrorType in self.dataPtr.data:
            if origName != self.__origName: continue
            return True
        return False
    
    

    def setMirror(self, side ):
        
        if not self.isMirrorAble(): return None
        
        if side == 'LtoR':
            if self.side() == 'left':
                source = self
                target = self.otherSide()
            else:
                source = self.otherSide()
                target = self
                
        if side == 'RtoL':
            if self.side() == 'right':
                source = self
                target = self.otherSide()
            else:
                source = self.otherSide()
                target = self
        
        self.setCtlData( source, target, self.getCtlData( source ), 'mirror' )
    
    
    def setFlip(self):

        if not self.isMirrorAble(): return None

        source = self
        target = self.otherSide()
        dataSource = self.getCtlData( source )
        dataTarget = self.getCtlData( target )
        
        self.setCtlData( source, target, dataSource, 'flip' )
        self.setCtlData( target, source, dataTarget, 'flip' )
    


    def flipH(self):
        
        if not self.isMirrorAble(): return None
        
        H = self.allChildren()
    
        flipedList = []
        sourceList = []
        targetList = []
        sourceDataList = []
        targetDataList = []
        
        for h in H:
            
            name = h.otherSide().name()
            if name in flipedList: continue
            flipedList.append( h.name() )
            
            otherSide = h.otherSide()
            sourceList.append( h )
            targetList.append( otherSide )
            sourceDataList.append( self.getCtlData( h ) )
            targetDataList.append( self.getCtlData( otherSide ) )
        
        for i in range( len( sourceList ) ):
            self.setCtlData( sourceList[i], targetList[i], sourceDataList[i], 'flip' )
            self.setCtlData( targetList[i], sourceList[i], targetDataList[i], 'flip' )


    def mirrorH(self, side ):
        
        if not self.isMirrorAble(): return None
        
        if side == 'LtoR':
            if self.side() == 'left':
                source = self
            else:
                source = self.otherSide()
                
        if side == 'RtoL':
            if self.side() == 'right':
                source = self
            else:
                source = self.otherSide()
        
        H = source.allChildren()
    
        sourceList = []
        targetList = []
        sourceDatas = []

        for h in H:
            if side == 'LtoR' and h.side() == 'right': continue
            if side == 'RtoL' and h.side() == 'left' : continue
            
            otherSide = h.otherSide()
            sourceList.append( h )
            targetList.append( otherSide )
            sourceDatas.append( self.getCtlData( h ) )
        
        for i in range( len( sourceList ) ):
            self.setCtlData( sourceList[i], targetList[i], sourceDatas[i], 'mirror' )
        


    def children(self):
        
        targetChildren = []
        for origName, pOrigName, otherSide, mirrorType in self.dataPtr.data:
            if not self.__origName in pOrigName.split( ',' ): continue
            print "origName : ", origName
            targetChildren.append( SymmetryControl( self.fullName( origName ), self.dataPtr ) )
        return targetChildren


    def allChildren(self):
        
        localChildren = self.children()
        childrenH = []
        for localChild in localChildren:
            childrenH += localChild.allChildren()
        localChildren += childrenH
        childrenNames = []

        localChildrenSet = []
        for localChild in localChildren:
            name = localChild.name()
            if name in childrenNames: continue
            childrenNames.append( name )
            localChildrenSet.append( localChild )
        
        return localChildrenSet
    
    
    def hierarchy(self):
        
        localChildren = [self]
        localChildren += self.allChildren()
        return localChildren
    

    def setDefault(self):

        attrs = self.sgtransform.listAttr( k=1 )
        for attr in attrs:
            if attr in self.dataPtr.defaultIgnore: continue
            try:self.sgtransform.attr(attr).setToDefault()
            except:pass





@convertSg_dec
def getTransformWorldVector( trNode, **options ):
    
    vectorName = 'v'
    vectorValue = [1,0,0]
    if options.has_key( 'vectorName' ):
        vectorName = options['vectorName']
    if options.has_key( 'vector' ):
        vectorValue = options['vector']
    
    dcmp = getDecomposeMatrix( trNode ).rename( 'dcmp_' + trNode.name() )
    compose = createNode( 'composeMatrix' ).rename( 'composeTrans_' + trNode.name() )
    dcmp.ot >> compose.inputTranslate
    inverse = createNode( 'inverseMatrix' ).rename( 'invm_' + trNode.name() )
    compose.matrixOutput() >> inverse.inputMatrix
    composeVector = createNode( 'composeMatrix', n='compose_%sVector' % vectorName )
    composeVector.it.set( *vectorValue )
    mmTrans = createNode( 'multMatrix', n='mmTrans_' + trNode.name() )
    
    composeVector.outputMatrix >> mmTrans.i[0]
    trNode.wm >> mmTrans.i[1]
    inverse.matrixOutput() >> mmTrans.i[2]
    
    return getDecomposeMatrix( mmTrans ).rename( 'dcmp%sVector_' % vectorName + trNode.name() )





@convertSg_dec
def getCloseMatrixOnMesh( matrixObj, mesh  ):

    matrixObjDcmp = getDecomposeMatrix( getLocalMatrix( matrixObj, mesh) )
    meshShape = mesh.shape()
    closePointOnMesh = createNode( 'closestPointOnMesh', n='close_%s_%s' %( matrixObj.name(), mesh.name() ) )
    meshShape.outMesh     >> closePointOnMesh.inMesh
    matrixObjDcmp.outputTranslate >> closePointOnMesh.inPosition
    
    normalVector = createNode( 'vectorProduct' ).setAttr( 'op', 3 )
    positionVector     = createNode( 'vectorProduct' ).setAttr( 'op', 4 )
    closePointOnMesh.normal >> normalVector.input1
    meshShape.worldMatrix >> normalVector.matrix
    closePointOnMesh.position >> positionVector.input1
    meshShape.worldMatrix >> positionVector.matrix
    
    dcmpYVector = getTransformWorldVector( matrixObj, vectorName = 'y', vector=[0,1,0] )
    
    xVectorNode = getCrossVectorNode( dcmpYVector, normalVector )
    yVectorNode = getCrossVectorNode( normalVector, xVectorNode )
    
    fbfNode = getFbfMatrix( xVectorNode, yVectorNode, normalVector )
    positionVector.outputX >> fbfNode.in30
    positionVector.outputY >> fbfNode.in31
    positionVector.outputZ >> fbfNode.in32
    
    mm = createNode( 'multMatrix' )
    trNode = createNode( 'transform' ).setAttr( 'dh', 1 )
    
    fbfNode.matrixOutput() >> mm.i[0]
    trNode.parentInverseMatrix >> mm.i[1]
    
    dcmp = getDecomposeMatrix( mm )
    dcmp.outputTranslate >> trNode.t
    dcmp.outputRotate >> trNode.r
    
    select( trNode )




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
    
    if cmds.attributeQuery( attrName, node=target, ex=1 ): return None
    
    cmds.addAttr( target, **options )
    
    if channelBox:
        cmds.setAttr( target+'.'+attrName, e=1, cb=1 )
    elif keyable:
        cmds.setAttr( target+'.'+attrName, e=1, k=1 )




def createTextureFileNode( filePath ):
    
    fileNode = convertSg( cmds.shadingNode( "file", asTexture=1, isColorManaged=1 ) )
    place2d  = convertSg( cmds.shadingNode( "place2dTexture", asUtility=1 ) )
    
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



@convertSg_dec
def assignToLayeredTexture( textureNode, layeredTexture, **options ):
    
    index = None
    blendMode = None
    if options.has_key( 'index' ):
        index = options['index']
    if options.has_key( 'blendMode' ):
        blendMode = options['blendMode']

    if index == None:
        inputsPlug = layeredTexture.attr( 'inputs' ).getPlug()
        if inputsPlug.numElements():
            logicalIndex = inputsPlug[ inputsPlug.numElements()-1 ].logicalIndex()
        else:
            logicalIndex = -1
        index = logicalIndex + 1

    textureNode.outColor >> layeredTexture.inputs[ index ].color
    textureNode.outAlpha >> layeredTexture.inputs[ index ].alpha
    
    if blendMode != None:
        layeredTexture.inputs[ index ].blendMode.set( blendMode )



@convertSg_dec
def clearArrayAttribute( attr ):

    connectedAttrs = attr.node().listConnections( s=1, d=0, p=1, c=1 )
    
    for i in range( 0, len( connectedAttrs ), 2 ):
        srcAttr = connectedAttrs[i+1]
        dstAttr = connectedAttrs[ i ]
        
        srcAttr // dstAttr
    
    plugAttr = attr.getPlug()
    for i in range( plugAttr.numElements() ):
        try:cmds.removeMultiInstance( plugAttr[i].name() )
        except:pass
    
    

@convertName_dec
def group( *args, **kwangs ):
    grp = cmds.group( *args, **kwangs )
    return convertSg( grp )





def getCurrentModelPanels():
    
    pannels = cmds.getPanel( vis=1 )

    modelPanels = []
    for pannel in pannels:
        if cmds.modelPanel( pannel, ex=1 ):
            modelPanels.append( pannel )
    return modelPanels




@convertName_dec
def combineMultiShapes( *shapeObjs ):
    
    shapes = []
    
    trNodes = cmds.listRelatives( shapeObjs, c=1, ad=1, type='transform' )
    if not trNodes: trNodes = []
    trNodes += shapeObjs
    
    for trNode in trNodes:
        childShapes = cmds.listRelatives( trNode, s=1, f=1 )
        if not childShapes: continue
        for childShape in childShapes:
            if cmds.nodeType( childShape ) != 'nurbsCurve': continue
            shapes.append( childShape )
    
    mtxGroup = cmds.getAttr( shapeObjs[0]+'.wm' )
    mmtxInvGroup = listToMatrix( mtxGroup ).inverse()
    
    for shape in shapes:
        shapeType = cmds.nodeType( shape )
        
        shapeTransform = cmds.listRelatives( shape, p=1 )[0]
        
        mtxShapeTransform = cmds.getAttr( shapeTransform+'.wm' )
        
        mmtxShapeTransform = listToMatrix( mtxShapeTransform )
        mmtxLocal = mmtxShapeTransform * mmtxInvGroup
        
        mtxLocal = matrixToList( mmtxLocal )
        trGeoNode = cmds.createNode( 'transformGeometry' )
        
        outputShapeNode = cmds.createNode( shapeType )
        outputShapeObject = cmds.listRelatives( outputShapeNode, p=1 )[0]
        if shapeType == 'mesh':
            outputAttr = 'outMesh'
            inputAttr = 'inMesh'
        elif shapeType == 'nurbsCurve':
            outputAttr = 'local'
            inputAttr  = 'create'
        elif shapeType == 'nurbsSurface':
            outputAttr = 'local'
            inputAttr = 'create'
        else:
            continue
            
        cmds.connectAttr( shape+'.'+outputAttr, trGeoNode+'.inputGeometry' )
        cmds.setAttr( trGeoNode+'.transform', mtxLocal, type='matrix' )
        cmds.connectAttr( trGeoNode+'.outputGeometry', outputShapeNode+'.'+inputAttr )
        
        outputShapeNode = cmds.parent( outputShapeNode, shapeObjs[0], add=1, shape=1 )
        cmds.delete( outputShapeObject )
        cmds.rename( outputShapeNode, shapeObjs[0]+'Shape' )
        cmds.refresh()
    
    cmds.delete( shapeObjs[1:])
    cmds.delete( cmds.listRelatives( shapeObjs[0], c=1, ad=1, f=1, type='transform' ) )
    
    return shapeObjs[0]



def duplicateShadingNetwork( shadingEngine ):
    
    import pymel.core
    shadingEngine = pymel.core.ls( shadingEngine )[0]
    shaderConnectedNodes = shadingEngine.listConnections( s=1, d=0 )
    
    hists = []
    for node in shaderConnectedNodes:
        if hasattr( node, 'worldMatrix' ):continue
        hists += node.history()
    
    shadingNodes = [shadingEngine.name()]
    duShadingNodes = [cmds.duplicate( shadingEngine.name() )[0]]
    for hist in hists:
        if hasattr( hist, 'worldMatrix' ): continue
        if hist.name() in shadingNodes: continue
        shadingNodes.append( hist.name() )
        duShadingNodes.append( cmds.duplicate( hist.name() )[0] )
    
    for i in range( len( shadingNodes ) ):
        shadingNode = shadingNodes[i]
        duOrig = duShadingNodes[i]
    
        srcCons = cmds.listConnections( shadingNode, s=1, d=0, p=1, c=1 )
        dstCons = cmds.listConnections( shadingNode, s=0, d=1, p=1, c=1 )
        if not srcCons: srcCons = []
        if not dstCons: dstCons = []

        for j in range( 0, len( srcCons ), 2 ):
            origCon = srcCons[j]
            srcCon  = srcCons[j+1]
            
            origAttr = '.'.join( origCon.split( '.' )[1:] )
            srcNode  = srcCon.split( '.' )[0]
            srcAttr  = '.'.join( srcCon.split( '.' )[1:] )
            
            if not srcNode in shadingNodes: continue
            targetIndex = shadingNodes.index(srcNode)
            duSrcNode = duShadingNodes[ targetIndex ]
            if cmds.isConnected( duSrcNode + '.' + srcAttr, duOrig + '.' + origAttr ): continue
            cmds.connectAttr( duSrcNode + '.' + srcAttr, duOrig + '.' + origAttr )
        
        for j in range( 0, len( dstCons ), 2 ):
            origCon = dstCons[j]
            dstCon  = dstCons[j+1]
            
            origAttr = '.'.join( origCon.split( '.' )[1:] )
            dstNode  = dstCon.split( '.' )[0]
            dstAttr  = '.'.join( dstCon.split( '.' )[1:] )

            if not dstNode in shadingNodes: continue
            targetIndex = shadingNodes.index(dstNode)
            duDstNode = duShadingNodes[ targetIndex ]
            if cmds.isConnected( duOrig + '.' + origAttr, duDstNode + '.' + dstAttr ): continue
            print duOrig + '.' + origAttr, duDstNode + '.' + dstAttr
            cmds.connectAttr( duOrig + '.' + origAttr, duDstNode + '.' + dstAttr )



def reverseOutput( target ):
    
    target = pymel.core.ls( target )[0]
    destCons = target.listConnections( s=0, d=1, p=1, c=1 )
    
    outputAttrs = []
    for origAttr, destAttr in destCons:
        if origAttr.parent():
            outputAttrs.append( origAttr.parent() )
        else:
            outputAttrs.append( origAttr )
    outputAttrs = list( set( outputAttrs ) )
    
    def connectReverseVectorOutput( outputAttr ):
        multNode = outputAttr.listConnections( type='multiplyDivide', s=0, d=1 )
        if multNode: multNode = multNode[0]
        else: multNode = None
        cons = outputAttr.listConnections( s=0, d=1, p=1, c=1 )
        if not cons: cons = []
        dstAttrs = []
        for origAttr, dstAttr in cons:
            dstAttrs.append( dstAttr )
        if not multNode:
            multNode = pymel.core.createNode( 'multiplyDivide' )
            outputAttr >> multNode.input1
            multNode.input2.set( 1,1,1 )
        if multNode.input2.listConnections( s=1, d=0 ):
            multNode = pymel.core.createNode( 'multiplyDivide' )
            outputAttr >> multNode.input1
            multNode.input2.set( 1,1,1 )
        origValue = multNode.input2.get()
        multNode.input2.set( -origValue[0], -origValue[1], -origValue[2] )
        for dstAttr in dstAttrs:
            if dstAttr.node() == multNode: continue
            multNode.output >> dstAttr
        
        childrenAttrs = outputAttr.children()
        for i in range( len( childrenAttrs ) ):
            childrenAttr = childrenAttrs[i]
            childrenCons = childrenAttr.listConnections( s=0, d=1, p=1, c=1 )
            if not childrenCons: childrenCons = []
            for origAttr, dstAttr in childrenCons:
                multNode.output.children()[i] >> dstAttr

    def connectReverseScalarOutput( outputAttr ):
        multNode = outputAttr.listConnections( type='multDoubleLinear', s=0, d=1 )
        if multNode: multNode = multNode[0]
        else: multNode = None
        if not multNode:
            multNode = pymel.core.createNode( 'multDoubleLinear' )
            outputAttr >> multNode.input1
            multNode.input2.set( 1 )
        if multNode.input2.listConnections( s=1, d=0 ):
            multNode = pymel.core.createNode( 'multDoubleLinear' )
            outputAttr >> multNode.input1
            multNode.input2.set( 1 )
        origValue = multNode.input2.get()
        multNode.input2.set( -origValue )
        cons = outputAttr.listConnections( s=0, d=1, p=1, c=1 )
        for origAttr, dstAttr in cons:
            if dstAttr.node() == multNode: continue
            multNode.output >> dstAttr

    for outputAttr in outputAttrs:
        try:
            childrenAttr = outputAttr.children()
            connectReverseVectorOutput( outputAttr )
        except:
            connectReverseScalarOutput( outputAttr )
            


@convertName_dec
def bezierCurve( *sels ):

    selPoses = []
    
    for sel in sels:
        selPos = cmds.xform( sel, q=1, ws=1, t=1 )[:3]
        selPoses.append( selPos )
    
    bezier = cmds.curve( bezier=1, p=selPoses, d=3 )
    bezier = cmds.listRelatives( bezier, s=1, f=1 )[0]
    
    for i in range( len( sels ) ):
        sel = sels[i]
        dcmp = cmds.createNode( 'decomposeMatrix' )
        cmds.connectAttr( sel + '.wm', dcmp + '.imat' )
        cmds.connectAttr( dcmp + '.ot', bezier + '.controlPoints[%d]' % i )



@convertSg_dec
def getCurveInfo( curve, **options ):
    
    space = 'world'
    if options.has_key( space ):
        space = options[ space ]
    
    curveShape = curve.shape()
    
    outputAttr = 'worldSpace'
    if space == 'local':
        outputAttr = 'local'
    
    cons = curveShape.attr( outputAttr ).listConnections( d=1, s=0, type='curveInfo' )
    if cons:
        return cons[0].name()
    
    curveInfo = createNode( 'curveInfo' )
    curveShape.attr( outputAttr ) >> curveInfo.inputCurve
    return curveInfo.name()



def makeCurveInfoTransforms( curve ):
    
    curve = pymel.core.ls( curve )[0]
    if curve.type() == 'transform':
        curveShape = curve.getShape()
    else:
        curveShape = curve
    numCVs = curveShape.numCVs()
    
    curveInfo = getCurveInfo( curve ) 
    curveInfo = pymel.core.ls( curveInfo )[0]
    
    targets = []
    for i in range( numCVs ):
        target = pymel.core.createNode( 'transform' )
        target.dh.set( 1 )
        vectorNode = pymel.core.createNode( 'vectorProduct' )
        vectorNode.op.set( 4 )
        curveInfo.controlPoints[i] >> vectorNode.input1
        target.pim >> vectorNode.matrix
        vectorNode.output >> target.t
        targets.append( target.name() )
    return targets



def makeFloorResult( tr, floorTr ):

    resultTr = createNode( 'transform' )
    condition = createNode( 'condition' ).setAttr( 'operation', 2 ).setAttr( 'colorIfFalseR', 0 )
    composeMtx = createNode( 'composeMatrix' )
    localDcmp = getDecomposeMatrix( getLocalMatrix( tr, floorTr ) )
    
    localDcmp.oty >> condition.firstTerm
    localDcmp.oty >> condition.colorIfTrueR
    
    localDcmp.otx >> composeMtx.itx
    condition.outColorR >> composeMtx.ity
    localDcmp.otz >> composeMtx.itz
    
    mm = createNode( 'multMatrix' )
    composeMtx.outputMatrix >> mm.i[0]
    convertSg( floorTr ).wm >> mm.i[1]
    resultTr.pim >> mm.i[2]
    dcmp = getDecomposeMatrix( mm )
    
    dcmp.ot >> resultTr.t



def setGeometryMatrixToTarget( geo, matrixTarget ):
    
    geo = convertSg( geo )
    matrixTarget = convertSg( matrixTarget )
    geoShapes = geo.listRelatives( s=1 )
    
    geoMatrix    = listToMatrix( geo.wm.get() )
    targetMatrix = listToMatrix( matrixTarget.wm.get() )
    
    for shape in geoShapes:
        if shape.attr( 'io' ).get():
            delete( shape )
    
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
            if cmds.nodeType( hist ) != 'mesh': continue
            if not cmds.getAttr( hist + '.io' ): continue
            origShape = convertSg( hist )
            break
        
        trGeo = createNode( 'transformGeometry' )
        origShape.attr( 'outMesh' ) >> trGeo.inputGeometry
        trGeo.outputGeometry >> geoShape.attr( 'inMesh' )
        trGeo.transform.set( matrixToList(geoMatrix * targetMatrix.inverse()), type='matrix' )
        cmds.select( geoShape.name() )
        cmds.DeleteHistory()
    
    geo.xform( ws=1, matrix= matrixTarget.wm.get() )


@convertSg_dec
def getNearPointOnCurve( tr, curve ):

    node = createNode( 'nearestPointOnCurve' )
    dcmp = getDecomposeMatrix( tr )
    curveShape = curve.shape()
    
    dcmp.ot >> node.inPosition
    curveShape.attr( 'worldSpace' ) >> node.inputCurve
    
    return node
    
    


@convertSg_dec
def replaceShape( src, dst ):
    
    dstShapes = dst.listRelatives( s=1 )
    srcShape = src.shape()
    
    delete( dstShapes )
    parent( srcShape, dst, add=1, shape=1 )
    
    
    
def todayNodeId():
    
    import datetime
    cuTime = datetime.datetime.now()
    sg = str( hex( 0x73 + 0x67 ) )
    today = str( hex( int( '%04d' % cuTime.year + '%02d' % cuTime.month + '%02d' % cuTime.day ) ) )
    return sg + " + " + today
    



@convertName_dec
def getSortedListByClosestPosition( srcGrp, targetGrp ):
    
    srcChildren = cmds.listRelatives( srcGrp, c=1, type='transform' )
    targetChildren = cmds.listRelatives( targetGrp, c=1, type='transform' )
    
    srcPoses = []
    for srcChild in srcChildren:
        srcPos = OpenMaya.MPoint( *cmds.xform( srcChild, q=1, ws=1, t=1 ) )
        srcPoses.append( srcPos )
    
    targetPoses = []
    for targetChild in targetChildren:
        targetPos = OpenMaya.MPoint( *cmds.xform( targetChild, q=1, ws=1, t=1 ) )
        targetPoses.append( targetPos )
    
    sortedChildren = []
    for i in range( len( srcPoses ) ):
        srcPose = srcPoses[i]
        minDist = 10000000.0
        minDistIndex = 0
        for j in range( len( targetPoses ) ):
            targetPose = targetPoses[j]
            dist = srcPose.distanceTo( targetPose )    
            if minDist > dist:
                minDist = dist
                minDistIndex = j
        
        sortedChildren.append( targetChildren[minDistIndex] )
    return sortedChildren
                


    

def getInfluencesFromSelVertices():
    
    sels = pymel.core.ls( sl=1, fl=1 )
    
    targetJnts = []
    for sel in sels:
        mesh = sel.node()
        hists = mesh.history()
        skinNode = None
        for hist in hists:
            if hist.type() == 'skinCluster':
                skinNode = hist
                break
        
        elements = skinNode.weightList[ sel.index() ].weights.elements()
        for element in elements:
            index = int( element.split( '[' )[-1].replace( ']', '' ) )
            jnts = skinNode.matrix[ index ].listConnections( s=1, d=0, type='joint' )
            for jnt in jnts:
                targetJnts.append( jnt.name() )
    
    return list( set( targetJnts ) )
    
    

def connectBindPre( targetGeo ):
    
    targetGeo = pymel.core.ls( sl=1, fl=1 )[0]
    
    hists = targetGeo.history( pdo=1 )
    
    skinNode = None
    for hist in hists:
        if hist.type() == 'skinCluster':
            skinNode = hist
            break
    
    cons = skinNode.matrix.listConnections( s=1, d=0, c=1 )
    for attr, targetJnt in cons:
        targetJnt.pim >> attr.replace( 'matrix', 'bindPreMatrix' )




def addOptionAttribute( target, enumName = "Options" ):
    
    target = convertSg( target )
    
    barString = '____'
    while target.attributeQuery( barString, ex=1 ):
        barString += '_'
    
    target.addAttr( ln=barString,  at="enum", en="%s:" % enumName, cb=1 )





def getUVAtPoint( point, mesh ):
    
    if type( point ) in [ type([]), type(()) ]:
        point = OpenMaya.MPoint( *point )
    
    meshShape = convertSg( mesh ).shape().name()
    fnMesh = OpenMaya.MFnMesh( getDagPath( meshShape ) )
    
    util = OpenMaya.MScriptUtil()
    util.createFromList( [0.0,0.0], 2 )
    uvPoint = util.asFloat2Ptr()
    fnMesh.getUVAtPoint( point, uvPoint, OpenMaya.MSpace.kWorld )
    u = OpenMaya.MScriptUtil.getFloat2ArrayItem( uvPoint, 0, 0 )
    v = OpenMaya.MScriptUtil.getFloat2ArrayItem( uvPoint, 0, 1 )
    
    return u, v
    
    
    

def createFollicleOnVertex( vertexName, ct= True, cr= True, **options ):
    
    vtx = pymel.core.ls( vertexName )[0]
    vtxPos = cmds.xform( vertexName, q=1, ws=1, t=1 )
    mesh = vertexName.split( '.' )[0]
    meshShape = vtx.plugNode().name()
    u, v = getUVAtPoint( vtxPos, mesh )
    
    follicleNode = cmds.createNode( 'follicle' )
    follicle = cmds.listRelatives( follicleNode, p=1, f=1 )[0]
    
    cmds.connectAttr( meshShape+'.outMesh', follicleNode+'.inputMesh' )
    cmds.connectAttr( meshShape+'.wm', follicleNode+'.inputWorldMatrix' )
    
    cmds.setAttr( follicleNode+'.parameterU', u )
    cmds.setAttr( follicleNode+'.parameterV', v )
    
    if options.has_key( 'local' ) and options['local']:
        if ct: cmds.connectAttr( follicleNode+'.outTranslate', follicle+'.t' )
        if cr: cmds.connectAttr( follicleNode+'.outRotate', follicle+'.r' )
    else:
        compose = cmds.createNode( 'composeMatrix' )
        mm = cmds.createNode( 'multMatrix' )
        dcmp = cmds.createNode( 'decomposeMatrix' )
        cmds.connectAttr( compose + '.outputMatrix', mm + '.i[0]' )
        cmds.connectAttr( follicle + '.pim', mm + '.i[1]' )
        cmds.connectAttr( mm + '.matrixSum', dcmp + '.imat' )
        if ct: cmds.connectAttr( follicleNode+'.outTranslate', compose+'.it' )
        if cr: cmds.connectAttr( follicleNode+'.outRotate', compose+'.ir' )
        if ct: cmds.connectAttr( dcmp + '.ot', follicle + '.t' )
        if cr: cmds.connectAttr( dcmp + '.or', follicle + '.r' )
    
    return follicle





def createFollicleOnClosestPoint( targetObj, mesh ):
        
    vtxPos = cmds.xform( targetObj, q=1, ws=1, t=1 )
    meshShape = convertSg( mesh ).shape().name()
    u, v = getUVAtPoint( vtxPos, mesh )
    
    follicleNode = cmds.createNode( 'follicle' )
    follicle = cmds.listRelatives( follicleNode, p=1, f=1 )[0]
    
    cmds.connectAttr( meshShape+'.outMesh', follicleNode+'.inputMesh' )
    cmds.connectAttr( meshShape+'.wm', follicleNode+'.inputWorldMatrix' )
    
    cmds.setAttr( follicleNode+'.parameterU', u )
    cmds.setAttr( follicleNode+'.parameterV', v )
    
    cmds.connectAttr( follicleNode+'.outTranslate', follicle+'.t' )
    cmds.connectAttr( follicleNode+'.outRotate', follicle+'.r' )






def getMeshAndIndicesPoints( selObjects ):
    
    selObjects = cmds.ls( cmds.polyListComponentConversion( selObjects, tv=1 ), fl=1 )
    
    mesh = ''
    vtxIndices = []
    for obj in selObjects:
        splits = obj.split( '.' )
        if len( splits ) == 1:
            mesh = obj
        else:
            mesh = splits[0]
            index = int( splits[1].split( '[' )[-1].replace( ']', '' ) )
            vtxIndices.append( index )
    
    if vtxIndices:
        vtxIndices = list( set( vtxIndices ) )
    else:
        vtxIndices = [ i for i in range( OpenMaya.MFnMesh( getDagPath( mesh ) ).numVertices() ) ]
    
    return mesh, vtxIndices



def getNodeFromHistory( target, nodeType ):
    
    pmTarget = pymel.core.ls( target )[0]
    hists = pmTarget.history( pdo=1 )
    targetNodes = []
    for hist in hists:
        if hist.type() == nodeType:
            targetNodes.append( hist.name() )
    return targetNodes



def getInfluenceAndWeightList( mesh, vertices = [] ):

    skinClusters = getNodeFromHistory( mesh, 'skinCluster' )
    if not skinClusters: return None
    
    skinCluster = skinClusters[0]
    print "skincluster : ", skinCluster
    
    fnSkinCluster = OpenMaya.MFnDependencyNode( getMObject( skinCluster ) )
    plugWeightList = fnSkinCluster.findPlug( 'weightList' )
    
    if not vertices: vertices = [ i for i in range( plugWeightList.numElements() ) ]
    influenceAndWeightList = [ [] for i in range( len( vertices ) ) ]
    phygicalMap = [ 0 for i in range( plugWeightList.numElements() ) ]
    
    for i in range( len( vertices ) ):
        logicalIndex = vertices[i]
        plugWeights = plugWeightList[ logicalIndex ].child( 0 )
        influenceNums = []
        values = []
        for j in range( plugWeights.numElements() ):
            influenceNum = plugWeights[j].logicalIndex()
            value = plugWeights[j].asFloat()
            influenceNums.append( influenceNum )
            values.append( value )
        
        influenceAndWeightList[i] = [ influenceNums, values ]
        phygicalMap[ logicalIndex ] = i
        
    return influenceAndWeightList, phygicalMap




def getMeshLocalPoints( mesh ):
    
    fnMesh = OpenMaya.MFnMesh( getDagPath( mesh ) )
    points = OpenMaya.MPointArray()
    fnMesh.getPoints( points )
    return points




def createRivetBasedOnSkinWeights( selectedObjs ):
    
    def getPlugMatrix( mesh ):
        skinCluster = getNodeFromHistory( mesh, 'skinCluster' )
        if not skinCluster: return None
        skinCluster = skinCluster[0]
        fnSkinCluster = OpenMaya.MFnDependencyNode( getMObject( skinCluster ) )
        
        return fnSkinCluster.findPlug( 'matrix' )
    
    def getPlugBindPre( mesh ):
    
        skinCluster = getNodeFromHistory( mesh, 'skinCluster' )
        if not skinCluster: return None
        skinCluster = skinCluster[0]
        fnSkinCluster = OpenMaya.MFnDependencyNode( getMObject( skinCluster ) )
        
        return fnSkinCluster.findPlug( 'bindPreMatrix' )
    
    
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


    mesh, vtxIndices = getMeshAndIndicesPoints( selectedObjs )
    
    skinClusterNode = getNodeFromHistory( mesh, 'skinCluster' )
    if not skinClusterNode: return None
    skinClusterNode = skinClusterNode[0]
    
    influenceAndWeightList, phygicalMap = getInfluenceAndWeightList( mesh, vtxIndices )
    
    meshMatrix = getDagPath( mesh ).inclusiveMatrix()
    meshPoints = getMeshLocalPoints( mesh )
    plugMatrix = getPlugMatrix( mesh )
    plugBindPre = getPlugBindPre( mesh )
    
    BB = OpenMaya.MBoundingBox()
    
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
    
    mmtxWtAdd = listToMatrix( mtxWtAdd )
    worldPoint *= mmtxWtAdd.inverse()
    cmds.setAttr( origObj+'.t', worldPoint.x, worldPoint.y, worldPoint.z )



def getCloseSurfaceNode( target, surface ):
    
    surfShape = cmds.listRelatives( surface, s=1 )[0]
    
    closeNode = cmds.createNode( 'closestPointOnSurface' )
    dcmp = cmds.createNode( 'decomposeMatrix' )
    
    cmds.connectAttr( target+'.wm', dcmp+'.imat' )
    cmds.connectAttr( dcmp+'.ot', closeNode+'.inPosition' )
    cmds.connectAttr( surfShape+'.worldSpace', closeNode+'.inputSurface' )
    
    print closeNode
    return closeNode



def getPointOnSurfaceNode( target, surface, keepClose=False ):
    
    surfShape = cmds.listRelatives( surface, s=1 )[0]
    
    node = cmds.createNode( 'pointOnSurfaceInfo' )
    cmds.connectAttr( surfShape+'.local', node+'.inputSurface' )
    
    closeNode = getCloseSurfaceNode( target, surface )
    
    if not keepClose:
        cmds.setAttr( node+'.u', cmds.getAttr( closeNode+'.u' ) )
        cmds.setAttr( node+'.v', cmds.getAttr( closeNode+'.v' ) )
        cmds.delete( closeNode )
    else:
        cmds.connectAttr( closeNode+'.u', node+'.u' )
        cmds.connectAttr( closeNode+'.v', node+'.v' )
    
    return node


def createTransformOnSurface( target, surface, keepClose=False ):
    
    pointOnSurfNode = getPointOnSurfaceNode( target, surface, keepClose )
    
    tr = cmds.createNode( 'transform', n='P'+target )
    fbfMtx = cmds.createNode( 'fourByFourMatrix' )
    dcmp   = cmds.createNode( 'decomposeMatrix' )
    vectorNode = cmds.createNode( 'vectorProduct' )
    cmds.setAttr( vectorNode+'.op', 2 )
    cmds.connectAttr( pointOnSurfNode+'.tu', vectorNode+'.input1' )
    cmds.connectAttr( pointOnSurfNode+'.n', vectorNode+'.input2' )
    cmds.connectAttr( vectorNode+'.outputX', fbfMtx+'.i00' )
    cmds.connectAttr( vectorNode+'.outputY', fbfMtx+'.i01' )
    cmds.connectAttr( vectorNode+'.outputZ', fbfMtx+'.i02' )
    cmds.connectAttr( pointOnSurfNode+'.px', fbfMtx+'.i30' )
    cmds.connectAttr( pointOnSurfNode+'.py', fbfMtx+'.i31' )
    cmds.connectAttr( pointOnSurfNode+'.pz', fbfMtx+'.i32' )
    cmds.connectAttr( pointOnSurfNode+'.nx', fbfMtx+'.i10' )
    cmds.connectAttr( pointOnSurfNode+'.ny', fbfMtx+'.i11' )
    cmds.connectAttr( pointOnSurfNode+'.nz', fbfMtx+'.i12' )
    cmds.connectAttr( pointOnSurfNode+'.position', tr+'.t' )
    cmds.connectAttr( fbfMtx+'.output', dcmp+'.imat' )
    cmds.connectAttr( dcmp+'.or', tr+'.r' )
    
    cmds.setAttr( tr+'.dh', 1 )
    cmds.setAttr( tr+'.dla', 1 )
    
    return tr


def setBindPreToJntP( sels ):
    
    for sel in sels:
        cons = cmds.listConnections( sel+'.wm', d=1, s=0, p=1, c=1, type='skinCluster' )
        selP = cmds.listRelatives( sel, p=1 )[0]
        
        inputCons = cons[1::2]
        
        for inputCon in inputCons:
            bindPreAttr = inputCon.replace( 'matrix[', 'bindPreMatrix[' )
            cmds.connectAttr( selP+'.wim', bindPreAttr )




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





def weightHammerCurve( targets ):
    import maya.OpenMaya as om
    
    def getWeights( plug ):
        childPlug = plug.child(0)
        numElements = childPlug.numElements()
        indicesAndValues = []
        for i in range( numElements ):
            logicalIndex = childPlug[i].logicalIndex()
            value        = childPlug[i].asFloat()
            indicesAndValues.append( [ logicalIndex, value ] )
        return indicesAndValues
    
    def getMixWeights( first, second, rate ):
        
        invRate = 1.0-rate
        
        print first
        print second
        
        firstMaxIndex = first[-1][0]
        secondMaxIndex = second[-1][0]
        maxIndex = firstMaxIndex+1
        
        if firstMaxIndex < secondMaxIndex:
            maxIndex = secondMaxIndex+1
        
        firstLogicalMap  = [ False for i in range( maxIndex ) ]
        secondLogicalMap = [ False for i in range( maxIndex ) ]
        
        for index, value in first:
            firstLogicalMap[ index ] = True
            
        for index, value in second:
            secondLogicalMap[ index ] = True
        
        returnTargets = []
        
        for index, value in first:
            returnTargets.append( [index, invRate * value] )
        for index, value in second:
            if firstLogicalMap[ index ]:
                for i in range( len( returnTargets ) ):
                    wIndex = returnTargets[i][0]
                    if wIndex == index:
                        returnTargets[i][1] += rate * value
                        break
            else:
                returnTargets.append( [index, rate * value] )
        return returnTargets
    
    def clearArray( targetPlug ):
        plugChild = targetPlug.child( 0 )
        targetInstances = []
        for i in range( plugChild.numElements() ):
            targetInstances.append( plugChild[i].name() )
        targetInstances.reverse()
        for i in range( len( targetInstances ) ):
            cmds.removeMultiInstance( targetInstances[i] )
        
    
    node = targets[0].split( '.' )[0]
    
    skinClusterNodes = getNodeFromHistory( node, 'skinCluster' )
    if not skinClusterNodes: return None
    
    fnSkinCluster = OpenMaya.MFnDependencyNode( getMObject( skinClusterNodes[0] ) )
    plugWeightList = fnSkinCluster.findPlug( 'weightList' )
    
    cmds.select( targets )
    for dagPath, uArr, vArr, wArr in getMDagPathAndComponent():
        
        fnCurve = OpenMaya.MFnNurbsCurve( dagPath )
        startNum = 0
        lastNum = fnCurve.numCVs()-1
        
        if uArr[-1] == lastNum:
            pass
        elif uArr[0] == startNum:
            pass
        elif uArr[0] == startNum and uArr[-1] == lastNum:
            pass
        else:
            weightStart = getWeights( plugWeightList[ uArr[0]-1 ] )
            weightEnd   = getWeights( plugWeightList[ uArr[-1]+1 ] )
            
            length = uArr.length()
            for i in range( uArr.length() ):
                clearArray( plugWeightList[ uArr[i] ] )
                plugWeightListEmelent = plugWeightList.elementByLogicalIndex( uArr[i] )
                
                rate = float( i+1 ) / (length+2)
                weights = getMixWeights( weightStart, weightEnd, rate )
                for index, value in weights:
                    targetPlug = plugWeightListEmelent.child(0).elementByLogicalIndex( index )
                    cmds.setAttr( targetPlug.name(), value )
        cmds.skinPercent( skinClusterNodes[0], normalize=1 )



def setSkinWeightOnlyVertices( selVertices ):
    
    for dagPath, vtxIds in getSelectedVertices( selVertices ):
        fnNode = OpenMaya.MFnDagNode( dagPath )
        mesh = cmds.ls( fnNode.partialPathName() )[0]
        hists = cmds.listHistory( mesh, pdo=1 )
        
        skinNode = ''
        for hist in hists:
            if cmds.nodeType( hist ) == 'skinCluster':
                skinNode = OpenMaya.MFnDependencyNode( getMObject( hist ) )
                break
        
        if not skinNode: continue
        
        weightListPlug = skinNode.findPlug( 'weightList' )
        
        for i in range( vtxIds.length() ):
            vtxId = vtxIds[i]
            weightsPlug = weightListPlug[vtxId].child( 0 )
            
            largeInfluence = 0.0
            largeIndex = -1
            for j in range( weightsPlug.numElements() ):
                weight = weightsPlug[j].asFloat()
                if weight > largeInfluence:
                    largeInfluence = weight
                    largeIndex = j
            
            if largeIndex == -1: continue
            
            targetMatrixIndex = -1
            for j in range( weightsPlug.numElements() ):
                if j == largeIndex:
                    cmds.setAttr( weightsPlug[j].name(), 1 )
                    targetMatrixIndex = weightsPlug[j].logicalIndex()
                else:
                    cmds.setAttr( weightsPlug[j].name(), 0 )
            
            if targetMatrixIndex == -1: continue
            
            for k in range( weightListPlug.numElements() ):
                if vtxId == k: continue
                weightsPlug = weightListPlug[k].child(0)
                for m in range( weightsPlug.numElements() ):
                    if targetMatrixIndex != weightsPlug[m].logicalIndex(): continue
                    cmds.setAttr( weightsPlug[m].name(), 0 )

    cmds.refresh()
    cmds.skinPercent( skinNode.name(), normalize=1 )










@convertName_dec
def aimConstraint( *args, **kwargs ):
    
    if kwargs.has_key( 'wuo' ) or kwargs.has_key( 'worldUpObject' ):
        kwargs['wuo'] = convertName( kwargs['wuo'] ) 
    
    return cmds.aimConstraint( *args, **kwargs )\
    





@convertSg_dec
def getMultDoubleLinear( node=None ):
    
    multNode = createNode( 'multDoubleLinear' )
    
    if node:
        if node.nodeType() == 'distanceBetween':
            node.distance >> multNode.input1
    
    return multNode




@convertSg_dec
def createSquashBend( *geos, **options ):
        
    if not type( geos ) in [ list, tuple ]:
        geos = [geos]
        
    geoNames = [ geo.name() for geo in geos ]
    
    allbb = OpenMaya.MBoundingBox()
    for geo in geos:
        bb = cmds.exactWorldBoundingBox( geo.name() )
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
    squashBase = createNode( 'transform', n='sauashBase' ).setAttr( 't', lowerPoint )
    upperCtl = makeController( sgdata.Controllers.trianglePoints, dist*0.2 )
    upperCtl.setAttr( 'shape_ty', 1 ).setAttr( 'shape_rz', 180 )
    pUpperCtl = convertSg( makeParent( upperCtl ) )
    lowerCtl = makeController( sgdata.Controllers.trianglePoints, dist*0.2 )
    lowerCtl.setAttr( 'shape_ty', -1 )
    pLowerCtl = convertSg( makeParent( lowerCtl ) )
    upperCtl.rename( 'Ctl_Upper' )
    lowerCtl.rename( 'Ctl_Lower' )
    pUpperCtl.t.set( *upperPoint )
    pLowerCtl.t.set( *lowerPoint )
    
    parent( pUpperCtl, squashBase )
    parent( pLowerCtl, squashBase )
    
    squashCenter = squashBase.makeChild().rename( 'squashCenter' )
    blendMtxNode = getBlendTwoMatrixNode( upperCtl, lowerCtl )
    multMtx = createNode( 'multMatrix' )
    blendMtxNode.matrixSum >> multMtx.i[0]
    squashCenter.attr( 'pim' ) >> multMtx.i[1]
    dcmpBlend = getDecomposeMatrix( multMtx )
    squashCenter.tx.set( pUpperCtl.tx.get() )
    squashCenter.tz.set( pUpperCtl.tz.get() )
    dcmpBlend.oty >> squashCenter.ty
    
    rigedCurve = createRigedCurve( lowerCtl, upperCtl )
    cmds.setAttr( rigedCurve + '.v' , 0 )
    upperFirstChild = upperCtl.listRelatives( c=1, type='transform' )[0]
    lowerFirstChild = lowerCtl.listRelatives( c=1, type='transform' )[0]
    parent( rigedCurve, squashBase )
    
    lookAtUpper = upperCtl.makeChild().rename( 'lookAtObj_' + upperCtl.name() )
    lookAtLower = lowerCtl.makeChild().rename( 'lookAtObj_' + lowerCtl.name() )
    lookAtConnect( squashCenter, lookAtUpper )
    lookAtConnect( squashCenter, lookAtLower )
    
    multLookAtUpper = createNode( 'multiplyDivide' )
    multLookAtLower = createNode( 'multiplyDivide' )
    
    lookAtUpper.r >> multLookAtUpper.input1
    lookAtLower.r >> multLookAtLower.input1
    addOptionAttribute( upperCtl )
    addOptionAttribute( lowerCtl )
    upperCtl.addAttr( ln='autoOrient', min=0, max=1, dv=1, k=1 )
    lowerCtl.addAttr( ln='autoOrient', min=0, max=1, dv=1, k=1 )
    upperCtl.autoOrient >> multLookAtUpper.input2X
    upperCtl.autoOrient >> multLookAtUpper.input2Y
    upperCtl.autoOrient >> multLookAtUpper.input2Z
    lowerCtl.autoOrient >> multLookAtLower.input2X
    lowerCtl.autoOrient >> multLookAtLower.input2Y
    lowerCtl.autoOrient >> multLookAtLower.input2Z
    
    multLookAtUpper.output >> upperFirstChild.r
    multLookAtLower.output >> lowerFirstChild.r
    
    rebuildCurve, rebuildNode = cmds.rebuildCurve( rigedCurve, ch=1, rpo=0, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=3, d=3, tol=0.01 )
    rebuildCurve = cmds.parent( rebuildCurve, squashBase.name() )
    
    numDiv = 4
    if options.has_key( 'numDiv' ):
        numDiv = options['numDiv']
    
    eachParam = 1.0 / (numDiv-1)
    targetNodes = []
    circleTrs = []
    for i in range( numDiv ):
        targetNode = createPointOnCurve( rebuildCurve, local=1 )
        cmds.setAttr( targetNode + '.dh', 0 )
        cmds.setAttr( targetNode + '.parameter', eachParam * i )
        targetNode = cmds.parent( targetNode, squashBase.name() )[0]
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
        blendNode = createBlendTwoMatrixNode( lookAtLower.name(), lookAtUpper.name() )
        cmds.setAttr( blendNode + '.blend', eachParam * i )
        tangentNode = cmds.tangentConstraint( rebuildCurve, targetNodes[i], aim=[0,1,0], u=[0,0,1], wu=[0,0,1], wut='objectrotation')[0]
        cmds.connectAttr( blendNode+ '.matrixSum', tangentNode + '.worldUpMatrix' )
    pass

    cmds.select( geoNames )
    ffd, ffdLattice, ffdLatticeBase = cmds.lattice( geoNames,  divisions=[2, numDiv, 2], objectCentered=True, ldv=[2,numDiv+1,2] )
    ffdLattice, ffdLatticeBase = cmds.parent( ffdLattice, ffdLatticeBase, squashBase.name() )
    
    cmds.setAttr( ffdLattice + '.inheritsTransform', 0 )
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
    
    upperCtl.addAttr( 'squash', min=0, dv=1, k=1 )
    upperCtl.addAttr( 'showDetail', min=0, max=1, cb=1 )
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
    
    



def makeCloneObject( target, **options  ):
    
    target = pymel.core.ls( target )[0]
    
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
            targetClone = pymel.core.createNode( 'transform', n= cuTarget.split( '|' )[-1]+cloneLabel )
            targetClone.message >> cuTarget.attr( op_cloneAttrName )
            
            if op_shapeOn:
                cuTargetShape = cuTarget.getShape()
                if cuTargetShape:
                    duObj = pymel.core.duplicate( cuTarget, n=targetClone+'_du' )[0]
                    duShape = duObj.getShape()
                    pymel.core.parent( duShape, targetClone, add=1, shape=1 )[0]
                    duShape.rename( targetClone+'Shape' )
                    pymel.core.delete( duObj )
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
    return targetCloneParent.name()




def copyShader( srcObj, dstObj ):
    
    srcObj = pymel.core.ls( srcObj )[0]
    dstObj = pymel.core.ls( dstObj )[0]
    
    if srcObj.type() == 'transform':
        srcObj = srcObj.getShape()
    if dstObj.type() == 'transform':
        dstObj = dstObj.getShape()
    
    shadingEngine = srcObj.listConnections( s=0, d=1, type='shadingEngine' )
    if not shadingEngine:
        cmds.warning( "%s has no shading endgine" % srcObj.name )
        return None
    cmds.sets( dstObj.name(), e=1, forceElement = shadingEngine[0].name() )




def getSourceConnectedMesh( meshGrp, cloneAttrName = '_other', **options ):
    
    copyShaderOn = True
    if options.has_key( 'copyShader' ):
        copyShaderOn = options['copyShader']
    
    
    meshGrp = pymel.core.ls( meshGrp )[0]
    children = meshGrp.listRelatives( c=1, ad=1, type='transform' )
    children.append( meshGrp )
    
    targetMeshs = []
    for child in children:
        childShape = child.getShape()
        if not childShape: continue
        if childShape.type() != 'mesh': continue
        targetMeshs.append( child )
    
    for targetMesh in targetMeshs:
        meshShape = targetMesh.getShape()
        clonedTransform = makeCloneObject( targetMesh, cloneAttrName= cloneAttrName )
        copyShapeToTransform( meshShape.name(), clonedTransform )
        
        clonedTransform = pymel.core.ls( clonedTransform )[0]
        clonedShape = clonedTransform.getShape()
        
        cons = meshShape.inMesh.listConnections( s=1, d=0, p=1 )
        if cons:
            cons[0] >> clonedShape.inMesh
        else:
            oTarget = getMObject( clonedTransform.name() )
            oMesh = getMObject( meshShape.name() )
            fnMesh = OpenMaya.MFnMesh( oMesh )
            fnMesh.copy( oMesh, oTarget )
        
        if copyShaderOn : copyShader( meshShape, clonedShape )
        else: cmds.sets( clonedShape.name(), e=1, forceElement = 'initialShadingGroup' )




def createFourByFourMatrixCube( target ):
    
    cubeObj, cubeNode = pymel.core.polyCube( ch=1, o=1, cuv=4 )
    
    xVtx = cubeObj.name() + '.vtx[7]'
    yVtx = cubeObj.name() + '.vtx[4]'
    zVtx = cubeObj.name() + '.vtx[0]'
    pVtx = cubeObj.name() + '.vtx[6]'
    
    xFollicle = createFollicleOnVertex( xVtx, True, False )
    yFollicle = createFollicleOnVertex( yVtx, True, False )
    zFollicle = createFollicleOnVertex( zVtx, True, False )
    pFollicle = createFollicleOnVertex( pVtx, True, False )
    
    cubeObj.addAttr( 'size', dv=1, k=1 )
    
    cubeShape = cubeObj.getShape()
    composeOffset = pymel.core.createNode( 'composeMatrix' )
    composeScale  = pymel.core.createNode( 'composeMatrix' )
    multMatrix = pymel.core.createNode( 'multMatrix' )
    trGeo = pymel.core.createNode( 'transformGeometry' )
    composeOffset.it.set( .5, .5, .5 )
    cubeObj.size >> composeScale.isx
    cubeObj.size >> composeScale.isy
    cubeObj.size >> composeScale.isz
    composeOffset.outputMatrix >> multMatrix.i[0]
    composeScale.outputMatrix >> multMatrix.i[1]
    cubeNode.output >> trGeo.inputGeometry
    multMatrix.matrixSum >> trGeo.transform
    trGeo.outputGeometry >> cubeShape.inMesh
    
    xDcmp = getDecomposeMatrix( getLocalMatrix( xFollicle, pFollicle ) )
    yDcmp = getDecomposeMatrix( getLocalMatrix( yFollicle, pFollicle ) )
    zDcmp = getDecomposeMatrix( getLocalMatrix( zFollicle, pFollicle ) )
    
    pFollicle = pymel.core.ls( pFollicle )[0]
    cubeObj.size >> pFollicle.sx
    cubeObj.size >> pFollicle.sy
    cubeObj.size >> pFollicle.sz
    
    fbf = pymel.core.createNode( 'fourByFourMatrix' )
    xDcmp.otx >> fbf.in00
    xDcmp.oty >> fbf.in01
    xDcmp.otz >> fbf.in02
    yDcmp.otx >> fbf.in10
    yDcmp.oty >> fbf.in11
    yDcmp.otz >> fbf.in12
    zDcmp.otx >> fbf.in20
    zDcmp.oty >> fbf.in21
    zDcmp.otz >> fbf.in22
    pFollicle.tx >> fbf.in30
    pFollicle.ty >> fbf.in31
    pFollicle.tz >> fbf.in32
    
    newTr = pymel.core.createNode( 'transform' )
    newTr.attr( 'dh').set( 1 )
    newTr.attr( 'dla').set( 1 )
    dcmp = pymel.core.createNode( 'decomposeMatrix' )
    fbf.output >> dcmp.imat
    
    dcmp.outputTranslate >> newTr.t
    dcmp.outputRotate  >> newTr.r
    dcmp.outputScale  >> newTr.s
    dcmp.outputShear >> newTr.sh
    
    pymel.core.select( newTr )
    pymel.core.group( newTr, cubeObj, xFollicle, yFollicle, zFollicle, pFollicle )
    
    cmds.xform( cubeObj.name(), ws=1, matrix= cmds.getAttr( target + '.wm' ) )
    
    return newTr.name(), cubeObj.name()
    
    
    
    
def selectNoneAffectMeshs( *args ):
    
    def cleanMesh( targetObj ):
    
        targetShapes = cmds.listRelatives( targetObj, s=1, f=1 )
        returnShapes  =[]
        for targetShape in targetShapes:
            if not cmds.getAttr( targetShape+'.io' ): continue
            if cmds.listConnections( targetShape, s=0, d=1 ): continue
            cmds.warning( "none affect mesh : %s" % targetShape )
            returnShapes.append( targetShape )
        return returnShapes
        
    meshs = cmds.ls( type='mesh' )
    
    meshObjs = []
    for mesh in meshs:
        if cmds.getAttr( mesh+'.io' ): continue
        meshP = cmds.listRelatives( mesh, p=1, f=1 )[0]
        if meshP in meshObjs: continue
        meshObjs.append( meshP ) 
    
    targetShapes = []
    for meshObj in meshObjs:
        targetShapes += cleanMesh( meshObj )
    cmds.select( targetShapes )




def duplicateRigedCurve( rigedCurve ):
    
    curveShapes = cmds.listRelatives( rigedCurve, s=1, f=1 )
    if not curveShapes: return None

    cons = cmds.listConnections( curveShapes[0], s=1, d=0, p=1, c=1 )
    
    srcCons = cons[1::2]
    dstCons = cons[::2]
    
    duCurve = cmds.duplicate( rigedCurve, n= rigedCurve.split('|')[-1] + '_du' )[0]
    duShape = cmds.listRelatives( duCurve, s=1, f=1 )[0]
    
    for i in range( len( srcCons ) ):
        srcAttr = srcCons[i]
        dstAttr = duShape + '.' + dstCons[i].split( '.' )[-1]
        cmds.connectAttr( srcAttr, dstAttr )
    return duCurve



@convertSg_dec
def createRigedCurve( *ctls ):
    
    firstCtl = ctls[0]
    firstCtlNext = ctls[1]
    lastCtlBefore = ctls[-2]
    lastCtl = ctls[-1]
    
    firstCtl.addAttr( ln='frontMult', cb=1, dv=0.3 )
    lastCtl.addAttr( ln='backMult', cb=1, dv=0.3 )
    
    firstPointerGrp = createNode( 'transform' )
    firstPointer1 = firstPointerGrp.makeChild()
    firstPointer2 = firstPointerGrp.makeChild()
    firstPointerGrp.parentTo( firstCtl ).setTransformDefault()
    
    lastPointerGrp = createNode( 'transform' )
    lastPointer1 = lastPointerGrp.makeChild()
    lastPointer2 = lastPointerGrp.makeChild()
    lastPointerGrp.parentTo( lastCtl ).setTransformDefault()
    
    dcmpFirst = getDecomposeMatrix( getLocalMatrix( firstCtlNext, firstCtl ) )
    distFirst = getDistance( dcmpFirst )
    dcmpLast = getDecomposeMatrix( getLocalMatrix( lastCtlBefore, lastCtl ) ) 
    distLast = getDistance( dcmpLast )
    
    firstDirIndex = getDirectionIndex( dcmpFirst.ot.get() )
    firstReverseMult = -1 if firstDirIndex >= 3 else 1
    firstTargetAttr = ['tx','ty','tz'][firstDirIndex%3]
    lastDirIndex = getDirectionIndex( dcmpLast.ot.get() )
    lastReverseMult = -1 if lastDirIndex >= 3 else 1
    lastTargetAttr  = ['tx','ty','tz'][lastDirIndex%3]
    
    firstReverseMultNode = createNode( 'multDoubleLinear' ).setAttr( 'input2', firstReverseMult )
    lastReverseMultNode = createNode( 'multDoubleLinear' ).setAttr( 'input2', lastReverseMult )
    firstReverseMultNode1 = createNode( 'multDoubleLinear' ).setAttr( 'input2', firstReverseMult )
    lastReverseMultNode1 = createNode( 'multDoubleLinear' ).setAttr( 'input2', lastReverseMult )
    multFirstPointer1 = createNode( 'multDoubleLinear' ).setAttr( 'input2',  0.05 )
    multFirstPointer2 = createNode( 'multDoubleLinear' ).setAttr( 'input2',  0.3 )
    multLastPointer1 = createNode( 'multDoubleLinear' ).setAttr( 'input2',  0.05 )
    multLastPointer2 = createNode( 'multDoubleLinear' ).setAttr( 'input2',  0.3 )
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
        
        ctlPointerGrp = ctl.makeChild()
        ctlPointer1 = ctlPointerGrp.makeChild()
        ctlPointer2 = ctlPointerGrp.makeChild()
        
        dcmpBefore = getDecomposeMatrix( getLocalMatrix( beforeCtl, ctl ) )
        distBefore = getDistance( dcmpBefore )
        dcmpAfter  = getDecomposeMatrix( getLocalMatrix( nextCtl, ctl ) ) 
        distAfter  = getDistance( dcmpAfter )
        
        dirIndexB = getDirectionIndex( dcmpBefore.ot.get() )
        reverseMultB = -1 if dirIndexB >= 3 else 1
        targetAttrB = ['tx','ty','tz'][dirIndexB%3]
        dirindexA = getDirectionIndex( dcmpAfter.ot.get() )
        reverseMultA = -1 if dirindexA >= 3 else 1
        targetAttrA = ['tx','ty','tz'][dirindexA%3]
        
        ctl.addAttr( 'beforeMult', dv=0.3, cb=1 )
        ctl.addAttr( 'afterMult', dv=0.3, cb=1 )
        multBefore = createNode( 'multDoubleLinear' ).setAttr( 'input2', reverseMultB )
        multAfter  = createNode( 'multDoubleLinear' ).setAttr( 'input2', reverseMultA )
        ctl.beforeMult >> multBefore.input1
        ctl.afterMult  >> multAfter.input1
        
        multBeforePointer = createNode( 'multDoubleLinear' ).setAttr( 'input2',  0.3 * reverseMultB )
        multAfterPointer  = createNode( 'multDoubleLinear' ).setAttr( 'input2',  0.3 * reverseMultA )
        
        distBefore.distance >> multBeforePointer.input1
        distAfter.distance >> multAfterPointer.input1
        multBefore.output >> multBeforePointer.input2
        multAfter.output >> multAfterPointer.input2
        
        multBeforePointer.output >> ctlPointer1.attr( targetAttrB )
        multAfterPointer.output >> ctlPointer2.attr( targetAttrA )
        
        pointerList.insert( -3, ctlPointer1 )
        pointerList.insert( -3, ctlPointer2 )

    return makeCurveFromSelection( pointerList )




def addCurveDistanceInfo( curve ):
    
    NAME_origLength = 'origLength'
    NAME_currentLength = 'currentLength'
    
    curve = pymel.core.ls( curve )[0]
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




def addCurveSquashInfo( curve ):
    
    NAME_squashValue = 'squashValue'
    origLengthAttr, currentLengthAttr = addCurveDistanceInfo( curve )
    
    curve = pymel.core.ls( curve )[0]
    if not pymel.core.attributeQuery( NAME_squashValue, node=curve, ex=1 ):curve.addAttr( NAME_squashValue )
    pymel.core.setAttr( curve.squashValue, e=1, cb=1 )
    
    if not curve.squashValue.listConnections( s=1, d=0, type='multiplyDivide' ):
        divNode = pymel.core.createNode( 'multiplyDivide' )
        powNode = pymel.core.createNode( 'multiplyDivide' )
        divNode.op.set( 2 )
        powNode.op.set( 3 ); powNode.input2X.set( 0.5 )
        curve.attr( origLengthAttr ) >> divNode.input1X
        curve.attr( currentLengthAttr ) >> divNode.input2X
        divNode.outputX >> powNode.input1X
        powNode.outputX >> curve.squashValue
    
    return NAME_squashValue





def getConnectedVertices( vtxName ):

    dagPath, vtxid = getSelectedVertices( vtxName )[0]
    
    util = OpenMaya.MScriptUtil()
    util.createFromInt(0)
    intPtr = util.asIntPtr()
    
    itVtx = OpenMaya.MItMeshVertex( dagPath )
    itVtx.setIndex( vtxid[0], intPtr )
    
    vtxIds = OpenMaya.MIntArray()
    itVtx.getConnectedVertices( vtxIds )
    
    fnMesh = OpenMaya.MFnMesh( dagPath )
    vtxNames = []
    for i in range( vtxIds.length() ):
        vtxNames.append( fnMesh.name() + '.vtx[%d]' % vtxIds[i] )
    return vtxNames




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
    



def getChildrenShapeExists( targets, typ='shape' ):
    selChildren = cmds.listRelatives( targets, c=1, ad=1, typ='shape', f=1 )
    
    children = []
    for child in selChildren:
        childP = cmds.listRelatives( child, p=1, f=1 )[0]
        children.append( childP )
    return children




def getDotWeight( first, second, firstVector, secondVector ):
    
    pmFirst = pymel.core.ls( first )[0]
    pmSecond = pymel.core.ls( second )[0]
    
    compose = pymel.core.createNode( 'composeMatrix' )
    compose.it.set( firstVector )
    multMtx = pymel.core.createNode( 'multMatrix' )
    compose.outputMatrix >> multMtx.i[0]
    pmFirst.wm >> multMtx.i[1]
    pmSecond.wim >> multMtx.i[2]
    dcmp = pymel.core.createNode( 'decomposeMatrix' )
    multMtx.o >> dcmp.imat
    
    vectorNode = pymel.core.createNode( 'vectorProduct' )
    vectorNode.normalizeOutput.set( 1 )
    dcmp.ot >> vectorNode.input1
    vectorNode.input2.set( secondVector )
    pymel.core.select( vectorNode )
    return vectorNode.name()
    
    
    
    
    
def makeSameChildren( first, second ):
    
    pSecond = cmds.listRelatives( second, p=1, f=1 )[0]
    return cmds.parent( first, pSecond )[0]



def freezeJointJo( sel ):
    
    mtxValue = cmds.getAttr( sel + '.wm' )
    cmds.setAttr( sel + '.jo', 0,0,0 )
    cmds.xform( sel, ws=1, matrix= mtxValue  )



def scaleConnect( point1Obj, point2Obj, scaleTarget ):
    
    dcmp = pymel.core.ls( getLocalDecomposeMatrix( point1Obj, point2Obj ).name() )[0]
    distNode = pymel.core.createNode( 'distanceBetween' )
    cmds.connectAttr( dcmp)
    
    
    
def makePivParent( target ):
    
    targetP = cmds.listRelatives( target, p=1, f=1 )[0]
    pivParent = cmds.group( em=1, n='Piv' + target )
    
    if targetP:
        pivParent = cmds.parent( pivParent, targetP )[0]
        cmds.xform( pivParent, os=1, matrix= matrixToList( OpenMaya.MMatrix() ) )
    
    target = cmds.parent( target, pivParent )[0]
    return target, pivParent
    
        

def copySkinWeightCombineObj( *args ):
    
    skinObjs = args[:-1]
    target = args[-1]
    
    bindJoints = []
    
    for sel in skinObjs:
        skinNodes = getNodeFromHistory( sel, 'skinCluster' )
        
        if not skinNodes: continue
        joints = cmds.listConnections( skinNodes[0] + '.matrix' )
        
        bindJoints += joints
    
    print bindJoints
    print target
    
    cmds.skinCluster( bindJoints, target, tsb=1 )
    cmds.select( skinObjs, target )
    cmds.copySkinWeights( noMirror=True, surfaceAssociation='closestPoint', influenceAssociation ='oneToOne' )



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
    
    if cmds.attributeQuery( attrName, node=target, ex=1 ): return None
    
    cmds.addAttr( target, **options )
    
    if channelBox:
        cmds.setAttr( target+'.'+attrName, e=1, cb=1 )
    elif keyable:
        cmds.setAttr( target+'.'+attrName, e=1, k=1 )



def createSquashObject( distTarget, distBase, scaleTarget ):

    import math
    
    scaleTargetMtx = cmds.getAttr( scaleTarget+'.wm' )
    
    xVector = OpenMaya.MVector( *scaleTargetMtx[0:3] )
    yVector = OpenMaya.MVector( *scaleTargetMtx[4:4+3] )
    zVector = OpenMaya.MVector( *scaleTargetMtx[8:8+3] )
    
    targetPos = cmds.xform( distTarget, q=1, ws=1, t=1 )
    basePos   = cmds.xform( distBase, q=1, ws=1, t=1 )
    aimVector = OpenMaya.MVector( targetPos[0] - basePos[0], targetPos[1] - basePos[1], targetPos[2] - basePos[2] )
    
    vectors = [ xVector, yVector, zVector ]
    maxDotValue = 0
    aimIndex = 0
    for i in range( 3 ):
        dotValue = math.fabs( aimVector * vectors[i] )
        if dotValue > maxDotValue:
            maxDotValue = dotValue
            aimIndex = i

    otherIndex1 = ( aimIndex + 1 ) % 3
    otherIndex2 = ( aimIndex + 2 ) % 3
        
    mm = cmds.createNode( 'multMatrix' )
    dcmp = cmds.createNode( 'decomposeMatrix' )
    distNode = cmds.createNode( 'distanceBetween' )
    cmds.connectAttr( mm + '.o', dcmp + '.imat' )
    cmds.connectAttr( distTarget+'.wm', mm+'.i[0]' )
    cmds.connectAttr( distBase+'.wim', mm+'.i[1]' )
    cmds.connectAttr( dcmp + '.ot', distNode + '.point2' )
    
    addAttr( scaleTarget, ln='distanceDefault', k=1 )
    addAttr( scaleTarget, ln='distanceCurrent', cb=1 )
    addAttr( scaleTarget, ln='lengthRate', k=1 )
    addAttr( scaleTarget, ln='squashRate', k=1 )
    
    cmds.connectAttr( distNode+'.distance', scaleTarget+'.distanceCurrent', f=1 )
    cmds.setAttr( scaleTarget+'.distanceDefault', cmds.getAttr( distNode+'.distance' ) )
    
    divNode    = cmds.createNode( 'multiplyDivide' )
    squashNode = cmds.createNode( 'multiplyDivide' )
    cmds.setAttr( divNode+'.operation', 2 )
    cmds.setAttr( squashNode + '.operation', 3 )
    cmds.setAttr( squashNode + '.input2X', 0.5 )
    
    cmds.connectAttr( scaleTarget+'.distanceDefault', divNode+'.input2X' )
    cmds.connectAttr( scaleTarget+'.distanceCurrent', divNode+'.input1X' )
    cmds.connectAttr( divNode + '.outputX', squashNode + '.input1X' )
    
    axisChar = ['X', 'Y', 'Z' ]
    
    blendTwoAttrForLength = cmds.createNode( 'blendTwoAttr' )
    blendTwoAttrForSqush  = cmds.createNode( 'blendTwoAttr' )
    
    cmds.setAttr( blendTwoAttrForLength + '.input[0]', 1 )
    cmds.setAttr( blendTwoAttrForSqush + '.input[0]', 1 )
    cmds.connectAttr( squashNode+'.outputX', blendTwoAttrForSqush+'.input[1]' )
    cmds.connectAttr( divNode+'.outputX', blendTwoAttrForLength+'.input[1]' )
    
    cmds.connectAttr( blendTwoAttrForSqush+'.output', scaleTarget+'.scale%s' % axisChar[ otherIndex1 ] )
    cmds.connectAttr( blendTwoAttrForSqush+'.output', scaleTarget+'.scale%s' % axisChar[ otherIndex2 ] )
    cmds.connectAttr( blendTwoAttrForLength+'.output', scaleTarget+'.scale%s' % axisChar[ aimIndex ] )
    
    cmds.connectAttr( scaleTarget + '.lengthRate', blendTwoAttrForLength + '.ab' )
    cmds.connectAttr( scaleTarget + '.squashRate', blendTwoAttrForSqush + '.ab' )
    
    

def createFollicleOnSurface( surface, paramU=0.5, paramV=0.5 ):
    
    surfaceShape = surface
    if cmds.nodeType( surfaceShape ) == 'transform':
        surfaceShape = cmds.listRelatives( surfaceShape, s=1, f=1 )[0]
    
    follicleNode = cmds.createNode( 'follicle' )
    follicleTr = cmds.listRelatives( follicleNode, p=1, f=1 )[0]
    
    cmds.connectAttr( surface + '.worldMatrix', follicleNode + '.inputWorldMatrix' )
    cmds.connectAttr( surface + '.local', follicleNode + '.inputSurface' )
    
    compose = cmds.createNode( 'composeMatrix' )
    mm = cmds.createNode( 'multMatrix' )
    dcmp = cmds.createNode( 'decomposeMatrix' )
    
    cmds.connectAttr( follicleNode + '.outTranslate', compose + '.it' )
    cmds.connectAttr( follicleNode + '.outRotate', compose + '.ir' )
    cmds.connectAttr( compose + '.outputMatrix', mm + '.i[0]' )
    cmds.connectAttr( follicleTr + '.pim', mm + '.i[1]' )    
    cmds.connectAttr( mm + '.o', dcmp + '.imat' )
    cmds.connectAttr( dcmp + '.ot', follicleTr + '.t' )
    cmds.connectAttr( dcmp + '.or', follicleTr + '.r' )
    
    cmds.setAttr( follicleNode + '.parameterU', paramU )
    cmds.setAttr( follicleNode + '.parameterV', paramV )



def getClosestPointOnMesh( pointer_input, mesh_input ):
    
    pointer = pymel.core.ls( pointer_input )[0]
    mesh  = pymel.core.ls( mesh_input )[0]
    
    if mesh.type() == 'mesh':
        meshShape = mesh
    else:
        meshShape = mesh.getShape()
    
    closeNode = pymel.core.createNode( 'closestPointOnMesh' )
    
    meshShape.outMesh >> closeNode.inMesh
    meshShape.worldMatrix >> closeNode.inputMatrix
    
    worldPointDcmp = pymel.core.createNode( 'decomposeMatrix' )
    pointer.wm >> worldPointDcmp.imat
    
    worldPointDcmp.ot >> closeNode.inPosition
    
    composeNode = pymel.core.createNode( 'composeMatrix' )
    closeNode.position >> composeNode.inputTranslate
    mm = pymel.core.createNode( 'multMatrix' )
    dcmp = pymel.core.createNode( 'decomposeMatrix' )
    mm.o >> dcmp.imat
    
    composeNode.outputMatrix >> mm.i[0]
    newTr = pymel.core.createNode( 'transform' )
    newTr.dh.set( 1 )
    newTr.pim >> mm.i[1]    
    dcmp.ot >> newTr.t
    
    return newTr.name()
    
    
def makeSubCtl( inputCtl ):
    
    ctl = pymel.core.ls( inputCtl )[0]
    
    ctlP = ctl.getParent()
    duCtlP = pymel.core.duplicate( ctlP )[0]
    duCtl = duCtlP.listRelatives( c=1, f=1 )[0]
    
    ctl.rename( 'sub_' + ctl.nodeName() )
    
    keyAttrs = pymel.core.listAttr( duCtl, k=1 )
    keyAttrs += pymel.core.listAttr( duCtl, cb=1 )
    for attr in keyAttrs:
        duCtl.attr( attr ) >> ctl.attr( attr )
    
    keyAttrsP = pymel.core.listAttr( duCtlP, k=1 )
    keyAttrs += pymel.core.listAttr( duCtlP, cb=1 )
    for attr in keyAttrsP:
        ctlP.attr( attr ) >> duCtlP.attr( attr )
    
    pymel.core.parent( duCtlP, w=1 )
    
    return duCtlP.name()



    
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
    
   
    


def addMiddleTranslateJoint( targetJnt ):
    
    parentJnt = cmds.listRelatives( targetJnt, p=1, f=1 )[0]
    cmds.select( parentJnt )
    try:
        radiusValue = cmds.getAttr( parentJnt + '.radius' ) * 1.5
    except:
        radiusValue = 1
    
    newJnt = cmds.joint( radius = radiusValue )
    cmds.addAttr( newJnt, ln='transMult', dv=0.5 )
    cmds.setAttr( newJnt + '.transMult', e=1, k=1 )
    
    multNode = cmds.createNode( 'multiplyDivide' )
    cmds.connectAttr( targetJnt + '.t', multNode + '.input1' )
    cmds.connectAttr( newJnt + '.transMult', multNode + '.input2X' )
    cmds.connectAttr( newJnt + '.transMult', multNode + '.input2Y' )
    cmds.connectAttr( newJnt + '.transMult', multNode + '.input2Z' )
    cmds.connectAttr( multNode + '.output', newJnt + '.t' )
    return newJnt



def getFutureByType( nodeName, nodeType ):

    node = pymel.core.ls( nodeName )[0]
    
    destTargets = node.listConnections( s=0, d=1 )
    targets = []
    for destTarget in destTargets:
        futures = destTarget.listFuture()
        for future in futures:
            if future.type() == 'ikHandle':
                targets.append( (len( futures ),future ) )
    targets = sorted( targets, key= lambda target : target[0] )
    returnTargets = []
    for numConnection, connectedNode in targets:
        returnTargets.append( connectedNode.name() )
    return returnTargets



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



def setMatrixToGeoGroup( mtx, target ):
    
    tr = cmds.createNode( 'transform' )
    setMatrixToTarget( mtx, tr )
    selChildren = cmds.listRelatives( target, c=1, f=1, type='transform' )
    if not selChildren: selChildren = []
    selChildren.append( target )
    unParentList = []
    for selChild in selChildren:
        if cmds.listRelatives( selChild, s=1 ):
            selP = cmds.listRelatives( selChild, p=1, f=1 )[0]
            selChild = cmds.parent( selChild, w=1 )[0]
            setGeometryMatrixToTarget( selChild, tr )
            unParentList.append( [selChild,selP] )
        else:
            setMatrixToTarget( mtx, selChild )
    for child, parent in unParentList:
        cmds.parent( child, parent )
    
    cmds.delete( tr )
    

def getAutoTwistNode( inputTarget, **options ):

    axis = [1,0,0]
    if options.has_key( 'axis' ):
        axis = options['axis']

    target = pymel.core.ls( inputTarget )[0]
    composeAxis = pymel.core.createNode( 'composeMatrix' )
    composeRot = pymel.core.createNode( 'composeMatrix' )
    composeAxis.it.set( axis )
    target.r >> composeRot.ir
    multRotMtx = pymel.core.createNode( 'multMatrix' )
    composeAxis.outputMatrix >> multRotMtx.i[0]
    composeRot.outputMatrix >> multRotMtx.i[1]
    dcmpRotMtx = pymel.core.createNode( 'decomposeMatrix' )
    multRotMtx.matrixSum >> dcmpRotMtx.imat
    angleNode = pymel.core.createNode( 'angleBetween' )
    angleNode.vector1.set( axis )
    dcmpRotMtx.ot >> angleNode.vector2
    composeAngle = pymel.core.createNode( 'composeMatrix' )
    invAngle = pymel.core.createNode( 'inverseMatrix' )
    multInvAngle = pymel.core.createNode( 'multMatrix' )
    angleNode.euler >> composeAngle.ir
    composeAngle.outputMatrix >> invAngle.inputMatrix
    composeRot.outputMatrix >> multInvAngle.i[0]
    invAngle.outputMatrix >> multInvAngle.i[1]
    composeDefault = pymel.core.createNode( 'composeMatrix' )
    wtAddMtx = pymel.core.createNode( 'wtAddMatrix' )
    composeDefault.outputMatrix >> wtAddMtx.i[0].m
    multInvAngle.matrixSum >> wtAddMtx.i[1].m
    wtAddMtx.addAttr( 'blend', min=0, max=1, dv=0, k=1 )
    wtAddMtx.blend >> wtAddMtx.i[1].w
    reverseWeight = pymel.core.createNode( 'reverse' )
    wtAddMtx.blend >> reverseWeight.inputX
    reverseWeight.outputX >> wtAddMtx.i[0].w
    return wtAddMtx.name()
    
    
    
    
    
    
def connectBindPreMatrix( joint, bindPreObj, targetMesh ):
    
    skinNodes = getNodeFromHistory( targetMesh, 'skinCluster' )
    
    if not skinNodes: return None
    
    cons = cmds.listConnections( joint+'.wm', type='skinCluster', p=1, c=1 )
    
    for con in cons[1::2]:
        skinCluster = con.split( '.' )[0]
        if skinCluster != skinNodes[0]: continue
        
        index = int( con.split( '[' )[-1].replace( ']', '' ) )
        if not cmds.isConnected( bindPreObj+'.wim', skinCluster+'.bindPreMatrix[%d]' % index ):
            cmds.connectAttr( bindPreObj+'.wim', skinCluster+'.bindPreMatrix[%d]' % index, f=1 )
    
    



def addMiddleJoint( jnt ):
    
    jntC = cmds.listRelatives( jnt, c=1, f=1 )[0]
    middleTransJnt = addMiddleTranslateJoint( jntC )
    cmds.setAttr( middleTransJnt + '.transMult', 0.05 )
    
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
    return middleTransJnt
    
    
    
    
class SymmetryControl_:
    
    parentAttr    = 'ctlParent'
    otherSideAttr = 'ctlOtherSide'
    reverseAttrsAttr = 'ctlReverseAttrs'
    mirrorTypeAttr   = 'ctlMirrorType'
    

    def __init__(self, name ):
        self.__namespace = ''
        self.__name = name
        self.__origname = name
        if self.__name.find( ':' ) != -1:
            self.__namespace = ':'.join( name.split( ':' )[:-1] ) + ':'
            self.__origname = name.split( ':' )[-1]
        self.sgtransform = pymel.core.ls( self.__name )[0]

    
    def fullName(self, origName ):
        return self.__namespace + origName


    def parent(self):
        if not cmds.attributeQuery( SymmetryControl.parentAttr, node=self.__name, ex=1 ): return None
        return [ target.strip() for target in cmds.getAttr( self.__name + '.'+ SymmetryControl.parentAttr ).split( ',' ) ]
    
    
    def side(self):
        if self.__name.find( '_L_' ) != -1: return 'left'
        if self.__name.find( '_R_' ) != -1: return 'right'
        return 'center'

    
    def otherSide(self):
        if not cmds.attributeQuery( SymmetryControl.otherSideAttr, node= self.__name, ex=1 ): return self
        if not cmds.getAttr( self.__name + '.' + SymmetryControl.otherSideAttr ): return self
        return SymmetryControl( self.__namespace + cmds.getAttr( self.__name + '.'+ SymmetryControl.otherSideAttr ) )


    def mirrorType(self):
        if not cmds.attributeQuery( SymmetryControl.mirrorTypeAttr, node= self.__name, ex=1 ): return []
        mirrorType = cmds.getAttr( self.__name + '.' + SymmetryControl.mirrorTypeAttr )
        return [ i.strip() for i in mirrorType.split( ',' ) ]


    def name(self):
        return self.__name


    def setMatrixByMirrorType( self, mirrorTypes, srcLocalMtx ):
        attrs  = ['tx', 'ty', 'tz','rx', 'ry', 'rz']
        revs = [1,1,1,1,1,1]
        values = [0,0,0,0,0,0]
        for mirrorType in mirrorTypes[1:]:
            for attr in attrs:
                mirrorAttr, rev, value= mirrorType.split( '_' )
                if mirrorAttr != attr: continue
                if rev == 'r': revs[ attrs.index( attr ) ] *= -1
                values[ attrs.index( attr ) ] = float( value )

        trans = getTranslateFromMatrix( srcLocalMtx )
        rots  = getRotateFromMatrix( srcLocalMtx )
        trans[0] *= revs[0]
        trans[1] *= revs[1]
        trans[2] *= revs[2]
        rots[0] *= revs[3]
        rots[1] *= revs[4]
        rots[2] *= revs[5]
        srcLocalMtx = setMatrixTranslate( srcLocalMtx, trans[0], trans[1], trans[2] )
        srcLocalMtx = setMatrixRotate( srcLocalMtx, rots[0], rots[1], rots[2] )
        transAddValues = values[:3]
        rotAddValues   = values[3:]
        rotMtxInside = getMatrixFromRotate( rotAddValues )
        transMtxOutside = getMatrixFromTranslate( transAddValues )
        srcLocalMtx = rotMtxInside * srcLocalMtx * transMtxOutside
        return srcLocalMtx


    def getCtlData(self, source ):
        
        sourceParent = source.parent()
        if not source.parent(): return None
        
        udAttrs = cmds.listAttr( source.__name, k=1, ud=1 )
        if not udAttrs: udAttrs = []
        udAttrValues = []
        if cmds.attributeQuery( SymmetryControl.reverseAttrsAttr, node= source.__name, ex=1 ):
            reverseAttrs = [ i.strip() for i in cmds.getAttr( source.__name + '.' + SymmetryControl.reverseAttrsAttr ).split( ',' ) ]
        else:
            reverseAttrs= []
        for attr in udAttrs:
            if attr in reverseAttrs:
                udAttrValues.append( -cmds.getAttr( source.__name + '.' + attr ) )
            else:
                udAttrValues.append(  cmds.getAttr( source.__name + '.' + attr ) )

        transformAttrs = ['tx','ty','tz','rx','ry','rz','sx','sy','sz']
        transformAttrValues = []
        for attr in transformAttrs:
            transformAttrValues.append( cmds.getAttr( source.__name + '.' + attr ) )
        worldMatrix = listToMatrix( cmds.getAttr( source.__name + '.wm' ) )
        pivMatrix   = getPivotMatrix( sourceParent[0] ) * listToMatrix( cmds.getAttr( sourceParent[0] + '.wm' ) )
        return udAttrs, udAttrValues, transformAttrs, transformAttrValues, worldMatrix * pivMatrix.inverse()
    
    
    def setCtlData( self, source, target, ctlData, typ='mirror' ):

        if not ctlData: return None

        mirrorTypes = source.mirrorType()
        udAttrs, udAttrValues, transformAttrs, transformValues, localMatrix = ctlData
        
        trg = target.sgtransform
        for i in range( len( udAttrs ) ):
            try:
                trg.attr( udAttrs[i] ).set( udAttrValues[i] )
            except:pass
        for i in range( len( transformAttrs ) ):
            try:trg.attr( transformAttrs[i] ).set( transformValues[i] )
            except:pass
        
        if 'none' in mirrorTypes: return None

        if 'local' in mirrorTypes:
            trg.tx.set( -trg.tx.get() )
            trg.ty.set( -trg.ty.get() )
            trg.tz.set( -trg.tz.get() )
            
            attrs  = ['tx', 'ty', 'tz','rx', 'ry', 'rz']
            revs = [1,1,1,1,1,1]
            values = [0,0,0,0,0,0]
            for mirrorType in mirrorTypes[1:]:
                for attr in attrs:
                    mirrorAttr, rev, value= mirrorType.split( '_' )
                    if mirrorAttr != attr: continue
                    if rev == 'r': revs[ attrs.index( attr ) ] *= -1
                    values[ attrs.index( attr ) ] = float( value )
            trg.tx.set( revs[0]*trg.tx.get() )
            trg.ty.set( revs[1]*trg.ty.get() )
            trg.tz.set( revs[2]*trg.tz.get() )
            print '%s - revs : ' % source.name(), revs
        
        if 'txm' in mirrorTypes:
            trg.tx.set( -trg.tx.get() )
        if 'tym' in mirrorTypes:
            trg.ty.set( -trg.ty.get() )
        if 'tzm' in mirrorTypes:
            trg.tz.set( -trg.tz.get() )
        if 'rxm' in mirrorTypes:
            trg.rx.set( -trg.rx.get() )
        if 'rym' in mirrorTypes:
            trg.ry.set( -trg.ry.get() )
        if 'rzm' in mirrorTypes:
            trg.rz.set( -trg.rz.get() )

        if 'matrix' in mirrorTypes:
            srcLocalMtx = getMirrorMatrix( localMatrix )
            dstMatrix = srcLocalMtx * getPivotMatrix( target.parent()[0] ) * listToMatrix( cmds.getAttr( target.parent()[0] + '.wm' ) )
            
            tr = cmds.createNode( 'transform' )
            cmds.setAttr( tr + '.dh', 1 )
            cmds.xform( tr, ws=1, matrix= matrixToList( dstMatrix ) )
            
            cmds.xform( target.name(), ws=1, t=getTranslateFromMatrix(dstMatrix) )
            rotList = getRotateFromMatrix( dstMatrix )
            cmds.xform( target.name(), ws=1, ro= rotList )

        if 'center' in mirrorTypes:
            if typ == 'flip':
                setMirrorLocal( target.sgtransform )
            elif typ == 'mirror':
                setCenterMirrorLocal( target.sgtransform )
        
    
    def isMirrorAble(self):
        
        if not cmds.attributeQuery( SymmetryControl.mirrorTypeAttr, node=self.__name, ex=1 ): return False
        mirrorTypes = cmds.getAttr( self.__name + '.' + SymmetryControl.mirrorTypeAttr )
        if not mirrorTypes: return False
        if mirrorTypes == 'none': return False
        return True
    
    

    def setMirror(self, side ):
        
        if not self.isMirrorAble(): return None
        
        if side == 'LtoR':
            if self.side() == 'left':
                source = self
                target = self.otherSide()
            else:
                source = self.otherSide()
                target = self
                
        if side == 'RtoL':
            if self.side() == 'right':
                source = self
                target = self.otherSide()
            else:
                source = self.otherSide()
                target = self
        
        self.setCtlData( source, target, self.getCtlData( source ), 'mirror' )
    
    
    def setFlip(self):

        if not self.isMirrorAble(): return None

        source = self
        target = self.otherSide()
        dataSource = self.getCtlData( source )
        dataTarget = self.getCtlData( target )
        
        self.setCtlData( source, target, dataSource, 'flip' )
        self.setCtlData( target, source, dataTarget, 'flip' )
    


    def flipH(self):
        
        if not self.isMirrorAble(): return None
        
        H = self.allChildren()
    
        flipedList = []
        sourceList = []
        targetList = []
        sourceDataList = []
        targetDataList = []
        
        for h in H:
            
            if h.name() in flipedList: continue
            name = h.otherSide().name()
            if name in flipedList: continue
            flipedList.append( h.name() )
            
            print "flip target : ", h.name()
            
            otherSide = h.otherSide()
            sourceList.append( h )
            targetList.append( otherSide )
            sourceDataList.append( self.getCtlData( h ) )
            targetDataList.append( self.getCtlData( otherSide ) )
        
        for i in range( len( sourceList ) ):
            self.setCtlData( sourceList[i], targetList[i], sourceDataList[i], 'flip' )
            self.setCtlData( targetList[i], sourceList[i], targetDataList[i], 'flip' )



    def mirrorH(self, side ):
        
        if not self.isMirrorAble(): return None
        
        if side == 'LtoR':
            if self.side() == 'left':
                source = self
            else:
                source = self.otherSide()
                
        if side == 'RtoL':
            if self.side() == 'right':
                source = self
            else:
                source = self.otherSide()
        
        H = source.allChildren()
    
        sourceList = []
        targetList = []
        sourceDatas = []

        for h in H:
            if side == 'LtoR' and h.side() == 'right': continue
            if side == 'RtoL' and h.side() == 'left' : continue
            
            otherSide = h.otherSide()
            sourceList.append( h )
            targetList.append( otherSide )
            sourceDatas.append( self.getCtlData( h ) )
        
        for i in range( len( sourceList ) ):
            self.setCtlData( sourceList[i], targetList[i], sourceDatas[i], 'mirror' )
        


    def children(self):
        
        allAttrs = cmds.ls( '*.' + SymmetryControl.parentAttr )
        
        targetChildren = []
        for attr in allAttrs:
            if attr.find( self.__namespace ) == -1: continue
            targetParent = cmds.getAttr( attr )
            if self.__name == self.__namespace + targetParent:
                targetChildren.append( SymmetryControl( attr.split( '.' )[0] ) )
        return targetChildren


    def allChildren(self):
        
        localChildren = self.children()
        childrenH = []
        for localChild in localChildren:
            childrenH += localChild.allChildren()
        localChildren += childrenH
        childrenNames = []

        localChildrenSet = []
        for localChild in localChildren:
            name = localChild.name()
            if name in childrenNames: continue
            childrenNames.append( name )
            localChildrenSet.append( localChild )
        
        return localChildrenSet
    
    
    def hierarchy(self):
        
        localChildren = [self]
        localChildren += self.allChildren()
        return localChildren
    

    def setDefault(self):

        attrs = self.sgtransform.listAttr( k=1 )
        for attr in attrs:
            if attr in self.dataPtr.defaultIgnore: continue
            try:self.sgtransform.attr(attr).setToDefault()
            except:pass



def getMeshGroups( meshs ):
    
    def getCompairData( meshName ):
        oMesh = OpenMaya.MObject()
        selList = OpenMaya.MSelectionList()
        selList.add( meshName )
        selList.getDependNode( 0, oMesh )
        fnMesh = OpenMaya.MFnMesh( oMesh )
        numVtx = fnMesh.numVertices()
        numEdge = fnMesh.numEdges()
        numPoly = fnMesh.numPolygons()
        startPoint = OpenMaya.MPoint()
        endPoint = OpenMaya.MPoint()
        fnMesh.getPoint(0, startPoint)
        fnMesh.getPoint(numVtx-1, endPoint)
        return numVtx, numEdge, numPoly, startPoint, endPoint
    
    compairDatas = []
    
    for mesh in meshs:
        if cmds.listConnections( mesh + '.inMesh', s=1, d=0 ): continue
        compairDatas.append( getCompairData( mesh ) )
    
    meshGroups = []
    for i in range( len( compairDatas ) ):
        compairSrc = compairDatas[i]
        srcExists = False
        for meshGroup in meshGroups:
            if i in meshGroup:
                srcExists = True
                break
        if srcExists: continue
        meshGroups.append( [i] )
        
        for j in range( i+1, len( compairDatas ) ):
            compairTrg = compairDatas[j]
            if compairSrc[0] != compairTrg[0]: continue
            if compairSrc[1] != compairTrg[1]: continue
            if compairSrc[2] != compairTrg[2]: continue
            if compairSrc[3].distanceTo( compairTrg[3] ) > 0.001: continue
            if compairSrc[4].distanceTo( compairTrg[4] ) > 0.001: continue
            
            for meshGroup in meshGroups:
                if i in meshGroup:
                    meshGroup.append( j )
                    break
    return meshGroups



def createDefaultPropRig( propGrp ):
    
    from sgModules import sgdata
    from sgModules import sgcommands
    
    propGrp = pymel.core.ls( propGrp )[0]
    
    def makeParent( target ):
        targetP = pymel.core.createNode( 'transform' )
        pymel.core.xform( targetP, ws=1, matrix= target.wm.get() )
        pymel.core.parent( target, targetP )
        targetP.rename( 'P' + target.shortName() )
        return targetP
    
    worldCtl = pymel.core.ls( makeController( sgdata.Controllers.circlePoints ).name() )[0]
    moveCtl  = pymel.core.ls( makeController( sgdata.Controllers.crossPoints ).name() )[0]
    rootCtl  = pymel.core.ls( makeController( sgdata.Controllers.circlePoints ).name() )[0]
    
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
    
    rootCtl.rename( 'Ctl_%s_Root' % propGrp.name() )
    moveCtl.rename( 'Ctl_%s_Move' % propGrp.name() )
    worldCtl.rename( 'Ctl_%s_World' % propGrp.name() )
    
    pRootCtl = makeParent( rootCtl )
    pMoveCtl = makeParent( moveCtl )
    pWorldCtl = makeParent( worldCtl )
    
    pymel.core.parent( pRootCtl, moveCtl )
    pymel.core.parent( pMoveCtl, worldCtl )

    sgcommands.setMatrixToGeoGroup( rootCtl.wm.get(), propGrp.name() )
    sgcommands.constrain_all( rootCtl, propGrp )

