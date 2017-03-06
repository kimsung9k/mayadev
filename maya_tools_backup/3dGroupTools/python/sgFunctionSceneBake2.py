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
import sgFunctionDag


def getExportBakeData( targetRefNode, selTargets ):

    selTargets = sgModelConvert.convertFullPathNames( selTargets )

    childTargets = cmds.listRelatives( selTargets, c=1, ad=1, type='transform', f=1 )
    if not childTargets: childTargets = []

    selTargets += childTargets

    exportTargets = []
    for selTarget in selTargets:
        if not cmds.referenceQuery( selTarget, inr=1 ): continue
        selTargetRefNode = cmds.referenceQuery( selTarget, rfn=1 )
        if selTargetRefNode != targetRefNode: continue
        exportTargets.append( selTarget )

    exportTargets = list( set( exportTargets ) )
    exportTargets.sort()

    bakeTargetList = []
    shapes = []

    for i in range( len( exportTargets ) ):
        target = exportTargets[i]
        
        targetMtx = cmds.getAttr( target+'.m' )
        targetPiv = cmds.xform( target, q=1, os=1, piv=1 )[:3]
        
        listAttrs = cmds.listAttr( target, k=1 )
        attrInfoList = []
        for attr in listAttrs:
            if cmds.getAttr( target+'.'+ attr, lock=1 ) and not cmds.listConnections( target+'.'+attr, s=1, d=0 ): continue

            attrValue = cmds.getAttr( target+'.'+ attr )
            if not type( attrValue ) in [ type( 123 ), type( 123.4 ), type( True ) ]: continue
            attrInfoList.append( [attr, sgModelDg.AnimCurveForBake( target+'.'+ attr )] )
                        
        bakeTargetList.append( [ target, targetMtx, targetPiv, attrInfoList ] )
        
        shape = sgModelDag.getShape( target )
        if shape: shapes.append( shape )
    
    deformedShapes = sgModelDag.getDeformedObjects( shapes )
    
    namespace = cmds.referenceQuery( targetRefNode, ns=1 )[1:].replace( ':', '_' )
    fileName  = cmds.referenceQuery( targetRefNode, filename=1 )
    
    return namespace, fileName, bakeTargetList, deformedShapes




