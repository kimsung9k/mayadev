import maya.cmds as cmds
from functools import partial
import command as mainCmd


class Button:
    
    def __init__(self):
        
        self._button = cmds.button( l='Edit Mesh', h=30, bgc=[0.392,0.392,0.392] )
        self._assignCmd = []
        self._indexAssignCmd = []
        self._editCmd  =  []
        
        cmds.button( self._button, e=1, c= self.editCmd )


    def assignCmd(self, *args ):
        
        for cmd, data in self._assignCmd:
            cmd( data )
            
        self.changeToEdit()
    
    
    def editCmd(self, *args ):
        
        for cmd, data in self._editCmd:
            cmd( data )
            
        self.changeToAssign()


    
    def changeToEdit( self, *args ):
        
        cmds.button( self._button, e=1, l='Edit Mesh', bgc=[0.392,0.392,0.392], c=self.editCmd )
    
        
    def changeToAssign(self, *args):
        
        cmds.button( self._button, e=1, l='Assign Mesh', bgc=[0.2,1.0,0.6], c=self.assignCmd )

    
    
    
class Slider:
    
    def __init__(self, attrName, width ):
        
        width = width
        deltaName = cmds.getAttr( attrName+'.deltaName' )
        value = cmds.getAttr( attrName+'.weight' )
        
        nameWidth  = 140
        fieldWidth = 70
        sliderWidth = width - nameWidth - fieldWidth 
        self._row  = cmds.rowColumnLayout( nc=3, cw=[(1,nameWidth),(2,fieldWidth),(3,sliderWidth)], 
                                           co=[(1,'left',8 ), (2,'right',5)], h=30 )
        self._textRow = cmds.rowColumnLayout( nc=1, cw=[(1,nameWidth-15)] )
        self._textRowPopup = cmds.popupMenu( mm=1 )
        self._text = cmds.text( al='left', h=20 )
        cmds.setParent( '..' )
        self._field = cmds.floatField( min=0.0, max=1.0 )
        self._fieldPopup = cmds.popupMenu()
        self._slider = cmds.floatSlider( min=0.0, max=1.0 )
        cmds.setParent( '..' )
        
        cmds.text( self._text, e=1, l=deltaName )
        cmds.floatField( self._field, e=1, v=value )
        cmds.floatSlider( self._slider, e=1, v=value )

        self._dragStart = False
        self._keepValue = 0.0
        self._attrName = attrName
        
        cmds.menuItem( l='Select Anim Curve', rp='W', c= self.selectAnimCurveCmd, p=self._textRowPopup )
        cmds.menuItem( l='Change Name', rp='E', c= self.changeNameMoveCmd, p=self._textRowPopup )
        cmds.menuItem( l='Delete Shape', rp='S', c= self.deleteShapeCmd, p=self._textRowPopup )
        #cmds.menuItem( l='Edit Mesh', rp='N', c=self.editMeshCmd, p=self._textRowPopup )
        
        cmds.menuItem( l='Set Key', c= self.setKeyCmd, p=self._fieldPopup )
        cmds.menuItem( l='Break Connection', c= self.breakConnectionCmd, p=self._fieldPopup )
        
        
    def updateCondition( self, *args ):
        
        namePlug = self._attrName+'.weight'
        self._keepValue = cmds.getAttr( namePlug )
        cmds.floatField( self._field, e=1, v= self._keepValue )
        cmds.floatSlider( self._slider, e=1, v= self._keepValue )
        
        cons = cmds.listConnections( namePlug )
        
        if not cons:
            cmds.floatField( self._field, e=1, bgc=[0.1,0.1,0.1] )
        else:
            if cmds.nodeType( cons[0] ) == 'animCurveTU':
                cmds.floatField( self._field, e=1, bgc=[0.95,0.45,0.45] )
                
                
    
    def editMeshCmd(self, *args ):
        
        target = self._attrName.split( '.' )[0]
        
        hists = cmds.listHistory( target )

        for hist in hists:
            if cmds.nodeType( hist ) == 'mesh':
                target = cmds.listRelatives( hist, p=1 )[0]
                break
        
        logicalIndex = int( self._attrName.split('[')[1].replace( ']', '' ) )
        mainCmd.indexAssignMesh(target, logicalIndex )
                
                
        
    def deleteShapeCmd(self, *args ):
        
        namePlug = self._attrName
        logicalIndex = int( self._attrName.split('[')[1].replace( ']', '' ) )
        nameNode = namePlug.split( '.' )[0]
        
        cons = cmds.listConnections( namePlug+'.weight' )
        if cons: cmds.delete( cons )
        cmds.psdJointBase_deleteIndex( nameNode, i=logicalIndex )
        cmds.deleteUI( self._row )
    
        
    def setKeyCmd(self, *args ):
        
        namePlug = self._attrName+'.weight'
        cmds.setKeyframe( namePlug )
        self.updateCondition()
        
    
    
    def selectAnimCurveCmd(self, *args ):
        
        namePlug = self._attrName+'.weight'
        cons = cmds.listConnections( namePlug )
        
        if cons:
            cmds.select( cons[0] )
            
            
    def breakConnectionCmd(self, *args ):
        
        namePlug = self._attrName+'.weight'
        cons = cmds.listConnections( namePlug )
        
        if cons:
            cmds.delete( cons[0] )
            self.updateCondition()
            
    
        
    def changeNameMoveCmd(self, *args ):
        
        children = cmds.rowColumnLayout( self._textRow, q=1, ca=1 )
        
        namePlug = self._attrName+'.deltaName'
        try: 
            nameShape = cmds.text( children[0], q=1, l=1 )
            cmds.deleteUI( children[0] )
            cmds.setParent( self._textRow )
            cmds.textField( tx= nameShape, h=20 )
        except:
            nameShape = cmds.textField( children[0], q=1, tx=1 )
            cmds.deleteUI( children[0] )
            cmds.setParent( self._textRow )
            cmds.text( l= nameShape, al='left', h=20 )
            cmds.setAttr( namePlug, nameShape, type='string' )
            
        
    def fieldDragCmd(self, attr, *args ):
        
        value = cmds.floatField( self._field, q=1, v=1 )
        cmds.floatSlider( self._slider, e=1, v=value )
        
        if not self._dragStart:
            self._dragStart = True
            cmds.undoInfo( swf=0 )
        
        cmds.setAttr( attr, value )
        
    
    def fieldChangeCmd(self, attr, *args ):
        
        value = cmds.floatField( self._field, q=1, v=1 )
        cmds.floatSlider( self._slider, e=1, v=value )
        cmds.setAttr( attr, value )
        
        if self._dragStart:
            self._dragStart = False
            cmds.setAttr( attr, self._keepValue )
            cmds.undoInfo( swf=1 )
            
        cmds.setAttr( attr, value )
        self._keepValue = value


    def sliderDragCmd(self, attr, *args ):
        
        value = cmds.floatSlider( self._slider, q=1, v=1 )
        cmds.floatField( self._field, e=1, v=value )
        
        if not self._dragStart:
            self._dragStart = True
            cmds.undoInfo( swf=0 )
        
        cmds.setAttr( attr, value )


    def sliderChangeCmd(self, attr, *args ):
        
        value = cmds.floatSlider( self._slider, q=1, v=1 )
        cmds.floatField( self._field, e=1, v=value )
        cmds.setAttr( attr, value )

        if self._dragStart:
            self._dragStart = False
            cmds.setAttr( attr, self._keepValue )
            cmds.undoInfo( swf=1 )
        
        cmds.setAttr( attr, value )
        self._keepValue = value

    
    def sliderSetMinMaxCmd(self, minValue=0.0, maxValue=1.0, *args ):
        
        cmds.floatSlider( self._slider, e=1, min=minValue, max=maxValue )
        
        
    def connectAttribute( self, attr ):
        
        cmds.floatSlider( self._slider, e=1, 
                             cc=partial( self.sliderChangeCmd, attr ), 
                             dc=partial( self.sliderDragCmd, attr ) )
        
        cmds.floatField( self._field, e=1, 
                             cc=partial( self.fieldChangeCmd, attr ), 
                             dc=partial( self.fieldDragCmd, attr ) )
        
        self._keepValue = cmds.getAttr( attr )