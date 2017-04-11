import maya.cmds as cmds
import model

import basic.goTo.cmdModel as goToCmdModel
import joint.cmdModel as jointCmdModel
import curve.cmdModel as curveCmdModel
import skinCluster.cmdModel as skinClusterCmdModel


class Create:
    
    def __init__(self, parentMenu, *args ):
        
        self._parentMenu = parentMenu
        
        cmds.popupMenu( self._parentMenu, e=1, deleteAllItems=1 )
        
        self.goToMenu( 'N' )
        self.jointMenu( 'W' )
        self.curveMenu( 'NW' )
        self.skinClusterMenu( 'NE' )
        
        
        
    def defaultSetting(self, name, rp=None ):
        
        cmds.setParent( self._parentMenu, menu=1 )
        if rp: cmds.menuItem( l=name, rp=rp, sm=1 )
        else: cmds.menuItem( l=name, sm=1 )
        
        
        
    def divider(self):
        
        cmds.setParent( self._parentMenu, menu=1 )
        cmds.menuItem( d=1 )
    
    
    def goToMenu(self, rp=None ):
        
        self.defaultSetting( 'Go to', rp )
        cmds.menuItem( l='Go To Target', rp='N', c=goToCmdModel.uiCmd_goToTarget )
        cmds.menuItem( l='Go To Target Position', rp='N', c=goToCmdModel.uiCmd_goToTargetPosition )
        cmds.menuItem( l='Go To Target Orient', rp='N', c=goToCmdModel.uiCmd_goToTargetOrient )
        
        
    def jointMenu(self, rp=None ):
        
        self.defaultSetting( 'Joint Menu', rp )
        cmds.menuItem( l='Add Middle Joint UI', rp='NE', c=jointCmdModel.uiCmd_openCreateMiddleJoint_ui )
        cmds.menuItem( l='Connect Matrix To Joint Orient', rp='N', c=jointCmdModel.uiCmd_connectMatrixToJointOrient )
        
        
        
    def curveMenu(self, rp=None ):
        
        self.defaultSetting( 'Curve', rp )
        cmds.menuItem( l='Create Edit Point Curve', rp='N', c=curveCmdModel.uiCmd_createEpCurve )
        cmds.menuItem( l='Create Spline Curve Each Spans', rp='NW', c=curveCmdModel.uiCmd_createSplineJointEachSpans )
        
        
    def skinClusterMenu(self, rp=None ):
        
        self.defaultSetting( 'Skin Cluster', rp)
        cmds.menuItem( l='Connect Bind Pre Matrix', rp='N', c=skinClusterCmdModel.uiCmd_connectBindPreMatrix )