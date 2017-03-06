import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import connect
import name
import controller
import dag
import ik
import transform
from sgModules import sgbase
import attribute
import value



def connectMiddles( top, end, middles, vector ):
    
    lookAtTarget = dag.putChild( top )
    lookAtTarget = name.addName( lookAtTarget, top, 'lookAt' )
    
    connect.lookAtConnect( end, lookAtTarget, vector )
    
    numMiddles = len( middles )
    multValue = 1.0/(numMiddles+1)
    
    for i in range( len( middles ) ):
        child = cmds.createNode( 'transform' )
        child = name.addName( child, lookAtTarget, 'child%02d' % i )
        
        child = cmds.parent( child, lookAtTarget )[0]
        dcmp= connect.createLocalDcmp( end, lookAtTarget )
        
        multNode = cmds.createNode( 'multiplyDivide' )
        cmds.connectAttr( dcmp + '.ot', multNode + '.input1' )
        cmds.setAttr( multNode + '.input2', multValue*(i+1), multValue*(i+1), multValue*(i+1) )
        
        cmds.connectAttr( multNode + '.output', child + '.t' )
        transform.setToDefault( child )
        
        middle = cmds.parent( middles[i], child )
            



def putStdJnt( stdObject ):
    
    jnt = cmds.createNode( 'joint' )
    jnt = name.replaceNameToTarget( stdObject, jnt, 'Std_', 'StdJnt_' )
    
    cmds.xform( jnt, ws=1, matrix= cmds.getAttr( stdObject + '.wm' ) )
    
    return jnt





def putStdJntHelp( stdObject ):
    
    stdJntHelp = cmds.createNode( 'transform' )
    stdJntHelp = name.replaceNameToTarget( stdObject, stdJntHelp, 'Std_', 'StdJntHelp_' )
    
    connect.constraint_parent( stdObject, stdJntHelp )
    
    return stdJntHelp




def getStdJntHelp( stdObject ):
    
    stdJntHelp = stdObject.replace( 'Std_', 'StdJntHelp_' )
    if cmds.objExists( stdJntHelp ): return stdJntHelp
    return putStdJntHelp( stdObject )





def makeLookAtChild( aimTarget, rotTarget ):
    rotTargetChild = dag.putChild( rotTarget )
    connect.lookAtConnect( aimTarget, rotTargetChild )
    return rotTargetChild




def makeFingerStdJnt( stds ):

    stdHelps = []
    stdJnts = []
    for std in stds:
        stdJntHelp = putStdJntHelp( std )
        stdJnt = putStdJnt( std )
        cmds.setAttr( stdJnt + '.t', 0,0,0 )
        cmds.setAttr( stdJnt + '.r', 0,0,0 )
        stdHelps.append( stdJntHelp )
        stdJnts.append( stdJnt )
    
    stdHelps.reverse()
    dag.parentByOlder( stdHelps )
    stdHelps.reverse()
    
    stdJnts.reverse()
    dag.parentByOlder( stdJnts )
    stdJnts.reverse()
    
    for i in range( len( stdHelps )-1 ):
        lookAtChild = makeLookAtChild( stdHelps[i+1], stdHelps[i] )
        connect.constraint_parent( lookAtChild, stdJnts[i] )
    
    connect.constraint_point( stdHelps[-1], stdJnts[-1] )




#---------------------------------------------------------------


def makeIkLookBase( stdBase, stdMiddle, stdEnd, stdPoleV, minusX=False, minusY=False ):

    dcmpEnd = connect.getLocalDcmp( stdEnd, stdBase )
    dcmpPoleV = connect.getLocalDcmp( stdPoleV, stdBase )
    dcmpBase = connect.getWorldDcmp( stdBase )
    
    vectorX = cmds.createNode( 'multiplyDivide' )
    vectorY_direction = cmds.createNode( 'multiplyDivide' )
    
    if minusX:
        cmds.setAttr( vectorX + '.input2', -1,-1,-1 )
    else:
        cmds.setAttr( vectorX + '.input2', 1,1,1 )
    
    if minusY:
        cmds.setAttr( vectorY_direction + '.input2', -1, -1, -1 )
    else:
        cmds.setAttr( vectorY_direction + '.input2', 1,1,1 )
    
    cmds.connectAttr( dcmpPoleV + '.ot', vectorY_direction + '.input1' )
        
    vectorY = cmds.createNode( 'vectorProduct' ); cmds.setAttr( vectorY + '.op', 2 )
    vectorZ = cmds.createNode( 'vectorProduct' ); cmds.setAttr( vectorZ + '.op', 2 )
    cmds.connectAttr( dcmpEnd + '.ot', vectorX + '.input1' )
    cmds.connectAttr( vectorX   + '.output', vectorY+'.input1' )
    cmds.connectAttr( vectorY_direction + '.output', vectorY+'.input2' )
    cmds.connectAttr( vectorX   + '.output', vectorZ+'.input1' )
    cmds.connectAttr( vectorY + '.output', vectorZ+'.input2' )
    
    ffm = cmds.createNode( 'fourByFourMatrix' )
    cmds.connectAttr( vectorX + '.outputX', ffm + '.i00' )
    cmds.connectAttr( vectorX + '.outputY', ffm + '.i01' )
    cmds.connectAttr( vectorX + '.outputZ', ffm + '.i02' )
    cmds.connectAttr( vectorY + '.outputX', ffm + '.i10' )
    cmds.connectAttr( vectorY + '.outputY', ffm + '.i11' )
    cmds.connectAttr( vectorY + '.outputZ', ffm + '.i12' )
    cmds.connectAttr( vectorZ + '.outputX', ffm + '.i20' )
    cmds.connectAttr( vectorZ + '.outputY', ffm + '.i21' )
    cmds.connectAttr( vectorZ + '.outputZ', ffm + '.i22' )
    cmds.connectAttr( dcmpBase + '.otx', ffm + '.i30' )
    cmds.connectAttr( dcmpBase + '.oty', ffm + '.i31' )
    cmds.connectAttr( dcmpBase + '.otz', ffm + '.i32' )
    
    mm = cmds.createNode( 'multMatrix' )
    dcmp = cmds.createNode( 'decomposeMatrix' )
    cmds.connectAttr( ffm + '.output', mm + '.i[0]' )
    cmds.connectAttr( stdBase + '.wim', mm + '.i[1]' )
    cmds.connectAttr( mm + '.o', dcmp + '.imat' )
    
    stdLookBase = dag.putChild( stdBase )
    stdLookBase = name.replaceNameToTarget( stdBase, stdLookBase, 'Help_', 'HelpLookBase_' )
    cmds.connectAttr( dcmp + '.ot', stdLookBase + '.t' )
    cmds.connectAttr( dcmp + '.or', stdLookBase + '.r' )
    
    return stdLookBase



def makeIkMiddle( stdMiddle, ikLookBase ):
    
    dcmpMiddle = connect.getLocalDcmp( stdMiddle, ikLookBase )
    ikMiddle = dag.putChild( ikLookBase )
    ikMiddle = name.replaceNameToTarget( stdMiddle, ikMiddle, 'Help_', 'HelpIkMiddle_' )
    cmds.connectAttr( dcmpMiddle + '.otx', ikMiddle + '.tx' )
    cmds.connectAttr( dcmpMiddle + '.otz', ikMiddle + '.tz' )
    return ikMiddle



def makeIkOffset( stdMiddle, ikMiddle ):
    
    dcmp = connect.getLocalDcmp( stdMiddle, ikMiddle )
    ikOffset = dag.putChild( ikMiddle, 'joint' )
    ikOffset = name.replaceNameToTarget( ikMiddle, ikOffset,'IkMiddle_', 'IkOffset_' )
    cmds.connectAttr( dcmp + '.ot', ikOffset + '.t' )
    return ikOffset



def makeIkStdJnts( stds, minusX = False, minusY= False ):
    
    stdBase   = putStdJntHelp(stds[0])
    stdMiddle = putStdJntHelp(stds[1])
    stdEnd    = putStdJntHelp(stds[2])
    stdPoleV  = putStdJntHelp(stds[3])

    ikLookBase = makeIkLookBase( stdBase, stdMiddle, stdEnd, stdPoleV, minusX, minusY )
    ikMiddle   = makeIkMiddle( stdMiddle, ikLookBase )
    
    baseLookAt = makeLookAtChild( ikMiddle, ikLookBase )
    middleLookAt = makeLookAtChild( stdEnd, ikMiddle )

    stdJntBase = putStdJnt( stds[0] )
    stdJntMiddle = putStdJnt( stds[1] )
    stdJntEnd = putStdJnt( stds[2] )
    
    connect.constraint_parent( baseLookAt, stdJntBase )
    connect.constraint_parent( middleLookAt, stdJntMiddle )
    connect.constraint_parent( stdEnd, stdJntEnd )

    dag.parentByOlder( [stdJntEnd, stdJntMiddle, stdJntBase ] )

    transform.setJointOrientZero([stdJntEnd, stdJntMiddle, stdJntBase ])
    dag.parentByOlder([stdEnd, stdMiddle, stdBase ])
    cmds.parent( stdPoleV, stdBase )
    
    makeIkOffset( stdMiddle, stdJntMiddle )
    
    return stdBase, stdJntBase
    

#---------------------------------------------------------------



def makeFootStdJnts( stds ):
    
    stdBase   = getStdJntHelp( stds[0] )
    stdMiddle = getStdJntHelp( stds[1] )
    stdEnd    = getStdJntHelp( stds[2] )
    
    lookAtBase = makeLookAtChild( stdMiddle, stdBase )
    lookAtMiddle = makeLookAtChild( stdEnd, stdMiddle )
    
    stdJntBase = putStdJnt( stds[0] )
    stdJntMiddle = putStdJnt( stds[1] )
    stdJntEnd = putStdJnt( stds[2] )
    
    connect.constraint_parent( lookAtBase, stdJntBase )
    connect.constraint_parent( lookAtMiddle, stdJntMiddle )
    connect.constraint_point( stdEnd, stdJntEnd )

    stdJntBase = name.replaceNameToTarget(stds[0], stdJntBase, 'Std_', 'StdFootJnt_' )
    
    dag.parentByOlder( [stdJntEnd, stdJntMiddle, stdJntBase ] )
    dag.parentByOlder( [stdEnd, stdMiddle, stdBase ] )
    transform.setJointOrientZero([stdJntEnd, stdJntMiddle, stdJntBase ])
    


#-----------------------------------------------------------------------



class MakeRigBase:
    
    
    def fixConnectBaseGrp(self, connector ):
        
        cons= cmds.listConnections( self.baseGrp, s=1, d=0, type='decomposeMatrix' )
        cmds.delete( cons )
        connect.constraint_parent( connector, self.baseGrp )
    
    
    def makeParentGroup(self, stdJnt, addName ):
        
        baseGrp = cmds.createNode( 'transform', n='Grp_base_%s' % addName )
        connect.constraint_parent( stdJnt, baseGrp )
        return baseGrp

    
    def makeSkinJoints(self):
        pass




