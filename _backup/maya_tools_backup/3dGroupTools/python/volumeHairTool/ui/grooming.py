import maya.cmds as cmds
import uiInfo
import volumeHairTool.command.grooming as mainCmd
import functions as fnc
from functools import partial
import os
import maya.mel as mel
import uiModel


class SetName:
    
    def __init__(self, cmdObject, surfs, surfGrp, basePointer, pointer ):
        
        self._winName = "volumeHairTool_setNameRename"
        self._title = "Set Name"
        self._width = 300
        self._height = 50
        
        self._cmdObject = cmdObject
        self._surfs = surfs
        self._surfGrp = surfGrp
        self._basePointer = basePointer
        self._pointer = pointer
        
        self.core()
        
    
    def core(self):
        
        if cmds.window( self._winName, ex=1 ):
            cmds.deleteUI( self._winName, wnd=1 )
        cmds.window( self._winName, title=self._title )
        
        cmds.columnLayout()
        
        cmds.rowColumnLayout( nc=2, cw=[(1,150),(2,150)])
        cmds.text( l='Set Name : ' )
        self._setName = cmds.textField()
        cmds.setParent( '..' )
        
        uiInfo.setSpace( 5 )
        
        cmds.rowColumnLayout( nc=2, cw=[(1,100),(2,150)])
        uiInfo.setSpace()
        self._eachSurface = cmds.checkBox( l='Set by Each Surface' )
        cmds.setParent( '..' )
        
        uiInfo.setSpace( 5 )
        
        cmds.rowColumnLayout( nc=3, cw=[(1,10),(2,self._width-20), (3,10)])
        uiInfo.setSpace()
        cmds.button( l= 'SET', c=self.setCmd, h=25 )
        uiInfo.setSpace()
        cmds.setParent( '..' )
        
        uiInfo.setSpace( 5 )

        cmds.window( self._winName, e=1, w=self._width, h=self._height )
        cmds.showWindow( self._winName )

    
    def setCmd(self, *args):
        
        setName = cmds.textField( self._setName, q=1, tx=1 )
        eachSurface = cmds.checkBox( self._eachSurface, q=1, v=1 )
        self._cmdObject( self._surfs, self._surfGrp, setName, 'set', eachSurface )
        cmds.deleteUI( self._winName )
        self.updateSet()
        
        
    def updateSet(self ):
        
        surfGrp = cmds.textField( self._basePointer._surfaceGroup, q=1, tx=1 )
        
        if not surfGrp: return None

        if cmds.attributeQuery( 'sets', node=surfGrp, ex=1 ):
            sets = cmds.listConnections( surfGrp+'.sets' )
        else:
            return None
        
        cmds.textScrollList( self._pointer._set, e=1, removeAll=1 )
        cmds.textScrollList( self._pointer._guideSet, e=1, removeAll=1 )
        
        if sets:
            for setElement in sets:
                if cmds.listConnections( setElement, type='pgYetiMaya' ):
                    cmds.textScrollList( self._pointer._guideSet, e=1, append = setElement )
                else:
                    cmds.textScrollList( self._pointer._set, e=1, append = setElement )



