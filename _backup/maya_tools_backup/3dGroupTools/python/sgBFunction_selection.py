import maya.cmds as cmds


def getMeshObjectFromGroup( targets ):
    
    children = cmds.listRelatives( targets, c=1, ad=1, type='transform', f=1 )
    if not children: children = []
    children += targets
    
    targetChildren = []
    for child in children:
        childShapes = cmds.listRelatives( child, s=1, f=1 )
        if not childShapes: continue
        
        targetShape = None
        for shape in childShapes:
            if cmds.getAttr( shape+'.io' ): continue
            if cmds.nodeType( shape ) == 'mesh':
                targetShape = shape
                break
        if targetShape:
            targetChildren.append( child )
    
    targetChildren = list( set( targetChildren ) )
    
    return targetChildren



def getTransformNodesFromGroup( targets ):
    
    children = cmds.listRelatives( targets, c=1, ad=1, type='transform', f=1 )
    if not children: children=[]
    children += cmds.ls( targets, l=1 )
    
    targetChildren = []
    for child in children:
        if not cmds.nodeType( child ) in [ 'transform', 'joint' ]: continue
        targetChildren.append( child )
    return targetChildren



def getGeoFromGroup( targets ):
    
    children = cmds.listRelatives( targets, c=1, ad=1, type='transform', f=1 )
    if not children: children=[]
    children += targets
    
    targetShapes = []
    for child in children:
        childShapes = cmds.listRelatives( child, s=1, f=1 )
        if not childShapes: continue
        
        for shape in childShapes:
            if cmds.getAttr( shape+'.io' ): continue
            if cmds.nodeType( shape ) in ['mesh', 'nurbsCurve', 'nurbsSurface']:
                targetShapes.append( shape )
                break

    return targetShapes



def getMeshFromGroup( targets ):
    
    children = cmds.listRelatives( targets, c=1, ad=1, type='transform', f=1 )
    if not children: children=[]
    children += targets
    
    targetShapes = []
    for child in children:
        childShapes = cmds.listRelatives( child, s=1, f=1 )
        if not childShapes: continue
        
        for shape in childShapes:
            if cmds.getAttr( shape+'.io' ): continue
            if cmds.nodeType( shape ) == 'mesh':
                targetShapes.append( shape )
                break

    return targetShapes




def getDeformedMeshObjectsFromGroup( targets ):
    
    meshs = getMeshFromGroup( targets )
    
    if not meshs: return []
    
    def getAffectHistory( mesh ):
        cons = cmds.listConnections( mesh+'.inMesh', s=1, d=0 )
        if not cons: return mesh
        if cmds.nodeType( cons[0] ) == 'mesh':
            return getAffectHistory( cons[0] )
        else:
            return cons[0]
    
    returnTransforms = []
    for mesh in meshs:
        if cmds.nodeType( getAffectHistory( mesh ) ) != 'mesh':
            returnTransforms.append( cmds.listRelatives( mesh, p=1, f=1  )[0] )
    
    return list( set( returnTransforms ) )





def getDeformedObjectsFromGroup( targets ):
    
    import sgBFunction_dag
    targets = sgBFunction_dag.getChildrenShapeExists( targets )
    if not targets: return []

    returnTransforms = []
    for target in targets:
        targetShape = sgBFunction_dag.getShape( target )
        nodeType = cmds.nodeType( targetShape )
        if nodeType == 'mesh': inputAttr = 'inMesh'
        elif nodeType in ['nurbsCurve', 'nurbsSurface']: inputAttr = 'create'
        cons = cmds.listConnections( targetShape+'.'+inputAttr, s=1, d=0 )
        if not cons: continue
        returnTransforms.append( target )
    
    return list( set( returnTransforms ) )




def getTransformConnectedObjectsFromGroup( targets ):
    
    import sgBFunction_dag
    
    transforms = cmds.listRelatives( targets, c=1, ad=1, type='transform', f=1 )
    if not transforms: transforms = []
    transforms += targets
    
    returnTargets = []
    for tr in transforms:
        if not sgBFunction_dag.itHasTransformConnection( tr ): continue
        returnTargets.append( tr )
    
    return returnTargets



def getGetOrderedEdgeRing( edge ):
    
    cmds.select( edge )
    cmds.SelectEdgeRingSp()
    baseEdges = cmds.ls( sl=1, fl=1 )
    
    def getNextEdge( edge, baseEdges, orderedEdges=[] ):
    
        faces = cmds.polyListComponentConversion( edge, tf=1 )
        targetEdges = cmds.polyListComponentConversion( faces, te=1 )
        
        for targetEdge in cmds.ls( targetEdges, fl=1 ):
            if targetEdge in orderedEdges: continue
            if not targetEdge in baseEdges: continue
            if targetEdge == edge: continue
            return targetEdge
        return None

    nextEdge = getNextEdge( edge, baseEdges )
    orderedEdges = [nextEdge]
    loofLimit = 10000
    while( loofLimit > 0 ):
        nextEdge = getNextEdge( nextEdge, baseEdges, orderedEdges )
        if not nextEdge: break
        orderedEdges.append( nextEdge )
        loofLimit -=1

    return orderedEdges



def getSpecifyNumEdgeRing( edge, num ):
    
    orderedEdges = getGetOrderedEdgeRing( cmds.ls( sl=1 )[0] )
    numEdges = len( orderedEdges )
    if num > numEdges: return orderedEdges
    
    divNum = float( numEdges ) / num
    
    targetEdges = []
    for i in range( num ):
        index = int( divNum * i )
        targetEdges.append( orderedEdges[ index ] )
    return targetEdges