class MakeBodyRig(MakeRigBase):
    
    def __init__(self, *stdJnts ):
        
        self.stdChest  = stdJnts[3]
        self.stdBack02 = stdJnts[2]
        self.stdBack01 = stdJnts[1]
        self.stdRoot   = stdJnts[0]
    
        self.ctlRoot    = self.createRootCtl()
        self.ctlPervis, self.pervPointer = self.createPervisRotater()
        self.ctlBodyRot1, self.ctlBodyRot2 = self.createBodyRotator()
        self.ctlChest   = self.createChestCtl()
        self.ctlWaist, self.pointerChest, self.pointerHip = self.createWaistCtl()
        self.ctlHip     = self.createHipCtl()
        
        self.curve    = self.createBindedCurve()
        self.topRigJoint = self.createSplineJoints()
        
        self.baseGrp  = cmds.listRelatives( self.ctlRoot, p=1, f=1 )[0]



    def createRootCtl(self):
        
        ctlRoot, pCtlRoot = controller.getCircleController([0,1,0], 1.5, 'Ctl_Root' )
        connect.translate( self.stdRoot, pCtlRoot )
        connect.rotate( self.stdRoot, pCtlRoot )
        return ctlRoot
    


    def createPervisRotater(self):
        
        ctlPervis, pCtlPervis = controller.getCircleController( [0,0,1], 1.5, 'Ctl_PervisRotator' )
        
        fnCtlPervis = OpenMaya.MFnDagNode( sgbase.getDagPath( ctlPervis ) )
        pCtlPervis = cmds.parent( pCtlPervis, self.ctlRoot )
        transform.setToDefault( pCtlPervis )
        
        pervisWaistPointer = cmds.createNode( 'transform', n='pointer_to_waist' )
        connect.translate( self.stdBack01, pervisWaistPointer )
        connect.rotate( self.stdBack01, pervisWaistPointer )
        pervisWaistPointer = cmds.parent( pervisWaistPointer, ctlPervis )[0]
        
        return fnCtlPervis.partialPathName(), pervisWaistPointer
    


    def createBodyRotator(self):
        
        ctlRotator, pCtlRotator = controller.getCircleController( [0,1,0], 5, 'Ctl_BodyRotator1' )
        ctlRotator2, pCtlRotator2 = controller.getCircleController( [0,1,0], 5, 'Ctl_BodyRotator2' )
        
        connect.constraint_point( self.pervPointer, pCtlRotator )
        cmds.connectAttr( self.stdBack01 + '.r', pCtlRotator + '.r' )
        cmds.connectAttr( self.stdBack02 + '.t', pCtlRotator2 + '.t' )
        cmds.connectAttr( self.stdBack02 + '.r', pCtlRotator2 + '.r' )
        
        fnCtlRotator = OpenMaya.MFnDagNode( sgbase.getDagPath( ctlRotator ) )
        pCtlRotator = cmds.parent( pCtlRotator, self.ctlRoot )
        transform.setToDefault( pCtlRotator )
        ctlRotator = fnCtlRotator.partialPathName()
        
        fnCtlRotator2 = OpenMaya.MFnDagNode( sgbase.getDagPath( ctlRotator2 ) )
        pCtlRotator2 = cmds.parent( pCtlRotator2, ctlRotator )
        transform.setToDefault( pCtlRotator2 )
        ctlRotator2 = fnCtlRotator2.partialPathName()
        
        return ctlRotator, ctlRotator2
    


    def createWaistCtl(self):
        
        ctlWaist, pCtlWaist = controller.getCircleController( [0,1,0], 2, 'Ctl_Waist' )
        ctlWaist, waistOffset = dag.makeParent( ctlWaist )[0]
        
        fnCtlWaist = OpenMaya.MFnDagNode( sgbase.getDagPath( ctlWaist ) )
        waistOffset = cmds.rename( waistOffset, 'OffsetCtl_Waist' )
        
        cmds.connectAttr( self.stdBack01+'.r', waistOffset + '.r' )
        
        pCtlWaist = cmds.parent( pCtlWaist, self.ctlRoot )[0]
        transform.setToDefault( pCtlWaist )
        ctlWaist = fnCtlWaist.partialPathName()
        
        halfMtx = connect.getLocalHalfMatrixNode( self.ctlBodyRot1 )
        halfMtxDcmp = connect.getDcmp( halfMtx )
        cmds.connectAttr( halfMtxDcmp + '.or', pCtlWaist + '.r' )
        attribute.addAttr( self.ctlBodyRot1, ln='blend', min=0, max=1, dv=0.3, k=1 )
        cmds.connectAttr( self.ctlBodyRot1 + '.blend', halfMtx + '.blend' )
        
        pervPointerDcmp = connect.getLocalDcmp( self.pervPointer, self.ctlRoot )
        cmds.connectAttr( pervPointerDcmp + '.ot', pCtlWaist + '.t' )
        
        dcmp = connect.getLocalDcmp( self.ctlPervis, waistOffset )
        pointerHip = dag.makeChild( ctlWaist, 'hipPointer' )
        cmds.connectAttr( dcmp + '.ot', pointerHip + '.t' )
        cmds.connectAttr( dcmp + '.or', pointerHip + '.r' )
        
        pointerChestLower = dag.makeChild( waistOffset, 'pointer_chestLower' )
        pointerChest = dag.makeChild( pointerChestLower, 'pointer_chest' )
        
        connect.constraint_point( self.ctlBodyRot2, pointerChestLower )
        connect.constraint_point( dag.getParent( self.ctlChest ), pointerChest )

        return fnCtlWaist.partialPathName(), pointerChest, pointerHip



    def createChestCtl(self):
        
        pointerChestCtl = dag.makeChild( self.ctlBodyRot2, 'pointerChest' )
        cmds.connectAttr( self.stdChest + '.t', pointerChestCtl + '.t' )
        
        ctlChest, pCtlChest = controller.getCircleController( [0,0,1], 1, 'Ctl_Chest' )
        fnCtlChest = OpenMaya.MFnDagNode( sgbase.getDagPath( ctlChest ) )
        pCtlChest = cmds.parent( pCtlChest, self.ctlRoot )[0]
        ctlChest = fnCtlChest.partialPathName()
        
        connect.constraint_parent( pointerChestCtl, pCtlChest )
        
        return ctlChest
    


    def createHipCtl(self):
        
        ctlHip, pCtlHip = controller.getCircleController( [0,1,0], 2, 'Ctl_Hip' )
        fnCtlHip = OpenMaya.MFnDagNode( sgbase.getDagPath( ctlHip ) )
        pCtlHip = cmds.parent( pCtlHip, self.ctlRoot )[0]
        ctlHip = fnCtlHip.partialPathName()
        connect.constraint_parent( self.pointerHip, pCtlHip )
        
        return ctlHip
    
    
    
    def createBindedCurve(self):
        
        bindedGrp = dag.makeChild( self.ctlRoot, 'bindedTransformGrp' )
        
        bindPre01 = dag.getParent( self.ctlHip )
        bindPre02 = dag.getParent( self.ctlChest )
        
        bind01 = dag.makeBrother( self.ctlHip, 'back_bind01' )
        bind02 = dag.makeBrother( self.ctlChest, 'back_bind02' )
        cmds.connectAttr( self.ctlHip + '.t', bind01+'.t' )
        cmds.connectAttr( self.ctlChest + '.t', bind02+'.t' )
        
        mmBind1 = cmds.createNode( 'multMatrix' )
        mmBind2 = cmds.createNode( 'multMatrix' )
        
        cmds.connectAttr( bindPre01 + '.wim', mmBind1 + '.i[0]' )
        cmds.connectAttr( bind01 + '.wm', mmBind1 + '.i[1]' )
        cmds.connectAttr( bindPre02 + '.wim', mmBind2 + '.i[0]' )
        cmds.connectAttr( bind02 + '.wm', mmBind2 + '.i[1]' )
        
        wtAddMtxs = []
        for i in range( 4 ):
            wtAddMtx = cmds.createNode( 'wtAddMatrix' )
            cmds.connectAttr( mmBind1 + '.o', wtAddMtx + '.i[0].m' )
            cmds.connectAttr( mmBind2 + '.o', wtAddMtx + '.i[1].m' )
            weight = .333333 * i
            cmds.setAttr( wtAddMtx + '.i[0].w', 1-weight )
            cmds.setAttr( wtAddMtx + '.i[1].w', weight )
            wtAddMtxs.append( wtAddMtx )
            
        pointsObjs = [ self.pointerHip, dag.getParent(self.ctlWaist), dag.getParent(self.pointerChest), self.pointerChest ]
        
        curve = cmds.curve( d=1, p=[ [0,0,0] for i in range( 4 )] )
        curveShape = dag.getShape( curve )
        
        for i in range( 4 ):
            mm = cmds.createNode( 'multMatrix' )
            cmds.connectAttr( pointsObjs[i]+'.wm', mm + '.i[0]' )
            cmds.connectAttr( wtAddMtxs[i] + '.o', mm + '.i[1]' )
            cmds.connectAttr( self.ctlRoot + '.wim', mm + '.i[2]' )
            dcmp = connect.getDcmp( mm )
            cmds.connectAttr( dcmp + '.ot', curveShape + '.controlPoints[%d]' % i )
            
        curve = cmds.parent( curve, bindedGrp )[0]
        transform.setToDefault( curve )
        cmds.setAttr( curve + '.v', 0 )
        
        return curve
    


    def createSplineJoints(self):
        
        topJoint, ikHandle = ik.createIkSplineHandleJoints( self.curve, self.ctlRoot )
        cmds.connectAttr( self.ctlChest + '.wm', ikHandle +'.dWorldUpMatrixEnd' )
        cmds.connectAttr( self.ctlHip   + '.wm', ikHandle +'.dWorldUpMatrix' )

        cmds.setAttr( ikHandle + '.dTwistControlEnable', 1 )
        cmds.setAttr( ikHandle + '.dWorldUpAxis', 3 )
        cmds.setAttr( ikHandle + '.dWorldUpVectorEnd', 0,0,1 )
        cmds.setAttr( ikHandle + '.dWorldUpVector', 0,0,1 )
        cmds.setAttr( ikHandle + '.dWorldUpType', 4 )
        
        jnt = cmds.createNode( 'joint', n='RigJnt_Root' )
        jnt = cmds.parent( jnt, self.ctlRoot )[0]
        connect.constraint_parent( self.ctlHip, jnt )
        topJoint = cmds.parent( topJoint, jnt )[0]
        
        children = cmds.listRelatives( topJoint, c=1, ad=1, type='joint' )
        connect.constraint_orient( self.ctlChest, children[0] )
        
        splineJoints = cmds.listRelatives( jnt, c=1, ad=1, f=1, type='joint' )
        splineJoints.append( jnt )
        splineJoints.reverse()
        fnSplineJoints = []
        for i in range( len( splineJoints ) ):
            fnSplineJoints.append( OpenMaya.MFnDagNode( sgbase.getDagPath(splineJoints[i]) ) )
        
        for i in range( len( fnSplineJoints ) ):
            cmds.rename( fnSplineJoints[i].partialPathName(), 'RigJnt_Spline%02d' % i )
        cmds.setAttr( ikHandle + '.v', 0 )
        
        return fnSplineJoints[0].partialPathName()
    


    def addHipConnector(self, stdHipJnt_L_, stdHipJnt_R_ ):
        
        rootChild_L_ = dag.makeChild( self.ctlRoot, 'pointer_hip_L_inRoot' )
        rootChild_R_ = dag.makeChild( self.ctlRoot, 'pointer_hip_R_inRoot' )
        hipChild_L_  = dag.makeChild( self.ctlHip, 'pointer_hip_L_inHip' )
        hipChild_R_  = dag.makeChild( self.ctlHip, 'pointer_hip_R_inHip' )
        
        cmds.connectAttr( stdHipJnt_L_+ '.t', rootChild_L_ + '.t' )
        cmds.connectAttr( stdHipJnt_R_+ '.t', rootChild_R_ + '.t' )
        cmds.connectAttr( stdHipJnt_L_+ '.t', hipChild_L_ + '.t' )
        cmds.connectAttr( stdHipJnt_R_+ '.t', hipChild_R_ + '.t' )
        cmds.connectAttr( stdHipJnt_L_+ '.r', rootChild_L_ + '.r' )
        cmds.connectAttr( stdHipJnt_R_+ '.r', rootChild_R_ + '.r' )
        cmds.connectAttr( stdHipJnt_L_+ '.r', hipChild_L_ + '.r' )
        cmds.connectAttr( stdHipJnt_R_+ '.r', hipChild_R_ + '.r' )
        
        connector_L_ = dag.makeChild( self.topRigJoint, 'connector_hip_L_' )
        connector_R_ = dag.makeChild( self.topRigJoint, 'connector_hip_R_' )
        attribute.addAttr( connector_L_, ln='connector', at='message' )
        attribute.addAttr( connector_R_, ln='connector', at='message' )
        
        connect.constraint_orient( rootChild_L_, connector_L_ )
        connect.constraint_orient( rootChild_R_, connector_R_ )
        connect.constraint_point( hipChild_L_, connector_L_ )
        connect.constraint_point( hipChild_R_, connector_R_ )
        
        self.hipConnector_L_ = connector_L_
        self.hipConnector_R_ = connector_R_
        
        hipConnectRotator = dag.makeChild( self.ctlRoot, 'rotator_hipConnector' )
        localDcmp = connect.getLocalDcmp( self.ctlHip, self.ctlRoot )
        yCompose = cmds.createNode( 'composeMatrix' ); cmds.setAttr( yCompose + '.ity', 1 )
        compose = cmds.createNode( 'composeMatrix' ); cmds.connectAttr( localDcmp + '.or', compose + '.ir' )
        mm = cmds.createNode( 'multMatrix' ); cmds.connectAttr( yCompose + '.outputMatrix', mm + '.i[0]' ); cmds.connectAttr( compose + '.outputMatrix', mm+ '.i[1]' )
        dcmp = connect.getDcmp( mm )
        angle = cmds.createNode( 'angleBetween' ); cmds.setAttr( angle + '.vector1', 0,1,0 ); cmds.connectAttr( dcmp + '.ot', angle + '.vector2' )
        composeAngle = cmds.createNode( 'composeMatrix'); cmds.connectAttr( angle + '.euler', composeAngle + '.ir' )
        invMtx = cmds.createNode( 'inverseMatrix' )
        mmForHip = cmds.createNode( 'multMatrix' ); cmds.connectAttr( compose + '.outputMatrix', mmForHip + '.i[0]' ); cmds.connectAttr( invMtx + '.outputMatrix', mmForHip + '.i[1]' )
        dcmpHipConnector = connect.getDcmp( mmForHip )
        cmds.connectAttr( dcmpHipConnector + '.or', hipConnectRotator + '.r' )
        
        cmds.parent( rootChild_L_, rootChild_R_, hipConnectRotator )
        
        return connector_L_, connector_R_
    
    
    def _getChestInverseMatrix(self):
        
        dcmpTrans = connect.getDcmp( self.stdChest )
        dcmpRotate = connect.getDcmp( self.stdBack02 )
        compose = cmds.createNode( 'composeMatrix' )
        cmds.connectAttr( dcmpTrans  + '.ot', compose + '.it' )
        cmds.connectAttr( dcmpRotate + '.or', compose + '.ir' )
        invMtx = cmds.createNode( 'inverseMatrix' )
        cmds.connectAttr( compose + '.outputMatrix', invMtx + '.inputMatrix' )
        return invMtx


    def addCollarConnector(self, stdCollarJnt_L_, stdCollarJnt_R_ ):
        
        endJnt = cmds.listRelatives( self.topRigJoint, c=1, ad=1, type='joint', f=1 )[0]
                
        child_L_ = dag.makeChild( endJnt, 'connector_collar_L_' )
        child_R_ = dag.makeChild( endJnt, 'connector_collar_R_' )
        attribute.addAttr( child_L_, ln='connector', at='message' )
        attribute.addAttr( child_R_, ln='connector', at='message' )
        
        invMtx = self._getChestInverseMatrix()
        mm_L_ = cmds.createNode( 'multMatrix' )
        mm_R_ = cmds.createNode( 'multMatrix' )
        cmds.connectAttr( stdCollarJnt_L_ + '.wm', mm_L_ + '.i[0]' )
        cmds.connectAttr( stdCollarJnt_R_ + '.wm', mm_R_ + '.i[0]' )
        cmds.connectAttr( invMtx + '.outputMatrix', mm_L_ + '.i[1]' )
        cmds.connectAttr( invMtx + '.outputMatrix', mm_R_ + '.i[1]' )
        dcmp_L_ = connect.getDcmp( mm_L_ )
        dcmp_R_ = connect.getDcmp( mm_R_ )
        
        cmds.connectAttr( dcmp_L_ + '.ot', child_L_ + '.t' )
        cmds.connectAttr( dcmp_L_ + '.or', child_L_ + '.r' )
        cmds.connectAttr( dcmp_R_ + '.ot', child_R_ + '.t' )
        cmds.connectAttr( dcmp_R_ + '.or', child_R_ + '.r' )
        
        self.connectorCollar_L_ = child_L_
        self.connectorCollar_R_ = child_R_
        
        return child_L_, child_R_
    


    def addNeckConnector(self, stdJntNeck ):
        
        endJnt = cmds.listRelatives( self.topRigJoint, c=1, ad=1, type='joint', f=1 )[0]
        connector = dag.makeChild( endJnt, 'connector_neck' )
        attribute.addAttr( connector, ln='connector', at='message' )
        
        invMtx = self._getChestInverseMatrix()
        mm = cmds.createNode( 'multMatrix' )
        cmds.connectAttr( stdJntNeck+ '.wm', mm+'.i[0]' )
        cmds.connectAttr( invMtx + '.outputMatrix', mm + '.i[1]' )
        dcmp = connect.getDcmp( mm )
        cmds.connectAttr( dcmp + '.ot', connector + '.t' )
        cmds.connectAttr( dcmp + '.or', connector + '.r' )
        
        self.connectorNeck = connector
        return self.connectorNeck
        
    
        


