import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import get
import node
import dag
import convert
import value
from sgModules import sgobject
import attribute
from sgModules import sgcommands
from sgModules import sgbase




def connectAttr( firstAttr, secondAttr, **options ):
    if cmds.isConnected( firstAttr, secondAttr ): return None
    cmds.connectAttr( firstAttr, secondAttr, **options )




def attrToAttr( firstAttr, secondAttr ):
    cmds.connectAttr( firstAttr, secondAttr, f=1 )




def outMeshToInMesh( firstObj, targetObj, evt=0 ):
    
    outTargets = dag.getNoneIoMesh( firstObj )
    inTargets  = dag.getNoneIoMesh( targetObj )
    
    if not len(outTargets): return;
    if not len(inTargets): return;
    
    cmds.connectAttr( outTargets[0] +'.outMesh', inTargets[0]+'.inMesh', f=1 )



def createDcmp( node ):
    
    dcmp = cmds.createNode( 'decomposeMatrix' )
    cmds.connectAttr( node+'.o', dcmp+'.imat' )
    return dcmp  



def getDcmp( node ):
    
    if type( node ) in [ str, unicode ]:
        nodeType = cmds.nodeType( node )
        if nodeType in ['transform','joint'] :
            targetAttr = node + '.wm'
        else:
            targetAttr = node + '.o'
        
        cons = cmds.listConnections( targetAttr, s=0, d=1 )
        if cons:
            for con in cons:
                if not cmds.nodeType( con ) == 'decomposeMatrix': continue
                return con
        
        dcmp = cmds.createNode( 'decomposeMatrix' )
        cmds.connectAttr( targetAttr, dcmp+'.imat' )
        return dcmp
    
    elif isinstance( node, sgobject.SGNode ):
        if node.nodeType() in ['transform', 'joint']:
            targetAttr = node.attr( 'wm' )
        else:
            targetAttr = node.attr( 'o' )
        
        cons = sgcommands.listConnections( targetAttr, s=0, d=1 )
        if cons:
            for con in cons:
                if con.nodeType() != 'decomposeMatrix': continue
                return con
        dcmp = sgcommands.createNode( 'decomposeMatrix' )
        targetAttr >> dcmp.attr( 'imat' )
        return dcmp



def createLocalMatrix( target, targetP ):
    
    mm = cmds.createNode( 'multMatrix' )
    mtxAttr = attribute.getOutputMatrixAttributeFromNode( target )
    mtxInvAttr = attribute.getOutputMatrixInvAttributeFromNode( targetP )
    cmds.connectAttr( mtxAttr, mm + '.i[0]' )
    cmds.connectAttr( mtxInvAttr, mm+ '.i[1]' )
    return mm



def getLocalMatrix( target, targetP ):

    mtxAttr     = attribute.getOutputMatrixAttributeFromNode( target )
    mtxInvAttr  = attribute.getOutputMatrixInvAttributeFromNode( targetP )
    consFirst = cmds.listConnections( mtxAttr, type='multMatrix', p=1 )
    consSecond = cmds.listConnections( mtxInvAttr, type='multMatrix', p=1 )
    
    if consFirst and consSecond:
        for i in range( len( consFirst ) ):
            conFirst = consFirst[i]
            firstNode,  firstAttr  = conFirst.split( '.' )
            if firstAttr != 'matrixIn[0]': continue
            for j in range( len( consSecond ) ):
                conSecond = consSecond[j]
                secondNode, secondAttr = conSecond.split( '.' )
                if firstNode != secondNode: continue
                if secondAttr != 'matrixIn[1]': continue
                cmds.select( firstNode )
                return firstNode
    
    localMtx = createLocalMatrix( target, targetP )
    cmds.select( localMtx )
    return localMtx



def createLocalDcmp( target, targetP, evt=0 ):
    
    mm = createLocalMatrix( target, targetP )
    return createDcmp( mm )




def getLocalDcmp( target, targetP ):
    
    mm = getLocalMatrix( target, targetP )
    dcmp = getDcmp( mm )
    cmds.select( dcmp )
    return dcmp



