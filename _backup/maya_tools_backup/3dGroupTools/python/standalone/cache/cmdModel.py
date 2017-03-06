import maya.standalone
import maya.cmds as cmds
import maya.OpenMaya as om
import maya.mel as mel
import model
import cPickle
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




def setCacheInfoFromText( pathString, setAndGeoString ):
    
    f = open( pathString, "r" )
    fileInfo = f.read().split( '\n' )
    f.close()
    
    model.fromFile  = fileInfo[0].strip().replace( '\\', '/' )
    model.toFile    = fileInfo[1].strip().replace( '\\', '/' )
    
    f = open( setAndGeoString, "r" )
    geoInfo = f.read()
    f.close()
    
    model.targetGeos= geoInfo.strip().split(',')




def checkNameInNames( checkName, names ):
    
    for name in names:
        if checkName.find( name ) != -1:
            if not checkName.replace( name, '' ) in model.namespaceList:
                model.namespaceList.append( checkName.replace( name, '' ) )
            return True
    return False




def getPolyCreateInfo( meshName ):
    
    selList = om.MSelectionList()
    selList.add( meshName )
    path = om.MDagPath()
    selList.getDagPath( 0,path )
    
    fnMesh = om.MFnMesh( path )
    meshMatrix = path.inclusiveMatrix()
    meshMtxList = []
    
    for i in range( 4 ):
        for j in range( 4 ):
            meshMtxList.append( meshMatrix( i, j ) )
    
    numVtx  = fnMesh.numVertices()
    numPoly = fnMesh.numPolygons()
    mPointArr = om.MPointArray()
    mCountArr = om.MIntArray()
    mConnectArr = om.MIntArray()
    
    fnMesh.getPoints( mPointArr )
    
    mCountArr.setLength( numPoly )
    
    for i in range( numPoly ):
        mCountArr[i] = fnMesh.polygonVertexCount( i )
        
        numStr = cmds.polyInfo( meshName+'.f[%d]' % i, fv=1 )[0].split( ':' )[1].strip()
        
        eachStr = ''
        
        nums = []
        
        for char in numStr:
            if char == ' ':
                if eachStr.isdigit():
                    nums.append( int( eachStr ) )
                eachStr = ''
            else:
                eachStr += char
        if eachStr:
            nums.append( int( eachStr ) )
        
        for j in range( len( nums ) ):
            mConnectArr.append( nums[j] )
            
    lPointArr = []
    lCountArr = []
    lConnectArr = []
    
    for i in range( mPointArr.length() ):
        lPointArr.append( [mPointArr[i].x,mPointArr[i].y,mPointArr[i].z] )
    for i in range( mCountArr.length() ):
        lCountArr.append( mCountArr[i] )
    for i in range( mConnectArr.length() ):
        lConnectArr.append( mConnectArr[i] )

    return meshName, meshMtxList, numVtx, numPoly, lPointArr, lCountArr, lConnectArr



def checkIsInView( target ):
    
    if not cmds.getAttr( target+'.v' ):
        return False
    if cmds.getAttr( target+'.io' ):
        return False
    targetP = cmds.listRelatives( target, p=1, f=1 )
    if not targetP: return True
    
    return checkIsInView( targetP[0] )




def createCachePerGeometry( meshDataPath, startEnd=None ):
    
    maya.standalone.initialize( name='python' )
    
    cmds.file( model.fromFile, force=True, open=True )
    cmds.refresh()
    print "Open Success"
    
    if not startEnd:
        start = cmds.playbackOptions( q=1, minTime=1 ) - 5
        end   = cmds.playbackOptions( q=1, maxTime=1 ) + 5
    else:
        start = startEnd[0]
        end   = startEnd[1]

    objectSets = cmds.ls( type='objectSet' ) 
    
    targetNodes = []
    
    for objectSet in objectSets:
        if not checkNameInNames( objectSet, model.setNames ): continue
        
        targetNodes += cmds.sets( objectSet, q=1, nodesOnly=1 )
    
    newTargetNodes = []
    
    targetGeos = []
    
    for targetGeo in model.targetGeos:
        if targetGeo:
            targetGeos.append( targetGeo)
    
    if targetGeos:
        meshs = cmds.ls( type='mesh' )
        
        for mesh in meshs:
            meshP = cmds.listRelatives( mesh, p=1 )[0]
            if not checkNameInNames( meshP, model.targetGeos ): continue
            if meshP in targetNodes:
                if not meshP in newTargetNodes:
                    if checkIsInView( meshP ) and checkIsInView( mesh ):
                        newTargetNodes.append( meshP )
    else:
        for targetNode in targetNodes:
            targetNodeShape = cmds.listRelatives( targetNode, s=1, f=1 )[0]
            if checkIsInView( targetNodeShape ):
                newTargetNodes.append( targetNode )
    
    timeUnit = cmds.currentUnit( q=1, time=1 )
    makeFile( model.timeUnitPath )
    f = open( model.timeUnitPath, 'w' )
    f.write( timeUnit )
    f.close()
    
    meshDataPathFolder = '/'.join( meshDataPath.split( '/' )[:-1] )
    namespaceInfoTxt = meshDataPathFolder+'/namespaceInfo.txt'
    
    f = open( namespaceInfoTxt, 'w' )
    for namespace in model.namespaceList:
        f.write( namespace+'\n' )
    f.close()
    
    print "build Mesh Data......"  
    f = open( meshDataPath, 'w' )
    meshDataInfos = []
    for targetNode in newTargetNodes:
        targetNodeShape = cmds.listRelatives( targetNode, s=1 )[0]
        meshDataInfo = getPolyCreateInfo( targetNodeShape )
        meshDataInfos.append( meshDataInfo )
    cPickle.dump( meshDataInfos, f )
    f.close()
    print "build Mesh Data Success"
    
    cmds.select( newTargetNodes )
    cmds.refresh()
    
    print "Select Target Success"
    for targetNode in newTargetNodes:
        print "TargetNode : %s" % targetNode
        
    print start, end
    print model.toFile
    
    mel.eval( 'doCreateGeometryCache 6 { "3", "%s", "%s", "OneFile", "1", "%s","1","","0", "export", "0", "1", "1","0","0","mcc","0" };' %( start, end, model.toFile ) )
    print "Cache Export Success"