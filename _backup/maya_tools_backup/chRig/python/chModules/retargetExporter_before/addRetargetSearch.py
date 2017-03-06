import maya.cmds as cmds
import mainInfo
import addMenu
import command
import os

from functools import partial


class Cmd:
    
    def __init__(self):
        
        pass
    
    
    def editUiInfo(self, *args ):
        
        cia = cmds.radioCollection( self._fileTypeCollection, q=1, cia=1 )
        sel = cmds.radioCollection( self._fileTypeCollection, q=1, sl=1 )
        
        for i in range( 3 ):
            if cia[i].split( '|' )[-1] == sel:
                if i == 0:
                    mainInfo.fileTypeOption = 'motion'
                elif i == 1:
                    mainInfo.fileTypeOption = 'hik'
                else:
                    mainInfo.fileTypeOption = 'all'

        
        fileString = mainInfo.fileTypeOption + '\n' + mainInfo.namespaceOption +'\n' + mainInfo.frontNameOption + '\n' + mainInfo.thisString
        f = open( mainInfo.uiInfoPath, 'w' )
        f.write( fileString )
        f.close()
        
        self._fileTypeOption   = mainInfo.fileTypeOption

    
    def setUiInfo( self, *args ):
    
        self._fileTypeOption   = mainInfo.fileTypeOption
        
        cia = cmds.radioCollection( self._fileTypeCollection, q=1, cia=1 )
        
        if self._fileTypeOption == 'motion':
            cmds.radioCollection( self._fileTypeCollection, e=1, sl=cia[0].split('|')[-1] )
        elif self._fileTypeOption == 'hik':
            cmds.radioCollection( self._fileTypeCollection, e=1, sl=cia[1].split('|')[-1] )
        else:
            cmds.radioCollection( self._fileTypeCollection, e=1, sl=cia[2].split('|')[-1] )



    def searchNameChangeCmd( self, *args ):
        
        searchName = cmds.textField( self._searchField, q=1, tx=1 )
        
        cia = cmds.radioCollection( self._fileTypeCollection, q=1, cia=1 )
        sel = cmds.radioCollection( self._fileTypeCollection, q=1, sl =1 )
        
        for i in range( 3 ):
            if cia[i].split( '|' )[-1] == sel:
                if i == 0:
                    extList = ['.motion']
                elif i == 1:
                    extList = ['.hik' ]
                else:
                    extList = ['.motion', '.hik']
        
        fileNames = []
        self._realFileNames = []
        
        for filePath in command.getFiles( extList, searchName ):
            filePath = os.path.abspath( filePath )
            
            folder, fileName = os.path.split( filePath )
            
            lastFolderName = folder.split( '\\' )[-1]
            fileNames.append( "../"+lastFolderName+"/"+fileName )
            self._realFileNames.append( filePath )
            
        cmds.textScrollList( self._fileNameScrollList, e=1, ra=1, a=fileNames )
        
        
    def fileTypeChangeCmd( self, *args ):
        
        self.editUiInfo()

    
    
    
class Add( Cmd ):
    
    def __init__( self ):
        
        self.core()
        
        Cmd.__init__(self)
        


    def core( self ):
        
        buttonWidth = 50
        fieldWidth = self._width - buttonWidth
        cmds.rowColumnLayout( nc=4, cw=[(1,self._sideWidth),
                                        (2,fieldWidth),
                                        (3,buttonWidth),
                                        (4,self._sideWidth)] )
        mainInfo.setSpace()
        self._searchField = cmds.textField( cc=self.searchNameChangeCmd )
        cmds.button( l='search', c=self.searchNameChangeCmd )
        mainInfo.setSpace()
        cmds.setParent( '..' )
        
        mainInfo.setSpaceH(10)
        
        addSideWidth = 20
        resizeWidth = self._width - addSideWidth*2
        firstWidth  = resizeWidth*0.37
        secondWidth = resizeWidth*0.42
        thirdWidth  = resizeWidth - firstWidth - secondWidth
        cmds.rowColumnLayout( nc=5, cw=[(1,self._sideWidth+addSideWidth),
                                        (2,firstWidth),
                                        (3,secondWidth),
                                        (4,thirdWidth),
                                        (5,self._sideWidth+addSideWidth)] )
        self._fileTypeCollection = cmds.radioCollection()
        mainInfo.setSpace()
        cmds.radioButton( l='Motion File', cc=self.fileTypeChangeCmd )
        cmds.radioButton( l='Human IK File', cc=self.fileTypeChangeCmd )
        cmds.radioButton( l='All', sl=1 )
        mainInfo.setSpace()
        cmds.setParent( '..' )
        
        mainInfo.setSpaceH( 10 )
        
        cmds.rowColumnLayout( nc=3, cw=[(1,self._sideWidth),
                                        (2,self._width),
                                        (3,self._sideWidth) ] )
        mainInfo.setSpace()
        self._fileNameScrollList = cmds.textScrollList( ams=1 )
        mainInfo.setSpace()
        cmds.setParent( '..' )