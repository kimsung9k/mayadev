import maya.api.OpenMaya as openMaya
import maya.OpenMaya as om
import maya.cmds as cmds



def getMObject( nameString ):
    
    selList = om.MSelectionList()
    selList.add( nameString )
    oNode = om.MObject()
    selList.getDependNode( 0, oNode )
    return oNode




def getMDagPath( nameString ):
    
    selList = om.MSelectionList()
    selList.add( nameString )
    dagPath = om.MDagPath()
    selList.getDagPath( 0, dagPath )
    return dagPath




def getMObject2( nameString ):
    
    selList = openMaya.MSelectionList()
    selList.add( nameString )
    return selList.getDependNode( 0 )




def getMDagPath2( nameString ):
    
    selList = openMaya.MSelectionList()
    selList.add( nameString )
    return selList.getDagPath( 0 )




def getShape( targetDagNode ):
    
    if cmds.nodeType( targetDagNode ) in ['joint', 'transform']:
        shapes = cmds.listRelatives( targetDagNode, s=1, f=1 )
        if not shapes:
            return None
        else:
            return shapes[0]
    else:
        return cmds.ls( targetDagNode, l=1 )[0]
    



def getShadingEngines( targetDagNode ):
    
    shape = getShape( targetDagNode )
    
    return cmds.listConnections( shape, s=0, d=1, type='shadingEngine')





def getTransform( targetDagNode ):
    
    if cmds.nodeType( targetDagNode ) in ['joint', 'transform']:
        return cmds.ls( targetDagNode, l=1 )[0]
    else:
        return cmds.listRelatives( targetDagNode, p=1, f=1 )[0]





def getParent( target ):
    
    targetParents = cmds.listRelatives( target, p=1, f=1 )
    if not targetParents: return None
    else: return targetParents[0]




def getParents( target, firstTarget='', parents = [] ):
    
    if not firstTarget:
        firstTarget = target
        parents = []

    ps = cmds.listRelatives( target, p=1, f=1 )
    if not ps: return parents
    parents.insert( 0, ps[0] )
    
    return getParents( ps[0], firstTarget, parents )




def getDirectChildren( target, children = [] ):
    
    def inGetDirectChildren( target, children = [] ):
        currentChildren = cmds.listRelatives( target, c=1, f=1, type='transform' )
        if not currentChildren: return children
        
        children.append( currentChildren[0] )
        return inGetDirectChildren( currentChildren[0], children )
    
    return inGetDirectChildren( target, [] )



def getFullPathName( target ):
    
    fnDagNode = openMaya.MFnDagNode( getMDagPath( target ) )
    return fnDagNode.fullPathName()




def getOriginalName( target ):
    
    fnDagNode = openMaya.MFnDagNode( getMDagPath( target ) )
    return fnDagNode.name()




def getNodeFromHistory( target, typeName, **options ):
    
    targetShapes = [getShape( target )]
    shapes = []
    for shape in targetShapes:
        if cmds.nodeType( shape ) == typeName:
            shapes.append( shape )
    
    if shapes: return shapes
    
    hists = cmds.listHistory( target, **options )
    
    if not hists: return []
    
    returnTargets = []
    for hist in hists:
        if cmds.nodeType( hist ) == typeName:
            returnTargets.append( hist )
    
    return returnTargets




