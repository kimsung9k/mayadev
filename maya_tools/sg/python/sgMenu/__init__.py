import os
import maya.cmds as cmds
from functools import partial



def makeFolder( pathName ):
    
    pathName = pathName.replace( '\\', '/' )
    splitPaths = pathName.split( '/' )
    
    cuPath = splitPaths[0]
    
    folderExist = True
    for i in range( 1, len( splitPaths ) ):
        checkPath = cuPath+'/'+splitPaths[i]
        if not os.path.exists( checkPath ):
            os.chdir( cuPath )
            os.mkdir( splitPaths[i] )
            folderExist = False
        cuPath = checkPath
        
    if folderExist: return None
        
    return pathName



def makeFile( filePath ):
    if os.path.exists( filePath ): return None
    filePath = filePath.replace( "\\", "/" )
    splits = filePath.split( '/' )
    folder = '/'.join( splits[:-1] )
    makeFolder( folder )
    f = open( filePath, "w" )
    f.close()
    



class SGFileBaseMenu:

    @staticmethod
    def getAnableUIName( name ):
        replaceStringList = "~!@#$%^&()-=+[]{},' "
        for char in replaceStringList:
            name = name.replace( char, '_' )
        return name


    @staticmethod
    def getUINameAndLabel( menuUiName, name ):
        splits = name.split( '.' )
        if not splits[0].isdigit():
            return SGFileBaseMenu.getAnableUIName( menuUiName +'_'+ name ), name
        targetName = splits[1]
        return SGFileBaseMenu.getAnableUIName( menuUiName +'_'+ '_'.join( splits[:2] ) ), targetName


    @staticmethod
    def getUIName( menuUiName, folderName ):
        splits = folderName.split( '.' )
        if not splits[0].isdigit():
            return SGFileBaseMenu.getAnableUIName( menuUiName +'_'+ folderName )
        targetName = '_'.join( splits[:2] )
        return SGFileBaseMenu.getAnableUIName( menuUiName +'_'+ targetName)


    @staticmethod
    def renameTargets( folderName ):

        for root, dirs, names in os.walk( folderName ):
            root = root.replace( '\\', '/' )
            targets = []
            
            imageExtensions = []
            imageNames = []
            images = []
            
            for directory in dirs:
                targets.append( directory )
            
            for name in names:
                extention = name.split( '.' )[-1]
                if extention.lower() in ['py', 'txt', 'mel']:
                    targets.append( name )
                elif extention.lower() in ['png', 'jpg','xmp']:
                    images.append( name )
                    imageExtensions.append( extention )
                    imageNames.append( '.'.join( name.split( '.' )[:-1] ) )
            
            targets.sort()
            targets_afterNames = []
            
            renameIndex = 1
            for i in range( len( targets ) ):
                target = targets[i]
                splits = target.split( '.' )
                indexNameStart = 0
                for j in range( len( splits ) ):
                    if splits[j].isdigit():
                        indexNameStart = j+1
                    else:
                        break
                
                #print "indexNameStart :", indexNameStart, target
                if '.'.join( splits[ indexNameStart: ] )[:2] == 'RP':
                    targets_afterNames.append( root+'/%02d.' % renameIndex +'.'.join( splits[ indexNameStart: ] ) )
                else:
                    if target.split( '.' )[-1] in ['py', 'txt', 'mel']:
                        noExtensionTarget = '.'.join( target.split('.')[:-1] )
                    else:
                        noExtensionTarget = target
                    
                    imageExistsIndex = -1
                    if noExtensionTarget in imageNames:
                        imageExistsIndex = imageNames.index( noExtensionTarget )
                    
                    try:
                        os.rename( root+'/'+target, root+'/%02d.' % renameIndex +'.'.join( splits[ indexNameStart: ] ) )
                        targets_afterNames.append( root+'/%02d.' % renameIndex +'.'.join( splits[ indexNameStart: ] ) )
                    except:
                        pass
                    
                    if imageExistsIndex != -1:
                        imageSplits = imageNames[ imageExistsIndex ].split( '.' )
                        os.rename( root+'/'+images[imageExistsIndex], root+'/%02d.' % renameIndex + '.'.join( imageSplits[indexNameStart:] ) + '.' + imageExtensions[ imageExistsIndex ] )
                    
                renameIndex += 1
                
            for target in targets_afterNames:
                SGFileBaseMenu.renameTargets( target )
    

    @staticmethod
    def assignCommand( menuUiName, targetPath ):
    
        for root, dirs, names in os.walk( targetPath ):
            root = root.replace( '\\', '/' )
            targets = []
            
            for directory in dirs:
                targets.append( [directory, 'isDir'] )
            
            for name in names:
                extention = name.split( '.' )[-1]
                if not extention.lower() in ['py', 'txt', 'mel']: continue
                f = open( root + '/' + name, 'r' )
                data = f.read()
                f.close() 
                
                if extention in ['mel','melScript']:
                    targets.append( [name, "import maya.mel\nmaya.mel.eval('source \"%s\"')" % (root + '/' + name) ] )
                else:
                    if data.find( '%' ) != -1:
                        targets.append( [name, 'execfile( "%s" )' % (root + '/' + name) ] )
                    else:
                        targets.append( [name, data ] )
            targets.sort()
            
            for i in range( len( targets ) ):
                target, command = targets[i]
                elsePath = root.replace( targetPath, '' )[1:]
                if not elsePath:
                    parentUIName = menuUiName
                else:
                    parentUIName = SGFileBaseMenu.getUIName( menuUiName, root.split( '/' )[-1] )
                
                targetUIName, label = SGFileBaseMenu.getUINameAndLabel( menuUiName, target )
                
                targetSplits = target.split( '.' )
                if targetSplits[0].isdigit():
                    targetOnlyName = targetSplits[1]
                else:
                    targetOnlyName = targetSplits[0]
                
                targetMenuItem = ''
                if targetOnlyName[0] == '@':
                    if targetOnlyName == '@radioCollection':
                        cmds.radioMenuItemCollection( targetUIName, p = parentUIName )
                    else:
                        firstLine = command.split( '\n' )[0]
                        uiName = firstLine.split( "'" )[-2]
                        targetMenuItem = cmds.menuItem( uiName, l=label[1:], c=command, radioButton=False, p = parentUIName )
                        
                elif targetOnlyName[0] == '#':
                    dividerLabel = targetOnlyName[1:].replace( '-', '' )
                    if dividerLabel:
                        if i == 0:
                            cmds.menuItem( targetUIName + 'labelSpace', l='', p=parentUIName )
                        targetMenuItem = cmds.menuItem( targetUIName + targetOnlyName, d=1, dividerLabel=dividerLabel, p=parentUIName )
                    else:
                        targetMenuItem = cmds.menuItem( targetUIName + targetOnlyName, d=1, p=parentUIName )
                else:
                    if command == 'isDir':
                        if targetOnlyName[:2] == 'RP':
                            splits = targetOnlyName.split( '-' )
                            targetMenuItem = cmds.menuItem( targetUIName, l='-'.join( splits[2:] ), sm=1, p=parentUIName, rp=splits[1], to=1 )
                        else:
                            targetMenuItem = cmds.menuItem( targetUIName, l=targetOnlyName, sm=1, p=parentUIName, to=1 )
                    else:
                        if targetOnlyName[:2] == 'RP':
                            splits = targetOnlyName.split( '-' )
                            targetMenuItem = cmds.menuItem( targetUIName, l='-'.join( splits[2:] ), c=command, p=parentUIName, rp=splits[1] )
                        else:
                            targetMenuItem = cmds.menuItem( targetUIName, l=targetOnlyName, c=command, p=parentUIName )

                if targetMenuItem:
                    dirAndNames = names+dirs
                    for name in dirAndNames:
                        extention = name.split( '.' )[-1]
                        if extention.lower() in ['py', 'txt', 'mel']: continue
                        if '.'.join( name.split( '.' )[:-1] ) != '.'.join( target.split( '.' )[:-1] ): continue
                        #print cmds.menuItem( targetMenuItem, e=1, image= root + '/' + name )


