import maya.cmds as cmds
import sgBModel_shader
import sgBFunction_dag
import pymel.core as pymelcore




def getReferencedShaderInfo( shadingEngine ):

    print "current shading engine : ", shadingEngine

    shaderInfo = sgBModel_shader.ReferencedShaderInfo()
    
    shader = cmds.listConnections( shadingEngine+'.surfaceShader', s=1, d=0 )
    displace = cmds.listConnections( shadingEngine+'.displacementShader', s=1, d=0 )
    volume = cmds.listConnections( shadingEngine+'.volumeShader', s=1, d=0 )
    
    if shader: shader = shader[0]
    if displace: displace = displace[0]
    if volume: volume = volume[0]
    
    if not shader: return None

    pmc_ShadingEngine = pymelcore.ls( shadingEngine )[0]
    
    targets = []
    for member in pmc_ShadingEngine.members():
        if 'indices' in dir( member ):
            targets.append( [member.node().name(), member.indices()] )
        else:
            targets.append( [member.node().name(), None] )

    if not cmds.reference( shader, q=1, inr=1 ):
        cmds.warning( "%s is not referenced" % shader )
        refPath = None
    else:
        refPath = cmds.reference( shader, q=1, f=1 )
    
    shaderInfo.referencePath   = refPath
    shaderInfo.shaderName      = shader.split( ':' )[-1]
    shaderInfo.displaceName    = displace
    shaderInfo.volumeName      = volume
    shaderInfo.assignedTargets = targets
    
    return shaderInfo



def getAllReferencedShaderInfoFromScene():
    
    shaderInfos = []
    
    for engine in cmds.ls( type='shadingEngine' ):
        shaderInfo = getReferencedShaderInfo( engine )
        if not shaderInfo: continue
        if not shaderInfo.referencePath: continue
        shaderInfos.append( shaderInfo )
    
    return shaderInfos




def getUserDefinedMeshAttrsInScene():
    
    import sgBFunction_attribute
    
    udAttrInfos = []
    for mesh in cmds.ls( type='mesh' ):
        attrInfos = sgBFunction_attribute.getUdAttrInfo( mesh )
        udAttrInfos.append( [mesh, attrInfos] )
    
    return udAttrInfos




def createShadingEngine( name ):
    
    linker = 'lightLinker1'
    partition = 'renderPartition'
    
    import maya.OpenMaya as om
    
    fnLinker = om.MFnDependencyNode( sgBFunction_dag.getMObject( linker ) )
    
    plugLink = fnLinker.findPlug( 'link' )
    
    linkIndex = plugLink.numElements()
    
    shadingEngine = cmds.shadingNode( 'shadingEngine', n=name, asUtility=1 )
    
    cmds.connectAttr( shadingEngine+'.message', linker+'.link[%d].object' % linkIndex, f=1 )
    cmds.connectAttr( shadingEngine+'.message', linker+'.shadowLink[%d].shadowObject' % linkIndex, f=1 )
    cmds.connectAttr( shadingEngine+'.partition', partition+'.sets[%d]' % linkIndex, f=1 )
    
    return shadingEngine



def getShadingEngine( shader ):
    
    if not cmds.objExists( shader ): return None
    shadingEngines = cmds.listConnections( shader+'.outColor', type='shadingEngine' )
    if shadingEngines: return shadingEngines[0]
    
    shadingEngine = createShadingEngine( shader+'SG' )
    cmds.connectAttr( shader+'.outColor', shadingEngine+'.surfaceShader' )
    
    return shadingEngine