def getConstraintDcmp( first, second, mo=0 ):
    
    import math
    mm = cmds.createNode( 'multMatrix' )
    dcmp = getDcmp( mm )
    
    if mo:
        mtxCompose = cmds.createNode( 'composeMatrix' )
        mtxSecond = convert.listToMatrix( cmds.getAttr( second + '.wm' ) )
        mtxFirst = convert.listToMatrix( cmds.getAttr( first + '.wm' ) )
        mtxLocal = mtxSecond * mtxFirst.inverse()
        mtxTr = OpenMaya.MTransformationMatrix( mtxLocal )
        trans = mtxTr.getTranslation( OpenMaya.MSpace.kTransform )
        rot = mtxTr.eulerRotation().asVector()
        rot = OpenMaya.MVector( math.degrees( rot.x ), math.degrees( rot.y ), math.degrees( rot.z ) )
        cmds.setAttr( mtxCompose + '.it', trans.x, trans.y, trans.z )
        cmds.setAttr( mtxCompose + '.ir', rot.x, rot.y, rot.z )
        cmds.connectAttr( mtxCompose + '.outputMatrix', mm + '.i[0]' )
        cmds.connectAttr( first + '.wm', mm + '.i[1]' )
        cmds.connectAttr( second + '.pim', mm + '.i[2]' )
    else:
        cmds.connectAttr( first + '.wm', mm + '.i[0]' )
        cmds.connectAttr( second + '.pim', mm + '.i[1]' )
    
    return dcmp



def getAnimCurveValueAtFloatInput( animCurveNode, inputFloat ):
    
    import maya.OpenMayaAnim as OpenMayaAnim
    
    oAnimCurve = sgbase.getMObject( animCurveNode )
    fnAnim = OpenMayaAnim.MFnAnimCurve( oAnimCurve )
    doublePtr2 = sgbase.getDoublePtr()
    fnAnim.evaluate( inputFloat, doublePtr2 )
    
    return sgbase.getDoubleFromDoublePtr( doublePtr2 )






def createLookAtDcmp( first, second ):
    
    mm = cmds.createNode( 'multMatrix' )
    cmds.connectAttr( first + '.wm', mm + '.i[0]' )
    cmds.connectAttr( second + '.pim', mm + '.i[1]' )
    return getDcmp( mm )



def getLookAtDcmp( first, second, evt=0 ):
    
    consFirst = cmds.listConnections( first + '.wm', type='multMatrix', p=1 )
    consSecond = cmds.listConnections( second + '.pim', type='multMatrix', p=1 )
    
    dcmp = ''
    if consFirst and consSecond:
        for i in range( len( consFirst ) ):
            conFirst = consFirst[i]
            firstNode,  firstAttr  = conFirst.split( '.' )
            if firstAttr != 'matrixIn[0]': continue
            for j in range( len( consSecond ) ):
                conSecond = consSecond[j]
                secondNode, secondAttr = conSecond.split( '.' )
                if firstNode != secondNode: continue
                if secondAttr != 'matrixIn[1]': continue
                dcmps  = cmds.listConnections( firstNode + '.o', type='decomposeMatrix' )
                if dcmps: dcmp = dcmps[0]
    if not dcmp:
        dcmp = createLookAtDcmp( first, second )
    
    cmds.select( dcmp )
    return dcmp




def getLocalDcmpDistance( first, second, evt=0 ):
    
    dcmp = getLocalDcmp( first, second )
    
    distNodes = cmds.listConnections( dcmp + '.ot', type='distanceBetween' )
    
    if not distNodes:
        distNode = cmds.createNode( 'distanceBetween' )
        cmds.connectAttr( dcmp + '.ot', distNode + '.point2' )
    else:
        distNode = distNodes[0]
    
    cmds.select( distNode )
    
    return distNode




def getLookAtConnectNode( lookTarget, rotTarget, evt=0 ):
    
    lookPoint = OpenMaya.MPoint( *cmds.xform( lookTarget, q=1, ws=1, t=1 ) )
    
    rotTargetPos = cmds.xform( rotTarget, q=1, ws=1, t=1 )
    rotPoint = OpenMaya.MPoint( *rotTargetPos )
    
    lookVector = lookPoint - rotPoint
    rotMtx = convert.listToMatrix( cmds.getAttr( rotTarget + '.wm' ) )
    maxDotValue, maxDotIndex = value.maxDotIndexAndValue( lookVector, rotMtx )
    
    baseDir = [[1,0,0], [0,1,0], [0,0,1]][maxDotIndex]
    if maxDotValue < 0:
        baseDir = [ i*-1 for i in baseDir ]
    
    dcmp = getLookAtDcmp( lookTarget, rotTarget )
    
    abnodes = cmds.listConnections( dcmp + '.ot', type='angleBetween' )
    if not abnodes:
        node = cmds.createNode( 'angleBetween' )
        cmds.setAttr( node + '.v1', *baseDir )
        cmds.connectAttr( dcmp +'.ot', node + '.v2' )
    else:
        node = abnodes[0]
    
    cmds.select( node )
    
    return node





