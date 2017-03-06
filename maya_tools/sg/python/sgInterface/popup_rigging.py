import maya.cmds as cmds
import command.connect
import command.dag
import command.transform
import command.naming
import command.rig
import sgPlugin


def create( parent ):
    
    menuPutObject = cmds.menuItem( l="Put Object", rp='N', p=parent, sm=1 )
    cmds.menuItem( l="Put Joint", rp='N', c= command.dag.putJoint )
    cmds.menuItem( l="Put Locator", rp='NW', c= command.dag.putLocator )
    cmds.menuItem( l="Put NULL", rp='NE', c= command.dag.putNull )
    cmds.menuItem( l="Put Each", rp='E', sm=1, p=menuPutObject )
    cmds.menuItem( l="Put Joints", rp='N', c= command.dag.putJoints )
    cmds.menuItem( l="Put Locators", rp='NW', c= command.dag.putLocators )
    cmds.menuItem( l="Put NULLs", rp='NE', c= command.dag.putNulls )
    cmds.menuItem( l='Put Object And Constraint', rp='S', c= command.dag.putAndConstraintJoints )
    cmds.menuItem( l="Put child", rp='S', sm=1, p=menuPutObject )
    cmds.menuItem( l='Put Child Null', rp='SE', c= command.dag.putChild )
    cmds.menuItem( l='Put Child Joint', rp='S', c= command.dag.putChildJoint )
    cmds.menuItem( l='Put Child Locator', rp='SW', c= command.dag.putChildLocator )
    cmds.menuItem( l='Tool', rp='W', sm=1, p=menuPutObject )
    cmds.menuItem( l='Tool - Put Follicle', rp='W', c= sgPlugin.setTool_putFollicleContext )
    cmds.menuItem( l='Tool - Put Inside', rp='SW', c= sgPlugin.setTool_putInsideContext )
    
    cmds.menuItem( l="Get", rp='NW', p=parent, sm=1 )
    cmds.menuItem( l="Get Angle", rp='N', c=command.connect.getAngle )
    cmds.menuItem( l="Get Distance", rp='NE', c=command.connect.getDistance )
    cmds.menuItem( l="Get FBF Matrix", rp='W', c=command.connect.getRotationMatrix )
    cmds.menuItem( l="Get DecomposeMatrix", rp='NW', c= command.connect.getDecomposeMatrix )
    cmds.menuItem( l="Get Cross Vector", rp="E", c= command.connect.getCrossVectorNode )
    cmds.menuItem( l='Get Local Matrix', rp='S', c = command.connect.getLocalMatrix )
    cmds.menuItem( l='Get Local Matrix Decompose', rp='SW', c = command.connect.getLocalMatrixDecompose )

    miDag = cmds.menuItem( l='Dag', rp='W', p=parent, sm=1 )
    cmds.menuItem( l='Make Parent', rp='N', c = command.dag.makeParent )
    cmds.menuItem( l='Parent Selected Older', rp='E', c= command.dag.parentSelectedOlder )
    cmds.menuItem( l="Copy Children", rp="W", c=command.dag.copyChildren )

    miConnection = cmds.menuItem( l="Connection", rp='SW', p=parent, sm=1 )
    cmds.menuItem( l="Look At", rp='N', c= command.connect.lookAt )
    cmds.menuItem( l='Constraint', rp='NW', p=miConnection, sm=1 )
    cmds.menuItem( l="Point",  rp='NW', c= command.connect.constrain_point )
    cmds.menuItem( l="Orient",  rp='W', c= command.connect.constrain_orient )
    cmds.menuItem( l="Parent", rp='SW', c= command.connect.constrain_parent )
    cmds.menuItem( l='Blend Matrix', rp='W', p=miConnection, sm=1 )
    cmds.menuItem( l='Blend Two Matrix', rp='NW', c= command.connect.setBlendTwoMatrixConnection )
    cmds.menuItem( l='Add Blend Matrix Connect', rp='W', c= command.connect.addBlendMatrix )
    cmds.menuItem( l='Add Blend Matrix Connect - mo', rp='SW', c=command.connect.addBlendMatrix_mo )
    cmds.menuItem( l='Node Editor', rp='SW', p=miConnection, sm=1 )
    cmds.menuItem( l='Get Source Connection', rp='W', c= command.connect.getSourceConnection )
    cmds.menuItem( l='Optimize Connection', rp='SW', c= command.connect.opptimizeConnection )
    cmds.menuItem( l='replace', rp='S', c= command.connect.replaceConnection )
    
    miRig = cmds.menuItem( l='Rig', rp='SE', p=parent, sm=1 )
    cmds.menuItem( l="Make Mirror", rp="N", c=command.rig.makeMirror )
    cmds.menuItem( l="Reverse Angle", rp="SE", c=command.rig.setAngleReverse )
    cmds.menuItem( l="Reverse Position", rp="S", c=command.rig.reversePosition )
    cmds.menuItem( l="Copy Rig", rp="E", c=command.rig.copyRig )
    
    cmds.menuItem( l="Set Position", rp="NE", p=parent, sm=1 )
    cmds.menuItem( l="Set Orient By child", rp='SW', c= command.transform.setOrientByChild )
    cmds.menuItem( l='Set Orient By Target', rp='W', c= command.transform.setOrientAsTarget )
    cmds.menuItem( l='Set Center', rp='NE', c= command.transform.setCenter )
    cmds.menuItem( l='Set Mirror', rp='E', c= command.transform.setMirror )
    cmds.menuItem( l='Go to Target', rp='N', c = command.transform.setTransformAsTarget )
    
    cmds.menuItem( l="Freeze", rp='SW', p=parent, sm=1 )
    cmds.menuItem( l="Freeze Orient", rp='W', c= command.transform.freezeJoint )
    cmds.menuItem( l="Set Joint Orient Zero", rp="NW", c= command.transform.setJointOrientZero )
    cmds.menuItem( l="Freeze by Parent", rp='SW', c= command.transform.freezeByParent )

    cmds.menuItem( l="Naming", rp="E", sm=1, p=parent )
    cmds.menuItem( l="Rename Sel Older", rp='N', c= command.naming.renameSelOlder )
    cmds.menuItem( l="Rename Parent", rp="SE", c= command.dag.renameParent )
    cmds.menuItem( l="Rename Other Side", rp="E", c= command.dag.renameOtherSide )
    
    cmds.menuItem( l="Controller", sm=1, p=parent )
    cmds.menuItem( l="Circle" )
    cmds.menuItem( l="Cube" )
    cmds.menuItem( l="Diamond" )
    
    