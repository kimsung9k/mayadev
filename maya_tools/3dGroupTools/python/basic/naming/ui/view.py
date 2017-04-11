from uiModel import *
from cmdModel import *
import UIs.button
import maya.cmds as cmds


class NumberingUI:
    
    def __init__(self):
        
        self._uiInstButton = UIs.button.TwoButton()
        self._field = ''
        
        
    def appendCmdToSetButton(self ):
        
        def cmdSet( *args ):
            text = cmds.textField( self._field, q=1, tx=1 )
            NameNumbering( text, cmds.ls( sl=1, l=1 ) )
            
        def cmdDeleteUI( *args ):
            cmds.deleteUI( NumberingUIInfo._winName )
        
        self._uiInstButton._cmdFirst.append( cmdSet )
        self._uiInstButton._cmdSecond.append( cmdDeleteUI )

    
    def show(self):
        
        if cmds.window( NumberingUIInfo._winName, ex=1 ):
            cmds.deleteUI( NumberingUIInfo._winName )
        cmds.window( NumberingUIInfo._winName, title=NumberingUIInfo._title )
        
        cmds.columnLayout()
        
        firstWidth = NumberingUIInfo._width * 0.4
        secondWidth = NumberingUIInfo._width - firstWidth
        cmds.rowColumnLayout( nc=2, cw=[(1,firstWidth),(2,secondWidth)])
        cmds.text( l='Set Name : ', al='right' )
        textField = cmds.textField()
        cmds.setParent( '..' )
        
        self._field = textField
        
        cmds.rowColumnLayout( nc=1, cw=(1,NumberingUIInfo._width) )
        self._uiInstButton.create( 23 )
        cmds.setParent( '..' )
        
        cmds.window( NumberingUIInfo._winName, e=1,
                     width  = NumberingUIInfo._width,
                     height = NumberingUIInfo._height )
        cmds.showWindow( NumberingUIInfo._winName )
        
        self.appendCmdToSetButton()
        
        
        
class ReplaceNameUI:
    
    def __init__(self):
        
        self._uiInstButton = UIs.button.TwoButton()
        self._firstField = ''
        self._secondField = ''
        self._checkH = ''
        self._checkN = ''
        
    
    def appendCmdToSetButton(self):
        
        def cmdSet( *args ):
            firstTx = cmds.textField( self._firstField, q=1, tx=1 )
            secondTx = cmds.textField( self._secondField, q=1, tx=1 )
            checkH = cmds.checkBox( self._checkH, q=1, v=1 )
            checkN = cmds.checkBox( self._checkN, q=1, v=1 )
            ReplaceName( firstTx, secondTx, cmds.ls( sl=1 ), checkH, checkN )
            
        def cmdDeleteUI( *args ):
            cmds.deleteUI( ReplaceNameUIInfo._winName )
            
        self._uiInstButton._cmdFirst.append( cmdSet )
        self._uiInstButton._cmdSecond.append( cmdDeleteUI )
        
        
    def show(self):
        
        if cmds.window( ReplaceNameUIInfo._winName, ex=1 ):
            cmds.deleteUI( ReplaceNameUIInfo._winName )
        cmds.window( ReplaceNameUIInfo._winName, title=ReplaceNameUIInfo._title )
        
        cmds.columnLayout()
        
        firstWidth = ReplaceNameUIInfo._width * 0.3
        secondWidth = ReplaceNameUIInfo._width * 0.35
        thirdWidth = ReplaceNameUIInfo._width - firstWidth - secondWidth
        cmds.rowColumnLayout( nc=3, cw=[(1,firstWidth),(2,secondWidth),(3,thirdWidth)] )
        cmds.text( l='Repace Name : ', al='right' )
        firstTF = cmds.textField()
        secondTF = cmds.textField()
        cmds.setParent( '..' )
        
        self._firstField = firstTF
        self._secondField = secondTF
        
        firstWidth = ReplaceNameUIInfo._width * 0.5
        secondWidth = ReplaceNameUIInfo._width - firstWidth
        cmds.rowColumnLayout( nc=2, cw=[(1,firstWidth),(2,secondWidth)] )
        checkHierarchy = cmds.checkBox( l='Hierarchy' )
        isNamespace    = cmds.checkBox( l='Is Namespace' )
        cmds.setParent( '..' )
        
        self._checkH = checkHierarchy
        self._checkN = isNamespace
        
        cmds.rowColumnLayout( nc=1, cw=(1,ReplaceNameUIInfo._width) )
        self._uiInstButton.create( 23 )
        cmds.setParent( '..' )
        
        cmds.window( ReplaceNameUIInfo._winName, e=1,
                     width = ReplaceNameUIInfo._width,
                     height = ReplaceNameUIInfo._height )

        cmds.showWindow( ReplaceNameUIInfo._winName )
        
        self.appendCmdToSetButton()