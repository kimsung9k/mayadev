import pymel.core

def addAttr( target, **options ):
    
    import pymel.core
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


def separateParentConnection( inputNode, attrName ):
    
    import pymel.core
    node = pymel.core.ls( inputNode )[0]
    node = node.name()
    
    parentAttr = pymel.core.attributeQuery( attrName, node=node, listParent=1 )
    
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


def getDirectionIndex( inputVector ):
    
    import math
    import pymel.core
    from maya import OpenMaya
    
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


def createLocalMatrix( matrixAttr, inverseMatrixAttr ):
    matrixAttr = pymel.core.ls( matrixAttr )[0]
    inverseMatrixAttr = pymel.core.ls( inverseMatrixAttr )[0]
    multMatrixNode = pymel.core.createNode( 'multMatrix' )
    matrixAttr >> multMatrixNode.i[0]
    inverseMatrixAttr >> multMatrixNode.i[1]
    return multMatrixNode


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


sels = pymel.core.ls( sl=1 )

ikCtl = sels[0]
ikJnt = sels[1]

ikMiddleJnt = ikJnt.listRelatives( c=1, type='joint' )[0]
ikEndJnt = ikMiddleJnt.listRelatives( c=1, type='joint' )[0]

addAttr( ikCtl, ln='stretch', k=1, min=0, max=1 )
#localDcmp = getDecomposeMatrix( getLocalMatrix( ikCtl, ikJnt ) )
addOrigDistance = pymel.core.createNode( 'addDoubleLinear' )
jnts = [ikMiddleJnt, ikEndJnt]
origInputAttrs = [ addOrigDistance.input1, addOrigDistance.input2 ]

for i in range( 2 ):
    jnt = jnts[i]
    origInputAttr = origInputAttrs[i]
    dirIndex = getDirectionIndex( jnt.t.get() )%3
    targetAttr = ['tx', 'ty', 'tz'][dirIndex]

    if jnt.t.listConnections( s=1, d=0 ):
        separateParentConnection( targetAttr )
    
    cons = jnt.attr( targetAttr ).listConnections( s=1, d=0, p=1 )
    absNode = pymel.core.createNode( 'multDoubleLinear' )
    if cons:
        cons[0] >> absNode.input1
    else:
        absNode.input1.set( jnt.attr( targetAttr ).get() )
    
    if jnt.attr( targetAttr ).get() < 0:
        absNode.input2.set( -1 )
    else:
        absNode.input2.set( 1 )
    absNode.output >> origInputAttr

multOrigDist = pymel.core.createNode( 'multDoubleLinear' )
addOrigDistance.output >> multOrigDist.input1
multOrigDist.input2.set( 0.9999 )

composeMatrix = pymel.core.createNode( 'composeMatrix' )
cons = ikJnt.t.listConnections( s=1, d=0, p=1 )
if cons:
    cons[0] >> composeMatrix.it
else:
    composeMatrix.it.set( ikJnt.t.get() )
localMtx = getLocalMatrix( ikCtl.wm, ikJnt.pim )
distNode = pymel.core.createNode( 'distanceBetween' )
composeMatrix.outputMatrix >> distNode.inMatrix1
localMtx.matrixSum >> distNode.inMatrix2

scaleOfStretch = pymel.core.createNode( 'multiplyDivide' )
scaleOfStretch.op.set( 2 )

distNode.distance >> scaleOfStretch.input1X
multOrigDist.output >> scaleOfStretch.input2X

conditionNode = pymel.core.createNode( 'condition' )
conditionNode.op.set( 2 )
conditionNode.secondTerm.set( 1 )
scaleOfStretch.outputX >> conditionNode.firstTerm
scaleOfStretch.outputX >> conditionNode.colorIfTrueR
conditionNode.colorIfFalseR.set( 1 )

blendStretch = pymel.core.createNode( 'blendTwoAttr' )
blendStretch.input[0].set( 1 )
conditionNode.outColorR >> blendStretch.input[1]

ikCtl.attr( 'stretch' ) >> blendStretch.ab

for i in range( 2 ):
    multStretch = pymel.core.createNode( 'multDoubleLinear' )
    
    jnt = jnts[i]
    origInputAttr = origInputAttrs[i]
    dirIndex = getDirectionIndex( jnt.t.get() )%3
    targetAttr = ['tx', 'ty', 'tz'][dirIndex]
    
    cons = jnt.attr( targetAttr ).listConnections( s=1, d=0, p=1 )
    if not cons:
        multStretch.input1.set( jnt.attr( targetAttr ).get() )
    else:
        cons[0] >> multStretch.input1
    
    blendStretch.output >> multStretch.input2
    multStretch.output >> jnt.attr( targetAttr )

