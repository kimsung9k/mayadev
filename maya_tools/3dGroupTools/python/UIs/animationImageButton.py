import maya.cmds as cmds
import os


class UI:
    
    def __init__(self):
        
        self.width = 192
        self.height = 108
        
        
    def cmdSlider(self, *args ):
        
        imageIndex = cmds.intSlider( self.slider, q=1, v=1 )
        imagePath = self.allImages[imageIndex]
        cmds.image( self.imageUi, e=1, image=imagePath )

    
    def create(self, imageFolderPath, formatName = 'iff' ):
        
        minusImages = []
        plusImages = []
        for root, dirs, names in os.walk( imageFolderPath ):
            for name in names:
                if name.find( formatName ) == -1: continue
                if name.find( '-' ) != -1:
                    minusImages.append( root+'/'+name )
                else:
                    plusImages.append( root+'/'+name )
            break
        
        minusImages.reverse()
        
        allImages = []
        allImages += minusImages
        allImages += plusImages
        
        lenImage = len( allImages )
        
        cmds.rowColumnLayout( nc=1, cw=(1,self.width) )

        imageUi    = cmds.image( image = allImages[0], h=self.height )
        slider     = cmds.intSlider( min=0, max=lenImage-1, dc=self.cmdSlider )
        cmds.setParent( '..' )
        
        self.allImages = allImages
        self.imageUi = imageUi
        self.slider = slider
        



class Window:
    
    def __init__(self):
        
        self.winName = 'animationImageButton_window'
        self.title   = 'Animation Image Button Window'
        self.width   = 200
        self.height   = 150
        self.uiInst = UI()
    
    
    def create(self, imageFolderPath ):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title )
        
        cmds.columnLayout()
        columnWidth = self.width - 2
        cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)])
        self.uiInst.create( imageFolderPath )
        cmds.setParent( '..' )
        
        cmds.window( self.winName, e=1,
                     w = self.width, h = self.height )
        cmds.showWindow( self.winName )