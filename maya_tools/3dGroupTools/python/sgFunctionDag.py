import maya.cmds as cmds
import maya.OpenMaya as om
import sgModelData
import sgModelDag
import sgModelConvert



def parent( targets, parentTarget ):
    
    targets = sgModelData.getArragnedList( targets )
    if not parentTarget: return targets

    parentedTargets = []
    for target in targets:
        parentTargetCu = cmds.listRelatives( target, p=1, f=1 )
        if not parentTargetCu:
            parentedTargets += cmds.parent( target, parentTarget )
            continue
        if cmds.ls( parentTarget )[0] == cmds.ls( parentTargetCu[0] )[0]:
            parentedTargets.append( target )
        else:
            parentedTargets+=cmds.parent( target, parentTarget )
    return parentedTargets



def createMesh( mMatrix, numVtx, numPoly, pointArr, countArr, connectArr, uArray=None, vArray=None ):
    
    trMesh = cmds.createNode( 'transform' )
    
    oTrMesh = sgModelDag.getMObject( trMesh )
    
    if uArray:
        om.MFnMesh().create( numVtx, numPoly, pointArr, countArr, connectArr, uArray, vArray, oTrMesh )
    else:
        om.MFnMesh().create( numVtx, numPoly, pointArr, countArr, connectArr, oTrMesh )
    
    matrix = sgModelConvert.convertMMatrixToMatrix( mMatrix )
    cmds.xform( trMesh, ws=1, matrix= matrix )
    
    return trMesh



def copyShape( shapeObject, **options ):
    
    try:shapeName = cmds.listRelatives( shapeObject, s=1, f=1 )[0]
    except: return None
    
    cons = cmds.listConnections( shapeObject+'.message', p=1, c=1 )
    if cons:
        inputCons = cons[1::2]
        for inputCon in inputCons:
            if inputCon.find( 'copyTarget' ) != -1:
                return cmds.ls( inputCon.split( '.' )[0], l=1 )[0]
    
    trShape = cmds.createNode( 'transform' )
    
    oShape = sgModelDag.getMObject( shapeName )
    oTrShape = sgModelDag.getMObject( trShape )
    
    if cmds.nodeType( shapeName ) == 'mesh':
        fnMesh = om.MFnMesh()
        fnMesh.copy( oShape, oTrShape )
    elif cmds.nodeType( shapeName ) == 'nurbsCurve':
        fnCurve = om.MFnNurbsCurve()
        fnCurve.copy( oShape, oTrShape )
    elif cmds.nodeType( shapeName ) == 'nurbsSurface':
        fnSurf = om.MFnNurbsSurface()
        fnSurf.copy( oShape, oTrShape )
    
    copyMatrix = sgModelData.getValueFromDict( options, 'copyMatrix' )
    
    if copyMatrix:
        cmds.xform( trShape, ws=1, matrix=cmds.getAttr( shapeName+'.wm' ) )
    
    try:cmds.sets( trShape, e=1, forceElement = 'initialShadingGroup' )
    except:pass
    
    cmds.addAttr( trShape, ln='copyTarget', at='message' )
    cmds.connectAttr( shapeObject+'.message', trShape+'.copyTarget' )
    
    return cmds.ls( trShape, l=1 )[0]



def copyTransform( transformName ):
    
    trObject = cmds.createNode( 'transform' )
    cmds.xform( trObject, ws=1, matrix=cmds.getAttr( transformName+'.wm' ) )
    
    return cmds.ls( trObject, l=1 )[0]



def copyTransformNoRepeat( transformName ):

    cons = cmds.listConnections( transformName+'.message', p=1, c=1 )
    if cons:
        inputCons = cons[1::2]
        for inputCon in inputCons:
            if inputCon.find( 'copyTarget' ) != -1:
                return cmds.ls( inputCon.split( '.' )[0], l=1 )[0]
    
    trObject = cmds.createNode( 'transform' )
    mtx = cmds.xform( transformName, q=1, ws=1, matrix=1 )
    cmds.xform( trObject, ws=1, matrix=mtx )
    cmds.addAttr( trObject, ln='copyTarget', at='message' )
    cmds.connectAttr( transformName+'.message', trObject+'.copyTarget' )
    return cmds.ls( trObject, l=1 )[0]



def duplicateHierarchy( target ):
    
    targetParents = sgModelDag.getParents( target )
    
    parentObject = None
    copyedObjects = []
    for targetParent in targetParents:
        copyTarget = copyTransformNoRepeat( targetParent )
        copyTarget = parent( copyTarget, parentObject )[0]
        copyedObjects.append( cmds.ls( copyTarget, l=1 )[0] )
        parentObject = copyedObjects[-1]
        
    targetShape = cmds.listRelatives( target, s=1 )
    if not targetShape:
        copyedObject = copyTransformNoRepeat( target )
        copyedObject = parent( copyedObject, parentObject )[0]
        copyedObjects += cmds.ls( copyedObject, l=1 )
    else:
        copyedObject = copyShape( target, copyMatrix=1 )
        copyedObject = parent( copyedObject, parentObject )[0]
        copyedObjects += cmds.ls( copyedObject, l=1 )

    return copyedObjects



def makeParent( target ):
    
    targetPos = cmds.getAttr( target+'.wm' )
    grp = cmds.group( em=1, n= 'P'+target )
    cmds.xform( grp, ws=1, matrix=targetPos )
    cmds.parent( target, grp )
    
    return grp




def getSurfaceColorValues( point, surf ):
    
    closeSurf = cmds.createNode( 'closestPointOnSurface' )
    surfShape = cmds.listRelatives( surf, s=1 )[0]
    shadingEngins = cmds.listConnections( surfShape+'.instObjGroups[0]' )
    engin = shadingEngins[0]
    
    shaders = cmds.listConnections( engin+'.surfaceShader' )
    
    textures = cmds.listConnections( shaders[0]+'.color' )
    
    cmds.connectAttr( surfShape+'.worldSpace', closeSurf+'.inputSurface' )
    
    cmds.setAttr( closeSurf+'.inPosition', *point )

    colors = cmds.colorAtPoint( textures[0], u=cmds.getAttr( closeSurf+'.u' ),
                                            v=cmds.getAttr( closeSurf+'.v' ) )

    return colors



def makeTransform( fullPathName ):
    
    if fullPathName[0] == '|':
        fullPathName = fullPathName[1:]
    
    splits = fullPathName.split( '|' )
    
    parentTarget = None
    for i in range( len( splits ) ):
        if cmds.objExists( '|'.join( splits[:i+1] ) ):
            parentTarget = '|'.join( splits[:i+1] )
            continue
        trNode = cmds.createNode( 'transform' )
        if parentTarget:
            trNode = cmds.parent( trNode, parentTarget )
        trNode = cmds.rename( trNode, splits[i] )
        parentTarget = trNode