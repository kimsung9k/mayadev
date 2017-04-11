import os, glob, sys, shutil
import sgBModel_string
import datetime



def getDocumentPath():
    return os.path.expanduser('~')




def getRemovedFilePath():
    removedFilePath = getDocumentPath() + '/removedFiles'
    makeFolder( removedFilePath )
    return removedFilePath




def getMayaDocPath():
    return os.path.expanduser( '~/maya' )




def getDefaultProjectPath():
    return getMayaDocPath() + '/projects/default'




def getLocusCommPackagePrefsPath():
    locusCommPackagePath = getMayaDocPath() + '/LocusCommPackagePrefs'
    makeFolder( locusCommPackagePath )
    return  locusCommPackagePath




def getPathInfo_sgPWindow_file_meshGroup():
    
    import sgBModel_fileAndPath
    locusCommPackagePrefsPath = getLocusCommPackagePrefsPath()
    return locusCommPackagePrefsPath + sgBModel_fileAndPath.pathInfo_sgPWindow_file_meshGroup


def getUiInfo_sgPWindow_file_meshGroup():
    
    import sgBModel_fileAndPath
    locusCommPackagePrefsPath = getLocusCommPackagePrefsPath()
    return locusCommPackagePrefsPath + sgBModel_fileAndPath.uiInfo_sgPWindow_file_meshGroup



def getPathInfo_sgPWindow_file_cache():
    
    import sgBModel_fileAndPath
    locusCommPackagePrefsPath = getLocusCommPackagePrefsPath()
    return locusCommPackagePrefsPath + sgBModel_fileAndPath.pathInfo_sgPWindow_file_cache


def getUiInfo_sgPWindow_file_cache():
    
    import sgBModel_fileAndPath
    locusCommPackagePrefsPath = getLocusCommPackagePrefsPath()
    return locusCommPackagePrefsPath + sgBModel_fileAndPath.uiInfo_sgPWindow_file_cache


def getPathInfo_sgPWindow_file_alembic():
    
    import sgBModel_fileAndPath
    locusCommPackagePrefsPath = getLocusCommPackagePrefsPath()
    return locusCommPackagePrefsPath + sgBModel_fileAndPath.pathInfo_sgPWindow_file_alembic


def getPathInfo_sgPWindow_file_key():
    
    import sgBModel_fileAndPath
    locusCommPackagePrefsPath = getLocusCommPackagePrefsPath()
    return locusCommPackagePrefsPath + sgBModel_fileAndPath.pathInfo_sgPWindow_file_key


def getUiInfo_sgPWindow_file_key():
    
    import sgBModel_fileAndPath
    locusCommPackagePrefsPath = getLocusCommPackagePrefsPath()
    return locusCommPackagePrefsPath + sgBModel_fileAndPath.uiInfo_sgPWindow_file_key


def getPathInfo_sgPWindow_file_sceneBakeInfo():
    
    import sgBModel_fileAndPath
    locusCommPackagePrefsPath = getLocusCommPackagePrefsPath()
    return locusCommPackagePrefsPath + sgBModel_fileAndPath.pathInfo_sgPWindow_file_sceneBakeInfo

    
def getPathInfo_sgPWindow_file_camera():
    
    import sgBModel_fileAndPath
    locusCommPackagePrefsPath = getLocusCommPackagePrefsPath()
    return locusCommPackagePrefsPath + sgBModel_fileAndPath.pathInfo_sgPWindow_file_camera




def getStandaloneExcutePyPath():
    standaloneExcutePyPath = getLocusCommPackagePrefsPath() + '/standaloneExcute.py'
    makeFile( standaloneExcutePyPath, False )
    return standaloneExcutePyPath



def getStandaloneRunCheckPath():
    default_standaloneRunCheckPath = getLocusCommPackagePrefsPath() + '/~standaloneRuningCheckFile.txt'
    return makeFile( default_standaloneRunCheckPath )




