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
        
        cia = cmds.radioCollection( self._nameCollection, q=1, cia=1 )
        sel = cmds.radioCollection( self._nameCollection, q=1, sl=1 )
        
        for i in range( 2 ):
            if cia[i].split( '|' )[-1] == sel:
                if i == 0:
                    mainInfo.namespaceOption = 'prefix'
                else:
                    mainInfo.namespaceOption = 'namespace'
        
        if cmds.optionMenu( self._frontNameOptionMenu, q=1, sl=1 ) == 1:
            mainInfo.frontNameOption = 'fileName'
            cmds.textField( self._thisStringField, e=1, en=0 )
        else:
            mainInfo.frontNameOption = 'thisString'
            cmds.textField( self._thisStringField, e=1, en=1 )
            
        mainInfo.thisString = cmds.textField( self._thisStringField, q=1, tx=1 )
        
        fileString = mainInfo.fileTypeOption + '\n' + mainInfo.namespaceOption +'\n' + mainInfo.frontNameOption + '\n' + mainInfo.thisString
        f = open( mainInfo.uiInfoPath, 'w' )
        f.write( fileString )
        f.close()
        
        self._fileTypeOption   = mainInfo.fileTypeOption
        self._namespaceOption  = mainInfo.namespaceOption
        self._frontNameOption  = mainInfo.frontNameOption
        self._thisString       = mainInfo.thisString

    
    def setUiInfo( self, *args ):
    
        self._fileTypeOption   = mainInfo.fileTypeOption
        self._namespaceOption  = mainInfo.namespaceOption
        self._frontNameOption  = mainInfo.frontNameOption
        self._thisString       = mainInfo.thisString
        
        cia = cmds.radioCollection( self._fileTypeCollection, q=1, cia=1 )
        
        if self._fileTypeOption == 'motion':
            cmds.radioCollection( self._fileTypeCollection, e=1, sl=cia[0].split('|')[-1] )
        elif self._fileTypeOption == 'hik':
            cmds.radioCollection( self._fileTypeCollection, e=1, sl=cia[1].split('|')[-1] )
        else:
            cmds.radioCollection( self._fileTypeCollection, e=1, sl=cia[2].split('|')[-1] )
        
        cia = cmds.radioCollection( self._nameCollection, q=1, cia=1 )
        
        if self._namespaceOption == 'prefix':
            cmds.radioCollection( self._nameCollection, e=1, sl=cia[0].split('|')[-1] )
        else:
            cmds.radioCollection( self._nameCollection, e=1, sl=cia[1].split('|')[-1] )
            
        if self._frontNameOption == 'fileName':
            cmds.optionMenu( self._frontNameOptionMenu, e=1, sl=1 )
            cmds.textField( self._thisStringField, e=1, en=0 )
        else:
            cmds.optionMenu( self._frontNameOptionMenu, e=1, sl=2 )
            cmds.textField( self._thisStringField, e=1, en=1 )



    def searchNameChangeCmd( self, *args ):
        
        searchName = cmds.textField( self._searchField, q=1, tx=1 )
        
        cia = cmds.radioCollection( self._fileTypeCollection, q=1, cia=1 )
        sel = cmds.radioCollection( self._fileTypeCollection, q=1, sl=1 )
        
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
    
    
    
    def namespaceChangeCmd( self, *args ):
        
        self.editUiInfo()
        
        
        
    def frontNameChangeCmd(self, *args ):

        self.editUiInfo()
        
    
    
    def thisStringCmd(self, *args ):
        
        self.editUiInfo()
        
        
    
    def loadToSceneCmd(self, option='import', *args ):
    
        indies = cmds.textScrollList( self._fileNameScrollList, q=1, sii=1 )
        self._thisString = cmds.textField( self._thisStringField, q=1, tx=1 )
        
        loadOption = { 'type':'mayaBinary', 'mnc':True, 'options':'v=0', 'pr':True, 'lrd':'all' }
        
        if option == 'import':
            loadOption.update( {'i':True, 'ra':True } )
        else:
            loadOption.update( {'r':True} )
            
        
        for index in indies:
            
            filePath = self._realFileNames[ index-1 ]
            
            folderPath, fileName = os.path.split( filePath )
            
            fileName, ext = fileName.split( '.' )
            
            if self._namespaceOption == 'prefix':
                if self._frontNameOption == 'fileName':
                    loadOption.update( {'rpr': fileName } )
                else:
                    loadOption.update( {'rpr': self._thisString } )
            else:
                if self._frontNameOption == 'fileName':
                    loadOption.update( {'namespace': fileName } )
                else:
                    loadOption.update( {'namespace': self._thisString } )
            
            cmds.file( filePath, **loadOption )
            
    

    
class Show( Cmd ):
    
    def __init__(self):
        
        self._sideWidth = 7
        self._width = mainInfo.width - self._sideWidth*2 - 2
        
        self.core()
        
        Cmd.__init__(self)
        
        self.setUiInfo()
        
        
    def core(self):
        
        if cmds.window( mainInfo.winName, ex=1 ):
            cmds.deleteUI( mainInfo.winName, wnd=1 )
        cmds.window( mainInfo.winName, title = mainInfo.title, menuBar=True )
        
        addMenu.Add()
        
        cmds.columnLayout()
        
        mainInfo.setSpaceH( 10 )
        
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
        
        mainInfo.setSpaceH( 10 )
        
        addSpaceWidth = 20
        editWidt = self._width-addSpaceWidth
        halfWidth = editWidt/2
        lastWidth   = editWidt - halfWidth
        cmds.rowColumnLayout( nc=4, cw=[(1,addSpaceWidth+self._sideWidth),
                                        (2,halfWidth),
                                        (3,lastWidth),
                                        (4,self._sideWidth)] )
        self._nameCollection = cmds.radioCollection()
        mainInfo.setSpace()
        cmds.radioButton( l='Prefix', cc=self.namespaceChangeCmd )
        cmds.radioButton( l='Namespace' )
        mainInfo.setSpace()
        cmds.setParent( '..' )
        
        mainInfo.setSpaceH( 5 )
        
        buttonWidth = self._width/2
        lastWidth   = self._width - buttonWidth
        
        cmds.rowColumnLayout( nc=4, cw=[(1,self._sideWidth),
                                        (2,buttonWidth),
                                        (3,lastWidth),
                                        (4,self._sideWidth)] )
        mainInfo.setSpace()
        self._frontNameOptionMenu = cmds.optionMenu( cc=self.frontNameChangeCmd )
        cmds.menuItem( l='the file name' )
        cmds.menuItem( l='this string')
        self._thisStringField = cmds.textField( en=0 )
        mainInfo.setSpace()
        cmds.setParent( '..' )
        
        mainInfo.setSpaceH( 10 )
        
        buttonWidth = self._width/2
        lastWidth   = self._width - buttonWidth
        
        cmds.rowColumnLayout( nc=4, cw=[(1,self._sideWidth),
                                        (2,buttonWidth),
                                        (3,lastWidth),
                                        (4,self._sideWidth)] )
        mainInfo.setSpace()
        cmds.button( l='Import File', h=30, c = partial( self.loadToSceneCmd, 'import' ) )
        cmds.button( l='Reference File', h=30, c = partial( self.loadToSceneCmd, 'reference' ) )
        mainInfo.setSpace()
        cmds.setParent( '..' )
        
        cmds.window( mainInfo.winName, e=1, w=mainInfo.width, h=mainInfo.height )
        cmds.showWindow( mainInfo.winName )