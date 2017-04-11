import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaMPx as mpx
import math
import basecode
import copy

ctlAllScale = 1


def mirrorShape( base, target ):
    baseShapes = cmds.listRelatives( base, s=1, f=1 )
    targetShapes = cmds.listRelatives( target, s=1, f=1 )
    colIndex = cmds.getAttr( targetShapes[0]+'.overrideColor' )
    cmds.delete( targetShapes )
    
    shapeInGeo = cmds.createNode( 'transform' )
    cmds.parent( baseShapes, shapeInGeo, add=1, shape=1 )
    
    duGeo = cmds.duplicate( shapeInGeo )[0]
    duShapes = cmds.listRelatives( duGeo, s=1, f=1 )
    
    for duShape in duShapes:
        mObj = om.MObject()
        selList = om.MSelectionList()
        selList.add( duShape )
        selList.getDependNode( 0, mObj )
        
        pointArr = om.MPointArray()
        crvNode = om.MFnNurbsCurve( mObj )
        crvNode.getCVs( pointArr )
        
        for i in range( pointArr.length() ):
            pointArr[i].x *= -1
            pointArr[i].y *= -1
            pointArr[i].z *= -1
            
        crvNode.setCVs( pointArr )
        cmds.setAttr( duShape+'.overrideColor', colIndex )
        
    cmds.parent( duShapes, target, add=1, shape=1 )
    cmds.delete( duGeo, shapeInGeo )


def setRotate_keepJointOrient( mtxList, jnt ):
    mtx = om.MMatrix()
    om.MScriptUtil.createMatrixFromList( mtxList, mtx )
        
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

def multList( listValue ):
    return [ v*ctlAllScale for v in listValue ]

def createWindow( windowName, **options ):
    if cmds.window( windowName, ex=1 ):
        cmds.deleteUI( windowName, wnd=1 )
    return cmds.window( windowName, **options )

def visConnect( attr, first, second ):
    if first:
        fcon = cmds.createNode( 'condition', n=first+'_vis' )
        cmds.connectAttr( attr, fcon+'.firstTerm' )
        cmds.setAttr( fcon+'.secondTerm', 1 )
        cmds.setAttr( first+'.v', e=1, lock=0 )
        cmds.connectAttr( fcon+'.ocr', first+'.v' )
        
    if second:
        scon = cmds.createNode( 'condition', n=second+'_vis' )
        cmds.connectAttr( attr, scon+'.firstTerm' )
        cmds.setAttr( scon+'.secondTerm', 0 )
        cmds.setAttr( second+'.v', e=1, lock=0 )
        cmds.connectAttr( scon+'.ocr', second+'.v' )

class Node( object ):
    def __init__(self, **options ):
        self.name = ''
    def __add__(self, target ):
        return self.name+target

class Transform( Node ):
    def __init__(self, **options ):
        items = options.items()
        trType = 'transform'
        for item in items:
            if item[0] in ['trType','transformType']:
                trType = item[1]
                options.pop( item[0] )
        Node.__init__( self, **options )
        if trType == 'transform':
            self.name = cmds.createNode( 'transform', **options )
        elif trType == 'joint':
            cmds.select( d=1 )
            self.name = cmds.joint( **options )

    def getChild( self, *children, **options ):
        items = options.items()
        transformPos = cmds.getAttr( self.name+'.wm' )
        
        defaultPos = False
        for item in items:
            if item[0] in ['dfp', 'defaultPos']: 
                defaultPos = item[1]
            
        for child in children:
            if not type( child ) in [ type('string'), type( u'string' ) ]:
                child = child.name
            
            objType = cmds.nodeType( child )
            childPos = cmds.getAttr( child+'.wm' )
            
            if objType == 'joint':
                childGrp = cmds.group( child )
                cmds.xform( childGrp, ws=1, matrix=transformPos )
                cmds.parent( child, self.name )
                cmds.delete( childGrp )
            else:
                cmds.parent( child, self.name )
                
            if defaultPos:
                cmds.xform( child, ws=1, matrix = [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1] )
            else:
                cmds.xform( child, ws=1, matrix = childPos )
                
    def setParent( self, parentObj, **options ):
        if not type( parentObj ) in [ type('string'), type( u'string' ) ]:
            parentObj = parentObj.name
        objPos = cmds.getAttr( parentObj+'.wm' )
        transformPos = cmds.getAttr( self.name+'.wm' )
        
        items = options.items()
        
        defaultPos = False
        for item in items:
            if item[0] in ['dfp', 'defaultPos']: 
                defaultPos = item[1]
        
        if cmds.nodeType( self.name ) == 'joint' :
            transformGrp = cmds.group( self.name )
            cmds.xform( transformGrp, ws=1, matrix= objPos )
            cmds.parent( self.name, parentObj )
            cmds.delete( transformGrp )
        else:
            cmds.parent( self.name, parentObj )
            
        if defaultPos:
            cmds.xform( self.name, ws=1, matrix = [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1] )
        else:
            cmds.xform( self.name, ws=1, matrix = transformPos )
            
    def goto(self, target ):
        if type( target ) == type( [] ):
            cmds.xform( self.name, ws=1, matrix = target )
        elif type( target ) in [type( u'string' ), type('string')]:
            mtx = cmds.getAttr( target+'.wm' )
            cmds.xform( self.name, ws=1, matrix = mtx )
            
    def defaultPos(self):
        cmds.xform( self.name, os=1, matrix=[1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1] )

