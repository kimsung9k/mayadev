import maya.cmds as cmds
import maya.OpenMaya as om
import math


def checkIsSurface( sels ):
    
    if not sels: return False
    
    selChildren = cmds.listRelatives( sels, c=1, ad=1, f=1 )
    
    if not selChildren: return False
    
    for sel in selChildren:
        
        selShapes = cmds.listRelatives( sel, s=1, f=1 )
        
        if not selShapes: continue
        
        if not cmds.nodeType( selShapes[0] ) == 'nurbsSurface':
            return False
    
    return True



def getAllSurfaceFromGroup( grp ):
    
    children = cmds.listRelatives( grp, c=1, ad=1, f=1 )
    if not children: return []
    
    surfaceShapes = []
    
    for child in children:
        
        shapes = cmds.listRelatives( child, s=1, f=1 )
        
        if not shapes: continue
        
        for shape in shapes:
            if cmds.getAttr( shape+'.io' ): continue
            if cmds.nodeType( shape ) == 'nurbsSurface':
                
                surfaceShapes.append( shape )
                
    return surfaceShapes



def getSurface( objs ):
    
    if not objs: return False
    
    shapes = []
    for obj in objs:
        if cmds.nodeType( obj ) == 'nurbsSurface':
            shapes.append( obj )

    selChildren = cmds.listRelatives( objs, c=1, ad=1, f=1 )
    if not selChildren:
        return shapes 
    selChildren.append( objs )
    
    if not selChildren: 
        return shapes
    
    surfaceShapes = []
    
    for obj in selChildren:
        objShapes = cmds.listRelatives( obj, s=1, f=1 )
    
        if not objShapes: continue
    
        for objShape in objShapes:
            if cmds.getAttr( objShape+'.io' ): continue
            if cmds.nodeType( objShape ) == 'nurbsSurface':
                surfaceShapes.append( objShape )
    
    surfaceShapes += shapes
    return surfaceShapes



def tryAddAttribute( target, **options ):
    
    items = options.items()
    
    longName = ''
    for item in items:
        if item[0] in ['ln', 'longName'] : longName = item[1]
    
    if cmds.attributeQuery( longName, node=target, ex=1 ):
        cmds.setAttr( target+'.'+longName, e=1, k=1 )
        return None
    else:
        cmds.addAttr( target, **options )
        cmds.setAttr( target+'.'+longName, e=1, k=1 )


def getLengthFromParam( fnCrv, param, toler=0.001 ):

    length = fnCrv.length()
    
    def doIt( cuMult, addValue, repeat=0 ):
        
        lengthValue = length*cuMult
        lParam = fnCrv.findParamFromLength( lengthValue )

        if repeat > 100:
            return lengthValue
        
        if math.fabs( lParam - param ) < toler:
            return lengthValue
        
        if lParam < param:
            cuMult += addValue
        else:
            cuMult -= addValue

        return doIt( cuMult, addValue/2.0, repeat+1 )
    
    return doIt( 0.5, 0.25 )


def getLastIndex( attr ):
    nodeName, attrName = attr.split( '.' )
    
    selList = om.MSelectionList()
    selList.add( nodeName )
    mObj = om.MObject()
    
    selList.getDependNode( 0, mObj )
    
    fnNode = om.MFnDependencyNode( mObj )
    wPlug = fnNode.findPlug( attrName )
    
    if not wPlug.numElements():
        return -1
    
    return wPlug[wPlug.numElements()-1].logicalIndex()


def getCvs( fnCurve ):
    
    cvs = om.MPointArray()
    
    fnCurve.getCVs( cvs )
    return cvs

def getRealCvNum( fnCurve ):
    
    cvNum  = fnCurve.numCVs()
    degree = fnCurve.degree()
    form   = fnCurve.form()
    
    cvNum -= degree

    return cvNum


