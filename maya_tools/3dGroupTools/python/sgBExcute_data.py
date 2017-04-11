import maya.cmds as cmds
import sgBFunction_fileAndPath
import sgBFunction_base
import sgBFunction_dag
import maya.OpenMaya as om



def exportSgMeshData( targetMesh, filePath=None, *args ):

    sgBFunction_base.autoLoadPlugin( "sgBDataCmd" )
    if not filePath: filePath = sgBFunction_fileAndPath.getDefaultSgMeshDataPath()
    filePath = filePath.replace( '\\', '/' )
    folderPath = '/'.join( filePath.split( '/' )[:-1] )
    sgBFunction_fileAndPath.makeFolder( folderPath )
    cmds.sgBDataCmd_mesh( targetMesh, em=1, fp=filePath )
    print '"%s" export to "%s"' %( targetMesh, filePath )


def importSgMeshData( filePath=None, skipByName = False, *args ):
    
    sgBFunction_base.autoLoadPlugin( "sgBDataCmd" )
    if not filePath: filePath = sgBFunction_fileAndPath.getDefaultSgMeshDataPath()
    cmds.sgBDataCmd_mesh( im=1, fp=filePath )





def exportSgMeshDatas( targetMeshs, folderPath = None, typ='old', *args ):
    
    sgBFunction_base.autoLoadPlugin( "sgBDataCmd" )
    if not folderPath: folderPath = sgBFunction_fileAndPath.getDefaultSgMeshDataFolder()
    sgBFunction_fileAndPath.makeFolder( folderPath )
    if typ == 'old':
        print len( targetMeshs )
        for targetMesh in targetMeshs:
            targetMeshName = cmds.ls( targetMesh )
            if not targetMeshName: continue
            filePath = folderPath + '/' + targetMeshName[0].replace( ':', '_' ).replace( '|', '_' ) + '.sgBData_mesh'
            cmds.sgBDataCmd_mesh( targetMeshName[0], em=1, fp= filePath )
    else:
        cmds.sgBDataCmd_mesh( targetMeshs, em=1, fdp= folderPath )


def importSgMeshDatas( folderPath=None, importByMatrix = True, typ='old', *args ):
    
    sgBFunction_base.autoLoadPlugin( "sgBDataCmd" )
    if not folderPath: folderPath = sgBFunction_fileAndPath.getDefaultSgMeshDataPath()
    if typ == 'old':
        import os
        for root, dirs, names in os.walk( folderPath ):
            for name in names:
                extension = name.split( '.' )[-1]
                if extension != 'sgBData_mesh': continue
                cmds.sgBDataCmd_mesh( im=1, ibm=importByMatrix, fp=root + '/' + name )
    else: 
        cmds.sgBDataCmd_mesh( im=1, ibm=importByMatrix, fdp=folderPath )







def exportSgUVData( targetMesh, filePath=None, *args ):
    
    sgBFunction_base.autoLoadPlugin( "sgBDataCmd" )
    if not filePath: filePath = sgBFunction_fileAndPath.getDefaultSgUVDataPath()
    filePath = filePath.replace( '\\', '/' )
    folderPath = '/'.join( filePath.split( '/' )[:-1] )
    sgBFunction_fileAndPath.makeFolder( folderPath )
    cmds.sgBDataCmd_mesh( targetMesh, euv=1, fp=filePath )
    print '"%s" export to "%s"' %( targetMesh, filePath )




