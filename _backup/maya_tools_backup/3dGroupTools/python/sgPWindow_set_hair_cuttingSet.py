import maya.cmds as cmds
from functools import partial
import sgBFunction_ui



class WinA_Global:
    
    winName = 'WinA_Global'
    title   = 'WinA_Global'
    width   = 400
    height  = 50
    
    fld_baseMesh = ''
    fld_moveMesh = ''
    fld_curves   = ''
    fld_joint = ''
    
        



class WinA_Cmd:
    
    @staticmethod
    def cmdSet( *args ):
        
        import sgBRig_hair
        
        baseMesh = cmds.textField( WinA_Global.fld_baseMesh, q=1, tx=1 )
        moveMesh = cmds.textField( WinA_Global.fld_moveMesh, q=1, tx=1 )
        curves   = cmds.textField( WinA_Global.fld_curves,   q=1, tx=1 ).split( ' ' )
        joint    = cmds.textField( WinA_Global.fld_joint   , q=1, tx=1 )

        sgBRig_hair.CuttingSet( baseMesh, moveMesh, curves, joint ).setAll()



class WinA:

    def __init__(self):

        self.winName = WinA_Global.winName
        self.title   = WinA_Global.title
        self.width   = WinA_Global.width
        self.height  = WinA_Global.height

        self.uiBaseMesh   = sgBFunction_ui.PopupFieldUI_b( 'Base Mesh : ' )
        self.uiMoveMesh   = sgBFunction_ui.PopupFieldUI_b( 'Move Mesh : ' )
        self.uiCurves     = sgBFunction_ui.PopupFieldUI_b( 'Curves : ' )
        self.uiJoint = sgBFunction_ui.PopupFieldUI_b( 'Joint : ' )


    def create(self):

        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title=self.title )

        form = cmds.formLayout()

        formBaseMesh = self.uiBaseMesh.create()
        formMoveMesh = self.uiMoveMesh.create()
        formCurves   = self.uiCurves.create()
        formCJoint   = self.uiJoint.create()
        formButton    = cmds.button( l='S E T' )

        cmds.formLayout( form, e=1,
                         af = [ (formBaseMesh, 'left', 0), (formBaseMesh, 'right', 0),
                                (formMoveMesh, 'left', 0), (formMoveMesh, 'right', 0),
                                (formCurves  , 'left', 0), (formCurves  , 'right', 0),
                                (formCJoint  , 'left', 0), (formCJoint  , 'right', 0),
                                (formButton, 'left', 0), (formButton, 'right', 0)],
                         ac = [ ( formMoveMesh, 'top', 0, formBaseMesh ),
                                ( formCurves, 'top', 0, formMoveMesh ),
                                ( formCJoint, 'top', 0, formCurves ),
                                ( formButton, 'top', 0, formCJoint ) ] )
        
        WinA_Global.fld_baseMesh = self.uiBaseMesh._field
        WinA_Global.fld_moveMesh = self.uiMoveMesh._field
        WinA_Global.fld_curves = self.uiCurves._field
        WinA_Global.fld_joint = self.uiJoint._field

        cmds.window( self.winName, e=1, wh=[ self.width, self.height ], rtf=1 )
        cmds.showWindow( self.winName )


        self.button = formButton
        self.assignCommandToUI()

    
    def assignCommandToUI(self):
        
        cmds.button( self.button, e=1, c = WinA_Cmd.cmdSet )