class Cmd:
    
    def __init__(self):
        
        self._defaultFilePath = self.openText()
        self._defaultFileBrowser = '/'.join( self._defaultFilePath.split('/')[:-1] )
    
    
    def saveData(self ):
        
        app_dir = mel.eval( 'getenv( "MAYA_APP_DIR" )' )+"/LocusCommPackagePrefs"

        path = app_dir+"/HSBVC_prefs/GROOMING.txt"
        
        filePath = cmds.textField( self._filePath, q=1, tx=1 )
        
        fileTextSpace = open( path, 'w' )
        fileTextSpace.write( filePath )
        fileTextSpace.close()
        
    
    def openText(self):
        
        app_dir = mel.eval( 'getenv( "MAYA_APP_DIR" )' )+"/LocusCommPackagePrefs"

        path = app_dir+"/HSBVC_prefs/GROOMING.txt"
        
        if not os.path.exists( path ):
            return ''
        
        fileTextSpace = open( path, 'r' )
        text = fileTextSpace.read()
        fileTextSpace.close()
        
        return text
    
    
    def createYetiCmd(self, basePointer, *args ):
        
        baseMesh = cmds.textField( basePointer._baseMesh, q=1, tx=1 )
        surfGrp = cmds.textField( basePointer._surfaceGroup, q=1, tx=1 )
        
        mainCmd.SetYeti( baseMesh, surfGrp, [] )
        
        
    def selectOnSetCmd( self, *args ):
        
        cmds.textScrollList( self._guideSet, e=1, da=1 )
        
        
    def selectOnGuideSetCmd( self, *args ):
        
        cmds.textScrollList( self._set, e=1, da=1 )
        
    
    def moveToRCmd(self, basePointer, *args ):
        
        baseMesh = cmds.textField( basePointer._baseMesh, q=1, tx=1 )
        surfGrp = cmds.textField( basePointer._surfaceGroup, q=1, tx=1 )
        selItems = cmds.textScrollList( self._set, q=1, si=1 )
        currentItems = cmds.textScrollList( self._guideSet, q=1, ai=1 )
        
        if not selItems:
            return None
        
        if not currentItems: currentItems = []
        
        currentItems += selItems
        
        print currentItems
        
        mainCmd.SetYeti( baseMesh, surfGrp, currentItems )
        
        self.updateSet()
        
    
    def moveToLCmd(self, basePointer, *args ):
        
        baseMesh = cmds.textField( basePointer._baseMesh, q=1, tx=1 )
        surfGrp = cmds.textField( basePointer._surfaceGroup, q=1, tx=1 )
        selItems = cmds.textScrollList( self._guideSet, q=1, si=1 )
        currentItems = cmds.textScrollList( self._guideSet, q=1, ai=1 )
        
        if not selItems:
            return None
        
        for selItem in selItems:
            if selItem in currentItems:
                currentItems.remove( selItem )
        
        mainCmd.SetYeti( baseMesh, surfGrp, currentItems )
        
        self.updateSet()
    
        
    
    def addCmd(self, winPointer, basePointer, *args ):
        
        sels = cmds.ls( sl=1 )
        
        surfGrp = cmds.textField( basePointer._surfaceGroup, q=1, tx=1 )
        surfs = winPointer.getSurfaceShapes( basePointer )
        
        crvs = fnc.getCurveShapes( sels )
        if crvs:
            surfs += crvs
        
        SetName(mainCmd.SetCurve,surfs,surfGrp, basePointer, self )
        
        if sels:
            cmds.select( sels )
            
            
    def resetCmd(self, winPointer, basePointer, *args ):
        
        sels = cmds.ls( sl=1 )
        
        surfGrp = cmds.textField( basePointer._surfaceGroup, q=1, tx=1 )
        surfs = winPointer.getSurfaceShapes( basePointer )
        
        selItems_inSet = cmds.textScrollList( self._set, q=1, si=1 )
        selItems_inGuide = cmds.textScrollList( self._guideSet, q=1, si=1 )
        
        selItems = []
        if selItems_inSet: selItems += selItems_inSet
        if selItems_inGuide: selItems += selItems_inGuide
        
        mainCmd.SetCurve( surfs, surfGrp, selItems[0], 'reset' )
        
        if sels:
            cmds.select( sels )
            
            
    def removeCmd(self, *args ):
        
        selItems_inSet = cmds.textScrollList( self._set, q=1, si=1 )
        selItems_inGuide = cmds.textScrollList( self._guideSet, q=1, si=1 )
        
        if selItems_inSet:
            for selItem in selItems_inSet:
                cmds.textScrollList( self._set, e=1, ri=selItem )
            cmds.delete( selItems_inSet )
        if selItems_inGuide:
            for selItem in selItems_inGuide:
                cmds.textScrollList( self._guideSet, e=1, ri=selItem )
            cmds.delete( selItems_inGuide )
            
    
    def loadFilePathCmd(self, *args ):
        
        loadedText = cmds.fileDialog2( fm= 1, dir= self._defaultFileBrowser, ff= "Filtered Files (*.grm)")
    
        if loadedText:
            cmds.textField( self._filePath, e=1, tx= loadedText[0] )
            self._defaultFileBrowser = '/'.join( loadedText[0].split( '/' )[:-1] )
            self.saveData()
        
        
    def importGroomCmd(self, basePointer, *args ):
        
        baseMesh = cmds.textField( basePointer._baseMesh, q=1, tx=1 )
        
        yetiCons = cmds.listConnections( baseMesh+'.worldMesh[0]', type='pgYetiMaya' )
        if not yetiCons : cmds.error( "Yeti node was not found" )
        
        path = cmds.textField( self._filePath, q=1, tx=1 )

        if os.path.isfile( path ):
            mainCmd.ImportGroom( cmds.listRelatives( yetiCons[0], s=1 )[0], path )


    def openGraphEditorCmd(self, basePointer, *args ):
        
        baseMesh = cmds.textField( basePointer._baseMesh, q=1, tx=1 )
        
        mainCmd.OpenEditor( baseMesh )
        
    
    def updateSet(self ):
        
        surfGrp = cmds.textField( self._basePointer._surfaceGroup, q=1, tx=1 )
        
        if not surfGrp: return None

        if cmds.attributeQuery( 'sets', node=surfGrp, ex=1 ):
            sets = cmds.listConnections( surfGrp+'.sets' )
        else:
            return None
        
        cmds.textScrollList( self._set, e=1, removeAll=1 )
        cmds.textScrollList( self._guideSet, e=1, removeAll=1 )
        
        if sets:
            for setElement in sets:
                if cmds.listConnections( setElement, type='pgYetiMaya' ):
                    cmds.textScrollList( self._guideSet, e=1, append = setElement )
                else:
                    cmds.textScrollList( self._set, e=1, append = setElement )
        


