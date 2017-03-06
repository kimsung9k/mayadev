import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import selection
import attribute
from sgModules import sgbase
import convert
from sgModules import sgcommands
import transform
import connect
import value


def getLocalName( dagNode ):
    
    dagNode = OpenMaya.MFnDagNode( sgbase.getDagPath( dagNode ) )
    return dagNode.name()




def getPartialPathName( dagNode ):
    
    dagNode = OpenMaya.MFnDagNode( sgbase.getDagPath( dagNode ) )
    return dagNode.partialPathName()




def getFullPathName( dagNode ):
    
    dagNode = OpenMaya.MFnDagNode( sgbase.getDagPath( dagNode ) )
    return dagNode.fullPathname()



def getDagPath( target ):
    dagPath = OpenMaya.MDagPath()
    selList = OpenMaya.MSelectionList()
    selList.add( target )
    selList.getDagPath( 0, dagPath )
    return dagPath



def getIoMesh( targets ):
    
    if not type( targets ) in [ type([]), type(()) ]:
        targets = [targets]
    
    meshs = []
    
    for target in targets:
        if cmds.nodeType( target ) == "transform":
            shapes = cmds.listRelatives( target, s=1, f=1 )
            for shape in shapes:
                if not cmds.getAttr( shape + ".io" ) : continue
                if cmds.nodeType( shape ) == "mesh":
                    meshs.append( shape )
        elif cmds.nodeType( target ) == "mesh" and cmds.getAttr( shape + ".io" ):
            meshs.append( target )
    
    return meshs



def getMeshTransforms( targets ):
    
    targets = convert.singleToList( targets )
    children = cmds.listRelatives( targets, c=1, ad=1, f=1, type='transform' )
    if not children: children = []
    children += targets
    meshChildren = []
    for child in children:
        childShape = getShape( child )
        if not childShape: continue
        meshChildren.append( child )
    return meshChildren



def getDagNode( dagNodeName ):
    
    if type( dagNodeName ) == type( OpenMaya.MFnDagNode ): return dagNodeName
    return OpenMaya.MFnDagNode( sgbase.getDagPath( dagNodeName ) )




def getNoneIoMesh( targets ):
    
    if not type( targets ) in [ type([]), type(()) ]:
        targets = [targets]
    
    meshs = []
    
    for target in targets:
        if cmds.nodeType( target ) == "transform":
            shapes = cmds.listRelatives( target, s=1, f=1 )
            if not shapes: continue
            for shape in shapes:
                if cmds.getAttr( shape + ".io" ) : continue
                if cmds.nodeType( shape ) == "mesh":
                    meshs.append( shape )
        elif cmds.nodeType( target ) == "mesh":
            meshs.append( target )
        
    return meshs




def getTransform( targetDagNode ):
    
    if cmds.nodeType( targetDagNode ) in ['joint', 'transform']:
        return cmds.ls( targetDagNode, l=1 )[0]
    else:
        return cmds.listRelatives( targetDagNode, p=1, f=1 )[0]



def getOrigShape( target, ignoreOtherTransform=True ):

    import maya.OpenMaya as om
    meshs    = getNodeFromHistory( target, 'mesh' )
    surfaces = getNodeFromHistory( target, 'nurbsSurface' )
    curves   = getNodeFromHistory( target, 'nurbsCurve' )
    
    for targetShapes in [ meshs, surfaces, curves ]:
        if not targetShapes: continue
        firstShape = targetShapes[0]
        if cmds.nodeType( firstShape ) == 'mesh':
            fnShapeFirst = OpenMaya.MFnMesh( getDagPath( firstShape ) )
            numComponentFirst = fnShapeFirst.numPolygons
        elif cmds.nodeType( firstShape ) in ['nurbsSurface', 'nurbsCurve']:
            numComponentFirst = len( cmds.ls( firstShape+'.cv[*]', fl=1 ) )
    
        targetShapes.reverse()
        
        for targetShape in targetShapes:
            if cmds.nodeType( targetShape ) == 'mesh':
                fnShapeOther = om.MFnMesh( getDagPath( targetShape ) )
                numComponentOther = fnShapeOther.numPolygons()
            elif cmds.nodeType( targetShape ) in ['nurbsSurface', 'nurbsCurve']:
                numComponentOther = len( cmds.ls( targetShape+'.cv[*]', fl=1 ) )
            
            if ignoreOtherTransform and cmds.listRelatives( targetShape, p=1, f=1 )[0] != cmds.listRelatives( firstShape, p=1, f=1 )[0]: continue
            if numComponentFirst == numComponentOther:
                return cmds.ls( targetShape, l=1 )[0]



