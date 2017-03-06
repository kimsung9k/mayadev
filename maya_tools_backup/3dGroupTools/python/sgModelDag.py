import maya.cmds as cmds
import maya.OpenMaya as om
import sgModelDg




def getMObject( target ):
    selList = om.MSelectionList()
    selList.add( target )
    mObj = om.MObject()
    selList.getDependNode( 0, mObj )
    return mObj



        

def getDagPath( targetDagNode ):
    
    selList = om.MSelectionList()
    selList.add( targetDagNode )
    dagPath = om.MDagPath()
    selList.getDagPath( 0, dagPath )
    return dagPath



def getShape( targetDagNode ):
    
    if cmds.nodeType( targetDagNode ) in ['joint', 'transform']:
        shapes = cmds.listRelatives( targetDagNode, s=1, f=1 )
        if not shapes:
            return None
        else:
            for shape in shapes:
                if not cmds.getAttr( shape+'.io' ): return shape
    else:
        return cmds.ls( targetDagNode, l=1 )[0]



def getTransform( targetDagNode ):
    
    if cmds.nodeType( targetDagNode ) in ['joint', 'transform']:
        return cmds.ls( targetDagNode, l=1 )[0]
    else:
        return cmds.listRelatives( targetDagNode, p=1, f=1 )[0]
    
    
    
    
def getBoundingBoxSize( target, **options ):
    
    options.update( { 'q':True, 'bb':True } )
    bb = cmds.xform( target, **options )
    
    bbmin = bb[:3]
    bbmax = bb[3:]

    sizeX = bbmax[0] - bbmin[0]
    sizeY = bbmax[1] - bbmin[1]
    sizeZ = bbmax[2] - bbmin[2]
    
    return sizeX, sizeY, sizeZ



def getBoundingBoxCenter( target, **options ):
    
    options.update( { 'q':True, 'bb':True } )
    bb = cmds.xform( target, **options )
    
    bbmin = bb[:3]
    bbmax = bb[:3]
    
    centerX = ( bbmin[0] + bbmax[0] )/2
    centerY = ( bbmin[1] + bbmax[1] )/2
    centerZ = ( bbmin[2] + bbmax[2] )/2
    
    return centerX, centerY, centerZ




def getMeshExistsChildren( topObj ):

    children = cmds.listRelatives( topObj, c=1, ad=1, type='mesh',f=1 )

    meshObjs = []
    
    for child in children:
        childP = cmds.listRelatives( child, p=1,f=1 )[0]
        meshObjs.append( childP )
    
    meshObjs = list( set( meshObjs ) )
    
    return meshObjs




def getMWorldMatrix( transformNodeName ):
    
    return getDagPath( transformNodeName ).inclusiveMatrix()





def getMMatrix( transformNodeName ):
    
    transform = om.MFnTransform( getDagPath( transformNodeName ) )
    return transform.transformation().asMatrix()





def getParents( target, firstTarget='', parents = [] ):
    
    if not firstTarget: 
        firstTarget = target
        parents = []

    ps = cmds.listRelatives( target, p=1, f=1 )
    if not ps: return parents
    parents.insert( 0, ps[0] )
    
    return getParents( ps[0], firstTarget, parents )





def getHierarchy( target, firstTarget = '', parents = [] ):
    
    if not firstTarget: 
        firstTarget = target
        parents = []
    ps = cmds.listRelatives( target, p=1, f=1 )
    if not ps: 
        parents.append( firstTarget )
        return parents
    parents.insert( 0, ps[0] )
    
    return getHierarchy( ps[0], firstTarget, parents )




def isShapeInVis( shapeObject ):
    
    if cmds.getAttr( shapeObject+'.io' ): return False
    
    dagObjs = getHierarchy( shapeObject )
    for dagObject in dagObjs:
        isVisOn    = cmds.getAttr( dagObject+'.v' )
        isLodVisOn = cmds.getAttr( dagObject+'.lodVisibility' )
        visConnection = cmds.listConnections( dagObject+'.v', s=1, d=0 )
        
        if isVisOn and isLodVisOn: continue
        if visConnection: continue
        return False
    return True