class Add( Cmd ):
    
    def __init__(self, winPointer, basePointer ):
        
        Cmd.__init__(self)
        
        self._uiName = "volumeHairTool_grooming"
        self._label = "  Grooming"
        self._width = winPointer._width-4
        
        self._winPointer = winPointer
        self._basePointer = basePointer
        
        self.core()


    def core(self):
        
        uiInfo.addFrameLayout( self._uiName, self._label )
        
        uiInfo.setSpace( 4 )
        
        cmds.rowColumnLayout( nc=3, cw=[(1,10),(2,self._width-20),(3,10)])
        uiInfo.setSpace()
        cmds.button( "Create Yeti", h=25, c=partial( self.createYetiCmd, self._basePointer) )
        uiInfo.setSpace()
        cmds.setParent( '..' )
        
        uiInfo.separator( self._width, 1 )
        
        textScrollArea = (self._width-20) / 2
        textScrollArea2 =  self._width-20-textScrollArea
        
        cmds.rowColumnLayout( nc=4, cw=[(1,10), (2,textScrollArea),(3,textScrollArea2),(4,10)] )
        uiInfo.setSpace()
        cmds.text( l='Set', h=25 )
        cmds.text( l='Guide Set', h=25 )
        uiInfo.setSpace()
        uiInfo.setSpace()
        self._set = cmds.textScrollList(  h=100, ams=1,  sc = partial( self.selectOnSetCmd) )
        self._guideSet = cmds.textScrollList(  h=100, ams=1,  sc = partial( self.selectOnGuideSetCmd) )
        uiInfo.setSpace()
        uiInfo.setSpace()
        cmds.button( l='Move to >>', c=partial( self.moveToRCmd, self._basePointer) )
        cmds.button( l='<< Move to', c=partial( self.moveToLCmd, self._basePointer) )
        uiInfo.setSpace()
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=3, cw=[(1,10),(2,self._width-20),(3,10)])
        uiInfo.setSpace()
        cmds.button( l='Add', h=25, c=partial( self.addCmd, self._winPointer, self._basePointer) )
        uiInfo.setSpace()
        uiInfo.setSpace()
        cmds.button( l='Reset', h=25, c=partial( self.resetCmd, self._winPointer, self._basePointer) )
        uiInfo.setSpace()
        uiInfo.setSpace()
        cmds.button( l='Remove', h=25, c=partial( self.removeCmd) )
        uiInfo.setSpace()
        cmds.setParent( '..' )
        
        uiInfo.separator( self._width )
        
        iconArea = 25
        fieldArea = ( self._width ) * .5
        textArea = self._width - fieldArea - iconArea -10
        
        cmds.rowColumnLayout( nc=3, cw=[(1,textArea),(2,fieldArea),(3,iconArea)] )
        cmds.text( l='Groom File Name : ' )
        self._filePath = cmds.textField( h=22, tx=self._defaultFilePath )
        cmds.iconTextButton( image=uiModel.iconPath+"/folder.png",
                             c=partial( self.loadFilePathCmd) )
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=3, cw=[(1,10),(2,self._width-20),(3,10)])
        uiInfo.setSpace()
        cmds.button( "Import Groom", h=25, c=partial( self.importGroomCmd, self._basePointer) )
        uiInfo.setSpace()
        uiInfo.setSpace()
        cmds.button( "Open Graph Editor", h=25, c= partial( self.openGraphEditorCmd, self._basePointer ) )
        uiInfo.setSpace()
        cmds.setParent( '..' )
        
        
        uiInfo.setSpace( 10 )
        
        uiInfo.getOutFrameLayout()
        
        
    def clear(self):
        
        cmds.textField( self._filePath, e=1, tx='' )
        self.saveData()
        
        cmds.textScrollList( self._set, e=1, ra=1 )
        cmds.textScrollList( self._guideSet, e=1, ra=1 )