def getStandaloneLaunchFolders( folderNum ):
    
    folderBase = getLocusCommPackagePrefsPath() + '/stadaloneLaunchFolders'
    
    folderPaths =[]
    for i in range( folderNum ):
        folderPath = folderBase + '/folder%d' % i
        makeFolder( folderPath )
        folderPaths.append( folderPath )
    return folderPaths




def getStandaloneTempFiles( standaloneLaunchFolders ):
    
    tempFiles = []
    for folder in standaloneLaunchFolders:
        tempFilePath = folder+ '/tempFile.tmp'
        makeFile( tempFilePath, False )
        tempFiles.append( tempFilePath )
    return tempFiles
        



def getStandaloneTempFile( standaloneFolder ):
    
    tempFile = standaloneFolder + '/tempFile.tmp'
    makeFile( tempFile, False )
    return tempFile




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




def getDefaultScenePath( autoMakeFile=False ):
    defaultSceneFolderPath = getMayaDocPath() + '/projects/default/scenes'
    defaultSceneFilePath   = defaultSceneFolderPath + '/defaultScene.mb'
    
    if not autoMakeFile: return defaultSceneFilePath
    
    if os.path.exists( defaultSceneFilePath ):
        return defaultSceneFilePath

    makeFolder( defaultSceneFolderPath )

    standaloneRunCheckPath = getStandaloneRunCheckPath()

    insSL = sgBModel_string.StringLines()
    insSL.addLine( "import maya.standalone" )
    insSL.addLine( "maya.standalone.initialize( name='python' )" )
    insSL.addLine( "import maya.cmds as cmds" )
    insSL.addLine( "cmds.file( rename='%s' )" % defaultSceneFilePath )
    insSL.addLine( "cmds.file( save=1, f=1, options='v=0' )" )
    insSL.addLine( "import os" )
    insSL.addLine( "os.remove( '%s' )" % standaloneRunCheckPath )

    stadaloneExcutePyPath = getStandaloneExcutePyPath()

    f = open( stadaloneExcutePyPath, 'w' )
    f.write( insSL.getString() )
    f.close()

    import maya.mel as mel
    mel.eval( 'system( "start %s %s" )' %( getMayaPyPath(), stadaloneExcutePyPath ) )
    
    #wait for standalone exit
    while( os.path.exists( standaloneRunCheckPath ) ): continue
    
    return defaultSceneFilePath




def getDefaultCachePath():
    return getLocusCommPackagePrefsPath() + "/defaultCachePath"




def getDefaultSgMeshDataFolder():
    return getLocusCommPackagePrefsPath() + "/defaultSgMeshDatas" 




def getDefaultSgMeshDataPath():
    return getLocusCommPackagePrefsPath() + "/defaultSgMeshData.sgMeshData" 




def getDefaultSgUVDataPath():
    return getLocusCommPackagePrefsPath() + "/defaultSgUVData.sgUVData" 




def getDefaultSgKeyDataPath():
    return getLocusCommPackagePrefsPath() + "/defaultSgKeyFolder"




def getDefaultStandaloneFolder():
    standaloneFolder = getLocusCommPackagePrefsPath() + "/defaultStandaloneFolder"
    makeFolder( standaloneFolder )
    return standaloneFolder




def getCurrentStandaloneInfoFile():
    return getLocusCommPackagePrefsPath() + "/currentStandaloneInfo.txt"




def getCachebodyPathInScene():
    
    import maya.cmds as cmds
    refNodes = cmds.ls( type='reference' )

    cacheBodyPaths = []
    for refNode in refNodes:
        try:
            cmds.referenceQuery( refNode, namespace=1 )
        except: continue
        
        filePath = cmds.referenceQuery( refNode, filename=1 )
        folderPath = '/'.join( filePath.split( '/' )[:-1] )
        fileName = filePath.split( '/' )[-1].split( '{' )[0]
        onlyFileName = fileName.split( '.' )[0]
        
        if onlyFileName[-9:].lower() == 'cachebody':
            cacheBodyPaths.append( folderPath + '/' + fileName )
        else:
            for root, dirs, names in os.walk( folderPath ):
                for name in names:
                    if name.split( '.' )[0][-9:].lower() == 'cachebody':
                        cacheBodyPaths.append( folderPath + '/' + name )
                break
    return list( set( cacheBodyPaths ) )




