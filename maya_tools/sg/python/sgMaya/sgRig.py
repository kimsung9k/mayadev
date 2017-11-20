from maya import OpenMaya
from maya import cmds
import pymel.core
from sgMaya import sgCmds
import random



def createXLookAtJointLine( inputTargets ):
    
    targets = []
    for inputTarget in inputTargets:
        targets.append( pymel.core.ls( inputTarget )[0] )
    
    beforeJnt = None
    baseMatrix = None
    joints = []
    for i in range( len( targets )-1 ):
        if not baseMatrix:
            baseMatrix = sgCmds.listToMatrix( cmds.getAttr( targets[i].wm.name() ) )
        else:
            baseMatrixList = sgCmds.matrixToList( baseMatrix )
            targetPos = pymel.core.xform( targets[i], q=1, ws=1, t=1 )
            baseMatrixList[12] = targetPos[0]
            baseMatrixList[13] = targetPos[1]
            baseMatrixList[14] = targetPos[2]
            baseMatrix = sgCmds.listToMatrix( baseMatrixList )

        targetPos = OpenMaya.MPoint( *pymel.core.xform( targets[i+1], q=1, ws=1, t=1 ) )
        localPos = targetPos * baseMatrix.inverse()
        
        angleValues = pymel.core.angleBetween( v1=[1,0,0], v2=[localPos.x, localPos.y, localPos.z], er=1 )
        rotMtx = sgCmds.rotateToMatrix( angleValues )
        
        jointMatrix = sgCmds.matrixToList( rotMtx * baseMatrix )
        if beforeJnt:
            pymel.core.select( beforeJnt )
        else:
            pymel.core.select( d=1 )
        cuJoint = pymel.core.joint()
        pymel.core.xform( cuJoint, ws=1, matrix=jointMatrix )
        baseMatrix = sgCmds.listToMatrix( jointMatrix )
        joints.append( cuJoint )
        beforeJnt = cuJoint
    
    pymel.core.select( beforeJnt )
    endJnt = pymel.core.joint()
    pymel.core.xform( endJnt, ws=1, matrix= targets[-1].wm.get() )
    endJnt.r.set( 0,0,0 )
    joints.append( endJnt )
    
    return joints
    