class Controler( Transform ):
    def __init__(self, **options ):
        Transform.__init__( self, **options )
        self.transformGrp = cmds.createNode( 'transform', n=self.name+'_GRP' )
        Transform.setParent( self, self.transformGrp )

    def setShape(self, **options ):
        typ = 'circle'
        
        offset = [0,0,0]
        orient = [0,0,0]
        size   = [1,1,1]
        name  = 'CTL'
        
        items = options.items()
        
        for item in items:
            if item[0] in [ 'offset', 'ofs' ]: offset = item[1]; options.pop( item[0] )
            elif item[0] in [ 'orient', 'ori' ]: orient = item[1]; options.pop( item[0] )
            elif item[0] in [ 'size', 's' ]: size = item[1]; options.pop( item[0] )
            elif item[0] in [ 'name', 'n' ]: name = item[1]; options.pop( item[0] )
            
        offset = multList( offset )
        size   = multList( size )
        
        try: typ = options.pop( 'typ' )
        except: pass
        try: options['r'] *= ctlAllScale
        except: pass
        try: options['radius'] *= ctlAllScale
        except: pass
        try:options['center'] = multList( options['center'] )
        except: pass
        
        if typ == 'circle':
            ctlObj = cmds.circle( **options )[0]
            ctlShape = cmds.listRelatives( ctlObj, s=1 )[0]
        else:
            typIndex = 0
            if typ == 'quadrangle':
                typIndex = 0
            elif typ == 'box':
                typIndex = 1
            elif typ == 'switch':
                typIndex = 2
            elif typ == 'eye':
                typIndex = 3
            elif typ == 'fly':
                typIndex = 4
            elif typ == 'bar':
                typIndex = 5
            elif typ == 'move':
                typIndex = 6
            elif typ == 'pin':
                typIndex = 7
            elif typ == 'sphere':
                typIndex = 8
            
            ctlShapeNode = cmds.createNode( 'controlerShape', n= name.replace( 'CTL', 'CtlShapeNode' ) )
            cmds.setAttr( ctlShapeNode+'.controlerType', typIndex )
            cmds.setAttr( ctlShapeNode+'.offset', *offset )
            cmds.setAttr( ctlShapeNode+'.orient', *orient )
            cmds.setAttr( ctlShapeNode+'.size', *size )
            ctlShape = cmds.createNode( 'nurbsCurve', n= name.replace( 'CTL', 'CTLShape' ) )
            ctlObj = cmds.listRelatives( ctlShape, p=1 )[0]
            cmds.connectAttr( ctlShapeNode+'.outputCurve', ctlShape+'.create' )
        
        cmds.parent( ctlShape, self.name, add=1, shape=1 )
        cmds.delete( ctlObj )
        cmds.rename( ctlShape, self.name+'Shape' )
        self.controlerShape = ctlShape

    def setParent( self, parentObj, **options ):
        name = copy.copy( self.name )
        self.name = copy.copy( self.transformGrp )
        Transform.setParent( self, parentObj, **options )
        self.name = name
        
    def gotoGrp(self, target ):
        if type( target ) == type( [] ):
            cmds.xform( self.transformGrp, ws=1, matrix = target )
        elif type( target ) == type( 'string' ):
            mtx = cmds.getAttr( target+'.wm' )
            cmds.xform( self.transformGrp, ws=1, matrix = mtx )
            
    def setColor(self, colorIndex ):
        shapes = cmds.listRelatives( self.name, s=1 )
        for shape in shapes:
            cmds.setAttr( shape + ".overrideEnabled", 1 )
            cmds.setAttr( shape + ".overrideColor", colorIndex )
            

def trySetAttr( attr, value ):
    try:cmds.setAttr( attr, value )
    except: pass

            
def controlerSetColor( ctl, colorIndex ):
    shapes = cmds.listRelatives( ctl, s=1 )
    for shape in shapes:
        cmds.setAttr( shape + ".overrideEnabled", 1 )
        cmds.setAttr( shape + ".overrideColor", colorIndex )
        
def setColor( ctl, colorIndex ):
    cmds.setAttr( ctl + ".overrideEnabled", 1 )
    cmds.setAttr( ctl + ".overrideColor", colorIndex )
        
def transformSetColor( transform, colorIndex ):
    cmds.setAttr( transform + ".overrideEnabled", 1 )
    cmds.setAttr( transform + ".overrideColor", colorIndex )

def addHelpTx( target, textName ):
    attrName = '____'
    
    while(1):
        if not cmds.attributeQuery( attrName, node=target, ex=1 ):
            break
        else:
            attrName += '_'
            
    cmds.addAttr( target, ln=attrName, at='enum', en=textName )
    cmds.setAttr( target+'.'+attrName, e=1, cb=1 )

