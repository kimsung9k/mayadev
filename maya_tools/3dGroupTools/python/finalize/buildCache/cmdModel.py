import maya.OpenMaya as om
import maya.cmds as cmds
import maya.mel as mel
import model
import cPickle

import sgModelDag

import os

def makePath( pathName ):
    splitPaths = pathName.split( '/' )
    
    cuPath = splitPaths[0]
    
    for i in range( 1, len( splitPaths ) ):
        checkPath = cuPath+'/'+splitPaths[i]
        if not os.path.exists( checkPath ):
            os.chdir( cuPath )
            os.mkdir( splitPaths[i] )
        cuPath = checkPath
        
        
        
def makeFile( pathName ):
    splitPaths = pathName.split( '/' )
    
    folderPath = '/'.join( splitPaths[:-1] )
    
    makePath( folderPath )
    
    if not os.path.exists( pathName ):
        f = open( pathName, 'w' )
        f.close()


def getMObject( target ):
    selList = om.MSelectionList()
    selList.add( target )
    mObj = om.MObject()
    selList.getDependNode( 0, mObj )
    return mObj


def getPathFromFile( *args ):
    
    infoPath = model.CacheDataPathInfo._setInfoPath
    makeFile( infoPath )
    
    f = open( infoPath, 'r' )
    string = f.read()
    f.close()
    
    splitInfo = string.split( '\n' )
    
    if len( splitInfo ) < 2: return '',''
    
    return splitInfo[0].strip(), splitInfo[1].strip()



def getGeoSetAndGeometryFromFile( *args ):
    
    meshInfoPath = model.CacheDataPathInfo._meshInfoPath
    makeFile( meshInfoPath )
    
    f = open( meshInfoPath, 'r' )
    string = f.read()
    f.close()
    
    return string.strip()



def getTimeUnitFromFile( *args ):

    timeUnitPath = model.CacheDataPathInfo._timeUnitPath
    makeFile( timeUnitPath )
    
    f = open( timeUnitPath, 'r' )
    unitStr = f.read()
    f.close()
    
    return unitStr



def setPathToFile( animPathName, cachePathName, *args ):
    
    infoPath = model.CacheDataPathInfo._setInfoPath
    makeFile( infoPath )
    
    writeStr = animPathName + '\n\r' + cachePathName
    
    f = open( infoPath, 'w' )
    f.write( writeStr )
    f.close()


def setGeometryToFile( geoNames, *args ):
    
    meshInfoPath = model.CacheDataPathInfo._meshInfoPath
    makeFile( meshInfoPath )
    
    writeStr = geoNames
    
    f = open( meshInfoPath, 'w' )
    f.write( writeStr )
    f.close()



def buildCacheStandalone( cachePath, *args ):
    
    cachePath = cachePath.replace( '\\', '/' )
    mel.eval( 'system( "start %s %s" )' %( model.BuildCacheInfo._mayapyPath, model.BuildCacheInfo._launchPath ) )
    


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




def openFileBrowser( path, *args ):
    
    if not os.path.exists( path ):
        cmds.error( "%s Path is not exists" % path )
    
    path = path.replace( '\\', '/' )
    if os.path.isfile( path ):
        path = '/'.join( path.split( '/' )[:-1] )

    os.startfile( path )
    
    
    