def makeWaveJoint( inputTopJoint ): 
    
    topJoint = pymel.core.ls( inputTopJoint )[0]
    children = topJoint.listRelatives( c=1, type='transform' )
    joints = [topJoint]
    
    while children:
        joints.append( children[0] )
        children = children[0].listRelatives( c=1, type='transform' )
    
    joints = list( filter( lambda x : x.nodeType() == 'joint', joints ) )
    
    methodList = ['Sine', 'Rand', 'RandBig']
    axisList   = ['X', 'Y', 'Z']
    
    firstJnt = joints[0]
    sgCmds.addOptionAttribute( firstJnt, 'All' )
    sgCmds.addAttr( firstJnt, ln='move', k=1 )
    sgCmds.addAttr( firstJnt, ln='allWeight', min=0, dv=1, k=1 )
    sgCmds.addAttr( firstJnt, ln='allSpeed', min=0, dv=1, k=1 )
    for method in methodList:
        sgCmds.addOptionAttribute( firstJnt, '%s' % method )
        sgCmds.addAttr( firstJnt, ln='all%sWeight' % method, min=0, dv=1, k=1 )
        sgCmds.addAttr( firstJnt, ln='all%sSpeed' % method, min=0, dv=1, k=1 )
    sgCmds.addOptionAttribute( firstJnt, 'intervalValueAdd' )
    sgCmds.addAttr( firstJnt, ln='intervalValueAdd', min=0, dv=15, k=1 )
    
    for joint in joints:
        try:sgCmds.freezeJoint( joint )
        except:pass
    
    for method in methodList:
        dvOffset = 0
        dvInterval = -2
        
        sgCmds.addOptionAttribute( firstJnt, 'control%s' % method )
        sgCmds.addAttr( firstJnt, ln='interval%s' %(method), k=1, dv=dvInterval )
        sgCmds.addAttr( firstJnt, ln='offset%s' %(method), k=1, dv=dvOffset )
        for axis in axisList:    
            dvValue = 5
            sgCmds.addAttr( firstJnt, ln='value%s%s' %(method,axis), min=-90, max=90, k=1, dv = dvValue )
        for axis in axisList:
            if axis == 'Y':
                dvSpeed = 1.2
            else:
                dvSpeed = 0.8
            sgCmds.addAttr( firstJnt, ln='speed%s%s' %(method,axis), k=1, dv=dvSpeed )
            
    
    for axis in axisList:  
        randValues = []
        for j in range( 100 ):
            randValue = random.uniform( -1, 1 )
            randValues.append( randValue )
        
        for i in range( 1, len(joints)-1 ):
            methodAdd = pymel.core.createNode( 'plusMinusAverage' )
            globalAllMult = pymel.core.createNode( 'multDoubleLinear' )
            firstJnt.attr( 'allWeight' ) >> globalAllMult.input1
            methodAdd.output1D >> globalAllMult.input2
            
            joint = joints[i]
            methodIndex = 0
            
            for method in methodList:
                globalAllSpeedMult = pymel.core.createNode( 'multDoubleLinear' )
                firstJnt.attr( 'allSpeed' ) >> globalAllSpeedMult.input1
                globalSpeedMult = pymel.core.createNode( 'multDoubleLinear' )
                firstJnt.attr( 'all%sSpeed' % method ) >> globalSpeedMult.input1
                globalSpeedMult.output >> globalAllSpeedMult.input2
                
                animCurve = pymel.core.createNode( 'animCurveUU' )
                animCurve.preInfinity.set( 3 )
                animCurve.postInfinity.set( 3 )
                if method in ['Rand','RandBig']:
                    for j in range( len( randValues ) ):
                        randValue = randValues[j]
                        if j == 0 or j == 99:
                            pymel.core.setKeyframe( animCurve, f=j*10, v=0 )
                        else:
                            pymel.core.setKeyframe( animCurve, f=j*10, v=randValue )
                elif method == 'Sine':
                    pymel.core.setKeyframe( animCurve, f=0,  v= 1 )
                    pymel.core.setKeyframe( animCurve, f=5, v=-1 )
                    pymel.core.setKeyframe( animCurve, f=10, v= 1 )
                
                valueMult = pymel.core.createNode( 'multDoubleLinear' )
                speedMult = pymel.core.createNode( 'multDoubleLinear' )
                intervalMult = pymel.core.createNode( 'multDoubleLinear' )
                inputSum = pymel.core.createNode( 'plusMinusAverage' )
                firstJnt.attr( 'offset%s' %( method ) ) >> inputSum.input1D[0]
                firstJnt.attr( 'move' ) >> speedMult.input1
                firstJnt.attr( 'speed%s%s' %( method, axis ) ) >> speedMult.input2
                speedMult.output >> globalSpeedMult.input2
                globalAllSpeedMult.output >> inputSum.input1D[1]
                intervalMult.input1.set( i )
                firstJnt.attr( 'interval%s' %( method ) ) >> intervalMult.input2
                intervalMult.output >> inputSum.input1D[2]
                inputSum.output1D >> animCurve.input
                animCurve.output >> valueMult.input1
                firstJnt.attr( 'value%s%s' %(method,axis) ) >> valueMult.input2
                
                globalWeightMult = pymel.core.createNode( 'multDoubleLinear' )
                firstJnt.attr( 'all%sWeight' % method ) >> globalWeightMult.input1
                valueMult.output >> globalWeightMult.input2
                globalWeightMult.output >> methodAdd.input1D[methodIndex]
                methodIndex+=1
            
            intervalValueAddPercent = pymel.core.createNode( 'multDoubleLinear' )
            intervalValueAddMult = pymel.core.createNode( 'multDoubleLinear' )
            intervalValueAddAdd  = pymel.core.createNode( 'addDoubleLinear' )
            
            intervalValueAddPercent.input1.set( 0.01 * i )
            firstJnt.attr('intervalValueAdd') >> intervalValueAddPercent.input2
            intervalValueAddPercent.output >> intervalValueAddMult.input1
            globalAllMult.output >> intervalValueAddMult.input2
            globalAllMult.output >>intervalValueAddAdd.input1
            intervalValueAddMult.output >> intervalValueAddAdd.input2
            
            intervalValueAddAdd.output >> joint.attr( 'rotate%s' % axis )
            
            
                


