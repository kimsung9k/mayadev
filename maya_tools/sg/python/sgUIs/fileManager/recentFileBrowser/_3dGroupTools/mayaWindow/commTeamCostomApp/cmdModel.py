import sys, os
import maya.cmds as cmds
import maya.mel as mel
from functools import partial

import sub_view
import model
import socket
import datetime
import view

import functions.path as pathFunction


def getMayaDocPath():
    
    mayaDocPath = os.path.expanduser('~\\maya').replace( '\\', '/' )
    return mayaDocPath



def makeFolder( pathName ):
    if os.path.exists( pathName ):return None
    os.makedirs( pathName )
    return pathName




def getTimeString():
    
    timenow = datetime.datetime.now()
    
    year = timenow.year
    month = timenow.month
    day   = timenow.day
    hour  = timenow.hour
    minute= timenow.minute
    second= timenow.second
    microsecond = timenow.microsecond
    
    return '%04d%02d%02d%02d%02d%02d%06d' %( year, month, day, hour, minute, second, microsecond )




def makeFile( pathName ):
    pathName = pathName.replace( '\\', '/' )
    splitPaths = pathName.split( '/' )
    
    folderPath = '/'.join( splitPaths[:-1] )
    
    makeFolder( folderPath )
    
    if not os.path.exists( pathName ):
        f = open( pathName, 'w' )
        f.close()
        
        
        
def deletePath( pathName ):
    pathName = pathName.replace( '\\', '/' )
    
    deleteDirTargets = []
    for root, dirs, names in os.walk( pathName ):
        for name in names:
            os.remove( root+'/'+name )
        if root == pathName: continue
        deleteDirTargets.append( root )
    
    deleteDirTargets.reverse()
    for deleteDirTarget in deleteDirTargets:
        if os.path.exists( deleteDirTarget ):
            try:os.rmdir( deleteDirTarget )
            except: print "Failed Remove Dir : %s" % deleteDirTarget



def deleteCategory( categoryName ):
    
    f = open( model.idPath, 'r' )
    data = f.read()
    f.close()
    
    idName = ''
    
    for line in data.split( '\n' ):
        hostName, id, date = line.split( ':' )
        if hostName == socket.gethostname():
            idName = id
    if not idName:  return None
    
    categoryPath = model.categoryBasePath + '/' + idName + '/' + categoryName
    deletePath( categoryPath )
    try:os.rmdir( categoryPath )
    except:pass



def checkIdExists():
    
    myHostName = socket.gethostname()
    
    idPath       = model.idPath.replace( '\\', '/' )
    f = open( idPath, 'r' )
    data = f.read()
    f.close()
    
    hostList = data.split( '\n' )
    
    for host in hostList:
        hostName, id, time = host.strip().split( ':' )
        if myHostName == hostName:
            return True
    return False



def checkSameIdExists( idName ):
    
    f = open( model.idPath, 'r' )
    data = f.read()
    f.close()
    
    for line in data.split( '\n' ):
        host, id, time = line.strip().split( ':' )
        if id == idName:
            return True
    
    return False
    
    



def getHostInfo():
    
    idPath       = model.idPath.replace( '\\', '/' )
    f = open( idPath, 'r' )
    data = idPath.read()
    f.close()
    
    hostList = data.split( '\n' )
    
    hostInfos = []
    
    for host in hostList:
        hostInfos.append( host.strip().split( '/' ) )



def getCategoryList():
    
    hostName = socket.gethostname()
    
    f = open( model.idPath, 'r' )
    data = f.read()
    f.close()
    
    myId = ''
    for line in data.split( '\n' ):
        host, id, date = line.strip().split( ':' )
        if hostName == host:
            myId = id
    if not myId:
        view.RegistrationUI().create()
        return None
    
    categoryPath = model.categoryBasePath.replace( '\\', '/' ) + '/' + myId
    pathFunction.makeFolder( model.categoryBasePath + '/' + myId )

    checkDirs = []
    for root, dirs, names in os.walk( categoryPath ):
        
        if categoryPath == root: continue
        
        mainCmdExists = False
        for name in names:
            if name.find( model.mainCommmandName ) != -1:
                mainCmdExists = True
        
        if mainCmdExists: continue
        
        replaceRoot = root.replace( '\\', '/' )
        checkDir = replaceRoot.replace( categoryPath+'/', '' )
        if not names: continue
        checkDirs.append( checkDir )
        
    return checkDirs



def makeCategory( category ):
    
    if not category: return None
    category = category.replace( '.', '/' )
    
    f = open( model.idPath, 'r' )
    data = f.read()
    f.close()
    
    categoryHierarcy = []
    for line in data.split( '\n' ):
        hostName, id, date = line.split( ':' )
        if hostName == socket.gethostname():
            categoryHierarcy = [ id ]
            break
    if not categoryHierarcy: return None

    categoryHierarcy += category.split( '/' )
    for i in range( len( categoryHierarcy ) ):
        categoryFolder = model.categoryBasePath+'/'
        for j in range( i+1 ):
            categoryFolder += categoryHierarcy[j] +'/'
        pathFunction.makeFile( categoryFolder )
        pathFunction.makeFile( categoryFolder+'/__init__.py' )



