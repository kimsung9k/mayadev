import maya.cmds as cmds
import maya.standalone
import os, glob
import datetime
import shutil
import model


def makePath( pathName ):
    pathName = pathName.replace( '\\', '/' )
    splitPaths = pathName.split( '/' )
    
    cuPath = splitPaths[0]
    
    for i in range( 1, len( splitPaths ) ):
        checkPath = cuPath+'/'+splitPaths[i]
        if not os.path.exists( checkPath ):
            os.chdir( cuPath )
            os.mkdir( splitPaths[i] )
        cuPath = checkPath
        
        
        
def makeFile( pathName ):
    pathName = pathName.replace( '\\', '/' )
    splitPaths = pathName.split( '/' )
    
    folderPath = '/'.join( splitPaths[:-1] )
    
    makePath( folderPath )
    
    if not os.path.exists( pathName ):
        f = open( pathName, 'w' )
        f.close()


def getInfoFromFile( filePath ):
    
    f = open( filePath, 'r' )
    data = f.read()
    f.close()
    
    animScenePath, camScenePath = data.split( '\n' )
    model.scenePath    = animScenePath.strip()
    model.bakeCamPath  = camScenePath.strip()


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



def createBakeCam( targetCams, start, end ):
    
    targetCamChildrenAttrs =[]
    duCamChildrenAttrs = []
    
    constObjects = []
    duCameras = []
    
    for targetCam in targetCams:
        targetCamParents = cmds.listRelatives( targetCam, p=1, f=1 )
        if targetCamParents:
            targetCamParent = targetCamParents[0]
            shapes = cmds.listRelatives( targetCamParent, s=1 )
            if shapes:
                if cmds.nodeType( shapes[0] ) == 'stereoRigCamera': continue

        constraintObject = cmds.createNode( 'transform' )
        cmds.loadPlugin( 'matrixNodes' )
        dcmp = cmds.createNode( 'decomposeMatrix' )
        cmds.connectAttr( targetCam+'.wm', dcmp+'.imat' )
        cmds.connectAttr( dcmp+'.ot',  constraintObject+'.t' )
        cmds.connectAttr( dcmp+'.or',  constraintObject+'.r' )
        cmds.connectAttr( dcmp+'.os',  constraintObject+'.s' )
        cmds.connectAttr( dcmp+'.osh', constraintObject+'.sh' )
        
        cons = cmds.listConnections( targetCam, s=1, d=0, c=1, p=1 )
        '''
        transformAttrs = []
        
        if cons:
            for con in cons[::2]:
                transformAttrs.append( con.split( '.' )[-1] )'''
        transformAttrs = ['tx','ty','tz','rx','ry','rz','sx','sy','sz']

        duCamera = cmds.duplicate( targetCam )[0]
        if cmds.listRelatives( duCamera, p=1 ):
            duCamera = cmds.parent( duCamera, w=1 )[0]
        duCameras.append( duCamera )
        constObjects.append( constraintObject )
        
        targetChildren = cmds.listRelatives( targetCam, c=1, ad=1, f=1 )
        duChildren     = cmds.listRelatives( duCamera, c=1, ad=1, f=1 )
        
        for i in range( len( targetChildren ) ):
            targetChild = targetChildren[i]
            duChild     = duChildren[i]
            
            cons = cmds.listConnections( targetChild, s=1, d=0, c=1, p=1 )
            if not cons: continue
            inputs = cons[::2]
            for j in range( len( inputs ) ):
                inputAttr = inputs[j]
                duChildAttr = duChild +'.'+ inputAttr.split( '.' )[-1]
                
                targetCamChildrenAttrs.append( inputAttr )
                duCamChildrenAttrs.append( duChildAttr )
        
        duCamShapes = cmds.listRelatives( duCamera, s=1, f=1 )
        if not duCamShapes: continue
        if cmds.nodeType( duCamShapes[0] ) == 'stereoRigCamera':
            leftRightCams = cmds.listRelatives( duCamera, c=1, type='transform', f=1 )
            cmds.connectAttr( duCamera+'.message', duCamera+'.centerCam' )
            try:
                leftCam = leftRightCams[0]
                rightCam = leftRightCams[1]
                cmds.connectAttr( leftCam+'.message', duCamera+'.leftCam' )
                cmds.connectAttr( rightCam+'.message', duCamera+'.rightCam' )
            except: pass
    
    for i in range( start, end+1 ):
        cmds.currentTime( i )
        for duCamera in duCameras:
            index = duCameras.index( duCamera )
            targetCam = constObjects[index]
            
            camMtx = cmds.getAttr( targetCam+'.wm' )
            cmds.xform( duCamera, ws=1, matrix=camMtx )
            
            for attr in transformAttrs:
                duCamAttr     = duCamera+'.'+attr
                try:
                    cmds.setKeyframe( duCamAttr )
                except: pass
        for j in range( len(targetCamChildrenAttrs) ):
            targetAttr = targetCamChildrenAttrs[j]
            duAttr     = duCamChildrenAttrs[j]
            try:
                lockPlug = cmds.connectionInfo( duAttr, gla=1 )
                try:
                    cmds.setAttr( lockPlug, e=1, lock=0 )
                except: pass
                cmds.setAttr( duAttr, cmds.getAttr( targetAttr ) )
                cmds.setKeyframe( duAttr )
            except: pass

    cmds.delete( constObjects )

    return duCameras