def putControler( transformNode, **options ):
    typ = 'circle'
    
    offset = [0,0,0]
    orient = [0,0,0]
    size   = [1,1,1]
    name  = 'CTL'
    
    items = options.items()
    
    for item in items:
        if item[0] in [ 'offset', 'ofs' ]: offset = item[1]
        elif item[0] in [ 'orient', 'ori' ]: orient = item[1]
        elif item[0] in [ 'size', 's' ]: size = item[1]
        elif item[0] in [ 'name', 'n' ]: name = item[1]
    
    offset = multList( offset )
    size   = multList( size )
        
    try: typ = options.pop( 'typ' )
    except: pass
    try: options['radius'] *= ctlAllScale
    except: pass
    try:options['center'] = multList( options['center'] )
    except: pass
    try:options['r'] *= ctlAllScale
    except: pass
    
    if typ == 'circle':
        ctl = cmds.circle( **options )[0]
    else:
        typIndex = 0
        if typ == 'quadrangle':
            typIndex = 0
        elif typ == 'box':
            typIndex = 1
        elif typ == 'switch':
            typIndex = 2
        elif typ == 'eye':
            typIndex = 3
        elif typ == 'fly':
            typIndex = 4
        elif typ == 'bar':
            typIndex = 5
        elif typ == 'move':
            typIndex = 6
        elif typ == 'pin':
            typIndex = 7
        elif typ == 'sphere':
            typIndex = 8
        
        ctlNode = cmds.createNode( 'controlerShape', n= name.replace( 'CTL', 'CtlShapeNode' ) )
        cmds.setAttr( ctlNode+'.controlerType', typIndex )
        cmds.setAttr( ctlNode+'.offset', *offset )
        cmds.setAttr( ctlNode+'.orient', *orient )
        cmds.setAttr( ctlNode+'.size', *size )
        ctlShape = cmds.createNode( 'nurbsCurve', n= name.replace( 'CTL', 'CTLShape' ) )
        ctl = cmds.listRelatives( ctlShape, p=1 )[0]
        
        cmds.connectAttr( ctlNode+'.outputCurve', ctlShape+'.create' )
        
    goToSamePosition( ctl, transformNode )
    ctlGrp = addParent( ctl, '_GRP' )
    return ctl, ctlGrp

def addControlerShape( target, **options ):
    typ = 'circle'
    
    offset = [0,0,0]
    orient = [0,0,0]
    size   = [1,1,1]
    name= 'CTL'
    
    items = options.items()
    
    for item in items:
        if item[0] in [ 'offset', 'ofs' ]: offset = item[1]; options.pop( item[0] )
        elif item[0] in [ 'orient', 'ori' ]: orient = item[1]; options.pop( item[0] )
        elif item[0] in [ 'size', 's' ]: size = item[1]; options.pop( item[0] )
        elif item[0] in [ 'name', 'n' ]: name = item[1]; options.pop( item[0] )
    
    offset = multList( offset )
    size   = multList( size )
        
    try: typ = options.pop( 'typ' )
    except: pass
    try: options['r'] *= ctlAllScale
    except: pass
    try: options['radius'] *= ctlAllScale
    except: pass
    try:options['center'] = multList( options['center'] )
    except: pass
    
    if typ == 'circle':
        ctlObj = cmds.circle( **options )[0]
        ctlShape = cmds.listRelatives( ctlObj, s=1 )[0]
    else:
        typIndex = 0
        if typ == 'quadrangle':
            typIndex = 0
        elif typ == 'box':
            typIndex = 1
        elif typ == 'switch':
            typIndex = 2
        elif typ == 'eye':
            typIndex = 3
        elif typ == 'fly':
            typIndex = 4
        elif typ == 'bar':
            typIndex = 5
        elif typ == 'move':
            typIndex = 6
        elif typ == 'pin':
            typIndex = 7
        elif typ == 'sphere':
            typIndex = 8
        
        ctlNode = cmds.createNode( 'controlerShape', n= name.replace( 'CTL', 'CtlShapeNode' ) )
        cmds.setAttr( ctlNode+'.controlerType', typIndex )
        cmds.setAttr( ctlNode+'.offset', *offset )
        cmds.setAttr( ctlNode+'.orient', *orient )
        cmds.setAttr( ctlNode+'.size', *size )
        ctlShape = cmds.createNode( 'nurbsCurve', n= name.replace( 'CTL', 'CTLShape' ) )
        ctlObj = cmds.listRelatives( ctlShape, p=1 )[0]
        
        cmds.connectAttr( ctlNode+'.outputCurve', ctlShape+'.create' )
        
    cmds.parent( ctlShape, target, add=1, shape=1 )
    cmds.delete( ctlObj )
    
    cmds.rename( ctlShape, target+'Shape' )

class AttrEdit:
    def __init__(self, *nodes ):
        self.nodes = nodes
        
    def lockAttrs( self, *attrs ):
        for node in self.nodes:
            for attr in attrs:
                cmds.setAttr( node+'.'+attr, e=1, lock=1 )
            
    def hideAttrs( self, *attrs ):
        for node in self.nodes:
            for attr in attrs:
                cmds.setAttr( node+'.'+attr, e=1, k=0 )
            
    def lockAndHideAttrs( self, *attrs ):
        for node in self.nodes:
            for attr in attrs:
                cmds.setAttr( node+'.'+attr, e=1, lock=1, k=0, cb=0 )
            
    def setAttrs( self, value, *attrs, **options ):
        for node in self.nodes:
            for attr in attrs:
                cmds.setAttr( node+'.'+attr, value, **options )
                
    def addAttr( self, **options ):
        k  = False
        cb = False
        
        try: k  = options.pop( 'k' )
        except: pass
        try: cb = options.pop( 'cb' )
        except: pass
        
        for node in self.nodes:
            cmds.addAttr( node, **options )
            try: attrName = options.pop( 'ln' )
            except: attrName = options.pop( 'longName' )
            cmds.setAttr( node+'.'+attrName, k=k, cb=cb )

