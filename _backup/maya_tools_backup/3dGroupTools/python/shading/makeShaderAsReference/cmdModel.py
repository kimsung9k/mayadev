import maya.cmds as cmds
import maya.mel as mel
import shutil, os, glob
import functions
from functools import partial
import datetime


class model:
    mayaDocPath = functions.getMayaDocPath()
    openPathInfoFile = mayaDocPath+'/LocusCommPackagePrefs/makeShaderAsReference/openPath.txt'
    shaderPathInfoFile = mayaDocPath+'/LocusCommPackagePrefs/makeShaderAsReference/shaderPath.txt'
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




class PathToFile:
    
    @staticmethod
    def getOpenPathFromFile():
    
        functions.makeFile( model.openPathInfoFile )
        
        f = open( model.openPathInfoFile, 'r' )
        serverPath = f.read().strip()
        f.close()
        
        return serverPath


    @staticmethod
    def setOpenPathFromFile( path ):
        
        functions.makeFile( model.openPathInfoFile )
        
        f = open( model.openPathInfoFile, 'w' )
        f.write( path.replace( '\\',  '/' ) )
        f.close()
        
    
    @staticmethod
    def getShaderPathFromFile():
    
        functions.makeFile( model.shaderPathInfoFile )
        
        f = open( model.shaderPathInfoFile, 'r' )
        path = f.read().strip()
        f.close()
        
        return path
    
    
    @staticmethod
    def setShaderPathFromFile( path ):
        
        functions.makeFile( model.shaderPathInfoFile )
        
        f = open( model.shaderPathInfoFile, 'w' )
        f.write( path.replace( '\\',  '/' ) )
        f.close()



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



def copyFromServerAndOpen( path, *args ):
    
    splitPath = path.replace( '\\', '/' ).split( '/' )
    
    fileName = splitPath[-1]
    
    nowTime = datetime.datetime.now()
    folderName ='%04d%02d%02d' %( nowTime.year, nowTime.month, nowTime.day )
    
    currentFolderPath = model.defaultFileBrowserPath +"/"+ folderName
    functions.makePath( currentFolderPath )
    
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
    functions.makePath( backupPath )
    return backupPath, serverSplit[-1]
    


def backup( currentPath, serverPath, *args ):
    
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
    
    functions.makePath( '/'.join( currentPath.split( '/' )[:-1] ) )
    print cmds.file( q=1, sceneName=1 )
    cmds.file( rename=currentPath )
    cmds.file( save=1 )
    
    if currentPath.replace( '\\', '/' ).strip() == serverPath.replace( '\\', '/' ).strip(): return None
    shutil.copy2( currentPath, serverPath )



def copyToClipboard( text ):
    
    import subprocess
    
    cmd='echo '+text.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)


class shaderModel:

    connectedEngines = []
    selTargetList = []
    shaderNameList = []



def backupShaderAdReference( path, exportOnly = False, *args ):
    
    sels = cmds.listRelatives( cmds.ls( sl=1 ), c=1, ad=1, type='transform' )
    if not sels: sels = []
    sels += cmds.ls( sl=1 )
    
    connectedEngines = []
    for sel in sels:
        if cmds.nodeType( sel ) == 'transform':
            selShapes = cmds.listRelatives( sel, s=1, f=1 )
        else:
            selShapes = [ sel ]
        if not selShapes: continue
        directShapes = []
        for selShape in selShapes:
            if cmds.getAttr( selShape+'.io' ): continue
            directShapes.append( selShape )
        if not directShapes: continue
        
        engines = []
        for directShape in directShapes:
            shadingEngines = cmds.listConnections( directShape, type='shadingEngine' )
            if not shadingEngines:
                print '"%s" has no shader' % directShape
                continue
            engines += shadingEngines
        if not engines:
            print "engine is not exists : ", directShape 
            continue

        for engine in engines:
            if not engine in connectedEngines:
                connectedEngines.append( engine )
    
    functions.makeFile( path )
    if not os.path.isfile(path): return None
    
    selTargetList = []
    shaderNameList = []
    dismapList = []
    
    selItems = []
    
    for engine in connectedEngines:
        shaders = cmds.listConnections( engine+'.surfaceShader', s=1, d=0 )
        if not shaders: continue
        cmds.hyperShade( objects=engine )
        shaderNameList.append( shaders[0] )
        selTargetList.append( cmds.ls( sl=1 ) )
        selItems.append( shaders[0] )
        
        dismaps = cmds.listConnections( engine+'.displacementShader', s=1, d=0 )
        if dismaps:
            dismapList.append( dismaps[0] )
            selItems.append( dismaps[0] )
        else:
            dismapList.append( None )
    
    sceneName = cmds.file( q=1, sceneName=1 )
    backup( path, path )
    
    if selItems:
        print "select items: ", selItems
        cmds.select( selItems )
        cmds.file( path, f=1, op='v=0;', typ='mayaBinary', pr=1, es=1 )
        cmds.file( rename=sceneName )
    else:
        print "nothing is Selected"

    if exportOnly: return None

    for engine in connectedEngines:
        engineHists = cmds.listHistory( engine )
        for hist in engineHists:
            if hist == engine: continue
            if not cmds.objExists( hist ): continue
            if cmds.attributeQuery( 'matrix', node=hist, ex=1 ): continue
            if cmds.nodeType( hist ) == "groupId": continue
            try:
                cmds.delete( hist )
            except:pass
    
    cmds.file( path, r=1, gl=1, loadReferenceDepth='all', mergeNamespacesOnClash=True, namespace=":", options='v=0' )
    
    for i in range( len( selTargetList ) ):
        shaderName = shaderNameList[i]
        engine     = connectedEngines[i]
        dismap     = dismapList[i]
        try:
            cmds.connectAttr( shaderName+'.outColor', engine+'.surfaceShader' )
        except:
            print "Can not connect '%s' to '%s'" %( shaderName+'.outColor', engine+'.surfaceShader' )
        if not dismap: continue
        cmds.connectAttr( dismap+'.displacement', engine+'.displacementShader' )
        
    cmds.select( d=1 )