import maya.cmds as cmds

import uiModel
import cmdModel


def addPopup( cmd ):

    cmds.popupMenu()
    cmds.menuItem( l='Load Selection', c= cmd )



class Window:
    
    def __init__(self):
        
        self.winName = uiModel.winName
        self.title   = uiModel.title
        self.width   = uiModel.width
        self.height  = uiModel.height
    
    
    def loadLeftWing(self, *args ):
        
        selTarget = cmds.ls( sl=1 )[-1]
        if selTarget.find( 'CtlIk_Wing_L1_02' ) != -1:
            cmds.textField( self.fieldLeft, e=1, tx= selTarget )
            cmds.textField( self.fieldRight, e=1, tx= selTarget.replace( '_L1_', '_R1_' ) )
            cmdModel.loadRelativeCtls( selTarget )
        else:
            cmds.warning( 'Select "CtlIk_Wing_L1_02"' )
    
    
    
    def loadRightWing(self, *args ):
        
        selTarget = cmds.ls( sl=1 )[-1]
        if selTarget.find( 'CtlIk_Wing_R1_02' ) != -1:
            cmds.textField( self.fieldLeft, e=1, tx= selTarget.replace( '_R1_', '_L1_' )  )
            cmds.textField( self.fieldRight, e=1, tx= selTarget )
            cmdModel.loadRelativeCtls( selTarget )
        else:
            cmds.warning( 'Select "CtlIk_Wing_R1_02"' )
            
            
            
    def setMirrorLtoR(self, *args ):
        
        cmdModel.setMirrorObjectLtoR()
        
        
    def setMirrorRtoL(self, *args ):
        
        cmdModel.setMirrorObjectRtoL()
        
        
        
    def mirrorSelected(self, *args ):
        
        for sel in cmds.ls( sl=1 ):
            cmdModel.setMirrorObjectOnce( sel )
            
            
            
    def copyKeyLtoR(self, *args ):
        
        minFrame = cmds.floatField( self.minFrame, q=1, v=1 )
        maxFrame = cmds.floatField( self.maxFrame, q=1, v=1 )
        cmdModel.keyCopyObjectLtoR( minFrame, maxFrame )
    
    def copyKeyRtoL(self, *args ):
        
        minFrame = cmds.floatField( self.minFrame, q=1, v=1 )
        maxFrame = cmds.floatField( self.maxFrame, q=1, v=1 )
        cmdModel.keyCopyObjectRtoL( minFrame, maxFrame )
        
    def copySelected(self, *args ):
        
        minFrame = cmds.floatField( self.minFrame, q=1, v=1 )
        maxFrame = cmds.floatField( self.maxFrame, q=1, v=1 )
        for sel in cmds.ls( sl=1 ):
            cmdModel.keyCopyObjectOnce(sel, minFrame, maxFrame)
    
    
    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title )
        
        cmds.columnLayout()
        columnWidth = self.width-2
        leftWidth = ( columnWidth -2 )*0.5
        rightWidth = ( columnWidth -2 ) - leftWidth
        cmds.rowColumnLayout( nc=2, cw=[(1,leftWidth),(2,rightWidth)])
        cmds.text( l='Right Wing' );cmds.text( l='Left Wing')
        fieldRight = cmds.textField()
        addPopup( self.loadRightWing )
        fieldLeft = cmds.textField()
        addPopup( self.loadLeftWing )
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=2, cw=[(1,leftWidth),(2,rightWidth)])
        cmds.button( l='Mirror R to L >>', c=self.setMirrorRtoL )
        cmds.button( l='<< Mirror L To R', c=self.setMirrorLtoR )
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=1, cw=(1,columnWidth) )
        cmds.button( l='Mirror Selected', c=self.mirrorSelected )
        cmds.setParent( '..' )
        
        cmds.text( l='', h=5 )
        
        textWidth = ( columnWidth-2 )*0.4
        f1Width = ( ( columnWidth -2 ) - textWidth )*0.5
        f2Width = ( columnWidth-2 ) - textWidth - f1Width
        cmds.rowColumnLayout( nc=3, cw=[(1,textWidth),(2,f1Width),(3,f2Width)])
        cmds.text( l='Frame Range : ' )
        minFrame = cmds.floatField( v=1.0, pre=2 )
        maxFrame = cmds.floatField( v=24.0, pre=2 )
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=2, cw=[(1,leftWidth),(2,rightWidth)])
        cmds.button( l='Copy Key R to L >>', c=self.copyKeyRtoL )
        cmds.button( l='<< Copy Key L To R', c=self.copyKeyLtoR )
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=1, cw=(1,columnWidth) )
        cmds.button( l='Copy Selected', c=self.copySelected )
        cmds.setParent( '..' )
        
        cmds.window( self.winName, e=1,
                     w = self.width, h = self.height )
        cmds.showWindow( self.winName )
        
        self.fieldLeft = fieldLeft
        self.fieldRight = fieldRight
        self.minFrame = minFrame
        self.maxFrame  = maxFrame