class Menu_Global:

    menuListFile = cmds.about( pd=True ) + '/%s/menuList.txt' % __name__
    popupListFile_sa = cmds.about( pd=True ) + '/%s/popupList_sa.txt' % __name__
    popupListFile_ca = cmds.about( pd=True ) + '/%s/popupList_ca.txt' % __name__
    loadedMenuInfoFile = cmds.about(pd=True) + "/%s/loadMenuList.txt" % __name__
    loadedPopupInfoFile_sa = cmds.about(pd=True) + "/%s/loadPopupList_sa.txt" % __name__
    loadedPopupInfoFile_ca = cmds.about(pd=True) + "/%s/loadPopupList_ca.txt" % __name__
    
    makeFile( menuListFile )
    makeFile( popupListFile_sa )
    makeFile( popupListFile_ca )
    makeFile( loadedMenuInfoFile )
    makeFile( loadedPopupInfoFile_sa )
    makeFile( loadedPopupInfoFile_ca )
    
    menuPrefix = 'sg_maya_mainWindow'
    popupPrefix = 'sg_maya_popupMenu'
    menuFolderPrefixList = ['_MENU_', '_MAINMENU_', '_POPUPMENU_' ]
    
    
    @staticmethod
    def isMenuDir( dirPath ):
        
        dirName = dirPath.split( '/' )[-1]
        exists = False
        for prefix in Menu_Global.menuFolderPrefixList:
            if dirName.find( prefix ) == -1: continue
            exists = True
        return exists
    
    
    @staticmethod
    def getMenuLabel( dirName ):
        import copy
        newName = copy.copy( dirName )
        for prefix in Menu_Global.menuFolderPrefixList:
            newName = newName.replace( prefix, '' )
        return newName
        




