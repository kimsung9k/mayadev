import maya.cmds as cmds
import chModules.ui as ui
import allCtlsMenu
import armandlegCtlsCmd
from functools import partial

CTL_basic = allCtlsMenu.CTL_basic

class IK_CTL( CTL_basic ):
    def __init__( self, parentUi, sels ):
        CTL_basic.__init__( self, parentUi, sels )
        self.ikCmd = armandlegCtlsCmd.IK_CTL()
        
    def openMenu(self):
        self.defaultMenu()
        self.mirrorMenu()
        self.flipMenu()
        self.followMenu()
        self.addMenu()

    def followMenu(self):
        target = self.sels[-1]
        switchCtl= target.replace( 'IK_CTL', 'Switch_CTL' ).replace( '_Foot', '' )
        attrs = cmds.listAttr( switchCtl, ud=1, k=1 )
        cmds.setParent( self.parentUi, menu=1 )
        cmds.menuItem( l='Follow', rp='E', sm=1 )
        index = 0
        cmds.menuItem( l='None Follow', rp=self.radialPosList[0], c=partial( self.ikCmd.noneFollow, switchCtl ) )
        for attr in attrs:
            if attr.find( 'Follow' ) != -1:
                if attr != 'pinFollow':
                    commend = partial( self.ikCmd.setFollow, switchCtl, attr )
                else:
                    commend = partial( self.ikCmd.pinFollow, switchCtl )
                labelName = attr.capitalize().replace( 'follow', ' Follow' )
                
                cmds.menuItem( l=labelName, rp=self.radialPosList[index+1], c=commend )
                
                index += 1
    
    def otherMenu(self):
        pass


class FK_CTL( CTL_basic ):
    
    def __init__(self, parentUi, sels ):
        CTL_basic.__init__( self, parentUi, sels )
        self.fkCmd = armandlegCtlsCmd.FK_CTL()
    
    def openMenu( self ):
        self.defaultMenu()
        self.mirrorMenu()
        self.flipMenu()
        self.addMenu()
        self.selectMenu()
    
    def selectMenu(self):
        target = self.sels[-1]
        command = partial( self.fkCmd.selectFks, target )
        cmds.menuItem( l="Select FKs", rp='W', c=command )

    
class Switch_CTL( CTL_basic ):
    def __init__(self, parentUi, sels ):
        CTL_basic.__init__( self, parentUi, sels )
        self.switchCmd = armandlegCtlsCmd.Switch_CTL(self.sels[-1])
        
    def openMenu(self):
        self.switchMenu()
        self.addMenu()
        
    def switchMenu(self):
        cmds.setParent( self.parentUi, menu=1 )
        cmds.menuItem( l='Fk Switch', rp='W', c= self.switchCmd.setFk )
        cmds.menuItem( l='Ik Swtich', rp='SW', c= self.switchCmd.setIk )