def createLocalHalfMatrixNode( target ):
    
    composeMatrix = cmds.createNode( 'composeMatrix' )
    wtAddMtx = cmds.createNode( 'wtAddMatrix' )
    revNode  = cmds.createNode( 'reverse' )
    
    attribute.addAttr( wtAddMtx, ln='blend', min=0, max=1, dv=0.5, k=1 )
    
    cmds.connectAttr( composeMatrix + '.outputMatrix', wtAddMtx + '.i[0].m' )
    cmds.connectAttr( target + '.m', wtAddMtx + '.i[1].m' )
    cmds.connectAttr( wtAddMtx + '.blend', revNode + '.inputX' )
    cmds.connectAttr( wtAddMtx + '.blend', wtAddMtx + '.i[0].w' )
    cmds.connectAttr( revNode + '.outputX', wtAddMtx + '.i[1].w' )

    return wtAddMtx



def getLocalHalfMatrixNode( target ):
    
    cons = cmds.listConnections( target + '.m', s=0, d=1, c=1 )
    if cons :
        for con in cons:
            if cmds.nodeType( con ) != 'wtAddMatrix': continue
            if not cmds.attributeQuery( 'blend', node=con, ex=1 ): continue
            return con

    return createLocalHalfMatrixNode( target )




def getBlendTwoMatrixNode( first, second, target=None, local = False ):
    
    wtAddMtx = cmds.createNode( 'wtAddMatrix' )
    revNode  = cmds.createNode( 'reverse' )
    
    firstAttr = first + '.wm'
    secondAttr = second + '.wm'
    
    if local:
        firstAttr = first + '.m'
        secondAttr = second + '.m'
    
    if cmds.nodeType( first ) == 'multMatrix':
        firstAttr = first + '.o'
    if cmds.nodeType( second ) == 'multMatrix':
        secondAttr = second + '.o'

    cmds.connectAttr( firstAttr, wtAddMtx + '.i[0].m' )
    cmds.connectAttr( secondAttr, wtAddMtx + '.i[1].m' )
    
    if target:
        attribute.addAttr( target, ln='blend', min=0, max=1, dv=0.5, k=1 )
        cmds.connectAttr( target + '.blend', revNode + '.inputX' )
        cmds.connectAttr( target + '.blend', wtAddMtx + '.i[1].w' )
        multMtx  = cmds.createNode( 'multMatrix' )
        cmds.connectAttr( target + '.pim', multMtx + '.i[1]' )
        cmds.connectAttr( revNode + '.outputX', wtAddMtx + '.i[0].w' )
        cmds.connectAttr( wtAddMtx + '.o', multMtx + '.i[0]' )
        return multMtx
    else:
        attribute.addAttr( wtAddMtx, ln='blend', min=0, max=1, dv=0.5, k=1 )
        cmds.connectAttr( wtAddMtx + '.blend', revNode + '.inputX' )
        cmds.connectAttr( revNode + '.outputX', wtAddMtx + '.i[0].w' )
        cmds.connectAttr( wtAddMtx + '.blend', wtAddMtx + '.i[1].w' )
        return wtAddMtx





def getBlendTwoMatrixDcmpNode( first, second, target ):
    
    multMtx = getBlendTwoMatrixNode( first, second, target )
    return getDcmp( multMtx )




def outMeshToSrcInMesh( firstObj, targetObjs, evt=0 ):
    
    outTargets = dag.getNoneIoMesh( firstObj )
    targetObjs = convert.singleToList( targetObjs )
    
    if not outTargets: return None
    outTarget = outTargets[0]
    
    for targetObj in targetObjs:
        inTargets  = get.ioMesh( targetObj )
        if not inTargets: continue
        for inTarget in inTargets:
            if cmds.listConnections( inTarget+'.inMesh' ): continue
            if not cmds.listConnections( inTarget + '.outMesh' ) and not cmds.listConnections( inTarget + '.worldMesh' ): continue
            cmds.connectAttr( outTarget + '.outMesh', inTarget + '.inMesh' )



def forceConnect( srcAttr, dstAttr ):
    
    if cmds.isConnected( srcAttr, dstAttr ): return None
    cmds.connectAttr( srcAttr, dstAttr, f=1 )
    


def translate( src, dst ):
    
    attrs = get.childrenAttr( dst + '.t' )
    connections = map( lambda attr : [cmds.listConnections( attr, s=1, d=0, p=1 ),attr], attrs )
    connections = filter( lambda srcDst : srcDst[0], connections )
    map( lambda srcDst : cmds.disconnectAttr( srcDst[0][0], srcDst[1] ), connections )
    forceConnect( src + '.t', dst + '.t' )
    



