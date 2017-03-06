import maya.cmds as cmds

import uiModel
import cmdModel



def addAttrUiPart( parentUi, columnWidth, *args ):
    
    beforeParent = cmds.setParent( q=1 )
    cmds.setParent( parentUi )
    
    halfWidth = ( columnWidth -2 )*0.5
    otherHalfWidth = ( columnWidth-2 ) - halfWidth
    firstLabelWidth = halfWidth * 0.45
    firstFieldWidth = halfWidth - firstLabelWidth
    secondLabelWidth = otherHalfWidth * 0.45
    secondFieldWidth = otherHalfWidth - secondLabelWidth
    
    cmds.rowColumnLayout( nc=4, cw=[(1,firstLabelWidth),(2,firstFieldWidth),(3,secondLabelWidth),(4,secondFieldWidth)] )
    cmds.text( l='Source : ', al='right' )
    fieldSrc  = cmds.textField()
    cmds.text( l='Dest : ', al='right' )
    fieldDest = cmds.textField()
    
    cmds.setParent( beforeParent )
    
    return fieldSrc, fieldDest

    
    


class Window:
    
    def __init__(self):

        self.winName = uiModel.winName
        self.title   = uiModel.title
        self.width   = uiModel.width
        self.height  = uiModel.height

        self.fieldSrc  = []
        self.fieldDest = []
        
            
    def appendAttrPartUI(self, *args ):
        
        fieldSrc, fieldDest = addAttrUiPart( self.attrPartRowColumn, self.width-2 )
        self.fieldSrc.append( fieldSrc )
        self.fieldDest.append( fieldDest )
        


    def cmdConnect(self, *args ):

        selIndex = cmds.optionMenu( self.optionMenu, q=1, sl=1 )

        if selIndex == 1:
            cmdModel.uiCmd_connectObjectMulti( self.fieldSrc, self.fieldDest )


    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title )
        
        column = cmds.columnLayout()
        cmds.text( l='', h=5 )
        firstWidth =( self.width -2 )*0.4
        secondWidth = ( self.width -2 )*0.3
        thirdWidth  = self.width-2 - firstWidth - secondWidth
        
        optionRowColumn = cmds.rowColumnLayout( nc=3, cw=[(1,firstWidth),(2,secondWidth),(3,thirdWidth)] )
        cmds.setParent( '..' )
        attrPartRowColumn = cmds.rowColumnLayout( nc=1, cw=[(1,self.width)] )
        cmds.setParent( '..' )
        buttonPartRowColumn = cmds.rowColumnLayout( nc=1, cw=[(1,self.width-2)])
        
        cmds.setParent( optionRowColumn )
        cmds.text( l='Connection Type : ', al='right' )
        optionMenu = cmds.optionMenu( h=23 )
        cmds.menuItem( l='Multi' )
        cmds.menuItem( l='Separate' )
        cmds.button( l='Append', c=self.appendAttrPartUI )
        cmds.setParent( '..' )
        
        fieldSrc, fieldDest = addAttrUiPart( attrPartRowColumn, self.width-2 )
        self.fieldSrc.append( fieldSrc )
        self.fieldDest.append( fieldDest )
        
        cmds.setParent(buttonPartRowColumn)
        cmds.button( l='Connect', c=self.cmdConnect )
        
        cmds.window( self.winName, e=1,
                     w = self.width, h = self.height )
        cmds.showWindow( self.winName )

        self.column = column
        self.optionMenu = optionMenu
        self.attrPartRowColumn = attrPartRowColumn