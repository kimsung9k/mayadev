import maya.cmds as cmds
import maya.mel as mel
import shutil, os, glob
from functools import partial
import datetime
import functions.path as pathFunctions
import _3dGroupTools.openFileHistoryCmdModel as _3dGroupFileHistroy


class model:
    mayaDocPath = pathFunctions.getMayaDocPath()
    serverPathInfoFilePath = mayaDocPath+'/LocusCommPackagePrefs/versionControlWorkSpaceInfo/asset_serverPath.txt'
    importPathInfoFilePath = mayaDocPath+'/LocusCommPackagePrefs/versionControlWorkSpaceInfo/asset_importPath.txt'
    defaultFileBrowserPath = mayaDocPath+'/projects'
    
    
    
def separateFolderAndfile( path ):
    
    if os.path.isdir( path ):
        return path, ''
    
    path = path.replace( '\\', '/' )
    splitPath = path.split( '/' )
    folderPath = '/'.join( splitPath[:-1] )
    filePath = splitPath[-1]
    
    return folderPath, filePath



def isFile( path ):
    
    return os.path.isfile( path )
    
    
    
def isFolder( path ):
    
    return os.path.isdir( path )


    
    
def getUIPosition( uiWidth ):

    mayaWindow_width = cmds.window( 'MayaWindow', q=1, w=1 )
    mayaWindow_top, mayaWindowLeft = cmds.window( 'MayaWindow', q=1, tlc=1 )
    
    uiTop  = mayaWindow_top + 195
    uiLeft = mayaWindowLeft + mayaWindow_width - uiWidth - 36
    
    return uiTop, uiLeft



def openFileBrowser( path='', *args ):
    
    if not isFile( path ) and not isFolder( path ):
        path = model.defaultFileBrowserPath
    
    path = path.replace( '\\', '/' )
    if isFile( path ):
        path = '/'.join( path.split( '/' )[:-1] )
        
    os.startfile( path )
    
    
    
def importFile( path ):
    
    extension = path.split('.')[-1].lower()
    pluginList = cmds.pluginInfo( q=1, listPlugins=1 )
    if extension == "fbx":
        if not 'fbxmaya' in pluginList:
            cmds.loadPlugin( 'fbxmaya' )
    if extension == 'obj':
        if not 'objExport' in pluginList:
            cmds.loadPlugin( 'objExport' )
    cmds.file( path, i=1, ignoreVersion=True, ra=True, mergeNamespacesOnClash=True, namespace=":", options="v=0;", pr=True, loadReferenceDepth="all" )



def checkSamePathAndRenamePath( path ):
    
    splitPath = path.replace( '\\', '/' ).split( '/' )
    
    currentFolderPath = '/'.join( splitPath[:-1] )
    fileName = splitPath[-1]
    onlyFileName, extension = fileName.split('.')
    extensionSize = len( extension )
    
    indexStrs = ''
    for i in range( len( onlyFileName ) ):
        cuIndex = len( onlyFileName ) - i -1
        if onlyFileName[cuIndex].isdigit():
            indexStrs = onlyFileName[cuIndex] + indexStrs
        else:
            break
    
    if indexStrs:
        onlyFileNameNumberCut = onlyFileName[:cuIndex+1]
        formatStr = onlyFileNameNumberCut+'*.'+extension
    else:
        onlyFileNameNumberCut = onlyFileName
        formatStr = onlyFileName+'*.'+extension
    
    sameFiles = glob.glob( currentFolderPath +'/'+ formatStr )
    compairName = (currentFolderPath+'/'+onlyFileNameNumberCut ).replace( '\\', '/' )
    checkSameFiles = []
    
    for sameFile in sameFiles:
        sameFile = sameFile.replace( '\\', '/' )
        if sameFile == compairName+'.'+extension:
            checkSameFiles.append( sameFile )
            continue
        digit = sameFile[:-(extensionSize+1)].replace( compairName, '' )
        
        if digit.isdigit():
            checkSameFiles.append( sameFile )
    
    for fileName in checkSameFiles:
        print fileName

    checkSameFiles.sort()
    if checkSameFiles:
        onlyFileName  = checkSameFiles[-1][:-(extensionSize+1)]
        extension     = checkSameFiles[-1][-extensionSize:]
        
        indexStrs = ''
        for i in range( len( onlyFileName ) ):
            cuIndex = len( onlyFileName ) - i -1
            if onlyFileName[cuIndex].isdigit():
                indexStrs = onlyFileName[cuIndex] + indexStrs
            else:
                break
        if indexStrs:
            lenIndex = len( indexStrs )
            formatStr = onlyFileName[:cuIndex+1]+'%0'+str(lenIndex)+'d'
            currentFilePath = formatStr % (int( indexStrs )+1) +'.'+extension
        else:
            #print onlyFileName + '%02d' %( 1 )+'.'+extension
            currentFilePath = onlyFileName + '%02d' %( 1 )+'.'+extension
    else:
        currentFilePath = currentFolderPath+'/'+fileName
    
    return currentFilePath



