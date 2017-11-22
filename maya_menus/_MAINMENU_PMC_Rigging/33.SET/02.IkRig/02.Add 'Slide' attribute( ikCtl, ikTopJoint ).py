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


sels = pymel.core.ls( sl=1 )

ikCtl = sels[0]
ikJnt = sels[1]

ikMiddleJnt = ikJnt.listRelatives( c=1, type='joint' )[0]
ikEndJnt = ikMiddleJnt.listRelatives( c=1, type='joint' )[0]

addAttr( ikCtl, ln='slide', k=1 )

jnts = [ikMiddleJnt,ikEndJnt]
multList = [1,-1]

for i in range( 2 ):
    jnt = jnts[i]
    multValue = multList[i]    
    dirIndex = getDirectionIndex( jnt.t.get() ) % 3
    targetAttr = ['tx', 'ty', 'tz'][dirIndex]
    
    if jnt.t.listConnections( s=1, d=0 ):
        separateParentConnection( jnt, targetAttr )
    
    powerNode = pymel.core.createNode( 'multiplyDivide' )
    multNode = pymel.core.createNode( 'multDoubleLinear' )
    multReverse = pymel.core.createNode( 'multDoubleLinear' )
    powerNode.op.set( 3 )
    powerNode.input1X.set( 2 )
    ikCtl.attr( 'slide' ) >> multReverse.input1
    multReverse.input2.set( multValue )
    multReverse.output >> powerNode.input2X
    powerNode.outputX >> multNode.input2
    
    srcCon = jnt.attr( targetAttr ).listConnections( s=1, d=0, p=1 )
    if srcCon:
        srcCon[0] >> multNode.input1
    else:
        multNode.input1.set( jnt.attr( targetAttr ).get() )
    
    multNode.output >> jnt.attr( targetAttr )