class MakeArmRig(MakeRigBase):
    
    def __init__(self, *stdJnts, **options ):

        self.stdStart  = stdJnts[0]
        self.stdMiddle = stdJnts[1]
        self.stdEnd    = stdJnts[2]
        self.stdOffset = stdJnts[3]
        self.stdPoleV  = stdJnts[4]
        
        self.name = value.getValueFromDict( options, 'name' )
        self.side = value.getValueFromDict( options, 'side' )
        self.sep  = value.getValueFromDict( options, 'sep' )
        
        self.baseGrp = self.makeParentGroup( self.stdStart, '%s_%s_' %( self.name, self.side ) )
        
        self.fks = self.makeFKs()
        self.iks = self.makeIKs()
        self.blendedTop   = self.makeBlendedJoints()
        self.createCurve()
        self.topRigJoint = self.createSplineJoints( self.sep )
        self.setVisConnections()
        self.connector = cmds.listRelatives( self.blendedTop, c=1, ad=1, type='joint' )[0]



    def makeFKs( self ):
        
        ctlFirst  = cmds.circle( ch=1, o=1, nr = [1,0,0] )[0]
        ctlSecond = cmds.duplicate( ctlFirst )[0]
        ctlThird  = cmds.duplicate( ctlFirst )[0]
        
        ctlFirst  = name.replaceNameToTarget( self.stdStart, ctlFirst, 'StdJnt_', 'Ctl_FK_' )
        ctlSecond = name.replaceNameToTarget( self.stdMiddle, ctlSecond, 'StdJnt_', 'Ctl_FK_' )
        ctlThird  = name.replaceNameToTarget( self.stdEnd, ctlThird, 'StdJnt_', 'Ctl_FK_' )
        
        dag.makeParent( [ctlFirst,ctlSecond,ctlThird])
        
        ctlFirstP = cmds.listRelatives( ctlFirst, p=1, f=1 )[0]
        ctlSecondP = cmds.listRelatives( ctlSecond, p=1, f=1 )[0]
        ctlThirdP = cmds.listRelatives( ctlThird, p=1, f=1 )[0]
        
        cmds.connectAttr( self.stdMiddle + '.t', ctlSecondP + '.t' )
        cmds.connectAttr( self.stdMiddle + '.r', ctlSecondP + '.r' )
        
        cmds.connectAttr( self.stdEnd + '.t', ctlThirdP + '.t' )
        cmds.connectAttr( self.stdEnd + '.r', ctlThirdP + '.r' )
        
        rigJntFirst  = cmds.createNode( 'joint' )
        rigJntSecond = cmds.joint()
        rigJntThird  = cmds.joint()
        
        rigJntFirst  = name.replaceNameToTarget( self.stdStart,  rigJntFirst,  'StdJnt_', 'JntFk_' )
        rigJntSecond = name.replaceNameToTarget( self.stdMiddle, rigJntSecond, 'StdJnt_', 'JntFk_' )
        rigJntThird  = name.replaceNameToTarget( self.stdEnd,  rigJntThird,  'StdJnt_', 'JntFk_' )
    
        connect.constraint_parent( ctlFirst,  rigJntFirst )
        connect.constraint_parent( ctlSecond, rigJntSecond )
        connect.constraint_parent( ctlThird,  rigJntThird )
        self.ctlFkFirst = ctlFirst
        self.ctlFkSecond = ctlSecond
        self.ctlFkThird = ctlThird
        
        ctlFirstP  = cmds.parent( ctlFirstP, self.baseGrp )
        ctlSecondP = cmds.parent( ctlSecondP, ctlFirst )
        ctlThirdP  = cmds.parent( ctlThirdP, ctlSecond )
        
        rigJntFirst = cmds.parent( rigJntFirst, self.baseGrp )[0]
        
        transform.setToDefault( ctlFirstP )
        transform.setJointOrientZero( rigJntFirst )
        
        fkGrp = cmds.group( rigJntFirst, ctlFirstP, n='fkGrp_%s_%s_' %( self.name, self.side ) )
        cmds.setAttr( rigJntFirst + '.v', 0 )
        
        return rigJntFirst, rigJntSecond, rigJntThird, fkGrp
    
    
    
    def makeIKs( self ):
        
        dcmpThird = connect.getLocalDcmp( self.stdEnd, self.stdStart )
        
        ctlFirst  = cmds.circle( ch=1, o=1, nr = [1,0,0] )[0]
        ctlFirst = cmds.rename( ctlFirst, 'Ctl_%sIK_%s_' %( self.name, self.side ) )
        dag.makeParent( ctlFirst )
        ctlFirstP = cmds.listRelatives( ctlFirst, p=1, f=1 )[0]
        fnCtlFirst = dag.getDagNode( ctlFirst )
        
        cmds.connectAttr( dcmpThird + '.ot', ctlFirstP + '.t' )
        cmds.connectAttr( dcmpThird + '.or', ctlFirstP + '.r' )
        
        ctlFirstP = cmds.parent( ctlFirstP, self.baseGrp )[0]
        transform.setToDefault( ctlFirstP )
        
        rigJntFirst = cmds.createNode( 'joint' )
        rigJntSecond = cmds.joint()
        rigJntThird  = cmds.joint()
        
        rigJntFirst = name.replaceNameToTarget( self.stdStart, rigJntFirst, 'StdJnt_', 'JntIk_' )
        rigJntSecond = name.replaceNameToTarget( self.stdMiddle, rigJntSecond, 'StdJnt_', 'JntIk_' )
        rigJntThird = name.replaceNameToTarget( self.stdEnd, rigJntThird, 'StdJnt_', 'JntIk_' )
        
        rigJntFirst = cmds.parent( rigJntFirst, self.baseGrp )[0]
        transform.setToDefault( rigJntFirst )
        
        cmds.connectAttr( self.stdMiddle + '.tx', rigJntSecond + '.tx' )
        cmds.connectAttr( self.stdEnd + '.tx', rigJntThird + '.tx' )
        angleNode = cmds.createNode( 'angleBetween' )
        cmds.connectAttr( self.stdPoleV + '.t', angleNode + '.vector1' )
        cmds.setAttr( angleNode + '.vector2', 1,0,0 )
        cmds.connectAttr( angleNode + '.eulerY', rigJntSecond + '.pay' )
        if self.side == 'R':
            md = cmds.createNode( 'multDoubleLinear' )
            cmds.connectAttr( angleNode + '.eulerY', md + '.input1' )
            cmds.setAttr( md + '.input2', -1 )
            cmds.connectAttr( md + '.output', rigJntSecond + '.pay', f=1 )
        
        handle = cmds.ikHandle( sj=rigJntFirst, ee=rigJntThird, sol='ikRPsolver' )[0]
        connect.constraint_point( ctlFirst, handle )
        
        ctlPoleV = controller.getPoleVectorController( radius = 0.3 )
        ctlPoleV = cmds.rename( ctlPoleV, 'Ctl_%sPoleVIK_%s_' %( self.name, self.side ) )
        dag.makeParent( ctlPoleV )
        ctlPoleVP = cmds.listRelatives( ctlPoleV, p=1, f=1 )[0]
        fnCtlPoleV = dag.getDagNode( ctlPoleV )
        
        dcmpPoleV = connect.getLocalDcmp( self.stdPoleV, self.stdStart )
        
        cmds.connectAttr( dcmpPoleV + '.ot', ctlPoleVP + '.t' )
        cmds.connectAttr( dcmpPoleV + '.or', ctlPoleVP + '.r' )
        
        ctlPoleVP = cmds.parent( ctlPoleVP, self.baseGrp )[0]
        
        dcmpPoleV = connect.getLocalDcmp( ctlPoleV, self.baseGrp )
        cmds.connectAttr( dcmpPoleV + '.ot', handle + '.poleVector' )
        handle = cmds.parent( handle, self.baseGrp )[0]
        
        connect.constraint_orient( ctlFirst, rigJntThird )
        
        ikGrp = cmds.group( rigJntFirst, ctlFirstP, ctlPoleVP, handle, n='ikGrp_%s_%s_' %( self.name, self.side ) )
        cmds.setAttr( rigJntFirst + '.v', 0 )
        cmds.setAttr( handle + '.v', 0 )
        
    
        self.ctlIk      = fnCtlFirst.partialPathName()
        self.ctlIkPoleV = fnCtlPoleV.partialPathName()
        self.ikGrp = ikGrp
        self.ikHandle = handle
    
        return rigJntFirst, rigJntSecond, rigJntThird, ikGrp
    



    def fixPoleVector(self):
        
        
        ctlPoleVP = cmds.listRelatives( self.ctlIkPoleV, p=1, f=1 )[0]
        lookAtPoleV = connect.makeLookAtChild( self.ikGrp, self.ctlIk, 'lookAt_PoleV_%s_' % self.side )
        ctlPoleVP = cmds.parent( ctlPoleVP, lookAtPoleV )[0]
        lookDcmp = connect.getLocalDcmp( self.stdEnd, self.stdStart )
        angleNode = cmds.createNode( 'angleBetween' )
        composeMatrix = cmds.createNode( 'composeMatrix' )
        cmds.setAttr( angleNode + '.vector1', 1,0,0 )
        if self.side == 'R': cmds.setAttr( angleNode + '.vector1', -1,0,0 )
        cmds.connectAttr( lookDcmp + '.ot', angleNode + '.vector2' )
        cmds.connectAttr( angleNode + '.euler', composeMatrix + '.inputRotate' )
        
        mm = cmds.createNode( 'multMatrix' )
        invMtx = cmds.createNode( 'inverseMatrix' )
        cmds.connectAttr( composeMatrix + '.outputMatrix', mm + '.i[0]')
        cmds.connectAttr( self.stdStart + '.wm', mm + '.i[1]')
        cmds.connectAttr( mm + '.o', invMtx + '.inputMatrix' )
        
        mm2 = cmds.createNode( 'multMatrix' )
        cmds.connectAttr( self.stdPoleV + '.wm', mm2 + '.i[0]' )
        cmds.connectAttr( invMtx + '.outputMatrix', mm2 + '.i[1]' )
        dcmp = connect.getDcmp( mm2 )
        
        cmds.connectAttr( dcmp + '.ot', ctlPoleVP + '.t', f=1 )
        cmds.connectAttr( dcmp + '.or', ctlPoleVP + '.r', f=1 )
        
        
        



    def makeBlendedJoints(self):
        
        ctlSwitch, pCtlSwitch = controller.getCircleController( [0,0,1], 0.5, 'Ctl_switch_%s_%s_' %( self.name, self.side ) )
        attribute.addAttr( ctlSwitch, ln='fkSwitch', min=0, max=1, dv=0, k=1 )
        
        cmds.select( self.baseGrp )
        blendJntFirst  = cmds.joint()
        blendJntSecond = cmds.joint()
        blendJntThird  = cmds.joint()
        
        blendJntFirst = name.replaceNameToTarget( self.stdStart, blendJntFirst, 'StdJnt_', 'Jnt_' )
        blendJntSecond = name.replaceNameToTarget( self.stdMiddle, blendJntSecond, 'StdJnt_', 'Jnt_' )
        blendJntThird = name.replaceNameToTarget( self.stdEnd, blendJntThird, 'StdJnt_', 'Jnt_' )
        attribute.addAttr( blendJntThird, ln='connector', at='message' )
        
        blendJnts = [blendJntFirst, blendJntSecond, blendJntThird]
        
        for i in range( 3 ):
            blendTwoMatrixNode = connect.getBlendTwoMatrixNode( self.iks[i], self.fks[i], None, True )
            dcmp = connect.getDcmp( blendTwoMatrixNode )
            cmds.connectAttr( dcmp + '.ot', blendJnts[i] + '.t' )
            cmds.connectAttr( dcmp + '.or', blendJnts[i] + '.r' )
            
            cmds.connectAttr( ctlSwitch + '.fkSwitch', blendTwoMatrixNode + '.blend' )
        
        fnCtlSwitch = dag.getDagNode( ctlSwitch )
        connect.constraint_parent( blendJntThird, pCtlSwitch )
        pCtlSwitch = cmds.parent( pCtlSwitch, self.baseGrp )[0]
        self.ctlSwitch = fnCtlSwitch.partialPathName()
        self.blendJntFirst = blendJntFirst
        self.blendJntSecond = blendJntSecond
        self.blendJntThird = blendJntThird
        cmds.select( self.blendJntSecond )
        self.blendJntOffset = cmds.joint( n='Jnt_%s_%s_offset' %( self.name, self.side ) )
        cmds.connectAttr( self.stdOffset + '.t', self.blendJntOffset + '.t' )
        cmds.setAttr( blendJntFirst + '.v', 0 )
        
        return blendJntFirst



    def setVisConnections(self):
        
        attribute.addAttr( self.ctlSwitch, ln='fkVis', dv=0, cb=1, min=0, max=1, at='long' )
        attribute.addAttr( self.ctlSwitch, ln='ikVis', dv=1, cb=1, min=0, max=1, at='long' )
        
        cmds.connectAttr( self.ctlSwitch + '.fkVis', self.fks[-1] + '.v' )
        cmds.connectAttr( self.ctlSwitch + '.ikVis', self.iks[-1] + '.v' )
    
    
    
    def createCurve(self):
        
        dcmpPoint1 = connect.getLocalDcmp( self.blendJntFirst, self.baseGrp )
        dcmpPoint2 = connect.getLocalDcmp( self.blendJntOffset, self.baseGrp )
        dcmpPoint3 = connect.getLocalDcmp( self.blendJntThird, self.baseGrp )
        
        curve1 = cmds.curve( p=[[0,0,0],[0,0,0]], d=1, n='CurveUpper_%s_%s' %( self.name, self.side ) )
        curve2 = cmds.curve( p=[[0,0,0],[0,0,0]], d=1, n='CurveLower_%s_%s' %( self.name, self.side ) )
        curveShape1 = cmds.listRelatives( curve1, s=1, f=1 )[0]
        curveShape2 = cmds.listRelatives( curve2, s=1, f=1 )[0]
        
        cmds.connectAttr( dcmpPoint1 + '.ot', curveShape1 + '.controlPoints[0]' )
        cmds.connectAttr( dcmpPoint2 + '.ot', curveShape1 + '.controlPoints[1]' )
        cmds.connectAttr( dcmpPoint2 + '.ot', curveShape2 + '.controlPoints[0]' )
        cmds.connectAttr( dcmpPoint3 + '.ot', curveShape2 + '.controlPoints[1]' )
        
        curve1 = cmds.parent( curve1, self.baseGrp )[0]
        curve2 = cmds.parent( curve2, self.baseGrp )[0]
        transform.setToDefault( curve1 )
        transform.setToDefault( curve2 )
        
        self.curve1 = curve1
        self.curve2 = curve2
        cmds.setAttr( curve1 + '.v', 0 )
        cmds.setAttr( curve2 + '.v', 0 )


    def createSplineJoints(self, numSep=3 ):

        topJoint1, ikHandle1 = ik.createIkSplineHandleJoints( self.curve1, self.baseGrp, numSep )
        topJoint2, ikHandle2 = ik.createIkSplineHandleJoints( self.curve2, self.baseGrp, numSep )

        cmds.setAttr( ikHandle1 + '.v', 0 )
        cmds.setAttr( ikHandle2 + '.v', 0 )

        joints1 = cmds.listRelatives( topJoint1, c=1, ad=1, f=1, type='joint' )[1:]
        joints1.append( topJoint1 )
        topJoint2 = cmds.parent( topJoint2, joints1[0] )[0]
        joints2 = cmds.listRelatives( topJoint2, c=1, ad=1, f=1, type='joint' )
        joints2.append( topJoint2 )
        
        joints = joints2 + joints1
        joints.reverse()
        
        cmds.setAttr( ikHandle1 + '.dTwistControlEnable', 1 )
        cmds.setAttr( ikHandle1 + '.dWorldUpType', 4 )
        cmds.setAttr( ikHandle2 + '.dTwistControlEnable', 1 )
        cmds.setAttr( ikHandle2 + '.dWorldUpType', 4 )
        
        upObjectArm0 = dag.makeChild( self.baseGrp, 'upObject%s0_%s_' % ( self.name, self.side ) )
        connect.lookAtConnect( self.blendJntSecond, upObjectArm0 )
        
        pLookAtUpObjectArm1 = dag.makeChild( self.blendJntSecond, 'PlookAtUpObject%s1_%s_' % ( self.name, self.side ) )
        lookAtUpObjectArm1  = dag.makeChild( pLookAtUpObjectArm1, 'lookAtUpObject%s1_%s_' % ( self.name, self.side ) )
        upObjectArm1 = dag.makeChild( pLookAtUpObjectArm1, 'upObject%s1_%s_' % ( self.name, self.side ) )
        cmds.connectAttr( self.blendJntThird + '.t', pLookAtUpObjectArm1+'.t' )
        aimTarget = dag.makeChild( self.blendJntThird, 'aimTarget%s1_%s_' % ( self.name, self.side ) )
        cmds.setAttr( aimTarget + '.t', 1,0,0 )
        connect.lookAtConnect( aimTarget, lookAtUpObjectArm1 )
        dcmp = connect.getLocalDcmp( self.blendJntThird, lookAtUpObjectArm1 )
        cmds.connectAttr( dcmp + '.or', upObjectArm1 + '.r' )
        
        cmds.connectAttr( upObjectArm0 + '.worldMatrix', ikHandle1 + '.dWorldUpMatrix' )
        cmds.connectAttr( self.blendJntOffset + '.worldMatrix', ikHandle1 + '.dWorldUpMatrixEnd' )
        cmds.connectAttr( self.blendJntOffset + '.worldMatrix', ikHandle2 + '.dWorldUpMatrix' )
        cmds.connectAttr( upObjectArm1 + '.worldMatrix', ikHandle2 + '.dWorldUpMatrixEnd' )
        
        fnJoints = []
        for joint in joints:
            fnJoint = OpenMaya.MFnDagNode( dag.getDagPath( joint ) )
            fnJoints.append( fnJoint )
        
        self.rigJnts = []
        for i in range( len( fnJoints ) ):
            cmds.rename( fnJoints[i].partialPathName(), 'RigJnt_%s_%s_%d' %( self.name, self.side, i ) )
            self.rigJnts.append( fnJoints[i].partialPathName() )

        connect.constraint_orient( self.blendJntThird, fnJoints[-1].partialPathName() )
        
        return fnJoints[0].partialPathName()
        


    def fixIKCtlOrientation(self, stdJntGrp, ctlWorldGrp ):
        
        multMatrices = cmds.listConnections( self.ctlIk, d=1, s=0, p=1 )

        pCtlIk       = dag.getParent( self.ctlIk )
        pCtlIkTransMtx = connect.getLocalMatrix( self.stdEnd, stdJntGrp )   
        ikGrpWorldCtlLocal = connect.getLocalMatrix( self.ikGrp, ctlWorldGrp )
        dcmpTranslate = connect.getLocalDcmp( pCtlIkTransMtx, ikGrpWorldCtlLocal )
        dcmpRotate    = connect.getLocalDcmp( stdJntGrp, ikGrpWorldCtlLocal )
        cmds.connectAttr( dcmpTranslate+ '.ot', pCtlIk + '.t', f=1 )
        cmds.connectAttr( dcmpRotate+ '.or', pCtlIk + '.r', f=1 )
        
        beforeIkCtl = cmds.rename( self.ctlIk, self.ctlIk + '_before' )
        ctlShape = dag.getShape( beforeIkCtl )
        cmds.select( pCtlIk )
        newCtl = cmds.joint( radius= 0, n= self.ctlIk )
        cmds.parent( ctlShape, newCtl, add=1, shape=1 )
        
        wristLocalMtx = connect.getLocalMatrix( self.stdEnd, stdJntGrp )
        wristDcmp = connect.getDcmp( wristLocalMtx )
        cmds.connectAttr( wristDcmp + '.or', newCtl + '.jo' )
        
        for mm in multMatrices:
            cmds.connectAttr( newCtl + '.wm', mm, f=1 )
        cmds.delete( beforeIkCtl )
    
    
    
    def addFootJointRig(self, footBaseGrp, aimTarget1, aimTarget2, ikConnector, stdFootAnkle, stdFootToe, stdFootToeEnd ):
        
        cons = cmds.listConnections( footBaseGrp, s=1, d=0, c=1, p=1 )
        
        for i in range( 0, len( cons ), 2):
            cmds.disconnectAttr( cons[i+1], cons[i] )
        connect.constraint_parent( self.ctlIk, footBaseGrp )
        
        cons = cmds.listConnections( self.ikHandle + '.t', s=1, d=0, p=1, c=1 )
        cmds.disconnectAttr( cons[1], cons[0] )

        connect.constraint_point( ikConnector, self.ikHandle )
        
        ankleIk = self.iks[2]
        ankleFk = self.fks[2]
        
        cmds.select( ankleIk )
        footIk = cmds.joint( n='JntIk_Foot_%s_' % self.side )
        pToeIk = dag.makeChild( footIk, 'PRigJntIk_toe_%s_' % self.side )
        toeIk  = cmds.joint( n='JntIk_toe_%s_' % self.side )
        toeEndIk = cmds.joint( n='RigJntIk_toeEnd_%s_' % self.side )
        
        cmds.select( ankleFk )
        footFk = cmds.joint( n='JntFk_Foot_%s_' % self.side )
        pToeFk = dag.makeChild( footFk, 'PJntFk_toe_%s_' % self.side )
        toeFk  = cmds.joint( n='JntFk_toe_%s_' % self.side )
        toeEndFk = cmds.joint( n='JntFk_toeEnd_%s_' % self.side )

        cmds.select( self.rigJnts[-1] )
        footBlend = cmds.joint( n='RigJnt_Foot_%s_' % self.side )
        pToeBlend = dag.makeChild( footBlend, 'PRigJnt_toe_%s_' % self.side )
        toeBlend  = cmds.joint( n='RigJnt_toe_%s_' % self.side )
        toeEndBlend = cmds.joint( n='RigJnt_toeEnd_%s_' % self.side )
        
        ctlToe, pCtlToe = controller.getCircleController([1,0,0], 2, 'Ctl_IkToe2_%s_' % self.side )
        pCtlToe = cmds.parent( pCtlToe, footBaseGrp )[0]
        
        pCtlToe, ppCtlToe = dag.makeParent( pCtlToe, footBaseGrp )[0]
        
        axisIndex = 0
        if self.side == 'R': axisIndex += 3
        connect.lookAtConnect( aimTarget2, pCtlToe, axisIndex )
        connect.lookAtConnect( aimTarget1, footIk, axisIndex )
        
        cmds.connectAttr( stdFootToe +'.t', pToeIk + '.t' )
        cmds.connectAttr( stdFootToe +'.r', pToeIk + '.r' )
        cmds.connectAttr( stdFootToeEnd +'.t', toeEndIk + '.t' )
        cmds.connectAttr( stdFootToeEnd +'.r', toeEndIk + '.r' )
        connect.constraint_parent( pToeIk, ppCtlToe )
        connect.constraint_parent( ctlToe, toeIk )
        
        
        ctlFkToe, pCtlFkToe = controller.getCircleController([1,0,0], 3, 'Ctl_FkToe2_%s_' % self.side )
        pCtlFkToe = cmds.parent( pCtlFkToe, self.ctlFkThird )[0]
        stdAnkle = dag.getParent( stdFootAnkle )
        dcmp = connect.getLocalDcmp( stdFootToe, stdAnkle )
        cmds.connectAttr( dcmp + '.ot', pCtlFkToe + '.t' )
        cmds.connectAttr( dcmp + '.or', pCtlFkToe + '.r' )
        
        cmds.connectAttr( stdFootAnkle + '.t', footFk + '.t' )
        cmds.connectAttr( stdFootAnkle + '.r', footFk + '.r' )
        cmds.connectAttr( stdFootToe +'.t', pToeFk + '.t' )
        cmds.connectAttr( stdFootToe +'.r', pToeFk + '.r' )
        cmds.connectAttr( ctlFkToe +'.t', toeFk + '.t' )
        cmds.connectAttr( ctlFkToe +'.r', toeFk + '.r' )
        cmds.connectAttr( stdFootToeEnd +'.t', toeEndFk + '.t' )
        cmds.connectAttr( stdFootToeEnd +'.r', toeEndFk + '.r' )
        
        cmds.connectAttr( stdFootToe +'.t', pToeBlend + '.t' )
        cmds.connectAttr( stdFootToe +'.r', pToeBlend + '.r' )
        cmds.connectAttr( stdFootToeEnd +'.t', toeEndBlend + '.t' )
        cmds.connectAttr( stdFootToeEnd +'.r', toeEndBlend + '.r' )
        
        footIks = [footIk, toeIk]
        footFks = [footFk, toeFk]
        footBlends = [footBlend, toeBlend]
        
        for i in range( 2 ):
            blendTwoMatrixNode = connect.getBlendTwoMatrixNode( footIks[i], footFks[i], None, True )
            dcmp = connect.getDcmp( blendTwoMatrixNode )
            cmds.connectAttr( dcmp + '.ot', footBlends[i] + '.t' )
            cmds.connectAttr( dcmp + '.or', footBlends[i] + '.r' )
            
            cmds.connectAttr( self.ctlSwitch + '.fkSwitch', blendTwoMatrixNode + '.blend' )

    
    def followConnect(self, stdJntGrp, stdJnts, controllers ):
        
        def getComposedMultMatrix( stdJntGrp, stdJnt ):
            dcmpRotate    = cmds.createNode( 'decomposeMatrix' )
            dcmpTranslate = cmds.createNode( 'decomposeMatrix' )
            compose = cmds.createNode( 'composeMatrix' )
            cmds.connectAttr( stdJnt + '.wm', dcmpTranslate + '.imat' )
            cmds.connectAttr( stdJntGrp + '.wm', dcmpRotate + '.imat' )
            cmds.connectAttr( dcmpTranslate + '.ot', compose + '.it' )
            cmds.connectAttr( dcmpRotate + '.or', compose + '.ir' )
            mm = cmds.createNode( 'multMatrix' )
            cmds.connectAttr( compose + '.outputMatrix', mm + '.i[0]' )
            return mm
        
        def getComposeFromConnection( pCtl ):
            translateAttr = cmds.listConnections( pCtl + '.t', p=1 )[0]
            rotateAttr    = cmds.listConnections( pCtl + '.r', p=1 )[0]
            composeMatrix = cmds.createNode( 'composeMatrix' )
            cmds.connectAttr( translateAttr, composeMatrix + '.it' )
            cmds.connectAttr( rotateAttr, composeMatrix + '.ir' )
            return composeMatrix
        
        pCtl = cmds.listRelatives( self.ctlIk, p=1, f=1 )[0]
        mtxCompose = getComposeFromConnection( pCtl )
        
        mms = [mtxCompose]
        followNames = []
        for i in range( len( stdJnts ) ):
            mm = getComposedMultMatrix( stdJntGrp, self.stdEnd )
            dcmp = connect.getDcmp( mm )
            cmds.connectAttr( stdJnts[i] + '.wim', mm + '.i[1]' )
            
            followName = 'follow_' + stdJnts[i].split( '_' )[-1]
            followAttrName = '_'.join( self.stdEnd.split( '_' )[1:] ) + followName
            followPtr = dag.makeChild( controllers[i], followAttrName )
            
            cmds.connectAttr( dcmp + '.ot', followPtr + '.t' )
            cmds.connectAttr( dcmp + '.or', followPtr + '.r' )
            
            mm = cmds.createNode( 'multMatrix' )
            cmds.connectAttr( followPtr + '.wm', mm + '.i[0]' )
            cmds.connectAttr( pCtl + '.pim', mm + '.i[1]' )
            mms.append( mm )
            followNames.append( followName )
        
        followMatrix = connect.getFollowMatrix( mms )
        dcmp = connect.getDcmp( followMatrix )
        
        cmds.connectAttr( dcmp + '.ot', pCtl + '.t', f=1 )
        cmds.connectAttr( dcmp + '.or', pCtl + '.r', f=1 )
        
        for i in range( len( followNames ) ):
            attribute.addAttr( self.ctlSwitch, ln='%s' % followNames[i], k=1, min=0, max=1, dv=0 )
            cmds.connectAttr( self.ctlSwitch + '.%s' % followNames[i], followMatrix + '.follow_%02d' % (i+1) )







