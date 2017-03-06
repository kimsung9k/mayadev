import maya.cmds as cmds
from functools import partial


class WinA_Global:
    
    winName = 'WinA_Global'
    title   = 'WinA_Global'
    width   = 450
    height  = 450
        
        

class WinA_Cmd:
    

    def __init__(self ):
        
        pass



class WinA_radialPose:

    def __init__(self):
        
        pass
    
    def create(self):
        
        form = cmds.formLayout()
        
        nButton = cmds.iconTextButton( w=45, h=45, image = 'pythonFamily.png', label='ABC' )
        neButton = cmds.iconTextButton( w=45, h=45, image = 'pythonFamily.png', label='DEF' )
        nwButton = cmds.iconTextButton( w=45, h=45, image = 'pythonFamily.png', label='GHI' )
        eButton = cmds.iconTextButton( w=45, h=45 )
        sButton = cmds.iconTextButton( w=45, h=45 )
        seButton = cmds.iconTextButton( w=45, h=45 )
        swButton = cmds.iconTextButton( w=45, h=45 )
        
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af = [ ( nButton, 'top', 10 ), ( neButton, 'top', 10 ), ( nwButton, 'top', 10 ) ],
                         ap = [ ( nButton, 'left', -22 , 50 ), ( neButton, 'left', -22, 25 ), ( nwButton, 'left', -22, 75 )] )
        
        return form



class WinA:

    
    def __init__(self):
        
        self.winName = WinA_Global.winName
        self.title   = WinA_Global.title
        self.width   = WinA_Global.width
        self.height  = WinA_Global.height
        
        self.radialPose = WinA_radialPose()


    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title=self.title )
        
        form = cmds.formLayout()
        radialPose = self.radialPose.create()
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af = [( radialPose, 'top', 10 ), ( radialPose, 'left', 0 ), ( radialPose, 'right', 0 )])
        
        cmds.window( self.winName, e=1, wh=[ self.width, self.height ], rtf=1 )
        cmds.showWindow( self.winName )