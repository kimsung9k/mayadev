from sgModules import sgcommands

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
    makeFolder( targetFolder )
    resultPath = targetFolder + '/' + selObj.replace( ':', '_' ).replace( '|', '_' ) + '.abc'
    print "info : ", start, end, selObj, resultPath
    cmds.AbcExport( j="-frameRange %d %d -uvWrite -writeVisibility -eulerFilter -dataFormat ogawa -root %s -file %s" %( start, end, selObj, resultPath ) )

    
    for i in range( len( topTransforms ) ):
        try:cmds.setAttr( topTransforms[i] + '.v', visValues[i] )
        except:pass
    
    try:
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
        if not cmds.pluginInfo( 'gpuCache', q=1, l=1 ):
            cmds.loadPlugin( 'gpuCache' )
        gpuCacheNode = cmds.createNode( 'gpuCache' )        
        gpuCacheObj = cmds.listRelatives( gpuCacheNode, p=1, f=1 )[0]        
        gpuCacheObj = cmds.rename( gpuCacheObj, gpuObjName )        
        gpuShapeName = cmds.listRelatives( gpuObjName, c=1,f=1 )[0]        
        cmds.setAttr( gpuShapeName+'.cacheFileName', resultPath, type='string' )        
        cmds.addAttr( gpuCacheObj, ln='refNode', at='message' )
        cmds.connectAttr( refNode + '.message', gpuCacheObj + '.refNode' )
    except:
        try:
            topTransforms = []
            visValues = []
            
            for i in range( len( topTransforms ) ):
                cmds.setAttr( topTransforms[i] + '.v', visValues[i] )
            
            cmds.file( lr = refNode )
        except:
            pass
        return False
    return True


sels = cmds.ls( sl=1 )
targets = []
for sel in sels:
    target = sgcommands.getParentNameOf( sel, 'SET' )
    if not target: continue
    targets.append( target )

targets = list( set( targets ) )

for target in targets:
    if not convertAssetReferenceToGpu( target ):
        cmds.warning( "failed to export '%s'" % target )