class MakeCollarRig(MakeRigBase):
    
    def __init__(self, *stdJnts, **options ):
        
        self.stdChest = stdJnts[0]
        self.stdCollar = stdJnts[1]
        self.stdCollarEnd = stdJnts[2]
        self.side = value.getValueFromDict( options, 'side' )
        
        self.baseGrp = self.makeParentGroup( self.stdChest, 'Collar_%s_' % self.side )
        self.ctl = self.createController()
        self.topRigJoint = self.createJoint()
        self.connector = cmds.listRelatives( self.topRigJoint, c=1, ad=1, f=1, type='joint' )[0]
        
    
    def createController(self):
        
        ctl, pCtl = controller.getCircleController( [1,0,0], 0.5, 'Ctl_Collar_%s_' %( self.side ) )
        fnCtl = dag.getDagNode( ctl )
        pCtl = cmds.parent( pCtl, self.baseGrp )[0]
        ctl = fnCtl.partialPathName()
        
        cmds.connectAttr( self.stdCollarEnd + '.t', pCtl + '.t' )
        
        dcmp = connect.getLocalDcmp( self.stdChest, self.stdCollar )
        cmds.connectAttr( dcmp + '.or', pCtl + '.r' )
        
        if self.side.lower() != 'l':
            ctl, ctlOffset = dag.makeParent( ctl, 'Offset_'  + ctl )[0]
            cmds.setAttr( ctlOffset + '.sx', -1 )
        return ctl


    def createJoint(self):
        
        cmds.select( self.baseGrp )
        topJnt = cmds.joint( n='RigJnt_Collar_%s_' % self.side )
        endJnt = cmds.joint( n='RigJnt_Collar_%s_end' % self.side )
        
    
        dcmpCtl = connect.getLocalDcmp( self.ctl, self.baseGrp )
        dist1 = cmds.createNode( 'distanceBetween' )
        dist2 = cmds.createNode( 'distanceBetween' )
        cmds.connectAttr( dcmpCtl + '.ot', dist1 + '.point1' )
        cmds.connectAttr( self.stdCollarEnd + '.t', dist2 + '.point2')
        divNode = cmds.createNode( 'multiplyDivide' ); cmds.setAttr( divNode + '.op', 2 )
        cmds.connectAttr( dist1 + '.distance', divNode + '.input1X' )
        cmds.connectAttr( dist2 + '.distance', divNode + '.input2X' )
        
        attribute.addAttr( self.ctl, ln='stretch', k=1, min=0, max=1 )
        blendNode = cmds.createNode( 'blendTwoAttr' )
        cmds.setAttr( blendNode + '.input[0]', 1 )
        cmds.connectAttr( divNode + '.outputX', blendNode + '.input[1]' )
        cmds.connectAttr( self.ctl + '.stretch', blendNode + '.ab' )
        
        multNode = cmds.createNode( 'multiplyDivide' )
        cmds.connectAttr( self.stdCollarEnd + '.t', multNode + '.input2' )
        cmds.connectAttr( blendNode + '.output', multNode + '.input1X' )
        cmds.connectAttr( blendNode + '.output', multNode + '.input1Y' )
        cmds.connectAttr( blendNode + '.output', multNode + '.input1Z' )
        cmds.connectAttr( multNode + '.output', endJnt + '.t' )
        
        connect.lookAtConnect( self.ctl, topJnt )
        
        endObject = dag.makeChild( self.baseGrp, 'RigObject_collar_%s_end' % self.side )
        cmds.connectAttr( self.stdCollarEnd + '.t', endObject + '.t' )
        cmds.connectAttr( self.stdCollarEnd + '.r', endObject + '.r' )
        connect.constraint_orient( endObject, endJnt )
        
        endJnt = cmds.listRelatives( topJnt, c=1, f=1, type='joint' )[0]
    
        return topJnt


    