def importSgUVData( targetMesh, filePath=None, *args ):
    
    sgBFunction_base.autoLoadPlugin( "sgBDataCmd" )
    if not filePath: filePath = sgBFunction_fileAndPath.getDefaultSgUVDataPath()
    
    targetMesh     = sgBFunction_dag.getShape( targetMesh )
    targetMeshOrig = sgBFunction_dag.getOrigShape( targetMesh )
    targetMeshOrigSrcCon = cmds.listConnections( targetMeshOrig+'.inMesh', p=1, c=1, s=1, d=0 )
    if targetMeshOrigSrcCon:
        cmds.disconnectAttr( targetMeshOrigSrcCon[1], targetMeshOrigSrcCon[0] )
        cmds.warning( '"%s" to "%s" are disconnected.' %( targetMeshOrigSrcCon[1], targetMeshOrigSrcCon[0] ) )

    cmds.sgBDataCmd_mesh( targetMeshOrig, iuv=1, fp=filePath )
    print targetMeshOrig
    
    cons = cmds.listConnections( targetMesh+'.inMesh', s=1, d=0, p=1, c=1 )
    if not cons: return targetMeshOrig
    cmds.disconnectAttr( cons[1], cons[0] )
    cmds.refresh()
    cmds.connectAttr( cons[1], cons[0] )
    return targetMeshOrig






def exportSgKeyData( targetTransformNodes, startFrame, endFrame, step, folderPath=None, exportByMatrix=False, *args ):
    
    import sgBFunction_scene
    import copy
    
    if step < 0.05:
        cmds.error( "Step Must be larger then %.f." % step )
    
    sgBFunction_base.autoLoadPlugin( "sgBDataCmd" )
    if not folderPath: folderPath = sgBFunction_fileAndPath.getDefaultSgKeyDataPath()
    sgBFunction_fileAndPath.makeFolder( folderPath )
    sgBFunction_fileAndPath.removeChildFiles( folderPath )
    
    targetTransformNodeParents = []
    for transformNode in targetTransformNodes:
        targetTransformNodeParents += sgBFunction_dag.getParents( transformNode )
        targetTransformNodeParents.append( transformNode )
    targetTransformNodeParents = list( set( targetTransformNodeParents ) )
    
    sgBFunction_scene.exportTransformData( targetTransformNodeParents, folderPath )
    
    cmds.sgBDataCmd_key( targetTransformNodes, se=1, folderPath= folderPath, ebm=exportByMatrix )
    
    cuTime = copy.copy( startFrame )
    
    while cuTime <= endFrame+1:
        cmds.currentTime( cuTime )
        cmds.sgBDataCmd_key( write=1 )
        cuTime += step

    cmds.sgBDataCmd_key( ee=1 )





def importSgKeyData( folderPath, *args ):
    
    import sgBFunction_scene
    import os
    
    sgBFunction_base.autoLoadPlugin( "sgBDataCmd" )
    if not folderPath: folderPath = sgBFunction_fileAndPath.getDefaultSgKeyDataPath()
    sgBFunction_fileAndPath.makeFolder( folderPath )
    
    sgBFunction_scene.importTransformData( folderPath )
    
    for root, dirs, names in os.walk( folderPath ):
        for name in names:
            if name.split( '.' )[-1] != 'sgKeyData': continue
            cmds.sgBDataCmd_key( im=1, fp= root + '/' + name )






def exportCacheData( targetTransformNodes, startFrame, endFrame, step, folderPath=None, exportType='mcc', pointsSpace = 'world', *args ):
    
    import maya.mel as mel
    import sgBFunction_selection
    
    if step < 0.05:
        cmds.error( "Step Must be larger then %.f." % step )
    
    if not folderPath: folderPath = sgBFunction_fileAndPath.getDefaultCachePath()
    folderPath = folderPath.replace( '\\', '/' )
    sgBFunction_fileAndPath.makeFolder( folderPath )
    targetTransforms = sgBFunction_selection.getDeformedObjectsFromGroup( targetTransformNodes )
    cmds.select( targetTransforms )
    
    print "exportTargets :", targetTransformNodes
    print "startFrame :", startFrame
    print "endFrame :", endFrame
    print "path :", folderPath 
    print "cacheType : ", exportType
    print "pointsSpace :", pointsSpace
    print 'doCreateGeometryCache 6 { "3", "%s", "%s", "OneFile", "1", "%s","1","","0", "export", "0", "%s", "1","0","1","%s" ,"%s" };' %( startFrame, endFrame, folderPath, step, exportType, int(pointsSpace=='world') )
    
    mel.eval( 'doCreateGeometryCache 6 { "3", "%s", "%s", "OneFile", "1", "%s","1","","0", "export", "0", "%s", "1","0","1","%s" ,"%s" };' %( startFrame, endFrame, folderPath, step, exportType, int(pointsSpace=='world') ) )

    


