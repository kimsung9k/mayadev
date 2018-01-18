import pymel.core
from maya import cmds

sels = pymel.core.ls( sl=1 )

class sgCmds:
    
    @staticmethod
    def isVisible( target ):
        allParents = target.getAllParents()
        allParents.append( target )
        for parent in allParents:
            if not parent.v.get(): return False
        return True
    
    
    @staticmethod
    def addAttr( target, **options ):
    
        items = options.items()
        
        attrName = ''
        channelBox = False
        keyable = False
        for key, value in items:
            if key in ['ln', 'longName']:
                attrName = value
            elif key in ['cb', 'channelBox']:
                channelBox = True
                options.pop( key )
            elif key in ['k', 'keyable']:
                keyable = True 
                options.pop( key )
        
        if pymel.core.attributeQuery( attrName, node=target, ex=1 ): return None
        
        pymel.core.addAttr( target, **options )
        
        if channelBox:
            pymel.core.setAttr( target+'.'+attrName, e=1, cb=1 )
        elif keyable:
            pymel.core.setAttr( target+'.'+attrName, e=1, k=1 )
    
    
    @staticmethod
    def getDecomposeMatrix( matrixAttr ):
    
        matrixAttr = pymel.core.ls( matrixAttr )[0]
        cons = matrixAttr.listConnections( s=0, d=1, type='decomposeMatrix' )
        if cons: 
            pymel.core.select( cons[0] )
            return cons[0]
        decomposeMatrix = pymel.core.createNode( 'decomposeMatrix' )
        matrixAttr >> decomposeMatrix.imat
        return decomposeMatrix
    
    
    @staticmethod
    def getConstrainMatrix( inputFirst, inputTarget ):
        first = pymel.core.ls( inputFirst )[0]
        target = pymel.core.ls( inputTarget )[0]
        mm = pymel.core.createNode( 'multMatrix' )
        first.wm >> mm.i[0]
        target.pim >> mm.i[1]
        return mm
    
    
    @staticmethod
    def constrain_all( first, target ):
    
        mm = sgCmds.getConstrainMatrix( first, target )
        dcmp = sgCmds.getDecomposeMatrix( mm.matrixSum )
        cmds.connectAttr( dcmp + '.ot',  target + '.t', f=1 )
        cmds.connectAttr( dcmp + '.or',  target + '.r', f=1 )
        cmds.connectAttr( dcmp + '.os',  target + '.s', f=1 )
        cmds.connectAttr( dcmp + '.osh',  target + '.sh', f=1 )
        
    
    @staticmethod
    def copyShader( inputFirst, inputSecond ):
        first = pymel.core.ls( inputFirst )[0]
        second = pymel.core.ls( inputSecond )[0]
        if not pymel.core.objExists( first ): return None
        if not pymel.core.objExists( second ): return None
        
        try:firstShape = first.getShape()
        except:firstShape = first
        try:secondShape = second.getShape()
        except:secondShape = second
        engines = firstShape.listConnections( type='shadingEngine' )
        if not engines: return None
        
        engines = list( set( engines ) )
        
        copyObjAndEngines = []
        for engine in engines:
            srcCons = filter( lambda x : x.longName() in ['message', 'outColor'], engine.listConnections( s=1, d=0, p=1 ) )
            if not srcCons: continue
            pymel.core.hyperShade( objects = srcCons[0].node() )
            selObjs = pymel.core.ls( sl=1 )
            targetObjs = []
            for selObj in selObjs:
                if selObj.node() != firstShape: continue
                if selObj.find( '.' ) != -1:
                    targetObjs.append( second+'.'+ selObj.split( '.' )[-1] )
                else:
                    targetObjs.append( secondShape.name() )
            if not targetObjs: continue        
            for targetObj in targetObjs:
                cmds.sets( targetObj, e=1, forceElement=engine.name() )
                copyObjAndEngines.append( [targetObj, engine.name()] )
        return copyObjAndEngines

    