def getMObject( curveName ):
    
    selList = om.MSelectionList()
    
    selList.add( curveName )
    
    mObj = om.MObject()
    selList.getDependNode( 0, mObj )

    return mObj


def getCurveShapes( sels ):
    
    sels = cmds.ls( sl=1 )
    
    curveObjects = []
    for sel in sels:
        shapes = cmds.listRelatives( sel, s=1 )
        
        if not shapes: continue
        
        for shape in shapes:
            if not cmds.getAttr( shape+'.io' ) and cmds.nodeType( shape ) == 'nurbsCurve':
                curveObjects.append( shape )
                continue
            
    return curveObjects


def addArrayMessageAttribute( node, attrName ):
    
    msgAttr = om.MFnMessageAttribute()
    
    aMessage = msgAttr.create( attrName, attrName )
    msgAttr.setArray( True )
    
    mdgMode = om.MDGModifier()
    mdgMode.addAttribute( getMObject( node ), aMessage )
    mdgMode.doIt()



def getCenterPoint( pointPoses ):
    
    minValue = [100000,100000,100000]
    maxValue = [-100000,-100000,-100000]
    
    for pos in pointPoses:
        for i in range( 3 ):
            if pos[i] < minValue[i]:
                minValue[i] = pos[i]
            if pos[i] > maxValue[i]:
                maxValue[i] = pos[i]
                
    cPoint = [0,0,0]
    
    for i in range( len(cPoint) ):
        cPoint[i] = (minValue[i]+maxValue[i])/2
        
    return cPoint



def visPointer( mPoint ):
    pos=[ mPoint.x, mPoint.y, mPoint.z ]
    grp = cmds.group( em=1 )
    cmds.setAttr( grp+'.dh', 1 )
    cmds.setAttr( grp+'.t', *pos )
    
    
def printPointer( mPoint ):
    pos=[ mPoint.x, mPoint.y, mPoint.z ]
    print pos
    
    
def surchDetailParam( fnCrv, pointV, cenPoint, cuParam, paramRate, maxParam, checkDetail = 10 ):
    
    checkDetail -= 1
    if checkDetail < 0: return cuParam
    
    increasePoint = om.MPoint()
    decreasePoint = om.MPoint()
    
    fnCrv.getPointAtParam( (maxParam + (cuParam + 0.0001))%maxParam, increasePoint )
    fnCrv.getPointAtParam( (maxParam + (cuParam - 0.0001))%maxParam, decreasePoint )
    
    incV = om.MVector( increasePoint - cenPoint )
    decV = om.MVector( decreasePoint - cenPoint )
    
    incProj = incV*( pointV*incV )/incV.length()**2
    decProj = decV*( pointV*decV )/decV.length()**2
    
    paramRate *= .5
    if incProj.length() > decProj.length():
        cuParam = ( maxParam + ( cuParam + paramRate ) ) % maxParam
    else:
        cuParam = ( maxParam + ( cuParam - paramRate ) ) % maxParam
                
    return surchDetailParam( fnCrv, pointV, cenPoint, cuParam, paramRate, maxParam, checkDetail )
    
    
def getProjectedParam( tarPoint, fnCrv, cenPoint, cross, cvLen ):

    length = fnCrv.length()
    paramRange = fnCrv.findParamFromLength( length )
    
    paramRate = paramRange/cvLen
    
    longProj = 0
    longParam = 0
    
    pointV = om.MVector( tarPoint - cenPoint )
    
    for i in range( cvLen ):
        paramPoint = om.MPoint()

        fnCrv.getPointAtParam( i*paramRate, paramPoint )
        paramV = om.MVector( paramPoint -  cenPoint )
        
        if paramV*pointV < 0: continue
        
        projV = paramV*( pointV*paramV )/paramV.length()**2
        
        if longProj < projV.length():
            longProj = projV.length()
            longParam = i*paramRate
    
    return surchDetailParam( fnCrv, pointV, cenPoint, longParam, paramRate/2, paramRange, 20 )