def makeWaveGlobal( inputTopJoints, inputCtl ):
    
    topJoints = []
    for inputTopJoint in inputTopJoints:
        topJoints.append( pymel.core.ls( inputTopJoint )[0] )

    ctl = pymel.core.ls( inputCtl )[0]

    sgCmds.addOptionAttribute( ctl, 'control_offset' )
    sgCmds.addAttr( ctl, ln='offsetGlobalInterval', k=1, dv=1 )
    sgCmds.addAttr( ctl, ln='offsetGlobalRand', k=1, dv=1 )

    attrs = topJoints[0].listAttr( ud=1 )
    sgCmds.addOptionAttribute( ctl, 'wave' )
    for attr in attrs:
        sgCmds.copyAttribute( topJoints[0], ctl, attr.longName() )
    
    circleAttrs = ctl.listAttr( ud=1, k=1 )
    
    for topJoint in topJoints:
        for circleAttr in circleAttrs:
            if not pymel.core.attributeQuery( circleAttr.longName(), node=topJoint, ex=1 ): continue
            circleAttr >> topJoint.attr( circleAttr.longName() )
    
    index = 0
    for topJoint in topJoints:
        offsetRand = pymel.core.createNode( 'multDoubleLinear' )
        offsetInterval = pymel.core.createNode( 'multDoubleLinear' )
        offsetAll = pymel.core.createNode( 'addDoubleLinear' )
        offsetRand.input1.set( random.uniform( -5, 5 ) )
        ctl.attr( 'offsetGlobalRand' ) >> offsetRand.input2
        offsetInterval.input1.set( index )
        ctl.attr( 'offsetGlobalInterval' ) >> offsetInterval.input2
        offsetRand.output >> offsetAll.input1
        offsetInterval.output >> offsetAll.input2
        offsetAll.output >> topJoint.attr( 'offsetSine' )
        index += 1
        allWeightPlug = topJoint.allWeight.listConnections( s=1, d=0, p=1 )[0]
        sgCmds.addAttr( topJoint, ln='globalWeight', min=0, max=1, k=1, dv=1 )
        multGlobal = pymel.core.createNode( 'multDoubleLinear' )
        topJoint.globalWeight >> multGlobal.input1
        allWeightPlug >> multGlobal.input2
        multGlobal.output >> topJoint.allWeight



def createRandomTranslate( inputCtl, inputTarget ):
    
    ctl    = pymel.core.ls( inputCtl )[0]
    target = pymel.core.ls( inputTarget )[0]
    
    sgCmds.addOptionAttribute( ctl, 'translateRandom' )
    sgCmds.addAttr( ctl, ln='move', k=1 )
    sgCmds.addAttr( ctl, ln='speed', k=1, min=0, dv=1 )
    multMove = pymel.core.createNode( 'multDoubleLinear' )
    ctl.attr( 'move' )  >> multMove.input1
    ctl.attr( 'speed' ) >> multMove.input2
    
    for axis in ['X', 'Y', 'Z']:
        animCurve = pymel.core.createNode( 'animCurveUU' )
        animCurve.preInfinity.set( 3 )
        animCurve.postInfinity.set( 3 )
        for j in range( 100 ):
            randValue = random.uniform( -1, 1 )
            if j == 0 or j == 99:
                pymel.core.setKeyframe( animCurve, f=j*10, v=0 )
            else:
                pymel.core.setKeyframe( animCurve, f=j*10, v=randValue )
                print "set rand value : %f" % randValue

        multMove.output >> animCurve.input
        sgCmds.addAttr( ctl, ln='weight_%s' % axis, min=0, dv=0.5, k=1 )
        multWeight = pymel.core.createNode( 'multDoubleLinear' )
        ctl.attr( 'weight_%s' % axis ) >> multWeight.input1
        animCurve.output >> multWeight.input2
        multWeight.output >> target.attr( 'translate%s' % axis )



