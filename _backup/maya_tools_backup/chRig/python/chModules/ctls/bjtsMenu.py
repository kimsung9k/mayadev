import maya.cmds as cmds
import allCtlsMenu
import bjtsCmd
from functools import partial

import chModules.driverSet.set as driverSet
import chModules.driverSet.bjtDriverSet as bjtDriverSet

class BJT( allCtlsMenu.CTL_basic ):
    def __init__(self, parentUi, sels ):
        allCtlsMenu.CTL_basic.__init__( self, parentUi, sels )
        self.bjtsCmdMain = bjtsCmd.BJT_Main()
        self.defaultAble = cmds.attributeQuery( 'parameter', node=sels[-1], ex=1 )
    
    def openMenu(self):
        if self.defaultAble:
            self.defaultMenu()
            self.mirrorAllMenu()
        self.addMidBjtMenu()
        self.selectMenu()
        
    def defaultMenu(self):
        cmds.setParent( self.parentUi, menu=1 )
        cmds.menuItem( l='Default Parameter', rp='N', c= partial( self.bjtsCmdMain.defaultParam, self.sels ) )
        cmds.menuItem( l='Default Parameter All', rp='S', c= partial( self.bjtsCmdMain.defaultParamAll, self.sels[-1] ) )
    
    def mirrorAllMenu(self):
        cmds.setParent( self.parentUi, menu=1 )
        cmds.menuItem( l='Mirror All <<', rp='W',c= partial( self.bjtsCmdMain.mirrorParamLToR, self.sels[-1] ) )
        cmds.menuItem( l='Mirror All >>', rp='E',c= partial( self.bjtsCmdMain.mirrorParamRToL, self.sels[-1] ) )
        
    def addMidBjtMenu(self):
        cmds.setParent( self.parentUi, menu=1 )
        cmds.menuItem( l='Add Middle Joint', c= partial( self.bjtsCmdMain.addMiddleJoint, self.sels ) )
        
    def selectMenu(self):
        cmds.setParent( self.parentUi, menu=1 )
        cmds.menuItem( l='Select Bind Joints', c= partial( self.bjtsCmdMain.selectBjts, self.sels[-1] ) )

        
class BJT_World( BJT ):
    def __init__(self, parentUi, sels ):
        BJT.__init__( self, parentUi, sels )
        self.bjtWorldCmdMain = bjtsCmd.BJT_World_Main()
        self.isConnected = self.bjtWorldCmdMain.isConnected( sels[-1] )
        
    def openMenu(self):
        self.disconnectMenu()
        self.selectMenu()
        self.driverSetMenu()
        
    def disconnectMenu(self):
        cmds.setParent( self.parentUi, menu=1 )
        if self.isConnected:
            cmds.menuItem( l='Disconnect Joint', c = partial( self.bjtWorldCmdMain.disconnect, self.sels[-1] ) )
        else:
            cmds.menuItem( l='Connect Joint',c = partial( self.bjtWorldCmdMain.connect, self.sels ) )


    def driverSetMenu(self):
        cmds.setParent( self.parentUi, menu=1 )
        
        ns = self.sels[-1].replace( 'BJT_World', '' )
        
        driverSet.bjtDriverSet( ns )
        
        if cmds.reference( self.sels[-1], inr=1 ): return None
        
        if not driverSet.isConnected( self.sels[-1] ):
            cmds.menuItem( l='Create Driver Joint', c= partial( driverSet.setConnect, ns ), rp='N' )
        else:
            cmds.menuItem( l='Delete Driver Joint', c= partial( driverSet.setDisconnect, ns ), rp='N' )