def rotate( src, dst ):
    
    attrs = get.childrenAttr( dst + '.r' )
    connections = map( lambda attr : [cmds.listConnections( attr, s=1, d=0, p=1 ),attr], attrs )
    connections = filter( lambda srcDst : srcDst[0], connections )
    map( lambda srcDst : cmds.disconnectAttr( srcDst[0][0], srcDst[1] ), connections )
    forceConnect( src + '.r', dst + '.r' )




def addMult( dstAttr, **options ):
    
    srcAttrs = cmds.listConnections( dstAttr, s=1, d=0, p=1 )
    if not srcAttrs: return None
    
    node, attr = dstAttr.split( '.' )
    multAttr = attr + '_mult'
    attribute.addAttr( node, multAttr, **options )
    
    multNode = cmds.createNode( 'multDoubleLinear' )
    cmds.disconnectAttr( srcAttrs[0], dstAttr )
    cmds.connectAttr( srcAttrs[0], multNode + '.input1' )
    cmds.connectAttr( node+'.'+multAttr, multNode + '.input2' )
    forceConnect( multNode+'.output', dstAttr)



def connectByChannel( src, dst ):
    
    attrs = cmds.channelBox( 'mainChannelBox', q=1, sma=1 )
    
    for attr in attrs:
        if not cmds.attributeQuery( attr, node=src, ex=1 ): continue
        if not cmds.attributeQuery( attr, node=dst, ex=1 ): continue
        forceConnect( src+'.'+attr, dst + '.' + attr )
        


def tx( first, others, evt=0 ):
    
    others = convert.singleToList( others )
    
    for other in others:
        cmds.connectAttr( first + '.tx', other + '.tx' )



def ty( first, others, evt=0 ):
    
    others = convert.singleToList( others )
    
    for other in others:
        cmds.connectAttr( first + '.ty', other + '.ty' )
    


def tz( first, others, evt=0 ):
    
    others = convert.singleToList( others )
    
    for other in others:
        cmds.connectAttr( first + '.tz', other + '.tz' )



def rx( first, others, evt=0 ):
    
    others = convert.singleToList( others )
    
    for other in others:
        cmds.connectAttr( first + '.rx', other + '.rx' )



def ry( first, others, evt=0 ):
    
    others = convert.singleToList( others )
    
    for other in others:
        cmds.connectAttr( first + '.ry', other + '.ry' )
    


def rz( first, others, evt=0 ):
    
    others = convert.singleToList( others )
    
    for other in others:
        cmds.connectAttr( first + '.rz', other + '.rz' )


def sx( first, others, evt=0 ):
    
    others = convert.singleToList( others )
    
    for other in others:
        cmds.connectAttr( first + '.sx', other + '.sx' )



def sy( first, others, evt=0 ):
    
    others = convert.singleToList( others )
    
    for other in others:
        cmds.connectAttr( first + '.sy', other + '.sy' )
    


def sz( first, others, evt=0 ):
    
    others = convert.singleToList( others )
    
    for other in others:
        cmds.connectAttr( first + '.sz', other + '.sz' )



def replace( first, second, target, evt=0 ):
    
    cons = cmds.listConnections( target, s=1, d=0, p=1, c=1 )
    for i in range( 0, len(cons), 2 ):
        con = cons[i+1]
        dest = cons[i]
        
        splits = con.split( '.' )
        node = splits[0]
        attr = '.'.join( splits[1:] )
        if node != first: continue 
        print con
        cmds.connectAttr( second + '.' + attr, dest, f=1 )
        


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




def addMultDoubleLinear( attrName, multValue=1 ):
    
    splits = attrName.split( '.' )
    sel = splits[0]
    attr = '.'.join( splits[1:] )
    
    newAttrName = 'mult_' + attr
    attribute.addAttr( sel, ln=newAttrName, cb=1, dv=multValue )
    multDouble = cmds.createNode( 'multDoubleLinear' )
    
    separateParentConnection( sel, attr )
    
    cons = cmds.listConnections( sel + '.' + attr, s=1, d=0, p=1, c=1 )
    cmds.connectAttr( cons[1], multDouble+'.input1' )
    cmds.connectAttr( sel+'.'+newAttrName, multDouble + '.input2' )
    cmds.connectAttr( multDouble + '.output', sel+'.'+attr, f=1 )