def makeUdAttrGlobal( inputTargets, inputCtl ):

    targets = []
    for inputTarget in inputTargets:
        targets.append( pymel.core.ls( inputTarget )[0] )

    ctl = pymel.core.ls( inputCtl )[0]

    attrs = targets[0].listAttr( ud=1 )
    for attr in attrs:
        sgCmds.copyAttribute( targets[0], ctl, attr.longName() )
    
    circleAttrs = ctl.listAttr( ud=1, k=1 )
    
    for target in targets:
        for circleAttr in circleAttrs:
            if not pymel.core.attributeQuery( circleAttr.longName(), node=target, ex=1 ): continue
            circleAttr >> target.attr( circleAttr.longName() )



def buildJointLineByVtxNum( mesh, vtxList, numJoints ):
    
    points = OpenMaya.MPointArray()
    
    for vtxIndex in vtxList:
        vtxPos = OpenMaya.MPoint( *cmds.xform( mesh + '.vtx[%d]' % vtxIndex, q=1, ws=1, t=1 )[:3] )
        points.append( vtxPos )
        #print "vtx pos[%d] : %5.3f, %5.3f, %5.3f " %( vtxIndex, vtxPos.x, vtxPos.y, vtxPos.z )
    
    curveData = OpenMaya.MFnNurbsCurveData()
    oData = curveData.create()
    fnCurve = OpenMaya.MFnNurbsCurve()
    
    fnCurve.createWithEditPoints( points, 3, fnCurve.kOpen, False, True, True, oData )
    
    newFnCurve = OpenMaya.MFnNurbsCurve( oData )
    
    eachLength = newFnCurve.length()/numJoints
    parentObj = None
    joints = []
    for i in range( numJoints+1 ):
        paramValue = newFnCurve.findParamFromLength( eachLength * i )
        point = OpenMaya.MPoint()
        newFnCurve.getPointAtParam( paramValue, point )
        
        if not parentObj:
            pymel.core.select( d=1 )
        else:
            pymel.core.select( parentObj )

        joint = pymel.core.joint()
        joints.append( joint )
        pymel.core.move( point.x, point.y, point.z, joint, ws=1 )
        parentObj = joint
    return joints[0]



class ParentedMove:
    
    offsetMatrixAttrName = 'parentedMove_offsetMatrix'
    parentTargetAttrName = 'parentedMove_parentTarget'
    expressionName       = 'ex_ParentedMove'
    
    @staticmethod
    def set( inputChildTarget, inputParentTarget ):
        
        childTarget  = pymel.core.ls( inputChildTarget )[0]
        parentTarget = pymel.core.ls( inputParentTarget )[0]
        
        sgCmds.addAttr( childTarget, ln=ParentedMove.offsetMatrixAttrName, at='matrix' )
        sgCmds.addAttr( childTarget, ln=ParentedMove.parentTargetAttrName, at='message' )
        
        try:parentTarget.message >> childTarget.attr( ParentedMove.parentTargetAttrName )
        except:pass
        
        localMatrix = sgCmds.getMMatrix( childTarget.wm ) * sgCmds.getMMatrix( parentTarget.wim )
        childTarget.attr( ParentedMove.offsetMatrixAttrName ).set( sgCmds.matrixToList( localMatrix ) )
    
    
    @staticmethod
    def reset( inputChildTarget ):
        
        childTarget = pymel.core.ls( inputChildTarget )[0]
        if not pymel.core.attributeQuery( ParentedMove.offsetMatrixAttrName, node=childTarget, ex=1 ) or\
           not pymel.core.attributeQuery( ParentedMove.parentTargetAttrName, node=childTarget, ex=1 ):
            pymel.core.error( "%s is not Parenting Move Object" % childTarget.name() )
        
        parentTargets = childTarget.attr( ParentedMove.parentTargetAttrName ).listConnections( s=1, d=0 )
        if not parentTargets:
            pymel.core.error( "%s is not Parenting Move Object" % childTarget.name() )
        
        localMatrix = sgCmds.getMMatrix( childTarget.wm ) * sgCmds.getMMatrix( parentTargets[0].wim )
        childTarget.attr( ParentedMove.offsetMatrixAttrName ).set( sgCmds.matrixToList( localMatrix ) )

    
    
    @staticmethod
    def run():
        attrs = pymel.core.ls( '*.' + ParentedMove.parentTargetAttrName )
        for attr in attrs:
            node = attr.node()
            parentTarget = attr.listConnections( s=1, d=0 )[0]
            parentMtx = sgCmds.getMMatrix( parentTarget.wm )
            localMtx = sgCmds.getMMatrix( node.attr( ParentedMove.offsetMatrixAttrName ) )
            worldMtxList = sgCmds.matrixToList( localMtx * parentMtx )
            pymel.core.xform( node, ws=1, matrix=worldMtxList )
    
    
    @staticmethod
    def createExpression():
        if pymel.core.ls( ParentedMove.expressionName + '*', type='expression' ): return None
        pymel.core.expression( s="python( \"from sgMaya import sgAnim;sgAnim.ParentedMove.run()\" )",  o="", ae=1, uc='all', n = ParentedMove.expressionName )
    
    
    @staticmethod
    def deleteExpression():
    
        if pymel.core.ls( ParentedMove.expressionName + '*', type='expression' ):
            pymel.core.delete( pymel.core.ls( ParentedMove.expressionName + '*', type='expression' ) )