def exportBakedData( selTargets, cachePath, startFrame, endFrame, offsetStart =-1, offsetEnd=1 ):

    defaultCachePath = sgModelFileAndPath.getDefaultCachePath()

    cachePath = cachePath.replace( '\\', '/' )
    defaultCachePath = defaultCachePath.replace( '\\', '/' )

    refNodes = []

    selTargetChildren = cmds.listRelatives( selTargets, c=1, ad=1, type='transform' )
    selTargetChildren += selTargets

    for selTarget in selTargetChildren:
        if not cmds.referenceQuery( selTarget, inr=1 ): continue
        refNode = cmds.referenceQuery( selTarget, rfn=1 )
        if refNode in refNodes: continue
        refNodes.append( refNode )

    namespaceArray = []
    fileNameArray  = []
    bakeTargetListArray = []
    deformedShapesArray = []
    for refNode in refNodes:
        namespace, fileName, bakeTargetList, deformedShapes = getExportBakeData( refNode, selTargets )

        namespaceArray.append( namespace )
        fileNameArray.append( fileName )
        bakeTargetListArray.append( bakeTargetList )
        deformedShapesArray += deformedShapes

    def setKeyframeBakeTargets( *args ):
        for k in range( len( refNodes ) ):
            bakeTargetList = bakeTargetListArray[ k ]
            
            for i in range( len( bakeTargetList ) ):
                for j in range( len( bakeTargetList[i][3] ) ):
                    attr = bakeTargetList[i][3][j][0]
                    info = bakeTargetList[i][3][j][1]
                    if not info.connectionExists: continue
                    '''
                    if cmds.currentTime( q=1 ) == 30:
                        print "setKeyframeTarget : ", bakeTargetList[i][0] + '.' + attr'''
                    info.appendKeyframeData()

    sgFunctionFileAndPath.makeFolder( cachePath )
    sgFunctionFileAndPath.makeFolder( defaultCachePath )
    if deformedShapesArray:
        callbackId = om.MEventMessage().addEventCallback( 'timeChanged', setKeyframeBakeTargets )
        cmds.select( deformedShapesArray )
        mel.eval( 'doCreateGeometryCache 6 { "3", "%s", "%s", "OneFile", "1", "%s","1","","0", "export", "0", "1", "1","0","0","mcc","0" };' %( startFrame + offsetStart, endFrame + offsetEnd, defaultCachePath ) )
        om.MMessage().removeCallback( callbackId )
    else:
        callbackId = om.MEventMessage().addEventCallback( 'timeChanged', setKeyframeBakeTargets )
        cmds.select( deformedShapes )
        for frame in range( startFrame+offsetStart, endFrame+offsetEnd + 1 ):
            cmds.currentTime( frame )
        om.MMessage().removeCallback( callbackId )

    animCurvesPaths = []
    bakeInfoPaths  = []
    for i in range( len( namespaceArray ) ):

        namespace = namespaceArray[i]
        fileName  = fileNameArray[i]
        bakeTargetList = bakeTargetListArray[i]
        bakeInfoPath  = cachePath + '/' + namespace + '.bakeInfo'
        assetInfoPath = cachePath + '/' + namespace + '.assetInfo'
        animCurvesPath = cachePath + '/' + namespace + '.ma'
        sgFunctionFileAndPath.makeFile( bakeInfoPath, False )
        sgFunctionFileAndPath.makeFile( assetInfoPath, False )

        animCurvesPaths.append( animCurvesPath )
        bakeInfoPaths.append( bakeInfoPath )

        f = open( bakeInfoPath, 'w' )
        cPickle.dump( bakeTargetList, f )
        f.close()

        f = open( assetInfoPath, 'w' )
        f.write( fileName )
        f.close()

        def makeAnimCurveScene():
            animCurves = []
            for k in range( len( bakeTargetList ) ):
                #print "bakeTrargetList : ", bakeTargetList[k]
                tr = bakeTargetList[k][0]
                
                for j in range( len( bakeTargetList[k][3] ) ):
                    attr = bakeTargetList[k][3][j][0]
                    info = bakeTargetList[k][3][j][1]
                    animCurve = info.createAnimCurve()
                    #animCurve = cmds.rename( animCurve, 'sceneBake_animCurve_for_%s' %( tr.split( '|' )[-1]+'_'+attr ) )
                    sgRigAttribute.addAttr( animCurve, ln='bakeTargetAttrName', dt='string' )
                    cmds.setAttr( animCurve+'.bakeTargetAttrName', tr+'.'+attr, type='string' )
                    animCurves.append( animCurve )
            
            if not animCurves: animCurves = [cmds.createNode( 'animCurveUU' )]
            cmds.select( animCurves )
            cmds.file( animCurvesPath, force=1, options="v=0;", typ="mayaAscii", es=1 )
            cmds.delete( animCurves )
        
        #makeAnimCurveScene()

    import sgFunctionStandalone
    standaloneInfoPath = 'C:/Users/skkim/Documents/maya/LocusCommPackagePrefs/sgStandalone/sgFunctionSceneBake2_makeScene.txt'
    sgFunctionStandalone.sgFunctionSceneBake2_makeScene( animCurvesPaths, bakeInfoPaths, standaloneInfoPath )

    timeUnit = cmds.currentUnit( q=1, time=1 )
    minTime  = startFrame
    maxTime  = endFrame
    
    sceneInfo = [ timeUnit, minTime, maxTime ]
    
    sceneInfoPath = cachePath + '/sceneInfo.sceneInfo'
    sgFunctionFileAndPath.makeFile( sceneInfoPath, False )
    
    f = open( sceneInfoPath, 'w' )
    cPickle.dump( sceneInfo, f )
    f.close()
    
    print "export : ", defaultCachePath, cachePath
    sgFunctionStandalone.moveFile( defaultCachePath, cachePath )
    print "------------- scene bake"





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
    
    sceneInfoPath = cachePath + '/sceneInfo.sceneInfo'
    f = open( sceneInfoPath, 'r' )
    sceneInfo = cPickle.load( f )
    f.close()
    
    timeUnit, minTime, maxTime = sceneInfo
    
    cmds.currentUnit( time=timeUnit )
    cmds.playbackOptions( minTime=minTime, maxTime=maxTime )
    cmds.currentTime( 1 )
    
    namespaces = []
    bakeInfoFiles = []
    assetInfoFiles = []
    animCurvesFiles = []
    for root, dirs, names in os.walk( cachePath ):
        for name in names:
            splits = name.split( '.' )
            assetInfoPath = root + '/' + name.replace( 'bakeInfo', 'assetInfo' )
            animCurvesPath = root + '/' + name.replace( 'bakeInfo', 'ma' )
            if splits[-1] == 'bakeInfo' and sgModelFileAndPath.isFile( assetInfoPath ) and sgModelFileAndPath.isFile( animCurvesPath ):
                namespaces.append( '.'.join( name.split('.')[:-1] ) )
                bakeInfoFiles.append( root + '/' + name )
                assetInfoFiles.append( assetInfoPath )
                animCurvesFiles.append( animCurvesPath )

    cacheBodyPathList = []
    for i in range( len( bakeInfoFiles ) ):
        bakeInfoFile = bakeInfoFiles[i]
        assetInfoFile = assetInfoFiles[i]
        animCurvesFile = animCurvesFiles[i]
        
        f = open( assetInfoFile, 'r' )
        assetPath = f.read()
        f.close()
        
        splits = assetPath.split( '.' )
        cacheBodyPath = '.'.join( splits[:-1] ) + '_cachebody.mb'
        
        if not sgModelFileAndPath.isFile( cacheBodyPath ): continue
        cmds.file( cacheBodyPath, i=True, type="mayaBinary", mergeNamespacesOnClash=False, ra=True, namespace = ':', rdn=1,
                   options= "v=0;",  pr=1, loadReferenceDepth="all" )
        cmds.file( animCurvesFile, r=True, type='mayaAscii', mergeNamespacesOnClash=False, namespace = '%s_anim' % namespaces[i],
                   options= "v=0;" )
        cacheBodyPathList.append( cacheBodyPath )
        
        f = open( bakeInfoFile, 'r' )
        bakeTargetList = cPickle.load( f )
        
        for j in range( len( bakeTargetList ) ):
            bakeObjectInfo = bakeTargetList[j]
            
            bakeObjectOrigName, matrix, piv, attrList = bakeObjectInfo
            
            localName = bakeObjectOrigName.split( '|' )[-1]
            localNameRemoveNamespace = localName.split( ':' )[-1]
            
            if not cmds.objExists( localNameRemoveNamespace ): continue
            shapeName = sgModelDag.getShape( localNameRemoveNamespace )
            
            if not shapeName: continue
            
            bakeObjectOrigName = bakeObjectOrigName.replace( ':', '_' )
            sgFunctionDag.makeTransform( bakeObjectOrigName )
            #print shapeName, '->', bakeObjectOrigName
            shapeName = cmds.parent( shapeName, bakeObjectOrigName, shape=1, r=1 )
            shapeLocalName = cmds.rename( shapeName, bakeObjectOrigName.split( '|' )[-1]+'Shape' )
            shapeCachePath = cachePath + '/' +  shapeLocalName + '.xml'
            if sgModelFileAndPath.isFile( shapeCachePath ):
                importCache( shapeLocalName, shapeCachePath )
            
            cmds.xform( bakeObjectOrigName, matrix=matrix )
            cmds.xform( bakeObjectOrigName, piv = piv )
            
            cmds.delete( localNameRemoveNamespace )
        
        try:cmds.delete( 'MOD' )
        except:pass

    for animCurve in cmds.ls( type='animCurve' ):
        if not cmds.attributeQuery( 'bakeTargetAttrName', node=animCurve, ex=1 ): continue
        targetAttr = cmds.getAttr( animCurve+'.bakeTargetAttrName' )
        if not cmds.ls( targetAttr.replace( ':', '_' ) ): continue
        if cmds.isConnected( animCurve+'.output', targetAttr.replace( ':', '_' ) ): continue
        cmds.connectAttr( animCurve+'.output', targetAttr.replace( ':', '_' ) )
    
    sameIndicesList = []
    for i in range( len( cacheBodyPathList )-1 ):
        for j in range( i+1, len( cacheBodyPathList ) ):
            if cacheBodyPathList[i] == cacheBodyPathList[j]:
                sameIndicesList.append( [i,j] )
    
    for i, j in sameIndicesList:
        first  = namespaces[i]+'_MOD'
        second = namespaces[j]+'_MOD'
        setMultiObjectShaderCombine( [ first, second ] )
        setMultiObjectOrigShapeCombine( [ first, second ] )
    
    
    