def makeTampCmdFolder():
    
    mayaDocPath = getMayaDocPath()
    cmdTempFolder = mayaDocPath + '/LocusCommPackagePrefs/commTeamCostomApp/cmdTempFolder'
    
    if os.path.exists( cmdTempFolder ):
        deletePath( cmdTempFolder )
    
    makeFolder( cmdTempFolder )
    return cmdTempFolder



def getTempCmdFolder():
    
    mayaDocPath = getMayaDocPath()
    cmdTempFolder = mayaDocPath + '/LocusCommPackagePrefs/commTeamCostomApp/cmdTempFolder'
    
    return cmdTempFolder



class uiCmd:
    
    def __init__(self, pWindow ):
        
        self.pWindow = pWindow
        self.winName = pWindow.winName



    def addChild( self, tabLayout, label='source_0', *args ):
    
        children  = cmds.tabLayout( tabLayout, q=1, ca=1 )
        tabLabels = cmds.tabLayout( tabLayout, q=1, tabLabel=1 )
        if not children: children = []; tabLabels=[]
        
        items = []
        for i in range( len( children ) ):
            items.append( (children[i], tabLabels[i] ) )
        cmds.setParent( tabLayout )
        newChild = cmds.scrollField()
        
        cmds.popupMenu( markingMenu=1 )
        cmds.menuItem( l='Add Tab', rp='N', c= sub_view.Window_addTab( self.pWindow ).create )
        if len( items ) != 0:
            cmds.menuItem( l='Delete Tab', rp='S', c= sub_view.Window_deleteTab( self.pWindow ).create )
        items.append( (newChild.split( '|' )[-1], label )  )
        
        cmds.tabLayout( tabLayout, e=1, tabLabel=items )
        
        return newChild



    def deleteChild( self, *args ):
        
        tabLayout = self.pWindow.tab
        selItemIndex = cmds.tabLayout(tabLayout, q=1, sti=1 )
        
        if selItemIndex == 1: cmds.error( 'Main Command tab Can not delete' )
        
        children  = cmds.tabLayout( tabLayout, q=1, ca=1 )
        tabLabels = cmds.tabLayout( tabLayout, q=1, tabLabel=1 )

        cmds.deleteUI( children.pop( selItemIndex-1 ) )
        tabLabels.pop( selItemIndex-1 )
        
        items = []
        for i in range( len( children ) ):
            items.append( (children[i], tabLabels[i] ) )
        
        cmds.tabLayout( tabLayout, e=1, tabLabel=items )
        
        
    
    def testApp(self, *args ):
        
        title   = cmds.textField( self.pWindow.titleField, q=1, tx=1 )
        selItem = cmds.radioCollection( self.pWindow.collection, q=1, sl=1 )
        collectionItems = cmds.radioCollection( self.pWindow.collection, q=1, collectionItemArray=1 )
        selItems = ['mel','python']

        for i in range( len( collectionItems ) ):
            if collectionItems[i].find( selItem ) != -1:
                break
        cmdTestApp( self.pWindow.tab, title, selItems[i] )
        
        
    def openUpdateApp( self, *args ):
        
        sub_view.Window_updateApp( self.pWindow ).create()
    
    
    
    def editApp(self, *args ):
        
        sub_view.Window_editApp( self.pWindow ).create()
    
        
    def deleteApp(self, *args ):
        
        sub_view.Window_deleteApp( self.pWindow ).create()
        
        
    def close(self, *args ):
        
        cmds.deleteUI( self.pWindow.winName )




def cmdLoadBeforeSetting( pWindow, textField, tabLayout, radioCollection, packageFolderPath ):

    packageFolderPath = packageFolderPath.replace( '\\', '/' )
    packageFolderName = packageFolderPath.split( '/' )[-1]

    codeNames = []
    codePaths = []
    codeTypeIndex = 0
    
    for root, dirs, names in os.walk( packageFolderPath ):
        if not names:
            return None
        else:
            for name in names:
                codeName, extension = name.split( '.' )
                
                if codeName == '__init__': continue
                
                if extension == 'mel':
                    codeTypeIndex = 0
                elif extension == 'py':
                    codeTypeIndex = 1
                else:
                    continue
                codeNames.append( codeName )
                codePaths.append( root+'/'+name )
        break
    
    items = []
    cmds.setParent( tabLayout )
    mainCommandField = cmds.tabLayout( tabLayout, q=1, ca=1 )[0]
    
    uiCmdInst = uiCmd( pWindow )
    
    for i in range( len( codeNames ) ):
        codeName = codeNames[i]
        codePath = codePaths[i]
        
        f = open( codePath, 'r' )
        data = f.read()
        f.close()
        
        if codeName == 'MainCommand':
            scrollField = mainCommandField
        else:
            scrollField = uiCmdInst.addChild(tabLayout, codeName)
        cmds.scrollField( scrollField, e=1, tx=data )
    cmds.setParent( '..' )
    
    childItems = cmds.radioCollection( radioCollection, q=1, cia=1 )
    
    cmds.radioCollection( radioCollection, e=1, sl=childItems[codeTypeIndex] )
    cmds.textField( textField, e=1, tx=packageFolderName )
    cmds.tabLayout( tabLayout, e=1, tabLabel=items )




