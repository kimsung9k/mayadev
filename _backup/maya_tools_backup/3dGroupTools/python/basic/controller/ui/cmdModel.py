import maya.cmds as cmds
import maya.OpenMaya as om
import functions
import math
import model


def createController( targetClass, shapeOption ):
    
    addCurve = False
    addPoly = False
    
    if shapeOption == 'Curve':
        addCurve = True
    elif shapeOption == 'Polygon':
        addPoly = True
    else:
        addCurve = True
        addPoly = True
    
    
    crvPoints = targetClass.pointList
    polyNode  = targetClass.polygonNode
    options   = targetClass.options
    
    jnt = cmds.createNode( 'transform', n='Put_CTL' )
    
    if addCurve:
        crvObject = cmds.curve( p=crvPoints, d=1 )
        crvShape = cmds.listRelatives( crvObject, s=1 )[0]
        cmds.parent( crvShape, jnt, add=1, shape=1 )
        cmds.rename( crvShape, jnt+'Shape' )
        cmds.delete( crvObject )
    
    if addPoly:
        polyName = jnt+'Shape1'
        if polyNode:
            node = cmds.createNode( polyNode )
            meshShape = cmds.createNode( 'mesh' )
            meshObject = cmds.listRelatives( meshShape, p=1 )[0]
            cmds.connectAttr( node+'.output', meshShape+'.inMesh' )
            if options:
                for attr, value in options:
                    cmds.setAttr( node+'.'+attr, value )
            meshShape = cmds.parent( meshShape, jnt, add=1, shape=1 )
            cmds.delete( meshObject )
            
            cmds.rename( meshShape, polyName )
        else:
            vtxCount = targetClass.vtxCount
            polyCount = targetClass.polyCount
            PointArr = functions.pointListToPointArr( targetClass.polyPointList )
            CountArr = functions.intListToIntArr( targetClass.polyCountList )
            ConnectArr = functions.intListToIntArr( targetClass.polyConnectList )
            
            fnMesh = om.MFnMesh()
            fnMesh.create( vtxCount, polyCount, PointArr, CountArr, ConnectArr, functions.getMObject( jnt ) )
            
            cmds.rename( fnMesh.fullPathName(), polyName )
        
        shader = functions.addCostomShader( polyName )
        
        if not cmds.attributeQuery( 'transparency', node=jnt, ex=1 ):
            cmds.addAttr( jnt, ln='transparency', min=0, max=1, dv=0.5 )
            cmds.setAttr( jnt+'.transparency', e=1, k=1 )
        revNode = cmds.createNode( 'reverse' )
        
        cmds.connectAttr( jnt+'.transparency', revNode+'.inputX' )
            
        cmds.connectAttr( jnt+'.transparency', shader+'.outTransparencyR' )
        cmds.connectAttr( jnt+'.transparency', shader+'.outTransparencyG' )
        cmds.connectAttr( jnt+'.transparency', shader+'.outTransparencyB' )
    
    return jnt




def buildMatrixByRot( rot ):
    
    trMtx = om.MTransformationMatrix()
    trMtx.rotateTo( om.MEulerRotation( math.radians( rot[0] ), math.radians( rot[1] ), math.radians( rot[2] ) ) )
    return trMtx.asMatrix()




def buildMatrixByScale( scale ):
    
    util = om.MScriptUtil()
    util.createFromDouble( scale[0], scale[1], scale[2] )
    ptr = util.asDoublePtr()
    trMtx = om.MTransformationMatrix()
    trMtx.setScale( ptr, om.MSpace.kTransform )
    return trMtx.asMatrix()



def editShapeByMatrix( target, mmtx ):
    
    targetShapes = cmds.listRelatives( target, s=1 )
    
    for shape in targetShapes:
        if cmds.nodeType( shape ) == 'mesh':
            fnMesh = om.MFnMesh( functions.getMObject( shape ) )
            points = om.MPointArray()
            fnMesh.getPoints( points )
            for i in range( points.length() ):
                points.set( points[i]*mmtx, i )
                cmds.move( points[i].x, points[i].y, points[i].z, shape+'.vtx[%d]' % i, os=1 )
        
        elif cmds.nodeType( shape ) == 'nurbsCurve':
            fnCurve = om.MFnNurbsCurve( functions.getMObject( shape ) )
            points = om.MPointArray()
            fnCurve.getCVs( points )
            for i in range( points.length() ):
                points.set( points[i]*mmtx, i )
                cmds.move( points[i].x, points[i].y, points[i].z, shape+'.cv[%d]' % i, os=1 )
                
                
                
def ucGetBasePoints():
    
    sels = cmds.ls( sl=1 )
    
    model.fnMeshList = []
    model.fnCrvList = []
    model.meshPoints = []
    model.crvPoints = []
    
    for target in sels:
        targetShapes = cmds.listRelatives( target, s=1 )
        
        for shape in targetShapes:
            if cmds.nodeType( shape ) == 'mesh':
                fnMesh = om.MFnMesh( functions.getMObject( shape ) )
                points = om.MPointArray()
                fnMesh.getPoints( points )
                model.fnMeshList.append( fnMesh )
                model.meshPoints.append( points )
            
            elif cmds.nodeType( shape ) == 'nurbsCurve':
                fnCurve = om.MFnNurbsCurve( functions.getMObject( shape ) )
                points = om.MPointArray()
                fnCurve.getCVs( points )
                model.fnCrvList.append( fnCurve )
                model.crvPoints.append( points )
                
                

