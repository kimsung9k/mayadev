import maya.cmds as cmds


class Window:
    
    def __init__(self):
        
        self.winName = 'modelEditorUi'
        self.title   = 'Model Editor'
        self.width   = 1280
        self.height   = 720
        
        self.camera = 'persp'
    
    
    def setCamera(self, cam ):
        
        self.camera = cam
        
        
    def setWindowName(self, winName ):
        
        self.winName = winName
        
        
    def setWidthHeight(self, width, height ):
        
        self.width  = width
        self.height = height
    
    
    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title )
        
        form = cmds.formLayout()
        editor = cmds.modelEditor( camera = self.camera,
                                   displayAppearance='smoothShaded',
                                   imagePlane = 0,
                                   useDefaultMaterial = 1,
                                   headsUpDisplay = 0,
                                   nurbsCurves = 0 )
        
        cmds.formLayout( form, e=1,
                         af=[(editor,'top', 0), (editor,'bottom', 0), (editor,'left', 0), (editor,'right', 0)] )
        
        cmds.window( self.winName, e=1,
                     w = self.width, h = self.height )
        cmds.showWindow( self.winName )
        
        cmds.modelEditor( editor, e=1, interactive=1 )
        
        self.editor = editor