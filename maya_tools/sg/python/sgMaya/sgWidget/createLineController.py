from maya import cmds
import pymel.core
from functools import partial
from sgMaya import sgCmds


class Win_Global:
    
    winName = 'sg_createLineController_ui'
    title = "UI - Create Line Controller"
    width = 300
    height = 50



class Win_Cmd:
    
    @staticmethod
    def create( *args ):
        
        controllerName = cmds.textField( Win_Global.textField, q=1, tx=1 )
        checked = cmds.checkBox( Win_Global.checkBox, q=1, v=1 )
        colorIndex1 = cmds.intField( Win_Global.intField1, q=1, v=1 )
        colorIndex2 = cmds.intField( Win_Global.intField2, q=1, v=1 )
        controllerSize = cmds.floatField( Win_Global.floatField, q=1, v=1 )
        
        topJoints = pymel.core.ls( sl=1 )
        for i in range( len( topJoints ) ):
            topJoint = topJoints[i]
            ctls, pinCtls = sgCmds.createFkControl( topJoint, controllerSize, checked )
            for j in range( len( ctls ) ):
                ctl = ctls[j]
                pinCtl = pinCtls[j]
                ctl.getShape().overrideEnabled.set( 1 )
                ctl.getShape().overrideColor.set( colorIndex1 )
                
                if pinCtl:
                    pinCtl.getShape().overrideEnabled.set( 1 )
                    pinCtl.getShape().overrideColor.set( colorIndex2 )
                
                if controllerName:
                    if len( topJoints ) == 1:
                        cuName = controllerName + '_%d' %( j )
                    else:
                        cuName = controllerName + '_%d_%d' %( i, j )
                    ctl.rename( cuName )
                    ctl.getParent().rename( 'P' + cuName )
                    if pinCtl:
                        pinCtl.rename( cuName + '_Move' )
                        pinCtl.getParent().rename( 'P' + pinCtl.name() )

    @staticmethod
    def close( *args ):
        cmds.deleteUI( Win_Global.winName )
    



class UI_ControllerName:
    
    def __init__(self):
        
        pass
    
    
    def create(self):
        
        form = cmds.formLayout()
        text = cmds.text( l='Controller Name : ', w=100, al='left', h=25 )
        textField = cmds.textField( h=25, w=150 )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af = [(text, 'top', 0 ), ( text, 'left', 20),
                               ( textField, 'top', 0 )],
                         ac = [(textField, 'left', 0, text )])
        Win_Global.textField = textField
        return form





class UI_ColorIndex:
    
    def __init__(self):
        
        pass
    
    
    def create(self):
        
        form = cmds.formLayout()
        text = cmds.text( l='ColorIndex : ', w=100, al='left', h=25 )
        intField1 = cmds.intField(h=25, w=100, v=0 )
        intField2 = cmds.intField(h=25, w=100, v=0 )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af = [(text,'top',0), (text,'left',20),
                               (intField1,'top',0),(intField2,'top',0)],
                         ac = [(intField1, 'left', 0, text), (intField2, 'left', 0, intField1)] )
        
        Win_Global.intField1 = intField1
        Win_Global.intField2 = intField2
        
        return form





class UI_ControllerSize:
    
    def __init__(self):
        
        pass
    
    
    def create(self):
        
        form = cmds.formLayout()
        text = cmds.text( l='Controller Size : ', w=100, al='left', h=25 )
        floatField = cmds.floatField(h=25, w=100, v=1.0, pre=2 )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af = [(text,'top',0), (text,'left',20),
                               (floatField,'top',0)],
                         ac = [(floatField, 'left', 0, text)] )
        
        Win_Global.floatField = floatField
        
        return form
    





class UI_Buttons:
    
    def __init__(self):
        
        pass


    def create(self):
        
        form = cmds.formLayout()
        createButton = cmds.button( l='Create', h=25, c=Win_Cmd.create )
        closeButton  = cmds.button( l='Close', h=25,  c=Win_Cmd.close )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af = [( createButton, 'top', 0 ), ( createButton, 'left', 0 ), ( createButton, 'bottom', 0 ),
                               ( closeButton, 'top', 0 ), ( closeButton, 'right', 0 ), ( closeButton, 'bottom', 0 )],
                         ap = [ ( createButton, 'right', 0, 50 ), ( closeButton, 'left', 0, 50 ) ])
    
        return form




class Win:
    
    def __init__(self):
        
        self.ui_controllerName = UI_ControllerName()
        self.ui_colorIndex = UI_ColorIndex()
        self.ui_controllerSize = UI_ControllerSize()
        self.ui_buttons  = UI_Buttons()


    def create(self):
        
        if cmds.window( Win_Global.winName, q=1, ex=1 ):
            cmds.deleteUI( Win_Global.winName )
        cmds.window( Win_Global.winName, title=Win_Global.title )
        
        form  = cmds.formLayout()
        text   = cmds.text( l= "Select joint tops", al='center', h=30, bgc=[.5,.5,.5] )
        check = cmds.checkBox( l='Add Pin Control' )
        controllerName = self.ui_controllerName.create()
        colorIndex = self.ui_colorIndex.create()
        controllerSize = self.ui_controllerSize.create()
        button = self.ui_buttons.create()
        cmds.setParent( '..' )

        cmds.formLayout( form, e=1, af=[ (text, 'top', 0 ), (text, 'left', 0 ), (text, 'right', 0 ),
                                         (check, 'top', 5 ), (check, 'left', 10 ), (check, 'right', 0 ),
                                         (controllerName, 'left', 10 ), (controllerName, 'right', 5 ),
                                         (colorIndex, 'left', 10 ), (colorIndex, 'right', 5 ),
                                         (controllerSize, 'left', 10 ), (controllerSize, 'right', 5 ),
                                         (button, 'left', 0 ), (button, 'right', 0 ), (button, 'bottom', 0 )],
                                    ac=[ (check, 'top', 5, text),
                                         (controllerName, 'top', 5, check),
                                         (colorIndex, 'top', 5, controllerName), 
                                         (controllerSize, 'top', 5, colorIndex), 
                                         (button, 'top', 5, controllerSize) ] )
        
        cmds.window( Win_Global.winName, e=1,
                     width = Win_Global.width, height = Win_Global.height,
                     rtf=1 )
        cmds.showWindow( Win_Global.winName )
        
        Win_Global.checkBox = check



def show():
    
    Win().create()
    
    

if __name__ == '__main__':
    show()




