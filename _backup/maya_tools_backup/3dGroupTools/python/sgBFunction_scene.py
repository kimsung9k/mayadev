import maya.cmds as cmds



def selectMODs():
    
    transforms = cmds.ls( tr=1 )
    
    targetMODs = []
    for tr in transforms:
        if tr[-4:] == ':MOD' or tr == 'MOD':
            targetMODs.append( tr )
    
    cmds.select( targetMODs )




def selectSETs():

    transforms = cmds.ls( tr=1 )

    targetSETs = []
    for tr in transforms:
        if tr[-4:] == ':SET' or tr == 'SET':
            targetSETs.append( tr )

    cmds.select( targetSETs )




def deleteUnused():
    import maya.mel as mel
    mel.eval( 'hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes")' )



def removeUnknown():
    
    unknownNodes = cmds.ls( type='unknown' )
    
    for node in unknownNodes:
        try:
            cmds.lockNode( node, lock=0 )
            cmds.delete( node )
            print "%s node is deleted" % node
        except:pass


def deleteSgNodes():
    
    sgNodeTypeList = ['keepRoundDeformer', 'slidingDeformer_before',
              'slidingDeformer', 'blendCurve', 'getLowerestValue',
              'aimObjectMatrix', 'meshRivet', 'collisionJoint',
              'sgLockAngleMatrix', 
              'psdJointBase',
              'volumeCurvesOnSurface', 'clusterControledSurface',
              'splineMatrix', 'matrixFromPolygon', 'simulatedCurveControledSurface',
              'sgWobbleCurve', 'sgWobbleCurve2',
              'ikSmoothStretch', 'meshSnap',
              'epCurveNode', 'epBindNode',
              'wristAngle', 'shoulderOrient', 'squash', 'blendTwoMatrix',
              'blendTwoAngle', 'matrixToThreeByThree', 'matrixToFourByFour',
              'followMatrix', 'followDouble',
              'smartOrient', 'ikStretch', 'twoSideSlidingDistance',
              'multMatrixDecompose','blendTwoMatrixDecompose','verticalVector',
              'splineCurveInfo', 'distanceSeparator', 'controlerShape', 'footControl',
              'angleDriver',
              'blendAndFixedShape', 'inverseSkinCluster', 'vectorWeight',
              'dgTransform', 'retargetBlender', 'retargetOrientNode', 'retargetTransNode',
              'editMatrixByCurve', 'transRotateCombineMatrix', 'retargetLocator', 'meshShapeLocator',
              'timeControl',
              'sgMeshIntersect','sgBlendTwoMatrix','sgFollowMatrix','sgMatrixToThreeByThree',
              'sgMultMatrixDecompose']

    for sgNodeType in sgNodeTypeList:
        
        sgNodes = cmds.ls( type=sgNodeType )
        if sgNodes: cmds.delete( sgNodes )




def buildShadingInfoData( filePaths ):
    
    import os
    import sgBFunction_shader
    import sgBFunction_fileAndPath
    
    reload( sgBFunction_shader )
    reload( sgBFunction_fileAndPath )
    
    cachebodyPaths = []
    for filePath in filePaths:
        filePath = filePath.replace( '\\', '/' )
        folderPath = '/'.join( filePath.split( '/' )[:-1] )
        
        fileName = filePath.split( '/' )[-1]
        onlyFileName = fileName.split( '.' )[0]
        
        for root, dirs, names in os.walk( folderPath ):
            for name in names:
                try:onlyName, extension = name.split( '.' )
                except: continue
                if onlyName[-10:] == '_cachebody' and onlyName.find( onlyFileName ) != -1:
                    cachebodyPaths.append( root+'/'+name )
                    break
            break
    
    if not cachebodyPaths: return None
    
    launchFolders  = sgBFunction_fileAndPath.getStandaloneLaunchFolders( len( cachebodyPaths ) )
    standaloneRemoveFiles = sgBFunction_fileAndPath.getStandaloneTempFiles( launchFolders ) 
    
    shadingInfoPaths = []
    for i in range( len( cachebodyPaths ) ):
        cachebodyPath = cachebodyPaths[i]
        cachebodyFolder = '/'.join( cachebodyPath.split( '/' )[:-1] )
        cachebodyFile   = cachebodyPath.split( '/' )[-1]
        cachebodyFileName = cachebodyFile.split( '.' )[0]
        shadingInfoPath = cachebodyFolder + '/' + cachebodyFileName + '.shadingInfo'
        shadingInfoPaths.append( shadingInfoPath )
        
        if os.path.exists( shadingInfoPath ):
            os.remove( standaloneRemoveFiles[i] )
            continue

        sgBFunction_fileAndPath.makeFile( shadingInfoPath, False )
        sgBFunction_shader.standalone_makeReferenceShaderInfoFile( cachebodyPath, shadingInfoPath, launchFolders[i] )
    
    while( True ):
        exists = False
        for tempFile in standaloneRemoveFiles:
            if os.path.exists( tempFile ):
                exists = True; break
        #cmds.refresh()
        if not exists: break
    
    return shadingInfoPaths