def assignReferenceShader( infoPath, objectNamespace, shaderNamespace=None ):
    
    import cPickle
    import maya.OpenMaya as om
    import copy
    import sgBModel_data
    
    
    f = open( infoPath, 'r' )
    refShaderInfos, userDefinedMeshAttrInfos = cPickle.load( f )
    f.close()
    
    if not shaderNamespace: shaderNamespace = copy.copy( objectNamespace )
    
    objectNamespace = objectNamespace.replace( ':', '_' )
    shaderNamespace = shaderNamespace.replace( ':', '_' )
    
    objNs = copy.copy( objectNamespace )
    shaderNs = copy.copy( shaderNamespace )
    
    if objNs: objNs +='_'
    if shaderNs: shaderNs +=':'
    
    existingPaths = []
    for data in refShaderInfos:
        refPath = data.referencePath.replace( '\\', '/' )
        for ref in cmds.ls( type='reference' ):
            existingPath = cmds.referenceQuery( ref, filename=1 )
            if not existingPath in existingPaths: existingPaths.append( existingPath )

        if not refPath in existingPaths:
            if not shaderNamespace : cmds.file( refPath, r=1, ignoreVersion=True, gl=1, mergeNamespacesOnClash = False, namespace=':', options="v=0;" )
            else: cmds.file( refPath, r=1, ignoreVersion=True, gl=1, mergeNamespacesOnClash = False, namespace=shaderNamespace, options="v=0;" )
            print "referenced path : ", refPath
        
        shaderName = data.shaderName
        disName = data.displaceName
        volumeName = data.volumeName
        targets = data.assignedTargets
        
        shaderName = shaderNs + shaderName
        if disName:
            disName = shaderNs + disName
        if volumeName:
            volumeName = shaderNs + volumeName
        
        for shape, indices in targets:
            if not cmds.objExists( objNs+shape ): continue
            dagPath = sgBFunction_dag.getMDagPath( objNs+shape )
            
            if indices:
                intArr = om.MIntArray()
                intArr.setLength( len( indices ) )
                for i in range( len( indices ) ):
                    intArr[i] = indices[i]
                singleIndexedComp = om.MFnSingleIndexedComponent()
                mObject = singleIndexedComp.create( om.MFn.kMeshPolygonComponent )
                singleIndexedComp.addElements( intArr )

                cmds.select( d=1 )
                om.MGlobal.select( dagPath, mObject )
                cmds.hyperShade( assign=shaderName )
                om.MGlobal.unselect( dagPath, mObject )
            else:
                cmds.select( objNs+shape )
                cmds.hyperShade( assign=shaderName )
                cmds.select( d=1 )
        
        shadingEngine = getShadingEngine( shaderName )
        if disName: cmds.connectAttr( disName + '.displacement', shadingEngine + '.displacementShader' )
    
    import sgBFunction_attribute
    
    for mesh, udAttrInfo in userDefinedMeshAttrInfos:
        targetMesh = objNs.replace( ':', '_' ) + mesh
        if not cmds.objExists( targetMesh ): continue
        sgBFunction_attribute.setUdAttrInfo( udAttrInfo, targetMesh )
        



def standalone_makeReferenceShaderInfoFile( scenePath, targetPath, launchFolder=None, *args ):
    
    import maya.mel as mel
    import sgBFunction_fileAndPath
    import sys
    import cPickle
    
    if not launchFolder:
        launchFolder = sgBFunction_fileAndPath.getDefaultStandaloneFolder()
    
    sysPathInfo    = launchFolder + "/sysPathInfo.txt"
    scenePathInfo  = launchFolder + "/scenePathInfo.txt"
    targetPathInfo = launchFolder + "/targetPathInfo.txt"
    
    f = open( sysPathInfo, 'w' )
    cPickle.dump( sys.path, f )
    f.close()
    
    f = open( scenePathInfo, 'w' )
    f.write( scenePath )
    f.close()

    f = open( targetPathInfo, 'w' )
    f.write( targetPath )
    f.close()
    
    launchPy       = launchFolder + "/launch.py"
    doStandaloneCommand = """import maya.standalone
maya.standalone.initialize( name='python' )

import sys, cPickle

launchFolder = "%s"

sysPathInfo    = launchFolder + '/sysPathInfo.txt'
scenePathInfo  = launchFolder + '/scenePathInfo.txt'
targetPathInfo = launchFolder + '/targetPathInfo.txt'

f = open( sysPathInfo, 'r' )
sysPath = cPickle.load( f )
f.close()

for path in sysPath:
    if not path in sys.path:
        sys.path.append( path )

import sgBFunction_fileAndPath
import sgBFunction_shader
import sgBFunction_scene
import os, cPickle

if not os.path.exists( scenePathInfo ):
    cmds.warning( '%s is not exist path' ) 
else:
    f = open( scenePathInfo, 'r' )
    scenePath = f.read()
    f.close()
    
    f = open( targetPathInfo, 'r' )
    targetPath = f.read()
    f.close()
    
    print "scene path ---> ", scenePath 
    
    cmds.file( scenePath, f=1, o=1 )
    cmds.refresh()
    print "current file path : ", cmds.file( q=1, sceneName=1 )
    
    refInfos = sgBFunction_shader.getAllReferencedShaderInfoFromScene()
    userDefinedMeshAttrsInfo = sgBFunction_shader.getUserDefinedMeshAttrsInScene()
    sgBFunction_scene.makeUvFiles()
    
    f = open( targetPath, 'w' )
    cPickle.dump( [refInfos,userDefinedMeshAttrsInfo], f )
    f.close()

tempFile = sgBFunction_fileAndPath.getStandaloneTempFile( launchFolder )
os.remove( tempFile )
    """ %( launchFolder, scenePathInfo )

    f = open( launchPy, 'w' )
    f.write( doStandaloneCommand )
    f.close()

    mel.eval( 'system( "start %s %s" )' %( sgBFunction_fileAndPath.getMayaPyPath(), launchPy ) )



