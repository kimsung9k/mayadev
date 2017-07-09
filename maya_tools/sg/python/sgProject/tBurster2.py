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
    for topNode in topNodes:
        children = topNode.listRelatives( c=1 )
        for child in children:
            if child.find( 'V3' ) != -1: 
                targets.append( topNode )
                continue
            pymel.core.delete( child )
    
    for target in targets:
        pymel.core.select( target )
        mel.eval( 'displaySmoothness -divisionsU 3 -divisionsV 3 -pointsWire 16 -pointsShaded 4 -polygonObject 3;' )
        children = target.listRelatives( c=1, ad=1 )
        for child in children:
            pymel.core.showHidden( child, a=1 )
        
        mel.eval( 'displaySmoothness -divisionsU 3 -divisionsV 3 -pointsWire 16 -pointsShaded 4 -polygonObject 3;' )
        
        combinedObj = sgCmds.combineMultiShapes( target )
        combinedObj.rename( target.shortName() + '_combined' )
        
        reducedObj = pymel.core.duplicate( combinedObj )[0]
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
        
        boundingBoxObj = pymel.core.polyCube( ch=1, o=1, cuv=4, n= target.shortName() + '_boundingBox' )[0]
        boundingBoxObjShape = boundingBoxObj.getShape()
        
        for i in range( 8 ):
            pymel.core.move( points[i][0], points[i][1], points[i][2], boundingBoxObj + '.vtx[%d]' % i )
        
        sceneName = cmds.file( q=1, sceneName=1 )
        gpuPath = os.path.dirname( sceneName )
        
        targetParents = cmds.listRelatives( target.name(), p=1, f=1 )
        targetPos = cmds.getAttr( target+ '.m' )
        cmds.xform( target.name(), os=1, matrix= sgCmds.getListFromMatrix( OpenMaya.MMatrix() ) )
        abcPath = cmds.gpuCache( target.name(), startTime=1, endTime=1, optimize=1, optimizationThreshold=1000, writeMaterials=0, dataFormat='ogawa',
                                 directory=gpuPath, fileName=target.replace( '|', '_' ), saveMultipleFiles=False )[0]
        cmds.xform( target.name(), os=1, matrix= targetPos )
        gpuObjName = target.split( '|' )[-1]+'_gpu'
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
        others = [combinedObj,reducedObj,boundingBoxObj]
        
        sceneName = cmds.file( q=1, sceneName=1 )
        fileName = sceneName.split( '/' )[-1].split( '.' )[0]
        targetPath = '.'.join( sceneName.split( '.' )[:-1] ) + '.mi'
        
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
        for sel in [gpuCacheObj,boundingBoxObj,reducedObj,combinedObj,target]:
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
