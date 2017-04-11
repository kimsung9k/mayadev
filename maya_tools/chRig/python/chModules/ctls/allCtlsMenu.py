import maya.cmds as cmds
import chModules.ui as ui
import allCtlsCmd
import chModules.jointBasePsd.ui.main as SkinEdit
import chModules.psd_jointBase.ui as psdUi
import chModules.retargetTool.ui as retargetUi
import chModules.retargetingCommandUI.main as retargetUi2
from ctlsAll import *
from functools import partial
import torsoCtlsCmd


class CTL_basic( CtlsAll ):
    def __init__( self, parentUi, sels ):
        self.sels = sels
        self.mainCmd = allCtlsCmd.CTL()
        cmds.popupMenu( 'locusChrigPopup', e=1, deleteAllItems=1 )
        self.mirrorType = 'object'
        self.parentUi = parentUi
        self.radialPosList = [ "N", "NE", "E", "SE", "S", "SW", "W", "NW" ]
        
        
    def openMenu(self):
        if not self.sels:
            self.locusChRigMenu()
        else:
            self.defaultMenu()
            self.mirrorMenu()
            self.flipMenu()
            self.selectMenu()
            self.addMenu()

        
    def locusChRigMenu(self):
        
        cmds.setParent( self.parentUi, menu=1 )
        cmds.menuItem( l='Locus Character UI', rp='N', c = ui.LocusHumanRig_ui )
        cmds.menuItem( l='Retarget UI', rp='W' , c = retargetUi.Show )
        cmds.menuItem( l='Retarget UI v2', rp='SW' , c = retargetUi2.Show )
        cmds.menuItem( l='Skined Shape Edit Tool', rp='E' , c = SkinEdit.Show )
        cmds.menuItem( l='PSD - Joint Base Tool', rp='SE' , c = psdUi.Show )

        
    def defaultMenu(self):
        cmds.setParent( self.parentUi, menu=1 )
        cmds.menuItem( l='Default Position', rp='S', sm=1 )
        cmds.menuItem( l='Default Selected', rp='SW', c= partial( self.mainCmd.setDefaultTransform, self.sels ) )
        cmds.menuItem( l='Default Hierarchy', rp='SE', c= partial( self.mainCmd.setDefaultTransformH, self.sels[-1] ) )
    

    def selectMenu(self):
        cmds.setParent( self.parentUi, menu=1 )
        
        
    def mirrorMenu(self):
        cmds.setParent( self.parentUi, menu=1 )
        cmds.menuItem( l='Mirror', rp='N', sm=1 )
        cmds.menuItem( l='Mirror Selected', rp='N', c= partial( self.mainCmd.mirror, self.sels ) )
        cmds.menuItem( l='Mirror Hierarchy >>', rp='NE', c= partial( self.mainCmd.mirrorH, self.sels[-1], 'L' ) )
        cmds.menuItem( l='<< Mirror Hierarchy', rp='NW', c= partial( self.mainCmd.mirrorH, self.sels[-1], 'R' ) )
        

    def flipMenu(self):
        cmds.setParent( self.parentUi, menu=1 )
        cmds.menuItem( l='Flip', rp='NE', sm=1 )
        cmds.menuItem( l='Flip Selected', rp='N', c= partial( self.mainCmd.flip, self.sels ) )
        cmds.menuItem( l='Flip Hierarchy', rp='NE', c= partial( self.mainCmd.flipH, self.sels[-1] ) )


    def addMenu(self):
        cmds.setParent( self.parentUi, menu=1 )
        if len( self.sels ) == 2:
            transformAttrList = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ']
            
            transformExist = False
            for attr in cmds.listAttr( self.sels[0], k=1 ):
                if attr in transformAttrList:
                    transformExist = True
                    break
            
            if transformExist:
                cmds.menuItem( l='Go To Target', rp='SW', c=partial( self.mainCmd.goToObject, self.sels[0], self.sels[1] ) )
        else:
            cmds.menuItem( l='Select Hierarchy', rp='SW', c= partial( self.mainCmd.selectH, self.sels[-1] ) )
        
        if self.sels[-1].find( '_R_' ) != -1 or self.sels[-1].find( '_L_' ):
            cmds.menuItem( l='Mirror Shape' , c=partial( self.mainCmd.mirrorShape, self.sels[-1] ))



class World_CTL( CTL_basic ):

    def __init__( self, parentUi, sels ):
        CTL_basic.__init__( self, parentUi, sels )
        self.mainCmd = allCtlsCmd.World_CTL()
        
    def openMenu(self):
        self.prefixMenu()
        self.defaultMenu()
        self.selectMenu()
        self.mocapMenu()
        
        
    def prefixMenu(self):
        
        if cmds.reference( self.sels[-1], inr=1 ): return None
        
        cmds.setParent( self.parentUi, menu=1 )
        cmds.menuItem( l='Add Prefix Name', rp='N', c= partial( self.mainCmd.AddNameSpace, self.sels[-1] ) )
        
        
    def mocapMenu(self):
        cmds.setParent( self.parentUi, menu=1 )
        
        if not self.mainCmd.mocExists( self.sels[-1] ):
            cmds.menuItem( l='Create Mocap Joint', c= partial( self.mainCmd.createMocapJoint, self.sels[-1] ) )
            cmds.menuItem( l='Create Mocap Joint With Skin', c= partial( self.mainCmd.createMocapJoint, self.sels[-1], True ) )
            return None
        
        if len( self.sels ) == 1:
            if self.mainCmd.isMocConnected( self.sels[-1] ):
                cmds.menuItem( l='Disconnect Mocap Joint', c=partial( self.mainCmd.disconnectMocapJoint, self.sels[-1] ) )
        else:
            if self.mainCmd.isAllMoc( self.sels[-2] ):
                if self.mainCmd.isMocConnected( self.sels[-1] ):
                    cmds.menuItem( l='Disconnect Mocap Joint', c=partial( self.mainCmd.disconnectMocapJoint, self.sels[-1] ) )
                else:
                    cmds.menuItem( l='Connect Mocap Joint', c=partial( self.mainCmd.connectMocapJoint, self.sels[-2], self.sels[-1] ) )



class All_Moc( CTL_basic ):

    def __init__( self, parentUi, sels ):
        CTL_basic.__init__( self, parentUi, sels )
        self.mainCmd = allCtlsCmd.All_Moc()
        
        self._target = self.sels[-1]
        
    def openMenu(self):
        cmds.setParent( self.parentUi, menu=1 )
        
        retargetNodes = cmds.listConnections( self._target+'.worldMatrix', type='HIKRetargeterNode' )
        
        if retargetNodes:
            if self.mainCmd.isMatchSource( self._target ):
                cmds.menuItem( l='Set Original', c=partial( self.mainCmd.setNotMatchSource, self._target ) )
            else:
                cmds.menuItem( l='Set Match Source', c=partial( self.mainCmd.setMatchSource, self._target ) )
            cmds.menuItem( l='Export HumanIK', c=partial( self.mainCmd.exportHIk, self._target ) )
        else:
            if self.mainCmd.isHIKCharacter( self._target ):
                cmds.menuItem( l='Delete HumanIK', c=partial( self.mainCmd.removeHumanIkCharacter, self._target ) )
            else:
                cmds.menuItem( l='Set HumanIK', c=partial( self.mainCmd.createCharacter, self._target ) )
        