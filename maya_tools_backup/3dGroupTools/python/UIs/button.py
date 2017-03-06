import maya.cmds as cmds


class TwoButton:
    
    def __init__( self ):
        
        self._cmdFirst = []
        self._cmdSecond = []
    
    
    def cmdFirst( self, *args ):
        for cmd in self._cmdFirst:   cmd()
        
        
    def cmdSecond( self, *args ):
        for cmd in self._cmdSecond: cmd()
    
    
    def create(self, height = 21, firstName='SET', secondName='CLOSE'):
        
        form = cmds.formLayout()
        
        buttonFirst   = cmds.button( l=firstName,   c= self.cmdFirst,   h=height )
        buttonSecond  = cmds.button( l=secondName,  c= self.cmdSecond, h=height )
        
        cmds.formLayout( form, e=1,
                         attachForm = [( buttonFirst, 'top', 0), ( buttonSecond, 'top', 0 ),
                                       ( buttonFirst, 'left',0), ( buttonSecond, 'right',0)],
                         ap = [( buttonFirst, 'right', 0, 50),( buttonSecond, 'left', 0, 50)] )
        cmds.setParent('..' )
        self._form = form