def setMultiObjectShaderCombine( MODs ):
    
    import sgRigConnection
    
    first =  MODs[0]
    others = MODs[1:]
    
    firstNamespace = first.replace( 'MOD', '' )
    
    otherNamespaces = []
    for other in others:
        otherNamespace = other.replace( 'MOD', '' )
        otherNamespaces.append( otherNamespace )
    
    children = cmds.listRelatives( first, c=1, ad=1, type='transform' )
    if not children: children = []
    children.append( first )
    
    for child in children:
        childShapes = cmds.listRelatives( child, s=1 )
        if not childShapes: continue
        
        for childShape in childShapes:
            if cmds.getAttr( childShape+'.io' ): continue
            
            for otherNamespace in otherNamespaces:
                otherShape = otherNamespace + childShape[ len( firstNamespace ) : ]
                sgRigConnection.copyShader( childShape, otherShape )



def setMultiObjectOrigShapeCombine( MODs ):
    
    import sgRigMesh
    
    first =  MODs[0]
    others = MODs[1:]
    
    if not first.find( 'MOD' ) == -1:
        sgRigMesh.setMultiObjectCombine( MODs )
    
    firstNamespace = first.replace( 'MOD', '' )
    
    otherNamespaces = []
    for other in others:
        otherNamespace = other.replace( 'MOD', '' )
        otherNamespaces.append( otherNamespace )
    
    children = cmds.listRelatives( first, c=1, ad=1, type='transform' )
    if not children: children = []
    children.append( first )
    
    for child in children:
        childShapes = cmds.listRelatives( child, s=1 )
        if not childShapes: continue
        
        otherChildren = []
        
        for otherNamespace in otherNamespaces:
            otherChildren.append( otherNamespace + child[ len( firstNamespace ) : ] )
        
        otherChildren.insert( 0, child )
        
        sgRigMesh.setMultiObjectCombine( otherChildren )