class connectSameAttr:
    def __init__(self, first, second ):
        self.first = first
        self.second = second
    
    def doIt(self, *attrs, **options ):
        for attr in attrs:
            cmds.connectAttr( self.first+'.'+attr, self.second+'.'+attr, **options )
            
def getDist( data ):
    if type( data ) == type( om.MVector() ):
        return data.length()
    elif type( data ) == type( om.MPoint() ):
        return math.sqrt( data.x**2 + data.y**2 + data.z**2 )
    elif type( data ) == type( [] ):
        return math.sqrt( data[0]**2 + data[1]**2 + data[2]**2 )
    
def parentOrder( *transforms ):
    for i in range( len( transforms )-1 ):
        cmds.parent( transforms[i], transforms[i+1] )
        
def makeAimObject( child, parent, **options ):
    dlaOn = False
    optionItems = options.items()
    
    aimAxis = 0
    upAxis = 1
    targetAxis = 2
    inverseAim = False
    inverseUp = False
    replaceTarget = ' '
    replace = ''
    upType = 'normal'
    upObject = None
    addName = 'AimObj'
    
    for opItem in optionItems:
        if opItem[0] == 'axis': aimAxis = opItem[1]; continue
        if opItem[0] == 'upAxis': upAxis = opItem[1]; continue
        if opItem[0] == 'inverseAim': inverseAim = opItem[1]; continue
        if opItem[0] == 'inverseUp': inverseUp = opItem[1]; continue
        if opItem[0] == 'replaceTarget' : replaceTarget = opItem[1]; continue
        if opItem[0] == 'replace' : replace = opItem[1]; continue
        if opItem[0] == 'upType' : upType = opItem[1]; continue
        if opItem[0] == 'upObject' : upObject = opItem[1]; continue
        if opItem[0] == 'addName'  : addName = opItem[1]; continue
        
    targetAxis = 3-aimAxis-targetAxis

    aimObject = cmds.createNode( 'transform', n=parent.replace( replaceTarget, replace ) + addName )
    
    if upType == 'normal' :
        mltMtxDcmp = cmds.createNode( 'multMatrixDecompose', n= parent.replace( replaceTarget, replace ) +'Dcmp' )
        ffmNode = cmds.createNode( 'fourByFourMatrix', n= parent.replace( replaceTarget, replace ) +'FFM' )
        smtOriNode = cmds.createNode( 'smartOrient', n= parent.replace( replaceTarget, replace ) +'SmtOri' )
            
        cmds.setAttr( mltMtxDcmp+'.invt', inverseAim )
        AttrEdit( aimObject ).lockAndHideAttrs( 't', 's', 'v' )
        cmds.setAttr( aimObject +'.dla', dlaOn )
        cmds.parent( aimObject, parent )
        cmds.setAttr( smtOriNode+'.aimAxis', aimAxis )
            
        cmds.connectAttr( child+'.wm', mltMtxDcmp+'.i[0]' )
        cmds.connectAttr( parent+'.wim', mltMtxDcmp+'.i[1]' )
        cmds.connectAttr( mltMtxDcmp+'.otx', ffmNode+'.i%d0' % aimAxis )
        cmds.connectAttr( mltMtxDcmp+'.oty', ffmNode+'.i%d1' % aimAxis )
        cmds.connectAttr( mltMtxDcmp+'.otz', ffmNode+'.i%d2' % aimAxis )
        cmds.connectAttr( ffmNode+'.output', smtOriNode+'.inputMatrix' )
        cmds.connectAttr( smtOriNode+'.outAngle', aimObject+'.r' )
        
        return aimObject, mltMtxDcmp
    
    elif upType == 'object':
        childPoseMltDcmp = cmds.createNode( 'multMatrixDecompose', n= child.replace( replaceTarget, replace ) +'MtxDcmp' )
        upObjPoseMltDcmp = cmds.createNode( 'multMatrixDecompose', n= upObject.replace( replaceTarget, replace ) +'MtxDcmp' )
        vvNode = cmds.createNode( 'verticalVector', n=parent.replace( replaceTarget, replace+'VV' ) )
        ffmNode = cmds.createNode( 'fourByFourMatrix', n=parent.replace( replaceTarget, replace+'FFM' ) )
        dcmpNode = cmds.createNode( 'decomposeMatrix', n=parent.replace( replaceTarget, replace+'Dcomp' ) )
        
        cmds.setAttr( childPoseMltDcmp+'.invt', inverseAim )
        cmds.setAttr( upObjPoseMltDcmp+'.invt', inverseUp )
        AttrEdit( aimObject ).lockAttrs( 't', 's', 'v' )
        cmds.parent( aimObject, parent )
        cmds.setAttr( aimObject+'.dla', dlaOn )
        
        cmds.connectAttr( child+'.wm', childPoseMltDcmp+'.i[0]' )
        cmds.connectAttr( parent+'.wim', childPoseMltDcmp+'.i[1]' )
        cmds.connectAttr( upObject+'.wm', upObjPoseMltDcmp+'.i[0]' )
        cmds.connectAttr( parent+'.wim', upObjPoseMltDcmp+'.i[1]' )
        cmds.connectAttr( childPoseMltDcmp+'.ot', vvNode+'.baseVector' )
        cmds.connectAttr( upObjPoseMltDcmp+'.ot', vvNode+'.iv' )
        cmds.connectAttr( childPoseMltDcmp+'.otx', ffmNode+'.i%d0' % aimAxis )
        cmds.connectAttr( childPoseMltDcmp+'.oty', ffmNode+'.i%d1' % aimAxis )
        cmds.connectAttr( childPoseMltDcmp+'.otz', ffmNode+'.i%d2' % aimAxis )
        cmds.connectAttr( vvNode+'.ovx', ffmNode+'.i%d0' % upAxis )
        cmds.connectAttr( vvNode+'.ovy', ffmNode+'.i%d1' % upAxis )
        cmds.connectAttr( vvNode+'.ovz', ffmNode+'.i%d2' % upAxis )
        cmds.connectAttr( vvNode+'.cvx', ffmNode+'.i%d0' % targetAxis )
        cmds.connectAttr( vvNode+'.cvy', ffmNode+'.i%d1' % targetAxis )
        cmds.connectAttr( vvNode+'.cvz', ffmNode+'.i%d2' % targetAxis )
        cmds.connectAttr( ffmNode+'.output', dcmpNode+'.imat' )
        cmds.connectAttr( dcmpNode+'.or', aimObject+'.r' )
        
        return aimObject, childPoseMltDcmp

