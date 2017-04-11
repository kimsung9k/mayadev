import maya.cmds as cmds

import uiModel
import cmdModel



class UI_indicesPopup:
    def __init__(self, targetMeshField ):
        self.popup = cmds.popupMenu()
        cmds.menuItem( l='Load Indices', c=self.load )
        self.targetMeshField = targetMeshField

    def load(self, *args ):
        mesh, indicesStr = cmdModel.getIndicesFromSelected()
        targetField = self.popup.split( '|' )[-2]
        cmds.textFieldGrp( targetField, e=1, tx=indicesStr )
        cmds.textFieldGrp( self.targetMeshField, e=1, tx=mesh )




class UI_meshPopup:
    def __init__(self):
        self.popup = cmds.popupMenu()
        cmds.menuItem( l='Laad Mesh', c=self.load )
        
    def load(self, *args ):
        mesh = cmdModel.getMeshFromSelected()
        targetField = self.popup.split( '|' )[-2]
        cmds.textFieldGrp( targetField, e=1, tx=mesh )




class Window:
    
    def __init__(self):
        
        self.winName = uiModel.winName
        self.title   = uiModel.title
        self.width   = uiModel.width
        self.height  = uiModel.height
        
        
    def cmdCreateOffsetCurve(self, *args ):
        
        offsetValue = cmds.floatSliderGrp( self.floatSlider, q=1, v=1 )
        
        sels = cmds.ls( sl=1, tr=1 )
        curves = sels[:-1]
        mesh = cmds.listRelatives( sels[-1],s=1 )[0]
        for curve in curves:
            curveShape= cmds.listRelatives( curve, s=1 )[0]
            cmdModel.offsetCurveBasedOnMesh( curveShape, mesh, offsetValue )
            
            
    def cutCurve(self, *args ):
        
        sels = cmds.ls( sl=1 )
        curves = sels[:-1]
        mesh = cmds.listRelatives( sels[-1], s=1 )[0]
        for curve in curves:
            curveShape= cmds.listRelatives( curve, s=1 )[0]
            try:cmdModel.cutCurve( curveShape, mesh )
            except:pass


    def cmdCreateCurveFromEdge(self, *args):
        
        cmdModel.createCurveToEdgeLoop()


    def cmdCancel(self, *args ):
        
        cmds.deleteUI( self.winName, wnd=1 )
    
    
    def create(self, *args ):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title, tbm=0 )
        
        cmds.columnLayout()
        columnWidth = self.width -2
        
        cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)] )
        cmds.button( l='Create Curve From Edge', c=self.cmdCreateCurveFromEdge )
        cmds.setParent( '..' )
        
        textWidth = (columnWidth-2)*0.3
        fieldWidth = 50
        sliderWidth = ( columnWidth-2 ) - fieldWidth - textWidth
        cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)])
        floatSlider = cmds.floatSliderGrp( l='Offset Rate :', f=1, cw=[(1,textWidth),(2,fieldWidth),(3,sliderWidth)], fmn=0, fmx=1, min=0, max=1, pre=2, v=0.5 )
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)] )
        cmds.button( l='Offset', h=25, c=self.cmdCreateOffsetCurve )
        cmds.button( l='Cut Curve', c=self.cutCurve )
        cmds.button( l='Cancel', h=25, c=self.cmdCancel )
        cmds.setParent( '..' )
        
        cmds.window( self.winName, e=1,
                     w = self.width, h = self.height )
        cmds.showWindow( self.winName )
        
        self.floatSlider = floatSlider

mc_showWindow = """import projectFunction.towerOfGod.view
projectFunction.towerOfGod.view.Window().create()
"""