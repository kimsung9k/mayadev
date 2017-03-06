import maya.cmds as cmds
import uiInfo
import volumeHairTool.command.rebuild as mainCmd
import volumeHairTool.progress as progress
from functools import partial
import maya.mel as mel
import os


class CanNotSurfaceCheck_UI:
    
    def __init__(self, checkList ):
        
        self._winName = 'canNotSurfaceCheck_ui'
        self._title = "Check Can't not rebuildAble"
        
        self._checkList = checkList
        
        self._width = 300
        self._height = 100
        
        self.core()
        
        
    def core(self):
        
        if cmds.window( self._winName, ex=1 ):
            cmds.deleteUI( self._winName, wnd=1 )
        cmds.window( self._winName, title = self._title )
        
        form = cmds.formLayout()
        self._scrollList = cmds.textScrollList( a=self._checkList, sc=self.selCmd, ams=1 )
        
        cmds.formLayout( form, e=1, attachForm=[( self._scrollList, 'top', 5 ),
                                                ( self._scrollList, 'left', 5 ),
                                                ( self._scrollList, 'right', 5 ),
                                                ( self._scrollList, 'bottom', 5 )] )
        
        cmds.window( self._winName, e=1, w=self._width, h=self._height )
        cmds.showWindow( self._winName )
        
        
    def selCmd(self):
        
        selItems  = cmds.textScrollList( self._scrollList, q=1, si=1 )
        cmds.select( selItems )
        


class Cmd:
    
    def __init__(self):
        
        self._canNotCheckList = []
        self._defaultValue = self.openText()
    
    
    def saveData(self, *args ):
        
        app_dir = mel.eval( 'getenv( "MAYA_APP_DIR" )' )+"/LocusCommPackagePrefs"

        path = app_dir+"/HSBVC_prefs/REBUILD.txt"
        
        value = cmds.floatSliderGrp( self._rebuildRate, q=1, v=1 )
        
        fileTextSpace = open( path, 'w' )
        fileTextSpace.write( str(value) )
        fileTextSpace.close()
        
    
    def openText(self):
        
        app_dir = mel.eval( 'getenv( "MAYA_APP_DIR" )' )+"/LocusCommPackagePrefs"

        path = app_dir+"/HSBVC_prefs/REBUILD.txt"
        
        if not os.path.exists( path ):
            return 1
        
        fileTextSpace = open( path, 'r' )
        text = fileTextSpace.read()
        fileTextSpace.close()
        
        return float( text )
    
    
    def checkCmd( self, winPointer, basePointer,*args ):
        
        sels = cmds.ls( sl=1 )
        
        baseMesh = cmds.textField( basePointer._baseMesh, q=1, tx=1 )
        surfs = winPointer.getSurfaceShapes( basePointer )
        
        progress.start()
        progress.append( 'Check Direction' )
        
        progress.setLength( len( surfs ) )
        
        self._canNotCheckList = []
        for surf in surfs:
            progress.addCount()
            try:
                directionIinst = mainCmd.SetDirection( surf, baseMesh )
                
                if directionIinst._canNotCheck:
                    self._canNotCheckList.append( surf )
            except:
                self._canNotCheckList.append( surf )

        progress.end()
        
        if self._canNotCheckList:
            CanNotSurfaceCheck_UI( self._canNotCheckList )
            cmds.select( self._canNotCheckList )
        else:
            if sels:
                cmds.select( sels )
    
    
    def setCmd(self, winPointer, basePointer, *args ):
        
        sels = cmds.ls( sl=1 )

        surfs = winPointer.getSurfaceShapes( basePointer )
        
        rebuildRate = cmds.floatSliderGrp( self._rebuildRate, q=1, v=1 )
        
        progress.start()
        progress.append( 'Rebuild' )
        
        progress.setLength( len( surfs ) )
        
        rebuildInst = mainCmd.AverageRebuild()
        
        for surf in surfs:
            if not surf in self._canNotCheckList:
                rebuildInst.appendSurfaceInfo( surf )
        
        keepOrigValue = cmds.checkBox( self._keepOriginal, q=1, v=1 )
        
        rebuildInst.doIt( rebuildRate, keepOrigValue )
        
        progress.end()
        
        self.saveData()
        
        if self._canNotCheckList:
            CanNotSurfaceCheck_UI( self._canNotCheckList )
            cmds.select( self._canNotCheckList )
        else:
            if sels:
                cmds.select( sels )
                
                
    def keepOriginalCheck(self, *args ):
        
        value = cmds.checkBox( self._keepOriginal, q=1, v=1 )
        if value:
            cmds.floatSliderGrp( self._rebuildRate, e=1, en=0 )
        else:
            cmds.floatSliderGrp( self._rebuildRate, e=1, en=1 )



class Add( Cmd ):
    
    def __init__(self, winPointer, basePointer ):
        
        Cmd.__init__(self)
        
        self._uiName = "volumeHairTool_checkRebuild"
        self._label = "  Rebuild"
        self._width = winPointer._width-4
        
        self._winPointer = winPointer
        self._basePointer = basePointer
        
        self.core()


    def core(self):
        
        uiInfo.addFrameLayout( self._uiName, self._label )
        
        uiInfo.setSpace( 10 )
        
        cmds.rowColumnLayout( nc=3, cw=[(1,10),(2,self._width-20),(3,10)])
        uiInfo.setSpace()
        cmds.button( l='Check Direction', c=partial( self.checkCmd, self._winPointer, self._basePointer ), h=30 )
        uiInfo.setSpace()
        cmds.setParent( '..' )
        
        uiInfo.setSpace( 10 )
        
        cmds.rowColumnLayout( nc=2, cw=[(1,50)])
        cmds.text( l='' )
        self._keepOriginal = cmds.checkBox( l='Keep Original', cc= self.keepOriginalCheck )
        cmds.setParent( '..' )
        
        uiInfo.floatSliderColumn( self._width )
        cmds.text( l='Rebuild Rate  :  ', al='right' )
        self._rebuildRate = uiInfo.floatSlider( 0.1, 2, 100, self._defaultValue, self.saveData )
        cmds.setParent( '..' )
        
        uiInfo.setSpace( 10 )
        
        cmds.rowColumnLayout( nc=3, cw=[(1,10),(2,self._width-20),(3,10)])
        uiInfo.setSpace()
        uiInfo.setButton( partial( self.setCmd, self._winPointer, self._basePointer ) )
        uiInfo.setSpace()
        cmds.setParent( '..' )
        
        uiInfo.setSpace( 10 )
        
        uiInfo.getOutFrameLayout()
        

    def clear(self):
        
        cmds.floatSliderGrp( self._rebuildRate, e=1, v=1 )
        self.saveData()