def addIOShape( target ):
    
    targetShape = getShape( target )
    if not targetShape: return None
    
    targetShapeName = targetShape.split( '|' )[-1]
    oShape = sgbase.getMObject( targetShape )
    fnCurve = OpenMaya.MFnNurbsCurve(oShape)
    fnCurve.copy( oShape )
    oOrigShape = fnCurve.object()
    
    fnOrigCurve = OpenMaya.MFnNurbsCurve( oOrigShape )
    origShape = fnOrigCurve.partialPathName()
    origTr = getTransform( origShape )
    origShape = cmds.rename( origShape, targetShapeName + 'Orig' )
    
    origShape = cmds.parent( origShape, target, add=1, shape=1 )[0]
    cmds.setAttr( origShape + '.io', 1 )
    cmds.delete( origTr )
    
    return origShape



def putObject( putTargets, typ='joint', putType='boundingBoxCenter' ):
    
    putTargets = convert.singleToList( putTargets )
    for i in range( len( putTargets )):
        putTargets[i] = sgcommands.convertName( putTargets[i] )
    
    if putType == 'boundingBoxCenter':
        center = selection.getCenter( putTargets )

        if typ == 'locator':
            putTarget = cmds.spaceLocator()[0]
        elif typ == 'null':
            putTarget = cmds.createNode( 'transform' )
            cmds.setAttr( putTarget + '.dh', 1 )
        else:
            putTarget = cmds.createNode( typ )
    
        cmds.move( center.x, center.y, center.z, putTarget, ws=1 )    
        
        if len( putTargets ) == 1:
            rot = cmds.xform( putTargets[0], q=1, ws=1, ro=1 )
            cmds.rotate( rot[0], rot[1], rot[2], putTarget, ws=1 )
        
        return putTarget
    
    else:
        newObjects = []
        for putTarget in putTargets:
            mtx = cmds.getAttr( putTarget + '.wm' )
            if typ == 'locator':
                newObject = cmds.spaceLocator()[0]
            elif typ == 'null':
                newObject = cmds.createNode( 'transform' )
                cmds.setAttr( putTarget + '.dh', 1 )
            else:
                newObject = cmds.createNode( typ )
            cmds.xform( newObject, ws=1, matrix=mtx )
            newObjects.append( newObject )
        return newObjects
            



def putChild( putTarget, typ='transform', evt=0 ):
    
    if typ == 'locator':
        putObject = cmds.spaceLocator()[0]
    else:
        putObject = cmds.createNode( typ )
    
    putObject = cmds.parent( putObject, putTarget )[0]
    transform.setToDefault( putObject )
    
    return putObject
    




def getParent( dagNode ):
    
    dagNodeParent = cmds.listRelatives( dagNode, p=1, f=1 )
    if not dagNodeParent: return None
    return dagNodeParent[0]




def getChildrenJoints( topNodes ):
    
    topNodes = convert.singleToList( topNodes )
    
    returnList = []
    
    for topNode in topNodes:
        childrenJnts = cmds.listRelatives( topNode, c=1, ad=1, type='joint', f=1 )
        returnList += childrenJnts
    
    returnList = list( set( returnList ) )
    return returnList





def getTopJointChildren( topNodes ):

    if not topNodes: return []
    
    topNodes = convert.singleToList( topNodes )

    returnList = []
    for topNode in topNodes:
        if cmds.nodeType( topNode ) == 'joint':
            returnList.append( topNode )
            continue
        returnList += getTopJointChildren( cmds.listRelatives( topNode, c=1, f=1 ) )
    return returnList
    
    
    


def getNodeFromHistory( target, historyType, **options ):
    
    hists = cmds.listHistory( target, **options )
    
    if not hists: return []
    
    returnTargets = []
    for hist in hists:
        if cmds.nodeType( hist ) == historyType:
            returnTargets.append( hist )
    
    return returnTargets



def getShape( target ):
    shapes = cmds.ls( target, type='shape')
    if not shapes:
        shapes = cmds.listRelatives( target,  ad=1, s=1, f=1 )
        
    if not shapes: return None
    return OpenMaya.MFnDagNode( getDagPath( shapes[0] ) ).partialPathName()



def makeParent( targets, pName = None ):
    
    targets = convert.singleToList( targets )
    
    returnList = []
    
    for target in targets:
        targetOrigP = cmds.listRelatives( target, p=1, f=1 )
        
        targetPos = cmds.getAttr( target + '.wm' )
        targetP = cmds.createNode( 'transform' )
        
        cmds.xform( targetP, ws=1, matrix=targetPos )
        if pName:
            targetP = cmds.rename( targetP, pName )
        else:
            targetP = cmds.rename( targetP, 'P' + target )
        
        if targetOrigP:
            targetP = cmds.parent( targetP, targetOrigP[0] )[0]
    
        results = [cmds.parent( target, targetP )[0], targetP]
        
        if cmds.nodeType( results[0] ) == 'joint':
            try:cmds.setAttr( results[0] + '.r', 0,0,0 )
            except:pass
            try:cmds.setAttr( results[0] + '.jo', 0,0,0 )
            except:pass
        
        returnList.append( results )
    
    return returnList