def convertAsAnimCurve( node, attr ):
    
    separateParentConnection( node, attr )
          
    cons = cmds.listConnections( node+'.'+attr, s=1, d=0, p=1, c=1 )
    if not cons: return None
    
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
    cmds.setKeyframe( animCurve, f=-.5, v=-.5 )
    cmds.setKeyframe( animCurve, f=  0, v=  0 )
    cmds.setKeyframe( animCurve, f= .5, v= .5 )
    cmds.setKeyframe( animCurve, f=  1, v=  1 )
    
    cmds.setAttr( animCurve + ".postInfinity", 1 )
    cmds.setAttr( animCurve + ".preInfinity", 1 )
    
    cmds.selectKey( animCurve )
    cmds.keyTangent( itt='spline', ott='spline' )
    
    return animCurve



def getSourceConnection( targets, src, evt=0 ):

    src = cmds.ls( src )[0]
    targets = convert.singleToList( targets )
    
    for trg in targets:
        trg = cmds.ls( trg )[0]
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



def opptimizeConnection( targetNodes, evt=0 ):
    
    targetNodes = convert.singleToList( targetNodes )
    
    for sel in targetNodes:
        srcCon = cmds.listConnections( sel, s=1, d=0, p=1 )
        dstCons = cmds.listConnections( sel, s=0, d=1, p=1 )
        
        for dstCon in dstCons:
            try:cmds.disconnectAttr( srcCon[0], dstCon )
            except:pass
            cmds.connectAttr( srcCon[0], dstCon, f=1 )
        
        if cmds.objExists( sel ): cmds.delete( sel )



def parentConstraint_local( first, second, third, evt=0 ):
    dcmp = getLocalDcmp( first, second )
    cmds.connectAttr( dcmp + '.ot', third + '.t' )
    cmds.connectAttr( dcmp + '.or', third + '.r' )
    



def constraint_point( first, seconds, mo=0, evt=0 ):
    
    seconds = convert.singleToList( seconds )
    
    for second in seconds:
        dcmp = getConstraintDcmp( first, second, mo )
        cmds.connectAttr( dcmp + '.ot', second + '.t' )




def constraint_orient( first, seconds, mo=0, evt=0 ):
    
    seconds = convert.singleToList( seconds )
    
    for second in seconds:
        dcmp = getConstraintDcmp( first, second, mo )
        cmds.connectAttr( dcmp + '.or', second + '.r' )




def constraint_scale( first, seconds, mo=0, evt=0 ):
    
    seconds = convert.singleToList( seconds )
    
    for second in seconds:
        dcmp = getConstraintDcmp( first, second, mo )
        cmds.connectAttr( dcmp + '.os', second + '.s' )





def constraint_parent( first, seconds, mo=0, evt=0 ):
    
    seconds = convert.singleToList( seconds )
    
    for second in seconds:
        dcmp = getConstraintDcmp( first, second, mo )
        cmds.connectAttr( dcmp + '.ot', second + '.t' )
        cmds.connectAttr( dcmp + '.or', second + '.r' )





def getBlendMatrix( matrixNodes ):

    wtAddMatrix = cmds.createNode( 'wtAddMatrix' )
    for i in range( len( matrixNodes ) ):
        matrixAttr = attribute.getOutputMatrixAttributeFromNode( matrixNodes[i] )
        cmds.connectAttr( matrixAttr, wtAddMatrix + '.i[%d].m' % i )
    return wtAddMatrix



def getFollowMatrix( matrixNodes ):
    
    wtAddMatrix = getBlendMatrix( matrixNodes )
    
    plusNode  = cmds.createNode( 'plusMinusAverage' )
    rangeNode = cmds.createNode( 'setRange' )
    condition = cmds.createNode( 'condition' )
    cmds.setAttr( rangeNode + '.minX', 1 )
    cmds.setAttr( rangeNode + '.maxX', 0 )
    cmds.setAttr( rangeNode + '.oldMinX', 0 )
    cmds.setAttr( rangeNode + '.oldMaxX', 1 )
    cmds.connectAttr( plusNode + '.output1D', rangeNode + '.valueX' )
    cmds.connectAttr( plusNode + '.output1D', condition + '.firstTerm' )
    cmds.connectAttr( plusNode + '.output1D', condition + '.colorIfTrueR' )
    cmds.setAttr( condition + '.op', 2 )
    cmds.setAttr( condition + '.secondTerm', 1 )
    
    attrs = []
    for i in range( 1, len( matrixNodes ) ):
        attribute.addAttr( wtAddMatrix, ln='follow_%02d' % i, min=0, max=1, dv=0, k=1 )
        setRange = cmds.createNode( 'setRange' )
        cmds.connectAttr( wtAddMatrix +'.follow_%02d' % i, setRange + '.valueX' )
        cmds.connectAttr( condition + '.outColorR', setRange+ '.oldMaxX' )
        cmds.connectAttr( setRange+'.outValueX', wtAddMatrix+'.i[%d].w' % i )
        cmds.setAttr( setRange + '.maxX', 1 )
        attrs.append( wtAddMatrix + '.follow_%02d' % i )
    
    for i in range( len( attrs ) ):
        cmds.connectAttr( attrs[i], plusNode + '.input1D[%d]' % i )
    
    cmds.connectAttr( rangeNode + '.outValueX', wtAddMatrix + '.i[0].w' )
    return wtAddMatrix
    




