import maya.cmds as cmds
import maya.OpenMaya as om

def export_transformsBake( targets, fileName=None ):
    
    import sgBFunction_fileAndPath
    import sgBFunction_dag
    import cPickle

    if not fileName:
        scenePath = cmds.file( q=1, sceneName=1 )
        if scenePath:
            sceneFolder = '/'.join( scenePath.split( '/' )[:-1] )
            fileName = sceneFolder + '/transformsBake/bakeFile.txt'
        else:
            fileName = sgBFunction_fileAndPath.getMayaDocPath()+ '/transformsBake/bakeFile.txt'
    defaultExportTransformBakePath = sgBFunction_fileAndPath.getMayaDocPath() + '/defaultExportTransformsBake.txt'
    
    exTargets = []
    for target in targets:
        if cmds.nodeType( target ) != 'transform': continue
        cloneH = sgBFunction_dag.getParents( target )
        cloneH.append( cmds.ls( target, l=1 )[0] )
        exTargets += cloneH

    exTargets = list( set( exTargets ) )
    exTargets.sort()
    exTargetMtxs = [ [] for i in range( len( exTargets ) ) ]
    
    minFrame = cmds.playbackOptions( q=1, min=1 )
    maxFrame = cmds.playbackOptions( q=1, max=1 )
    unit     = cmds.currentUnit( q=1, time=1 )
    
    for t in range( int( minFrame ), int( maxFrame+1 ) ):
        cmds.currentTime( t )
        for i in range( len( exTargets ) ):
            exTargetMtx = cmds.getAttr( exTargets[i] + '.m' )
            exTargetMtxs[i].append( exTargetMtx )
    
    fileName = sgBFunction_fileAndPath.makeFile( fileName )
    f = open( fileName, 'w' )
    datas = [ unit, minFrame, maxFrame ]
    for i in range( len( exTargets ) ):
        extargetName = exTargets[i].replace( ':', '_' )
        datas.append( [ extargetName, exTargetMtxs[i] ] )
    cPickle.dump( datas, f )
    f.close()
    
    f = open( defaultExportTransformBakePath, 'w' )
    cPickle.dump( fileName, f )
    f.close()
    
    print "Export Path : ", fileName



def makeExportObjects( exportTargets ):
    
    import sgBFunction_dag
    import sgBFunction_connection
    
    exportMeshs = sgBFunction_dag.getChildrenMeshExists( exportTargets )

    for exportMesh in exportMeshs:
        
        exportMeshP = cmds.listRelatives( exportMesh, p=1, f=1 )[0]
        cloneP = sgBFunction_dag.makeCloneObject2( exportMeshP, [':', '_'], connectionOn=True )

        exportMeshName = exportMesh.split( '|' )[-1]
        exportMeshOrigShape = sgBFunction_dag.getOrigShape( exportMesh, True )
        meshShape = cmds.createNode( 'mesh' )
        cmds.connectAttr( exportMeshOrigShape + '.outMesh', meshShape + '.inMesh' )
        meshObj = cmds.listRelatives( meshShape, p=1 )[0]
        meshObj = cmds.rename( meshObj, exportMeshName.replace( ':', '_' ) )
        meshShape = sgBFunction_dag.getShape( meshObj )
        meshShape = cmds.rename( meshShape, exportMeshName.replace( ':', '_' ) + 'Shape' )
        pivotScale = cmds.getAttr( exportMesh + '.scalePivot' )[0]
        pivotRotate = cmds.getAttr( exportMesh + '.rotatePivot' )[0]
        pivotScaleTr = cmds.getAttr( exportMesh + '.scalePivotTranslate' )[0]
        pivotRotateTr = cmds.getAttr( exportMesh + '.rotatePivotTranslate' )[0]

        cmds.setAttr( meshObj + '.scalePivot', *pivotScale )
        cmds.setAttr( meshObj + '.rotatePivot', *pivotRotate )
        cmds.setAttr( meshObj + '.scalePivotTranslate', *pivotScaleTr )
        cmds.setAttr( meshObj + '.rotatePivotTranslate', *pivotRotateTr )

        cmds.parent( meshObj, cloneP )
        
        blendShape = cmds.blendShape( exportMesh, meshObj )[0]
        cmds.setAttr( blendShape + '.origin', 0 )
        cmds.setAttr( blendShape + '.w[0]', 1 )
        
        cmds.sets( meshObj, e=1, forceElement = 'initialShadingGroup' )