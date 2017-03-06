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
        
        
    def cmdCreateRivet(self, *args ):
        
        meshName = cmds.textFieldGrp( self.tf_meshName, q=1, tx=1 )
        centerIndicesStr = cmds.textFieldGrp( self.tf_centerIndices, q=1, tx=1 )
        aimIndicesStr = cmds.textFieldGrp( self.tf_aimIndices, q=1, tx=1 )
        upIndicesStr = cmds.textFieldGrp( self.tf_upIndices, q=1, tx=1 )
        aimPivIndicesStr = cmds.textFieldGrp( self.tf_aimPivIndices, q=1, tx=1 )
        upPivIndicesStr = cmds.textFieldGrp( self.tf_upPivIndices, q=1, tx=1 )
        
        centerIndices = []
        aimPivIndices = []
        aimIndices    = []
        upPivIndices  = []
        upIndices     = []
        
        for indexStr in centerIndicesStr.split( ',' ):
            centerIndices.append( int( indexStr ) )
        for indexStr in aimIndicesStr.split( ',' ):
            aimIndices.append( int( indexStr ) )
        for indexStr in upIndicesStr.split( ',' ):
            upIndices.append( int( indexStr ) )
        
        if aimPivIndicesStr:
            for indexStr in aimPivIndicesStr.split( ',' ):
                aimPivIndices.append( int( indexStr ) )
        if upPivIndicesStr:
            for indexStr in upPivIndicesStr.split( ',' ):
                upPivIndices.append( int( indexStr ) )
        
        aimIndex = cmds.optionMenuGrp( self.op_aimAxis, q=1, select=1 )-1
        upIndex  = cmds.optionMenuGrp( self.op_upAxis,  q=1, select=1 )-1
        
        print aimIndex, upIndex
        
        cmdModel.createRivet( meshName, centerIndices, aimPivIndices, aimIndices, upPivIndices, upIndices, aimIndex, upIndex )
        
        
    def cmdCancel(self, *args ):
        
        cmds.deleteUI( self.winName, wnd=1 )
    
    
    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title )
        
        cmds.columnLayout()
        columnWidth = self.width -2
        firstWidth = ( columnWidth - 2 ) * 0.4
        secondWidth = ( columnWidth -2 ) - firstWidth
        cmds.rowColumnLayout( nc=1, cw=[(1,self.width-2)])
        tf_meshName = cmds.textFieldGrp( l='Target Mesh : ', cw=[(1,firstWidth),(2,secondWidth)] ); UI_meshPopup()
        tf_centerIndices = cmds.textFieldGrp( l='Center Indices : ', cw=[(1,firstWidth),(2,secondWidth)] ); UI_indicesPopup( tf_meshName )
        tf_aimIndices = cmds.textFieldGrp( l='Aim Indices : ', cw=[(1,firstWidth),(2,secondWidth)] ); UI_indicesPopup( tf_meshName )
        tf_upIndices = cmds.textFieldGrp( l='Up Indices : ', cw=[(1,firstWidth),(2,secondWidth)] ); UI_indicesPopup( tf_meshName )
        cmds.separator()
        tf_aimPivIndices = cmds.textFieldGrp( l='Aim Piv Indices : ', cw=[(1,firstWidth),(2,secondWidth)] ); UI_indicesPopup( tf_meshName )
        tf_upPivIndices = cmds.textFieldGrp( l='Up Piv Indices : ', cw=[(1,firstWidth),(2,secondWidth)] ); UI_indicesPopup( tf_meshName )
        cmds.setParent( '..' )
        
        firstWidth = ( columnWidth - 2 ) * 0.5
        secondWidth = ( columnWidth -2 ) - firstWidth
        textWidth = firstWidth*0.6
        menuWidth = firstWidth - textWidth
        cmds.rowColumnLayout( nc=2, cw=[(1,firstWidth),(2,secondWidth)])
        optionAimAxis = cmds.optionMenuGrp( l= 'Aim Axis : ' , cw=[(1,textWidth),(2,menuWidth)])
        cmds.menuItem( l='X' );cmds.menuItem( l='Y' );cmds.menuItem( l='Z' );
        cmds.menuItem( l='-X' );cmds.menuItem( l='-Y' );cmds.menuItem( l='-Z' );
        optionUpAxis = cmds.optionMenuGrp( l= 'Up Axis : ' , cw=[(1,textWidth),(2,menuWidth)])
        cmds.menuItem( l='X' );cmds.menuItem( l='Y' );cmds.menuItem( l='Z' );
        cmds.menuItem( l='-X' );cmds.menuItem( l='-Y' );cmds.menuItem( l='-Z' );
        cmds.optionMenuGrp( optionUpAxis, e=1, select=2 )
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=2, cw=[(1,firstWidth),(2,secondWidth)])
        cmds.button( l='Create', h=25, c=self.cmdCreateRivet )
        cmds.button( l='Cancel', h=25, c=self.cmdCancel )
        
        cmds.window( self.winName, e=1,
                     w = self.width, h = self.height )
        cmds.showWindow( self.winName )
        
        self.tf_meshName      = tf_meshName
        self.tf_centerIndices = tf_centerIndices
        self.tf_aimIndices    = tf_aimIndices
        self.tf_upIndices     = tf_upIndices
        self.tf_aimPivIndices    = tf_aimPivIndices
        self.tf_upPivIndices     = tf_upPivIndices
        
        self.op_aimAxis = optionAimAxis
        self.op_upAxis  = optionUpAxis