import maya.cmds as cmds
import sgModelUI
import sgRigConnection



class Window:
    
    def __init__(self):
        
        self.uiname = 'sgBlendShapeConnectWidthController'
        self.title  = 'SG Blend Shape Connect'
        self.width = 300
        self.height = 50
        
        self.controllerField  = sgModelUI.PopupFieldUI( 'Controller : ', 'Load Selected', 'single', position = 40 )
        self.blendShapesField = sgModelUI.PopupFieldUI( 'Blend Shapes : ', 'Load Selected', 'list', position = 40 )
        self.targetField      = sgModelUI.PopupFieldUI( 'Target : ', 'Load Selected', 'single', position = 40 )
    
    
    def cmdSet(self, *args ):
        
        ctl = self.controllerField.getFieldText()
        others = self.blendShapesField.getFieldTexts()
        target = self.targetField.getFieldText()
        
        sgRigConnection.blendShapeConnectWidthController( ctl, others, target )
        
        
    def cmdCancel(self, *args ):
        
        cmds.deleteUI( self.uiname, wnd=1 )
        

    
    def show(self):
        
        self.fields = []
        
        if cmds.window( self.uiname, ex=1 ):
            cmds.deleteUI( self.uiname, wnd=1 )
        
        cmds.window( self.uiname, title= self.title )
        
        cmds.columnLayout()
        columnWidth = self.width - 2
        
        cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)] )
        self.controllerField.create()
        self.blendShapesField.create()
        self.targetField.create()
        cmds.setParent( '..' )
        
        firstWidth = ( columnWidth - 2 )/2
        secondWidth = ( columnWidth -2 ) - firstWidth
        cmds.rowColumnLayout( nc=2, cw=[(1,firstWidth),(2,secondWidth)] )
        cmds.button( l='Set', c= self.cmdSet )
        cmds.button( l='Close', c= self.cmdCancel )
        cmds.setParent( '..' )
        
        cmds.window( self.uiname, e=1, width= self.width, height = self.height )
        cmds.showWindow( self.uiname )
        
        self.columnWidth = self.width -2


mc_showWindow = """import sgUISetAttr
sgUISetAttr.Window().show()"""