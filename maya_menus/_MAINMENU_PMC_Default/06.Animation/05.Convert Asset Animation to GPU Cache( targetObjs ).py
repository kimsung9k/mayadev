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


def convertAssetReferenceToGpu( selObj ):
    topTransforms = []
    visValues = []
    for tr in cmds.ls( tr=1 ):
        if cmds.listRelatives( tr, p=1 ): continue
        topTransforms.append( tr )
        visValues.append( cmds.getAttr( tr+'.v' ) )
        try:cmds.setAttr( tr+'.v', 0 )
        except:pass
    cmds.refresh()
    
    cmds.showHidden( selObj, a=1 )
    
    start = cmds.playbackOptions( q=1, min=1 )
    end = cmds.playbackOptions( q=1, max=1 )
    sceneName = cmds.file( q=1, sceneName=1 )
    folder = os.path.dirname( sceneName )
    onlyFileName = sceneName.split( '/' )[-1].split( '.' )[0]
    targetFolder = folder + '/' + onlyFileName + '_caches'
    resultPath = cmds.gpuCache( selObj, startTime=start, endTime=end, optimize=1, optimizationThreshold=40000, writeMaterials=1, dataFormat='ogawa', directory=targetFolder, fileName= selObj.replace( ':', '_' ) )
    
    for i in range( len( topTransforms ) ):
        try:cmds.setAttr( topTransforms[i] + '.v', visValues[i] )
        except:pass
    
    if resultPath:
        refNode = cmds.referenceQuery( selObj, rfn=1 )
        
        gpuTargets = cmds.listConnections( refNode + '.message', s=0, d=1, type='transform' )
        if not gpuTargets: gpuTargets = []
        for gpuTarget in gpuTargets:
            gpuShapes = cmds.listRelatives( gpuTarget, c=1, s=1 )
            if not gpuShapes: continue
            if cmds.nodeType( gpuShapes[0] ) == 'gpuCache':
                cmds.delete( gpuTarget )
        
        cmds.file( unloadReference = refNode )
        
        gpuObjName = selObj+'_gpu'
        gpuCacheNode = cmds.createNode( 'gpuCache' )
        gpuCacheObj = cmds.listRelatives( gpuCacheNode, p=1, f=1 )[0]
        gpuCacheObj = cmds.rename( gpuCacheObj, gpuObjName )
        gpuShapeName = cmds.listRelatives( gpuObjName, c=1,f=1 )[0]
        cmds.setAttr( gpuShapeName+'.cacheFileName', resultPath[0], type='string' )
        cmds.addAttr( gpuCacheObj, ln='refNode', at='message' )
        cmds.connectAttr( refNode + '.message', gpuCacheObj + '.refNode' )
    else:
        return False
    return True

sels = cmds.ls( sl=1 )
for sel in sels:
    if not convertAssetReferenceToGpu( sel ): break