class NetControlRig:
    
    groupAttrName = 'netControlGroup'
    rowAttrName   = 'netControlRow'
    columnAttrName = 'netControlColumn'
    bigControlAttrName = 'netControlBigTarget'


    def __init__(self, netGroupName ):
        
        self.baseName = netGroupName
        self.numRows = 0
        self.numColumns = 0
        self.targets = []


    def setRows( self, *inputOrderedTargets ):
        
        orderedTargets = [ pymel.core.ls( inputOrderedTarget )[0] for inputOrderedTarget in inputOrderedTargets ]
        for i in range( len( orderedTargets ) ):
            orderedTargets[i].rename( self.baseName + '_%02d' % i )
            sgCmds.addAttr( orderedTargets[i], ln=NetControlRig.groupAttrName, dt='string' )
            orderedTargets[i].attr( NetControlRig.groupAttrName ).set( self.baseName )
            sgCmds.addAttr( orderedTargets[i], ln=NetControlRig.rowAttrName, at='long' )
            orderedTargets[i].attr( NetControlRig.rowAttrName ).set( i )
            self.numRows += 1
            self.targets.append( orderedTargets[i] )


    def setBigConnect( self, *inputBigTargets ):
        
        bigTargets = [ pymel.core.ls( inputBigControl )[0] for inputBigControl in inputBigTargets ]
        
        for i in range( len( bigTargets ) ):
            closeTarget = sgCmds.getClosestTransform( bigTargets[i], self.targets )
            sgCmds.addAttr( closeTarget, ln=NetControlRig.bigControlAttrName, at='message' )
            bigTargets[i].message >> closeTarget.attr( NetControlRig.bigControlAttrName )
    
    
    def setParentContraint(self, circle=False, toParent=False ):
        
        def getBigControl( target ):
            return target.attr( NetControlRig.bigControlAttrName ).listConnections( s=1, d=0 )[0]
        
        if not self.numColumns:
            bigControlIndices = []
            
            for i in range( len( self.targets ) ):
                if not pymel.core.attributeQuery( NetControlRig.bigControlAttrName,
                                                  node = self.targets[i], ex=1 ):
                    continue
                bigControlIndices.append( i )

            for i in range( len( self.targets ) ):
                if toParent:
                    parentTarget = self.targets[i].getParent()
                else:
                    parentTarget = self.targets[i]

                if i in bigControlIndices:
                    bigControl = getBigControl(self.targets[i])
                    pymel.core.parentConstraint( bigControl, parentTarget, mo=1 )
                else:
                    twoSideBigControlsIndices = [None, None]
                    for j in range( len( bigControlIndices ) ):
                        if i < bigControlIndices[j]:
                            if j == 0:
                                if circle:
                                    twoSideBigControlsIndices = [ bigControlIndices[0], bigControlIndices[-1]]
                                else:
                                    twoSideBigControlsIndices = [ bigControlIndices[0], bigControlIndices[0]]
                            else:
                                twoSideBigControlsIndices = [bigControlIndices[j-1],bigControlIndices[j]]
                            break
                    
                    if twoSideBigControlsIndices[0] == None:
                        if circle:
                            twoSideBigControlsIndices = [bigControlIndices[-1], bigControlIndices[0]]
                        else:
                            twoSideBigControlsIndices = [bigControlIndices[-1], bigControlIndices[-1]]
                    
                    twoSideControls = [ getBigControl( self.targets[k] ) for k in twoSideBigControlsIndices ]
                    
                    first  = sgCmds.getMVector( twoSideControls[0] )
                    second = sgCmds.getMVector( twoSideControls[1] )
                    target = sgCmds.getMVector( self.targets[i] )
                    
                    baseVector = second - first
                    targetVector = target - first
                    
                    if baseVector.length() < 0.00001:
                        pymel.core.parentConstraint( twoSideControls[0], parentTarget, mo=1 )
                        continue
                    
                    projTargetToBase = baseVector * ( ( targetVector * baseVector )/baseVector.length()**2 )
                    
                    secondWeight = projTargetToBase.length() / baseVector.length()
                    if secondWeight > 1:
                        secondWeight = 1
                    firstWeight = 1.0 - secondWeight
                    
                    print firstWeight, secondWeight
                    
                    if firstWeight == 0:
                        constraint = pymel.core.parentConstraint( twoSideControls[1], parentTarget, mo=1 )
                    elif secondWeight == 0:
                        constraint = pymel.core.parentConstraint( twoSideControls[0], parentTarget, mo=1 )
                    else:
                        constraint = pymel.core.parentConstraint( twoSideControls[0], twoSideControls[1], parentTarget, mo=1 )
                        constraint.w0.set( firstWeight )
                        constraint.w1.set( secondWeight )
                    
                    
                    