def getSceneBakeInfo():
    
    unit = cmds.currentUnit( q=1, time=1 )
    minFrame = cmds.playbackOptions( q=1, min=1 )
    maxFrame = cmds.playbackOptions( q=1, max=1 )
    namespaces       = []
    filePaths = []
    
    refNodes = cmds.ls( type='reference' )
    for refNode in refNodes:
        try:
            namespace = cmds.referenceQuery( refNode, namespace=1 )[1:]
        except: continue
        
        filePath = cmds.referenceQuery( refNode, filename=1 )
        
        filePaths.append( filePath )
        namespaces.append( namespace )
        
    return unit, minFrame, maxFrame, namespaces, filePaths



def buildSceneBakeInfoFile( path=None ):
    
    import sgBFunction_fileAndPath
    import cPickle
    
    if not path: path = sgBFunction_fileAndPath.getSceneBakeInfoPath()
    info = getSceneBakeInfo()
    
    path = path.replace( '\\', '/' )
    folderPath = '/'.join( path.split( '/' )[:-1] )
    sgBFunction_fileAndPath.makeFolder( folderPath )
    
    f = open( path, 'w' )
    cPickle.dump( info, f )
    f.close()

    return path





def makeUvFiles():

    import sgBFunction_base
    sgBFunction_base.autoLoadPlugin( 'sgBDataCmd' )
    
    import sgBModel_fileAndPath
    import sgBFunction_fileAndPath
    
    scenePath = cmds.file( q=1, sceneName=1 )
    
    cmds.file( scenePath, f=1, options="v=0;", ignoreVersion=True )
    
    folderPath = '/'.join( scenePath.split( '/' )[:-1] )
    uvPath = folderPath + '/' + sgBModel_fileAndPath.cacheBodyUvFolderName
    
    sgBFunction_fileAndPath.makeFolder( uvPath )
    
    meshs = cmds.ls( type='mesh' )
    for mesh in meshs:
        if cmds.getAttr( mesh+'.io' ): continue
        meshName = mesh.replace( '|', '_' ).replace( ':', '_' )
        uvFilePath = uvPath + '/' + meshName + '.sgBData_uvs'
        cmds.sgBDataCmd_mesh( mesh, euv=1, filePath = uvFilePath )




def standalone_makeUvFiles( scenePath, launchFolder=None, *args ):
    
    import maya.mel as mel
    import sgBFunction_fileAndPath
    import sys
    import cPickle
    
    if not launchFolder:
        launchFolder = sgBFunction_fileAndPath.getDefaultStandaloneFolder() + '/thread'
    
    launchFolder = sgBFunction_fileAndPath.makeFolder( launchFolder, True )
    
    sysPathInfo    = launchFolder + "/sysPathInfo.txt"
    scenePathInfo  = launchFolder + "/scenePathInfo.txt"
    
    f = open( sysPathInfo, 'w' )
    cPickle.dump( sys.path, f )
    f.close()
    
    f = open( scenePathInfo, 'w' )
    f.write( scenePath )
    f.close()
    
    launchPy       = launchFolder + "/launch.py"
    doStandaloneCommand = """import maya.standalone
maya.standalone.initialize( name='python' )

import sys, cPickle

launchFolder = "%s"

sysPathInfo    = launchFolder + '/sysPathInfo.txt'
scenePathInfo  = launchFolder + '/scenePathInfo.txt'

f = open( sysPathInfo, 'r' )
sysPath = cPickle.load( f )
f.close()

for path in sysPath:
    if not path in sys.path:
        sys.path.append( path )

import sgBFunction_fileAndPath
import sgBFunction_scene
import os, cPickle

if not os.path.exists( scenePathInfo ):
    cmds.warning( '%s is not exist path' ) 
else:
    f = open( scenePathInfo, 'r' )
    scenePath = f.read()
    f.close()
    
    print "scene path ---> ", scenePath 
    
    cmds.file( scenePath, f=1, o=1 )
    cmds.refresh()
    print "current file path : ", cmds.file( q=1, sceneName=1 )
    
    sgBFunction_scene.makeUvFiles()

tempFile = sgBFunction_fileAndPath.deletePathHierarchy( launchFolder )
os.rmdir( launchFolder )
    """ %( launchFolder, scenePathInfo )

    f = open( launchPy, 'w' )
    f.write( doStandaloneCommand )
    f.close()

    mel.eval( 'system( "start %s %s" )' %( sgBFunction_fileAndPath.getMayaPyPath(), launchPy ) )