class MakeHandRig(MakeRigBase):
    
    def getStdJnt( self, name ):
        targets = cmds.ls( '*StdJnt_' + name + '*_%s_*' % self.side, l=1 )
        
        for target in targets:
            if target.find( self.handStdJnt ) != -1:
                return dag.getLocalName( target )
    
    
    def __init__(self, handStdJnt, side ):
        
        self.handStdJnt = handStdJnt
        self.side = side
        
        self.stdThumb  = self.getStdJnt( 'Thumb' )
        self.stdIndex  = self.getStdJnt( 'Index' )
        self.stdMiddle = self.getStdJnt( 'Middle' )
        self.stdRing   = self.getStdJnt( 'Ring' )
        self.stdPinky  = self.getStdJnt( 'Pinky' )        
        self.baseGrp   = self.makeParentGroup( self.handStdJnt, 'hand_%s_' % self.side )
        
        if self.stdThumb:  self.ctlThumbs    = self.createCtls( self.stdThumb )
        if self.stdIndex:  self.ctlIndexs    = self.createCtls( self.stdIndex )
        if self.stdMiddle: self.ctlMiddles   = self.createCtls( self.stdMiddle )
        if self.stdRing:   self.ctlRings     = self.createCtls( self.stdRing )
        if self.stdPinky:  self.ctlPinkys    = self.createCtls( self.stdPinky )
        
        self.topRigJoints =[]
        if self.stdThumb:  self.topRigJoints.append( self.createJoints( self.stdThumb, self.ctlThumbs ) )
        if self.stdIndex:  self.topRigJoints.append( self.createJoints( self.stdIndex, self.ctlIndexs ) )
        if self.stdMiddle: self.topRigJoints.append( self.createJoints( self.stdMiddle, self.ctlMiddles ) )
        if self.stdRing:   self.topRigJoints.append( self.createJoints( self.stdRing, self.ctlRings ) )
        if self.stdPinky:  self.topRigJoints.append( self.createJoints( self.stdPinky, self.ctlPinkys ) )



    def createCtls(self, stdJntTop ):
        
        children = cmds.listRelatives( stdJntTop, c=1, ad=1, f=1 ,type='joint' )
        children.append( stdJntTop )
        children.reverse()
        
        parentTarget = self.baseGrp
        ctls = []
        for i in range( len( children )-1 ):
            ctl, pCtl = controller.getCircleController( [1,0,0], 0.3, dag.getLocalName(children[i]).replace( 'StdJnt_', 'Ctl_' ) )
            fnCtl = dag.getDagNode( ctl )
            pCtl = cmds.parent( pCtl, parentTarget )[0]
            parentTarget = fnCtl.partialPathName()
            cmds.connectAttr( children[i] + '.t', pCtl + '.t' )
            cmds.connectAttr( children[i] + '.r', pCtl + '.r' )
            ctls.append( fnCtl.partialPathName() )

        return ctls
    
    
    def createJoints(self, stdJntTop, ctls ):
        
        children = cmds.listRelatives( stdJntTop, c=1, ad=1, f=1, type='joint' )
        children.append( stdJntTop )
        children.reverse()
        
        lookAtObjs = []
        for i in range( len( ctls )-1 ):
            lookAtChild = makeLookAtChild( ctls[i+1], ctls[i] )
            lookAtObjs.append( lookAtChild )
        
        cmds.select( self.baseGrp )
        rigJnts = []
        
        for i in range( len( lookAtObjs ) ):
            jnt = cmds.joint( n=children[i].split( '|' )[-1].replace( 'StdJnt_', 'RigJnt_' ) )
            connect.constraint_parent( lookAtObjs[i], jnt )
            cmds.select( jnt )
            rigJnts.append( jnt )
        
        lastJnt = cmds.joint( n= children[-2].split( '|' )[-1].replace( 'StdJnt_', 'RigJnt_' ) )
        lastEndJnt = cmds.joint( n= children[-1].split( '|' )[-1].replace( 'StdJnt_', 'RigJnt_' ) )
        connect.constraint_parent( ctls[-1], lastJnt )
        cmds.connectAttr( children[-1] + '.t', lastEndJnt + '.t' )
        
        return rigJnts[0]
    
    


