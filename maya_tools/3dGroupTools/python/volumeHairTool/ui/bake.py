import maya.cmds as cmds
import uiInfo
import volumeHairTool.command.bake as mainCmd
from functools import partial
import maya.mel as mel
import os
import uiModel


class progress:
    
    def __init__(self, numSurfaces ):
        
        self._winName = 'volumeHairTool_cuttingProgress'
        
        self._title = 'Cutting Progress'
        
        self._numSurfaces = numSurfaces
        
        self._bgc = [ 0.95, 0.95, 0 ]
        
        self._progCw = [(1,150),(2,200)]
        self._cw = [(1,1),(2,199)]
        
        
    def setNum(self,num ):
        
        self._numSurfaces = num
        
    
    def start(self):
        
        if cmds.window( self._winName, ex=1 ):
            cmds.deleteUI( self._winName )
        
        cmds.window( self._winName, title= self._title )
        
        column = cmds.columnLayout()
        
        cmds.rowColumnLayout( nc=2, cw=self._progCw )
        cmds.text( 'Cut curve and attach : ', al='right' )
        cmds.frameLayout( labelVisible=0 )
        self._cutting = cmds.rowColumnLayout( nc=2, cw=self._cw )
        cmds.text( l='', bgc=self._bgc )
        cmds.setParent( column )

        
        cmds.window( self._winName, e=1, wh=[ 350,50 ], rtf=1 )
        
        cmds.showWindow( self._winName )
        
        
    def end(self):
        
        cmds.deleteUI( self._winName )
        
        
    def setElement(self, target, num ):
        
        value = int( float( num )/self._numSurfaces * 200 )
        invValue = 201-value
        
        cmds.rowColumnLayout( target, e=1, cw=[(1,value),(2,invValue)] )



class Cmd:
    
    def __init__(self):
        
        path, value1, value2, value3 = self.openText()
        
        self._defaultPath = path
        self._fileBrowserPath = '/'.join( self._defaultPath.split( '/' )[:-1] )
        self._value1 = value1
        self._value2 = value2
        self._value3 = value3
        
        
    def saveData(self, *args):
        
        app_dir = mel.eval( 'getenv( "MAYA_APP_DIR" )' )+"/LocusCommPackagePrefs"

        path = app_dir+"/HSBVC_prefs/BAKE.txt"
        
        filePath = cmds.textField( self._filePath, q=1, tx=1 )
        value1, value2, value3 = cmds.floatFieldGrp( self._timeAndSample, q=1, v=1 )
        
        fileTextSpace = open( path, 'w' )
        fileTextSpace.write( '%s|%f|%f|%f' % (filePath,value1,value2,value3) )
        fileTextSpace.close()
        
    
    def openText(self):
        
        app_dir = mel.eval( 'getenv( "MAYA_APP_DIR" )' )+"/LocusCommPackagePrefs"

        path = app_dir+"/HSBVC_prefs/BAKE.txt"
        
        if not os.path.exists( path ):
            return '', 1.0, 10.0, 3.0
        
        fileTextSpace = open( path, 'r' )
        text = fileTextSpace.read()
        fileTextSpace.close()
        
        path, value1, value2, value3 = text.split('|')
        
        return path, float( value1 ), float( value2 ), float( value3 )
    

            
    def loadFilePathCmd(self, *args ):
        
        loadedText = cmds.fileDialog2( fm= 0, dir= self._fileBrowserPath )
    
        if loadedText:
            cmds.textField( self._filePath, e=1, tx= loadedText[0] )
            self._fileBrowserPath = '/'.join( loadedText[0].split( '/' )[:-1] )
            
        self.saveData()
        

    
    def createCacheCmd(self, basePointer, *args ):
        
        path = cmds.textField( self._filePath, q=1, tx=1 )
        path = path.replace( '\\', '/' )
        start, end, sample = cmds.floatFieldGrp( self._timeAndSample, q=1, v=1 )
        
        baseMesh = cmds.textField( basePointer._baseMesh, q=1, tx=1 )
        
        if baseMesh and cmds.objExists( baseMesh ): 
            yetiNodes = cmds.listConnections( baseMesh+'.worldMesh[0]', type='pgYetiMaya' )
            if yetiNodes:
                yetiNode = cmds.listRelatives( yetiNodes[0], s=1 )[0]
                mel.eval( 'pgYetiCommand -writeCache "%s" -range %d %d -samples %d -updateViewport %d "%s";' %( path, start, end, sample, 1, yetiNode ) )
        else:
            mel.eval( 'pgYetiCommand -writeCache "%s" -range %d %d -samples %d -updateViewport %d;' %( path, start, end, sample, 1 ) )
        

        self.saveData()



class Add( Cmd ):
    
    def __init__(self, winPointer, basePointer ):
        
        Cmd.__init__(self)
        
        self._uiName = "volumeHairTool_bake"
        self._label = "  Bake"
        self._width = winPointer._width-4
        
        self._winPointer = winPointer
        self._basePointer = basePointer
        
        self.core()


    def core(self):
        
        uiInfo.addFrameLayout( self._uiName, self._label )
        
        uiInfo.setSpace( 10 )
        
        iconArea = 25
        fieldArea = ( self._width ) * .5
        textArea = self._width - fieldArea - iconArea -10
        
        cmds.rowColumnLayout( nc=3, cw=[(1,textArea),(2,fieldArea),(3,iconArea)] )
        cmds.text( l='Cache File Name : ', al='right' )
        self._filePath = cmds.textField( h=22, tx= self._defaultPath )
        cmds.iconTextButton( image=uiModel.iconPath+"/folder.png",
                             c=partial( self.loadFilePathCmd ) )
        cmds.setParent( '..' )
        
        iconArea = 25
        fieldArea = ( self._width ) * .5
        textArea = self._width - fieldArea - iconArea -10
        eachFieldArea = fieldArea/3-2
        
        cmds.rowColumnLayout( nc=3, cw=[(1,textArea),(2,fieldArea),(3,iconArea)] )
        cmds.text( l='Frame Range / Samples : ', al='right')
        self._timeAndSample = cmds.floatFieldGrp( nf=3, v=[self._value1,self._value2,self._value3,0], cw3 = [eachFieldArea,eachFieldArea,eachFieldArea], cc=self.saveData )
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=3, cw=[(1,10),(2,self._width-20),(3,10)])
        uiInfo.setSpace()
        cmds.button( l="Bake", c=partial( self.createCacheCmd, self._basePointer ), h=25 )
        uiInfo.setSpace()
        cmds.setParent( '..' )
        uiInfo.setSpace( 10 )
        cmds.setParent( '..' )
        
        uiInfo.getOutFrameLayout()
        
        
    def clear(self):
        
        cmds.textField( self._filePath, e=1, tx='' )
        cmds.floatFieldGrp( self._timeAndSample, e=1, v=[1,10,3,0] )
        
        self.saveData()