def setSceneFromSceneBakeInfo( sceneBakeInfoPath, importCachebody = False ):
    
    import os
    import cPickle
    import sgBFunction_mesh
    import sgBFunction_shader
    import sgBModel_fileAndPath
    
    f = open( sceneBakeInfoPath, 'r' )
    shaderInfo = cPickle.load( f )
    f.close()
    
    unit, minFrame, maxFrame, namespaces, filePaths = shaderInfo
    
    cmds.currentUnit( time= unit )
    cmds.playbackOptions( min=minFrame, max=maxFrame )
    
    """
    buildShadingInfoData( filePaths )
    
    for i in range( len( filePaths ) ):
        folderPath = '/'.join( filePaths[i].split( '/' )[:-1] ) + '/' + sgBModel_fileAndPath.cacheBodyUvFolderName
        namespace = namespaces[i]
        if not namespace:
            sgBFunction_mesh.assignUvFiles( folderPath , '' )
        else:
            sgBFunction_mesh.assignUvFiles( folderPath, namespace +'_' )

    for i in range( len( namespaces ) ):
        filePath = filePaths[i]
        folderPath = '/'.join( filePath.split( '/' )[:-1] )
        fileName   = filePath.split( '/' )[-1]
        onlyFileName = fileName.split( '.' )[0]
        if onlyFileName.lower().find( 'cachebody' ) == -1: onlyFileName += '_cachebody'
        shadingInfoFile = folderPath + '/' + onlyFileName + '.shadingInfo'
        if not os.path.exists( shadingInfoFile ): continue
        sgBFunction_shader.assignReferenceShader( shadingInfoFile, namespaces[i] )
    """
    if importCachebody:
        for i in range( len( namespaces ) ):
            namespace = namespaces[i]
            filePath = filePaths[i]
            folderPath = '/'.join( filePath.split( '/' )[:-1] )
            fileName   = filePath.split( '/' )[-1]
            onlyFileNameAndExtension = fileName.split( '.' )
            if onlyFileNameAndExtension[0].lower().find( 'cachebody' ) == -1: onlyFileNameAndExtension[0] += '_cachebody'
            cachebodyPath = folderPath + '/' + '.'.join( onlyFileNameAndExtension )
            print "cachebodyPath : ", cachebodyPath
            if not os.path.exists( cachebodyPath ): continue
            cmds.file( cachebodyPath, i=1, ignoreVersion=True, ra=True, mergeNamespacesOnClash = False, rpr=namespace, options="v=0;", pr=1 )
        
        