def getOrigShape( target, ignoreOtherTransform=True ):

    import maya.OpenMaya as om
    meshs    = getNodeFromHistory( target, 'mesh' )
    surfaces = getNodeFromHistory( target, 'nurbsSurface' )
    curves   = getNodeFromHistory( target, 'nurbsCurve' )
    
    for targetShapes in [ meshs, surfaces, curves ]:
        if not targetShapes: continue
        firstShape = targetShapes[0]
        if cmds.nodeType( firstShape ) == 'mesh':
            fnShapeFirst = openMaya.MFnMesh( getMDagPath2( firstShape ) )
            numComponentFirst = fnShapeFirst.numPolygons
        elif cmds.nodeType( firstShape ) in ['nurbsSurface', 'nurbsCurve']:
            numComponentFirst = len( cmds.ls( firstShape+'.cv[*]', fl=1 ) )
    
        targetShapes.reverse()
        
        for targetShape in targetShapes:
            if cmds.nodeType( targetShape ) == 'mesh':
                fnShapeOther = om.MFnMesh( getMDagPath( targetShape ) )
                numComponentOther = fnShapeOther.numPolygons()
            elif cmds.nodeType( targetShape ) in ['nurbsSurface', 'nurbsCurve']:
                numComponentOther = len( cmds.ls( targetShape+'.cv[*]', fl=1 ) )
            
            if ignoreOtherTransform and cmds.listRelatives( targetShape, p=1, f=1 )[0] != cmds.listRelatives( firstShape, p=1, f=1 )[0]: continue
            if numComponentFirst == numComponentOther:
                return cmds.ls( targetShape, l=1 )[0]



def addIOShape( target ):
    
    target      = getTransform( target )
    targetShape = getShape( target )
    if not targetShape: return None
    
    targetShapeName = targetShape.split( '|' )[-1]
    
    targetOrigShape = getOrigShape( target )
    
    if cmds.nodeType( targetShape ) == 'mesh':
        outAttr = 'outMesh'
        inAttr  = 'inMesh'
    elif cmds.nodeType( targetShape ) in [ 'nurbsCurve', 'nurbsSurface' ]:
        outAttr = 'local'
        inAttr = 'create'
    else:
        return None
    
    newOrigShape = cmds.createNode( cmds.nodeType( targetShape ), n = targetShapeName+'Orig' )
    newOrigTransform = getTransform( newOrigShape )
    cmds.parent( newOrigShape, target, add=1, shape=1 )
    
    cons = cmds.listConnections( targetOrigShape+'.'+outAttr, s=1, d=0, c=1, p=1 )
    if not cons: 
        cmds.connectAttr( targetOrigShape +'.'+outAttr, newOrigShape +'.'+inAttr )
        cmds.refresh()
        cmds.disconnectAttr( targetOrigShape +'.'+outAttr, newOrigShape +'.'+inAttr )
    else: 
        cmds.connectAttr( cons[1], newOrigShape+'.'+inAttr )
        cmds.connectAttr( targetOrigShape+'.'+outAttr, newOrigShape+'.'+inAttr, f=1 )
    
    cmds.setAttr( newOrigShape+'.io', 1 )
    cmds.delete( newOrigTransform )
    
    return newOrigShape




def getChildrenSpecifyNodeTypes( topNodes, nodeTypes ):
    
    sels = cmds.ls( topNodes, tr=1 )
    if not sels: return []
    
    selH = cmds.listRelatives( sels, c=1, ad=1, f=1 )
    if not selH: selH = []
    selH += sels
    
    targets = []
    for sel in selH:
        if not cmds.nodeType( sel ) in nodeTypes: continue
        targets.append( sel )
    
    return targets




def getChildrenShapeExists( topNodes ):
    
    sels = cmds.ls( topNodes )
    
    trNodes = []
    for sel in sels:
        trNodes.append( getTransform( sel ) )
    
    if not trNodes: return []

    selH = cmds.listRelatives( trNodes, c=1, ad=1, f=1, type='transform' )
    if not selH: selH = []
    selH += trNodes
    
    targets = []
    for sel in selH:
        selShape = getShape( sel )
        if not selShape: continue
        targets.append( sel )
    targets = list( set( targets ) )
    
    return targets



def getChildrenJointExists( topNodes ):
    
    sels = cmds.ls( topNodes )
    
    trNodes = []
    for sel in sels:
        trNodes.append( getTransform( sel ) )
    
    if not trNodes: return []

    selH = cmds.listRelatives( trNodes, c=1, ad=1, f=1, type='transform' )
    if not selH: selH = []
    selH += trNodes
    
    targets = []
    for sel in selH:
        if cmds.nodeType( sel ) != 'joint': continue
        targets.append( sel )
    targets = list( set( targets ) )
    
    return targets