class SplineRig:
    
    def __init__(self, topJoint ):
        
        self.topJoint = pymel.core.ls( topJoint )[0]
        self.jointH = self.topJoint.listRelatives( c=1, ad=1, type='joint' )
        self.jointH.append( self.topJoint )
        self.jointH.reverse()
    
    
    def createSplineCurve(self):
        
        poses = []
        for jnt in self.jointH:
            pos = pymel.core.xform( jnt, q=1, ws=1, t=1 )
            poses.append( pos )
        
        curve = pymel.core.curve( ep=poses, d=3 )
        return curve
    
    
    def assignToCurve(self, inputCurve ):
        
        curve = pymel.core.ls( inputCurve )[0]
        return pymel.core.ikHandle( sj=self.topJoint, ee=self.jointH[-1], sol="ikSplineSolver", ccv=False, pcv=False, curve=curve )[0]
        
        
        


class IkDetailJoint:

    def __init__( self, baseJoint, targetJoint ):
        
        self.baseJoint   = pymel.core.ls( baseJoint )[0]
        self.targetJoint = pymel.core.ls( targetJoint )[0]
        self.joints = []
    
        localMtx = sgCmds.getLocalMatrix( self.targetJoint.wm, self.baseJoint.wim )
        upVectorStart = pymel.core.createNode( 'vectorProduct' ); upVectorStart.op.set( 3 )
        upVectorEnd   = pymel.core.createNode( 'vectorProduct' ); upVectorEnd.op.set( 3 )
        directionIndex = sgCmds.getDirectionIndex( [localMtx.o.get().a30, localMtx.o.get().a31, localMtx.o.get().a32] )
        upVector = sgCmds.getVectorList()[(directionIndex+1)%6]
        upVectorStart.input1.set( upVector )
        upVectorEnd.input1.set( upVector )
        localMtx.o >> upVectorEnd.matrix
        
        self.aimIndex = ( directionIndex ) % 3
        self.upIndex  = ( directionIndex + 1 ) % 3
        self.crossIndex = ( directionIndex + 2 ) % 3
        self.upVectorStart = upVectorStart
        self.upVectorEnd   = upVectorEnd
        self.reverseVector = False
        if directionIndex >= 3:
            self.reverseVector = True


    def makeCurve(self):
        
        crvGrp = pymel.core.createNode( 'transform', n='CrvGrp_'+self.baseJoint )
        crv = pymel.core.curve( p=[[0,0,0],[0,0,0]], n='Crv_'+self.baseJoint, d=1 )
        crv.setParent( crvGrp )
        dcmp = sgCmds.getLocalDecomposeMatrix( self.targetJoint.wm, self.baseJoint.wim )
        dcmp.ot >> crv.getShape().controlPoints[1]
        sgCmds.constrain_all( self.baseJoint, crvGrp )
        self.baseGrp = crvGrp
        self.curve = crv



    def addJointAtParam(self, paramValue ):
        
        pointOnCurveInfo = pymel.core.createNode( 'pointOnCurveInfo' )
        self.curve.getShape().local >> pointOnCurveInfo.inputCurve
        pointOnCurveInfo.top.set( 1 )
        pymel.core.select( self.baseGrp )
        newJoint = pymel.core.joint()
        sgCmds.addAttr( newJoint, ln='param', min=0, max=1, dv=paramValue, k=1 )
        newJoint.attr( 'param' ) >> pointOnCurveInfo.parameter
        
        fbfMtx = pymel.core.createNode( 'fourByFourMatrix' )
        
        def getMultVector( outputAttr, reverse ):
            multVector = pymel.core.createNode( 'multiplyDivide' )
            outputAttr >> multVector.input1
            if reverse:
                multVector.input2.set( -1, -1, -1 )
            else:
                multVector.input2.set( 1,1,1 )
            return multVector
        
        aimMultVector = getMultVector( pointOnCurveInfo.tangent, self.reverseVector )
        
        aimMultVector.outputX >> fbfMtx.attr( 'in%d0' % self.aimIndex )
        aimMultVector.outputY >> fbfMtx.attr( 'in%d1' % self.aimIndex )
        aimMultVector.outputZ >> fbfMtx.attr( 'in%d2' % self.aimIndex )   
        
        blendColor = pymel.core.createNode( 'blendColors' )
        self.upVectorEnd.output >> blendColor.color1
        self.upVectorStart.output >> blendColor.color2
        newJoint.param >> blendColor.blender
        
        upMultVector = getMultVector( blendColor.output, self.reverseVector )
        
        upMultVector.outputX >> fbfMtx.attr( 'in%d0' % self.upIndex )
        upMultVector.outputY >> fbfMtx.attr( 'in%d1' % self.upIndex )
        upMultVector.outputZ >> fbfMtx.attr( 'in%d2' % self.upIndex )
        
        print self.aimIndex, self.upIndex, self.crossIndex
        
        crossVector = sgCmds.getCrossVectorNode( aimMultVector.output, upMultVector.output )
        
        crossVector.outputX >> fbfMtx.attr( 'in%d0' % self.crossIndex )
        crossVector.outputY >> fbfMtx.attr( 'in%d1' % self.crossIndex )
        crossVector.outputZ >> fbfMtx.attr( 'in%d2' % self.crossIndex )
        
        pointOnCurveInfo.positionX >> fbfMtx.in30
        pointOnCurveInfo.positionY >> fbfMtx.in31
        pointOnCurveInfo.positionZ >> fbfMtx.in32
        
        dcmp = sgCmds.getDecomposeMatrix( fbfMtx.output )
        dcmp.ot >> newJoint.t
        dcmp.outputRotate >> newJoint.r
        
        self.joints.append( newJoint )
    
    
    def renameJoints(self, name ):
        
        for i in range( len( self.joints ) ):
            self.joints[i].rename( name + '_%02d' % i )
            
            
        
        