def shadowEffect( lightTransform, projectTargets, projectBase ):
    
    children = pymel.core.listRelatives( projectTargets, c=1, ad=1, type='mesh' )
    projectTargets = [ child.getParent() for child in children if sgCmds.isVisible( child ) ]
    
    def getLocalGeometry( geometry, parentObject ):
        geometryShape = geometry.getShape()
        mm = pymel.core.createNode( 'multMatrix' )
        trGeo = pymel.core.createNode( 'transformGeometry' )
        newMeshShape = pymel.core.createNode( 'mesh' )
        
        geometry.wm >> mm.i[0]
        parentObject.wim >> mm.i[1]
        
        geometryShape.attr( 'outMesh' ) >> trGeo.inputGeometry
        mm.matrixSum >> trGeo.transform
        trGeo.outputGeometry >> newMeshShape.attr( 'inMesh' )
        return newMeshShape.getParent()
    
    def projectMesh( projTarget, projBase ):
        projTargetShape = projTarget.getShape()
        projBaseShape   = projBase.getShape()
        shrinkWrap = pymel.core.deformer( projTargetShape, type='shrinkWrap' )[0]
        shrinkWrap.attr( 'reverse' ).set( 1 )
        shrinkWrap.attr( 'projection' ).set( 2 )
        attrList = ['keepMapBorders','continuity','smoothUVs','keepBorder',
                    'boundaryRule','keepHardEdge','propagateEdgeHardness']
        for attr in attrList:
            projTargetShape.attr( attr ) >> shrinkWrap.attr( attr )
        projBaseShape.attr( 'worldMesh' ) >> shrinkWrap.attr( 'targetGeom' )
        return shrinkWrap

    def getOutMesh( targetMesh ):
        targetMeshShape = targetMesh.getShape()
        newMesh = pymel.core.createNode( 'mesh' )
        targetMeshShape.outMesh >> newMesh.inMesh
        return newMesh.getParent()

    
    def getProjectionTypeOutput( lightTransform ):
        sgCmds.addAttr( lightTransform, ln='projectionType', at='enum', en=':point:directionX:directionY:directionZ', k=1 )
        pmaNode = pymel.core.createNode( 'plusMinusAverage' )
        for i, outputValues in [ (0,[0,0,0]),(1,[1,0,0]),(2,[0,1,0]),(3,[0,0,1]) ]:
            condition = pymel.core.createNode( 'condition' )
            lightTransform.attr( 'projectionType' ) >> condition.firstTerm
            condition.attr( 'secondTerm' ).set( i )
            condition.colorIfTrue.set( *outputValues )
            condition.colorIfFalse.set( 0,0,0 )
            condition.outColor >> pmaNode.input3D[i]
        return pmaNode.attr( 'output3Dx' ), pmaNode.attr( 'output3Dy' ), pmaNode.attr( 'output3Dz' )
    
    def addOffsetAttribute( lightTransform, shrinkWrapNode ):
        sgCmds.addAttr( lightTransform, ln='offset', min=0, k=1 )
        lightTransform.attr( 'offset' ) >> shrinkWrapNode.attr( 'targetInflation' )

    constrainGrp = pymel.core.createNode( 'transform', n=lightTransform.nodeName() + '_shadowCoreGrp' )
    resultGrp    = pymel.core.createNode( 'transform', n=lightTransform.nodeName() + '_shadowResultGrp' )
    localProjBase = getLocalGeometry( projectBase, lightTransform )
    localProjBase.setParent( constrainGrp )
    localProjBase.attr( 'inheritsTransform' ).set( 0 )
    localProjBase.v.set( 0 )
    
    xOutput, yOutput, zOutput = getProjectionTypeOutput( lightTransform )
    
    localGeometrys = []
    resultObjects = []
    for projectTarget in projectTargets:
        localProjTarget = getLocalGeometry( projectTarget, lightTransform )
        localProjTarget.attr( 'inheritsTransform' ).set( 0 )
        localProjTarget.v.set( 0 )
        
        shrinkWrap = projectMesh( localProjTarget, localProjBase )
        resultObject = getOutMesh( localProjTarget )
        sgCmds.copyShader( projectTarget, resultObject )
        xOutput >> shrinkWrap.attr( 'alongX' )
        yOutput >> shrinkWrap.attr( 'alongY' )
        zOutput >> shrinkWrap.attr( 'alongZ' )
        addOffsetAttribute( lightTransform, shrinkWrap )
        
        pymel.core.parent( localProjTarget, resultObject, constrainGrp )
        localGeometrys.append( localProjTarget )
        resultObjects.append( resultObject )
    
    pymel.core.group( localGeometrys, n='LocalObjects' )
    pymel.core.parent( resultObjects, resultGrp )
    
    if not cmds.objExists( 'shadowEffectSurfaceShader' ):
        surfaceShader = cmds.shadingNode( 'surfaceShader', asShader=1, n='shadowEffectSurfaceShader' )
    else:
        surfaceShader = 'shadowEffectSurfaceShader'
    if not cmds.objExists( 'shadowEffectSurfaceShaderSG' ):
        surfaceShaderSG = cmds.sets( renderable=True, noSurfaceShader=True, empty=1, name=surfaceShader + 'SG' )
    else:
        surfaceShaderSG = 'shadowEffectSurfaceShaderSG'

    if not cmds.isConnected( surfaceShader + '.outColor', surfaceShaderSG + '.surfaceShader' ):
        cmds.connectAttr( surfaceShader + '.outColor', surfaceShaderSG + '.surfaceShader' )  
    cmds.sets( resultGrp.name(), forceElement=surfaceShaderSG )
    
    sgCmds.constrain_all( lightTransform, constrainGrp )
    sgCmds.constrain_all( lightTransform, resultGrp )

shadowEffect( sels[0], sels[1:-1], sels[-1] )