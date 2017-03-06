import maya.cmds as cmds
import sgModelDag



def duplicateToTargetAndParent( duBase, target ):
    
    mtx = cmds.getAttr( duBase+'.matrix' )
    duObject = cmds.duplicate( duBase )[0]
    
    cmds.parent( duObject, target )
    
    cmds.xform( duObject, os=1, matrix= mtx )



def duplicateToTargetAndConnect( duBase, target ):
    
    duObject = cmds.duplicate( duBase )[0]
    
    mmdc = cmds.createNode( 'multMatrixDecompose' )
    cmds.connectAttr( target+'.wm', mmdc+'.i[0]' )
    cmds.connectAttr( duObject+'.pim', mmdc+'.i[1]' )
    cmds.connectAttr( mmdc+'.ot', duObject+'.t' )
    cmds.connectAttr( mmdc+'.or', duObject+'.r' )



def makeParentTargetPosition( positionTarget, target ):
    
    targetP = cmds.listRelatives( target, p=1, f=1 )[0]
    positionTargetMatrix = cmds.getAttr( positionTarget+'.wm' )
    grp = cmds.createNode( 'transform', n= 'P'+target )
    cmds.xform( grp, ws=1, matrix=positionTargetMatrix )
    
    grp = cmds.parent( grp, targetP )[0]
    cmds.parent( target, grp )
    
    return grp



def addChild( obj, addName = 'C' ):
    
    child = cmds.createNode( 'transform', n= addName + obj )
    child = cmds.parent( child, obj )[0]
    
    return child



def addParent( obj, addName = 'P' ):
    objP = cmds.listRelatives( obj, p=1, f=1 )
    
    pose = cmds.getAttr( obj+'.wm' )
    grp = cmds.createNode( 'transform', n=addName + obj )
    cmds.xform( grp, ws=1, matrix=pose )
    obj = cmds.parent( obj, grp )[0]
    
    if objP:
        grp = cmds.parent( grp, objP )[0]
        
    return obj, grp



def parentObjectToTargetParent( first, second ):
    
    secondP = cmds.listRelatives( second, p=1, f=1 )[0]
    first = cmds.parent( first, secondP )
    
    return first



def setMatrixToTarget( shapeObject, target ):
    
    shapeObject = sgModelDag.getTransform( shapeObject )
    origParent= cmds.listRelatives( shapeObject, p=1, f=1 )
    
    if origParent:
        if cmds.ls( origParent[0] ) == cmds.ls( target ):
            origParent = -1 # keep dag position
        else:
            print shapeObject, target
            shapeObject = cmds.parent( shapeObject, target )[0]
    else:
        shapeObject = cmds.parent( shapeObject, target )[0]
    
    cmds.makeIdentity( shapeObject, apply=True, t=1, r=1, s=1 )
    cmds.xform( shapeObject, piv=[0,0,0] )
    
    if origParent == -1:
        cmds.select( shapeObject )
    elif origParent:
        shapeObject = cmds.parent( shapeObject, origParent )[0]
    else:
        shapeObject = cmds.parent( shapeObject, w=1 )[0]
    return shapeObject



def duplicateObjectToTarget( source, target ):
    
    duSource = cmds.duplicate( source )[0]
    
    wmtx = cmds.getAttr( target+'.wm' )
    
    cmds.xform( duSource, ws=1, matrix=wmtx )
    
    return duSource




def replaceObject( source, target ):
    
    import sgBFunction_connection
    
    sgBFunction_connection.getSourceConnection( target, source )
    
    sourceParent = cmds.listRelatives( source, p=1, f=1 )
    targetParent = cmds.listRelatives( target, p=1, f=1 )
    
    mtx = cmds.getAttr( target+'.wm' )
    cmds.xform( source, ws=1, matrix=mtx )
    cmds.delete( target )
    
    if targetParent:
        if sourceParent:
            if cmds.ls( targetParent[0] ) != cmds.ls( sourceParent[0] ):
                cmds.parent( source, targetParent[0] )
        else:
            cmds.parent( source, targetParent[0] )




def getGeometryConstObj( target ):
    
    import sgModelFileAndPath
    
    sgModelFileAndPath.autoLoadPlugin( 'sgMatrix' )
    
    import sgRigAttribute
    
    sgRigAttribute.addAttr( target, ln='geometryConstObj', at='message' )
    
    cons = cmds.listConnections( target+'.geometryConstObj', s=1, d=0 )
    if cons: return cons[0]
    
    geomConstObj = cmds.createNode( 'transform', n= 'GeomConstObj_'+target )
    
    mmdc = cmds.createNode( 'sgMultMatrixDecompose' )
    cmds.connectAttr( target+'.wm', mmdc+'.i[0]' )
    cmds.connectAttr( geomConstObj+'.pim', mmdc+'.i[1]' )
    cmds.connectAttr( mmdc+'.ot', geomConstObj+'.t' )
    cmds.connectAttr( mmdc+'.or', geomConstObj+'.r' )
    cmds.connectAttr( mmdc+'.os', geomConstObj+'.s' )
    cmds.connectAttr( mmdc+'.osh', geomConstObj+'.sh' )
    
    cmds.connectAttr( geomConstObj+'.message', target+'.geometryConstObj' )
    
    return geomConstObj



mc_setMatrixToTarget = '''import maya.cmds as cmds
import sgRigDag
sels = cmds.ls( sl=1 )

firsts = sels[::2]
seconds = sels[1::2]
for i in range( len( seconds ) ):
    sgRigDag.setMatrixToTarget( firsts[i], seconds[i] )
'''


mc_duplicateObjectToTarget = '''import maya.cmds as cmds
import sgRigDag
sels = cmds.ls( sl=1 )

src = sels[0]
targets = sels[1:]
for target in targets:
    sgRigDag.duplicateObjectToTarget( src, target )
'''


mc_replaceObject = '''import maya.cmds as cmds
import sgRigDag
sels = cmds.ls( sl=1 )

firsts = sels[::2]
seconds = sels[1::2]
for i in range( len( seconds ) ):
    sgRigDag.replaceObject( firsts[i], seconds[i] )
'''