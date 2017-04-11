import maya.cmds as cmds

import functions.autoLoadPlugin

import uiModel
import cmdModel

class Window:
    
    def __init__(self):
        
        self.winName = uiModel.winName
        self.title   = uiModel.title
        self.width   = uiModel.width
        self.height  = uiModel.height
        self.buttonHeight = uiModel.buttonHeight
        
        functions.autoLoadPlugin.AutoLoadPlugin().load( 'sgRigAdditionalNodes' )
    
    
    def cmdCreate(self, *args ):
        
        axisIndex = cmds.optionMenuGrp( self.optionMenu, q=1, sl=1 )-1
        inverseAim = cmds.checkBoxGrp( self.checkInverseAim, q=1, value1=1 )
        displayAxis = cmds.checkBoxGrp( self.checkDisplayAxis, q=1, value1=1 )
        #worldPosition = cmds.checkBoxGrp( self.checkWorldPosition, q=1, value1=1 )
        cmdModel.uiCmd_createAimObject(axisIndex, inverseAim, displayAxis, True )
    
    
    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title )
        
        cmds.columnLayout()
        
        columnWidth = self.width - 2
        firstTextWidth = columnWidth * 0.4
        secondTextWidth = columnWidth * 0.4
        firstHalfWidth = columnWidth * 0.5
        secondHalfWidth = columnWidth * 0.5
        cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)] )
        cmds.text( l='', h=5 )
        optionMenu = cmds.optionMenuGrp( l='Aim Axis : ', cw=[(1,firstTextWidth)] )
        cmds.menuItem( l='X'), cmds.menuItem( l='Y'), cmds.menuItem( l='Z')
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=2, cw=[(1,firstHalfWidth), (2,secondHalfWidth)])
        inverseAim   = cmds.checkBoxGrp( l='Inverse Aim : ', cw=[(1,firstTextWidth)] )
        displayAxis  = cmds.checkBoxGrp( l='Display Axis : ', cw=[(1,secondTextWidth)] )
        #worldPosition= cmds.checkBoxGrp( l='World Position : ', cw=[(1,secondTextWidth)] )
        cmds.setParent('..')
        cmds.text( l='', h=5 )
        
        cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)])
        cmds.button( l='Create', h=self.buttonHeight,
                     c=self.cmdCreate )
        
        cmds.window( self.winName, e=1,
                     w = self.width, h = self.height )
        cmds.showWindow( self.winName )
        
        self.optionMenu = optionMenu
        self.checkInverseAim = inverseAim
        self.checkDisplayAxis = displayAxis
        #self.checkWorldPosition = worldPosition