def getPlaybackInfomationInScene():
    
    minTime= cmds.playbackOptions( q=1, minTime=1 )
    maxTime= cmds.playbackOptions( q=1, maxTime=1 )
    unit   = cmds.currentUnit( q=1, time=1 )
    
    return minTime, maxTime, unit



def getBakeCamsInScene():
    
    sels = cmds.ls( type='camera', l=1 )

    bakeCams = []
    for sel in sels:
        if not cmds.getAttr( sel+'.orthographic' ):
            perspCam =  cmds.listRelatives( sel, p=1, f=1 )[0]
            
            if perspCam.find('persp') != -1:
                continue
            bakeCams.append( perspCam )
    
    return bakeCams



class NameInfo:

    def __init__(self, animPath ):
        
        animPath = animPath.replace( '\\', '/' )
        splits = animPath.split( '/' )
        self.sceneName = splits[-1]
        self.partName  = splits[-2]
        self.cutName   = splits[-3]
        self.shotName  = splits[-4]
        self.mainPath  = '/'.join( splits[:-2] )
    
    
    def getCamNameFromScene(self):
        
        minTime, maxTime, unit = getPlaybackInfomationInScene()
        
        unitDict = {'game':'15f','film': '24f', 'pal':'25f','ntsc':'30f',
                'show':'48f','palf':'50f','ntscf':'60f' }
        unitStr = unitDict[unit]
        
        minTime = str(int(minTime)).replace( '-', 'm' )
        maxTime = str(int(maxTime)).replace( '-', 'm' )
        
        return self.shotName+self.cutName+'_%s_%s_%s_bake' %( minTime, maxTime, unitStr )
    

def getBackupPath( path ):
    path = path.replace( '\\', '/' )
    nowTime = datetime.datetime.now()
    backupfolderName ='%04d%02d%02d' %( nowTime.year, nowTime.month, nowTime.day )
    backupPath = '/'.join( path.split('/')[:-1] )+'/backup/'+backupfolderName + '/'+path.split('/')[-1]
    return checkSamePathAndRenamePath( backupPath )
        
    

def createBakeCamFromScene( scenePath, bakeCamPath ):
    
    maya.standalone.initialize( name='python' )    
    cmds.file( scenePath, force=True, open=True )
    cmds.refresh()
    
    unknowns = cmds.ls( type='unknown' )

    for unknown in unknowns:
        cmds.lockNode( unknown, lock=0 )
        cmds.delete( unknown )
    
    
    minFrame, maxFrame, timeUnit = getPlaybackInfomationInScene()
    
    
    bakeCams = getBakeCamsInScene()
    "---------------- write info to file----------------"
    camNameStr = ''
    for camName in bakeCams:
        camName = camName.strip()
        camNameStr += camName +'\n'
    camNameStr = camNameStr[:-1]
    
    animationFolder = '/'.join( scenePath.replace( '\\', '/' ).split( '/' )[:-1] )
    infoPath = animationFolder + '/camList.txt'
    
    f = open( infoPath, 'w' )
    f.write( camNameStr )
    f.close()
    
    nameInfoInst = NameInfo( scenePath )
    
    camNameInScene  = nameInfoInst.getCamNameFromScene()
    
    duBakeCams = createBakeCam( bakeCams, minFrame, maxFrame )

    normalCams = []
    streoCams = []
    for duBakeCam in duBakeCams:
        duBakeCam = cmds.rename( duBakeCam, camNameInScene )
        duCamShapes = cmds.listRelatives( duBakeCam, s=1, f=1 )
        if not duCamShapes: continue
        if cmds.nodeType( duCamShapes[0] ) == 'stereoRigCamera':
            duBakeCam = cmds.rename( duBakeCam, camNameInScene+'_stereo' )
            streoCams.append( duBakeCam )
        else:
            normalCams.append( duBakeCam )
        
    cmds.select( d=1 )
    if normalCams:
        cmds.select( normalCams, add=1 )
    if streoCams:
        cmds.select( streoCams, add=1 )
    
    if cmds.ls( sl=1 ):
        cmds.file( bakeCamPath, f=1, options="v=0", typ='mayaBinary', pr=1, es=1 )
        print "Camera Bake Success"
    else:
        print "There is no Camera"

    "---------------- back up---------------------------"
    backupPath = getBackupPath( bakeCamPath )
    makeFile( backupPath )
    shutil.copy2( bakeCamPath, backupPath )
    '''
    try:
        cmds.loadPlugin( 'fbxmaya.mll' )
    except:
        print 'load FBX plugin Failed'
    
    try:
        bakeCamPath_fbx = '.'.join( bakeCamPath.split( '.' )[:-1] ).strip() + '.fbx'
        backupPath_fbx = getBackupPath( bakeCamPath_fbx )
        
        cmds.select( normalCams )
        print normalCams

        cmds.file( bakeCamPath_fbx, f=1, options='fbx', typ="FBX export", pr=1, es=1 )
        makeFile( backupPath_fbx )
        shutil.copy2( bakeCamPath_fbx, backupPath_fbx )

    except: print "FBX Export Failed"'''