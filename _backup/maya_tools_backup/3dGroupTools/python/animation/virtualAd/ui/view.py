import maya.cmds as cmds
import uiModel



class KeyControlUI_copyKeyLayout():
    
    def __init__(self):
        
        pass
    
    
    def create(self):
        
        winWidth = uiModel.KeyControlUIInfo._width - 2
        frameWidth = winWidth -4
        
        cmds.frameLayout( l='Copy Key', w=winWidth )
        
        firstWidth = 40
        secondWidth = ( frameWidth-firstWidth ) * 0.5
        thirdWidth  = frameWidth - firstWidth - secondWidth
        fieldFirstWidth = secondWidth * 0.6
        fieldSecondWidth = secondWidth - fieldFirstWidth -2
        
        cmds.rowColumnLayout( nc=3, cw=[(1,firstWidth),(2,secondWidth),(2,thirdWidth)] )
        cmds.text( l='From : ', al='right')
        
        cmds.floatFieldGrp( l='Start Frame : ', cw=[(1,fieldFirstWidth),(2,fieldSecondWidth)] )
        cmds.floatFieldGrp( l='End Frame : '  , cw=[(1,fieldFirstWidth),(2,fieldSecondWidth)] )
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=3, cw=[(1,firstWidth),(2,secondWidth),(2,thirdWidth)] )
        cmds.text( l='To : ', al='right')
        cmds.floatFieldGrp( l='Start Frame : ', cw=[(1,fieldFirstWidth),(2,fieldSecondWidth)] )
        cmds.floatFieldGrp( l='End Frame : '  , cw=[(1,fieldFirstWidth),(2,fieldSecondWidth)] )
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=1, cw=[1,frameWidth])
        cmds.button( l='Copy Key' )
        




class KeyControlUI:
    
    def __init__(self):
        
        self._copyKeyLayout = KeyControlUI_copyKeyLayout()
    
    
    def create(self):
        
        winName  = uiModel.KeyControlUIInfo._winName
        winTitle = uiModel.KeyControlUIInfo._title
        winWidth = uiModel.KeyControlUIInfo._width
        winHeight= uiModel.KeyControlUIInfo._height
        
        if cmds.window( winName, ex=1 ):
            cmds.deleteUI( winName, wnd=1 )
        cmds.window( winName, title=winTitle )
        
        cmds.columnLayout()
        self._copyKeyLayout.create()
        
        
        cmds.window( winName, e=1, w=winWidth, h=winHeight )
        cmds.showWindow( winName )