def duplicateAndMatrixConnect( targets, **options ):
    
    import sgModelData
    
    name = sgModelData.getValueFromDict( options, 'name' )
    
    if not type( targets ) in [ type( [] ), type( () ) ]:
        targets = [ targets ]
    for i in range( len( targets ) ):
        target = targets[i]
        
        dcmp = cmds.createNode( 'decomposeMatrix' )
        
        if not name:
            duObject = cmds.duplicate( target )[0]
        else:
            duObject = cmds.duplicate( target, n=name+'_%d' % i )[0]
        
        cmds.connectAttr( target+'.wm', dcmp+'.imat' )
        cmds.connectAttr( dcmp+'.otx', duObject+'.tx' )
        cmds.connectAttr( dcmp+'.oty', duObject+'.ty' )
        cmds.connectAttr( dcmp+'.otz', duObject+'.tz' )
        cmds.connectAttr( dcmp+'.orx', duObject+'.rx' )
        cmds.connectAttr( dcmp+'.ory', duObject+'.ry' )
        cmds.connectAttr( dcmp+'.orz', duObject+'.rz' )
        cmds.connectAttr( dcmp+'.osx', duObject+'.sx' )
        cmds.connectAttr( dcmp+'.osy', duObject+'.sy' )
        cmds.connectAttr( dcmp+'.osz', duObject+'.sz' )
        cmds.connectAttr( dcmp+'.oshx', duObject+'.shxy' )
        cmds.connectAttr( dcmp+'.oshy', duObject+'.shxz' )
        cmds.connectAttr( dcmp+'.oshz', duObject+'.shyz' )
        cmds.setAttr( duObject+'.shxy', k=1 )
        cmds.setAttr( duObject+'.shxz', k=1 )
        cmds.setAttr( duObject+'.shyz', k=1 )
        
        rPiv = cmds.getAttr( target+'.rotatePivot' )[0]
        sPiv = cmds.getAttr( target+'.scalePivot' )[0]
        
        cmds.setAttr( target+'.rotatePivot', *rPiv )
        cmds.setAttr( target+'.scalePivot', *sPiv )
        
        if cmds.listRelatives( duObject, p=1 ): duObject = cmds.parent( duObject, w=1 )
        trChildren =  cmds.listRelatives( duObject, c=1, type='transform', f=1 )
        if trChildren: cmds.delete( trChildren )
    '''
    transformBakePath = cachePath+'/transformBake.cPickle'
    f = open( transformBakePath, 'r' )
    importedData = cPickle.load( f )
    
    namespaces, filePaths, cacheBodyPaths, objectList, timeUnit = importedData
    
    cmds.currentUnit( time=timeUnit )
    
    for k in range( len( namespaces ) ):
        cacheBodyPath = cacheBodyPaths[k]
        print "cachebody path : ", cacheBodyPath
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
            importCache( targetMesh, xmlFilePath )'''