class MakeFootRig(MakeRigBase):
    
    def getStdJnt( self, name ):
        targets = cmds.ls( '*StdJnt_' + name + '*_%s_*' % self.side, l=1 )
        
        for target in targets:
            if target.find( self.footStdJnt ) != -1:
                return dag.getLocalName( target )


    def __init__(self, footStdJnt, side ):
        
        self.footStdJnt = footStdJnt
        self.side = side
        
        self.stdFootPivot     = self.getStdJnt( 'FootPivot' )
        self.stdFootCenter    = self.getStdJnt( 'FootCenter' )
        self.stdFootBankIn    = self.getStdJnt( 'FootBankIn' )
        self.stdFootBankOut   = self.getStdJnt( 'FootBankOut' )
        self.stdFootRotateEnd = self.getStdJnt( 'FootRotateEnd' )
        self.stdFootAnkle     = self.getStdJnt( 'FootAnkle' )
        self.stdFootToe       = self.getStdJnt( 'FootToe' )
        self.stdToeEnd        = self.getStdJnt( 'ToeEnd' )
        self.baseGrp = self.makeParentGroup( self.footStdJnt, 'Foot_%s_' % self.side )
        self.ctlFoot = self.createController()
        self.createRigJoints()
        self.createConnection()

    
    
    def createController(self ):
    
        ctl, pCtl = controller.getCircleController( [0,1,0], 1, 'Ctl_Foot_%s_' % self.side )
        fnCtl = dag.getDagNode( ctl )
        pCtl = cmds.parent( pCtl, self.baseGrp )[0]
        connect.connect( self.stdFootPivot, pCtl, ['t', 'r'], ['t', 'r'] )
        
        return fnCtl.partialPathName()
    

    
    def createRigJoints(self):
        
        cmds.select( self.baseGrp )
        self.rigJntFootCenter  = cmds.joint( n='Jnt_FootCenter_%s_' % self.side )
        self.rigJntFootPivot   = cmds.joint( n='Jnt_FootPivot_%s_' % self.side )
        self.rigJntFootBall    = cmds.joint( n='Jnt_FootBall _%s_' % self.side )
        self.rigJntFootBandIn  = cmds.joint( n='Jnt_FootBandIn_%s_' % self.side )
        self.rigJntFootBandOut = cmds.joint( n='Jnt_FootBandOut_%s_' % self.side )
        self.rigJntFootRotateEnd = cmds.joint( n='Jnt_FootRotateEnd_%s_' % self.side )
        self.rigJntFootToe = cmds.joint( n='Jnt_FootToe_%s_' % self.side )
        self.rigJntFootEnd = cmds.joint( n='Jnt_FootEnd_%s_' % self.side )
        
        dcmpFootCenter = connect.getLocalDcmp( self.stdFootCenter, self.footStdJnt )
        connect.connect( dcmpFootCenter, self.rigJntFootCenter, ['ot', 'or'], ['t', 'jo'] )
        dcmpFootPivot = connect.getLocalDcmp( self.stdFootPivot, self.stdFootCenter )
        connect.connect( dcmpFootPivot, self.rigJntFootPivot, ['ot', 'or'], ['t', 'jo'] )
        connect.connect( self.stdFootCenter, self.rigJntFootBall, ['t'], [ 't'] )
        connect.connect( self.stdFootBankIn, self.rigJntFootBandIn, ['t'], ['t'] )
        connect.connect( self.stdFootBankOut, self.rigJntFootBandOut, ['t'], ['t'] )
        connect.connect( self.stdFootRotateEnd, self.rigJntFootRotateEnd, ['t'], ['t'] )
        dcmpFootToe = connect.getLocalDcmp( self.stdFootToe, self.stdFootRotateEnd )
        connect.connect( dcmpFootToe, self.rigJntFootToe, ['ot', 'or'], ['t', 'jo'] )
        dcmpFootEnd = connect.getLocalDcmp( self.stdFootAnkle, self.stdFootToe )
        connect.connect( dcmpFootEnd, self.rigJntFootEnd, ['ot', 'or'], ['t', 'jo'] )
        
        cmds.setAttr( self.rigJntFootCenter + '.v', 0 )
        
        
    
    def createConnection(self):
    
        attribute.addAttr( self.ctlFoot, ln='walkRoll', k=1 )
        attribute.addAttr( self.ctlFoot, ln='footEndAngle', min=1, dv=10, max=90 )
        attribute.addAttr( self.ctlFoot, ln='walkRollAngle', k=1, min=1, dv=30, max=90 )
        attribute.addAttr( self.ctlFoot, ln='bank', k=1 )
        
        dcmp = connect.getLocalDcmp( self.stdToeEnd, self.stdFootCenter )
        angleNode = cmds.createNode( 'angleBetween' )
        cmds.setAttr( angleNode + '.vector1', 0,0,1 )
        if self.side == 'R':
            cmds.setAttr( angleNode + '.vector1', 0,0,-1 )
        cmds.connectAttr( dcmp + '.ot', angleNode + '.vector2' )
        multNode = cmds.createNode( 'multDoubleLinear' )
        cmds.connectAttr( angleNode + '.eulerX', multNode + '.input1' )
        cmds.setAttr( multNode + '.input2', -1 )
        cmds.connectAttr( multNode + '.output', self.ctlFoot + '.footEndAngle' )
        
        rangeNode = cmds.createNode( 'setRange')
        cmds.connectAttr( self.ctlFoot+ '.walkRoll', rangeNode + '.valueX' )
        cmds.setAttr( rangeNode + '.minX', -180 )
        cmds.setAttr( rangeNode + '.oldMinX', -180 )
        cmds.connectAttr( rangeNode + '.outValueX', self.rigJntFootPivot + '.rotateX' )
        divNode = cmds.createNode( 'multiplyDivide' ); cmds.setAttr( divNode + '.op', 2 )
        animCurve = cmds.createNode( 'animCurveUU' );
        cmds.setKeyframe( animCurve, f=0, v=0 )
        cmds.keyTangent( animCurve, f=(0,0), itt='linear', ott='linear' )
        cmds.setKeyframe( animCurve, f=1.5, v=1 )
        cmds.keyTangent( animCurve, f=(1.5,1.5), itt='flat', ott='flat' )
        cmds.connectAttr( divNode + '.outputX', animCurve + '.input' )
        multDouble = cmds.createNode( 'multDoubleLinear' )
        cmds.connectAttr( self.ctlFoot + '.walkRoll', divNode + '.input1X' )
        cmds.connectAttr( self.ctlFoot + '.footEndAngle', divNode + '.input2X' )
        cmds.connectAttr( animCurve + '.output', multDouble + '.input1' )
        cmds.connectAttr( self.ctlFoot + '.footEndAngle', multDouble + '.input2' )
        cmds.connectAttr( multDouble + '.output', self.rigJntFootCenter + '.rx' )
        
        add1 = cmds.createNode( 'addDoubleLinear' )
        add2 = cmds.createNode( 'addDoubleLinear' )
        setRange = cmds.createNode( 'setRange' )
        animCurve = cmds.createNode( 'animCurveUA' )
        cmds.connectAttr( self.ctlFoot + '.footEndAngle', add1 + '.input1' )
        cmds.connectAttr( self.ctlFoot + '.walkRollAngle', add1 + '.input2' )
        cmds.connectAttr( add1 + '.output', add2 + '.input1' )
        cmds.setAttr( add2 + '.input2', 180 )
        cmds.connectAttr( self.ctlFoot + '.walkRoll', setRange + '.valueX' )
        cmds.connectAttr( add1 + '.output', setRange + '.oldMinX' )
        cmds.connectAttr( add2 + '.output', setRange + '.oldMaxX' )
        cmds.setAttr( setRange + '.maxX', 180 )
        cmds.setKeyframe( animCurve, f=0, v=0 )
        cmds.keyTangent( animCurve, f=(0,0), itt='flat', ott='flat' )
        cmds.setKeyframe( animCurve, f=11, v=4 )
        cmds.keyTangent( animCurve, f=(11,11), itt='Spline', ott='Spline' )
        cmds.setKeyframe( animCurve, f=30, v=20 )
        cmds.keyTangent( animCurve, f=(30,30), itt='Spline', ott='Spline' )
        cmds.connectAttr( setRange + '.outValueX', animCurve + '.input' )
        cmds.connectAttr( animCurve + '.output',self.rigJntFootRotateEnd + '.rx' )
        cmds.setAttr( animCurve + '.postInfinity', 1 )
        
        add3 = cmds.createNode( 'addDoubleLinear' )
        setRange2 = cmds.createNode( 'setRange' )
        divNode = cmds.createNode( 'multiplyDivide' ); cmds.setAttr( divNode + '.op', 2 )
        animCurve1 = cmds.createNode( 'animCurveUU' )
        animCurve2 = cmds.createNode( 'animCurveUU' )
        mult1 = cmds.createNode( 'multDoubleLinear' )
        mult2 = cmds.createNode( 'multDoubleLinear' )
        add4 = cmds.createNode( 'addDoubleLinear' )
        cmds.connectAttr( self.ctlFoot + '.footEndAngle', add3 + '.input1' )
        cmds.setAttr( add3 + '.input2', 180 )
        cmds.connectAttr( self.ctlFoot + '.footEndAngle', setRange2 + '.oldMinX' )
        cmds.connectAttr( self.ctlFoot + '.walkRoll', setRange2 + '.valueX' )
        cmds.connectAttr( add3 + '.output', setRange2 + '.oldMaxX' )
        cmds.setAttr( setRange2 + '.maxX', 180 )
        cmds.connectAttr( setRange2 + '.outValueX', divNode + '.input1X' )
        cmds.connectAttr( self.ctlFoot + '.walkRollAngle', divNode + '.input2X' )
        cmds.connectAttr( setRange + '.outValueX', animCurve1 + '.input' )
        cmds.connectAttr( divNode + '.outputX', animCurve2 + '.input' )
        cmds.setKeyframe( animCurve1, f=0, v=0 )
        cmds.keyTangent( animCurve1, f=(0,0), itt='flat', ott='flat' )
        cmds.setKeyframe( animCurve1, f=90, v=1 )
        cmds.keyTangent( animCurve1, f=(90,90), itt='Spline', ott='Spline' )
        cmds.setKeyframe( animCurve2, f=0, v=0 )
        cmds.keyTangent( animCurve2, f=(0,0), itt='flat', ott='flat' )
        cmds.setKeyframe( animCurve2, f=2, v=1 )
        cmds.keyTangent( animCurve2, f=(2,2), itt='auto', ott='auto' )
        cmds.setAttr( animCurve1 + '.postInfinity', 1 )
        cmds.connectAttr( animCurve1 + '.output', mult1 + '.input1' )
        cmds.setAttr( mult1 + '.input2', -90 )
        cmds.connectAttr( animCurve2 + '.output', mult2 + '.input1' )
        cmds.connectAttr( self.ctlFoot + '.walkRollAngle', mult2 + '.input2' )
        cmds.connectAttr( mult1 + '.output', add4 + '.input1' )
        cmds.connectAttr( mult2 + '.output', add4 + '.input2' )
        cmds.connectAttr( add4 + '.output', self.rigJntFootToe + '.ry' )
        
        rangeBankIn  = cmds.createNode( 'setRange' )
        cmds.setAttr( rangeBankIn + '.maxX', 180 )
        cmds.setAttr( rangeBankIn + '.oldMaxX', 180 )
        rangeBankOut = cmds.createNode( 'setRange' )
        cmds.setAttr( rangeBankOut + '.minX', -180 )
        cmds.setAttr( rangeBankOut + '.oldMinX', -180 )
        multIn  = cmds.createNode( 'multDoubleLinear' )
        multOut = cmds.createNode( 'multDoubleLinear' )
        cmds.setAttr( multIn  + '.input2', -1 )
        cmds.setAttr( multOut + '.input2', -1 )
        cmds.connectAttr( self.ctlFoot + '.bank', multIn + '.input1' )
        cmds.connectAttr( self.ctlFoot + '.bank', multOut + '.input1' )
        cmds.connectAttr( self.ctlFoot + '.bank', rangeBankIn  + '.valueX' )
        cmds.connectAttr( self.ctlFoot + '.bank', rangeBankOut + '.valueX' )
        cmds.connectAttr( rangeBankIn + '.outValueX', self.rigJntFootBandIn  + '.rotateZ' )
        cmds.connectAttr( rangeBankOut + '.outValueX', self.rigJntFootBandOut + '.rotateZ' )
        
    
    