def betweenRigInAimObject( betweenObjs, aimObject, **options ):
    betweenObjs = basecode.oneToList( betweenObjs )
    
    replaceTarget = ' '
    replace = ''
    axis = 0
    dcmp = None
    globalMult = 1
    
    optionItems = options.items()
    for opItem in optionItems:
        if opItem[0] == 'replaceTarget' : replaceTarget = opItem[1]; continue
        if opItem[0] == 'replace' : replace = opItem[1]; continue
        if opItem[0] == 'axis' : axis = opItem[1]; continue
        if opItem[0] == 'dcmp' : dcmp = opItem[1]; continue
        if opItem[0] == 'globalMult' : globalMult = opItem[1]; continue
    
    try:
        smtOri = cmds.listConnections( aimObject, type='smartOrient' )[0]
        ffm = cmds.listConnections( smtOri, type='fourByFourMatrix' )[0]
        dcmp = cmds.listConnections( ffm, type='' )[0]
        axis = cmds.getAttr( smtOri+'.aimAxis' )
    except: pass
    
    poseList = ['tx', 'ty', 'tz']
    axisPose = poseList.pop(axis)
    
    distNode = cmds.createNode( 'distanceBetween', n=aimObject.replace( 'AimObj', 'dist' ) )
    cmds.connectAttr( dcmp+'.ot', distNode+'.point1' )
    
    divValue = globalMult*1.0/( len( betweenObjs )+1 )
    for betweenObj in betweenObjs:
        i = betweenObjs.index( betweenObj )
        betweenObjGrp = cmds.createNode( 'transform', n=betweenObj+'_ctlGRP' )
        multNode = cmds.createNode( 'multDoubleLinear', n=betweenObj.replace( replaceTarget, replace )+'PoseMlt' )
        cmds.setAttr( multNode+'.input2', (i+1)*divValue )
        
        AttrEdit( betweenObjGrp ).lockAttrs( poseList[0], poseList[1], 'r', 's', 'v' )
        
        cmds.connectAttr( distNode+'.distance', multNode+'.input1' )
        cmds.connectAttr( multNode+'.output', betweenObjGrp+'.'+axisPose )
        
        cmds.parent( betweenObjGrp, aimObject )
        cmds.parent( betweenObj, betweenObjGrp )
        
        AttrEdit( betweenObj ).lockAttrs( 'r', 's', 'v' )

def addParent( obj, addName = '_GRP' ):
    objP = cmds.listRelatives( obj, p=1 )
    
    pose = cmds.getAttr( obj+'.wm' )
    grp = cmds.createNode( 'transform', n=obj+addName )
    cmds.xform( grp, ws=1, matrix=pose )
    cmds.parent( obj, grp )
    
    if objP:
        cmds.parent( grp, objP )
        
    return grp


def tryConnect( first, second ):
    try: cmds.connectAttr( first, second, f=1 )
    except: pass
    
    


def listConnections( node, attrList, **options ):
    
    allCons = []
    
    for attr in attrList:
        cons = cmds.listConnections( node+'.'+attr, **options )
        if not cons: continue
        allCons += cons
        
    return allCons
    