def makeSparateShader( targetObject ):

    import random
    import maya.OpenMaya as om
    import sgBFunction_dag
    import sgBFunction_base
    import copy
    
    sgBFunction_base.autoLoadPlugin( 'sgMesh' )
    
    cmds.sgGetMeshElementInfo( targetObject, set=1 )
    
    targetShape = sgBFunction_dag.getShape( targetObject )
    dagPathShape = sgBFunction_dag.getMDagPath( targetShape )
    
    numElement  = cmds.sgGetMeshElementInfo( ne=1 )
    numFaces    = cmds.sgGetMeshElementInfo( np=1 )
    faceIndices = cmds.sgGetMeshElementInfo( fi=1 )
    
    for i in range( numElement ):
        startFaceIndex = 0
        lastFaceIndex  = 0
        
        for j in range( i ):
            startFaceIndex += int( numFaces[j] )
        for j in range( i+1 ):
            lastFaceIndex += int( numFaces[j] )
    
        compArray = om.MIntArray()
        compArray.setLength( int( numFaces[i] ) )    
        for j in range( startFaceIndex, lastFaceIndex ):
            compArray.set( faceIndices[j], j-startFaceIndex )
    
        blinnShader = cmds.shadingNode( 'blinn', asShader=1 )
        blinnSet = cmds.sets( renderable=1, noSurfaceShader=1, empty=1, name='blinnSG' )
        cmds.connectAttr( blinnShader+'.outColor', blinnSet+'.surfaceShader', f=1 )
        
        colorR = random.uniform( 0, 1 )
        colorG = random.uniform( 0, 1 )
        colorB = random.uniform( 0, 1 )
        
        cmds.setAttr( blinnShader+'.color', colorR, colorG, colorB, type='double3' )
        
        singleComp = om.MFnSingleIndexedComponent()
        singleCompObj = singleComp.create( om.MFn.kMeshPolygonComponent )
        singleComp.addElements( compArray )
        
        selList = om.MSelectionList()
        selList.add( dagPathShape, singleCompObj )
        om.MGlobal.selectCommand( selList )
    
        cmds.sets( e=1, forceElement=blinnSet )




def assigneRandomShader( meshs ):
    
    import sgBFunction_dag
    import random
    
    meshs = sgBFunction_dag.getChildrenMeshExists( meshs )
    
    for i in range( len( meshs ) ):
        
        colorR = random.uniform( 0, 1 )
        colorG = random.uniform( 0, 1 )
        colorB = random.uniform( 0, 1 )
        
        blinnShader = cmds.shadingNode( 'blinn', asShader=1 )
        blinnSet = cmds.sets( renderable=1, noSurfaceShader=1, empty=1, name='blinnSG' )
        cmds.connectAttr( blinnShader+'.outColor', blinnSet+'.surfaceShader', f=1 )
        
        cmds.setAttr( blinnShader+'.color', colorR, colorG, colorB, type='double3' )
        cmds.select( meshs[i] )
        cmds.sets( e=1, forceElement=blinnSet )



def shadingAssignToFace( sourceGroup, targetGroup ):
    
    import sgBFunction_mesh
    
    sources = sgBFunction_dag.getChildrenMeshExists( sourceGroup )
    targets = sgBFunction_dag.getChildrenMeshExists( targetGroup )
    
    sourceMeshElementInfos = []
    targetMeshElementInfos = []
    
    for source in sources:
        sourceMeshElementInfos += sgBFunction_mesh.getMeshElementInfo( source )
    
    for target in targets:
        targetMeshElementInfos += sgBFunction_mesh.getMeshElementInfo( target )
    
    
    for targetMeshElementInfo in targetMeshElementInfos:
        
        targetNumVertices = targetMeshElementInfo.numVertices
        targetNumPolygons = targetMeshElementInfo.numPolygons
        targetBBC = targetMeshElementInfo.bbc
        
        for sourceMeshElementInfo in sourceMeshElementInfos:
            
            sourceNumVertices = sourceMeshElementInfo.numVertices
            sourceNumPolygons = sourceMeshElementInfo.numPolygons
            sourceBBC = sourceMeshElementInfo.bbc
            sourceShadingSet  = sourceMeshElementInfo.shadingSet
            
            if sourceBBC.distanceTo( targetBBC ) > 0.001: continue
            if sourceNumVertices != targetNumVertices: continue
            if sourceNumPolygons != targetNumPolygons: continue
            
            targetMeshElementInfo.selectFaces()
            print cmds.ls( sl=1 ), sourceShadingSet
            cmds.sets( e=1, forceElement = sourceShadingSet )