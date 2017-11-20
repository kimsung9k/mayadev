import pymel.core
from sgMaya import sgCmds
from maya import cmds, mel, OpenMaya
import os

def BG_ASM_SET():
    trs = pymel.core.ls( tr=1 )
    
    topNodes = []
    for tr in trs:
        if tr.getParent(): continue
        children = tr.listRelatives( c=1 )
        proxyExists = False
        for child in children:
            if child[0] == 'V':
                proxyExists = True
                break
        if proxyExists: topNodes.append( tr )
    
    targets = []
    
    pymel.core.makeIdentity( topNodes, apply=1, t=1, r=1, s=1, n=0, pn=1 )
    
    for topNode in topNodes:
        children = topNode.listRelatives( c=1 )
        for child in children:
            if child.find( 'V3' ) != -1: 
                targets.append( topNode )
                continue
            pymel.core.delete( child )
    
    for target in targets:
        children = target.listRelatives( c=1, ad=1 )
        for child in children:
            pymel.core.showHidden( child, a=1 )
        
        reducedObj = sgCmds.combineMultiShapes( target )
        pymel.core.polyReduce( reducedObj, ver=1, trm=0, p=90, vct=0, tct=0, shp=0, keepBorder=1, keepMapBorder=1, 
                               keepColorBorder=1, keepFaceGroupBorder=1, keepHardEdge=1, keepCreaseEdge=1, keepBorderWeight=0.5, 
                               keepMapBorderWeight=0.5, keepColorBorderWeight=0.5, keepFaceGroupBorderWeight=0.5, keepHardEdgeWeight=0.5, 
                               keepCreaseEdgeWeight=0.5, useVirtualSymmetry=0, symmetryTolerance=0.01, sx=0, sy=1, sz=0, sw=0, preserveTopology=1, keepQuadsWeight=1, vertexMapName="",
                               replaceOriginal=1, cachingReduce=1, ch=1 )
        reducedObj.rename( target.shortName() + '_reduced' )
        pymel.core.select( reducedObj )
        cmds.DeleteHistory()
        
        bb = pymel.core.exactWorldBoundingBox( target )    
        bbmin = bb[:3]
        bbmax = bb[-3:]
        points = [[] for i in range(8)]
        points[0] = [bbmin[0], bbmin[1], bbmax[2]]
        points[1] = [bbmax[0], bbmin[1], bbmax[2]]
        points[2] = [bbmin[0], bbmax[1], bbmax[2]]
        points[3] = [bbmax[0], bbmax[1], bbmax[2]]
        points[4] = [bbmin[0], bbmax[1], bbmin[2]]
        points[5] = [bbmax[0], bbmax[1], bbmin[2]]
        points[6] = [bbmin[0], bbmin[1], bbmin[2]]
        points[7] = [bbmax[0], bbmin[1], bbmin[2]]
        
        boundingBoxObj = pymel.core.polyCube( ch=1, o=1, cuv=4, n= target.shortName() + '_gpu' )[0]
        boundingBoxObjShape = boundingBoxObj.getShape()
        boundingBoxObjShape.overrideEnabled.set( 1 )
        boundingBoxObjShape.overrideDisplayType.set( 2 )
        
        newLambert = pymel.core.shadingNode( 'lambert', asShader=1 )
        newLambertSG = pymel.core.sets( renderable=1, noSurfaceShader=1, empty=1, name= newLambert + 'SG' )
        newLambert.outColor >> newLambertSG.surfaceShader
        newLambert.transparency.set( 1,1,1 )
        cmds.sets( boundingBoxObj.name(), e=1, forceElement=newLambertSG.name() )
        
        for i in range( 8 ):
            pymel.core.move( points[i][0], points[i][1], points[i][2], boundingBoxObj + '.vtx[%d]' % i )
        
        sceneName = cmds.file( q=1, sceneName=1 )
        gpuPath = os.path.dirname( sceneName )
        
        pymel.core.select( target )
        mel.eval( 'displaySmoothness -divisionsU 0 -divisionsV 0 -pointsWire 4 -pointsShaded 1 -polygonObject 1;' )
        
        targetParents = cmds.listRelatives( target.name(), p=1, f=1 )
        targetPos = cmds.getAttr( target+ '.m' )
        cmds.xform( target.name(), os=1, matrix= sgCmds.getListFromMatrix( OpenMaya.MMatrix() ) )
        abcPath = cmds.gpuCache( target.name(), startTime=1, endTime=1, optimize=1, optimizationThreshold=1000, writeMaterials=0, dataFormat='ogawa',
                                 directory=gpuPath, fileName=target.replace( '|', '_' ), saveMultipleFiles=False )[0]
        cmds.xform( target.name(), os=1, matrix= targetPos )
        gpuObjName = target.split( '|' )[-1]+'_gpuOrig'
        gpuCacheNode = cmds.createNode( 'gpuCache' )
        gpuCacheObj = cmds.listRelatives( gpuCacheNode, p=1, f=1 )[0]
        gpuCacheObj = cmds.rename( gpuCacheObj, gpuObjName )
        gpuShapeName = cmds.listRelatives( gpuCacheObj, c=1,f=1 )[0]
        cmds.setAttr( gpuShapeName+'.cacheFileName', abcPath, type='string' )
        if targetParents:
            gpuCacheObj = cmds.parent( gpuCacheObj, targetParents[0] )
        cmds.xform( gpuCacheObj, os=1, matrix= targetPos )
        gpuCacheObj = pymel.core.ls( gpuCacheObj )[0]
        
        src = target
        gpuShape = gpuCacheObj.getShape()
        pymel.core.parent( gpuShape, boundingBoxObj, shape=1, add=1 )
        pymel.core.delete( gpuCacheObj )
        others = [reducedObj,boundingBoxObj]
        
        sceneName = cmds.file( q=1, sceneName=1 )
        fileName = sceneName.split( '/' )[-1].split( '.' )[0]
        targetPath = '.'.join( sceneName.split( '.' )[:-1] ) + '.mi'
        
        pymel.core.select( target )
        mel.eval( 'displaySmoothness -divisionsU 3 -divisionsV 3 -pointsWire 16 -pointsShaded 4 -polygonObject 3;' )
        
        pymel.core.select( src )
        cmds.file( targetPath, options='binary=1;compression=0;tabstop=8;perframe=0;padframe=0;perlayer=1;pathnames=3313323333;assembly=0;fragment=0;fragsurfmats=0;fragsurfmatsassign=0;fragincshdrs=0;fragchilddag=0;passcontrimaps=1;passusrdata=1;overrideAssemblyRootName=0;assemblyRootName=binary=1;compression=0;tabstop=8;perframe=0;padframe=0;perlayer=0;pathnames=3313333333;assembly=1;fragment=1;fragsurfmats=1;fragsurfmatsassign=1;fragincshdrs=1;fragchilddag=1;passcontrimaps=1;passusrdata=0;filter=00000011010000001101000;overrideAssemblyRootName=0;assemblyRootName=',
                   typ='mentalRay', pr=1, es=1, force=1 )
        mel.eval( 'Mayatomr -mi  -exportFilter 721600 -active -binary -fe  -fem  -fma  -fis  -fcd  -pcm  -as  -asn "%s" -xp "3313333333" -file "%s"' % (fileName,targetPath) )
        
        for other in others:
            otherShape = other.getShape()
            if otherShape.nodeType() == 'mesh':
                otherShape.miUpdateProxyBoundingBoxMode.set(3)
                otherShape.miProxyFile.set( targetPath )
        
        target.rename( target + '_orig' )
        
        folderPath = os.path.dirname( cmds.file( q=1, sceneName=1 ) )
        fileName = cmds.file( q=1, sceneName=1 ).split( '/' )[-1].split( '.' )[0]
        if not cmds.pluginInfo( 'sceneAssembly', q=1, l=1 ):
            cmds.loadPlugin( 'sceneAssembly' )
        
        mel.eval( 'assemblyCreate assemblyDefinition' )
        asmNode = pymel.core.ls( type='assemblyDefinition' )[-1]
        asmNode.rename( 'ASM_' + fileName )
        reps = pymel.core.assembly( asmNode, q=1, listRepresentations=1 )
        if reps:
            for rep in reps:
                pymel.core.assembly( asmNode, e=1, deleteRepresentation=rep )
        
        index = 0
        repNames = []
        for sel in [boundingBoxObj,reducedObj,target]:
            selShape = sel.getShape()
            repName = sel.split( '_' )[-1]
            repNames.append( repName )
            if selShape:
                if selShape.nodeType() == 'gpuCache':
                    pymel.core.assembly( asmNode, edit=True, createRepresentation='Cache',
                      input=selShape.cacheFileName.get(), repName=repName )
                    asmNode.attr( 'representations' )[index].repLabel.set( repName )
                    index+=1
                    continue            
            pymel.core.select( sel )
            filePath = folderPath + '/ASMOBJ_' + sel.shortName() + '.mb'
            cmds.file( filePath, force=1, options="v=0;", typ="mayaBinary", pr=1, es=1 )    
            pymel.core.assembly( asmNode, edit=True, createRepresentation='Scene',
                      input=filePath, repName=repName )
            asmNode.attr( 'representations' )[index].repLabel.set( repName )
            index+=1
        
        scenePath = cmds.file( q=1, sceneName=1 )
        folderName = os.path.dirname( scenePath )
        fileName = scenePath.split( '/' )[-1].split( '.' )[0]
        exportPath = folderName + '/ASM_' + fileName + '.mb'
        
        pymel.core.select( asmNode )
        cmds.file( exportPath, force=1, options="v=0;", typ="mayaBinary", pr=1, es=1 )



