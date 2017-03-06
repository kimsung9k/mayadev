import maya.cmds as cmds
import sgRigConnection
import sgRigSpline 
import sgUISetAttr
import sgUIReloadModules


class ControllerMenu:
    
    def __init__(self, parentUiName ):
        
        cmds.setParent( parentUiName, menu=1 )

        cmds.menuItem( l='Constraint', c=sgRigConnection.mc_constraint )
        cmds.menuItem( l='Constraint All', c=sgRigConnection.mc_constraintAll )
        cmds.menuItem( l='Constraint To Parent', c=sgRigConnection.mc_constraintToParent )
        cmds.menuItem( l='Connect Local MMDC',  c=sgRigConnection.mc_connectLocalMMDC_toTarget )
        cmds.menuItem( l='Connect Local MMDC To Parent', c=sgRigConnection.mc_connectLocalMMDC_toParent )
        cmds.menuItem( l='Connect Blend Two Matrix', c=sgRigConnection.mc_connectBlendTwoMatrix )
        cmds.menuItem( l='Connect Blend Two Matrix( keep Position )', c=sgRigConnection.mc_connectBlendTwoMatrix_keepPosition )
        cmds.menuItem( l='C Blend Two Mtx( keep Pos, skip second Trans )', c=sgRigConnection.mc_connectBlendTwoMatrix_keepPositionAndSkipSecondTrans )



class SetMenu:
    
    def __init__(self, parentUiName ):
        
        cmds.setParent( parentUiName, menu=1 )
        cmds.menuItem( l='UI Set Attr', c= sgUISetAttr.mc_showWindow )



class RigSetMenu:
    
    def __init__(self, parentUiName ):
        
        cmds.setParent( parentUiName, menu=1 )
        cmds.menuItem( l='Create Spline Rig Set', c= sgRigSpline.mc_createControlInJointLine )


    
class SystemMenu:
    
    def __init__(self, parentUiName ):
        
        cmds.setParent( parentUiName, menu=1 )
        cmds.menuItem( l='UI Reload Modules', c= sgUIReloadModules.mc_showWindow )



class MyMenu:

    def __init__(self):

        self.uiname = 'sgMyMenu'
        self.title  = 'MY MENU'


    def create(self):

        if cmds.menu( self.uiname, ex=1 ):
            cmds.deleteUI( self.uiname )
        cmds.menu( self.uiname, l= self.title, p='MayaWindow', to=1 )
        
        return self.uiname



def showMyMenu():
    
    parentUi = MyMenu().create()
    ControllerMenu( parentUi )
    RigSetMenu( parentUi )
    SetMenu( parentUi )
    SystemMenu( parentUi )