def isDeformedObject( shape ):
    
    if cmds.nodeType( shape ) == 'mesh':
        if cmds.listConnections( shape+'.inMesh' ): return True
        else: return False
    if cmds.nodeType( shape ) == 'nurbsCurve' or cmds.nodeType( shape ) == 'nurbsSurface':
        if cmds.listConnections( shape+'.create' ): return True
        else: return False
        

     
     
     
def getDeformedObjects( shapes ):
    
    deformedObjs = []
    for shape in shapes:
        if cmds.nodeType( shape ) == 'transform':
            rShapes = cmds.listRelatives( shape, s=1 )
            if not rShapes: continue
            shape = rShapes[0]
        if isDeformedObject( shape ):
            deformedObjs.append( shape )
    return deformedObjs





def getMeshsIsInVis( topDagNode='' ):
    
    if not topDagNode:
        checkMeshs = cmds.ls( type='mesh', l=1 )
    else:
        checkMeshs = cmds.listRelatives( topDagNode, c=1, ad=1, type='mesh', f=1 )
    if not checkMeshs: return []
    
    meshs = []
    for mesh in checkMeshs:
        if isShapeInVis( mesh ):
            meshs.append( mesh )
    
    return meshs





def getShapeSrcCon( crv ):
    
    try:
        return cmds.listConnections( crv, s=1, d=0, p=1, c=1 )[1]
    except:
        duObj = cmds.duplicate( crv )[0]
        duShape = cmds.listRelatives( duObj, s=1, f=1 )[0]
        duShape = cmds.parent( duShape, crv, add=1, shape=1 )
        cmds.delete( duObj )
        cmds.setAttr( duShape+'.io', 1 )
        return duShape+'.local'





def getPolygonInfo( meshName ):
    
    dagPath = getDagPath( meshName )
    fnMesh = om.MFnMesh( dagPath )
    meshMatrix = dagPath.inclusiveMatrix()

    numVtx  = fnMesh.numVertices()
    numPoly = fnMesh.numPolygons()
    mPointArr = om.MPointArray()
    mCountArr = om.MIntArray()
    mConnectArr = om.MIntArray()
    
    fnMesh.getPoints( mPointArr )
    
    mCountArr.setLength( numPoly )
    
    for i in range( numPoly ):
        mCountArr[i] = fnMesh.polygonVertexCount( i )
        
        numStr = cmds.polyInfo( meshName+'.f[%d]' % i, fv=1 )[0].split( ':' )[1].strip()
        
        eachStr = ''
        
        nums = []
        
        for char in numStr:
            if char == ' ':
                if eachStr.isdigit():
                    nums.append( int( eachStr ) )
                eachStr = ''
            else:
                eachStr += char
        if eachStr:
            nums.append( int( eachStr ) )
        
        for j in range( len( nums ) ):
            mConnectArr.append( nums[j] )

    pointArr = om.MPointArray()
    countArr = om.MIntArray()
    connectArr = om.MIntArray()
    uArray    = om.MFloatArray()
    vArray    = om.MFloatArray()

    for i in range( mPointArr.length() ):
        pointArr.append( om.MPoint( mPointArr[i].x,mPointArr[i].y,mPointArr[i].z ) )
    for i in range( mCountArr.length() ):
        countArr.append( mCountArr[i] )
    for i in range( mConnectArr.length() ):
        connectArr.append( mConnectArr[i] )
        
    fnMesh.getUVs( uArray, vArray )

    return meshMatrix, numVtx, numPoly, pointArr, countArr, connectArr, uArray, vArray




def getFullPathName( target ):
    
    fnDagNode = om.MFnDagNode( getDagPath( target ) )
    return fnDagNode.fullPathName()




def getOriginalName( target ):
    
    fnDagNode = om.MFnDagNode( getDagPath( target ) )
    return fnDagNode.name()




def getNodeFromHistory( target, typeName ):
    
    hists = cmds.listHistory( target )
    
    returnTargets = []
    for hist in hists:
        if cmds.nodeType( hist ) == typeName:
            returnTargets.append( hist )
    
    return returnTargets