class MakeHeadRig( MakeRigBase ):
    
    def __init__(self, stdJntNeck, stdJntHead, stdJntEye_L_, stdJntEye_R_ ):
        
        self.stdJntNeck = stdJntNeck
        self.stdJntHead = stdJntHead
        self.stdJntEye_L_  = stdJntEye_L_
        self.stdJntEye_R_  = stdJntEye_R_
        
        self.baseGrp = self.makeParentGroup( stdJntNeck, 'Neck' )
        self.baseJnts = self.createBaseJoint()
        self.createController()
        self.topRigJoint = self.createResults()
        self.createEyeRig()
        
        cmds.setAttr( self.baseJnts[0] + '.v', 0 )
        

    def createBaseJoint(self):
        
        multNode = cmds.createNode( 'multiplyDivide' )
        cmds.select( self.baseGrp )
        jnt0 = cmds.joint( n='RigJntBase_neck' )
        jnt1 = cmds.joint( n='RigJntBase_neckMiddle' )
        jnt2 = cmds.joint( n='RigJntBase_head' )
        
        cmds.connectAttr( self.stdJntHead + '.t', multNode + '.input1' )
        cmds.setAttr( multNode + '.input2', 0.5, 0.5, 0.5 )
        
        cmds.connectAttr( multNode + '.output', jnt1 + '.t' )
        cmds.connectAttr( multNode + '.output', jnt2 + '.t' )
        
        return jnt0, jnt1, jnt2
    
    

    def createController(self):
        
        ctlNeck, pCtlNeck = controller.getCircleController( [0,1,0], 1, 'Ctl_Neck' )
        ctlHead, pCtlHead = controller.getCircleController( [0,0,1], 1, 'Ctl_Head' )
        
        fnCtlNeck = OpenMaya.MFnDagNode( sgbase.getDagPath(ctlNeck) )
        fnCtlHead = OpenMaya.MFnDagNode( sgbase.getDagPath(ctlHead) )
        
        pCtlNeck = cmds.parent( pCtlNeck, self.baseGrp )[0]
        pCtlHead = cmds.parent( pCtlHead, self.baseGrp )[0]
        ctlNeck  = fnCtlNeck.partialPathName()
        ctlHead  = fnCtlHead.partialPathName()
        cmds.connectAttr( self.stdJntHead + '.r', pCtlHead + '.r' )
        connect.getSourceConnection( pCtlNeck, self.baseJnts[1] )
        cmds.setAttr( pCtlNeck + '.r', 0,0,0 )
        connect.constraint_orient( ctlNeck, self.baseJnts[1] )
        dcmp = connect.getBlendTwoMatrixDcmpNode( ctlNeck, pCtlNeck, self.baseJnts[0] )
        cmds.connectAttr( dcmp + '.or', self.baseJnts[0] + '.r' )
        connect.constraint_point( self.baseJnts[2], pCtlHead )
        
        self.ctlHead = ctlHead
        self.ctlNeck = ctlNeck
    

    def createResults(self):
        
        pCtlHead = cmds.listRelatives( self.ctlHead, p=1, f=1 )[0]
        headPointer = dag.makeChild( pCtlHead, 'PointerCtl_head' )
        cmds.connectAttr( self.ctlHead + '.t', headPointer + '.t' )
        
        wtAddMtx = connect.createSkinWeightMatrix( [self.baseGrp, pCtlHead], [self.baseGrp, headPointer] )
        cmds.setAttr( wtAddMtx + '.skinWeight_0', 0.5 )
        cmds.setAttr( wtAddMtx + '.skinWeight_1', 0.5 )
        mm = cmds.createNode( 'multMatrix' )
        dcmp = connect.getDcmp( mm )
        cmds.connectAttr( self.baseJnts[1] + '.wm', mm + '.i[0]' )
        cmds.connectAttr( wtAddMtx + '.o', mm + '.i[1]' )
        
        neckCenter = dag.makeChild( self.baseGrp, 'Pointer_neck' )
        cmds.connectAttr( neckCenter + '.pim', mm + '.i[2]' )
        
        cmds.connectAttr( dcmp + '.ot', neckCenter + '.t' )
        cmds.connectAttr( dcmp + '.or', neckCenter + '.r' )
        cmds.setAttr( neckCenter + '.dh', 1 )
        
        rigJntResultGrp = dag.makeChild( self.baseGrp, 'PRigJnt_Neck' )
        resultJnt0 = cmds.joint( n='RigJnt_Neck' )
        pResultJnt1 = dag.makeChild( resultJnt0, 'PRigJnt_NeckMiddle' )
        resultJnt1 = cmds.joint( n='RigJnt_NeckMiddle' )
        resultJnt2 = cmds.joint( n='RigJnt_head' )
        
        cmds.connectAttr( self.baseJnts[0] + '.r', rigJntResultGrp + '.r' )
        connect.lookAtConnect( neckCenter, resultJnt0 )
        connect.constraint_point( neckCenter, pResultJnt1 )
        connect.lookAtConnect( headPointer, resultJnt1 )
        connect.constraint_parent( self.ctlHead, resultJnt2 )
        
        pResultJnt1 = dag.getParent( resultJnt1 )
        dcmpPHead = connect.getDcmp( pCtlHead )
        dcmpHead = connect.getDcmp( self.ctlHead )
        compose1 = cmds.createNode( 'composeMatrix' ); cmds.connectAttr( dcmpPHead + '.ot', compose1 + '.it' ); cmds.connectAttr( dcmpHead + '.or', compose1 + '.ir' )
        compose2 = cmds.createNode( 'composeMatrix' ); cmds.setAttr( compose2 + '.ity', 1 )
        mm = cmds.createNode( 'multMatrix' ); cmds.connectAttr( compose2 + '.outputMatrix', mm + '.i[0]' );cmds.connectAttr( compose1 + '.outputMatrix', mm + '.i[1]' ); cmds.connectAttr( pCtlHead + '.wim', mm + '.i[2]' )
        dcmpForAngle = connect.getDcmp( mm )
        angleNode = cmds.createNode( 'angleBetween' ); cmds.setAttr( angleNode + '.vector1', 0,1,0); cmds.connectAttr( dcmpForAngle + '.ot', angleNode + '.vector2' )
        compose3 = cmds.createNode( 'composeMatrix' ); cmds.connectAttr( angleNode + '.euler', compose3 + '.ir' )
        invMtx = cmds.createNode( 'inverseMatrix' ); cmds.connectAttr( compose3 + '.outputMatrix', invMtx + '.inputMatrix' )
        mm = cmds.createNode( 'multMatrix' ); cmds.connectAttr( self.ctlHead + '.m', mm + '.i[0]' ); cmds.connectAttr( invMtx + '.outputMatrix', mm + '.i[1]' )
        compose3 = cmds.createNode( 'composeMatrix' )
        addMtx = cmds.createNode( 'addMatrix' ); cmds.connectAttr( compose3 + '.outputMatrix', addMtx + '.matrixIn[0]' );cmds.connectAttr( mm + '.o', addMtx + '.matrixIn[1]' )
        dcmp = connect.getDcmp( addMtx )
        cmds.connectAttr( dcmp + '.or', pResultJnt1 + '.r' )
        
        return resultJnt0
    
    
    def createEyeRig(self):
        
        headJnt = cmds.listRelatives( self.topRigJoint, c=1, ad=1, f=1 )[0]
        
        cmds.select( headJnt )
        rigJntEye_L_ = cmds.joint( n='RigJnt_eye_L_')
        cmds.select( headJnt )
        rigJntEye_R_ = cmds.joint( n='RigJnt_eye_R_')
        rigJntEye_L_, pRigJntEye_L_ = dag.makeParent( rigJntEye_L_ )[0]
        rigJntEye_R_, pRigJntEye_R_ = dag.makeParent( rigJntEye_R_ )[0]
        
        cmds.connectAttr( self.stdJntEye_L_ + '.t', pRigJntEye_L_ + '.t' )
        cmds.connectAttr( self.stdJntEye_R_ + '.t', pRigJntEye_R_ + '.t' )
        
        averageNode = cmds.createNode( 'plusMinusAverage' ); cmds.setAttr( averageNode + '.operation', 3 )
        cmds.connectAttr( self.stdJntEye_L_ + '.t', averageNode + '.input3D[0]' )
        cmds.connectAttr( self.stdJntEye_R_ + '.t', averageNode + '.input3D[1]' )
        addZ = cmds.createNode( 'plusMinusAverage' ); cmds.setAttr( addZ + '.input3D[0].input3Dz', 10 )
        cmds.connectAttr( averageNode + '.output3D', addZ + '.input3D[1]' )
        
        ctlEye, pCtlEye = controller.getCircleController([0,0,1], 6, 'Ctl_Eye')
        pCtlEye = cmds.parent( pCtlEye, self.ctlHead )[0]
        cmds.connectAttr( addZ + '.output3D', pCtlEye + '.t' )
        
        ctlEye_L_, pCtlEye_L_ = controller.getCircleController([0,0,1], 2, 'Ctl_Eye_L_')
        ctlEye_R_, pCtlEye_R_ = controller.getCircleController([0,0,1], 2, 'Ctl_Eye_R_')
        
        pCtlEye_L_ = cmds.parent( pCtlEye_L_, ctlEye )[0]
        pCtlEye_R_ = cmds.parent( pCtlEye_R_, ctlEye )[0]
        
        pma_L_ = cmds.createNode( 'plusMinusAverage' ); cmds.setAttr( pma_L_ + '.op', 2 )
        pma_R_ = cmds.createNode( 'plusMinusAverage' ); cmds.setAttr( pma_R_ + '.op', 2 )
        cmds.connectAttr( self.stdJntEye_L_ + '.t', pma_L_ + '.input3D[0]' )
        cmds.connectAttr( self.stdJntEye_R_ + '.t', pma_R_ + '.input3D[0]' )
        cmds.connectAttr( averageNode + '.output3D', pma_L_ + '.input3D[1]' )
        cmds.connectAttr( averageNode + '.output3D', pma_R_ + '.input3D[1]' )
        
        cmds.connectAttr( pma_L_ + '.output3D', pCtlEye_L_ + '.t' )
        cmds.connectAttr( pma_R_ + '.output3D', pCtlEye_R_ + '.t' )
        
        connect.lookAtConnect( ctlEye_L_, rigJntEye_L_ )
        connect.lookAtConnect( ctlEye_R_, rigJntEye_R_ )

        attribute.addAttr( ctlEye, ln='distance', min=0.01, dv=10, k=1 )
        cmds.connectAttr( ctlEye + '.distance', addZ + '.input3D[0].input3Dz' )




def makeSkinJoints( sep ):
        
    rigJnts = cmds.ls( 'RigJnt_*' )
    
    newJnts = []
    for jnt in rigJnts:
        cmds.setAttr( jnt + '.v', 0 )
        jntP = cmds.listRelatives( jnt, p=1 )[0]
        newJnt = cmds.createNode( 'joint', n=jnt.replace( 'RigJnt_', 'SkinJnt_' ) )
        if jntP.split( '_' )[0] in ['RigJnt']:
            cmds.connectAttr( jnt + '.t', newJnt + '.t' )
            cmds.connectAttr( jnt + '.r', newJnt + '.r' )
        else:
            connect.constraint_parent( jnt, newJnt )    
        
        newJnts.append( dag.getDagNode( newJnt ) )


    for i in range( len( rigJnts ) ):
        newJnt = newJnts[i].partialPathName()
        rigJnt = rigJnts[i]
        if cmds.nodeType( rigJnt ) == 'joint':cmds.setAttr( rigJnt + '.jo', 0,0,0 )
        
        rigJntP = cmds.listRelatives( rigJnt, p=1 )[0]
        newJntP = rigJntP.replace( 'RigJnt_', 'SkinJnt_' )
        
        if cmds.objExists( newJntP ) and newJntP.find( 'SkinJnt_' ) != -1:
            cmds.parent( newJnt, newJntP )
            transform.setToDefault( newJnts[i].partialPathName() )
            cmds.setAttr( newJnt + '.jo', 0,0,0 )
    
    for side in ['L', 'R']:
        jnt = cmds.parent( 'SkinJnt_eye_%s_' % side, 'SkinJnt_head' )[0]
        transform.setJointOrientZero( jnt )
        jnt = cmds.parent( 'SkinJnt_toe_%s_' % side, 'SkinJnt_Foot_%s_' % side )[0]
        transform.setJointOrientZero( jnt )
        jnt = cmds.parent( 'SkinJnt_Leg_%s_0' % side, 'SkinJnt_Spline00' )[0]
        transform.setJointOrientZero( jnt )
        jnt = cmds.parent( 'SkinJnt_Arm_%s_0' % side, 'SkinJnt_Collar_%s_end' % side )
        transform.setJointOrientZero( jnt )
        jnt = cmds.parent( 'SkinJnt_Collar_%s_' % side, 'SkinJnt_Spline04' )
        transform.setJointOrientZero( jnt )
        fingers = cmds.ls( 'SkinJnt_*_%s_00' % side )
        for finger in fingers:
            finger = cmds.parent( finger, 'SkinJnt_Arm_%s_%d' % (side,sep*2) )[0]
            transform.setJointOrientZero( finger )
    
    jnt = cmds.parent( 'SkinJnt_NeckMiddle', 'SkinJnt_Neck' )
    transform.setJointOrientZero( jnt )
    jnt = cmds.parent( 'SkinJnt_Neck', 'SkinJnt_Spline04' )
    transform.setJointOrientZero( jnt )
    
    topJnt = 'SkinJnt_Spline00'
    grp = cmds.group( em=1, n='Grp_skinJnt' )
    cmds.parent( topJnt, grp )
    
    
    




def editControllerShape():
    
    import json, os
    
    f = open( os.path.dirname(__file__) + '/ctlShapeInfo.txt', 'r' )
    items = json.load( f ).items()
    
    for ctlName, infos in items:
        if not cmds.objExists( ctlName ): continue
        colorIndex = infos[0]
        points = infos[1:]
        
        curve = cmds.curve( p=points, d=1 )
        curveShape = cmds.listRelatives( curve, s=1, f=1 )[0]
        cmds.setAttr( curveShape + '.overrideEnabled', 1 )
        cmds.setAttr( curveShape + '.overrideColor', colorIndex )
        
        ctlShapes = cmds.listRelatives( ctlName, s=1, f=1 )
        if ctlShapes:cmds.delete( ctlShapes )
        
        cmds.parent( curveShape, ctlName, add=1, shape=1 )
        cmds.delete( curve )



def lockAndHideAttrs():
    
    ctls = cmds.ls( 'Ctl_*', type='transform' )
    
    for ctl in ctls:
        if ctl == 'Ctl_All': continue
        cmds.setAttr( ctl + '.s', lock=1 )
        cmds.setAttr( ctl + '.sx', e=1, k=0 )
        cmds.setAttr( ctl + '.sy', e=1, k=0 )
        cmds.setAttr( ctl + '.sz', e=1, k=0 )
        
        cmds.setAttr( ctl + '.v', lock=1 )
        cmds.setAttr( ctl + '.v', e=1, k=0 )
    
        if ctl.find( 'Ctl_Collar_' ) != -1 or ctl.find( 'Ctl_Foot' ) != -1 or ctl.find( 'Ctl_switch_' ) != -1:
            cmds.setAttr( ctl + '.r', lock=1 )
            cmds.setAttr( ctl + '.rx', e=1, k=0 )
            cmds.setAttr( ctl + '.ry', e=1, k=0 )
            cmds.setAttr( ctl + '.rz', e=1, k=0 )
    
        if ctl.find( 'Ctl_Foot' ) != -1 or ctl.find( 'Ctl_switch_' ) != -1 or ctl.find( 'Ctl_Neck' ) != -1:
            cmds.setAttr( ctl + '.t', lock=1 )
            cmds.setAttr( ctl + '.tx', e=1, k=0 )
            cmds.setAttr( ctl + '.ty', e=1, k=0 )
            cmds.setAttr( ctl + '.tz', e=1, k=0 )



def makeControllerHistory():
    
    ctls = cmds.ls( 'Ctl_*', type='transform' )
    
    for ctl in ctls:
        ctlShape = dag.getShape( ctl )
        ctlShape = cmds.rename( ctlShape, ctl + 'Shape' )
        
        ctlOrig = dag.addIOShape( ctl )
        trGeoNode = cmds.createNode( 'transformGeometry' )
        cmds.connectAttr( ctlOrig + '.local', trGeoNode + '.inputGeometry' )
        cmds.connectAttr( trGeoNode + '.outputGeometry', ctlShape + '.create' )
        compose = cmds.createNode( 'composeMatrix' )
        cmds.connectAttr( 'Grp_std.s', compose + '.is' )
        cmds.connectAttr( compose + '.outputMatrix', trGeoNode + '.transform' )
        



