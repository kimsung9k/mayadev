import maya.cmds as cmds
import uifunctions as uifnc
import globalInfo

import chModules.jointBasePsd.baseCommand as bcCmd
import chModules.jointBasePsd.assignMeshCommand as amCmd
import chModules.jointBasePsd.functions as fnc
import chModules.jointBasePsd.checkFunctions as chf

import math

from functools import partial


class Cmd:
    
    def __init__(self):
        
        globalInfo.editMeshInst = self
        
        
    def getEditMeshShader(self):
        
        blinns = cmds.ls( type='blinn' )
        
        editMeshShader=None
        for blinn in blinns:
            if cmds.attributeQuery( 'isEditMeshShader', node=blinn, ex=1 ):
                editMeshShader = blinn
                SG = cmds.listConnections( blinn+'.outColor' )[0]
                
        if not editMeshShader:
            blinn = cmds.shadingNode( 'blinn', asShader=1 )
            editMeshShader = cmds.rename( blinn, 'EditMeshShader' )
            cmds.addAttr( editMeshShader, ln='isEditMeshShader', at='bool' )
            SG = cmds.sets( renderable=True, noSurfaceShader=True, empty=1, n='EditMeshSG' )
            cmds.connectAttr( editMeshShader+'.outColor', SG+'.surfaceShader' )
            cmds.setAttr( editMeshShader+'.color', .2,1,.6, type='double3' )
            cmds.setAttr( editMeshShader+'.specularColor', .2,.2,.2, type='double3' )
            
        return editMeshShader,SG
    
    
    def editMeshCmd(self, *args ):
        
        globalInfo.newElement = None
        
        self.checkAngleDriverCondition()
        
        targetMeshs = cmds.textScrollList( globalInfo.meshInfoInst._selMeshList, q=1, ai=1 )
        
        editMeshs = []
        for targetMesh in targetMeshs:
            if not cmds.attributeQuery( 'editMesh', node=targetMesh, ex=1 ):
                cmds.addAttr( targetMesh, ln='editMesh', at='message' )
            editMeshCons = cmds.listConnections( targetMesh+'.editMesh', s=1, d=0 ) 
            if editMeshCons: 
                cmds.delete( editMeshCons )
        
            editMesh = cmds.createNode( 'mesh' )
            targetMeshShape = cmds.listRelatives( targetMesh, s=1 )[0]
            cmds.connectAttr( targetMeshShape+'.outMesh', editMesh+'.inMesh' )
        
            meshObj = cmds.listRelatives( editMesh, p=1 )[0]
            cmds.connectAttr( meshObj+'.message', targetMesh+'.editMesh' )
            meshObj = cmds.rename( meshObj, targetMesh+'_edit0' )
            editMeshs.append( meshObj )

        cmds.refresh()
        
        for targetMesh in targetMeshs:
            targetMeshShape = cmds.listRelatives( targetMesh, s=1 )[0]
            cons = cmds.listConnections( targetMeshShape+'.outMesh', p=1, c=1 )
            cmds.disconnectAttr( cons[0], cons[1] )
        
        blinns = cmds.ls( type='blinn' )
        
        editMeshShader,SG = self.getEditMeshShader()
        
        for meshObj in editMeshs:
            cmds.sets( meshObj, e=1, forceElement=SG )
            
        for targetMesh in targetMeshs:
            cmds.setAttr( targetMesh+'.v', 0 )
            
        self.updateCmd()
            
        
    def assignMesh( self, *args ):
        
        targetMeshs = cmds.textScrollList( globalInfo.meshInfoInst._selMeshList, q=1, ai=1 )
        
        editTargetMeshs = []
        editMeshs = []
        for targetMesh in targetMeshs:
            print targetMesh
            if not cmds.attributeQuery( 'editMesh', node=targetMesh, ex=1 ): continue
            
            cons = cmds.listConnections( targetMesh+'.editMesh', p=1, c=1 )

            editMesh = cons[1].split( '.' )[0]
            
            editTargetMeshs.append( targetMesh )
            editMeshs.append( editMesh )
        
        for i in range( len( editTargetMeshs ) ):
            targetMesh = editTargetMeshs[i]
            editMesh   = editMeshs[i]
            
            driverStrings = cmds.textScrollList( globalInfo.driverInfoInst._driverScrollList, q=1, ai=1 )

            driverAndAttrs = []
            for driverString in driverStrings:
                driver, other = driverString.split( ' | ' )
                attr, value = other.split( ' : ' )
                driverAndAttrs.append( [driver, attr.replace( 'angle', 'outDriver' )] )
                print repr( driver+ attr )
            
            inst = amCmd.Main( editMesh, targetMesh, driverAndAttrs )
            globalInfo.newElement = [inst._node, inst._assignIndex]
            cmds.setAttr( targetMesh+'.v', 1 )
            
        self.updateCmd()
        
        
        
    def editAssigned( self, index, *args ):
        
        targetMeshs = cmds.textScrollList( globalInfo.meshInfoInst._selMeshList, q=1, ai=1 )
        
        if not targetMeshs: return None
        targetMesh = targetMeshs[0]
        
        if not cmds.attributeQuery( 'editAssignedMesh', node = targetMesh, ex=1 ):
            cmds.addAttr( targetMesh, ln='editAssignedMesh', at='message' )
        if not cmds.attributeQuery( 'invMesh', node = targetMesh, ex=1 ):
            cmds.addAttr( targetMesh, ln='invMesh', at='message' )
        
        editMesh, invMesh = cmds.buildSkinMesh( targetMesh, index = index )
        
        cmds.connectAttr( editMesh+'.message', targetMesh+'.editAssignedMesh' )
        cmds.connectAttr( invMesh+'.message',  targetMesh+'.invMesh' )
        
        editMeshShader,SG = self.getEditMeshShader()
        cmds.sets( editMesh, forceElement = SG )
        cmds.setAttr( targetMesh+'.v', 0 )

        self.checkEditMeshCondition()
        
        
        
    def assignedEdited( self, *args ):
        
        targetMeshs = cmds.textScrollList( globalInfo.meshInfoInst._selMeshList, q=1, ai=1 )
        
        if not targetMeshs: return None
        targetMesh = targetMeshs[0]
        
        cons = cmds.listConnections( targetMesh+'.editAssignedMesh' )
        if not cons: return None
        editMesh = cons[0]
        
        cons = cmds.listConnections( targetMesh+'.invMesh' )
        if not cons: return None
        invMesh = cons[0]
        
        cmds.setAttr( targetMesh+'.v', 1 )
        cmds.refresh()
        
        cmds.delete( invMesh, editMesh )
        
        self.checkEditMeshCondition()
        
        
        
    def setDeltaBySelectionCmd(self, *args ):
        
        items = cmds.textScrollList( globalInfo.meshInfoInst._selMeshList, q=1, ai=1 )
        
        if not items : return False
        
        targetMesh = items[0]
        
        sels = cmds.ls( sl=1, fl=1 )
        
        indices = []
        for sel in sels:
            if sel.find( '.vtx' ) != -1:
                indices.append( int( sel.split( '[' )[1].replace( ']','' )) )
        
        chf.setDeltaBySelected( targetMesh, self._deltaIndex, indices )
        
        cmds.select( cl=1 )
        
        self.checkEditMeshCondition()
        
        
        
    def getDeltaModeCondition( self, *args ):
            
        items = cmds.textScrollList( globalInfo.meshInfoInst._selMeshList, q=1, ai=1 )
        
        if not items : return False
        
        targetMesh = items[0]
        
        sels = cmds.ls( sl=1 )
        
        if not sels: return False
        
        for sel in sels:
            if sel.find( targetMesh+'.vtx' ) != -1:
                return True
        
        return False

        
        

    def checkEditMeshCondition( self, *args ):
        
        items = cmds.textScrollList( globalInfo.meshInfoInst._selMeshList, q=1, ai=1 )
        
        if not items: return None
        
        if not cmds.objExists( items[0] ): return None
        
        cons = cmds.listConnections( items[0]+'.editMesh' )
        
        columns = globalInfo.driverInfoInst._rowColumns
        columns += globalInfo.meshInfoInst._rowColumns
        columns += self._rowColumns
        
        if not cons:
            if not cmds.attributeQuery( 'editAssignedMesh', node=items[0], ex=1 ):
                cmds.addAttr( items[0], ln='editAssignedMesh', at='message' )
            
            cons2 = cmds.listConnections( items[0]+'.editAssignedMesh' )
            
            if not cons2:
                if not self.getDeltaModeCondition():
                    cmds.button( self._editButton, e=1, l='Edit Mesh', c=self.editMeshCmd, bgc=[0.392,0.392,0.392] )
                else:
                    cmds.button( self._editButton, e=1, l='Set Delta By Selection', c=self.setDeltaBySelectionCmd, bgc=[1.0, 1.0, 0.5] )
                
            else:
                cmds.button( self._editButton, e=1, l='Assign Edited Mesh', c=self.assignedEdited, bgc=[1.0, 0.8, 0.5])
        else:
            cmds.button( self._editButton, e=1, l='Assign Mesh', c=self.assignMesh, bgc=[0.2,1.0,0.6] )
            
        if cmds.button( self._editButton, q=1, l=1 ) == 'Edit Mesh':
            for column in columns:
                cmds.rowColumnLayout( column, e=1, en=1 )
        else:
            for column in columns:
                cmds.rowColumnLayout( column, e=1, en=0 )
            
            


    def checkAngleDriverCondition(self, *args ):
        
        items = cmds.textScrollList( globalInfo.driverInfoInst._driverScrollList, q=1, ai=1 )
        
        if not items:
            cmds.error( "Add Driver Angle First")
            
        for item in items:
            driverName, other = item.split( ' | ' )
            angleName, value  = other.split( ' : ' )
            angleName = angleName.replace( 'angle', 'outDriver' )
            
            cuValue = cmds.getAttr( driverName+'.'+angleName )
            value   = float( value )
            cuValue = float( "%.2f" % cuValue )
                        
            if cuValue != value: cmds.error( "Loaded Angle Value is not Equal to Current Angle Value. Refresh First.")
            
        for item in items:
            driverName, other = item.split( ' | ' )
            angleName, value  = other.split( ' : ' )
            angleName = angleName.replace( 'angle', 'outDriver' )
            
            if value < 0.1: cmds.error( "%s.%s value is too small" %( driverName, angleName ) )
 
        

    def removeBlendMeshInfoElement(self, nodeName, logicalIndex, *args ):
        
        globalInfo.node = nodeName
        
        cons = cmds.listConnections( nodeName+'.blendMeshInfos[%d].inputMesh' % logicalIndex, s=1, d=0 )
        
        cmds.deleteBlendMeshInfo( nodeName, index = logicalIndex )
        self.addShapeList()
        
        
    def editAnimCurveCmd(self, nodeName, logicalIndex, *args ):
        
        attrName = nodeName+'.blendMeshInfos[%d]' % logicalIndex
        meshName = cmds.getAttr( attrName+'.meshName' )
        
        cons = cmds.listConnections( attrName+'.animCurve' )
        
        if cons:
            animUU = cons[0]
        else:
            animUU = cmds.createNode( 'animCurveUU', n=meshName+'_anim' )
            cmds.setKeyframe( animUU, f=0  , v=0 )
            cmds.setKeyframe( animUU, f=0.5, v=0.5 )
            cmds.setKeyframe( animUU, f=1  , v=1 )
            cmds.setKeyframe( animUU, f=1.5, v=1.5 )
            cmds.setKeyframe( animUU, f=2  , v=2 )
            
            cmds.connectAttr( animUU+'.message', attrName+'.animCurve' )
            cmds.connectAttr( animUU+'.output', attrName+'.animCurveOutput' )
        
        cmds.GraphEditor()
        cmds.select( animUU )
        
        
    def addMirrorMeshCmd(self, logicalIndex, *args ):
        
        items = cmds.textScrollList( globalInfo.meshInfoInst._selMeshList, q=1, ai=1 )
        
        if not items: return None
        
        nodeName = amCmd.getBlendAndFixedShapeNode( items[0] )
        targetName, driverInfo, returnIndex = amCmd.addMirrorTarget( items[0], logicalIndex )
        
        cmds.setParent( self._scrollLay )
        cmds.rowColumnLayout( nc=3, cw=[(1,25),(2,self._mainWidthList[0]-30),(3,self._mainWidthList[1]-30) ] )
        cmds.button( l="X", c= partial( self.removeBlendMeshInfoElement, nodeName, logicalIndex ) )
        meshNameField = cmds.textField( tx=targetName.replace( items[0]+'_', '' ), cc=partial( self.meshNameChangeCmd, nodeName, returnIndex ) )
        self._meshNameList.append( meshNameField )
        cmds.popupMenu( markingMenu = 1 )
        cmds.menuItem( l='Edit Anim Curve', rp='W', c=partial( self.editAnimCurveCmd, nodeName, returnIndex ) )
        cmds.menuItem( l='Edit Mesh',rp='N', c=partial( self.editAssigned, returnIndex) )
        cmds.menuItem( l='Add Mirror Mesh',rp='E', c=partial( self.addMirrorMeshCmd, returnIndex) )
        cmds.menuItem( l='Select Delta Points', rp='S', c=partial( self.selectDeltaPointsCmd, items[0], logicalIndex ) )
        widthList = uifnc.setWidthByPerList( [50,50], self._mainWidthList[1] )
        cmds.rowColumnLayout( nc=2, cw=[(1,widthList[0]),(2,widthList[1]-30)] )
        for element in driverInfo:
            engleName, value1, value2, value3= element
            cmds.text( l= engleName )
            cmds.floatFieldGrp( precision=2, nf=3, cw3=[50,50,50], v1=value1, v2=value2, v3=value3 )
        cmds.setParent( '..' )
                
    
    def meshNameChangeCmd( self, nodeName, index, *args ):
        
        targetString = cmds.textField( self._meshNameList[index], q=1, tx=1 )
        
        items = cmds.textScrollList( globalInfo.meshInfoInst._selMeshList, q=1, ai=1 )
        if not items: return None
        
        realName = items[0] + '_' + targetString
        cmds.setAttr( nodeName+'.blendMeshInfos[%d].meshName' % index, realName, type='string' )
        
        
    def selectDeltaPointsCmd(self, meshObj, index, *args ):
        
        self._deltaIndex = index
        chf.selectDeltaPoints(meshObj, index)
        self.checkEditMeshCondition()


    def updateCmd(self, *args ):
        
        self.addShapeList()
        self.checkEditMeshCondition()