def ucSetBasePoints():
    for i in range( len( model.fnMeshList ) ):
        fnMesh = model.fnMeshList[i]
        points = model.meshPoints[i]
        fnMesh.setPoints( points )

    for i in range( len( model.fnCrvList ) ):
        fnCurve = model.fnCrvList[i]
        points  = model.crvPoints[i]
        fnCurve.setCVs( points )

            

def ucSetPointsDrag( scale ):
    
    mtx = buildMatrixByScale( scale )
    
    for i in range( len( model.fnMeshList ) ):
        fnMesh = model.fnMeshList[i]
        points = model.meshPoints[i]
        newPoints = om.MPointArray()
        newPoints.setLength( points.length() )
        for j in range( newPoints.length() ):
            newPoints.set( points[j]*mtx, j )
        fnMesh.setPoints( newPoints )
    
    cmds.undoInfo( swf=0 )
    for i in range( len( model.fnCrvList ) ):
        fnCurve = model.fnCrvList[i]
        points  = model.crvPoints[i]
        newPoints = om.MPointArray()
        newPoints.setLength( points.length() )
        for j in range( newPoints.length() ):
            newPoint = points[j]*mtx
            cmds.move( newPoint.x, newPoint.y, newPoint.z, fnCurve.name() + '.cv[%d]' % j, os=1  )
    cmds.undoInfo( swf=1 )

            
            
def ucSetPoints( scale ):
    
    mtx = buildMatrixByScale( scale )
    
    newPoint = om.MPoint()
    for i in range( len( model.fnMeshList ) ):
        fnMesh = model.fnMeshList[i]
        points = model.meshPoints[i]
        for j in range( points.length() ):
            newPoint = points[j]*mtx
            cmds.move( newPoint.x, newPoint.y, newPoint.z, fnMesh.name() + '.vtx[%d]' % j, os=1  )
    
    for i in range( len( model.fnCrvList ) ):
        fnCurve = model.fnCrvList[i]
        points  = model.crvPoints[i]
        for j in range( points.length() ):
            newPoint = points[j]*mtx
            cmds.move( newPoint.x, newPoint.y, newPoint.z, fnCurve.name() + '.cv[%d]' % j, os=1  )
        


def editShapeByRot( ctl, rot ):
    mtx = buildMatrixByRot( rot )
    editShapeByMatrix( ctl, mtx )

                
def ucEditShapeByRot( rot, *args ):
    mtx = buildMatrixByRot( rot )
    
    sels = cmds.ls( sl=1 )
    for sel in sels:
        editShapeByMatrix( sel, mtx )
    
    
def editShapeByScale( ctl, scale ):
    
    mtx = buildMatrixByScale( scale )
    editShapeByMatrix( ctl, mtx )
    

def ucEditShapeByScale( scale, *args ):

    mtx = buildMatrixByScale( scale )
    
    sels = cmds.ls( sl=1 )
    for sel in sels:
        editShapeByMatrix( sel, mtx )
    

    
    
def ucCreateControler( targetClass, shapeOption, poseOption, *args ):
    
    def makeGRP( target ):
    
        targetP = cmds.listRelatives( target, p=1 )
        
        mtx = cmds.getAttr( target +'.wm' )
        grp = cmds.createNode( 'transform', n=target + '_GRP' )
        cmds.xform( grp, ws=1, matrix=mtx )
        target = cmds.parent( target, grp )[0]
        
        if cmds.nodeType( target ) == 'joint':
            jntMtx = cmds.getAttr( target+'.m' )
            mMtx = om.MMatrix()
            om.MScriptUtil.createMatrixFromList( jntMtx, mMtx )
            trMtx = om.MTransformationMatrix( mMtx )
            rotV = trMtx.eulerRotation().asVector()
            rot = [ math.degrees( rotV.x),  math.degrees( rotV.y ), math.degrees( rotV.z ) ]
            cmds.setAttr( target+'.r', 0,0,0 )
            cmds.setAttr( target+'.jo', *rot )
        
        if targetP:
            cmds.parent( grp, targetP[0] )
            
        return target
    

    sels = cmds.ls( sl=1 )
    
    trans = False
    rotate = False
    
    if poseOption == 'Translate':
        trans = True
    elif poseOption == 'Rotate':
        rotate = True
    else:
        trans = True
        rotate = True
    
    if not sels:
        jnt = createController( targetClass, shapeOption )
        cmds.select( jnt )
    else:
        jnts = []
        for sel in sels:
            jnt = createController( targetClass, shapeOption )
            if not cmds.nodeType( sel ) in ['transform', 'joint']: continue
            if trans:
                pos = cmds.xform( sel, q=1, ws=1, t=1 )
                cmds.move( pos[0], pos[1], pos[2], jnt, ws=1 )
            if rotate:
                rot = cmds.xform( sel, q=1, ws=1, ro=1 )
                cmds.rotate( rot[0], rot[1], rot[2], jnt, ws=1 )
            
            jnt = makeGRP( jnt )
            jnts.append( jnt )
        cmds.select( jnts )