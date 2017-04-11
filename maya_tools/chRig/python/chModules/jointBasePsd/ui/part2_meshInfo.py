import maya.cmds as cmds
import uifunctions as uifnc
import globalInfo

import chModules.jointBasePsd.baseCommand as bcCmd

import math
from functools import partial


class Cmd:
    
    def __init__(self ):
        
        globalInfo.meshInfoInst = self
        

    def updateCmd( self, *args ):
        
        rootName = globalInfo.rootDriver

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
        

    def scrollSelectObjectCmd(self, *args ):
        
        selObjs = cmds.textScrollList( self._meshList, q=1, si=1 )
        selObjs2 = cmds.textScrollList( self._selMeshList, q=1, si=1 )
        cmds.select( selObjs, selObjs2 )
        
        
    def selectionChangedCmd( self, *args ):
        
        cmds.textScrollList( self._meshList, e=1, da=1 )
        cmds.textScrollList( self._selMeshList, e=1, da=1 )
        sels = cmds.ls( sl=1 )
        
        if not sels: return None
        
        meshItems = cmds.textScrollList( self._meshList, q=1, ai=1 )
        selMeshItems = cmds.textScrollList( self._selMeshList, q=1, ai=1 )
        
        if not meshItems: meshItems = []
        if not selMeshItems: selMeshItems = []
        
        meshItemTargets = []
        selMeshItemTargets = []
        for sel in sels:
            if sel in meshItems:
                meshItemTargets.append( sel )
            if sel in selMeshItems:
                selMeshItemTargets.append( sel )
        
        if not meshItemTargets: return None
        cmds.textScrollList( self._meshList, e=1, si=meshItemTargets )
        if not selMeshItemTargets : return None
        cmds.textScrollList( self._selMeshList, e=1, si=selMeshItemTargets )
        
        
    def makePsdMeshCmd(self, *args ):
        
        sels = cmds.ls( sl=1 )
        
        for sel in sels:
            try: bcCmd.blendAndFix_toSkin( sel )
            except: pass
        
        
    def addSelectedCmd( self, *args ):
        
        selItems = cmds.textScrollList( self._meshList, q=1, si=1 )
        if not selItems: return None
        
        existItems = cmds.textScrollList( self._selMeshList, q=1, ai=1 )
        
        addItems = []
        
        if existItems:
            for item in selItems:
                if item in existItems:
                    addItems.append( item )
        else:
            addItems = selItems
        
        if not addItems: return None
        
        cmds.textScrollList( self._selMeshList, e=1, ra=1, a=addItems )
        
        globalInfo.editMeshInst.updateCmd()
    

    def removeAllCmd( self, *args ):
    
        selItems = cmds.textScrollList( self._selMeshList, q=1, si=1 )
        
        if selItems:
            cmds.textScrollList( self._selMeshList, e=1, ri=selItems )



class Add( Cmd ):
    
    def __init__(self, width ):
        
        self._emptyWidth = 10
        self._width = width - self._emptyWidth*2 - 4
        self._height = 140
        
        sepList = [ 65, 50 ]
        self._mainWidthList = uifnc.setWidthByPerList( sepList, self._width )
        
        Cmd.__init__( self ) 
        self._rowColumns = []
        mainLayout = self.core()
        self.scriptJob( mainLayout )
        
        
    def scriptJob( self, parentUi ):
        
        cmds.scriptJob( e=['SelectionChanged', self.selectionChangedCmd ], p = parentUi )


    def core(self):
        
        mainLayout = cmds.rowColumnLayout( nc= 3, cw=[(1,self._emptyWidth),
                                         (2,self._width),
                                         (3,self._emptyWidth)])
        
        uifnc.setSpace()
        cmds.button( l='Set Selected Mesh To PSD Mesh', h=30, c= self.makePsdMeshCmd )
        uifnc.setSpace()
        
        uifnc.setSpace()
        uifnc.setSpace(10)
        uifnc.setSpace()
        
        uifnc.setSpace()
        cmds.text( l='MESH LIST' )
        uifnc.setSpace()
        
        cmds.setParent( '..' )
        
        uifnc.setSpace( 5 )
        
        column1 = cmds.rowColumnLayout( nc=4, cw=[(1,self._emptyWidth),
                                        (2,self._mainWidthList[0]),
                                        (3,self._mainWidthList[1]),
                                        (4,self._emptyWidth) ] )
        uifnc.setSpace()
        self._meshList = cmds.textScrollList( h=self._height )
        cmds.popupMenu()
        cmds.menuItem( l='Add Selected', c= self.addSelectedCmd )
        cmds.textScrollList( self._meshList, e=1, sc= partial( self.scrollSelectObjectCmd ) )
        self._selMeshList = cmds.textScrollList( h=self._height )
        cmds.popupMenu()
        cmds.menuItem( l='Remove Selected', c= self.removeAllCmd )
        cmds.textScrollList( self._selMeshList, e=1, sc= partial( self.scrollSelectObjectCmd ) )
        uifnc.setSpace()
        
        cmds.setParent( '..' )
        
        self._rowColumns = [mainLayout, column1]
        
        return mainLayout