def makeParentAndReplaceConnect( targets, evt=0 ):
    
    targets = convert.singleToList( targets )
    
    returnList = []
    
    for target in targets:
        targetOrigP = cmds.listRelatives( target, p=1, f=1 )
        
        targetPos = cmds.getAttr( target + '.wm' )
        targetP = cmds.createNode( 'transform' )
        targetP = cmds.rename( targetP, 'P'+target )
        cmds.xform( targetP, ws=1, matrix=targetPos )
        
        if targetOrigP:
            targetP = cmds.parent( targetP, targetOrigP[0] )
        
        connect.getSourceConnection( targetP, target )
        cons = cmds.listConnections( target, s=1, d=0, c=1, p=1 )
        if cons:
            for i in range( 0, len( cons ), 2 ):
                if not cmds.getAttr( cons[i], k=1 ): continue
                cmds.disconnectAttr( cons[i+1], cons[i] )
        
        results = [cmds.parent( target, targetP )[0], targetP ]
        
        if cmds.nodeType( results[0] ) == 'joint':
            try:cmds.setAttr( results[0] + '.r', 0,0,0 )
            except:pass
            try:cmds.setAttr( results[0] + '.jo', 0,0,0 )
            except:pass
        
        returnList.append( results )
    
    return returnList



def getParents( target, firstTarget='', parents = [] ):
    
    print "---", parents
    ps = cmds.listRelatives( target, p=1, f=1 )
    if not ps: return parents
    parents.insert( 0, ps[0] )
    if cmds.ls( ps[0] ) == cmds.ls( firstTarget ): return parents
    
    return getParents( ps[0], firstTarget, parents )



def makeCloneObject( target, cloneLabel= '_clone', **options  ):

    if not cmds.nodeType( target ) in ['transform', 'joint']: return None

    op_cloneAttrName = value.getValueFromDict( options, 'cloneAttrName' )

    if op_cloneAttrName:
        attrName = op_cloneAttrName
    else:
        attrName = 'cloneObject'

    targets = getParents( target )
    targets.append( target )
    
    targetCloneParent = None
    for cuTarget in targets:
        attribute.addAttr( cuTarget, ln=attrName, at='message' )
        cloneConnection = cmds.listConnections( cuTarget+'.'+attrName, s=1, d=0 )
        if not cloneConnection:
            targetClone = cmds.createNode( cmds.nodeType( cuTarget ), n= cuTarget.split( '|' )[-1]+cloneLabel )
            cmds.connectAttr( targetClone+'.message', cuTarget+'.'+attrName )

        else:
            targetClone = cloneConnection[0]
        
        targetCloneParentExpected = getParent( targetClone )
        if cmds.ls( targetCloneParentExpected ) != cmds.ls( targetCloneParent ) and targetCloneParent:
            targetClone = cmds.parent( targetClone, targetCloneParent )[0]

        cuTargetPos = cmds.getAttr( cuTarget+'.m' )
        cmds.xform( targetClone, os=1, matrix=cuTargetPos )

        targetCloneParent = targetClone
    return targetClone



def parentByOlder( targets ):
    
    targetsDagNodes = []
    for i in range( len( targets ) ):
        dagNode = OpenMaya.MFnDagNode( sgbase.getDagPath( targets[i] ) )
        targetsDagNodes.append( dagNode )
    
    for i in range( len( targetsDagNodes )-1 ):
        try:cmds.parent( targetsDagNodes[i].partialPathName(), targetsDagNodes[i+1].partialPathName() )
        except:pass
    
    for i in range( len( targets ) ):
        targets[i] = targetsDagNodes[i].partialPathName()




def makeChild( targetNode, name=None ):
    
    trNode = cmds.createNode( 'transform' )
    trNode = cmds.parent( trNode, targetNode )[0]
    transform.setToDefault( trNode )
    
    if name:
        trNode = cmds.rename( trNode, name )
    return trNode



    
    
    
def makeBrother( targetNode, name=None ):
    
    pTargetNode = cmds.listRelatives( targetNode, p=1, f=1 )
    trNode = cmds.createNode( 'transform' )
    if pTargetNode:
        trNode = cmds.parent( trNode, pTargetNode[0] )[0]
    transform.setToDefault( trNode )
    
    if name:
        trNode = cmds.rename( trNode, name )
        
    return trNode
    
    
    
def parent( targets, targetP ):
    
    targetP = getDagNode( targetP )
    
    returnTargets = []
    for target in targets:
        fnTarget = getDagNode( target )
        cmds.parent( fnTarget.partialPathName(), targetP.partialPathName() )
        returnTargets.append( fnTarget )
    
    return returnTargets
    
    
    
    