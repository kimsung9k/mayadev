import maya.cmds as cmds
import chModules.jointBasePsd.ui.uifunctions as uifnc
import chModules.jointBasePsd.baseCommand as bcCmd
import chModules.jointBasePsd.editMeshCommand as emCmd
import chModules.jointBasePsd.assignMeshCommand as amCmd
import listLays
import math
from functools import partial


class Cmd( object ):
    
    def __init__(self):
        
        self._assignMeshTargets = []
        self._movedDrivers = []
    

    def loadCmd(self, *args ):
        
        sels = cmds.ls( sl=1 )
        
        cmds.textField( self._driverRootField, e=1, tx= sels[-1] )
        
        width = cmds.scrollLayout( self._driverListLay, q=1, width=1 )
        self.refreshDriverCmd( (width+2)*.95 )
        self.updateSkinedObjects()
        self.updateEditMeshMode()

    
    def refreshDriverCmd(self, width, *args ):
        
        rootName = cmds.textField( self._driverRootField, q=1, tx=1 )
        minValue = cmds.floatField( self._minValueField, q=1, v=1 )
        movedDriverCheck = cmds.checkBox( self._movedDriverCheck, q=1, v=1 )
        
        movedDriverInst = listLays.MovedDriverList( width, minValue )
        
        children = cmds.listRelatives( rootName, c=1, ad=1 )
        
        angleDriverList = []
        for child in children:
            hists = cmds.listHistory( child )
            
            for hist in hists:
                if cmds.nodeType( hist ) == 'angleDriver':
                    if not hist in angleDriverList:
                        angleDriverList.append( hist )
        
        showDrivers = []
        
        for driver in angleDriverList:
            
            if movedDriverCheck:
                angle1, angle2, angle3 = cmds.getAttr( driver+'.outDriver' )[0]
                
                if math.fabs( angle1 ) > minValue or math.fabs( angle2 ) > minValue or math.fabs( angle3 ) > minValue:
                    showDrivers.append( driver )
            else:
                showDrivers.append( driver )
        
        childUis = cmds.scrollLayout( self._driverListLay, q=1, ca=1 )
        
        if childUis:
            for childUi in childUis:
                cmds.deleteUI( childUi )
        
        cmds.setParent( self._driverListLay )
        
        for driver in showDrivers:
            values = cmds.getAttr( driver+'.outDriver' )[0]
            movedDriverInst.add( driver, values )
            
        self._movedDrivers = showDrivers
            
            
    def updateSkinedObjects(self, *args ):
        
        rootName = cmds.textField( self._driverRootField, q=1, tx=1 )

        childJnts = cmds.listRelatives( rootName, c=1, ad=1, type='joint' )
        
        skinClusterList = []
        for child in childJnts:
            skinClNodes = cmds.listConnections( child, s=0, d=1, type='skinCluster' )
            
            if not skinClNodes:
                continue
            
            for skinCl in skinClNodes:
                if not skinCl in skinClusterList:
                    skinClusterList.append( skinCl )
            
        meshObjs = cmds.ls( type='mesh' )
        
        targetMeshObjs = []
        
        for meshObj in meshObjs:
            
            if not cmds.objExists( meshObj ):
                continue
            
            hists = cmds.listHistory( meshObj, pdo=1 )
            
            if not hists: continue
            
            for hist in hists:
                if cmds.nodeType( hist ) == 'skinCluster':
                    if hist in skinClusterList:
                        if bcCmd.blendAndFixedShapeExists( meshObj ):
                            meshObjP = cmds.listRelatives( meshObj, p=1 )[0]
                            targetMeshObjs.append( meshObjP )
                            break
                        
        cmds.textScrollList( self._meshList, e=1, ra=1, a=targetMeshObjs )
        
    
    def updateEditMeshMode(self, *args ):
        
        targetMeshs = cmds.textScrollList( self._meshList, q=1, ai=1 )
        
        editMeshTargetEx = False
        
        self._assignMeshTargets = []
        for targetMesh in targetMeshs:
            
            if not cmds.attributeQuery( 'editMeshTarget', node=targetMesh, ex=1 ):
                cmds.addAttr( targetMesh, ln='editMeshTarget', at='message' )
            
            cons = cmds.listConnections( targetMesh+'.editMeshTarget' )
            
            if cons:
                editMeshTargetEx = True
                self._assignMeshTargets.append( targetMesh )
        
        if editMeshTargetEx:
            cmds.button( self._editMeshButton, e=1, l='Assine Mesh', c=self.assignMeshCmd )
        else:
            cmds.button( self._editMeshButton, e=1, l='Edit Mesh', c= self.editMeshCmd )


    def scrollSelectObjectCmd(self, scrollUi, *args ):
        
        selObjs = cmds.textScrollList( scrollUi, q=1, si=1 )

        cmds.select( selObjs )
        


    def editMeshCmd(self, *args ):
        
        minValue = cmds.floatField( self._minValueField, q=1, v=1 )
        meshList = cmds.textScrollList( self._meshList, q=1, si=1 )
                
        if not meshList:
            cmds.error( 'Select Mesh Item in Mesh List.')
        
        inst = emCmd.Main( minValue, *meshList )
        inst.changeEditMeshMode()
        
        self.updateEditMeshMode()

                
                
    def assignMeshCmd( self, *args ):

        minValue = cmds.floatField( self._minValueField, q=1, v=1 )
        
        for target in self._assignMeshTargets:
            editingMesh = cmds.listConnections( target+'.editMeshTarget', s=1, d=0 )[0]
            
            amCmd.Main( editingMesh, self._movedDrivers, minValue )
            
        self.updateEditMeshMode()
                
    
    def meshListSelectCmd( self, *args ):
        
        selItems = cmds.textScrollList( self._meshList, q=1, si=1 )
        
        cmds.select( selItems )
        
        
    def selectionChangedCmd(self, *args ):
        
        sels = cmds.ls( sl=1 )
        
        items = cmds.textScrollList( self._meshList, q=1, ai=1 )
                
        selItems = []
        
        for sel in sels:
            if sel in items:
                selItems.append( sel )
        
        cmds.textScrollList( self._meshList, e=1, da=1, si=selItems )
            



