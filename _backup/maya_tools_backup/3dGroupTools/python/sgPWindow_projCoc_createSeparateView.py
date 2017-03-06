import maya.cmds as cmds
from functools import partial
import sgBFunction_ui



class WinA_Global:
    
    winName = 'sgPWindow_projCoc_createSeparateView'
    title   = 'UI Separate View Creator'
    width   = 450
    height  = 50
    
    camField  = ''
    resField1 = ''
    resField2 = ''
    sepGroup1 = ''
    sepGroup2 = '' 
    sepField1 = ''
    sepField2 = ''
    scaleField= ''
    createWindowCheck = ''



class WinA_Cmd:
    
    @staticmethod
    def uiCmdChangeCondition( *args ):
        
        resWidth = cmds.intField( WinA_Global.resField1, q=1, v=1 )
        resHeight = cmds.intField( WinA_Global.resField2, q=1, v=1 )
        sepGroupWidth  = cmds.intField( WinA_Global.sepGroup1, q=1, v=1 )
        sepGroupHeight = cmds.intField( WinA_Global.sepGroup2, q=1, v=1 )
        sepFieldWidth  = cmds.intField( WinA_Global.sepField1, q=1, v=1 )
        sepFieldHeight = cmds.intField( WinA_Global.sepField2, q=1, v=1 )
        
        resultWidth  = float( resWidth ) / sepFieldWidth / sepGroupWidth
        resultHeight = float( resHeight ) / sepFieldHeight / sepGroupHeight
        
        cmds.floatField( WinA_Global.resultField1, e=1, v=resultWidth )
        cmds.floatField( WinA_Global.resultField2, e=1, v=resultHeight )
    
    
    @staticmethod
    def uiCmdCheckOnOff( *args ):
        
        createWindow = cmds.checkBox( WinA_Global.createWindowCheck, q=1, v=1 )
        cmds.floatField( WinA_Global.scaleField, e=1, en=createWindow )
    
     
    @staticmethod
    def cmdCreate( *args ):
        
        cam    = cmds.textField( WinA_Global.camField, q=1, tx=1 )
        width  = cmds.intField( WinA_Global.resField1, q=1, v=1 )
        height = cmds.intField( WinA_Global.resField2, q=1, v=1 )
        sepGH  = cmds.intField( WinA_Global.sepGroup1, q=1, v=1 )
        sepGV  = cmds.intField( WinA_Global.sepGroup2, q=1, v=1 )
        sepH   = cmds.intField( WinA_Global.sepField1, q=1, v=1 )
        sepV   = cmds.intField( WinA_Global.sepField2, q=1, v=1 )
        scale  = cmds.floatField( WinA_Global.scaleField, q=1, v=1 )
        createWindow = cmds.checkBox( WinA_Global.createWindowCheck, q=1, v=1 )
        
        import sgBProject_coc
        sgBProject_coc.createUiSeparactedViewGroup( cam, width, height, sepGH, sepGV, sepH,sepV, scale, createWindow )

    @staticmethod
    def cmdClear( *args ):
        
        cam = cmds.textField( WinA_Global.camField, q=1, tx=1 )
        import sgBProject_coc
        sgBProject_coc.removeUiSeparateView( cam )
        




class WinA_TwoIntField:
    
    def __init__(self, label1, label2, w1, w2, h ):
        
        self.label1 = label1
        self.label2 = label2
        self.width1 = w1
        self.width2 = w2
        self.height = h
    
    
    def create(self):
        
        form = cmds.formLayout()
        text1 = cmds.text( l= self.label1, w=self.width1, h=self.height, al='right' )
        text2 = cmds.text( l= self.label2, w=self.width1, h=self.height, al='right' )
        field1 = cmds.intField( w=self.width2, h=self.height )
        field2 = cmds.intField( w=self.width2, h=self.height )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af=[( text1, 'top', 0 ), ( text1, 'left', 0 ),
                             ( text2, 'top', 0 )],
                         ac=[( text1, 'right', 0, field1 ), ( field2, 'left', 0, text2 )],
                         ap=[( field1, 'right', 0, 50 ),( text2, 'left', 0, 50 )] )
        
        self.field1 = field1
        self.field2 = field2
        
        self.form = form
        return form




class WinA_TwoFloatField:
    
    def __init__(self, label1, label2, w1, w2, h ):
        
        self.label1 = label1
        self.label2 = label2
        self.width1 = w1
        self.width2 = w2
        self.height = h
    
    
    def create(self):
        
        form = cmds.formLayout()
        text1 = cmds.text( l= self.label1, w=self.width1, h=self.height, al='right' )
        text2 = cmds.text( l= self.label2, w=self.width1, h=self.height, al='right' )
        field1 = cmds.floatField( w=self.width2, h=self.height )
        field2 = cmds.floatField( w=self.width2, h=self.height )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af=[( text1, 'top', 0 ), ( text1, 'left', 0 ),
                             ( text2, 'top', 0 )],
                         ac=[( text1, 'right', 0, field1 ), ( field2, 'left', 0, text2 )],
                         ap=[( field1, 'right', 0, 50 ),( text2, 'left', 0, 50 )] )
        
        self.field1 = field1
        self.field2 = field2
        
        self.form = form
        return form




class WinA_FloatField:
    
    def __init__(self, label1, w1, w2, h ):
        
        self.label1 = label1
        self.width1 = w1
        self.width2 = w2
        self.height = h
    
    
    def create(self):
        
        form = cmds.formLayout()
        text1 = cmds.text( l= self.label1, w=self.width1, h=self.height, al='right' )
        field1 = cmds.floatField( w=self.width2, h=self.height )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af=[( text1, 'top', 0 ), ( text1, 'left', 0 )],
                         ac=[( text1, 'right', 0, field1 )],
                         ap=[( field1, 'right', 0, 50 )] )
        
        self.field = field1
        
        self.form = form
        return form





