import maya.cmds as cmds
import allCtlsMenu
import initCtlsCmd
from functools import partial

class InitCTL( allCtlsMenu.CTL_basic ):
    def __init__(self, parentUi, sels ):
        allCtlsMenu.CTL_basic.__init__(self, parentUi, sels )
        
        self.initCtlCmd = initCtlsCmd.Main()
        self.sels = sels
        self.target = sels[-1]
        self.other = ''
        if len( sels ) > 1:
            self.other = sels[-2]
        if not self.other: self.other = self.target
        
    def openMenu(self):
        self.mirrorMenu()
        self.showMenu()
        
    def mirrorMenu(self):
        cmds.setParent( self.parentUi, menu=1 )
        cmds.menuItem( l='Mirror <<', rp='W', c=partial( self.initCtlCmd.mirrorLtoR, self.target ) )
        cmds.menuItem( l='Mirror >>', rp='E', c=partial( self.initCtlCmd.mirrorRtoL, self.target ) )
        
    def showMenu(self):
        cmds.setParent( self.parentUi, menu=1 )
        if self.initCtlCmd.showAllCondition(self.target):
            cmds.menuItem( l='Show Selected Hierarchy', rp='N', c=partial( self.initCtlCmd.showTargetHierarchy, self.target ) )
        else:
            cmds.menuItem( l='Show All Init Controler', rp='N', c=partial( self.initCtlCmd.showAll, self.target ) )
        cmds.menuItem( l='Hide Selected Hierarchy', rp='S', c=partial( self.initCtlCmd.hideSelectedHierarchy, self.sels ) )
        
class All_InitCTL( InitCTL ):
    def openMenu(self):
        self.mirrorMenu()
        self.conAndDisconMenu()
        
    def conAndDisconMenu(self):
        if self.target == self.other and not cmds.objExists( self.getNamespace( self.target )+'All_Init' ): return None
        if self.initCtlCmd.isConnect( self.target ):
            cmds.menuItem( l='Disonnect Init', rp='S', parent = self.parentUi, c= partial( self.initCtlCmd.disConnect, self.target ) )
        else:
            cmds.menuItem( l='Connect Init', rp='S', parent = self.parentUi, c= partial( self.initCtlCmd.connect, self.target, self.other ) )
        #cmds.menuItem( l='Create Mocap Joint', parent = self.parentUi, c=partial( self.initCtlCmd))