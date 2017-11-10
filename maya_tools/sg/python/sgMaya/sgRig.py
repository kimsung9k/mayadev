from sgCmds import *
import pymel.core


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
            addAttr( orderedTargets[i], ln=NetControlRig.groupAttrName, dt='string' )
            orderedTargets[i].attr( NetControlRig.groupAttrName ).set( self.baseName )
            addAttr( orderedTargets[i], ln=NetControlRig.rowAttrName, at='long' )
            orderedTargets[i].attr( NetControlRig.rowAttrName ).set( i )
            self.numRows += 1
            self.targets.append( orderedTargets[i] )


    def setBigConnect( self, *inputBigTargets ):
        
        bigTargets = [ pymel.core.ls( inputBigControl )[0] for inputBigControl in inputBigTargets ]
        
        for i in range( len( bigTargets ) ):
            closeTarget = getClosestTransform( bigTargets[i], self.targets )
            addAttr( closeTarget, ln=NetControlRig.bigControlAttrName, at='message' )
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
                    
                    first  = getMVector( twoSideControls[0] )
                    second = getMVector( twoSideControls[1] )
                    target = getMVector( self.targets[i] )
                    
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
    
        localMtx = getLocalMatrix( self.targetJoint.wm, self.baseJoint.wim )
        upVectorStart = pymel.core.createNode( 'vectorProduct' ); upVectorStart.op.set( 3 )
        upVectorEnd   = pymel.core.createNode( 'vectorProduct' ); upVectorEnd.op.set( 3 )
        directionIndex = getDirectionIndex( [localMtx.o.get().a30, localMtx.o.get().a31, localMtx.o.get().a32] )
        upVector = getVectorList()[(directionIndex+1)%6]
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
        dcmp = getLocalDecomposeMatrix( self.targetJoint.wm, self.baseJoint.wim )
        dcmp.ot >> crv.getShape().controlPoints[1]
        constrain_all( self.baseJoint, crvGrp )
        self.baseGrp = crvGrp
        self.curve = crv



    def addJointAtParam(self, paramValue ):
        
        pointOnCurveInfo = pymel.core.createNode( 'pointOnCurveInfo' )
        self.curve.getShape().local >> pointOnCurveInfo.inputCurve
        pointOnCurveInfo.top.set( 1 )
        pymel.core.select( self.baseGrp )
        newJoint = pymel.core.joint()
        addAttr( newJoint, ln='param', min=0, max=1, dv=paramValue, k=1 )
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
        
        crossVector = getCrossVectorNode( aimMultVector.output, upMultVector.output )
        
        crossVector.outputX >> fbfMtx.attr( 'in%d0' % self.crossIndex )
        crossVector.outputY >> fbfMtx.attr( 'in%d1' % self.crossIndex )
        crossVector.outputZ >> fbfMtx.attr( 'in%d2' % self.crossIndex )
        
        pointOnCurveInfo.positionX >> fbfMtx.in30
        pointOnCurveInfo.positionY >> fbfMtx.in31
        pointOnCurveInfo.positionZ >> fbfMtx.in32
        
        dcmp = getDecomposeMatrix( fbfMtx.output )
        dcmp.ot >> newJoint.t
        dcmp.outputRotate >> newJoint.r
        
        self.joints.append( newJoint )
    
    
    def renameJoints(self, name ):
        
        for i in range( len( self.joints ) ):
            self.joints[i].rename( name + '_%02d' % i )
            
            
        
        