def makeForAnimFile():
    
    asm = pymel.core.ls( type='assemblyDefinition' )[0]
    reps = pymel.core.assembly( asm, q=1, lr=1 )
    
    dataPaths = []
    for i in range( len( reps ) ):
        dataPath = asm.attr( 'representations' )[i].repData.get()
        dataPaths.append( dataPath )
    
    for rep in reps:
        pymel.core.assembly( asm, e=1, dr=rep )
    
    cachePath = ''
    for root, dirs, names in os.walk( os.path.dirname( dataPaths[0] ) ):
        for name in names:
            if not name.split( '.' )[-1].lower() == 'abc': continue
            cachePath = root + '/' + name
    
    pymel.core.assembly( asm, edit=True, createRepresentation='Cache',
                      input=cachePath )
    asm.attr( 'representations' )[0].repName.set( reps[0] )
    asm.attr( 'representations' )[0].repLabel.set( reps[0] )
    for i in range( 1, 3 ):
        pymel.core.assembly( asm, edit=True, createRepresentation='Scene',
                      input=dataPaths[i] )
        asm.attr( 'representations' )[i].repName.set( reps[i] )
        asm.attr( 'representations' )[i].repLabel.set( reps[i] )


    scenePath = cmds.file( q=1, sceneName=1 )
    folderPath = os.path.dirname( scenePath )
    newFileName = scenePath.split( '/' )[-1].replace( '.mb', '_forAnim.mb' )
    newFilePath = folderPath + '/' + newFileName
    cmds.file( rename=newFilePath )
    cmds.file( f=1, save=1,  options="v=0;" )