class MakeRig:
    
    def getStdJnt( self, name ):
        targets = cmds.ls( '*StdJnt_' + name )
        if len( targets ) == 1:
            return targets[0]
        
        for target in targets:
            if target.find( self.stdJntGrp ) != -1:
                return target
    
    
    def __init__(self, stdGroup, sep=3 ):
        
        ns = stdGroup.replace( 'Grp_std', '' )
        if cmds.objExists( ns + 'Grp_set' ): return None
        
        stdChildren = cmds.listRelatives( stdGroup, c=1, f=1 )
        
        self.stdJntGrp = None
        for stdChild in stdChildren:
            if stdChild[-7:] != 'StdJnts': continue
            self.stdJntGrp = stdChild
        if not self.stdJntGrp: return None
        
        self.root          = self.getStdJnt( 'Root' )
        self.back01        = self.getStdJnt( 'Back01' )
        self.back02        = self.getStdJnt( 'Back02' )
        self.chest            = self.getStdJnt( 'Chest' )
        self.neck             = self.getStdJnt( 'Neck' )
        self.head             = self.getStdJnt( 'Head' )
        self.eye_L_             = self.getStdJnt( 'Eye_L_' )
        self.eye_R_             = self.getStdJnt( 'Eye_R_' )
        
        self.collar_L_        = self.getStdJnt( 'Collar_L_' )
        self.shoulder_L_      = self.getStdJnt( 'Shoulder_L_' )
        self.elbow_L_         = self.getStdJnt( 'Elbow_L_' )
        self.elbow_L_offset   = self.getStdJnt( 'Elbow_L_Offset' )
        self.wrist_L_         = self.getStdJnt( 'Wrist_L_' )
        self.armPoleVector_L_ = self.getStdJnt( 'ArmPoleVector_L_' )
        
        self.collar_R_        = self.getStdJnt( 'Collar_R_' )
        self.shoulder_R_      = self.getStdJnt( 'Shoulder_R_' )
        self.elbow_R_         = self.getStdJnt( 'Elbow_R_' )
        self.elbow_R_offset   = self.getStdJnt( 'Elbow_R_Offset' )
        self.wrist_R_         = self.getStdJnt( 'Wrist_R_' )
        self.armPoleVector_R_ = self.getStdJnt( 'ArmPoleVector_R_' )
        
        self.hip_L_           = self.getStdJnt( 'Hip_L_' )
        self.knee_L_          = self.getStdJnt( 'Knee_L_' )
        self.knee_L_offset    = self.getStdJnt( 'Knee_L_Offset' )
        self.ankle_L_         = self.getStdJnt( 'Ankle_L_' )
        self.legPoleVector_L_ = self.getStdJnt( 'LegPoleVector_L_' )
        
        self.hip_R_           = self.getStdJnt( 'Hip_R_' )
        self.knee_R_          = self.getStdJnt( 'Knee_R_' )
        self.knee_R_offset    = self.getStdJnt( 'Knee_R_Offset' )
        self.ankle_R_         = self.getStdJnt( 'Ankle_R_' )
        self.legPoleVector_R_ = self.getStdJnt( 'LegPoleVector_R_' )
        
        self.hand_L_          = self.getStdJnt( 'Wrist_L_' )
        self.hand_R_          = self.getStdJnt( 'Wrist_R_' )

        self.bodyRig      = MakeBodyRig( self.root, self.back01, self.back02, self.chest )
        self.collarRig_L_ = MakeCollarRig( self.chest, self.collar_L_, self.shoulder_L_, side='L' )
        self.collarRig_R_ = MakeCollarRig( self.chest, self.collar_R_, self.shoulder_R_, side='R' )
        self.armRig_L_    = MakeArmRig( self.shoulder_L_, self.elbow_L_, self.wrist_L_, self.elbow_L_offset, self.armPoleVector_L_, name='Arm', side='L', sep=sep )
        self.armRig_R_    = MakeArmRig( self.shoulder_R_, self.elbow_R_, self.wrist_R_, self.elbow_R_offset, self.armPoleVector_R_, name='Arm', side='R', sep=sep )
        self.legRig_L_    = MakeArmRig( self.hip_L_, self.knee_L_, self.ankle_L_, self.knee_L_offset, self.legPoleVector_L_, name='Leg', side='L', sep=sep )
        self.legRig_R_    = MakeArmRig( self.hip_R_, self.knee_R_, self.ankle_R_, self.knee_R_offset, self.legPoleVector_R_, name='Leg', side='R', sep=sep )
        self.handRig_L_   = MakeHandRig( self.hand_L_, 'L' )
        self.handRig_R_   = MakeHandRig( self.hand_R_, 'R' )
        self.footRig_L_   = MakeFootRig( self.ankle_L_, 'L' )
        self.footRig_R_   = MakeFootRig( self.ankle_R_, 'R' )
        self.headRig      = MakeHeadRig( self.neck, self.head, self.eye_L_, self.eye_R_ )

        self.armRig_L_.fixConnectBaseGrp( self.collarRig_L_.connector )
        self.armRig_R_.fixConnectBaseGrp( self.collarRig_R_.connector )
        
        self.bodyRig.addNeckConnector( self.neck )
        self.headRig.fixConnectBaseGrp( self.bodyRig.connectorNeck )
        
        self.bodyRig.addHipConnector( self.hip_L_, self.hip_R_ )
        self.legRig_L_.fixConnectBaseGrp( self.bodyRig.hipConnector_L_ )
        self.legRig_R_.fixConnectBaseGrp( self.bodyRig.hipConnector_R_ )
        
        self.bodyRig.addCollarConnector( self.collar_L_, self.collar_R_ )
        self.collarRig_L_.fixConnectBaseGrp( self.bodyRig.connectorCollar_L_ )
        self.collarRig_R_.fixConnectBaseGrp( self.bodyRig.connectorCollar_R_ )
        
        self.handRig_L_.fixConnectBaseGrp( self.armRig_L_.connector )
        self.handRig_R_.fixConnectBaseGrp( self.armRig_R_.connector )
        
        self.legRig_L_.addFootJointRig( self.footRig_L_.baseGrp, self.footRig_L_.rigJntFootToe, self.footRig_L_.rigJntFootRotateEnd, self.footRig_L_.rigJntFootEnd,
                                        self.footRig_L_.stdFootAnkle, self.footRig_L_.stdFootToe, self.footRig_L_.stdToeEnd )
        self.legRig_R_.addFootJointRig( self.footRig_R_.baseGrp, self.footRig_R_.rigJntFootToe, self.footRig_R_.rigJntFootRotateEnd, self.footRig_R_.rigJntFootEnd,
                                        self.footRig_R_.stdFootAnkle, self.footRig_R_.stdFootToe, self.footRig_R_.stdToeEnd )

        self.ctlAll, self.pCtlAll = controller.getCircleController( [0,1,0], 10, 'Ctl_All' )
        cmds.parent( self.bodyRig.baseGrp, self.collarRig_L_.baseGrp, self.collarRig_R_.baseGrp, self.armRig_L_.baseGrp, self.armRig_R_.baseGrp, self.legRig_L_.baseGrp, self.legRig_R_.baseGrp,
                     self.handRig_L_.baseGrp, self.handRig_R_.baseGrp, self.footRig_L_.baseGrp, self.footRig_R_.baseGrp, self.headRig.baseGrp, self.ctlAll )

        self.armRig_L_.fixIKCtlOrientation( self.stdJntGrp, self.ctlAll )
        self.armRig_R_.fixIKCtlOrientation( self.stdJntGrp, self.ctlAll )
        self.legRig_L_.fixIKCtlOrientation( self.stdJntGrp, self.ctlAll )
        self.legRig_R_.fixIKCtlOrientation( self.stdJntGrp, self.ctlAll )

        self.armRig_L_.followConnect( self.stdJntGrp, [self.chest, self.root], [self.bodyRig.ctlChest, self.bodyRig.ctlRoot] )
        self.armRig_R_.followConnect( self.stdJntGrp, [self.chest, self.root], [self.bodyRig.ctlChest, self.bodyRig.ctlRoot] )
        self.legRig_L_.followConnect( self.stdJntGrp, [self.root], [self.bodyRig.ctlRoot] )
        self.legRig_R_.followConnect( self.stdJntGrp, [self.root], [self.bodyRig.ctlRoot] )

        makeSkinJoints( sep )
        editControllerShape()
        lockAndHideAttrs()
        makeControllerHistory()
        connect.constraint_scale( ns + 'Ctl_All', ns + 'Grp_skinJnt' )
        setGrp = cmds.group( em=1, n= ns + 'Grp_set' )
        self.pCtlAll = cmds.parent( self.pCtlAll, setGrp )[0]
        
        setGrp = cmds.createNode( 'transform', n= ns + 'SET' )
        cmds.parent( ns + 'Grp_std', ns + 'Grp_set', ns + 'Grp_skinJnt', setGrp )
        cmds.setAttr( ns + 'Grp_std.v', 0 )
        
        for armAndLegRig in [self.armRig_L_, self.armRig_R_, self.legRig_L_, self.legRig_R_]:
            armAndLegRig.fixPoleVector()
    



def getMocapJoint( grpSet ):
    
    children = cmds.listRelatives( grpSet, c=1, ad=1, type='transform' )
    
    ctlAll = ''
    for child in children:
        if child.find( 'Ctl_All' ) != -1:
            ctlAll = child
            break
    if not ctlAll: return None
    
    stdJntTop = ctlAll.replace( 'Ctl_All', 'StdJnt_Root' )
    
    print "stdJntTop : ", stdJntTop
    mocJntTopName = dag.getLocalName(stdJntTop).replace( 'StdJnt_', 'MocJnt_' )
    if cmds.objExists( mocJntTopName ): return mocJntTopName
    mocJntTop = cmds.duplicate( stdJntTop, n=mocJntTopName )[0]
    mocJoints = cmds.listRelatives( mocJntTop, c=1, ad=1, f=1 )
    for mocJoint in mocJoints:
        mocJoint = cmds.rename( mocJoint, dag.getLocalName( mocJoint ).replace( 'StdJnt_', 'MocJnt_' ) )
        if mocJoint.find( 'FootPivot' ) != -1:
            cmds.delete( mocJoint )
    
    cmds.setAttr( mocJntTop + '.v', 0 )
    ctlAll = 'Ctl_All'
    return cmds.parent( mocJntTop, ctlAll )[0]



def connectMocapJoint( grpSet ):
    
    mocTop = getMocapJoint( grpSet )
    ns = mocTop.replace( 'MocJnt_Root', '' )
    
    targets = []
    targets.append( [ 'Root', 'Root' ] )
    targets.append( [ 'Hip_%SIDE%_', 'FK_Hip_%SIDE%_' ] )
    targets.append( [ 'Knee_%SIDE%_', 'FK_Knee_%SIDE%_' ] )
    targets.append( [ 'Ankle_%SIDE%_', 'FK_Ankle_%SIDE%_' ] )
    targets.append( [ 'Ankle_%SIDE%_', 'LegIK_%SIDE%_'] )
    targets.append( [ 'LegPoleVector_%SIDE%_', 'LegPoleVIK_%SIDE%_' ] )
    targets.append( [ 'Back01', 'BodyRotator1' ] )
    targets.append( [ 'Chest', 'Chest' ] )
    targets.append( [ 'Neck', 'Neck' ] )
    targets.append( [ 'Head', 'Head' ] )
    targets.append( [ 'Shoulder_%SIDE%_', 'FK_Shoulder_%SIDE%_' ] )
    targets.append( [ 'Shoulder_%SIDE%_', 'Collar_%SIDE%_' ] )
    targets.append( [ 'Elbow_%SIDE%_', 'FK_Elbow_%SIDE%_' ] )
    targets.append( [ 'Wrist_%SIDE%_', 'FK_Wrist_%SIDE%_' ] )
    targets.append( [ 'Wrist_%SIDE%_', 'ArmIK_%SIDE%_' ] )
    targets.append( [ 'ArmPoleVector_%SIDE%_', 'ArmPoleVIK_%SIDE%_' ] )
    targets.append( [ 'Thumb_%SIDE%_%NUM%', 'Thumb_%SIDE%_%NUM%' ] )
    targets.append( [ 'Index_%SIDE%_%NUM%', 'Index_%SIDE%_%NUM%' ] )
    targets.append( [ 'Middle_%SIDE%_%NUM%','Middle_%SIDE%_%NUM%' ] )
    targets.append( [ 'Ring_%SIDE%_%NUM%',  'Ring_%SIDE%_%NUM%' ] )
    targets.append( [ 'Pinky_%SIDE%_%NUM%', 'Pinky_%SIDE%_%NUM%' ] )
    
    for mocName, ctlName in targets:
        mocJnt = ns + 'MocJnt_' + mocName
        ctl    = ns + 'Ctl_'    + ctlName
        
        if cmds.objExists( mocJnt ):
            try:cmds.parentConstraint( mocJnt, ctl )
            except: cmds.orientConstraint( mocJnt, ctl )
            continue
        
        mocJnt_L_ = mocJnt.replace( '%SIDE%', 'L' )
        mocJnt_R_ = mocJnt.replace( '%SIDE%', 'R' )
        ctl_L_    = ctl.replace( '%SIDE%', 'L' )
        ctl_R_    = ctl.replace( '%SIDE%', 'R' )
        
        if cmds.objExists( mocJnt_L_ ):
            try:cmds.parentConstraint( mocJnt_L_, ctl_L_ )
            except:cmds.pointConstraint( mocJnt_L_, ctl_L_ )
            try:cmds.parentConstraint( mocJnt_R_, ctl_R_ )
            except:cmds.pointConstraint( mocJnt_R_, ctl_R_ )
        else:
            cuIndex = -1
            while True:
                cuIndex +=1
                if cuIndex > 10: break
                targetMocJnt_L_ = mocJnt_L_.replace( '%NUM%', '%02d' % cuIndex )
                targetMocJnt_R_ = mocJnt_R_.replace( '%NUM%', '%02d' % cuIndex )
                targetCtl_L_ = targetMocJnt_L_.replace( 'MocJnt_', 'Ctl_' )
                targetCtl_R_ = targetMocJnt_R_.replace( 'MocJnt_', 'Ctl_' )
                if not cmds.objExists( targetCtl_L_ ) or not cmds.objExists( targetCtl_R_ ):break
                cmds.orientConstraint( targetMocJnt_L_, targetCtl_L_ )
                cmds.orientConstraint( targetMocJnt_R_, targetCtl_R_ )
            
            


    
    
    
    