def copyFromServerAndOpen( path ):
    
    splitPath = path.replace( '\\', '/' ).split( '/' )
    
    fileName = splitPath[-1]
    
    nowTime = datetime.datetime.now()
    folderName ='%04d%02d%02d' %( nowTime.year, nowTime.month, nowTime.day )
    
    currentFolderPath = model.defaultFileBrowserPath +"/"+ folderName
    pathFunctions.makePath( currentFolderPath )
    
    currentFilePath = checkSamePathAndRenamePath( currentFolderPath+'/'+fileName )
    print "currentFilePath : ", currentFilePath
    
    shutil.copy2( path, currentFilePath )
    cmds.file( currentFilePath, f=1, options="v=0;" , ignoreVersion=1, o=1 )
    


def getCurrentScenePath():
    
    return cmds.file( q=1, sceneName=1 )



def getBackupPath( serverPath ):
    
    serverSplit = serverPath.replace( '\\', '/' ).split( '/' )
    nowTime = datetime.datetime.now()
    folderName ='%04d%02d%02d' %( nowTime.year, nowTime.month, nowTime.day )
    backupPath = '/'.join( serverSplit[:-1] )+'/backup/%s' % folderName
    pathFunctions.makePath( backupPath )
    return backupPath, serverSplit[-1]
    


def saveAndUpdate( currentPath, serverPath ):
    
    backupFolderPath, fileName = getBackupPath( serverPath )
    #print "before : ", backupFolderPath+'/'+fileName
    backupFileName = checkSamePathAndRenamePath( backupFolderPath+'/'+fileName )
    
    if os.path.exists( serverPath ):
        shutil.copy2( serverPath, backupFileName )
        print "from    : ", serverPath
        print "copy to : ", backupFileName
    
    serverFolderName, serverFileName = separateFolderAndfile( serverPath )
    currentFileName = ''
    if serverFileName:
        currentFileName = serverFileName
    else:
        currentFileName = 'temp.mb'
        
    if not os.path.exists( currentPath ):
        nowTime = datetime.datetime.now()
        folderName ='%04d%02d%02d' %( nowTime.year, nowTime.month, nowTime.day )
        filePath = model.defaultFileBrowserPath+'/'+folderName+'/'+currentFileName
        currentPath = checkSamePathAndRenamePath( filePath )
    
    pathFunctions.makePath( '/'.join( currentPath.split( '/' )[:-1] ) )
    cmds.file( rename=currentPath )
    cmds.file( save=1 )
    
    shutil.copy2( currentPath, serverPath )



def loadScrollList( scrollList ):
    
    paths = []
    
    for root, dirs, names in os.walk( _3dGroupFileHistroy.Model.fileHistoryPath ):
        
        for name in names:
            filePath = root.replace( '\\', '/' ) + '/' + name
            pathFunctions.makeFile( filePath )
        
            f = open( filePath, 'r' )
            data = f.read()
            f.close()
            
            for line in data.split( '\n' ):
                splits = line.split( '-' )
                line = splits[0]
                path = '-'.join( splits[1:] )
                if path in paths:
                    paths.remove( path )
                paths.append( path )
                
            paths.reverse()
        break
    
    cmds.textScrollList( scrollList, e=1, ra=1, append=paths )