def getChildrenCurveExists( topNodes ):
    
    sels = cmds.ls( topNodes )
    
    trNodes = []
    for sel in sels:
        trNodes.append( getTransform( sel ) )
    
    if not trNodes: return []

    selH = cmds.listRelatives( trNodes, c=1, ad=1, f=1, type='transform' )
    if not selH: selH = []
    selH += trNodes
    
    targets = []
    for sel in selH:
        selShape = getShape( sel )
        if not selShape: continue
        if cmds.nodeType( selShape ) != 'nurbsCurve': continue
        targets.append( sel )
    targets = list( set( targets ) )
    
    return targets



def getChildrenSurfaceExists( topNodes ):
    
    sels = cmds.ls( topNodes )
    
    trNodes = []
    for sel in sels:
        trNodes.append( getTransform( sel ) )
    
    if not trNodes: return []

    selH = cmds.listRelatives( trNodes, c=1, ad=1, f=1, type='transform' )
    if not selH: selH = []
    selH += trNodes
    
    targets = []
    for sel in selH:
        selShape = getShape( sel )
        if not selShape: continue
        if cmds.nodeType( selShape ) != 'surface': continue
        targets.append( sel )
    targets = list( set( targets ) )
    
    return targets



def getChildrenMeshExists( topNodes ):
    
    sels = cmds.ls( topNodes )
    
    trNodes = []
    for sel in sels:
        trNodes.append( getTransform( sel ) )
    
    if not trNodes: return []

    selH = cmds.listRelatives( trNodes, c=1, ad=1, f=1, type='transform' )
    if not selH: selH = []
    selH += trNodes
    
    targets = []
    for sel in selH:
        selShape = getShape( sel )
        if not selShape: continue
        if cmds.nodeType( selShape ) != 'mesh': continue
        targets.append( sel )
    targets = list( set( targets ) )
    
    return targets



def getChildrenGpuCacheExists( topNodes ):
    
    sels = cmds.ls( topNodes )
    
    trNodes = []
    for sel in sels:
        trNodes.append( getTransform( sel ) )
    
    if not trNodes: return []

    selH = cmds.listRelatives( trNodes, c=1, ad=1, f=1, type='transform' )
    if not selH: selH = []
    selH += trNodes
    
    targets = []
    for sel in selH:
        selShape = getShape( sel )
        if not selShape: continue
        if cmds.nodeType( selShape ) != 'gpuCache': continue
        targets.append( sel )
    targets = list( set( targets ) )
    
    return targets



def getChildrenTopJointExists( topNodes ):
    
    sels = cmds.ls( topNodes )
    
    trNodes = []
    for sel in sels:
        trNodes.append( getTransform( sel ) )
    
    if not trNodes: return []
    
    selChildren = cmds.listRelatives( trNodes, c=1, f=1, type='transformo' )




def getTopJointChildren( topNodes ):

    import sgBFunction_convert
    
    topNodes = sgBFunction_convert.singleToList( topNodes )

    returnList = []
    for topNode in topNodes:
        if cmds.nodeType( topNode ) == 'joint':
            returnList.append( topNode )
            continue
        returnList += getTopJointChildren( cmds.listRelatives( topNode, c=1, f=1 ) )
    return returnList



def getNodeAndComponentIndicesFromSelection():
    
    selList = om.MSelectionList()
    om.MGlobal.getActiveSelectionList( selList )
    
    if not selList: return None
    
    returnTargets= []
    for i in range( selList.length() ):
        dagPath = om.MDagPath()
        mObj    = om.MObject()
        selList.getMDagPath( i, dagPath, mObj )
        indices = om.MIntArray()
        
        if not mObj.isNull():
            components = om.MFnSingleIndexedComponent( mObj )
            components.getElements( indices )
        
        returnTargets.append( [ om.MFnDagNode( dagPath ).name(), indices ] )
    
    return returnTargets




