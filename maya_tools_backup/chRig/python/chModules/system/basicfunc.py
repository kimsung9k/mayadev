import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaMPx as mpx
import math

defaultMtxList = [ 1,0,0,0,  0,1,0,0, 0,0,1,0, 0,0,0,1 ]
DML = defaultMtxList

def projVector( vector, baseVector ):
    return baseVector*( (vector*baseVector)/(baseVector.length()**2))

def verticalVector( inVector, baseVector ):
    return inVector - projVector( inVector, baseVector )

def trySetAttrs( target, *attrAndValues ):
    for attr, value in attrAndValues:
        try: cmds.setAttr( target+'.'+attr, value )
        except: pass
        
def getMMatrix( target, **options ):
    os = 1 # objectSpace
    ws = 0 # worldSpace
    
    items = options.items()
    
    for item in items:
        if item[0] in ['os', 'objectSpace'] : os = item[1]; ws = 1 - item[1]
        elif item[0] in ['ws', 'worldSpace' ] : ws = item[1]; os = 1 - item[1]
    
    if os:
        mAttr = 'm'
    else:
        mAttr = 'wm'
        
    mtxList = cmds.getAttr( target+'.'+mAttr )
    MMtx = om.MMatrix()
    om.MScriptUtil.createMatrixFromList( mtxList, MMtx )
    
    return MMtx

def setMMatrix( target, MMatrix, **options ):
    os = True # objectSpace
    ws = False # worldSpace
    
    items = options.items()
    
    for item in items:
        if item[0] in ['os', 'objectSpace'] : os = item[1]; ws = not item[1]
        elif item[0] in ['ws', 'worldSpace' ] : ws = item[1]; os = not item[1]
    
    M = MMatrix
    
    mtxList = [ M(0,0),  M(0,1),  M(0,2),  M(0,3), 
                M(1,0),  M(1,1),  M(1,2),  M(1,3),
                M(2,0),  M(2,1),  M(2,2),  M(2,3),
                M(3,0),  M(3,1),  M(3,2),  M(3,3) ]
    
    cmds.xform( target, os=os, ws=ws, matrix = mtxList )
    
def setTrMMatrix( target, MMatrix, **options ):
    os = True # objectSpace
    ws = False # worldSpace
    
    items = options.items()
    
    for item in items:
        if item[0] in ['os', 'objectSpace'] : os = item[1]; ws = not item[1]
        elif item[0] in ['ws', 'worldSpace' ] : ws = item[1]; os = not item[1]
    
    M = MMatrix
    
    trans = [ M(3,0),  M(3,1),  M(3,2) ]
    
    cmds.xform( target, os=os, ws=ws, t = trans )
    
def setRotMMatrix( target, MMatrix, **options ):
    os = True # objectSpace
    ws = False # worldSpace
    
    items = options.items()
    
    for item in items:
        if item[0] in ['os', 'objectSpace'] : os = item[1]; ws = not item[1]
        elif item[0] in ['ws', 'worldSpace' ] : ws = item[1]; os = not item[1]
    
    mpxMatrix = mpx.MPxTransformationMatrix( MMatrix )
    rot = mpxMatrix.eulerRotation().asVector()
    
    cmds.xform( target, os=os, ws=ws, ro = [math.degrees( rot.x ), math.degrees( rot.y ), math.degrees( rot.z )] )
    
def getLocalMMatrix( target, parent ):
    targetMtx = getMMatrix( target, ws=1 )
    parentMtx = getMMatrix( parent, ws=1 )
    
    return targetMtx*parentMtx.inverse()

def mtxToMtxList( mtx ):
    return [ mtx(0,0), mtx(0,1), mtx(0,2), 0,
             mtx(1,0), mtx(1,1), mtx(1,2), 0,
             mtx(2,0), mtx(2,1), mtx(2,2), 0,
             mtx(3,0), mtx(3,1), mtx(3,2), 1 ]

def setRotate_keepJointOrient( mtx, jnt ):
    jntP = cmds.listRelatives( jnt, p=1 )[0]
    joValue = cmds.getAttr( jnt+'.jo' )[0]
    joMEuler = om.MEulerRotation( math.radians( joValue[0] ), math.radians( joValue[1] ), math.radians( joValue[2] ) )
    joTransform = mpx.MPxTransformationMatrix( om.MMatrix() )
    joTransform.rotateBy( joMEuler )
    jo_im = joTransform.asMatrixInverse()
        
    jntP_wim_list = cmds.getAttr( jntP+'.wim' )
    jntP_wim = om.MMatrix()
    om.MScriptUtil.createMatrixFromList( jntP_wim_list, jntP_wim )
        
    cuMtx = mtx*jntP_wim*jo_im
        
    transform = mpx.MPxTransformationMatrix( cuMtx )
    rot = transform.eulerRotation().asVector()
    
    degrees = [math.degrees( rot.x ), math.degrees( rot.y ), math.degrees( rot.z )]
    
    for i in range( len( degrees ) ):
        if degrees[i] > 180:
            degrees[i] = degrees[i]-360
        elif degrees[i] < -180:
            degrees[i] = degrees[i]+360
    cmds.setAttr( jnt+'.r', *degrees )
    
def twistVectorByVector( inVector, baseVector, rValue ):
    projV = projVector( inVector, baseVector )
    verticalV = inVector - projV
    
    dist = verticalV.length()
    
    axis1 = verticalV.normal()
    axis2 = ( baseVector ^ verticalV ).normal()
    
    radValue = math.radians( rValue )
    
    axis1V = axis1*math.cos( radValue )*dist
    axis2V = axis2*math.sin( radValue )*dist
    
    return axis1V + axis2V + projV

def getRotateFromMatrix( mtx ):
    transform = mpx.MPxTransformationMatrix( mtx )
    r = transform.eulerRotation().asVector()
    return math.degrees(r.x), math.degrees(r.y), math.degrees(r.z)