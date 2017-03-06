import UIs.modelEditorWindow
import os
import maya.OpenMayaUI as apiUI
import maya.OpenMaya as api
import maya.cmds as cmds



def makePath( pathName ):
    splitPaths = pathName.split( '/' )
    
    cuPath = splitPaths[0]
    
    for i in range( 1, len( splitPaths ) ):
        checkPath = cuPath+'/'+splitPaths[i]
        if not os.path.exists( checkPath ):
            os.chdir( cuPath )
            os.mkdir( splitPaths[i] )
        cuPath = checkPath



class CommandBase:
    
    def __init__( self ):
        
        self.modelWindowInst = UIs.modelEditorWindow.Window()
        self.renderPath = ''
        self.minFrame = 1
        self.maxFrame = 24
        self.fileName = 'playBlastImage'
        
        
        

    def playblast( self, camera, folderPath, min, max, width=1280, height=720 ):
        
        makePath( folderPath )
        self.modelWindowInst.setCamera( camera )
        self.modelWindowInst.setWidthHeight( width, height)
        self.modelWindowInst.create()
        
        modelEditor = self.modelWindowInst.editor
        
        view = apiUI.M3dView()
        view.getM3dViewFromModelEditor( modelEditor, view )
        image = api.MImage()
        
        cmds.currentTime( min )
        cmds.refresh()
        
        for i in range( min, max+1 ):
            cmds.currentTime( i )
            fileName = folderPath+'/%s%04d.iff' %( self.fileName, i )
            view.readColorBuffer( image, True )
            image.writeToFile( fileName )