def constraint( first, second, **options ):
    translate = True
    rotate = True
    scale = False
    shear = False
    
    optionItems = options.items()
    for opItem in optionItems:
        if opItem[0] == 't': translate=opItem[1]; continue
        if opItem[0] == 'r': rotate=opItem[1]; continue
        if opItem[0] == 's': scale=opItem[1]; continue
        if opItem[0] == 'sh': shear=opItem[1]; continue
    
    mmdc = cmds.createNode( 'multMatrixDecompose', n=second+'_mmdc' )
    cmds.connectAttr( first+'.wm', mmdc+'.i[0]' )
    cmds.connectAttr( second+'.pim', mmdc+'.i[1]' )
    
    if translate: 
        '''
        try:cmds.connectAttr( mmdc+'.ot', second+'.t' )
        except:pass
        '''
        tryConnect( mmdc+'.otx', second+'.tx' )
        tryConnect( mmdc+'.oty', second+'.ty' )
        tryConnect( mmdc+'.otz', second+'.tz' )
    if rotate :
        '''
        try:cmds.connectAttr( mmdc+'.or', second+'.r' )
        except:pass
        '''
        tryConnect( mmdc+'.orx', second+'.rx' )
        tryConnect( mmdc+'.ory', second+'.ry' )
        tryConnect( mmdc+'.orz', second+'.rz' )
    if scale : 
        '''
        try:cmds.connectAttr( mmdc+'.os', second+'.s', f=1 )
        except: pass
        '''
        tryConnect( mmdc+'.osx', second+'.sx' )
        tryConnect( mmdc+'.osy', second+'.sy' )
        tryConnect( mmdc+'.osz', second+'.sz' )
    if shear :
        '''
        try:cmds.connectAttr( mmdc+'.osh', second+'.sh', f=1 )
        except: pass
        '''
        tryConnect( mmdc+'.oshx', second+'.shxy' )
        tryConnect( mmdc+'.oshy', second+'.shxz' )
        tryConnect( mmdc+'.oshz', second+'.shyz' )
    
    return mmdc

def decomposeDirectConnection( first, second, **options ):
    translate = True
    rotate = True
    scale = False
    shear = False
    component = False
    
    optionItems = options.items()
    for opItem in optionItems:
        if opItem[0] == 't': translate=opItem[1]; continue
        if opItem[0] == 'r': rotate=opItem[1]; continue
        if opItem[0] == 's': scale=opItem[1]; continue
        if opItem[0] == 'sh': shear=opItem[1]; continue
        if opItem[0] == 'component': component=opItem[1]; continue
        
    dcmp = cmds.createNode( 'decomposeMatrix', n=second+'_dcmp' )
    cmds.connectAttr( first+'.wm', dcmp+'.imat' )
    
    if component:
        cmds.connectAttr( dcmp+'.ot', second )
        return dcmp
    
    if translate: cmds.connectAttr( dcmp+'.ot', second+'.t' )
    if rotate : cmds.connectAttr( dcmp+'.or', second+'.r' )
    if scale : cmds.connectAttr( dcmp+'.os', second+'.s' )
    if shear : cmds.connectAttr( dcmp+'.osh', second+'.sh' )
    
    return dcmp

def hierarchyCopyConnections( topTransform, **options ):
    replaceTarget = ' '
    replace = ''
    addName = ''
    trans = True
    rot   = True
    scale = False
    shear = False
    jo = False
    typ   = 'transform'
    
    optionItems = options.items()
    for opItem in optionItems:
        if opItem[0] == 'replaceTarget' : replaceTarget = opItem[1]; continue
        elif opItem[0] == 'replace' : replace = opItem[1]; continue
        elif opItem[0] == 'addName' : addName = opItem[1]; continue
        elif opItem[0] in ['t','translate'] : trans = opItem[1]; continue
        elif opItem[0] in ['r','rotate'] : rot = opItem[1]; continue
        elif opItem[0] in ['s', 'scale'] : scale = opItem[1]; continue
        elif opItem[0] in ['sh','shear'] : shear = opItem[1]; continue
        elif opItem[0] in ['jo','jointOrient'] : jo = opItem[1]; continue
        elif opItem[0] == 'typ'  : typ   = opItem[1]; continue
    
    connectAttrList = []
    if trans: connectAttrList.append( 't' )
    if rot:   connectAttrList.append( 'r' )
    if scale: connectAttrList.append( 's' )
    if shear: connectAttrList.append( 'sh' )
    if jo   : connectAttrList.append( 'jo' )
    
    copyObjectName = topTransform.replace( replaceTarget, replace )+addName
    if copyObjectName == topTransform:
        addName = '_copy'
        
    def doit( topTransform ):
        if not cmds.nodeType( topTransform ) in ['transform','joint']:
            return None
        
        copyObject = cmds.createNode( typ, n=topTransform.replace( replaceTarget, replace )+addName )
        for con in connectAttrList:
            cmds.connectAttr( topTransform+'.'+con, copyObject+'.'+con )
        children = cmds.listRelatives( topTransform, c=1 )
        
        if children:
            for child in children:
                doitChild = doit( child )
                if doitChild:
                    cmds.parent( doitChild, copyObject )
                    transformDefault( doitChild )
        return copyObject
    
    return doit( topTransform )

def goToSamePosition( obj, target ):
    wt = cmds.xform( target, q=1, ws=1, t=1 )[:3]
    wr = cmds.xform( target, q=1, ws=1, ro=1 )[:3]
    cmds.move( wt[0], wt[1], wt[2], obj, ws=1 )
    cmds.rotate( wr[0], wr[1], wr[2], obj, ws=1 )
    