def showMayaWindow( menuName, targetPath ):
    if not os.path.exists( targetPath ): return None
    
    targetPath = targetPath.replace( '\\', '/' )
    menuUiName = Menu_Global.menuPrefix +'_'+ menuName

    cmds.menu( menuUiName, l= menuName, parent='MayaWindow', to=1 )
    cmds.refresh()

    SGFileBaseMenu.renameTargets( targetPath )
    SGFileBaseMenu.assignCommand( menuUiName, targetPath )




def showPopupMenu( menuName, targetPath, typ ):
    
    if not os.path.exists( targetPath ): return None
    
    targetPath = targetPath.replace( '\\', '/' )
    menuUiName = Menu_Global.popupPrefix + '_%s_' % typ + menuName
    
    def show(*args):
        pass
        #cmds.popupMenu( menuUiName, e=1, deleteAllItems=1 )
    if typ == 'ca':
        cmds.popupMenu( menuUiName, ctl=1, alt=1, mm=1, p="viewPanes", pmc=show )
    elif typ == 'sa':
        cmds.popupMenu( menuUiName, sh=1, alt=1, mm=1, p="viewPanes", pmc=show )
    
    SGFileBaseMenu.renameTargets( targetPath )
    SGFileBaseMenu.assignCommand( menuUiName, targetPath )




def loadMenu( evt=0 ):
    from sgModules import sgcommands
    sgcommands.reloadModules()
    MenuController().create()




def getMenuPaths( infoFilePath ):
    
    f = open( infoFilePath, 'r' )
    data = f.read()
    f.close()
    
    paths = data.split( ';' )
    existPaths = []
    for path in paths:
        if not os.path.exists( path ) or path in existPaths: continue
        existPaths.append( path.replace( '\\', '/' ) )
    
    f = open( infoFilePath, 'w' )
    f.write( ';'.join( existPaths ) )
    f.close()
    
    return existPaths




def setMainMenuPaths( paths ):
    existsPaths = []
    for path in paths:
        if os.path.exists( path ) and not path in existsPaths:
            existsPaths.append( path )
    f = open( Menu_Global.menuListFile, 'w' )
    f.write( ';'.join( existsPaths ) )
    f.close()




def setPopupMenuPaths( paths, typ ):
    existsPaths = []
    for path in paths:
        if os.path.exists( path ) and not path in existsPaths:
            existsPaths.append( path )
    
    if typ=='sa':
        popupListFile = Menu_Global.popupListFile_sa
    elif typ=='ca':
        popupListFile = Menu_Global.popupListFile_ca
    
    f = open( popupListFile, 'w' )
    f.write( ';'.join( existsPaths ) )
    f.close()

    