def blendMatrixConnect( constObjs, target, mo=0, evt=0 ):
    
    wtAddMtx = cmds.createNode( 'wtAddMatrix' )
    plusNode = cmds.createNode( 'plusMinusAverage' )
    outMM    = cmds.createNode( 'multMatrix' )
    
    cmds.connectAttr( wtAddMtx + '.o', outMM + '.i[0]' )
    cmds.connectAttr( target + '.pim', outMM + '.i[1]' )
    
    outDcmp = getDcmp( outMM )
    
    for i in range( len(constObjs) ):
        constObj = constObjs[i]
        
        if mo:
            targetClone = cmds.createNode( 'transform' )
            cmds.xform( targetClone, ws=1, matrix= cmds.getAttr( target + '.wm' ) )
            cmds.setAttr( targetClone + '.dh', 1 )
            targetClone = cmds.parent( targetClone, constObj )[0]
    
            mtxCompose = cmds.createNode( 'composeMatrix' )
            mm         = cmds.createNode( 'multMatrix' )
            cmds.connectAttr( targetClone + '.t', mtxCompose+'.it' )
            cmds.connectAttr( targetClone + '.r', mtxCompose+'.ir' )
            cmds.connectAttr( mtxCompose + '.outputMatrix', mm + '.i[0]' )
            cmds.connectAttr( constObj + '.wm', mm + '.i[1]' )
            constMatrixAttr = mm + '.o'
        else:
            constMatrixAttr = constObj + '.wm'
        
        divNode = cmds.createNode( 'multiplyDivide' )
        cmds.setAttr( divNode + '.op', 2 )
        
        attribute.addAttr( target, ln='constWeight_%d' % i, k=1, dv=1 )
        cmds.connectAttr( target +'.constWeight_%d' % i, plusNode + '.input1D[%d]' % i )
        cmds.connectAttr( target +'.constWeight_%d' % i, divNode + '.input1X' )
        cmds.connectAttr( plusNode +'.output1D', divNode + '.input2X' )
        
        cmds.connectAttr( constMatrixAttr, wtAddMtx + '.i[%d].m' % i )
        cmds.connectAttr( divNode + '.outputX', wtAddMtx + '.i[%d].w' % i )
    
    cmds.connectAttr( outDcmp + '.ot', target + '.t' )
    cmds.connectAttr( outDcmp + '.or', target + '.r' )
    
    

def blendMatrixAdd( constObjs, target, evt=0 ):
    
    constObjs = convert.singleToList( constObjs )
    
    wtAddMtx = get.nodeFromHistory( target, 'wtAddMatrix' )
    averages = get.nodeFromHistory( target, 'plusMinusAverage' )
    if not wtAddMtx:
        blendMatrixConnect( constObjs, target )
        return 0
    
    multNodes = cmds.listConnections( wtAddMtx, s=1, type='multiplyDivide' )
    length = len( multNodes )
    
    for i in range( len( constObjs ) ):
        cuNumber = length + i
        attribute.addAttr( target, ln='constWeight_%d' % cuNumber, k=1 )
        
        divNode = cmds.createNode( 'multiplyDivide' ); cmds.setAttr( divNode + '.op', 2 )
        
        cmds.connectAttr( target + '.constWeight_%d' % cuNumber, averages[0] +'.input1D[%d]' % cuNumber )
        cmds.connectAttr( target + '.constWeight_%d' % cuNumber, divNode +'.input1X' )
        cmds.connectAttr( averages[0] +'.output1D', divNode + '.input2X' )
        
        cmds.connectAttr( constObjs[i] + '.wm', wtAddMtx[0] +'.i[%d].m' % cuNumber )
        cmds.connectAttr( divNode + '.outputX', wtAddMtx[0] + '.i[%d].w' % cuNumber )
    
    return length




