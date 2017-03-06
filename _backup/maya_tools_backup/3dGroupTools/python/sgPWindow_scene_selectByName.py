import maya.cmds as cmds
from functools import partial
import sgBFunction_ui



class WinA_Global:
    
    winName = 'sgPWindow_scene_selectByName'
    title   = 'Select By Name'
    width   = 450
    height  = 50

    fld_searchString = ''



class WinA_Field:
    
    def __init__(self, label, w, h, al ):
        
        self.label  = label
        self.width  = w
        self.height = h
        self.aline  = al


    def create(self):
        
        form = cmds.formLayout()
        text = cmds.text( l=self.label, w=self.width, h=self.height, al= self.aline )
        txf  = cmds.textField( h = self.height )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af = [( text, 'top', 0 ), ( text, 'left', 0 ),
                               ( txf,  'top', 0 ), ( txf,  'right', 0 )],
                         ac = [( txf, 'left', 0, text )] )
        
        self.txf  = txf
        self.form = form
        
        return form
    
    
        
        



class WinA_Cmd:
    

    @staticmethod
    def cmdSelectByName( *args ):
        
        searchString = cmds.textField( WinA_Global.fld_searchString, q=1, tx=1 )
        
        targets = cmds.ls( tr=1 )
        
        selTargets = []
        for target in targets:
            targetName = target.split( '|' )[-1]
            if targetName.find( searchString ) != -1:
                selTargets.append( target )

        cmds.select( selTargets )
                





class WinA:

    
    def __init__(self):
        
        self.winName = WinA_Global.winName
        self.title   = WinA_Global.title
        self.width   = WinA_Global.width
        self.height  = WinA_Global.height
        
        self.uiField = WinA_Field( 'Search String : ', 100, 23, 'right' )


    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title=self.title )
        
        form = cmds.formLayout()
        form_field = self.uiField.create()
        bt_select  = cmds.button( l='S E L E C T', c= WinA_Cmd.cmdSelectByName )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af=[( form_field, 'top', 5 ), ( form_field, 'left', 5 ), ( form_field, 'right', 5 ),
                             ( bt_select, 'left', 0 ), ( bt_select, 'right', 0 )],
                         ac=[( bt_select, 'top', 5, form_field )] )
        
        cmds.window( self.winName, e=1, wh=[ self.width, self.height ], rtf=1 )
        cmds.showWindow( self.winName )
        
        WinA_Global.fld_searchString = self.uiField.txf