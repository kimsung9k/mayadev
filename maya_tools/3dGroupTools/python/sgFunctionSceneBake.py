import sgModelFileAndPath
import sgFunctionFileAndPath
import maya.cmds as cmds
import sgModelConvert
import sgRigAttribute
import sgModelData
import cPickle
import sgModelDg, sgModelDag
import os
import maya.mel as mel
import maya.OpenMaya as om
import maya.OpenMayaAnim as omAnim


def exportBakeData( targets, startFrame, endFrame, cachePath = '' ):
    
    transformBakePath = cachePath + '/transformBake.cPickle'
    
    targets = sgModelConvert.convertFullPathNames( targets )
    trObjs = cmds.listRelatives( targets, c=1, ad=1, type='transform', f=1 )
    if not trObjs: trObjs = []
    trObjs += targets
    
    trParents = []
    for trObj in trObjs:
        parents = sgModelDag.getParents( trObj )
        trParents += parents
    
    trs = list( set( trObjs + trParents ) )
    
    trs.sort()
    
    namespaces = []
    filePaths  = []
    cacheBodyPaths = []
    
    namespaceIndices = []
    for tr in trs:
        if not cmds.reference( tr, q=1, inr=1 ):
            namespaceIndices.append( None )
            continue
        
        namespace = cmds.referenceQuery( tr, ns=1 )
        filePath = cmds.reference( tr, q=1, filename =1 ).split( '{' )[0]
        
        cacheBodyPath = '.'.join( filePath.split( '.' )[:-1] ) + '_cachebody.' + filePath.split( '.' )[-1]

        if not os.path.exists( cacheBodyPath ):
            cacheBodyPath = ''

        if not namespace in namespaces:
            print "appended namespace :", namespace
            namespaces.append( namespace )
            filePaths.append( filePath )
            cacheBodyPaths.append( cacheBodyPath )
        
        namespaceIndex = namespaces.index( namespace )
        namespaceIndices.append( namespaceIndex )

    parentList = []
    objectList = []
    
    shapes = []
    for i in range( len( trs ) ):
        tr = trs[i]
        trParent = cmds.listRelatives( tr, p=1, f=1 )
        trMtx = cmds.getAttr( tr+'.m' )
        trPiv = cmds.xform( tr, q=1, os=1, piv=1 )[:3]
        
        listAttrs = cmds.listAttr( tr, k=1 )
        attrInfoList = []
        for attr in listAttrs:
            if not cmds.attributeQuery( attr, node=tr, ex=1 ): continue
            if cmds.listConnections( tr+'.'+ attr, s=1, d=0 ):
                animCurves = cmds.listConnections( tr+'.'+ attr, s=1, d=0, type='animCurve' )
                if animCurves:
                    attrInfoList.append( [attr, sgModelDg.AnimCurveData( animCurves[0] )] )
                else:
                    attrInfoList.append( [attr, []] )
            else:
                parentAttrs = cmds.attributeQuery( attr, node=tr, listParent = 1 )
                if parentAttrs:
                    if cmds.listConnections( tr+'.'+parentAttrs[0], s=1, d=0 ):
                        attrInfoList.append( [attr, []] )

        if trParent: trParent = trParent[0]
        if trParent in parentList:
            parentIndex= parentList.index( trParent )
        else:
            parentIndex = -1
        
        objectList.append( [ namespaceIndices[i], parentIndex, tr, trMtx, trPiv, attrInfoList ] )
        parentList.append( tr )
        
        shape = sgModelDag.getShape( tr )
        if shape: shapes.append( shape )
    
    timeUnit = cmds.currentUnit( q=1, time=1 )
    dataForExport = [ namespaces, filePaths, cacheBodyPaths, objectList, timeUnit ]

    deformedShapes = sgModelDag.getDeformedObjects( shapes )

    if deformedShapes:
        def setKeyframeBakeTargets( *args ):
            cuTime = cmds.currentTime( q=1 )
            
            for i in range( len(objectList) ):
                for j in range( len( objectList[i][5] ) ):
                    attr = objectList[i][5][j][0]
                    info = objectList[i][5][j][1]
                    if type( info ) != type( [] ): continue
                    tr = objectList[i][2]
                    value = cmds.getAttr( tr+'.' + attr )
                    objectList[i][5][j][1].append( [ cuTime, value ] )
        
        callbackId = om.MEventMessage().addEventCallback( 'timeChanged', setKeyframeBakeTargets )
        cmds.select( deformedShapes )
        sgFunctionFileAndPath.makeFolder( cachePath )
        mel.eval( 'doCreateGeometryCache 6 { "3", "%s", "%s", "OneFile", "1", "%s","1","","0", "export", "0", "1", "1","0","0","mcc","0" };' %( startFrame, endFrame, cachePath ) )
        om.MMessage().removeCallback( callbackId )

    transformBakePath = sgFunctionFileAndPath.makeFile( transformBakePath, False )
    f = open( transformBakePath, 'w' )
    cPickle.dump( dataForExport, f )
    f.close()
    
    return transformBakePath