def getSourceCurveAttr( shape ):
    
    cons = cmds.listConnections( shape+'.create', s=1, d=0, p=1, c=1 )
    shapeP = cmds.listRelatives( shape, p=1 )[0]
    
    if not cons:
        duObj = cmds.duplicate( shape )[0]
        duShapes = cmds.listRelatives( duObj, s=1, f=1 )
        
        targetOrig = ''
        for duShape in duShapes:
            if not cmds.getAttr( duShape+'.io' ):
                targetOrig = duShape
                break
        
        cmds.setAttr( targetOrig+'.io', 1 )
        targetOrig = cmds.parent( targetOrig, shapeP, s=1, add=1 )[0]
        
        cmds.delete( duObj )
        
        cons = cmds.listConnections( shape+'.controlPoints', p=1, c=1, s=1, d=0 )

        if cons:
            for i in range( 0, len( cons ), 2 ):
                attr = cons[i].split( '.' )[-1]
                cmds.connectAttr( cons[i+1], targetOrig+'.'+attr )
                cmds.disconnectAttr( cons[i+1], cons[i] )
            
        return targetOrig+'.local'
        
    else:
        return cons[1]




def getOrigShape( shape ):
    
    shape = getShape( shape )
    if not shape: return None
    
    nodeType = cmds.nodeType( shape )
    
    outputAttr = ''
    inputAttr = ''
    if nodeType in ['nurbsSurface','nurbsCurve']:
        outputAttr = 'local'
        inputAttr  = 'create'
    elif nodeType == 'mesh':
        outputAttr = 'outMesh'
        inputAttr  = 'inMesh'
    
    cons = cmds.listConnections( shape, s=1, d=0, c=1, p=1 )
    
    origShapeNode = None
    
    if cons:
        outputCons = cons[1::2]
        inputCons = cons[::2]
        
        outputNode = ''
        for i in range( len( inputCons ) ):
            if inputCons[i].split( '.' )[1] == inputAttr:
                outputNode = outputCons[i].split( '.' )[0]
        
        checkList = []
        if outputNode:
            def getOrigShapeNode( node ):
                if node in checkList: return None
                checkList.append( node )
                if not cmds.nodeType( node ): return None
                if cmds.nodeType( node ) == nodeType:
                    if cmds.getAttr( node+'.io' ):
                        return node

                cons = cmds.listConnections( node, s=1, d=0, p=1, c=1 )
                nodes = []
                if cons:
                    for con in cons[1::2]:
                        nodes.append( getOrigShapeNode( con.split( '.' )[0] ) )
                for node in nodes:
                    if node:
                        return node
                return None
            origShapeNode = getOrigShapeNode( outputNode )
    
    if origShapeNode:
        return origShapeNode
    else:
        cons = 1
        while( cons ):
            cons = cmds.listConnections( shape+'.'+inputAttr, p=1,c=1 )
            if cons:
                for con in cons[1::2]:
                    cmds.delete( con.split( '.' )[0] )
        
        origNode = cmds.createNode( nodeType, n='temp_origNodeShape' )
        origP    = cmds.listRelatives( origNode, p=1 )[0]
        cmds.connectAttr(    shape +  '.'+outputAttr, origNode+'.'+inputAttr )
        duOrigP  = cmds.duplicate( origP )[0]
        duOrig   = cmds.listRelatives( duOrigP, s=1, f=1 )[0]
        cmds.connectAttr(    duOrig+'.'+outputAttr, shape+   '.'+inputAttr )
        shapeP   = cmds.listRelatives( shape, p=1, f=1 )[0]
        duOrig = cmds.parent( duOrig, shapeP, add=1, shape=1 )[0]
        cmds.delete( origP, duOrigP )
        cmds.setAttr( duOrig+'.io', 1 )
        origShapeNode = cmds.rename( duOrig.split( '|' )[-1], shape+'Orig' )
        return origShapeNode




def getIntermediateObjects( target ):
    
    transform = getTransform( target )
    shapes = cmds.listRelatives( transform, s=1 )
    
    if not shapes: return []
    
    returnShapes = []
    for shape in shapes:
        if cmds.getAttr( shape+'.io' ):
            returnShapes.append( shape )
    
    return returnShapes