import maya.cmds as cmds
from functools import partial
import sgBFunction_ui



class WinA_Global:
    
    winName = 'sgPWindow_projCoc_translateCam'
    title   = 'UI View Controller'
    width   = 1920
    height  = 80 + 1080
        
        



class WinA_Cmd:
    
    @staticmethod
    def getCamControllerAndCamControled( targetCam ):
    
        import sgBFunction_dag
        import sgBFunction_connection
        import sgBFunction_attribute
        
        cloneObject = sgBFunction_dag.getConstrainedObject( targetCam )
        sgBFunction_attribute.addAttr( targetCam, ln='transController', at='message' )
        sgBFunction_attribute.addAttr( targetCam, ln='transControllerP', at='message' )
        sgBFunction_attribute.addAttr( targetCam, ln='camControled', at='message' )
        
        transController  = cmds.listConnections( targetCam+'.transController' )
        transControllerP = cmds.listConnections( targetCam+'.transControllerP' )
        camControled     = cmds.listConnections( targetCam+'.camControled' )
        
        for target in [ transController, transControllerP, camControled ]:
            if not target: continue
            cmds.delete( target )
        
        transControllerP = cmds.createNode( 'transform' )
        transController  = cmds.polyPlane( width=.192, height=.108, subdivisionsHeight=1, subdivisionsWidth=1  )[0]
        camControled     = cmds.duplicate( targetCam )[0]
        
        transController = cmds.parent( transController, transControllerP )[0]
    
        cmds.setAttr( transController+'.rx', -90 )
        cmds.setAttr( transController+'.s', .725, .725, .725 )
        
        cmds.makeIdentity( transController, apply=1, t=1, r=1, s=1, n=0 )
        
        cmds.setAttr( transController+'.overrideEnabled', 1 )
        cmds.setAttr( transController+'.overrideLevelOfDetail', 1 )
        cmds.setAttr( transController+'.overrideDisplayType', 2 )
        
        cmds.setAttr( transControllerP+'.tz', -2.779 )
        
        for attr in [ 'tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz' ]:
            cmds.setAttr( transControllerP+'.'+attr, e=1, lock=1 )
        for attr in [ 'tz', 'rx', 'ry', 'rz' ]:
            cmds.setAttr( transController+'.'+attr, e=1, lock=1, k=0 )
    
        cmds.parent( transControllerP, cloneObject )
    
        camControledShape = sgBFunction_dag.getShape( camControled )
        cmds.setAttr( camControledShape+'.displayResolution', 0 )
        cmds.setAttr( camControledShape+'.displayGateMask', 0 )
        
        cmds.connectAttr( transController+'.tx', camControledShape+'.filmTranslateH' )
        cmds.connectAttr( transController+'.ty', camControledShape+'.filmTranslateV' )
    
        multNode = cmds.createNode( 'multiplyDivide' )
        luminance = cmds.createNode( 'luminance' )
        multDouble = cmds.createNode( 'multDoubleLinear' )
        cmds.setAttr( multNode+'.input1', 1,1,1 )
        cmds.setAttr( multNode+'.op', 2 )
        cmds.connectAttr( transController+'.sx', multNode+'.input2X' )
        cmds.connectAttr( transController+'.sy', multNode+'.input2Y' )
        cmds.connectAttr( transController+'.sz', multNode+'.input2Z' )
        cmds.connectAttr( multNode+'.output', luminance+'.value' )
        cmds.connectAttr( luminance+'.outValue', multDouble+'.input1' )
        cmds.setAttr( multDouble+'.input2', 14 )
        cmds.connectAttr( multDouble+'.output', camControledShape+'.postScale' )
    
        sgBFunction_connection.constraintAll( targetCam, camControled )
        
        cmds.connectAttr( transController +'.message', targetCam+'.transController' )
        cmds.connectAttr( transControllerP+'.message', targetCam+'.transControllerP' )
        cmds.connectAttr( camControled+'.message',     targetCam+'.camControled' )
    
    
    @staticmethod
    def selectController( modelEditor, *args ):

        cam = cmds.modelEditor( modelEditor, q=1, camera=1 )
        transController  = cmds.listConnections( cam+'.transController' )
        cmds.select( transController )





class WinA_ModelEditor:
    
    def __init__(self, width=1920, height=1080, **options ):
        
        self.width = width
        self.height = height
        self.options = options
    
    
    def create(self):
        
        form = cmds.formLayout()
        panLayout = cmds.paneLayout( w=self.width, h=self.height )
        modelEditor = cmds.modelEditor( **self.options )
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[( panLayout, 'top', 0 ), ( panLayout, 'left', 0 ), ( panLayout, 'right', 0 ), ( panLayout, 'bottom', 0 )] )
        
        self.modelEditor = modelEditor
        
        return form




class WinA_ModelPanel:
    
    def __init__(self, width=1920, height=1080, **options ):
        
        self.width = width
        self.height = height
        self.options = options
    
    
    def create(self):
        
        form = cmds.formLayout( w=self.width, h=self.height )
        modelPanel = cmds.modelPanel( **self.options )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[( modelPanel, 'top', 0 ), ( modelPanel, 'left', 0 ), ( modelPanel, 'right', 0 ), ( modelPanel, 'bottom', 0 )] )
        
        self.modelPanel = modelPanel
        
        return form
    




class WinA:
    
    def __init__(self):
        
        self.winName = WinA_Global.winName
        self.title   = WinA_Global.title
        self.width   = WinA_Global.width
        self.height  = WinA_Global.height

        sels = cmds.ls( sl=1 )
        if not sels: cmds.error( "Select Camera" )
        targetCam = sels[0]
        WinA_Cmd.getCamControllerAndCamControled( targetCam )
        
        self.transController  = cmds.listConnections( targetCam+'.transController' )[0]
        self.camControled     = cmds.listConnections( targetCam+'.camControled' )[0]

        self.uiModelEditor1 = WinA_ModelEditor( 1920, int( 1920 * 0.04 ) + 1,   
                                                camera = targetCam, hud=0, cameras=0, dynamics=0, ikHandles=0, nurbsCurves=0,
                                                textures=False, grid=False, da='smoothShaded' )
        self.uiModelEditor2  = WinA_ModelPanel( 1920, 1115, camera = self.camControled )

        cmds.select( self.camControled )

    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title=self.title )
        
        form = cmds.formLayout()
        modelEditorForm = self.uiModelEditor1.create()
        modelPanelForm  = self.uiModelEditor2.create()
        button = cmds.button( l='S E L E C T    P L A N E', h=22, p=form, c= partial( WinA_Cmd.selectController, self.uiModelEditor1.modelEditor ),
                              bgc=[0.7, 0.9, 0.5] )
        cmds.setParent( '..' )
        
        cmds.modelEditor( self.uiModelEditor2.modelPanel, edit=1, displayAppearance='smoothShaded',
                          textures = False, hud=False, grid=False,
                          activeOnly = False )

        cmds.formLayout( form, e=1,
                         af=[ ( modelEditorForm, 'top', 15 ), ( modelEditorForm, 'left', 15 ), ( modelEditorForm, 'right', 15 ),
                              ( modelPanelForm, 'left', 15 ), ( modelPanelForm, 'right', 15 ), ( modelPanelForm, 'bottom', 15 ),
                              ( button, 'left', 15 ), ( button, 'right', 15 ) ],
                         ac=[ ( button, 'top', 5, modelEditorForm ), 
                              ( modelPanelForm, 'top', 5, button ) ] )
        
        cmds.window( self.winName, e=1, wh=[ self.width, self.height ], rtf=1 )
        cmds.showWindow( self.winName )