def bulidMeshFromData( meshShapeNames=[] ):
    
    f = open( model.CacheDataPathInfo._setInfoPath, 'r' )
    paths = f.read()
    f.close()
    path = paths.split( '\n' )[1].strip().replace( '\\', '/' )+'/meshData.bat'
    if not os.path.exists( path ): return []
    
    f = open( path, 'r' )

    data = cPickle.load( f )
    
    f.close()
    
    mPointArr   = om.MPointArray()
    mCountArr   = om.MIntArray()
    mConnectArr = om.MIntArray()
    
    returnMeshShapeNames = []
    
    for i in range( len( data ) ):
        meshName, meshMatrix, numVtx, numPoly, lPointArr, lCountArr, lConnectArr = data[i]
        replaceMeshName = meshName.replace( ':', '_' )
        if meshShapeNames:
            if not replaceMeshName in meshShapeNames:
                continue
        meshTrName = meshName.replace( 'Shape', '' )
        
        if cmds.objExists( meshTrName ):
            returnMeshShapeNames.append( meshName )
            continue

        mPointArr.setLength( len( lPointArr ) )
        for j in range( mPointArr.length() ):
            mPoint = om.MPoint( *lPointArr[j] )
            mPointArr.set( mPoint, j )
        mCountArr.setLength( len( lCountArr ) )
        for j in range( mCountArr.length() ):
            mCountArr.set( lCountArr[j], j )
        mConnectArr.setLength( len( lConnectArr  ) )
        for j in range( mConnectArr.length() ):
            mConnectArr.set( lConnectArr[j], j )
        
        trMesh = cmds.createNode( 'transform', n=meshTrName )
        cmds.xform( trMesh, ws=1, matrix=meshMatrix )
        oTrMesh = getMObject( trMesh )
        
        fnMesh = om.MFnMesh()
        fnMesh.create( numVtx, numPoly, mPointArr, mCountArr, mConnectArr, oTrMesh )
        
        trMeshShapes = cmds.listRelatives( trMesh, s=1, f=1 )
        if not trMeshShapes: continue
        meshName = cmds.rename( trMeshShapes[0], meshName )
        returnMeshShapeNames.append( meshName )
    
    if not meshShapeNames: meshShapeNames = []
    for meshShapeName in meshShapeNames:
        if cmds.objExists( meshShapeName ):
            if not meshShapeName in returnMeshShapeNames:
                returnMeshShapeNames.append( meshShapeName )
    return returnMeshShapeNames
                
    


def buildCacheScene( meshShapeNames, cachePath ):
    
    cachePath = cachePath.replace( '\\', '/' )
    meshs = bulidMeshFromData( meshShapeNames )
    
    xmlFiles = []
    for root, dirs, names in os.walk( cachePath ):
        for name in names:
            if name[-4:].lower() == '.xml':
                xmlFiles.append( name )
    
    for mesh in meshs:
        xmlFileName = mesh.replace( ':', '_' )+'.xml'
        if not xmlFileName in xmlFiles: continue
        
        xmlFilePath = cachePath + '/' + xmlFileName
        
        deformer = cmds.createNode( 'historySwitch' )
        cacheNode = cmds.createNode( 'cacheFile' )
        
        cmds.connectAttr( cacheNode+'.outCacheData[0]', deformer+'.inPositions[0]')
        cmds.connectAttr( cacheNode+'.inRange',         deformer+'.playFromCache' )
        cmds.connectAttr( 'time1.outTime', cacheNode+'.time' )
        
        cmds.setAttr( cacheNode+'.cachePath', cachePath, type='string' )
        cmds.setAttr( cacheNode+'.cacheName', mesh.replace( ':', '_' ), type='string' )
        
        timeUnit = getTimeUnitFromFile()
        if timeUnit:
            cmds.currentUnit( time=timeUnit )
        
        startFrame, endFrame = getStartAndEndFrameFromXmlFile( xmlFilePath )
        cmds.playbackOptions( animationStartTime = startFrame, animationEndTime= endFrame,
                              minTime = startFrame+5, maxTime= endFrame-5 )
        
        cmds.setAttr( cacheNode+'.startFrame',    startFrame )
        cmds.setAttr( cacheNode+'.sourceStart',   startFrame )
        cmds.setAttr( cacheNode+'.sourceEnd',     endFrame )
        cmds.setAttr( cacheNode+'.originalStart', startFrame )
        cmds.setAttr( cacheNode+'.originalEnd',   endFrame )

        origMesh = sgModelDag.getOrigShape( mesh )
        
        cmds.connectAttr( origMesh+'.worldMesh', deformer+'.undeformedGeometry[0]' )
        cmds.connectAttr( deformer+'.outputGeometry[0]', mesh+'.inMesh', f=1 )