class Add( Cmd ):
    
    def __init__(self, width ):
        
        self._emptyWidth = 10
        self._width = width - self._emptyWidth*2 - 4
        self._height = 170
        
        sepList = [ 30,60 ]
        self._mainWidthList = uifnc.setWidthByPerList( sepList, self._width )
        
        self._rowColumns = []
        Cmd.__init__( self )
        mainLayout = self.core()
        
        self.scriptJob( mainLayout )
        
        
    def scriptJob(self, mainLayout ):
        
        cmds.scriptJob( e=['Undo', self.updateCmd], p=mainLayout )
        cmds.scriptJob( e=['Redo', self.updateCmd], p=mainLayout )
        
    
    def addShapeList(self):
        
        items = cmds.textScrollList( globalInfo.meshInfoInst._selMeshList, q=1, ai=1 )
        
        childrenUIs = cmds.scrollLayout( self._scrollLay, q=1, ca=1 )
        
        if childrenUIs:
            for child in childrenUIs:
                cmds.deleteUI( child )
        
        if not items: return None
        
        for item in items:
            
            self._meshNameList = []
            
            shapeInfoList, nodeName = chf.getShapeInfo( item )
            if not shapeInfoList: continue
            
            cmds.setParent( self._scrollLay )
            
            cmds.rowColumnLayout( nc=3, cw=[(1,25),(2,self._mainWidthList[0]-30),(3,self._mainWidthList[1]-30) ] )
            
            for shapeInfo in shapeInfoList:
                shapeName, angleListAndValues, logicalIndex = shapeInfo
                
                cmds.button( l="X", c= partial( self.removeBlendMeshInfoElement, nodeName, logicalIndex ) )
                meshNameField = cmds.textField( tx=shapeName.replace( item+'_', '' ), cc=partial( self.meshNameChangeCmd, nodeName, shapeInfoList.index( shapeInfo ) ) )
                cmds.popupMenu( markingMenu = 1 )
                cmds.menuItem( l='Edit Anim Curve', rp='W', c=partial( self.editAnimCurveCmd, nodeName, shapeInfoList.index( shapeInfo ) ) )
                cmds.menuItem( l='Edit Mesh', rp='N', c=partial( self.editAssigned, shapeInfoList.index( shapeInfo ) ) )
                cmds.menuItem( l='Add Mirror Mesh', rp='E', c=partial( self.addMirrorMeshCmd, shapeInfoList.index( shapeInfo ) ) )
                cmds.menuItem( l='Select Delta Points', rp='S', c=partial( self.selectDeltaPointsCmd, item, logicalIndex ) )
                self._meshNameList.append( meshNameField )
                
                widthList = uifnc.setWidthByPerList( [50,50], self._mainWidthList[1] )
                cmds.rowColumnLayout( nc=2, cw=[(1,widthList[0]),(2,widthList[1]-30)] )
                for element in angleListAndValues:
                    engleName, value1, value2, value3= element
                    cmds.text( l= engleName )
                    cmds.floatFieldGrp( precision=2, nf=3, cw3=[50,50,50], v1=value1, v2=value2, v3=value3 )
                cmds.setParent( '..' )
            
            cmds.setParent( '..' )
    
        
    def core(self):
        
        mainLayout = cmds.rowColumnLayout( nc=3, cw=[(1, self._emptyWidth), (2,self._width), (3, self._emptyWidth)] )
        uifnc.setSpace()
        self._editButton = cmds.button( l='Edit Mesh', h=30, c=self.editMeshCmd, bgc=[0.376,0.384,0.392] )
        uifnc.setSpace()
        cmds.setParent( '..' )
        
        uifnc.setSpace(5)
        
        column1 = cmds.rowColumnLayout( nc=3, cw=[(1, self._emptyWidth), (2,self._width), (3, self._emptyWidth)] )
        uifnc.setSpace()
        self._scrollLay = cmds.scrollLayout( h=self._height )
        cmds.popupMenu()
        cmds.menuItem( l='Refresh', c= self.updateCmd )
        cmds.setParent( '..' )
        uifnc.setSpace()
        cmds.setParent( '..' )
        
        self._rowColumns = [column1]
        
        return mainLayout