def exportKeyAndCacheData( keyTransformNodes, cacheTransformNodes, keyFolderPath, cacheFolderPath, startFrame, endFrame, step, exportByMatrix=False, exportType='mcc', *args ):
    
    import maya.mel as mel
    import sgBFunction_selection
    import maya.OpenMaya as om
    import sgBFunction_scene
    
    sgBFunction_base.autoLoadPlugin( "sgBDataCmd" )
    
    keyFolderPath   = keyFolderPath.replace( '\\', '/' )
    cacheFolderPath = cacheFolderPath.replace( '\\', '/' )
    
    def exportKeyEachFrame( *args ):
        cmds.sgBDataCmd_key( write=1 )
    
    connectedTransforms = sgBFunction_selection.getTransformConnectedObjectsFromGroup( keyTransformNodes )
    deformedTransforms  = sgBFunction_selection.getDeformedObjectsFromGroup( cacheTransformNodes )

    if deformedTransforms and connectedTransforms:
        sgBFunction_fileAndPath.makeFolder( keyFolderPath )
        sgBFunction_fileAndPath.makeFolder( cacheFolderPath )
        
        targetTransformNodeParents = []
        for transformNode in connectedTransforms:
            targetTransformNodeParents += sgBFunction_dag.getParents( transformNode )
            targetTransformNodeParents.append( transformNode )
        targetTransformNodeParents = list( set( targetTransformNodeParents ) )
        
        sgBFunction_scene.exportTransformData( targetTransformNodeParents, keyFolderPath )
        
        cmds.sgBDataCmd_key( connectedTransforms, se=1, folderPath= keyFolderPath, ebm=exportByMatrix )
        callbackId = om.MEventMessage().addEventCallback( 'timeChanged', exportKeyEachFrame )
        cmds.select( deformedTransforms )
        mel.eval( 'doCreateGeometryCache 6 { "3", "%s", "%s", "OneFile", "1", "%s","1","","0", "export", "0", "%s", "1","0","0","%s","0" };' %( startFrame, endFrame, cacheFolderPath, step, exportType ) )
        om.MMessage().removeCallback( callbackId )
        cmds.sgBDataCmd_key( ee=1 )

    elif deformedTransforms and not connectedTransforms:
        exportCacheData( deformedTransforms, startFrame, endFrame, step, cacheFolderPath, exportType )
        
    elif not deformedTransforms and connectedTransforms:
        exportSgKeyData( connectedTransforms, startFrame, endFrame, step, keyFolderPath, exportByMatrix )




def importCacheData( folderPath ):
    
    import os
    
    for root, dirs, names in os.walk( folderPath ):
        for name in names:
            filePath = root + '/' + name
            if filePath[-4:].lower() != '.xml': continue
            
            meshName = name.split( '.' )[0]
            
            if not cmds.objExists( meshName ):
                cmds.warning( "%s is not exists" % meshName )
                continue
            
            if sgBFunction_dag.getNodeFromHistory( meshName, 'cacheFile' ): continue
            
            sgBFunction_fileAndPath.importCache( meshName, filePath )
            #print "*** %s's cache is imported ***" % meshName