def itHasTransformConnection( target ):
    
    dagNode = om.MFnDagNode( getMDagPath( target ) )
    
    connections = om.MPlugArray()
    for attr in [ 't', 'tx', 'ty', 'tz', 'r', 'rx', 'ry', 'rz', 's', 'sx', 'sy', 'sz', 'v' ]:
        plug = dagNode.findPlug( attr )
        plug.connectedTo( connections, True, False )
        if connections.length(): return True
    return False



def getBoundingBoxCenter( target ):
    
    bbmin = cmds.getAttr( target+'.boundingBoxMin' )[0]
    bbmax = cmds.getAttr( target+'.boundingBoxMax' )[0]
    
    return [(bbmin[0]+bbmax[0])/2, (bbmin[1]+bbmax[1])/2, (bbmin[2]+bbmax[2])/2]



def getFollicleFromCurve( curve ):
    
    follicles = getNodeFromHistory( curve, 'follicle' )
    if follicles:
        return follicles[0]
    else:
        curveShape = getShape( curve )
        cons = cmds.listConnections( curveShape+'.create', s=1, d=0, type='follicle', shapes=1 )
        if not cons: return None
        return cons[0]



def makeCloneObject( target, cloneLabel= '_clone', **options  ):
    
    import sgBModel_dag
    import sgBFunction_attribute
    import sgBFunction_value
    import sgBFunction_connection
    
    op_cloneAttrName = None
    op_shapeOn       = None
    op_connectionOn  = None
    
    op_cloneAttrName = sgBFunction_value.getValueFromDict( options, 'cloneAttrName' )
    op_shapeOn = sgBFunction_value.getValueFromDict( options, 'shapeOn' )
    op_connectionOn = sgBFunction_value.getValueFromDict( options, 'connectionOn' )

    if op_cloneAttrName:
        attrName = op_cloneAttrName
    else:
        attrName = sgBModel_dag.cloneTargetAttrName

    targets = getParents( target )
    targets.append( target )
    
    targetCloneParent = None
    for cuTarget in targets:
        sgBFunction_attribute.addAttr( cuTarget, ln=attrName, at='message' )
        cloneConnection = cmds.listConnections( cuTarget+'.'+attrName, s=1, d=0 )
        if not cloneConnection:
            targetClone = cmds.createNode( 'transform', n= cuTarget.split( '|' )[-1]+cloneLabel )
            cmds.connectAttr( targetClone+'.message', cuTarget+'.'+attrName )
            
            if op_shapeOn:
                cuTargetShape = getShape( cuTarget )
                if cuTargetShape:
                    duObj = cmds.duplicate( cuTarget, n=targetClone+'_du' )[0]
                    duShape = cmds.listRelatives( duObj, s=1, f=1 )[0]
                    duShape = cmds.parent( duShape, targetClone, add=1, shape=1 )[0]
                    cmds.delete( duObj )
                    cmds.rename( duShape, targetClone+'Shape' )
            if op_connectionOn:
                sgBFunction_connection.getSourceConnection( cuTarget, targetClone )
                cuTargetShape    = getShape( cuTarget )
                targetCloneShape = getShape( targetClone )
                
                if cuTargetShape and targetCloneShape:
                    sgBFunction_connection.getSourceConnection( cuTargetShape, targetCloneShape )
        else:
            targetClone = cloneConnection[0]
        
        targetCloneParentExpected = getParent( targetClone )
        if cmds.ls( targetCloneParentExpected ) != cmds.ls( targetCloneParent ) and targetCloneParent:
            targetClone = cmds.parent( targetClone, targetCloneParent )[0]

        cuTargetPos = cmds.getAttr( cuTarget+'.m' )
        cmds.xform( targetClone, os=1, matrix=cuTargetPos )

        targetCloneParent = targetClone
    return targetCloneParent