def makeAppFolders( tabLayout, title, cmdType, folderPath ):
    
    childArr  = cmds.tabLayout( tabLayout, q=1, ca=1 )
    tabLabels = cmds.tabLayout( tabLayout, q=1, tabLabel=1 )
    
    appFolder = folderPath+'/'+ title
    deletePath( appFolder )
    
    if cmdType == 'python':
        initPath = appFolder+'/__init__.py'
        makeFile( initPath )

        for i in range( len( childArr ) ):
            childUi  = childArr[i]
            tabLabel = tabLabels[i].replace( ' ', '_' )
            
            srcFile = appFolder+'/'+tabLabel+'.py'
            makeFile( srcFile )
            
            f = open( srcFile, 'w' )
            f.write( cmds.scrollField( childUi, q=1, tx=1 ) )
            f.close()
        
    elif cmdType == 'mel':
        for i in range( len( childArr ) ):
            childUi  = childArr[i]
            tabLabel = tabLabels[i].replace( ' ', '_' )
            
            srcFile = appFolder+'/'+tabLabel+'.mel'
            makeFile( srcFile )
            
            f = open( srcFile, 'w' )
            f.write( cmds.scrollField( childUi, q=1, tx=1 ) )
            f.close()




def cmdTestApp( tabLayout, title, cmdType ):
    
    cmdTempFolder = makeTampCmdFolder()
    makeAppFolders( tabLayout, title, cmdType, cmdTempFolder )
    
    appFolder = cmdTempFolder+'/'+title
    
    mainCmdFile =''
    otherFiles = []
    
    for root, dirs, names in os.walk( appFolder ):
        for name in names:
            if name.find( 'MainCommand' ) != -1:
                mainCmdFile = root+'/'+name
            else:
                otherFiles.append( root+'/'+name )
    
    if cmdType == 'python':
        if not cmdTempFolder in sys.path:
            sys.path.append( cmdTempFolder )
        importString = mainCmdFile.replace( cmdTempFolder+'/', '' ).split( '.' )[0].replace( '/', '.' )
        try:
            reload( sys.modules['%s' % importString ] )
        except:
            exec( 'import %s' % importString )
    elif cmdType == 'mel':
        f=open( mainCmdFile, 'r' )
        cmdStr = f.read()
        f.close()
        for otherFile in otherFiles:
            mel.eval( 'source "%s";' % otherFile )
        mel.eval( cmdStr )



        

def cmdUpdateApp( tabLayout, optionMenu, title, cmdType ):
    
    menuItems = cmds.optionMenu( optionMenu, q=1, itemListShort=1 )
    selectIndex = cmds.optionMenu( optionMenu, q=1, select=1 )-1
    addPath = cmds.menuItem( menuItems[ selectIndex ], q=1, l=1 )
    
    f = open( model.idPath, 'r' )
    data = f.read()
    f.close()
    
    myHost = socket.gethostname()
    lines = data.split( '\n' )
    myId = ''
    for line in lines:
        host, id, date = line.strip().split( ':' )
        if myHost == host:
            myId = id
    
    if not myId:
        view.RegistrationUI().create()
        return None
    
    if addPath == 'None':
        folderPath = folderPath = model.categoryBasePath + '/' + myId
    else:
        folderPath = model.categoryBasePath + '/' + myId + "/" + addPath
    
    makeAppFolders( tabLayout, title, cmdType, folderPath )




def cmdEditApp( tabLayout, folderPath, title, cmdType ):
    makeAppFolders( tabLayout, title, cmdType, folderPath )



def makeInitFilesInPaths( basePath, assignPath ):
    
    basePath = basePath.replace( '\\', '/' )
    assignPath = assignPath.replace( '\\', '/' )
    
    elsePath = assignPath.replace( basePath,'' )
    splitsElse = elsePath.split( '/' )
    
    folderHierarchy = []
    for splitElse in splitsElse:
        if splitElse:
            folderHierarchy.append( splitElse )
    
    folderHierarchyLength = len( folderHierarchy )
    
    for i in range( folderHierarchyLength ):
        addPath = '/'.join( folderHierarchy[:i+1] )
        makeFile( basePath + '/' + addPath + '/__init__.py'  )
        
        
        
def checkHostIsMine( path ):
    
    hostName = socket.gethostname()
    f = open( model.idPath, 'r' )
    data = f.read()
    f.close()
    
    lines = data.split( '\n' )
    targetId = ''
    for line in lines:
        host, id, date = line.strip().split( ':' )
        if hostName == host:
            targetId = id
            break
    
    if not targetId: return False
    if path.find( targetId ) != -1:
        return True
    else:
        return False
    
    