import maya.cmds as cmds
import assign
import controlerConnection as ctlCon
import fixShapeEditMode


class AssignPsd_uiCmd:
    
    def __init__(self, uiPointer ):
        
        self._uiPointer = uiPointer
    
    
    def controlerModeCheck( self, ctl ):
        
        if not cmds.objExists( ctl ): return False 
        
        if not cmds.attributeQuery( 'fixShapeMode', node=ctl, ex=1 ):
            
            cmds.addAttr( ctl, ln='fixShapeMode', at='bool' )
            return False
        
        return cmds.getAttr( ctl+'.fixShapeMode' )
            
            

    def loadSel(self, *args ):
    
        sels = cmds.ls( sl=1 )
        
        selItem = sels[-1]
        
        cmds.textField( self._uiPointer.txf, e=1, tx=selItem )
        
        self.controlerModeCheck( selItem )
        self._uiPointer.fixModeButton_condition()
            
            
    def selControlCmd(self, *args ):
        
        targetCtl = cmds.textField( self._uiPointer.txf, q=1, tx=1 )
        
        if not targetCtl: return None
        
        if cmds.objExists( targetCtl ):
            
            cmds.select( targetCtl )
            
            
            
    def assignCmd(self, *args):
        
        targetCtl = cmds.textField( self._uiPointer.txf, q=1, tx=1 )
        
        sels = cmds.ls( sl=1 )
        
        targets = sels[:-1]
        base = sels[-1]
        
        assign.Assign( targets, base )
        
        ctlCon.ConnectWidthMainBlendShape( targetCtl, base )
        
        
        
    def editMode(self, *args ):
        
        targetCtl = cmds.textField( self._uiPointer.txf, q=1, tx=1 )
        
        self._editModeInst = fixShapeEditMode.Control( targetCtl )

        #self._editModeInst.fixShapeExistCheck()
        self._editModeInst.edit()
        
        cmds.setAttr( targetCtl+'.fixShapeMode', True )
        self._uiPointer.fixModeButton_condition()
        
        
        
    def assignMode(self, *args ):

        targetCtl = cmds.textField( self._uiPointer.txf, q=1, tx=1 )
        
        editModeInst = fixShapeEditMode.Control( targetCtl )
        editModeInst.assign( targetCtl )
        
        cmds.setAttr( targetCtl+'.fixShapeMode', False )
        self._uiPointer.fixModeButton_condition()
        

class AssignPsd_ui:
    
    def __init__(self):

        self.uiCmd = AssignPsd_uiCmd( self )

        if cmds.uiTemplate( 'worldBasePsdTemplate', exists=True ):
            cmds.deleteUI( 'worldBasePsdTemplate', uiTemplate=True )
            
        template = cmds.uiTemplate( 'worldBasePsdTemplate' )
        cmds.text( defineTemplate=template, l='' )

        if cmds.window( "assignPsd_ui", ex=1 ):
            cmds.deleteUI( "assignPsd_ui" )
        
        self.win = cmds.window( "assignPsd_ui", title="Assign   UI" )

        cmds.columnLayout()
        
        cmds.setUITemplate( template, pushTemplate=True )
        
        cmds.rowColumnLayout( nc=3, cw=[(1,120),(2,120),(3,60)] )
        cmds.text( l='Blend Shape Controler' )
        self.txf = cmds.textField()
        cmds.popupMenu()
        cmds.menuItem( l='Load Selected', c=self.uiCmd.loadSel )
        cmds.button( l='Select', c= self.uiCmd.selControlCmd )
        cmds.setParent( '..' )
        
        cmds.text(h=10)
        
        cmds.rowColumnLayout( nc=3, cw=[(1,50),(2,200),(3,50)] )
        cmds.text()
        cmds.button( l="Assign BlendShape", c=self.uiCmd.assignCmd, h=25 )
        cmds.text()
        cmds.setParent( '..' )
        
        cmds.text()
        cmds.rowColumnLayout( nc=1, cw=(1,300) )
        cmds.separator()
        cmds.setParent( '..' )
        cmds.text()
        
        cmds.rowColumnLayout( nc=3, cw=[(1,50),(2,200),(3,50)] )
        cmds.text()
        self.fixModeButton = cmds.button( l="", h=25 )
        self.fixModeButton_condition()
        cmds.text()
        cmds.setParent( '..' )
        cmds.text()
        
        '''
        cmds.rowColumnLayout( nc=1, cw=( 1,300 ) )
        self.scroll = cmds.textScrollList()
        '''
        
        cmds.window( self.win, e=1, wh=( 305, 150 ) )
        cmds.showWindow( self.win )
        
        cmds.setUITemplate( template, popTemplate=True )
        
        self.scriptJobSetting()
    
    def fixModeButton_condition(self, *args ):
        
        targetCtl = cmds.textField( self.txf, q=1, tx=1 )
        
        isFixMode = self.uiCmd.controlerModeCheck( targetCtl )
        
        if not isFixMode:
            cmds.button( self.fixModeButton, e=1, l='Fix Shape Edit Mode', c=self.uiCmd.editMode, bgc=[0.7,0.7,0.7] )
            
        else:
            cmds.button( self.fixModeButton, e=1, l='Assign Fix Shape', c=self.uiCmd.assignMode, bgc=[0.579,1,0.579] )
            
            
    def scriptJobSetting(self):
        
        cmds.scriptJob( e=['Undo', self.fixModeButton_condition ], p=self.win )
        cmds.scriptJob( e=['Redo', self.fixModeButton_condition ], p=self.win )