def loadMenuPathEditor( evt=0 ):
    
    from sgUIs import menuLister
    from sgUIs import fileDialog
    menuLister.Win_Global.winName = 'sg_menuList'
    menuLister.Win_Global.title = 'Menu Paths'
    uiInstance = menuLister.Win()
    uiInstance.addListUI( 'Main Menu List' )
    uiInstance.addListUI( 'Popup List ( Shift + Alt )' )
    uiInstance.addListUI( 'Popup List ( Ctrl + Alt )' )
    uiInstance.create()
    
    callbackData = ''

    def showMainMenuList():
        menuPaths = getMenuPaths( Menu_Global.menuListFile )
        menuPaths = list( set( menuPaths ) )
        cmds.textScrollList( uiInstance.ui_folderLists[0].textList, e=1, ra=1, append = menuPaths )
    
    def showPopupMenuList( typ ):
        if typ=='sa':
            popupListFile = Menu_Global.popupListFile_sa
        elif typ=='ca':
            popupListFile = Menu_Global.popupListFile_ca
        menuPaths = getMenuPaths( popupListFile )
        menuPaths = list( set( menuPaths ) )
        if typ == 'sa':
            cmds.textScrollList( uiInstance.ui_folderLists[1].textList, e=1, ra=1, append = menuPaths )
        elif typ == 'ca':
            cmds.textScrollList( uiInstance.ui_folderLists[2].textList, e=1, ra=1, append = menuPaths )


    def addMainMenuFolder( evt=0 ):
        allPaths = getMenuPaths( Menu_Global.menuListFile )
        addPath = fileDialog.getDirectory()
        if addPath and Menu_Global.isMenuDir( addPath ):
            allPaths.append( addPath )
        setMainMenuPaths( allPaths )
        showMainMenuList()
        loadMenu()


    def addPopupMenuFolder( typ, evt=0 ):
        if typ=='sa':
            popupListFile = Menu_Global.popupListFile_sa
        elif typ=='ca':
            popupListFile = Menu_Global.popupListFile_ca
        allPaths = getMenuPaths( popupListFile )
        addPath = fileDialog.getDirectory()
        if addPath and Menu_Global.isMenuDir( addPath ):
            allPaths.append( addPath )
        
        setPopupMenuPaths( allPaths, typ )
        showPopupMenuList(typ)
        loadMenu()



    def removeMainMenuFolder( evt=0 ):
        items = cmds.textScrollList( uiInstance.ui_folderLists[0].textList, q=1, selectItem=1 )
        if not items: return None
        allPaths = getMenuPaths( Menu_Global.menuListFile )
        for item in items:
            cmds.textScrollList( uiInstance.ui_folderLists[0].textList, e=1, removeItem=item )
            if item in allPaths:
                allPaths.remove( item )
        setMainMenuPaths( allPaths )
        showMainMenuList()
        loadMenu()
        

    
    def removePopupMenuFolder( typ, evt=0 ):
        if typ == 'sa':
            items = cmds.textScrollList( uiInstance.ui_folderLists[1].textList, q=1, selectItem=1 )
            if not items: return None
            allPaths = getMenuPaths( Menu_Global.popupListFile_sa )
            for item in items:
                cmds.textScrollList( uiInstance.ui_folderLists[1].textList, e=1, removeItem=item )
                if item in allPaths:
                    allPaths.remove( item )
        elif typ == 'ca':
            items = cmds.textScrollList( uiInstance.ui_folderLists[2].textList, q=1, selectItem=1 )
            if not items: return None
            allPaths = getMenuPaths( Menu_Global.popupListFile_ca )
            for item in items:
                cmds.textScrollList( uiInstance.ui_folderLists[2].textList, e=1, removeItem=item )
                if item in allPaths:
                    allPaths.remove( item )

        setPopupMenuPaths( allPaths, typ )
        showPopupMenuList( typ )
        loadMenu()
    
    
    def drag( *args ):
        print args
    
    def drop( *args ):
        print args


    cmds.button( uiInstance.ui_folderLists[0].addButton, e=1, c=addMainMenuFolder )
    cmds.button( uiInstance.ui_folderLists[1].addButton, e=1, c=partial( addPopupMenuFolder, 'sa' ) )
    cmds.button( uiInstance.ui_folderLists[2].addButton, e=1, c=partial( addPopupMenuFolder, 'ca' ) )
    
    cmds.textScrollList( uiInstance.ui_folderLists[0].textList, e=1, dgc=drag, dpc=drop  )
    cmds.textScrollList( uiInstance.ui_folderLists[1].textList, e=1, dgc=drag, dpc=drop  )
    cmds.textScrollList( uiInstance.ui_folderLists[2].textList, e=1, dgc=drag, dpc=drop  )
    
    cmds.popupMenu( p=uiInstance.ui_folderLists[0].textList)
    cmds.menuItem( l='Remove', c = removeMainMenuFolder )
    cmds.popupMenu( p=uiInstance.ui_folderLists[1].textList )
    cmds.menuItem( l='Remove', c = partial( removePopupMenuFolder, 'sa' ) )
    cmds.popupMenu( p=uiInstance.ui_folderLists[2].textList )
    cmds.menuItem( l='Remove', c = partial( removePopupMenuFolder, 'ca' ) )
    
    showMainMenuList()
    showPopupMenuList('ca')
    showPopupMenuList('sa')

    
        