def makeCloneObject2( target, replaceName=['SOURCENAME_', 'TARGETNAME_'], **options ):
    
    import sgBModel_dag
    import sgBFunction_attribute
    import sgBFunction_value
    import sgBFunction_connection
    
    op_cloneAttrName = None
    op_shapeOn       = None
    op_connectionOn  = None
    
    op_cloneAttrName = sgBFunction_value.getValueFromDict( options, 'cloneAttrName' )
    op_shapeOn = sgBFunction_value.getValueFromDict( options, 'shapeOn' )
    op_connectionOn = sgBFunction_value.getValueFromDict( options, 'connectionOn' )
    
    if op_cloneAttrName:
        attrName = op_cloneAttrName
    else:
        attrName = sgBModel_dag.cloneTargetAttrName
    
    targets = getParents( target )
    targets.append( target )
    
    targetCloneParent = None
    for cuTarget in targets:
        sgBFunction_attribute.addAttr( cuTarget, ln=attrName, at='message' )
        cloneConnection = cmds.listConnections( cuTarget+'.'+attrName, s=1, d=0 )
        if not cloneConnection:
            print "replaceName : ", cuTarget.split( '|' )[-1].replace( replaceName[0], replaceName[1] )
            targetClone = cmds.createNode( 'transform', n= cuTarget.split( '|' )[-1].replace( replaceName[0], replaceName[1] ) )
            cmds.connectAttr( targetClone+'.message', cuTarget+'.'+attrName )
            
            if op_shapeOn:
                cuTargetShape = getShape( cuTarget )
                if cuTargetShape:
                    duObj = cmds.duplicate( cuTarget, n=targetClone+'_du' )[0]
                    duShape = cmds.listRelatives( duObj, s=1, f=1 )[0]
                    duShape = cmds.parent( duShape, targetClone, add=1, shape=1 )[0]
                    cmds.delete( duObj )
                    cmds.rename( duShape, targetClone+'Shape' )
            if op_connectionOn:
                sgBFunction_connection.getSourceConnection( cuTarget, targetClone )
                cuTargetShape    = getShape( cuTarget )
                targetCloneShape = getShape( targetClone )
                
                if cuTargetShape and targetCloneShape:
                    sgBFunction_connection.getSourceConnection( cuTargetShape, targetCloneShape )
        else:
            targetClone = cloneConnection[0]
        
        targetCloneParentExpected = getParent( targetClone )
        if cmds.ls( targetCloneParentExpected ) != cmds.ls( targetCloneParent ) and targetCloneParent:
            targetClone = cmds.parent( targetClone, targetCloneParent )[0]

        cuTargetPos = cmds.getAttr( cuTarget+'.m' )
        cmds.xform( targetClone, os=1, matrix=cuTargetPos )

        targetCloneParent = targetClone
    return targetCloneParent





def getConstrainedObject( target, constLabel = '_coned' ):
    
    import sgBModel_dag
    import sgBFunction_attribute
    import sgBFunction_connection
    
    attrName = sgBModel_dag.constrainedTargetAttrName
    
    sgBFunction_attribute.addAttr( target, ln= attrName, at='message' )
    connections = cmds.listConnections( target+'.'+attrName, s=1, d=0 )
    if not connections:
        constTarget = cmds.createNode( 'transform', n= target.split( '|' )[-1].replace( ':', '_' ) + constLabel )
        cmds.connectAttr( constTarget+'.message', target+'.'+attrName )
        sgBFunction_connection.constraintAll( target, constTarget )
    else:
        constTarget = connections[0]
    
    return constTarget
    



def getTopTransformNodes():
    
    trs = cmds.ls( type='transform' )
    
    topTransforms = []
    for tr in trs:
        if cmds.listRelatives( tr, p=1 ): continue
        topTransforms.append( cmds.ls( tr, l=1 )[0] )
    
    return topTransforms


def isBoundingBoxCross( firstObj, secondObj ):
    
    bboxFirst   = cmds.exactWorldBoundingBox( firstObj )
    bboxSecond  = cmds.exactWorldBoundingBox( secondObj )
    
    firstMin = bboxFirst[:3]
    firstMax = bboxFirst[3:]
    secondMin = bboxSecond[:3]
    secondMax = bboxSecond[3:]
    
    isCross = True
    for dimantion in [ [0,1], [1,2], [2,0] ]: 
        for i in dimantion:
            if firstMax[i] < secondMin[i] or firstMin[i] > secondMax[i]:
                isCross = False
                break
    return isCross