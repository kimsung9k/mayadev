import maya.cmds as cmds
import sgBFunction_ui
import sgRigCurve
import sgRigAttribute
    


class Window:
    
    def __init__(self):
        
        self.uiname = 'sgUISgWobbleCurve'
        self.title   = 'SG Wobble Curve'
        self.width   = 400
        self.height  = 50
        
        self.popupController = sgBFunction_ui.PopupFieldUI( 'Wobble Controller : ', 'load Selected', 'single', position = 40 )
        self.popupCurves     = sgBFunction_ui.PopupFieldUI( 'Target Curves : ', 'load Selected', 'multi', position = 40 )
    
    
    def cmdCreate(self, *args ):
        
        import sgBFunction_dag
        
        controller = self.popupController.getFieldText()
        curves = self.popupCurves.getFieldTexts()
        
        curves = sgBFunction_dag.getChildrenShapeExists( curves )
        
        copyAttrs = [ 'globalEnvelope', 'globalWave1', 'globalTimeMult1', 'globalOffset1', 'globalLength1', 'globalWave2', 'globalTimeMult2', 'globalOffset2', 'globalLength2' ]
        
        targetCrvs = []
        aimMatrixs = []
        
        targetCrvGrps = cmds.createNode( 'transform', n= 'WobbleCurveGrp' )
        aimMatrixGrps = cmds.createNode( 'transform', n= 'aimMatrixGrp' )
        
        for curve in curves:
            targetCrv, aimMatrix = sgRigCurve.createSgWobbleCurve( curve, True, True, '_wobble' )
            
            targetCrvs.append( targetCrv )
            aimMatrixs.append( aimMatrix )
            
            for copyAttr in copyAttrs:
                sgRigAttribute.copyAttribute( targetCrv+'.'+copyAttr, controller )
                cmds.connectAttr( controller+'.'+copyAttr, targetCrv+'.'+copyAttr )
        
        cmds.parent( targetCrvs, targetCrvGrps )
        cmds.parent( aimMatrixs, aimMatrixGrps )


    def show(self):
        
        columnWidth = self.width -2
        
        if cmds.window( self.uiname, ex=1 ):
            cmds.deleteUI( self.uiname, wnd=1 )
        cmds.window( self.uiname, title= self.title )
        
        cmds.columnLayout()
        
        self.columnNewSystem = cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)])
        self.popupController.create()
        self.popupCurves.create()
        cmds.setParent( '..' )
        
        cmds.separator( w=self.width )
        
        cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth )])
        cmds.button( l='Create', en=1, c= self.cmdCreate )
        cmds.setParent( '..' )
        
        cmds.window( self.uiname, e=1,
                     w = self.width, h = self.height )
        cmds.showWindow( self.uiname )


mc_showWindow = """import sgUIsgWobbleCurve
sgUIsgWobbleCurve.Window().show()"""