def blendTwoMatrixConnection( first, second, blendedNode, evt=1 ):

    dcmp = getBlendTwoMatrixDcmpNode(first, second, blendedNode)
    
    cmds.connectAttr( dcmp + '.ot', blendedNode + '.t' )
    cmds.connectAttr( dcmp + '.or', blendedNode + '.r' )
    
    return blendedNode






def lookAtConnect( lookTarget, rotTargets, axisIndex = None ):
    
    rotTargets = convert.singleToList( rotTargets )
    
    lookPoint = OpenMaya.MPoint( *cmds.xform( lookTarget, q=1, ws=1, t=1 ) )
    
    for rotTarget in rotTargets:
        rotTargetP = cmds.listRelatives( rotTarget, p=1, f=1 )
        rotTargetPos = OpenMaya.MPoint( *cmds.xform( rotTarget, q=1, ws=1, t=1 ) )
        rotTargetPPos = OpenMaya.MPoint( *cmds.xform( rotTargetP, q=1, ws=1, t=1 ) )
        
        if not rotTargetP or rotTargetPos.distanceTo( rotTargetPPos ) > 0.001:
            rotTarget, rotTargetP = dag.makeParent( rotTarget )[0]
        
        lookVector = lookPoint - rotTargetPos
        rotMtx = convert.listToMatrix( cmds.getAttr( rotTarget + '.wm' ) )
        maxDotValue, maxDotIndex = value.maxDotIndexAndValue( lookVector, rotMtx )
        
        dcmp = getLookAtDcmp( lookTarget, rotTarget )
    
        abnodes = cmds.listConnections( dcmp + '.ot', type='angleBetween' )
        if not abnodes:
            pma = cmds.createNode( 'plusMinusAverage' )
            directionList = [[1,0,0], [0,1,0], [0,0,1],[-1,0,0], [0,-1,0], [0,0,-1]]
            attribute.addAttr( rotTarget, ln='lookAtAxis', at="enum", en="X:Y:Z:-X:-Y:-Z:", k=1 )
            for i in range( len( directionList ) ):
                condition = cmds.createNode( 'condition' )
                cmds.connectAttr( rotTarget + '.lookAtAxis', condition + '.firstTerm' )
                cmds.setAttr( condition + '.secondTerm', i )
                cmds.setAttr( condition + '.colorIfTrue', *(directionList[i]) )
                cmds.setAttr( condition + '.colorIfFalse', 0,0,0 )
                cmds.connectAttr( condition + '.outColor', pma + '.input3D[%d]' % i )
            if maxDotValue < 0:
                maxDotIndex += 3
            node = cmds.createNode( 'angleBetween' )
            cmds.connectAttr( pma + '.output3D', node + '.v1' )
            cmds.connectAttr( dcmp +'.ot', node + '.v2' )
            if axisIndex != None:
                cmds.setAttr( rotTarget + '.lookAtAxis', axisIndex )
            else:
                cmds.setAttr( rotTarget + '.lookAtAxis', maxDotIndex )
            
        else:
            node = abnodes[0]
        
        cmds.connectAttr( node + '.euler', rotTarget + '.r' )
        try:cmds.setAttr( rotTarget + '.jo', 0,0,0 )
        except:pass



def makeLookAtChild( lookTarget, aimTarget, name=None, dirIndex=None ):
    
    lookAtChild = dag.makeChild( lookTarget, name )
    lookAtConnect( aimTarget, lookAtChild, dirIndex )
    return lookAtChild




def scaleConnectByLookTarget( lookTarget, scaleTargets, evt=0 ):
    
    scaleTargets = convert.singleToList( scaleTargets )
    
    lookPoint = OpenMaya.MPoint( *cmds.xform( lookTarget, q=1, ws=1, t=1 ) )
    
    for scaleTarget in scaleTargets:
        scaleTargetP = cmds.listRelatives( scaleTarget, p=1, f=1 )
        scaleTargetPos = cmds.xform( scaleTarget, q=1, ws=1, t=1 )
        if not scaleTargetP or cmds.xform( scaleTargetP, q=1, ws=1, t=1 ) != scaleTargetPos:
            rotTarget = dag.makeParent( scaleTarget )
        scalePoint = OpenMaya.MPoint( *scaleTargetPos )
        
        lookVector = lookPoint - scalePoint
        rotMtx = convert.listToMatrix( cmds.getAttr( rotTarget + '.wm' ) )
        maxDotValue, maxDotIndex = value.maxDotIndexAndValue( lookVector, rotMtx )
        
        targetAttr = ['sx', 'sy', 'sz'][maxDotIndex]



