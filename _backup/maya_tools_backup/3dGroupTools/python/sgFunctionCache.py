import sgModelFileAndPath
import sgModelDag
import sgModelData
import sgFunctionDag
import sgModelConvert

import maya.cmds as cmds
import maya.mel as mel
import cPickle



def geometryBake( shapes, startFrame, endFrame, cachePath = '' ):
    
    if not cachePath: cachePath = sgModelFileAndPath.getDefaultCachePath() 
    
    shapes = sgModelDag.getDeformedObjects( shapes )
    if not shapes: return cachePath
    cmds.select( shapes )
    mel.eval( 'doCreateGeometryCache 6 { "3", "%s", "%s", "OneFile", "1", "%s","1","","0", "export", "0", "1", "1","0","0","mcc","0" };' %( startFrame, endFrame, cachePath ) )
    return cachePath



def transformBake( targets, startFrame, endFrame, filePath = '' ):
    
    if not filePath: filePath = sgModelFileAndPath.getDefaultCachePath()
    filePath += '/transformBake.pickle'
    
    bakeInfomation = {}
    
    bakeInfomation.update( {"currentTimeUnit" :cmds.currentUnit( q=1, time=1 )} )
    bakeInfomation.update( {"startFrame":startFrame} )
    bakeInfomation.update( {"endFrame"  :endFrame} )
    
    targets = list( set( targets ) )
    targets = sgModelConvert.convertFullPathNames( targets )

    for target in targets:
        bakeInfomation.update( { target : {} } )
        
    for target in targets:
        listAttrs = cmds.listAttr( target, k=1 )
        for attr in listAttrs:
            if cmds.listConnections( target+'.'+ attr, s=1, d=0 ):
                animCurves = cmds.listConnections( target+'.'+ attr, s=1, d=0, type='animCurve' )
                if animCurves:
                    bakeInfomation[ target ].update( { attr + '_animCurve' : animCurves[0] } )
                else:
                    bakeInfomation[ target ].update( { attr : [] } )
            else:
                parentAttrs = cmds.attributeQuery( attr, node=target, listParent = 1 )
                if parentAttrs:
                    if cmds.listConnections( target+'.'+parentAttrs[0], s=1, d=0 ):
                        bakeInfomation[ target ].update( { attr : [] } )
                
    
    cmds.undoInfo( swf=0 )
    for frame in range( startFrame, endFrame + 1 ):
        cmds.currentTime( frame )
        for target in targets:
            listAttrs = cmds.listAttr( target, k=1 )
            bakeInfomationTarget = bakeInfomation[ target ]
            for attr in listAttrs:
                try:
                    value = cmds.getAttr( target+'.'+attr )
                    bakeInfomationTarget[ attr ].append( value )
                except:pass
    cmds.undoInfo( swf=1 )
    f = open( filePath, 'w' )
    cPickle.dump( bakeInfomation, f )
    f.close()
    
    return filePath



def bake( topObjects=[], **options ):
    
    startFrame = sgModelData.getValueFromDict( options, 'startFrame' )
    endFrame   = sgModelData.getValueFromDict( options, 'endFrame' )
    cachePath   = sgModelData.getValueFromDict( options, 'cachePath' )
    transformBakeOn = sgModelData.getValueFromDict( options, 'transformBake' )
    geometryBakeOn  = sgModelData.getValueFromDict( options, 'geometryBake' )
    
    if not startFrame: startFrame = 1
    if not endFrame: endFrame = sgModelData.getCurrentUnitFrameRate()
    
    meshs = []
    if topObjects:
        topObjects = sgModelData.getArragnedList( topObjects )
        for topObj in topObjects:
            meshs += sgModelDag.getMeshsIsInVis( topObj )
    else:
        meshs += sgModelDag.getMeshsIsInVis()

    bakeTargets =[]
    for mesh in meshs:
        meshParent = cmds.listRelatives( mesh, p=1, f=1 )[0]
        bakeTargets += sgModelDag.getHierarchy( meshParent )
    
    print "geometryBakeOn : ", geometryBakeOn
    if geometryBakeOn:
        geometryBake( meshs, startFrame, endFrame, cachePath )
    if transformBakeOn:
        transformBake( bakeTargets, startFrame, endFrame, cachePath )
    
    return cachePath



