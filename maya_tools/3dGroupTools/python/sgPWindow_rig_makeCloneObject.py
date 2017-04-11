import maya.cmds as cmds
from functools import partial
import sgBFunction_ui



class WinA_Global:
    
    winName = 'makeCloneObject'
    title   = 'Make Clone Object'
    width   = 450
    height  = 50
    
    ui_clones   = ''
    chk_shapeOn = ''
    chk_connectionOn = ''
    fld_cloneaLabel = ''
        



class WinA_cloneLabel:
    
    def __init__(self, label, labelArea=30 ):
        
        self.label = label
        self.labelArea = labelArea
    
    
    def create(self):
        
        form = cmds.formLayout()
        tx  = cmds.text( l= self.label, al='right', h=22, w=120 )
        fld = cmds.textField( h=22, w=100, tx='_clone' )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af=[ ( tx, 'top', 0 ), ( tx, 'left', 0 ) ],
                         ac=[ ( fld, 'left', 0, tx ) ] )
        
        self.fld = fld
        
        return form




class WinA_Cmd:
    
    @staticmethod
    def cmdCreateClone( *args ):
        
        clones = WinA_Global.ui_clones.getFieldTexts()
        shapeOn = cmds.checkBox( WinA_Global.chk_shapeOn, q=1, v=1 )
        connectionOn = cmds.checkBox( WinA_Global.chk_connectionOn, q=1, v=1 )

        import sgBFunction_dag
        
        clones = sgBFunction_dag.getChildrenShapeExists( clones )
        for clone in clones:
            sgBFunction_dag.makeCloneObject( clone, shapeOn=shapeOn, connectionOn=connectionOn )



class WinA:

    
    def __init__(self):

        self.winName = WinA_Global.winName
        self.title   = WinA_Global.title
        self.width   = WinA_Global.width
        self.height  = WinA_Global.height
        
        self.uiCloneTargets = sgBFunction_ui.PopupFieldUI_b( 'Clone Targets : ', typ='multiple' )
        self.uiCloneLabel   = WinA_cloneLabel( 'Clone Label : ' )
        

    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title=self.title )
        
        form = cmds.formLayout()
        form_cloneTarget = self.uiCloneTargets.create()
        form_cloneLabel  = self.uiCloneLabel.create()
        chk_shapeOn      = cmds.checkBox( l='Shape On', v=1 )
        chk_connectionOn = cmds.checkBox( l='Connection On', v=1 )
        bt_createClone   = cmds.button( l='C R E A T E   C L O N E', h=25, c = WinA_Cmd.cmdCreateClone )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af = [( form_cloneTarget, 'top', 5 ), ( form_cloneTarget, 'left', 5 ), ( form_cloneTarget, 'right', 5 ),
                               ( form_cloneLabel, 'top', 5 ), ( form_cloneLabel, 'left', 5 ), ( form_cloneLabel, 'right', 5 ), 
                               ( chk_shapeOn, 'left', 50 ),
                               ( bt_createClone, 'left', 0 ),( bt_createClone, 'right', 0 )],
                         ac = [( form_cloneLabel, 'top', 10, form_cloneTarget ), 
                               ( chk_shapeOn, 'top', 10, form_cloneLabel ), 
                               ( chk_connectionOn, 'top', 10, form_cloneLabel ), ( chk_connectionOn, 'left', 30, chk_shapeOn ),
                               ( bt_createClone, 'top', 10, chk_connectionOn )] )
        
        cmds.window( self.winName, e=1, wh=[ self.width, self.height ], rtf=1 )
        cmds.showWindow( self.winName )
        
        WinA_Global.ui_clones = self.uiCloneTargets
        WinA_Global.chk_shapeOn = chk_shapeOn
        WinA_Global.chk_connectionOn = chk_connectionOn
        