def getPath_defaultSgMeshData():
    
    defaultFolderPath = getLocusCommPackagePrefsPath() + '/sgPWindow_file_mesh';
    defaultPath = getLocusCommPackagePrefsPath() + '/sgPWindow_file_mesh/defaultMeshData.sgMeshData'
    makeFolder( defaultFolderPath )
    return defaultPath




def getPath_defaultSgUVData():
    
    defaultFolderPath = getLocusCommPackagePrefsPath() + '/sgPWindow_file_mesh';
    defaultPath = getLocusCommPackagePrefsPath() + '/sgPWindow_file_mesh/defaultMeshData.sgUVData'
    makeFolder( defaultFolderPath )
    return defaultPath




def getPath_sgPWindow_file_mesh_info():
    
    infoPath = getLocusCommPackagePrefsPath() + '/sgPWindow_file_mesh/info.txt'
    makeFile( infoPath, False )
    return infoPath



def saveDefaultScenePath():
    
    import maya.cmds as cmds
    
    defaultScenePath = getDefaultScenePath()
    cmds.file( rename= defaultScenePath )
    cmds.file( save=1, f=1, options='v=0', typ='mayaBinary' )




def openDefaultScenePath():
    
    import maya.cmds as cmds
    
    defaultScenePath = getDefaultScenePath()
    cmds.file( defaultScenePath, f=1, options='v=0', ignoreVersion=1,
               typ='mayaBinary', o=1 )
    



def removeChildFiles( pathName ):
    pathName = pathName.replace( '\\', '/' )
    
    deleteDirTargets = []
    for root, dirs, names in os.walk( pathName ):
        for name in names:
            try:os.remove( root+'/'+name )
            except:pass
        if root == pathName: continue
    
    deleteDirTargets.reverse()
    for deleteDirTarget in deleteDirTargets:
        if os.path.exists( deleteDirTarget ):
            try:os.rmdir( deleteDirTarget )
            except:pass




def getMayaPyPath():
    
    mayapyPath = ''
    
    for path in sys.path:
        
        path = path.replace( '\\', '/' )
        
        if not os.path.isdir( path ):
            continue
        dirList = os.listdir( path )
        if 'CER' in dirList and 'Symbol' in dirList:
            mayapyPath = path+'/mayapy.exe'
    
    return mayapyPath



def get3dGroupPath():
    
    _3dGroupPath = ''
    
    for path in sys.path:
        path = path.replace( '\\', '/' )
        if path.find( '/packages/3dGroupTools' ) != -1:
            _3dGroupPath = path.split( '/packages/3dGroupTools' )[0]
            _3dGroupPath += '/packages/3dGroupTools'
            break
        if path.find( '/packages/3dGroup' ) != -1:
            _3dGroupPath = path.split( '/packages/3dGroup' )[0]
            _3dGroupPath += '/packages/3dGroup'
            break
    
    return _3dGroupPath




def getMayaPath():
    
    mayapyPath = ''
    
    for path in sys.path:
        
        path = path.replace( '\\', '/' )
        
        if not os.path.isdir( path ):
            continue
        dirList = os.listdir( path )
        if 'CER' in dirList and 'Symbol' in dirList:
            mayapyPath = path+'/maya.exe'
    
    return mayapyPath




def getFolderFromPath( filePath ):
    
    filePath = filePath.replace( '\\', '/' )
    return '/'.join( filePath.split( '/' )[:-1] )




def makeFolder( pathName, rename=False ):
    
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
    
    if folderExist and rename:
        pathName = checkSamePathAndRenamePath( pathName )
        os.mkdir( pathName )
        
    return pathName
        