def doBake( cameraPath, minFrame, maxFrame, maya=True, mb = True, fbx=True ):
    
    import os, time, socket
    
    import sgBFunction_dag
    import sgBFunction_base
    
    sgBFunction_base.autoLoadPlugin( 'fbxmaya' )
    removeUnknown()
    
    cameraPath = cameraPath.replace( '\\', '/' )

    ##_ex_Atts = ["renderable"]
    _attrs = ["horizontalFilmAperture", "verticalFilmAperture", "focalLength", "lensSqueezeRatio", "fStop", "focusDistance", "shutterAngle", "centerOfInterest", "nearClipPlane", "farClipPlane",
    "filmFit", "filmFitOffset", "horizontalFilmOffset", "verticalFilmOffset", "shakeEnabled", "horizontalShake", "verticalShake", "shakeOverscanEnabled", "shakeOverscan", "preScale",
    "filmTranslateH", "filmTranslateV", "horizontalRollPivot", "verticalRollPivot", "filmRollValue", "filmRollOrder", "postScale", "depthOfField", "focusRegionScale"]

    if not (maya or fbx):
        print "AAA"
        return
    if not cmds.ls(sl=1):
        print "BBB"
        return
    sels = cmds.ls(sl=1)
    src    = None
    src_sh = None
    for sel in sels:
        selShape = sgBFunction_dag.getShape( sel )
        if cmds.nodeType( selShape ) == 'camera':
            src = sel
            src_sh = selShape

    if not src_sh:
        cmds.error( "No Camera Selected")

    if not (cmds.nodeType(src_sh) == "camera"):
        return
    trg = cmds.camera()[0]
    
    unit = cmds.currentUnit( q=1, time=1 )
    unitDict = { 'game':15, 'film':24, 'pal':25, 'ntsc':30, 'show':48, 'palf':50, 'ntscf':60 }
    camName = cameraPath.split( '/' )[-1]
    camName += '_%d_%d_%df_bake' %( minFrame, maxFrame, unitDict[ unit ] )
    
    trg = cmds.rename( trg, camName )
    trg_sh = cmds.listRelatives(trg, s=True, f=True)[0]
    
    ##for at in cmds.listAttr(src_sh):
    for at in _attrs:
    ##if at in _ex_Atts: continue
        try:
            ##cmds.setAttr("%s.%s" % (src_sh, at), k=1)
            cmds.setAttr("%s.%s" % (trg_sh, at), k=1)
            cmds.setAttr("%s.%s" % (trg_sh, at), cmds.getAttr("%s.%s" % (src_sh, at)))
            cmds.connectAttr("%s.%s" % (src_sh, at), "%s.%s" % (trg_sh, at), f=1)
        except:
            pass
    
    cmds.pointConstraint(src, trg, offset=[0,0,0], weight=1)
    cmds.orientConstraint(src, trg, offset=[0,0,0], weight=1)
    cmds.setAttr(trg + ".rotateAxisX", cmds.getAttr(src + ".rotateAxisX"))
    cmds.setAttr(trg + ".rotateAxisY", cmds.getAttr(src + ".rotateAxisY"))
    cmds.setAttr(trg + ".rotateAxisZ", cmds.getAttr(src + ".rotateAxisZ"))
    
    cmds.refresh(suspend=True)
    try:
        cmds.bakeResults(trg, sm=True, t=(minFrame, maxFrame), sb=1, dic=True, pok=True, sac=False, removeBakedAttributeFromLayer=False, bakeOnOverrideLayer=False, cp=False, s=True)
    finally:
        cmds.refresh(suspend=False)
        cmds.refresh()
        cmds.delete(trg, constraints=1)
    try:
        a = cmds.listConnections(src_sh, s=0, d=1, c=1, p=1, scn=1, sh=1)[::2]
        b = cmds.listConnections(src_sh, s=0, d=1, c=1, p=1, scn=1, sh=1)[1::2]
        for i in range(len(a)):
            cmds.disconnectAttr(a[i], b[i])
    except:
        pass
    
    outFN = cameraPath

    rntN = cmds.fileDialog2(fm=0, dir=outFN)
    if not rntN:
        return
    rntFN = os.path.splitext(rntN[0])[0]
    if maya: 
        cmds.file(rntFN, force=1, options="v=0;", typ="mayaAscii", pr=1, es=1)
    if mb: 
        cmds.file(rntFN, force=1, options="v=0;", typ="mayaBinary", pr=1, es=1)
    if fbx:
        cmds.file(rntFN, force=1, options="v=0;", typ="FBX export", pr=1, es=1)
    
    #print rnt
    ##setClipboardData(rnt)
    
    def showExportCamera():
        if cmds.window("exportCamera", ex=1):
            cmds.deleteUI("exportCamera")
            cmds.window("exportCamera")
            cmds.columnLayout( adjustableColumn=True )
            cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 100), (2, 100)] )
            mayaCB = cmds.checkBox(l="Maya", v=True)
            fbxCB = cmds.checkBox(l="FBX", v=True)
            cmds.setParent("..")
            #cmds.button(l="Tear off", c=lambda x:tearOffPanel())
            cmds.button(l="Export", c=lambda x:doBake(cmds.checkBox(mayaCB, q=1, v=1), cmds.checkBox(fbxCB, q=1, v=1)))
            cmds.showWindow()

    showExportCamera()




def turtleClear( *args ):
    cmds.unloadPlugin( 'Turtle.mll', f=1 )

    if cmds.objExists("TurtleDefaultBakeLayer") :
        cmds.lockNode( "TurtleDefaultBakeLayer" , l = False)
        cmds.delete( 'TurtleDefaultBakeLayer' )
    if cmds.objExists("TurtleBakeLayerManager") :
        cmds.lockNode( "TurtleBakeLayerManager" , l = False)
        cmds.delete( 'TurtleBakeLayerManager' )
    if cmds.objExists("TurtleRenderOptions") :
        cmds.lockNode( "TurtleRenderOptions" , l = False)
        cmds.delete( 'TurtleRenderOptions' )
    if cmds.objExists("TurtleUIOptions") :
        cmds.lockNode( "TurtleUIOptions" , l = False)
        cmds.delete( 'TurtleUIOptions' )
        




