import maya.cmds as cmds
from functools import partial
import sgBFunction_base



class WinA_Global:
    
    winName = 'sgPWindow_curve_rebuildByMinMaxSpans'
    title   = 'UI Rebuild By Min Max'
    width   = 300
    height  = 50

    fld_min = ''
    fld_max = ''



class WinA_Cmd:

    @staticmethod
    def rebuild(self, *args ):

        import sgBFunction_curve
        sgBFunction_base.reloadModule( sgBFunction_curve )

        minSpans = cmds.intField( WinA_Global.fld_min, q=1, v=1 )
        maxSpans = cmds.intField( WinA_Global.fld_max, q=1, v=1 )

        sels = cmds.ls( sl=1 )
        sgBFunction_curve.rebuildByMinMaxSpans( sels, minSpans, maxSpans )
        cmds.select( sels )





class WinA_minMaxField:
    
    def __init__(self):
        
        pass
    
    
    def create(self):
        
        form = cmds.formLayout()
        
        minText = cmds.text( l = 'Min : ', h=21 )
        minField = cmds.intField( v = 10, h=21 )
        maxText = cmds.text( l = 'Max : ', h=21 )
        maxField = cmds.intField( v = 30, h=21 )
        
        cmds.setParent( '..' )

        cmds.formLayout( form, e=1, 
                         ap = [ ( minField, 'right', 30, 50 ), ( maxField, 'right', 30, 100 ) ],
                         ac = [ ( minText, 'right', 0, minField ), ( maxText, 'right', 0, maxField )] )
        
        WinA_Global.fld_min = minField
        WinA_Global.fld_max = maxField
        
        return form





class WinA:


    def __init__(self):

        self.winName = WinA_Global.winName
        self.title   = WinA_Global.title
        self.width   = WinA_Global.width
        self.height  = WinA_Global.height
        
        self.uiMinMaxField = WinA_minMaxField()

    def create(self):

        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title=self.title )

        form = cmds.formLayout()
        frm_minMaxField = self.uiMinMaxField.create()
        bt_rebuild = cmds.button( l='Rebuild', c= WinA_Cmd.rebuild )
        
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af=[( frm_minMaxField, 'left', 0 ), ( frm_minMaxField, 'right', 0 ), ( frm_minMaxField, 'top', 5 ),
                             ( bt_rebuild, 'left', 0 ), ( bt_rebuild, 'right', 0 ) ],
                         ac = [( bt_rebuild, 'top', 5, frm_minMaxField )] )

        cmds.window( self.winName, e=1, wh=[ self.width, self.height ], rtf=1 )
        cmds.showWindow( self.winName )