class MenuController:
    
    def __init__(self):
        
        self.mainMenu = __name__ + '_controller'
        self.label = 'PMC'


    def selectMenu(self, checkMenuName, menuPath, evt=0 ):
        
        checkOn = cmds.menuItem( checkMenuName, q=1, cb=1 )
        
        menuPathLastDirName = Menu_Global.getMenuLabel( menuPath.split( '/' )[-1] )
        if cmds.menu( Menu_Global.menuPrefix + '_' + menuPathLastDirName, q=1, ex=1 ):
            cmds.deleteUI( Menu_Global.menuPrefix + '_' + menuPathLastDirName )
        
        if checkOn:
            f = open( Menu_Global.loadedMenuInfoFile, 'r' )
            pathString = f.read()
            f.close()
            
            if not pathString: pathString = ''
            paths = pathString.split( ';' )
            
            if not menuPath in paths:
                paths.append( menuPath )
                data = ';'.join( paths )
                f = open( Menu_Global.loadedMenuInfoFile, 'w' )
                f.write( data )
                f.close()
            
            showMayaWindow( menuPathLastDirName, menuPath )
        else:
            f = open( Menu_Global.loadedMenuInfoFile, 'r' )
            pathString = f.read()
            f.close()
            
            if not pathString: pathString = ''
            paths = pathString.split( ';' )
            
            if menuPath in paths:
                paths.remove( menuPath )
            
            data = ';'.join( paths )
            f = open( Menu_Global.loadedMenuInfoFile, 'w' )
            f.write( data )
            f.close()
    
    
    
    def selectPopup(self, popupPath, typ, evt=0 ):
        
        if typ == 'sa': 
            self.clearPopupSa()
            loadedPopupInfoFile = Menu_Global.loadedPopupInfoFile_sa
        elif typ == 'ca': 
            self.clearPopupCa()
            loadedPopupInfoFile = Menu_Global.loadedPopupInfoFile_ca
        
        showPopupMenu( Menu_Global.getMenuLabel(popupPath.split( '/' )[-1]), popupPath, typ )
        
        f = open( loadedPopupInfoFile, 'w' )
        f.write( popupPath )
        f.close()
    


    def clearPopupCa(self, evt=0):
        
        for ui in cmds.lsUI( m=1 ):
            if ui.find( Menu_Global.popupPrefix+'_ca_' ) != -1:
                if not ui in cmds.lsUI( m=1 ): continue
                cmds.deleteUI( ui )
    
    
    def clearPopupSa(self, evt=0):
        
        for ui in cmds.lsUI( m=1 ):
            if ui.find( Menu_Global.popupPrefix+'_sa_' ) != -1:
                if not ui in cmds.lsUI( m=1 ): continue
                cmds.deleteUI( ui )
    


    def clearMenu(self, evt=0 ):
        
        for ui in cmds.lsUI( m=1 ):
            if ui.find( Menu_Global.menuPrefix ) != -1:
                if not ui in cmds.lsUI( m=1 ): continue
                cmds.deleteUI( ui )
    


    def isMenuChecked(self, menuPath ):
        
        f = open( Menu_Global.loadedMenuInfoFile, 'r' )
        pathString = f.read()
        f.close()
        
        if not pathString: pathString = ''
        paths = pathString.split( ';' )
        
        return menuPath in paths
    


    def isPopupChecked(self, popupPath, typ ):
        
        if typ=='sa':
            loadedPopupInfoFile = Menu_Global.loadedPopupInfoFile_sa
        elif typ=='ca':
            loadedPopupInfoFile = Menu_Global.loadedPopupInfoFile_ca
        
        f = open( loadedPopupInfoFile, 'r' )
        pathString = f.read()
        f.close()
        
        return pathString == popupPath
    


    def create(self):
        
        self.clearMenu()
        self.clearPopupCa()
        self.clearPopupSa()
        
        if cmds.menu( self.mainMenu, q=1, ex=1 ):
            cmds.deleteUI( self.mainMenu )
        cmds.menu( self.mainMenu, p='MayaWindow', l= self.label, to=1  )
        
        cmds.menuItem( l= 'UI - List Menu Paths', p= self.mainMenu, c= loadMenuPathEditor,
                       image=os.path.dirname( __file__ ) + '/icons/list.png' )
        cmds.menuItem( d=1, dl="Main Menu", p=self.mainMenu )
        
        for menuPath in getMenuPaths( Menu_Global.menuListFile ):
            menuChecked = self.isMenuChecked( menuPath )
            dirname = Menu_Global.getMenuLabel( menuPath.split( '/' )[-1] )
            menuName = cmds.menuItem( l= dirname, p= self.mainMenu, cb=menuChecked )
            cmds.menuItem( menuName, e=1, c= partial( self.selectMenu, menuName, menuPath ) )
            if menuChecked: self.selectMenu( menuName, menuPath )
        
        cmds.menuItem( d=1, dl="Popup Menu( Shift + alt + RMB )", p=self.mainMenu )
        popupShiftAlt = cmds.menuItem( l="Popup Menu( Shift + alt + RMB )", p=self.mainMenu, sm=1 )
        cmds.radioMenuItemCollection( p = popupShiftAlt )
        cmds.menuItem( l= "Clear", p= popupShiftAlt, rb=1, c=self.clearPopupSa )
        for menuPath in getMenuPaths( Menu_Global.popupListFile_sa ):
            popupChecked = self.isPopupChecked( menuPath, 'sa' )
            dirname = Menu_Global.getMenuLabel( menuPath.split( '/' )[-1] )
            popupName = cmds.menuItem( l= dirname, p= popupShiftAlt, rb=popupChecked )
            cmds.menuItem( popupName, e=1, c= partial( self.selectPopup, menuPath, 'sa' ), p=popupShiftAlt )
            if popupChecked: self.selectPopup( menuPath, 'sa' )
        
        cmds.menuItem( d=1, dl="Popup Menu( Ctrl + alt + RMB )", p=self.mainMenu )
        popupCtrlAlt = cmds.menuItem( l="Popup Menu( Shift + alt + RMB )", p=self.mainMenu, sm=1 )
        cmds.radioMenuItemCollection( p = popupCtrlAlt )
        cmds.menuItem( l= "Clear", p= popupCtrlAlt, rb=1, c=self.clearPopupCa )
        for menuPath in getMenuPaths( Menu_Global.popupListFile_ca ):
            popupChecked = self.isPopupChecked( menuPath, 'ca' )
            dirname = Menu_Global.getMenuLabel( menuPath.split( '/' )[-1] )
            popupName = cmds.menuItem( l= dirname, p= popupCtrlAlt, rb=popupChecked )
            cmds.menuItem( popupName, e=1, c= partial( self.selectPopup, menuPath, 'ca' ) )
            if popupChecked: self.selectPopup( menuPath, 'ca' )
        
        cmds.menuItem( d=1, dl="", p=self.mainMenu )
        cmds.menuItem( l="Get Icon", p=self.mainMenu, c="import webbrowser;url = 'http://www.flaticon.com/';webbrowser.open_new_tab( url )",
                       image=os.path.dirname( __file__ ) + '/icons/search.png')
        cmds.menuItem( d=1, dl="", p=self.mainMenu )
        cmds.menuItem( l="Reload Menu", c=loadMenu, p=self.mainMenu, 
                       image=os.path.dirname( __file__ ) + '/icons/reload.png' )