class WinA:

    
    def __init__(self):
        
        self.winName = WinA_Global.winName
        self.title   = WinA_Global.title
        self.width   = WinA_Global.width
        self.height  = WinA_Global.height
        
        self.uiTargetCam   = sgBFunction_ui.PopupFieldUI_b( 'Target Camera : ' )
        self.uiResolution  = WinA_TwoIntField( "Resolusion Width : ", "Resolusion Height : ", 120, 80, 22 )
        self.uiSepGroup    = WinA_TwoIntField( "Sep Group Width num : ", "Sep Group Height num : ", 120, 80, 22 )
        self.uiSeparate    = WinA_TwoIntField( "Sep Width : ", "Sep Height : ", 120, 80, 22 )
        self.uiResult      = WinA_TwoFloatField( "Result Width : ", "Result Height", 120, 80, 22 )
        self.uiWindowScale = WinA_FloatField( "Window Scale : ", 120, 80, 22 )


    def create(self):

        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title=self.title )

        form = cmds.formLayout()
        uiTargetCamForm  = self.uiTargetCam.create()
        uiResolutionForm = self.uiResolution.create()
        uiSepGroupForm   = self.uiSepGroup.create()
        uiSeparateForm   = self.uiSeparate.create()
        uiResultForm     = self.uiResult.create()
        uiCheckBox        = cmds.checkBox( l='Create Window', cc= WinA_Cmd.uiCmdCheckOnOff )
        uiWindowScaleForm= self.uiWindowScale.create()
        uiButton1From     = cmds.button( l='C R E A T E', c= WinA_Cmd.cmdCreate )
        uiButton2From     = cmds.button( l='C L E A R', c= WinA_Cmd.cmdClear )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[( uiTargetCamForm, 'top', 5 ), ( uiTargetCamForm, 'left', 5 ), ( uiTargetCamForm, 'right', 5 ),
                             ( uiResolutionForm, 'left', 5 ), ( uiResolutionForm, 'right', 5 ),
                             ( uiSepGroupForm, 'left', 5 ), ( uiSepGroupForm, 'right', 5 ),
                             ( uiSeparateForm, 'left', 5 ), ( uiSeparateForm, 'right', 5 ),
                             ( uiResultForm, 'left', 5 ), ( uiResultForm, 'right', 5 ),
                             ( uiCheckBox, 'left', 165 ),
                             ( uiWindowScaleForm, 'left', 5 ),( uiWindowScaleForm, 'right', 5 ),
                             ( uiButton1From, 'left', 2 ),   ( uiButton1From, 'right', 2 ),
                             ( uiButton2From, 'left', 2 ),   ( uiButton2From, 'right', 2 ),   ( uiButton2From, 'bottom', 2 )],
                         ac=[( uiResolutionForm, 'top', 10, uiTargetCamForm ),
                             ( uiSepGroupForm, 'top', 10, uiResolutionForm ),
                             ( uiSeparateForm, 'top', 10, uiSepGroupForm ),
                             ( uiResultForm, 'top', 10, uiSeparateForm ),
                             ( uiCheckBox, 'top', 10, uiResultForm ),
                             ( uiWindowScaleForm, 'top', 10, uiCheckBox ),
                             ( uiButton1From, 'top', 15, uiWindowScaleForm ),
                             ( uiButton2From, 'top', 2, uiButton1From )])
        
        cmds.window( self.winName, e=1, wh=[ self.width, self.height ], rtf=1 )
        cmds.showWindow( self.winName )
        
        cmds.intField( self.uiResolution.field1, e=1, v=1920, cc= WinA_Cmd.uiCmdChangeCondition )
        cmds.intField( self.uiResolution.field2, e=1, v=1080, cc= WinA_Cmd.uiCmdChangeCondition )
        cmds.intField( self.uiSepGroup.field1, e=1, v=1, cc= WinA_Cmd.uiCmdChangeCondition )
        cmds.intField( self.uiSepGroup.field2, e=1, v=1, cc= WinA_Cmd.uiCmdChangeCondition )
        cmds.intField( self.uiSeparate.field1, e=1, v=2, cc= WinA_Cmd.uiCmdChangeCondition )
        cmds.intField( self.uiSeparate.field2, e=1, v=2, cc= WinA_Cmd.uiCmdChangeCondition )
        cmds.floatField( self.uiResult.field1, e=1, v=960, en=0 )
        cmds.floatField( self.uiResult.field2, e=1, v=540, en=0 )
        cmds.floatField( self.uiWindowScale.field, e=1, v=0.5, pre=2, en=0 )
        
        WinA_Global.camField  = self.uiTargetCam._field
        WinA_Global.resField1 = self.uiResolution.field1
        WinA_Global.resField2 = self.uiResolution.field2
        WinA_Global.sepGroup1 = self.uiSepGroup.field1
        WinA_Global.sepGroup2 = self.uiSepGroup.field2
        WinA_Global.sepField1 = self.uiSeparate.field1
        WinA_Global.sepField2 = self.uiSeparate.field2
        WinA_Global.resultField1 = self.uiResult.field1
        WinA_Global.resultField2 = self.uiResult.field2
        WinA_Global.scaleField= self.uiWindowScale.field
        WinA_Global.createWindowCheck  = uiCheckBox

