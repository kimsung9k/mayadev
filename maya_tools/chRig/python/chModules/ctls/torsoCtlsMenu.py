import maya.cmds as cmds
import allCtlsMenu
import torsoCtlsCmd
from functools import partial

CTL_basic = allCtlsMenu.CTL_basic


class Fly_CTL( CTL_basic ):
    
    def __init__(self, parentUi, sels ):
        CTL_basic.__init__( self, parentUi, sels )
        self.torsoCmd = torsoCtlsCmd.Fly_CTL() 
        
        
    def openMenu(self):
        self.defaultMenu()
        self.mirrorMenu()
        self.flipMenu()
        self.forRootMenu()
        self.addMenu()
        
    def forRootMenu(self):
        cmds.setParent( self.parentUi, menu=1 )
        cmds.menuItem( l=' @  ---->  R', c= partial( self.torsoCmd.goToRoot , self.sels[-1] ) )   
        cmds.menuItem( l=' +  ---->  R', c= partial( self.torsoCmd.setFlyControlPoint , self.sels[-1] ) )   


class Root_CTL( CTL_basic ):
    
    def __init__(self, parentUi, sels ):
        CTL_basic.__init__( self, parentUi, sels )
        self.torsoCmd = torsoCtlsCmd.Root_CTL()
        
    def openMenu(self):
        self.defaultMenu()
        self.selectMenu()
        self.mirrorMenu()
        self.flipMenu()
        self.forFlyMenu()
        self.addMenu()
        
    def forFlyMenu(self):
        cmds.setParent( self.parentUi, menu=1 )
        cmds.menuItem( l='R -----> + ', c= partial( self.torsoCmd.goToFlyControlPoint, self.sels[-1] ) )    