class Show( Cmd ):

    def __init__(self):

        self._winName = "jointBasePSD_ui"
        self._title   = "Joint Base PSD Tool"
        
        self._width = 600
        self._height = 500

        self.core()

        Cmd.__init__(self)
        
    
    def scriptJob( self ):
        
        cmds.scriptJob( e=['SelectionChanged', self.selectionChangedCmd ], p = self._winName )
        
        
    def driverRootPart( self, width ):
        
        widthList = uifnc.setWidthByPerList( [60,40], width )
        cmds.rowColumnLayout( nc=2, cw=[(1,widthList[0]),(2,widthList[1])] )
        self._driverRootField = cmds.textField()
        self._driverRootButton = cmds.button( l='Load', c = partial( self.loadCmd, self._driverRootField ), h=25 )
        cmds.setParent( '..' )
        
        
    def editMeshPart( self, width ):
        self._editMeshButton = cmds.button( l='Edit Mesh', c = self.editMeshCmd )
        
        
    def driverListPart(self, width, height ):
        
        cmds.rowColumnLayout( nc=1, cw=[(1,width)] )
        cmds.text( l='Driver List', al='center' )
        uifnc.setSpace( 10 )
        
        widthList = uifnc.setWidthByPerList( [1,60,30,1], width )
        cmds.rowColumnLayout( nc=4, cw=[(1,widthList[0]),(2,widthList[1]),(3,widthList[2]),(4,widthList[3])] )
        uifnc.setSpace()
        self._movedDriverCheck = cmds.checkBox( l='Show Only Moved Driver', cc = partial( self.refreshDriverCmd, width*.95 ) )
        cmds.button( l='Refresh', c= partial( self.refreshDriverCmd, width*.95 ) )
        uifnc.setSpace()
        cmds.setParent( '..' )
        
        self._driverListLay = cmds.scrollLayout( height = height-45 )
        cmds.setParent( '..' )
        
        
        widthList = uifnc.setWidthByPerList( [1,80,20,1], width )
        cmds.rowColumnLayout( nc=4, cw=[(1,widthList[0]),(2,widthList[1]),(3,widthList[2]),(4,widthList[3])] )
        uifnc.setSpace()
        cmds.text( l='Min Value :    ', al='right' )
        self._minValueField = cmds.floatField( v=0.01, pre=2 )
        uifnc.setSpace()
        cmds.setParent('..')
        
        cmds.setParent( '..' )


    def meshListPart(self, width, height ):
        
        cmds.rowColumnLayout( nc=1, cw=[(1, width)] )
        cmds.text( l='Mesh List', al='center' )
        uifnc.setSpace( 10 )
        self._meshList = cmds.textScrollList( height = height, ams=1, sc= self.meshListSelectCmd )
        cmds.setParent( '..' )
        
        
    def affectedShapeListPart( self, width, height ):
        
        cmds.rowColumnLayout( nc=1, cw=(1,width ) )
        affectMeshInfo = cmds.textScrollList(  )
        


    def setSpace(self, numOfColumn, h=10 ):
        
        for i in range( numOfColumn ):
            uifnc.setSpace( h )


    def core(self):
        
        if cmds.window( self._winName, ex=1 ):
            cmds.deleteUI( self._winName )

        cmds.window( self._winName, title= self._title )
        
        cmds.columnLayout()
        
        uifnc.setSpace( 10 )
        
        widthList = uifnc.setWidthByPerList( [3,60,30,3], self._width )
        cmds.rowColumnLayout( nc=4, cw=[ (1,widthList[0]), (2,widthList[1]),(3,widthList[2]), (4,widthList[3]) ] )
        
        uifnc.setSpace()
        self.driverRootPart( widthList[1] )
        self.editMeshPart( widthList[1] )
        uifnc.setSpace()
        
        self.setSpace( 4, 15 )
        
        uifnc.setSpace()
        self.driverListPart( widthList[1], 150 )
        self.meshListPart( widthList[2], 150 )
        uifnc.setSpace()
        
        cmds.setParent( '..' )
        
        cmds.window( self._winName, e=1, wh=[ self._width, self._height ] )
        cmds.showWindow( self._winName )
        
        self.scriptJob()