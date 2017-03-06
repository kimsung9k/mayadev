import os, glob
import shutil
import sgModelFileAndPath
import datetime



def isFile( path ):
    
    return os.path.isfile( path )
    
    
    
def isFolder( path ):
    
    return os.path.isdir( path )



def openFileBrowser( path='', *args ):
    
    path = path.replace( '\\', '/' )
    
    if not sgModelFileAndPath.isFile( path ) and not sgModelFileAndPath.isFolder( path ):
        return None
    
    if sgModelFileAndPath.isFile( path ):
        path = '/'.join( path.split( '/' )[:-1] )
        
    os.startfile( path )




def makePath( pathName ):
    splitPaths = pathName.split( '/' )
    
    cuPath = splitPaths[0]
    
    for i in range( 1, len( splitPaths ) ):
        checkPath = cuPath+'/'+splitPaths[i]
        if not os.path.exists( checkPath ):
            os.chdir( cuPath )
            os.mkdir( splitPaths[i] )
        cuPath = checkPath




def makeFolder( pathName ):
    splitPaths = pathName.split( '/' )
    
    cuPath = splitPaths[0]
    
    for i in range( 1, len( splitPaths ) ):
        checkPath = cuPath+'/'+splitPaths[i]
        if not os.path.exists( checkPath ):
            os.chdir( cuPath )
            os.mkdir( splitPaths[i] )
        cuPath = checkPath
        
        


def makeFile( pathName, autoRename=True ):
    splitPaths = pathName.split( '/' )
    
    folderPath = '/'.join( splitPaths[:-1] )
    
    makeFolder( folderPath )
    
    if not os.path.exists( pathName ):
        f = open( pathName, 'w' )
        f.close()
    else:
        if autoRename:
            pathName = checkSamePathAndRenamePath( pathName )
    
    return pathName
        
        


def deletePathHierarchy( pathName ):
    pathName = pathName.replace( '\\', '/' )
    
    deleteDirTargets = []
    for root, dirs, names in os.walk( pathName ):
        for name in names:
            try:os.remove( root+'/'+name )
            except:pass
        if root == pathName: continue
        deleteDirTargets.append( root )
    
    deleteDirTargets.reverse()
    for deleteDirTarget in deleteDirTargets:
        if os.path.exists( deleteDirTarget ):
            try:os.rmdir( deleteDirTarget )
            except:pass




def checkExistsFolderAndGetNewFolder( folder ):
    
    if not os.path.exists( folder ):
        makeFolder( folder )
        return folder
    
    for root, dirs, names in os.walk( folder ):
        if not dirs and not names:
            return root
        break

    digits = []
    for char in folder:
        if char.isdigit():
            digits.append( char )
        else:
            digits = []
    if not digits: digits = ['0']
    
    return checkExistsFolderAndGetNewFolder( folder[:-len( digits )] + str( int( ''.join( digits ) )+1 ) )




def getDefaultCachePath():
    
    cachePath = checkExistsFolderAndGetNewFolder( sgModelFileAndPath.getMayaDocPath() + "/projects/default/cache/tempCache" )
    makeFolder( cachePath )
    return cachePath




def removeFileTypeHierarcy( path, fileType ):
    
    lenFileType = len( fileType )
    for root, dirs, names in os.walk( path ):
        for name in names:
            if len( name ) < lenFileType: continue
            if name[-lenFileType:] == fileType:
                os.remove( root+'/'+name )



def removeFileHierarchy( path ):
    
    for root, dirs, names in os.walk( path ):
        for name in names:
            os.remove( root+'/'+name )




def copyFilesToTargetPath( fromPath, toPath ):
    
    fromPath = fromPath.replace( '\\', '/' )
    toPath = toPath.replace( '\\', '/' )
    
    for root, dirs, names in os.walk( fromPath ):
        
        toRoot = root.replace( '\\', '/' ).replace( fromPath, toPath )
        
        for directory in dirs:
            makeFolder( toRoot+'/'+directory )
        for name in names:
            if name.split('.')[1].lower() == 'pyc': continue
            shutil.copy2( root+'/'+name, toRoot+'/'+name )



def moveDefulatCacheFilesToCurrentCacheFiles( defaultCacheFolder, currentCacheFolder ):
    
    copyFilesToTargetPath( defaultCacheFolder, currentCacheFolder )
    removeFileHierarchy( defaultCacheFolder )
    



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
        print "exist path -", fileName

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



def autoLoadPlugin( pluginName ):
    import maya.mel as mel
    import maya.cmds as cmds
    def displayMessage( message, messageOn = False ):
        if messageOn:
            print message
        
    pluginPaths = []
    for path in mel.eval( 'getenv MAYA_PLUG_IN_PATH' ).split( ';' ):
        if not path: continue
        pluginPaths.append( path )
    pluginList = cmds.pluginInfo( q=1, listPlugins=1 )
    
    loadPluginPaths = []
    for path in pluginPaths:
        loadPluginPaths += glob.glob( "%s/%s*.mll" %( path, pluginName ) )
    
    targetPlugList = []
    paths = []
    for pluginPath in loadPluginPaths:
        path, plugin = pluginPath.split( '\\' )
       
        digit = plugin[ len( pluginName ): -4].replace( '_', '' )
        if not digit:
            targetPlugList.append( plugin[:-4] )
            if not len( paths ) : paths.append( path )
            if not path in paths: paths.append( path )
        elif digit.isdigit():
            targetPlugList.append( plugin[:-4] )
            if not len( paths ) : paths.append( path )
            if not path in paths: paths.append( path )

    targetPlugList.sort()
    if not targetPlugList: 
        displayMessage( '"%s" is not existing in plug-in path' % pluginName )
        return None
         
    if len( paths ) > 1:
        displayMessage( "\nTarget Plug-in exist in multiple paths" )
        displayMessage( "------------------------------------------------------" )
        for path in paths:
            displayMessage( path )
        displayMessage( "------------------------------------------------------\n" )
        displayMessage( "Target Plug-in exist in multiple paths" )
        return None
    
    if pluginList:
        if targetPlugList[-1] in pluginList:
            displayMessage( "%s is already loaded" % targetPlugList[-1] )
            return None
        for targetPlug in targetPlugList:
            if targetPlug in pluginList:
                try:
                    cmds.unloadPlugin( targetPlug )
                    displayMessage( '"%s" is unloaded' % targetPlug )
                except: 
                    displayMessage( "UnloadPlugin Failed : %s" % targetPlug )
                    return None
    else:
        for targetPlug in targetPlugList:
            try: 
                cmds.unloadPlugin( targetPlug )
                displayMessage( '"%s" is unloaded' % targetPlug )
            except: 
                displayMessage( "UnloadPlugin Failed : %s" % targetPlug )
                return None

    cmds.loadPlugin( targetPlugList[-1] )
    displayMessage( '"%s" is loaded' % targetPlugList[-1] )