def cleanMeshInScene( *args ):
    
    import sgBFunction_mesh
    meshs = cmds.ls( type='mesh' )
    
    meshObjs = []
    for mesh in meshs:
        if cmds.getAttr( mesh+'.io' ): continue
        meshP = cmds.listRelatives( mesh, p=1, f=1 )[0]
        if meshP in meshObjs: continue
        meshObjs.append( meshP ) 
    
    for meshObj in meshObjs:
        sgBFunction_mesh.cleanMesh( meshObj )


        

mc_turtleClear = """import sgBFunction_scene
sgBFunction_scene.turtleClear()"""



mc_cleanMesh = """import sgBFunction_scene
sgBFunction_scene.cleanMeshInScene()"""



def exportTransformData( targets, folderPath ):
    
    import cPickle
    
    import sgBFunction_fileAndPath
    
    sgBFunction_fileAndPath.makeFolder( folderPath )
    
    for target in targets:

        filePath = folderPath + '/' + target.split( '|' )[-1].replace( ':', '_' )+'.transformData'
        sgBFunction_fileAndPath.makeFile( filePath )
        
        tx = cmds.getAttr( target+'.tx' )
        ty = cmds.getAttr( target+'.ty' )
        tz = cmds.getAttr( target+'.tz' )
        
        rx = cmds.getAttr( target+'.rx' )
        ry = cmds.getAttr( target+'.ry' )
        rz = cmds.getAttr( target+'.rz' )
        
        sx = cmds.getAttr( target+'.sx' )
        sy = cmds.getAttr( target+'.sy' )
        sz = cmds.getAttr( target+'.sz' )
        
        values = [target, tx, ty, tz, rx, ry, rz, sx, sy, sz]
        
        f = open( filePath, 'w' )
        cPickle.dump( values, f )
        f.close()



def importTransformData( folderPath ):

    import os
    import cPickle
    
    for root, dirs, names in os.walk( folderPath ):
        for name in names:
            nameSplits = name.split( '.' )
            if not nameSplits[-1] == 'transformData': continue
            objName = name.split( '.' )[0].replace( ':', '_' )
            filePath = root + '/' + name
            
            print "filePath : ", filePath
            
            try:
                f = open( filePath, 'r' )
                target, tx, ty, tz, rx, ry, rz, sx, sy, sz = cPickle.load( f )
                f.close()
            except:continue
            
            target = target.replace( ':', '_' )
            if not cmds.objExists( target ): continue
            cmds.setAttr( target+'.tx', tx )
            cmds.setAttr( target+'.ty', ty )
            cmds.setAttr( target+'.tz', tz )
            cmds.setAttr( target+'.rx', rx )
            cmds.setAttr( target+'.ry', ry )
            cmds.setAttr( target+'.rz', rz )
            cmds.setAttr( target+'.sx', sx )
            cmds.setAttr( target+'.sy', sy )
            cmds.setAttr( target+'.sz', sz )
                
        break



def getCutNumber():
    
    scenePath = cmds.file( q=1, sceneName=1 )

    splits = scenePath.split( '/' )
    
    try:
        sceneIndex = splits.index( 'scenes' )
    except:
        try:sceneIndex = splits.index( 'scene' )
        except:
            return 'abc'
    
    if len( splits ) == sceneIndex+1:
        return ''
    return splits[ sceneIndex + 1 ]



def hideTopTransforms():
    
    import sgBFunction_dag
    import sgBModel_data
    
    topTransforms = sgBFunction_dag.getTopTransformNodes()
    sgBModel_data.topTransformAndVisValues = []
    for topTransform in topTransforms:
        value = cmds.getAttr( topTransform+'.v' )
        sgBModel_data.topTransformAndVisValues.append( [topTransform, value] )
        cmds.setAttr( topTransform+'.v', 0 )



def showTopTransforms():
    
    import sgBModel_data
    
    for topTransform, visValue in sgBModel_data.topTransformAndVisValues:
        cmds.setAttr( topTransform+'.v', visValue )
        


def getCurrentCam():
    panel = cmds.getPanel( wf=1 )
    if cmds.getPanel( to=panel ) != "modelPanel": return None
    return cmds.modelEditor( panel, q=1, camera=1 )



def getCurrentPanel():
    return cmds.getPanel( wf=1 )
    