def exportAlembicData( prefix, exportTargets, startFrame, endFrame, step, path ):
    
    import sgBFunction_base
    sgBFunction_base.autoLoadPlugin( 'AbcExport' )
    sgBFunction_base.autoLoadPlugin( 'AbcImport' )
    
    if prefix:
        prefix += '_'
    
    topTransforms = []
    visValues = []
    for tr in cmds.ls( tr=1 ):
        if cmds.listRelatives( tr, p=1 ): continue
        topTransforms.append( tr )
        visValues.append( cmds.getAttr( tr+'.v' ) )
        cmds.setAttr( tr+'.v', 0 )

    sgBFunction_fileAndPath.makeFolder( path )
    
    for target in exportTargets:
        target = cmds.ls( target, l=1 )[0]
        
        cmds.showHidden( target, a=1 )
        
        targetName = target.split( '|' )[-1]
        filePath = path + '/' + prefix + targetName.replace( ':', '_' ) + '_s' + str( step ).replace( '.', '_' ) + '.abc'
        cmds.AbcExport( target, j="-frameRange %s %s -step %s -writeVisibility -uvWrite -dataFormat ogawa -root %s -file %s" %( startFrame, endFrame, step, target, filePath ) )
        for tr in topTransforms:
            cmds.setAttr( tr+'.v', 0 )

    for i in range( len( topTransforms ) ):
        cmds.setAttr( topTransforms[i] + '.v', visValues[i] )




def importAlembicData( prefix, filePath ):
    
    import sgBFunction_base
    sgBFunction_base.autoLoadPlugin( 'AbcExport' )
    
    beforeTopNodes = sgBFunction_dag.getTopTransformNodes()
    cmds.AbcImport( filePath, mode='import' )
    afterTopNodes = sgBFunction_dag.getTopTransformNodes()
    
    fnTargets = []
    for afterTopNode in afterTopNodes:
        if afterTopNode in beforeTopNodes: continue
        
        children = cmds.listRelatives( afterTopNode, c=1, ad=1, f=1, type='transform' )
        if not children: children = []
        children.append( afterTopNode )
        for child in children:
            fnTarget = om.MFnTransform( sgBFunction_dag.getMDagPath( child ) )
            fnTargets.append( fnTarget )

    for target in fnTargets:
        targetName = target.name()
        fullName   = target.fullPathName()
        cmds.rename( fullName, prefix + targetName )




def standalone_makeReferenceShaderInfoFile( scenePath, targetPath, launchFolder=None, *args ):
    
    import maya.mel as mel
    
    if not launchFolder:
        launchFolder = sgBFunction_fileAndPath.getDefaultStandaloneFolder()
    
    launchPy       = launchFolder + "/launch.py"
    scenePathInfo  = launchFolder + "/scenePathInfo.txt"
    targetPathInfo = launchFolder + "/targetPathInfo.txt"
    
    doStandaloneCommand = """import maya.standalone
maya.standalone.initialize( name='python' )

import sgBFunction_fileAndPath
import sgBFunction_shader
import os, cPickle

launchFolder = "%s"

scenePathInfo  = launchFolder + '/scenePathInfo.txt'
targetPathInfo = launchFolder + '/targetPathInfo.txt'


if not os.path.exists( scenePathInfo ):
    cmds.warning( '%s is not exist path' ) 
else:
    f = open( scenePathInfo, 'r' )
    scenePath = f.read()
    f.close()
    
    f = open( targetPathInfo, 'r' )
    targetPath = f.read()
    f.close()
    
    cmds.file( scenePath, f=1, o=1 )
    cmds.refresh()
    print "current file path : ", cmds.file( q=1, sceneName=1 )
    
    refInfos = sgBFunction_shader.getAllReferencedShaderInfoFromScenes()
    
    sgBFunction_fileAndPath.makeFile( targetPath, False )
    
    f = open( targetPath, 'w' )
    cPickle.dump( refInfos, f )
    f.close()
    """ %( launchFolder, scenePathInfo )

    f = open( scenePathInfo, 'w' )
    f.write( scenePath )
    f.close()

    f = open( targetPathInfo, 'w' )
    f.write( targetPath )
    f.close()

    f = open( launchPy, 'w' )
    f.write( doStandaloneCommand )
    f.close()

    mel.eval( 'system( "start %s %s" )' %( sgBFunction_fileAndPath.getMayaPyPath(), launchPy ) )