def convertAssemblyReference():
    
    from maya import cmds, mel
    sels = cmds.ls( sl=1 )
    results = []
    for sel in sels:
        path = cmds.getAttr( sel + '.representations[0].repData' )
        asmPath = path.replace( '__gpu', '' ).replace( 'ASMOBJ_PRP_', 'ASM_' ).replace( 'ASMOBJ_BG_', 'ASM_' )
        if not os.path.exists( asmPath ): continue
        asmref = mel.eval( 'container -type assemblyReference -name "%s";' % sel )
        cmds.setAttr( asmref + '.definition', asmPath, type='string' )
        cmds.xform( asmref, ws=1, matrix= cmds.getAttr( sel + '.wm' ) )
        results.append( asmref )
    cmds.select( results )
    
    
    
def convertAssemblyReferenceForAnim():
    
    pass
    
    
    
def villageOptimize():
    
    import pymel.core

    references = pymel.core.ls( type='reference' )
    for refNode in references:
        try:cmds.file( importReference=1, referenceNode=refNode.name() )
        except:pass
    
    references = pymel.core.ls( type='reference' )
    for refNode in references:
        try:cmds.file( importReference=1, referenceNode=refNode.name() )
        except:pass
        
        
    import pymel.core
    from sgMaya import sgCmds
    from maya import cmds, OpenMaya, mel
    import ntpath, os
            
    
    def getBoundingBoxDistStr( sel ):
        
        bbMin = sel.getShape().boundingBoxMin.get()
        bbMax = sel.getShape().boundingBoxMax.get()
        
        minPoint = OpenMaya.MPoint( *bbMin )
        maxPoint = OpenMaya.MPoint( *bbMax )
        
        dist = minPoint.distanceTo( maxPoint )
        startSum = minPoint.x + minPoint.y + minPoint.z
        
        distStr = ( '%.3f' % (dist + startSum) ).replace( '.', '_' )
        return distStr
    
    
    def isVisible( target ):
        allParents = target.getAllParents()
        allParents.append( target )
        for parent in allParents:
            if not parent.v.get(): return False
        return True
    
    
    targetGrps = pymel.core.ls( sl=1 )
    
    resultGrps = []
    otherGrps = []
    meshs = {}
    sels = []
    
    for child in pymel.core.ls( type='transform' ):
        childShapes = child.listRelatives( s=1 )
        meshExists = False
        gpuExists = False
        for childShape in childShapes:
            if childShape.nodeType() == 'mesh':
                meshExists = True
            elif childShape.nodeType() == 'gpuCache':
                gpuExists = True
        if not meshExists: continue
        if gpuExists: continue
        sels.append( child )
    
    for sel in sels:
        selShape = sel.getShape()
        numVertices = selShape.numVertices()
        bbStr = getBoundingBoxDistStr( sel )
        keyStr = ('mesh_%d_%s' %( numVertices, bbStr )).replace( '-', 'm' )
        if not meshs.has_key( keyStr ):
            print sel
            meshs[ keyStr ] = [sel]
        else:
            meshs[ keyStr ].append( sel )
    
    srcMeshGrp = 'srcMeshs'
    if not pymel.core.objExists( srcMeshGrp ):
        pymel.core.createNode( 'transform', n=srcMeshGrp )
    
    lenKeys = len( meshs.keys() )
    cuIndex = 0
    for key in meshs.keys():
        if not pymel.core.objExists( key ):
            meshTr = pymel.core.duplicate( meshs[ key ][0] )[0]
            meshTr.rename( key )
            meshTr.setParent( srcMeshGrp )
        
        targetMeshs = meshs[ key ]
        for targetMesh in targetMeshs:
            cmds.connectAttr( key + '.outMesh', targetMesh.getShape().inMesh.name() )
        cuIndex += 1
        print "%.2f is done" % (float( cuIndex )/lenKeys * 100)
    
    
    import pymel.core
    
    
    def copyShader_multi( inputFirst, inputSeconds ):
        first = pymel.core.ls( inputFirst )[0]
        if not pymel.core.objExists( first ): return None
        try:firstShape = first.getShape()
        except:firstShape = first
        engines = firstShape.listConnections( type='shadingEngine' )
        if not engines: return None
        
        engines = list( set( engines ) )
        copyObjAndEngines = []
        
        seconds = [ pymel.core.ls( inputSecond )[0] for inputSecond in inputSeconds ]
        
        for engine in engines:
            srcCons = filter( lambda x : x.longName() in ['message', 'outColor'], engine.listConnections( s=1, d=0, p=1 ) )
            if not srcCons: continue
            pymel.core.hyperShade( objects = srcCons[0].node() )
            selObjs = pymel.core.ls( sl=1 )
            targetObjs = []
            for selObj in selObjs:
                if selObj.node() != firstShape: continue
                if selObj.find( '.' ) != -1:
                    for second in seconds:
                        targetObjs.append( second+'.'+ selObj.split( '.' )[-1] )
                else:
                    for second in seconds:
                        targetObjs.append( second )
            if not targetObjs: continue        
            for targetObj in targetObjs:
                cmds.sets( targetObj, e=1, forceElement=engine.name() )
                copyObjAndEngines.append( [targetObj, engine.name()] )
    
        return copyObjAndEngines
    
    for key in meshs.keys():
        keyShapes = cmds.listRelatives( key, s=1 )
        if not keyShapes: continue
        keyShape = keyShapes[0]
        targets = cmds.listConnections( keyShape + '.outMesh', s=0, d=1 )
        if not targets: continue
        if len( targets ) == 1: continue
        copyShader_multi( key, targets )
