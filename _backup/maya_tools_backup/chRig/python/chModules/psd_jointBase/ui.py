import maya.cmds as cmds
import uifunction as uifunc
import command as mainCmd



class Cmd:
    
    def __init__(self):
        
        pass
    
    
    def selectPsdCmd( self, *args ):
        
        pass
    
    
    
    def refreshTarget(self, *args ):
        
        target = cmds.textField( self._targetMeshField, q=1, tx=1 )
        if not cmds.attributeQuery( 'editMesh', node=target, ex=1 ):
            cmds.addAttr( target, ln='editMesh', at='message' )
        cons = cmds.listConnections( target+'.editMesh' )
        
        mode = 'edit'
        if cons:
            editMesh = cons[0]
            if cmds.attributeQuery( 'isEditMesh', node = editMesh, ex=1 ):
                mode = 'assign'
        
        if mode == 'edit':
            self._editButton.changeToEdit()
        else:
            self._editButton.changeToAssign()
        
        self.loadShapeList()
        self.timeChangeCmd()
        
            


    def loadCmd(self, *args ):
        
        sels = cmds.ls( sl=1 )
        if not sels: return None
        target = sels[-1]
        
        if cmds.attributeQuery( 'isEditMesh', node=target, ex=1 ):
            target = cmds.listConnections( target+'.message' )[0]
        
        cmds.textField( self._targetMeshField, e=1, tx=target )
        self.refreshTarget()
        
        self._editButton._editCmd = []
        self._editButton._assignCmd = []
        self._editButton._editCmd.append( [mainCmd.createEditMesh, target] )
        self._editButton._assignCmd.append( [mainCmd.assignMesh, target] )
        self._editButton._assignCmd.append( [self.refreshTarget, ''] )


    def loadShapeList(self, *args ):
        
        targetObj = cmds.textField( self._targetMeshField, q=1, tx=1 )
        shapeList = mainCmd.getShapeList( targetObj )
        
        children = cmds.scrollLayout( self._targetShapeScroll, q=1, ca=1 )
        if children:
            for child in children:
                cmds.deleteUI( child )
        
        cmds.setParent( self._targetShapeScroll )
        scrollSpace = cmds.text( l='', h=10 )
        
        self._sliders = []
        
        for deltaInfo in shapeList:
            slider = uifunc.Slider( deltaInfo._attrName, self._width-30 )
            slider.connectAttribute( deltaInfo._attrName+'.weight' )
            self._sliders.append( slider )
            
            
    def selectPsdNode(self, *args):
        
        target = cmds.textField( self._targetMeshField, q=1, tx=1 )
        psdNode = mainCmd.getPsdJointBaseNode( target )
        cmds.select( psdNode )
    
    
    
class Show( Cmd ):
    
    def __init__(self, *args ):
        
        self._title   = "PSD Joint Base"
        self._winName = "psd_jointBaseUI"
        
        self._width = 450
        self._height = 400
        
        self.core()
        self.scriptJob()
        self.commandSetting()
        self._sliders = []

        
        
    def scriptJob(self):
        
        cmds.scriptJob( e=['Undo', self.refreshTarget ], p=self._winName )
        cmds.scriptJob( e=['Redo', self.refreshTarget ], p=self._winName )
        #cmds.scriptJob( e=['timeChanged',self.timeChangeCmd], p=self._winName )
        
        
    def core(self):
        
        if cmds.window( self._winName, ex=1 ):
            cmds.deleteUI( self._winName, wnd=1 )
            
        cmds.window( self._winName, title = self._title )
        
        form = cmds.formLayout()
        
        target = cmds.text( '   Target Mesh : ', w=120 )
        field  = cmds.textField()
        cmds.popupMenu()
        cmds.menuItem( l='Select PSD Node', c=self.selectPsdNode )
        button = cmds.button( l='Load', w=60 )
        
        editButton = uifunc.Button()
        
        tap = cmds.tabLayout()
        scroll = cmds.scrollLayout()
        
        cmds.tabLayout( tap, e=1, tabLabel=( scroll, 'Shape List' ) )
        
        cmds.formLayout( form, e=1,
                         attachForm=[(target, 'top', 5), (field, 'top', 5), (button, 'top', 5),
                                     (target, 'left', 5 ), ( tap, 'left', 5 ), ( editButton._button, 'left', 5 ),
                                     (button, 'right',5),(tap,'right',5), ( editButton._button, 'right', 5 ),
                                     (tap,'bottom',5)],
                         attachControl = [(editButton._button, 'top', 20, target ),
                                          (field, 'left', 5, target), (field, 'right', 5, button),
                                          (tap, 'top', 10, editButton._button)] )
        
        cmds.window( self._winName, e=1, wh=[ self._width + 4, self._height ] )
        cmds.showWindow( self._winName )
        
        self._targetMeshField = field
        self._targetMeshButton = button
        self._targetShapeScroll = scroll
        self._editButton = editButton


    def timeChangeCmd(self, *args ):
        
        for slider in self._sliders:
            slider.updateCondition()


    def commandSetting(self):
        
        cmds.button( self._targetMeshButton, e=1, c= self.loadCmd )