def importCache( mesh, xmlFilePath ):
    
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
    startFrame, endFrame = sgModelData.getStartAndEndFrameFromXmlFile( xmlFilePath )
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



def importCacheAndBake( topObjects=[], **options ):
    
    cachePath = sgModelData.getValueFromDict( options, 'cachePath' )
    if not cachePath:
        print "cache path is not exists"
        return None
    
    bakeCacheFile = cachePath + '/transformBake.pickle'
    
    f = open( bakeCacheFile, 'r' )
    bakeInfomation = cPickle.load( f )
    f.close()
    
    currentTimeUnit = bakeInfomation['currentTimeUnit']
    startFrame      = bakeInfomation['startFrame']
    endFrame        = bakeInfomation['endFrame']
    
    cmds.currentUnit( time=currentTimeUnit )
    
    meshs = []
    if topObjects:
        topObjects = sgModelData.getArragnedList( topObjects )
        for topObj in topObjects:
            meshs += sgModelDag.getMeshsIsInVis( topObj )
    else:
        meshs += sgModelDag.getMeshsIsInVis()
    
    originalTargets = []
    bakeTargets = []
    for mesh in meshs:
        meshParent = cmds.listRelatives( mesh, p=1, f=1 )[0]
        bakeTargets += sgFunctionDag.duplicateHierarchy( meshParent )
    bakeTargets = list( set( bakeTargets ) )
    dagBakeTargets = sgModelConvert.convertMFnDagNodes( bakeTargets )
    
    renamedBakeTargets = []
    for dagBakeTarget in dagBakeTargets:
        bakeTarget = dagBakeTarget.fullPathName()
        listAttrs = cmds.listAttr( bakeTarget, k=1 )
        copyTarget = sgModelDag.getFullPathName( cmds.listConnections( bakeTarget+'.copyTarget' )[0] )
        
        for attr in listAttrs:
            keyAttr = bakeTarget+'.'+attr
            try:    values = bakeInfomation[copyTarget][attr]
            except:
                try:
                    animCurve = bakeInfomation[copyTarget][attr+'_animCurve']
                    bakedAnimCurve = cmds.duplicate( animCurve, n= animCurve+'_BAKE' )[0]
                    cmds.connectAttr( bakedAnimCurve+'.output', keyAttr )
                    continue
                except:continue
            for i in range( startFrame, endFrame+1 ):
                index = i - startFrame
                cmds.setKeyframe( keyAttr, time=i, value= values[index] )
        
        originalTargets.append( copyTarget )
        copyTarget = sgModelDag.getOriginalName( copyTarget )
        dagBakeTarget = cmds.rename( dagBakeTarget.fullPathName(), copyTarget.replace( ':', '_' )+'_BAKE' )
        renamedBakeTargets.append( dagBakeTarget )
    
    for mesh in meshs:

        if not sgModelDag.isDeformedObject( mesh ): continue
        
        meshOrigName = sgModelDag.getOriginalName( mesh )
        importCachePath = cachePath + '/' + meshOrigName.replace( ':', '_' ) + '.xml'
        
        meshParent = cmds.listRelatives( mesh, p=1, f=1 )[0]
        cons = cmds.listConnections( meshParent+'.message', p=1, c=1 )
        for con in cons[1::2]:
            split = con.split( '.' )
            if split[1].find( 'copyTarget' ) != -1:
                targetMesh = split[0]
                importCache( targetMesh, importCachePath )
                break
    
    for bakeTarget in renamedBakeTargets:
        cmds.deleteAttr( bakeTarget, attribute = 'copyTarget' )