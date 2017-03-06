import maya.cmds as cmds
from functools import partial
import uiInfo
import volumeHairTool.command.rebuild as mainCmd
import functions as fnc
import maya.mel as mel
import os

class Cmd:
    
    def __init__(self):
        
        pass
    
    
    def saveData(self ):
        
        app_dir = mel.eval( 'getenv( "MAYA_APP_DIR" )' )+"/LocusCommPackagePrefs"

        path = app_dir+"/HSBVC_prefs/HSBVC_BASE.txt"
        
        meshName = cmds.textField( self._baseMesh, q=1, tx=1 )
        surfaceGrpName = cmds.textField( self._surfaceGroup, q=1, tx=1 )
        
        text = meshName+'\n\r'+surfaceGrpName
        
        fileTextSpace = open( path, 'w' )
        fileTextSpace.write( text )
        fileTextSpace.close()
        
    
    def openData(self):
        
        app_dir = mel.eval( 'getenv( "MAYA_APP_DIR" )' )+"/LocusCommPackagePrefs"

        path = app_dir+"/HSBVC_prefs/HSBVC_BASE.txt"
        
        if not os.path.exists( path ):
            return None
        
        fileTextSpace = open( path, 'r' )
        text = fileTextSpace.read()
        fileTextSpace.close()
        
        try:meshName, surfaceGrpName = text.split( '\n\r' )
        except: return None
        
        cmds.textField( self._baseMesh, e=1, tx=meshName )
        cmds.textField( self._surfaceGroup, e=1, tx=surfaceGrpName )
        
    
    
    def loadBaseMesh(self, *args ):
        
        sels = cmds.ls( sl=1 )
        
        if not sels: cmds.error( "Select mesh" )
        
        selShapes = cmds.listRelatives( sels[-1], s=1 )
        
        if not selShapes: cmds.error( "Select mesh" )
        
        
        meshShape = ''
        
        for shape in selShapes:
            if not cmds.getAttr( shape+'.io' ):
                if cmds.nodeType( shape ) == 'mesh':
                    meshShape = shape
                    break
                
        if not meshShape:
            cmds.error( "Selected Object has no mesh")
        
        cmds.textField( self._baseMesh, e=1, tx=meshShape )
        
        self.saveData()
        
        
    def loadSurfaceGroup(self, *args ):
        
        sels = cmds.ls( sl=1 )
        
        if not sels: cmds.error( "Select Surface Group" )
        
        children = cmds.listRelatives( sels[-1], c=1, ad=1 )
        
        if not children: cmds.error( "Select Surface Group" )
        
        
        surfaceGrp = ''
        
        for child in children:
            shapes = cmds.listRelatives( child, s=1 )
            if not shapes: continue
            for shape in shapes:
                if cmds.nodeType( shape ) == 'nurbsSurface':
                    surfaceGrp = sels[-1]
                    break
            if surfaceGrp: break
                
        if not surfaceGrp:
            cmds.error( "Select Surface Group" )
        
        cmds.textField( self._surfaceGroup, e=1, tx=surfaceGrp )
        
        if not cmds.attributeQuery( 'sets', node=surfaceGrp, ex=1 ):
            fnc.addArrayMessageAttribute( surfaceGrp, 'sets' )
            
        self.saveData()


class Add( Cmd ):
    
    def __init__(self, winPointer ):
        
        self._uiName = "volumeHairTool_baseObj"
        
        self._width = winPointer._width-4
        
        self._font = "boldLabelFont"
        
        self._winPointer = winPointer
        
        self.core()
        
        self.openData()
        
    
    def core(self):
        
        cmds.rowColumnLayout( self._uiName, nc=1, cw=( 1, self._width ) )
        
        firstWidth = 140
        thirdWidth = 60
        secondWidth = self._width - firstWidth - thirdWidth - 10
        
        cmds.rowColumnLayout( nc=3, cw=[(1, firstWidth ), (2, secondWidth ), (3,thirdWidth) ] )
        
        cmds.text( l='Base Mesh   :   ', al='right', fn=self._font)
        self._baseMesh = cmds.textField()
        cmds.button( l='Load', h=25, c=partial( self.loadBaseMesh) )
        cmds.text( l='Surface Group   :   ', al='right', fn=self._font )
        self._surfaceGroup = cmds.textField()
        cmds.button( l='Load', h=25, c=partial( self.loadSurfaceGroup) )
        cmds.setParent( '..' )
        
        cmds.setParent( '..' )
        
        
    def clear(self):
        
        cmds.textField( self._baseMesh, e=1, tx='' )
        cmds.textField( self._surfaceGroup, e=1, tx='' )
        self.saveData()