def followAdd( first, second ):
    mtxDcmp = cmds.listConnections( second, type='multMatrixDecompose' )
    if mtxDcmp:
        followMtx = cmds.listConnections( mtxDcmp[0], type='followMatrix' )
        if followMtx:      
            FM = followMtx[0]
            inputs = cmds.listConnections( FM+'.inputMatrix', p=1, c=1 )
            
            if inputs:
                connectAbleIndex = inputs[-2].split( '[' )[1].replace( ']', '' )+1
            else:
                connectAbleIndex = 0
            cmds.connectAttr( first+'.wm', FM+'.inputMatrix[%d]' % connectAbleIndex )
            
            return FM
    
    FM = cmds.createNode( 'followMatrix', n= second+'_followMtx' )
    mtxDcmp = cmds.createNode( 'multMatrixDecompose', n= second+'._mtxDcmp' )
            
    cmds.connectAttr( first+'.wm', FM+'.originalMatrix', f=1 )
    cmds.connectAttr( FM+'.outputMatrix', mtxDcmp+'.i[0]', f=1 )
    cmds.connectAttr( second+'.pim', mtxDcmp+'.i[1]', f=1 )
            
    cmds.connectAttr( mtxDcmp+'.ot', second+'.t', f=1 )
    cmds.connectAttr( mtxDcmp+'.or', second+'.r', f=1 )
            
    return FM

def getChildMtx( child, parent, addName = '_childPosMtx' ):
    mtx = cmds.createNode( 'multMatrix', n=child+addName )
    cmds.connectAttr( child+'.wm', mtx+'.i[0]')
    cmds.connectAttr( parent+'.wim', mtx+'.i[1]' )
    return mtx

def getChildMtxDcmp( child, parent, addName = '_childPosMtxDcmp' ):
    mtxDcmp = cmds.createNode( 'multMatrixDecompose', n=child+addName )
    cmds.connectAttr( child+'.wm', mtxDcmp+'.i[0]')
    cmds.connectAttr( parent+'.wim', mtxDcmp+'.i[1]' )
    return mtxDcmp

def transformDefault( *transforms ):
    for transform in transforms:
        if not type( transform ) in [ type( u'string' ), type('string') ]:
            transform = transform.name
        try: cmds.setAttr( transform+'.tx', 0 )
        except: pass
        try: cmds.setAttr( transform+'.ty', 0 )
        except: pass
        try: cmds.setAttr( transform+'.tz', 0 )
        except: pass
        try: cmds.setAttr( transform+'.rx', 0 )
        except: pass
        try: cmds.setAttr( transform+'.ry', 0 )
        except: pass
        try: cmds.setAttr( transform+'.rz', 0 )
        except: pass
        try: cmds.setAttr( transform+'.sx', 1 )
        except: pass
        try: cmds.setAttr( transform+'.sy', 1 )
        except: pass
        try: cmds.setAttr( transform+'.sz', 1 )
        except: pass
        try: cmds.setAttr( transform+'.shx', 0 )
        except: pass
        try: cmds.setAttr( transform+'.shy', 0 )
        except: pass
        try: cmds.setAttr( transform+'.shz', 0 )
        except: pass
        try: cmds.setAttr( transform+'.jox', 0 )
        except: pass
        try: cmds.setAttr( transform+'.joy', 0 )
        except: pass
        try: cmds.setAttr( transform+'.joz', 0 )
        except: pass

def replaceShape( first, target ):
    targetShape = cmds.listRelatives( target, s=1 )[0]
    cmds.delete( targetShape )
    duObj = cmds.duplicate( first )[0]
    
    chs = cmds.ls( cmds.listRelatives( duObj, c=1, f=1 ), tr=1 )
    if chs: cmds.delete( chs )
        
    duShape = cmds.listRelatives( duObj, s=1 )
        
    cmds.parent( duShape, target, add=1, shape=1 )
    cmds.delete( duObj )
    
    duShape = cmds.rename( duShape, targetShape )
    return duShape
    
def reverseSurfShape( target ):
    MObj = om.MObject()
    selList = om.MSelectionList()
    selList.add( target )
    selList.getDependNode( 0, MObj )
        
    surf = om.MFnNurbsSurface( MObj )
    pointArr = om.MPointArray()
    surf.getCVs( pointArr )
        
    for i in range( pointArr.length() ):
        point = pointArr[i]
        pointArr.set( i, -point.x, -point.y, -point.z )
            
    surf.setCVs( pointArr )
    
def reverseCurveShape( target ):
    MObj = om.MObject()
    selList = om.MSelectionList()
    selList.add( target )
    selList.getDependNode( 0, MObj )
        
    crv = om.MFnNurbsCurve( MObj )
    pointArr = om.MPointArray()
    crv.getCVs( pointArr )
        
    for i in range( pointArr.length() ):
        point = pointArr[i]
        pointArr.set( i, -point.x, -point.y, -point.z )
            
    crv.setCVs( pointArr )
    
def getSkinedMeshByJnt( jnts ):
    meshs = cmds.ls( type='mesh' )
    
    outputMeshs = []
    meshObjs = []
    
    for mesh in meshs:
        meshP = cmds.listRelatives( mesh, p=1, f=1 )[0]
        
        if not meshP in meshObjs:
            meshObjs.append( meshP )
            
    for jnt in jnts:
        try:
            skinCls = cmds.listConnections( jnt+'.worldMatrix', type='skinCluster' )
            if not skinCls:
                skinCls = []
        except: continue
        
        for meshObj in meshObjs:
            try:
                meshHists = cmds.listHistory( meshObj, pdo=1 )
                
                for meshHist in meshHists:
                    if meshHist in skinCls:
                        if not meshObj in outputMeshs:
                            outputMeshs.append( meshObj )
            except: pass
    
    return outputMeshs

def getHistory( object, type ):
    hists = cmds.listHistory( object, pdo=1 )
    
    returnHists = []
    for hist in hists:
        if cmds.nodeType( hist ) == type:
            returnHists.append( hist )
            
    return returnHists