def makeFile( pathName, autoRename=True ):
    
    pathName = pathName.replace( '\\', '/' )
    splitPaths = pathName.split( '/' )
    folderPath = '/'.join( splitPaths[:-1] )
    makeFolder( folderPath )
    
    if not os.path.exists( pathName ):
        f = open( pathName, 'w' )
        f.close()
    else:
        if autoRename:
            pathName = checkSamePathAndRenamePath( pathName )
            f = open( pathName, 'w' )
            f.close()
    
    return pathName




def getStartAndEndFrameFromXmlFile( xmlFilePath ):
    
    import xml.etree.ElementTree as ET
    
    root = ET.parse( xmlFilePath ).getroot()
    timeRange= root.find( 'time' ).attrib['Range']
    perFrame = root.find( 'cacheTimePerFrame' ).attrib['TimePerFrame']
    
    startFrame = 1
    endFrame   = 1
    perFrame = int( perFrame )
    
    startFrameAssigned = False
    
    for str1 in timeRange.split( '-' ):
        if not startFrameAssigned:
            if str1 == '':
                startFrame *= -1
                continue
            else:
                startFrame *= int( str1 )
                startFrameAssigned = True
                continue
        
        if str1 == '':
            endFrame *= -1
        else:
            endFrame *= int( str1 )
            
    startFrame /= perFrame
    endFrame /= perFrame
    
    return startFrame, endFrame




def importCache( mesh, xmlFilePath ):
    
    import sgBFunction_dag
    import maya.cmds as cmds
    
    mesh = sgBFunction_dag.getShape( mesh )
    
    xmlFileSplits = xmlFilePath.split( '/' )
    cachePath = '/'.join( xmlFileSplits[:-1] )
    cacheName = xmlFileSplits[-1].split( '.' )[0]
    
    deformer = cmds.createNode( 'historySwitch' )
    cacheNode = cmds.createNode( 'cacheFile' )
    
    cmds.connectAttr( cacheNode+'.outCacheData[0]', deformer+'.inPositions[0]')
    cmds.connectAttr( cacheNode+'.inRange',         deformer+'.playFromCache' )
    cmds.connectAttr( 'time1.outTime', cacheNode+'.time' )
    
    cmds.setAttr( cacheNode+'.cachePath', cachePath, type='string' )
    cmds.setAttr( cacheNode+'.cacheName', cacheName, type='string' )
    
    #print "xml filePath : ", xmlFilePath
    startFrame, endFrame = getStartAndEndFrameFromXmlFile( xmlFilePath )
    
    cmds.setAttr( cacheNode+'.startFrame',    -10000 )
    cmds.setAttr( cacheNode+'.sourceStart',   -10000 )
    cmds.setAttr( cacheNode+'.sourceEnd',     10000 )
    cmds.setAttr( cacheNode+'.originalStart', startFrame )
    cmds.setAttr( cacheNode+'.originalEnd',   endFrame )

    cmds.select( mesh )
    cmds.DeleteHistory()
    meshP = cmds.listRelatives( mesh, p=1, f=1 )[0]
    for shape in cmds.listRelatives( meshP, s=1, f=1 ):
        if cmds.getAttr( shape+'.io' ): cmds.delete( shape )
    
    print cmds.listRelatives( meshP, s=1 )
    
    origMesh = sgBFunction_dag.addIOShape( mesh )
    
    if cmds.nodeType( mesh ) == 'mesh':
        cmds.connectAttr( origMesh+'.worldMesh', deformer+'.undeformedGeometry[0]' )
        cmds.connectAttr( deformer+'.outputGeometry[0]', mesh+'.inMesh', f=1 )
    elif cmds.nodeType( mesh ) in [ 'nurbsCurve', 'nurbsSurface' ]:
        cmds.connectAttr( origMesh+'.worldSpace', deformer+'.undeformedGeometry[0]' )
        cmds.connectAttr( deformer+'.outputGeometry[0]', mesh+'.create', f=1 )



