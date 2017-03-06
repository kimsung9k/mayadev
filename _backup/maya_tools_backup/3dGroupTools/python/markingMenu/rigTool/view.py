import maya.cmds as cmds
import basic.naming.cmdModel as naming
import basic.put.cmdModel as put
import put.cmdModel as put2
import basic.joint.cmdModel as joint
import basic.controller.cmdModel as controller
import basic.connection.cmdModel as connection
import basic.splineRig.cmdModel  as splineRig
import basic.skinCluster.cmdModel as skinCluster
import basic.rigging.cmdModel as rigging
import basic.createNodes.cmdModel as createNodes
import basic.deform.cmdModel as deform
import basic.goTo.cmdModel as goToCmdModel
import model
import sgRigConnection


def setConnectionTypeOriginal( *arg ):
    model.RigToolInfo._selOriginal = True
    model.RigToolInfo._selParent = False
    connection.mmSetParentModeFalse()

def setConnectionTypeParent( *arg ):
    model.RigToolInfo._selOriginal = False
    model.RigToolInfo._selParent = True
    connection.mmSetParentModeTrue()


class Create:
    
    def __init__(self, parentMenu, *args ):
        
        self._parentMenu = parentMenu
        
        cmds.popupMenu( self._parentMenu, e=1, deleteAllItems=1 )
        
        self.putMenu( 'N' )
        self.jointSetMenu( 'NW' )
        self.controllerMenu( 'W' )
        self.connectMenu( 'E' )
        self.goToMenu( 'NE' )
        self.skinClusterMenu( 'S' )
        self.riggingMenu( 'SW' )
        self.deformMenu( 'SE' )
        self.createNodesMenu()
        self.divider()
        self.namingMenu()
        
    
    
    def defaultSetting(self, name, rp=None ):
        
        cmds.setParent( self._parentMenu, menu=1 )
        if rp: cmds.menuItem( l=name, rp=rp, sm=1 )
        else: cmds.menuItem( l=name, sm=1 )
        
        
    def goToMenu(self, rp=None ):
        
        self.defaultSetting( 'Go to', rp )
        cmds.menuItem( l='Go To Target', rp='N', c=goToCmdModel.uiCmd_goToTarget )
        cmds.menuItem( l='Go To Target Position', rp='N', c=goToCmdModel.uiCmd_goToTargetPosition )
        cmds.menuItem( l='Go To Target Orient', rp='N', c=goToCmdModel.uiCmd_goToTargetOrient )
        
        
        
    def divider(self):
        
        cmds.setParent( self._parentMenu, menu=1 )
        cmds.menuItem( d=1 )
    
    
    def namingMenu(self, rp=None ):
        
        self.defaultSetting( 'Naming', rp )
        cmds.menuItem( l='Name Numbering UI', c=naming.mmShowNumberingUI )
        cmds.menuItem( l='Replace Name UI', c=naming.mmShowReplaceNameUI )
        cmds.menuItem( l='Remove Namespace SelH', c=naming.mmRemoveNamespaceSelH )
        cmds.menuItem( l='Rename Shape Selected', c=naming.mmRenameShapeSelected )



    def riggingMenu(self, rp=None ):

        self.defaultSetting( 'Rigging', rp )
        cmds.menuItem( l='Create Rivet', rp='N', c=rigging.mmCreateRivet )
        cmds.menuItem( l='Constrained Joint', rp='NW', c=rigging.mmConstrainedJoint )
        cmds.menuItem( l='Aim Object', rp='SW', c=rigging.mmMakeChildAimObject )
        cmds.menuItem( l='Add Curve To Sel Joints', rp='NE', c=splineRig.mmAddConnectCurve )
        cmds.menuItem( l='Create Curve Info UI', rp='N', c=splineRig.mmShowCurveInfoSetUI )



    def skinClusterMenu(self, rp=None ):

        self.defaultSetting( 'Skin Cluster', rp )
        cmds.menuItem( l='Skin Weight Edit Tool', rp='N', c=skinCluster.mmShowSkinWeightEditUI )
        cmds.menuItem( l='Set Skin BindPre Default', rp='NE', c=skinCluster.mmSetBindDefault )



    def putMenu(self, rp=None ):

        self.defaultSetting( 'Put', rp )
        cmds.menuItem( l='Put Null', rp='N', c=put.mmPutNull )
        cmds.menuItem( l='Put Joint', rp='NE', c=put.mmPutJoint )
        cmds.menuItem( l='Put Child', rp='S', c=put.mmPutChild )
        cmds.menuItem( l='Put Child Joint', rp='SE', c=put.mmPutChildJoint )
        cmds.menuItem( l='Put Null BBC', rp='W', c=put.mmPutNullBBC )
        cmds.menuItem( l='Put Joint BBC', rp='NW', c=put.mmPutJointBBC )
        cmds.menuItem( l='Put Joint Commponent Center', rp='SW', c=put2.uiCmd_putToVtxCenter )



    def jointSetMenu(self, rp=None ):
        
        self.defaultSetting( 'Joint Set', rp )
        cmds.menuItem( l='Create Joint UI',  rp='N', c=joint.mmShowCreateJointUI )
        cmds.menuItem( l='Hide Other Hierarchy', rp='W', c=joint.mmShowOnlySelectHierarchy )
        cmds.menuItem( l='Show All Hierarchy', rp='SW', c=joint.mmShowAllSelectedHierarchy )
        cmds.menuItem( l='Set Joint Orient UI', rp='E', c=joint.mmShowSetJointOrientUI )
        cmds.menuItem( l='Set Orient To Target', rp='S', c=joint.mmSetOrientToTarget )
        cmds.menuItem( l='Mirror', rp='NW', c=joint.mmMirrorJoint )
        cmds.menuItem( l='Parent Selected Order', rp='NE', c=joint.mmParentSelectedOrder )
        cmds.menuItem( l='Insert Joint Tool', rp='SE', c=joint.mmInsertJoint )
        
        cmds.menuItem( l='Add AngleDriver', c=joint.mmAddAngleDriver )
        cmds.menuItem( l='Freeze Joint Orient', c=joint.mmFreezeJointOrient )
        


    def controllerMenu(self, rp=None ):
        
        self.defaultSetting( 'Controller', rp )
        cmds.menuItem( l='Make GRP', rp='N', c=controller.mmMakeGRP )
        cmds.menuItem( l='Add Shape', rp='NW', c=controller.mmAddShape )
        cmds.menuItem( l='Mirror Controller', rp='NE', c=controller.mmMirrorController )
        cmds.menuItem( l='IK Handle', rp='E', c=controller.mmIkHandle )
        
        cmds.menuItem( l='UI', rp='W', sm=1 )
        cmds.menuItem( l='Color Override', rp='W', c=controller.mc_OpenColorOverride )
        cmds.menuItem( l='Open Build Controller', rp='SW', c=controller.mc_OpenBuildControllerUI )
        cmds.setParent( '..', menu=1 )
        
        cmds.menuItem( l='Rotation Order', sm=1 )
        cmds.menuItem( l='xyz', c=controller.MmSetOrder().xyz_0 )
        cmds.menuItem( l='yzx', c=controller.MmSetOrder().yzx_1 )
        cmds.menuItem( l='zxy', c=controller.MmSetOrder().zxy_2 )
        cmds.menuItem( l='xzy', c=controller.MmSetOrder().xzy_3 )
        cmds.menuItem( l='yxz', c=controller.MmSetOrder().yxz_4 )
        cmds.menuItem( l='zyx', c=controller.MmSetOrder().zyx_5 )
        cmds.setParent( '..', menu=1 )
        
        
    
    def connectMenu(self, rp=None ):
        
        self.defaultSetting( 'Connect', rp )
        cmds.menuItem( l='translate', rp='N', c=connection.MmConnectEach().translate )
        cmds.menuItem( l='rotate', rp='NE',  c=connection.MmConnectEach().rotate )
        
        cmds.menuItem( l='Scale Shear', rp='E', sm=1 )
        cmds.menuItem( l='scale', rp='E', c=connection.MmConnectEach().scale )
        cmds.menuItem( l='shear', rp='SE', c=connection.MmConnectEach().shear )
        cmds.setParent( '..', menu=1 )
        
        cmds.menuItem( l='Sel Target', rp='SE', sm=1 )
        cmds.radioMenuItemCollection()
        cmds.menuItem( l='Sel Original',radioButton= model.RigToolInfo._selOriginal, c=setConnectionTypeOriginal  )
        cmds.menuItem( l='Sel Parent'  ,radioButton= model.RigToolInfo._selParent, c=setConnectionTypeParent  )
        cmds.setParent( '..', menu=1 )
        
        cmds.menuItem( l='local Connect', rp='S', c=connection.MmConnectEach().localTransform )
        cmds.menuItem( l='Constraint', rp='SW', c=connection.MmConnectEach().constraint )
        cmds.menuItem( l='Const Orient', rp='W', c=connection.MmConnectEach().constraintOrient )
        
        cmds.menuItem( l='Connect All', rp='NW', sm=1 )
        cmds.menuItem( l='translate', rp='N', c=connection.MmConnectAll().translate )
        cmds.menuItem( l='rotate', rp='NE',  c=connection.MmConnectAll().rotate )
        cmds.menuItem( l='scale', rp='E', c=connection.MmConnectAll().scale )
        cmds.menuItem( l='shear', rp='SE', c=connection.MmConnectAll().shear )
        cmds.menuItem( l='local Connect', rp='S', c=connection.MmConnectAll().localTransform )
        cmds.menuItem( l='Constraint', rp='SW', c=connection.MmConnectAll().constraint )
        cmds.menuItem( l='Const Orient', rp='W', c=connection.MmConnectAll().constraintOrient )
        cmds.setParent( '..', menu=1 )
        
        cmds.menuItem( l='Aim Object Connect', c=connection.mmAimObjectConnect )
        cmds.menuItem( l='Blend Two Matrix Connect', c=connection.mmLocalBlendMatrixConnect )
        cmds.menuItem( l='Switch Vis Connect', c=connection.mmSwitchVisConnection )
        cmds.menuItem( l='Get Local mm node', c=connection.mmGetChildMatrix )
        cmds.menuItem( l='Get Local mmdc node', c=connection.mmGetChildDecompose )
        cmds.menuItem( l='Replace by Target', c=connection.mmReplaceByTarget )
        cmds.menuItem( l='Replace connections', c=connection.mmReplaceConnections )
        cmds.menuItem( l='Optimize connections', c=sgRigConnection.mc_optimizeConnection )
        
    


    def createNodesMenu(self, rp=None ):
        
        self.defaultSetting( 'Create Nodes', rp )
        cmds.menuItem( l='decomposeMatrix', c=createNodes.mmDecomposeMatrix )
        cmds.menuItem( l='multMatrixDecompose', c=createNodes.mmMultMatrixDcmp )
        cmds.menuItem( l='shoulderOrient', c=createNodes.mmShoulderOrient )
        cmds.menuItem( l='fourByfourMatrix', c=createNodes.mmFourByFourMatrix )
        cmds.menuItem( l='wristAngle', c=createNodes.mmWristAngle )
        
        
        
    def deformMenu(self, rp=None ):
        
        self.defaultSetting( 'Deformer', rp )
        cmds.menuItem( l='Sliding Deformer', c=deform.mmCreateSlidingDeformer )
