import maya.cmds as cmds
import maya.mel as mel
from uiModel import *
from cmdModel import *
import UIs.field, UIs.menu, UIs.button
from functools import partial



class CreateJointUI:
    
    def __init__(self):
        
        self._cmdSetTool = []


    def cmdSetTool( self, *args ):
        for cmd in self._cmdSetTool: cmd()
    

    def create(self):
        
        if cmds.window( CreateJointUIInfo._winName, ex=1 ):
            cmds.deleteUI( CreateJointUIInfo._winName, wnd=1 )
        cmds.window( CreateJointUIInfo._winName,
                     title = CreateJointUIInfo._title )
        
        cmds.rowColumnLayout( nc=1, cw=[(1,CreateJointUIInfo._width-2)])
        cmds.button( l='Set Tool', c= self.cmdSetTool )
        
        cmds.window( CreateJointUIInfo._winName, e=1,
                     width = CreateJointUIInfo._width,
                     height = CreateJointUIInfo._height )
        cmds.showWindow( CreateJointUIInfo._winName )



class SetJointOrientUI:

    def __init__(self):
        
        self._uiInstTopObject = UIs.field.PopupFieldUI( SetJointOrientUIInfo._labelTopObject, 'Load Selected', 40 )
        self._uiInstEndObject = UIs.field.PopupFieldUI( SetJointOrientUIInfo._labelEndObject, 'Load Selected', 40 )
        self._uiInstUpObject  = UIs.field.PopupFieldUI( SetJointOrientUIInfo._labelUpObject , 'Load Selected', 40 )
        
        self._uiInstUpType = UIs.menu.OptionMenu( SetJointOrientUIInfo._labelUpObjectType, ['Object Up', 'Object Rotation Up'] )
        
        self._uiInstAimAxis     = UIs.menu.OptionMenu( SetJointOrientUIInfo._labelAimAxis, ['x','y','z','-x','-y','-z'] )
        self._uiInstUpAxis      = UIs.menu.OptionMenu( SetJointOrientUIInfo._labelUpAxis, [] )
        self._uiInstWorldUpAxis = UIs.menu.OptionMenu( SetJointOrientUIInfo._labelWorldUpAxis, ['x','y','z','-x','-y','-z'] )
        
        self._uiInstButton      = UIs.button.TwoButton()
        

    
    def appendTopObjectCmd(self):
        
        def cmdLoadChild():
            sels = cmds.ls( sl=1 )
            if not sels: return None
            children = cmds.listRelatives( sels[-1], c=1, f=1, ad=1 )
            if not children: return None
            child = cmds.ls( children[0], sn=1 )[0]
            cmds.textField( self._uiInstEndObject._field, e=1, tx=child )
        
        self._uiInstTopObject._cmdPopup.append( cmdLoadChild )
        


    def checkAndUpdateUpAxis(self, *args):
        
        axisList = ['x','y','z','-x','-y','-z']
        selNum = cmds.optionMenuGrp( self._uiInstAimAxis._menu, q=1, select=1 )
        removeIndex1 = (selNum-1)%3
        removeIndex2 = removeIndex1 + 3
        axisList.pop( removeIndex2 )
        axisList.pop( removeIndex1 )
        self._uiInstUpAxis.resetMenu( axisList )
        
        
    
    def checkAndUpdateWorldUpAxis(self, *args ):
        
        selNum = cmds.optionMenuGrp( self._uiInstUpType._menu, q=1, select=1 )
        cmds.optionMenuGrp( self._uiInstWorldUpAxis._menu, e=1, en=selNum-1 )



    def appendCmdsToTwoButtons(self, *args ):
        
        self._uiInstButton._cmdFirst  = []
        self._uiInstButton._cmdSecond = []
        
        
        def cmdFirst( *args ):        
            topObject = cmds.textField( self._uiInstTopObject._field, q=1, tx=1 )
            if cmds.textField( self._uiInstEndObject._field, q=1, en=1 ):
                endObject = cmds.textField( self._uiInstEndObject._field, q=1, tx=1 )
            else:
                endObject = cmds.listRelatives( topObject, c=1 )[0]
            upObject  = cmds.textField( self._uiInstUpObject._field,  q=1, tx=1 )
            aimIndex     = cmds.optionMenuGrp( self._uiInstAimAxis._menu, q=1, select=1 )-1
            upIndex      = cmds.optionMenuGrp( self._uiInstUpAxis._menu, q=1, select=1 )-1
            worldUpIndex = cmds.optionMenuGrp( self._uiInstWorldUpAxis._menu, q=1, select=1 )-1
            upTypeIndex       = cmds.optionMenuGrp( self._uiInstUpType._menu, q=1, select=1 )-1
            
            indexOver = False
            if upIndex >= 2:
                indexOver = True
                upIndex %= 2
            if aimIndex % 3 <= upIndex:
                upIndex += 1
            if indexOver:
                upIndex += 3
            upType = ['object', 'objectRotation'][upTypeIndex]
            SetJointOrient( topObject, endObject, upObject, aimIndex, upIndex, upType, worldUpIndex )

        self._uiInstButton._cmdFirst.append( cmdFirst )
        self._uiInstButton._cmdSecond.append( self.deleteUI )

    

    def Show(self):
        
        if cmds.window( SetJointOrientUIInfo._winName, ex=1 ):
            cmds.deleteUI( SetJointOrientUIInfo._winName, wnd=1 )
        cmds.window( SetJointOrientUIInfo._winName, title=SetJointOrientUIInfo._title )
        
        cmds.columnLayout()
        
        cmds.text( h=3, l='' )
        
        cmds.rowColumnLayout( nc=2, cw=[(1,200),(2,200)])
        self._uiInstTopObject.create()
        self._uiInstEndObject.create()
        cmds.popupMenu( p=self._uiInstEndObject._form )
        def setEnableForm( *args ):
            if cmds.text( self._uiInstEndObject._text, q=1, en=1 ):
                cmds.text( self._uiInstEndObject._text, e=1, en=0 )
                cmds.textField( self._uiInstEndObject._field, e=1, en=0 )
            else:
                cmds.text( self._uiInstEndObject._text, e=1, en=1 )
                cmds.textField( self._uiInstEndObject._field, e=1, en=1 )
        cmds.menuItem( l='Enable', c= setEnableForm )
        cmds.setParent('..' )
        
        cmds.text( h=3, l='' )
        
        cmds.rowColumnLayout( nc=1, cw=[(1,400)])
        cmds.separator()
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=2, cw=[(1,200),(2,200)])
        self._uiInstUpObject.create()
        self._uiInstUpType.create( [70, 100] )
        cmds.optionMenuGrp( self._uiInstUpType._menu, e=1, cc=self.checkAndUpdateWorldUpAxis )
        cmds.setParent( '..' )
        
        cmds.text( h=3, l='' )
        
        cmds.rowColumnLayout( nc=3, cw=[(1,123),(2,143),(3,133)])
        self._uiInstAimAxis.create()
        cmds.optionMenuGrp( self._uiInstAimAxis._menu, e=1, cc=self.checkAndUpdateUpAxis )
        self._uiInstUpAxis.create()
        self._uiInstWorldUpAxis.create()
        cmds.setParent( '..' )
        
        cmds.text( h=3, l='' )
        
        cmds.rowColumnLayout( nc=1, cw=[(1,400)])
        cmds.separator()
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=1, cw=[(1,400)])
        self._uiInstButton.create( 25 )
        cmds.setParent( '..' )
        
        cmds.window( SetJointOrientUIInfo._winName, e=1,
                     w=SetJointOrientUIInfo._width,
                     h=SetJointOrientUIInfo._height )
        cmds.showWindow( SetJointOrientUIInfo._winName )
                
        self.appendTopObjectCmd()
        self.checkAndUpdateUpAxis()
        self.checkAndUpdateWorldUpAxis()
        self.appendCmdsToTwoButtons()
        


    def deleteUI(self, *args ):
        cmds.deleteUI( SetJointOrientUIInfo._winName, wnd=1 )
        

