import maya.cmds as cmds
import maya.OpenMaya as om
import math
import maya.mel as mel


def addArrayMessageAttribute( node, attrName ):
    
    msgAttr = om.MFnMessageAttribute()
    
    aMessage = msgAttr.create( attrName, attrName )
    msgAttr.setArray( True )
    
    mdgMode = om.MDGModifier()
    mdgMode.addAttribute( node, aMessage )
    mdgMode.doIt()


def getPlugFromString( attr ):
    
    def plugAttr( plug, attrName ):
        
        try:
            origAttrName, indexSep = attrName[0].split( '[' )
        except:
            origAttrName = attrName
            indexSep = None
        
        i=0
        
        while ( i < plug.numChildren() ):
           
            childPlug = plug.child( i )
            
            if childPlug.name() == origAttrName:
                
                if not indexSep:
                    nextPlug = childPlug
                
                else:
                    index = int( indexSep[0] )
                    nextPlug = childPlug[ index ]
                    
                if not len( attrName ) > 1:
                    return nextPlug
                else:
                    return plugAttr( nextPlug, attrName[1:] )
            
            i+=1
        
    
    def findAttrPlug( fnNode, attrName ):

        try:
            origAttrName, indexSep = attrName[0].split( '[' )
        except:
            return fnNode.findPlug( attrName[0] )
        
        plug = fnNode.findPlug( origAttrName )
        
        index = int( indexSep[0] )
        nextPlug = plug.elementByLogicalIndex( index )
        
        if not len( attrName ) > 1:
            return nextPlug
        else:
            return plugAttr( nextPlug, attrName[1:] )
            
    splitData = attr.split( '.' )
    
    node = splitData[0]
    attrName = splitData[1:]
    
    mObj = om.MObject()
    
    selList = om.MSelectionList()
    selList.add( node )
    selList.getDependNode( 0, mObj )
    
    fnNode = om.MFnDependencyNode( mObj )
    
    return findAttrPlug( fnNode, attrName )


def clearArrayElement( targetAttr ):
    
    targetAttrPlug = getPlugFromString( targetAttr )
    
    numElements = targetAttrPlug.numElements()
    
    delIndies = []
    for i in range( numElements ):
        logicalIndex = targetAttrPlug[i].logicalIndex()
        
        if not cmds.listConnections( targetAttr+'[%d]' % logicalIndex ):
            delIndies.append( logicalIndex )
            
    for delIndex in delIndies:
        cmds.removeMultiInstance( '%s[%d]' %( targetAttr, delIndex ) )
    

def setAttrApi( attr, value ):
    
    plug = getPlugFromString( attr )
    
    if type( value ) == type( True ):
        plug.setBool( value )
    elif type( value ) == type( 1 ):
        plug.setInt( value )
    elif type( value ) == type( 1.0 ):
        plug.setDouble( value )
    elif type( value ) == type( '' ):
        plug.setString( value )


def disconnectAttrApi( attr1, attr2 ):
    
    plug1 = getPlugFromString( attr1 )
    plug2 = getPlugFromString( attr2 )
    
    mode = om.MDGModifier()
    mode.disconnect( plug1, plug2 )
    mode.doIt()

        
def connectAttrApi( attr1, attr2 ):
    
    cons = cmds.listConnections( attr2, s=1, d=0, p=1, c=1 )
    if cons:
        disconnectAttrApi( cons[1], cons[0] )
    
    plug1 = getPlugFromString( attr1 )
    plug2 = getPlugFromString( attr2 )
    
    mode = om.MDGModifier()
    mode.connect( plug1, plug2 )
    mode.doIt()


def tryConnect( first, second ):
    
    if not cmds.isConnected( first, second ):
        cmds.connectAttr( first, second, f=1 )


def setColor( shape, colorIndex ):
    cmds.setAttr( shape + ".overrideEnabled", 1 )
    cmds.setAttr( shape + ".overrideColor", colorIndex )


def getSourceCurveAttr( shape ):
    
    cons = cmds.listConnections( shape+'.create', s=1, d=0, p=1, c=1 )
    shapeP = cmds.listRelatives( shape, p=1 )[0]
    
    if not cons:
        duObj = cmds.duplicate( shape )[0]
        duShapes = cmds.listRelatives( duObj, s=1 )
        
        targetOrig = ''
        for shape in duShapes:
            if not cmds.getAttr( shape+'.io' ):
                targetOrig = shape
                break
        
        cmds.setAttr( targetOrig+'.io', 1 )
        cmds.parent( targetOrig, shapeP, s=1, add=1 )
        
        cmds.delete( duObj )
        
        return targetOrig+'.local'
    else:
        return cons[1]
    
    
def checkIsSurface( sels ):
    
    for sel in sels:
        
        selShape = cmds.listRelatives( sel, s=1 )[0]
        if not cmds.nodeType( selShape ) == 'nurbsSurface':
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
    
    surfaceShapes = []
    
    for obj in objs:
        objShapes = cmds.listRelatives( obj, s=1, f=1 )
    
        for objShape in objShapes:
            if cmds.getAttr( objShape+'.io' ): continue
            if cmds.nodeType( objShape ):
                surfaceShapes.append( objShape )
            
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

def getRealCvNum( crvShape ):
    
    fnCurve = om.MFnNurbsCurve( getMObject( crvShape ) )
    
    cvNum  = fnCurve.numCVs()
    degree = fnCurve.degree()
    form   = fnCurve.form()
    
    if form == 3:
        cvNum -= degree

    return cvNum


def getRealCvNum_fn( fnCurve ):
    
    cvNum  = fnCurve.numCVs()
    degree = fnCurve.degree()
    form   = fnCurve.form()
    
    if form == 3:
        cvNum -= degree

    return cvNum


def getMObject( curveName ):
    
    selList = om.MSelectionList()
    
    selList.add( curveName )
    
    mObj = om.MObject()
    selList.getDependNode( 0, mObj )

    return mObj


def getCurveLength( curveShape ):
    
    fnCrv = om.MFnNurbsCurve( getMObject( curveShape ) )
    return fnCrv.length()


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


def getCenterPoint_fn( fnCurve ):
    
    bb = fnCurve.boundingBox()
    
    bbMin = bb.min()
    bbMax = bb.max()
    
    return om.MPoint( ( bbMin.x + bbMax.x )/2, ( bbMin.y + bbMax.y )/2, ( bbMin.z + bbMax.z )/2 )



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