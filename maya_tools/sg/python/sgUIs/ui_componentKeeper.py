from maya import cmds
import pymel.core
from functools import partial
from sgMaya import sgCmds


class Win_Global:
    
    winName = 'sg_componentKeeper_ui'
    title = "UI - Component Keeper"
    width = 400
    height = 50



class Win_Cmd:
    
    @staticmethod
    def close( *args ):
        cmds.deleteUI( Win_Global.winName )
    
    
    @staticmethod
    def getComponent( *args ):
        
        sels = pymel.core.ls( sl=1, fl=1 )
        compList = []
        for sel in sels:
            if sel.find( '.' ) == -1: continue
            compList.append( sel.split( '.' )[-1] )
        compList = list( set( compList ) )
        compListString = ','.join( compList )
        cmds.textField( Win_Global.textField, e=1, tx=compListString )
    
    
    @staticmethod
    def selectComponent( *args ):
        
        sels = pymel.core.ls( sl=1 )
        
        compList = cmds.textField( Win_Global.textField, q=1, tx=1 ).split( ',' )
        
        targetComps = []
        for sel in sels:
            if sel.find( '.' ) != -1: continue
            for comp in compList:
                targetComp = cmds.ls( sel + '.' + comp )
                if not targetComp: continue
                targetComps.append( targetComp )
        
        pymel.core.select( targetComps )
    



class UI_GetComponent:
    
    def __init__(self):
        
        pass
    
    
    def create(self):
        
        form = cmds.formLayout()
        text = cmds.text( l='Component List : ', h=25 )
        textField = cmds.textField( h=25 )
        button = cmds.button( l='Get Component', h=25, c= Win_Cmd.getComponent )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af=[ (text, 'top', 5), (text, 'left', 5),
                              (textField, 'top', 5), (textField, 'right', 5),
                              (button, 'left', 0), (button, 'right', 0), (button, 'bottom', 0) ],
                         ac=[ (textField, 'left', 0, text),
                              (button, 'top', 5, text) ] )
        
        Win_Global.textField = textField
        
        return form




class UI_SelectComponent:
    
    def __init__(self):
        
        pass
    
    
    def create(self):
        
        form = cmds.formLayout()
        #text = cmds.text( l="Select Shape Objects", h=30, bgc=[0.5,0.5,0.5], al='center' )
        button = cmds.button( l='Select Component', h=25, c= Win_Cmd.selectComponent )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[ ( button, 'top', 0 ),( button, 'left', 0 ), ( button, 'right', 0 ), ( button, 'bottom', 0 ) ] )
        
        return form





class Win:
    
    def __init__(self):

        self.ui_getComponent = UI_GetComponent()
        self.ui_selectComponent = UI_SelectComponent()


    def create(self):
        
        if cmds.window( Win_Global.winName, q=1, ex=1 ):
            cmds.deleteUI( Win_Global.winName )
        cmds.window( Win_Global.winName, title=Win_Global.title )
        
        form  = cmds.formLayout()
        form_getComponent = self.ui_getComponent.create()
        separator = cmds.separator()
        form_selectComponent = self.ui_selectComponent.create()
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af = [ (form_getComponent, 'top', 0), (form_getComponent, 'left', 0), (form_getComponent, 'right', 0),
                                (separator, 'left', 0), (separator, 'right', 0),
                                (form_selectComponent, 'left', 0), (form_selectComponent, 'right', 0) ],
                         ac = [ (separator, 'top', 0, form_getComponent),
                                (form_selectComponent, 'top', 0, separator)] )
        
        cmds.window( Win_Global.winName, e=1,
                     width = Win_Global.width, height = Win_Global.height,
                     rtf=1 )

        cmds.showWindow( Win_Global.winName )