def checkSameFolderAndRenameFolder( path ):
    
    splitPath = path.replace( '\\', '/' ).split( '/' )
    upfolderPath = '/'.join( splitPath[:-1] )
    endFolder = splitPath[-1]
    sameFiles = glob.glob( upfolderPath +'/'+ endFolder + '*' )
    
    formatStr = '%02d'
    lastNum = 0
    for sameFile in sameFiles:
        sameFile = sameFile.replace( '\\', '/' )
        folderName = sameFile.split( '/' )[-1]
        olnyVersion = folderName.replace( endFolder, '' )
        versionLength = len( olnyVersion )
        if olnyVersion.isdigit():
            formatStr = '%0' + str( versionLength ) + 'd'
            lastNum = int( olnyVersion ) + 1
    
    return upfolderPath + '/' + endFolder + formatStr % lastNum






def checkSamePathAndRenamePath( path ):
    
    splitPath = path.replace( '\\', '/' ).split( '/' )
    
    currentFolderPath = '/'.join( splitPath[:-1] )
    fileName = splitPath[-1]
    try:
        onlyFileName, extension = fileName.split('.')
    except:
        onlyFileName = fileName
        extension = ''
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
        formatStr = onlyFileNameNumberCut+'*'
        if extension:
            formatStr += '.' + extension
    else:
        onlyFileNameNumberCut = onlyFileName
        formatStr = onlyFileName+'*'
        if extension:
            formatStr += '.' + extension
    
    sameFiles = glob.glob( currentFolderPath +'/'+ formatStr )
    compairName = (currentFolderPath+'/'+onlyFileNameNumberCut ).replace( '\\', '/' )
    checkSameFiles = []
    
    for sameFile in sameFiles:
        sameFile = sameFile.replace( '\\', '/' )
        if sameFile == compairName+'.'+extension or sameFile == compairName:
            checkSameFiles.append( sameFile )
            continue
        digit = sameFile[:-(extensionSize+1)].replace( compairName, '' )
        
        if digit.isdigit():
            checkSameFiles.append( sameFile )
    
    for fileName in checkSameFiles:
        print "exist path -", fileName

    checkSameFiles.sort()
    if checkSameFiles:
        if extension:
            onlyFileName  = checkSameFiles[-1][:-(extensionSize+1)]
            extension     = checkSameFiles[-1][-extensionSize:]
        else:
            onlyFileName  = checkSameFiles[-1]
        
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
            currentFilePath = formatStr % (int( indexStrs )+1)
        else:
            #print onlyFileName + '%02d' %( 1 )+'.'+extension
            currentFilePath = onlyFileName + '%02d' %( 1 )
        if extension:
            currentFilePath += '.' + extension
    else:
        currentFilePath = currentFolderPath+'/'+fileName
    
    return currentFilePath




def getSgKeyDatasInFolder( folderPath ):
    
    returnPaths = []
    
    for root, dirs, names in os.walk( folderPath ):
        for name in names:
            if name[-10:] != '.sgKeyData': continue
            returnPaths.append( root + '/' + name )
    
    return returnPaths




def getSceneBakeInfoPath():
    
    import maya.cmds as cmds
    currentFilePath = cmds.file( q=1, sceneName=1 )
    currentFileFolder = '/'.join( currentFilePath.split( '/' )[:-1] )
    fileName = currentFilePath.split( '/' )[-1]
    onlyFileName = fileName.split( '.' )[0]
    sceneInfoFileName = onlyFileName + '.sceneBakeInfo'
    
    return currentFileFolder + '/' + sceneInfoFileName




def copyFileToLocal( sourcePath, localDriver = 'D' ):
    
    import maya.cmds as cmds
    
    driverName = sourcePath.split( ':' )[0]
    
    if driverName.lower() == localDriver.lower():
        cmds.warning( "Path is Already Local" )
        return None
    
    targetPath = localDriver + sourcePath[1:]
    
    targetPath = makeFile( targetPath )
    shutil.copy2( sourcePath, targetPath)
    
    print "result path : %s" % targetPath
    
    return targetPath