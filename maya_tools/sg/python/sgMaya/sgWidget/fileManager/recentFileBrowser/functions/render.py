import maya.cmds as cmds
import shutil


class ScreenCaptureRender:
    
    def __init__( self, imagePath, frame=None ):
        
        self._renderGlobalNode = 'defaultRenderGlobals'
        self._renderPath = ''
        self._lights = []
        self._cam    = 'persp'
        self._width  = 250
        self._height = 250
        self._imageFormat = 32
        
        if frame != None:
            cmds.currentTime( frame )
        
        self.keepRenderGlobalInfo()
        self.setRenderGlobalInfo_fromSnapshot()
        self.render()
        self.setRenderGlobalInfo_fromBase()
        
        if self._renderPath:
            shutil.copy2( self._renderPath, imagePath )

    
    def keepRenderGlobalInfo(self):
        
        self._imageFormat = cmds.getAttr( self._renderGlobalNode+'.imageFormat' )
        self._imagePrefix = cmds.getAttr( self._renderGlobalNode+'.imageFilePrefix' )
        self._baseImageAnimValue = cmds.getAttr( self._renderGlobalNode+'.animation' )
        if not self._imagePrefix: self._imagePrefix = ''
        

        ambientShape = cmds.ambientLight( i=0.0 )
        directShape  = cmds.directionalLight( i=1.5 )
        ambient = cmds.listRelatives( ambientShape, p=1 )[0]
        direct  = cmds.listRelatives( directShape,  p=1 )[0]
        
        self._lights = [ ambient, direct ]
        
        mtx = cmds.getAttr( self._cam + '.wm' )
        cmds.xform( direct, ws=1, matrix=mtx )
        cmds.refresh()


    def setRenderGlobalInfo_fromSnapshot(self):

        cmds.setAttr( self._renderGlobalNode+'.imageFormat', self._imageFormat )
        cmds.setAttr( self._renderGlobalNode+'.animation',   0 )

    def setRenderGlobalInfo_fromBase(self):
        
        cmds.setAttr( self._renderGlobalNode+'.imageFormat',     self._imageFormat )
        cmds.setAttr( self._renderGlobalNode+'.imageFilePrefix', self._imagePrefix, type='string' )
        cmds.setAttr( self._renderGlobalNode+'.animation', self._baseImageAnimValue )
        
        cmds.delete( self._lights )
        

    def render(self):

        self._renderPath = cmds.render( self._cam, 
                                           x= self._width, y= self._height )