def cleanMesh( meshObj ):
    shapes = cmds.listRelatives( meshObj, s=1, f=1 )
    
    for shape in shapes:
        if cmds.getAttr( shape+'.intermediateObject' ):
            cmds.delete( shape )
            
def reconnectContraint():
    attrs = ['ot', 'or', 'os', 'osh']
    mtxDcmps = cmds.ls( type='multMatrixDecompose' )
    for mtxDcmp in mtxDcmps:
        target = cmds.listConnections( mtxDcmp+'.ot' )
        if target:
            cmds.disconnectAttr( mtxDcmp+'.ot', target+'.t' )
            cmds.connectAttr( )
            
def repairConstraint():
    mtxObjs = cmds.ls( type='multMatrixDecompose' )
    mtxObjs += cmds.ls( type='decomposeMatrix' )
    mtxObjs += cmds.ls( type='blendTwoMatrixDecompose' )
    for mtx in mtxObjs:
        cons = cmds.listConnections( mtx, d=1, s=0, c=1, p=1, type='transform' )
        
        if not cons:
            continue
        
        outputs = cons[::2]
        inputs = cons[1::2]
        
        for i in range( len( outputs ) ):
            output = outputs[i]
            input = inputs[i]
            
            if input.find( 'jointOrient' ):
                continue
            
            try:
                cmds.connectAttr( output+'X', input+'X' )
                cmds.connectAttr( output+'Y', input+'Y' )
                cmds.connectAttr( output+'Z', input+'Z' )
                
                cmds.disconnectAttr( output, input )
            except: pass
            
def pInvRotConst( obj ):
    blMtx = cmds.createNode( 'blendTwoMatrixDecompose', n=obj+'_blMtxDcmp' )
    objP = cmds.listRelatives( obj, p=1 )[0]
    cmds.connectAttr( objP+'.m', blMtx+'.inMatrix1' )
    cmds.connectAttr( blMtx+'.or', obj+'.r' )
            
def matchMesh( poseMesh, targetMesh ):
    selList = om.MSelectionList()
    selList.add( poseMesh )
    selList.add( targetMesh )
    
    poseObj = om.MObject()
    targetObj = om.MObject()
    
    selList.getDependNode( 0, poseObj )
    selList.getDependNode( 1, targetObj )
    
    fnPoseMesh = om.MFnMesh( poseObj )
    fnTargetMesh = om.MFnMesh( targetObj )
    
    poseMeshPntArr = om.MPointArray()
    fnPoseMesh.getPoints( poseMeshPntArr )
    
    fnTargetMesh.setPoints( poseMeshPntArr )
    
def rebindCurrentPose( trNode ):
    hists = cmds.listHistory( trNode, pdo=1 )

    for hist in hists:
        if not cmds.nodeType( hist ) == 'skinCluster': continue
        
        cons = cmds.listConnections( hist+'.matrix', type='joint', c=1, p=1, s=1, d=0 )
        
        outputs = cons[1::2]
        inputs = cons[::2]
        
        for i in range( len( outputs ) ):
            mtx = cmds.getAttr( outputs[i].replace( 'worldMatrix', 'worldInverseMatrix' ) )
            cmds.setAttr( inputs[i].replace( 'matrix', 'bindPreMatrix' ), mtx, type='matrix' )
            
def setTransformAttrToOther( base, target ):
    t = cmds.getAttr( base+'.t' )[0]
    r = cmds.getAttr( base+'.r' )[0]
    s = cmds.getAttr( base+'.s' )[0]
    sh = cmds.getAttr( base+'.sh' )[0]
    try:jo = cmds.getAttr( base+'.jo' )[0]
    except:pass
    
    try:cmds.setAttr( target+'.tx', t[0] )
    except:pass
    try:cmds.setAttr( target+'.ty', t[1] )
    except:pass
    try:cmds.setAttr( target+'.tz', t[2] )
    except:pass
    try:cmds.setAttr( target+'.rx', r[0] )
    except:pass
    try:cmds.setAttr( target+'.ry', r[1] )
    except:pass
    try:cmds.setAttr( target+'.rz', r[2] )
    except:pass
    try:cmds.setAttr( target+'.sx', s[0] )
    except:pass
    try:cmds.setAttr( target+'.sy', s[1] )
    except:pass
    try:cmds.setAttr( target+'.sz', s[2] )
    except:pass
    try:cmds.setAttr( target+'.shx', sh[0] )
    except:pass
    try:cmds.setAttr( target+'.shy', sh[1] )
    except:pass
    try:cmds.setAttr( target+'.shz', sh[2] )
    except:pass
    try:cmds.setAttr( target+'.jox', jo[0] )
    except:pass
    try:cmds.setAttr( target+'.joy', jo[1] )
    except:pass
    try:cmds.setAttr( target+'.joz', jo[2] )
    except:pass

def setShapeToOther( base, target ):
    baseShapes = cmds.listRelatives( base, s=1, f=1 )
    targetShapes = cmds.listRelatives( target, s=1, f=1 )
    
    cmds.delete( targetShapes )
    
    targetShapes = cmds.parent( baseShapes, target, shape=1, add=1 )
    
    for targetShape in targetShapes:
        cmds.rename( targetShape, target+'Shape' )

        
def lockAttrs( node, *attrs ):
    for attr in attrs:
        cmds.setAttr( node+'.'+attr, e=1, lock=1 )