def getConstrainedObject( target, constLabel = '_coned' ):
    
    attrName = 'constObjPointer'
    
    attribute.addAttr( target, ln= attrName, at='message' )
    connections = cmds.listConnections( target+'.'+attrName, s=1, d=0 )
    if not connections:
        constTarget = cmds.createNode( 'transform', n= target.split( '|' )[-1].replace( ':', '_' ) + constLabel )
        cmds.connectAttr( constTarget+'.message', target+'.'+attrName )
        constraint_parent( target, constTarget )
    else:
        constTarget = connections[0]
    
    return constTarget



def parentToConstrainedObject( targets, parentTarget ):
    
    targets = convert.singleToList( targets )
    parentTarget = getConstrainedObject( parentTarget )
    cmds.parent( targets, parentTarget )




def getWorldDcmp( target ):
    
    cons = cmds.listConnections( target + '.wm', d=1, type='decpmposeMatrix', s=0 )
    if cons:
        return cons[0]
    
    dcmp = cmds.createNode( 'decomposeMatrix' )
    cmds.connectAttr( target + '.wm', dcmp + '.imat' )
    
    return dcmp
    




def createSkinWeightMatrix( bindPreObjs, matrixObjs ):

    wtAddMtx = cmds.createNode( 'wtAddMatrix' )
    
    def getMultMtx( bindPreObj, matrixObj ):
        bindPreMultMtxs = cmds.listConnections( bindPreObj + '.wim', type='multMatrix' )
        matrixMultMtxs  = cmds.listConnections( matrixObj + '.wm', type='multMatrix' )
        
        print bindPreObj, bindPreMultMtxs
        print matrixObj, matrixMultMtxs
        
        if bindPreMultMtxs and matrixMultMtxs:  
            for bindPreMultMtx in bindPreMultMtxs:
                if bindPreMultMtx in matrixMultMtxs:
                    return bindPreMultMtx
        
        multMtx = cmds.createNode( 'multMatrix' )
        cmds.connectAttr( bindPreObjs[i] + '.wim', multMtx + '.i[0]' )
        cmds.connectAttr( matrixObjs[i] + '.wm', multMtx + '.i[1]' )
        return multMtx


    for i in range( len( bindPreObjs ) ):
        attribute.addAttr( wtAddMtx, ln='skinWeight_%d' % i, min=0, max=1, k=1 )
        
        multMtx = getMultMtx( bindPreObjs[i], matrixObjs[i] )
        
        cmds.connectAttr( multMtx + '.o', wtAddMtx + '.i[%d].m' % i )
        cmds.connectAttr( wtAddMtx + '.skinWeight_%d' % i, wtAddMtx + '.i[%d].w' % i )
    
    return wtAddMtx




def connect( src, dst, srcAttrs, dstAttrs ):
    
    for i in range( len( srcAttrs ) ):
        cmds.connectAttr( src + '.' + srcAttrs[i], dst + '.' + dstAttrs[i] )



#--------------------sg object exists ----------------------------------------------

def getAngle( node, axis=[1,0,0] ):
    
    node = sgcommands.convertSg( node )
    
    attrOt = node.attr( 'ot' )
    connectedAttrs = sgcommands.listConnections( attrOt, s=0, d=1, p=1 )
    
    connectionExists = False
    for connectedAttr in connectedAttrs:
        if connectedAttr.node().type() == 'angleBetween':
            value = connectedAttr.node().attr( 'vector1' ).get()
            if axis == value:
                connectionExists = True
                break
    
    if not connectionExists:
        angleNode = sgcommands.createNode("angleBetween")
        attr = angleNode.attr( 'vector2' )
        attrOt >> attr
        
        return angleNode



def getRotationMatrixNode( xNode, yNode, zNode ):
    
    xAttr = sgobject.SGNode( xNode ).vectorOutput()
    yAttr = sgobject.SGNode( yNode ).vectorOutput()
    zAttr = sgobject.SGNode( zNode ).vectorOutput()
    
    fbfMtx = sgcommands.createNode( 'fourByFourMatrix' )
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



def getCrossVectorNode( first, second ):
    
    crossVector = sgcommands.createNode( 'vectorProduct' )
    crossVector.attr( 'op' ).set( 2 )
    
    first.vectorOutput()  >> crossVector.attr( 'input1' )
    second.vectorOutput() >> crossVector.attr( 'input2' )
    
    return crossVector



