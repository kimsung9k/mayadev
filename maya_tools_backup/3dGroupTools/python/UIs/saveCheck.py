import maya.cmds as cmds


class Window:
    
    def __init__(self, winName, afterCmd ):
        
        width, height = cmds.window( winName, q=1, wh=1 )
        title = cmds.window( winName, q=1, title=1 )
        
        self.pWinName = winName
        self.pHeight  = height
        self.winName  = winName + '_saveCheck'
        self.title    = title + ' - Save Check'
        self.width    = width
        self.height   = 50
        self.afterCmd = afterCmd
        
        self.create()

        
    def cmdSave(self, *args ):
        
        cmds.deleteUI( self.winName, wnd=1 )
        cmds.file( save=1 )
        self.afterCmd()
        
        
    def cmdDoNotSave(self, *args):
        
        cmds.deleteUI( self.winName, wnd=1 )
        self.afterCmd()
        
        
    def cmdCancel(self, *args):
        
        cmds.deleteUI( self.winName, wnd=1 )
        
    
    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title=self.title )
        
        columnWidth = self.width - 2
        cmds.columnLayout()
        cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)])
        cmds.text( l='Scene is not saveed !', h=25 )
        cmds.setParent( '..' )
        
        firstWidth = (columnWidth ) / 3.0
        secondWidth = ( columnWidth ) / 3.0
        thirdWidth = ( columnWidth ) - firstWidth - secondWidth
        cmds.rowColumnLayout( nc=3, cw=[(1,firstWidth),(2,secondWidth),(3,thirdWidth)])
        cmds.button( l='Save', c=self.cmdSave )
        cmds.button( l='Do not save', c=self.cmdDoNotSave )
        cmds.button( l='Cancel', c=self.cmdCancel )
        cmds.setParent( '..' )
        
        top, left = cmds.window( self.pWinName, q=1, tlc=1 )
        
        cmds.showWindow( self.winName )
        
        cmds.window( self.winName, e=1,
                     tlc=[ top+self.pHeight+37, left ], w = self.width, h = self.height )