def importCache( mesh, xmlFilePath ):
    
    mesh = sgModelDag.getShape( mesh )
    
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
    if not origMesh: return None
    
    cmds.connectAttr( origMesh+'.worldMesh', deformer+'.undeformedGeometry[0]' )
    cmds.connectAttr( deformer+'.outputGeometry[0]', mesh+'.inMesh', f=1 )



def importBakeData( cachePath ):
    
    transformBakePath = cachePath+'/transformBake.cPickle'
    f = open( transformBakePath, 'r' )
    importedData = cPickle.load( f )
    
    namespaces, filePaths, cacheBodyPaths, objectList, timeUnit = importedData
    
    cmds.currentUnit( time=timeUnit )
    
    for k in range( len( namespaces ) ):
        cacheBodyPath = cacheBodyPaths[k]
        #print "cachebody path : ", cacheBodyPath
        if not os.path.exists( cacheBodyPath ): continue
        cmds.file( cacheBodyPath, i=True, type="mayaBinary", mergeNamespacesOnClash=False, ra=True, namespace = 'cachebody%d' % k, 
                   options= "v=0;",  pr=1, loadReferenceDepth="all" )

    for i in range( len( objectList ) ):
        namespaceIndex, parentIndex, tr, trMtx, trPiv, attrInfoList = objectList[i]
        
        if namespaceIndex != None:
            origName = tr.split( '|' )[-1].replace( namespaces[ namespaceIndex ][1:]+':', '' )
            targetCacheBody = 'cachebody%d:%s' %( namespaceIndex , origName )
        else:
            origName = tr.split( '|' )[-1]
            targetCacheBody = origName
        
        if not cmds.objExists( targetCacheBody ):
            targetCacheBody = cmds.createNode( 'transform', n=targetCacheBody )

        if parentIndex != -1:
            try:targetCacheBody = cmds.parent( targetCacheBody, objectList[ parentIndex ][2] )[0]
            except:pass
        
        try:
            cmds.xform( targetCacheBody, os=1, matrix=trMtx )
            cmds.xform( targetCacheBody, os=1, piv=trPiv )
            objectList[i][2] = cmds.ls( targetCacheBody, l=1 )[0]
        except: continue
        
        for attrInfo in attrInfoList:
            attr, animCurveInfos = attrInfo
            
            if type( animCurveInfos ) == type( [] ):
                animCurve = cmds.createNode( 'animCurveTU', n=origName+'_'+attr )
                fnAnimCurve = omAnim.MFnAnimCurve( sgModelDg.getMObject( animCurve ) )
                
                time = om.MTime()
                for animCurveInfo in animCurveInfos:
                    timeValue, value = animCurveInfo
                    time.setValue( timeValue )
                    fnAnimCurve.addKey( time, value )
                #print animCurve, targetCacheBody, attr
                try:cmds.connectAttr( animCurve+'.output', targetCacheBody+'.'+attr, f=1 )
                except:pass
                    
            else:
                try:
                    animCurve = animCurveInfo.createAnimCurve()
                    cmds.connectAttr( animCurve+'.output', targetCacheBody + '.' + attr, f=1 )
                except:pass
        
        targetMesh = sgModelDag.getShape( targetCacheBody )
        if not targetMesh: continue
        if namespaceIndex == None: continue
        xmlFileName = namespaces[ namespaceIndex ][1:] + '_' + origName.replace( ':', '_' )+'Shape.xml'
        
        xmlFilePath = cachePath + '/' +  xmlFileName
        
        if os.path.exists( xmlFilePath ):
            print 'xml file path : ', xmlFilePath
            importCache( targetMesh, xmlFilePath )