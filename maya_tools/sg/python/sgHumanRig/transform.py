import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import convert
import value
import selection
import attribute



def setTranslateDefault():
    sels = cmds.ls( sl=1 )
    attrs = ['tx', 'ty', 'tz' ]
    for sel in sels:
        for attr in attrs:
            try:cmds.setAttr( sel + "." + attr, 0 )
            except:pass
            


def setRotateDefault():
    sels = cmds.ls( sl=1 )
    attrs = ['rx', 'ry', 'rz' ]
    for sel in sels:
        for attr in attrs:
            try:cmds.setAttr( sel + "." + attr, 0 )
            except:pass



def setScaleDefault():
    sels = cmds.ls( sl=1 )
    attrs = ['sx', 'sy', 'sz' ]
    for sel in sels:
        for attr in attrs:
            try:cmds.setAttr( sel + "." + attr, 1 )
            except:pass



def setShearDefault():
    sels = cmds.ls( sl=1 )
    attrs = ['shearXY', 'shearXZ', 'shearYZ' ]
    for sel in sels:
        for attr in attrs:
            try:cmds.setAttr( sel + "." + attr, 0 )
            except:pass



def setTransformDefault():
    
    setTranslateDefault()
    setRotateDefault()
    setScaleDefault()
    setShearDefault()
    
    




    



def setJointOrientZero( joints ):
    
    joints = convert.singleToList( joints )
    for joint in joints:
        cmds.setAttr( joint + '.jo', 0,0,0 )




def freezeJoint( joints, evt=0 ):
    
    import math
    joints = convert.singleToList( joints )
    
    for joint in joints:
        mat = convert.listToMatrix( cmds.getAttr( joint + '.m' ) )
        rot = OpenMaya.MTransformationMatrix( mat ).eulerRotation().asVector()
        cmds.setAttr( joint + '.jo', math.degrees( rot.x ), math.degrees( rot.y ), math.degrees( rot.z ) )
        cmds.setAttr( joint + '.r', 0,0,0 )
        


def setOrientAsTarget( rotTargets, target, evt=0 ):
    
    rotTargets = convert.singleToList( rotTargets )
    rotValue = cmds.xform( target, q=1, ws=1, ro=1 )
    
    for rotTarget in rotTargets:
        cmds.rotate( rotValue[0], rotValue[1], rotValue[2], rotTarget, ws=1 )
    cmds.select( rotTargets )





def lookAt( rotTarget, aimTargets, evt=0 ):
    
    rotMtx = convert.listToMatrix( cmds.getAttr( rotTarget + '.wm' ) )
    rotPos = OpenMaya.MPoint( rotMtx[3] )
    aimPos    = selection.getCenter( aimTargets )
    direction = OpenMaya.MVector( aimPos - rotPos ).normal()
    
    maxDotValue, maxDotIndex = value.maxDotIndexAndValue( direction, rotMtx )
    
    baseDir = [[1,0,0], [0,1,0], [0,0,1]][maxDotIndex]
    
    if maxDotValue < 0: direction *= -1
    rotValue = cmds.angleBetween( v1=baseDir, v2=[direction.x, direction.y, direction.z], er=1 )
    
    cmds.rotate( rotValue[0], rotValue[1], rotValue[2], rotTarget, ws=1 )
    cmds.select( rotTarget )



def setOrientByChild( targetJnt, evt=0 ):
    
    children = cmds.listRelatives( targetJnt, c=1, f=1 )
    if not children: return None
    
    childrenMats = []
    for child in children:
        childrenMats.append( cmds.getAttr( child + '.wm' ) )
    
    lookAt( targetJnt, children )
    
    for i in range( len(children) ):
        cmds.xform( children[i], ws=1, matrix= childrenMats[i] )
    



def setMatrixAsTarget( editTarget, lookTarget ):
    cmds.xform( editTarget, ws=1, matrix= cmds.getAttr( lookTarget+'.wm' ) )
   




def freezeByParent( targets, evt=0 ):
    
    targets = convert.singleToList( targets )
    
    for target in targets:
        pTarget = cmds.listRelatives( target, p=1 )[0]
        cmds.xform( pTarget, ws=1, matrix = cmds.getAttr( target + '.wm' ) )
        try:cmds.xform( target, ws=1, matrix= cmds.getAttr( pTarget + '.wm' ) )
        except:pass



def makeCenter( sels, evt=0 ):
    
    import math
    import copy
    
    for sel in sels:
        matList = cmds.getAttr( sel + '.wm' )
        mat = convert.listToMatrix(matList)
        
        maxXIndex = 0
        maxXValue = 0
        
        minXIndex = 1
        minXValue = 100000000.0
        
        for i in range( 3 ):
            v = OpenMaya.MVector( mat[i] )
            if math.fabs( v.x ) > maxXValue:
                maxXValue = math.fabs( v.x )
                maxXIndex = i
            if math.fabs( v.x ) < minXValue:
                minXValue = math.fabs( v.x )
                minXIndex = i
        
        minVector = OpenMaya.MVector( mat[minXIndex] )
        maxVector = OpenMaya.MVector( mat[maxXIndex] )
        
        maxVector.y = 0
        maxVector.z = 0
        minVector.x = 0
        
        maxVector.normalize()
        minVector.normalize()
        otherVector = maxVector ^ minVector
        
        if (maxXIndex + 1) % 3 != minXIndex:
            otherVector *= -1
        
        allIndices = [0,1,2]
        allIndices.remove( minXIndex )
        allIndices.remove( maxXIndex )
        
        otherIndex = allIndices[0]
        
        newMatList = copy.copy( matList )
        
        newMatList[ minXIndex * 4 + 0 ] = minVector.x
        newMatList[ minXIndex * 4 + 1 ] = minVector.y
        newMatList[ minXIndex * 4 + 2 ] = minVector.z
        
        newMatList[ maxXIndex * 4 + 0 ] = maxVector.x
        newMatList[ maxXIndex * 4 + 1 ] = maxVector.y
        newMatList[ maxXIndex * 4 + 2 ] = maxVector.z
        
        newMatList[ otherIndex * 4 + 0 ] = otherVector.x
        newMatList[ otherIndex * 4 + 1 ] = otherVector.y
        newMatList[ otherIndex * 4 + 2 ] = otherVector.z
        
        newMatList[3*4] = 0
        
        newMat = convert.listToMatrix( newMatList )
        
        trMat = OpenMaya.MTransformationMatrix( newMat )
        trans = trMat.getTranslation( OpenMaya.MSpace.kWorld )
        rot   = trMat.eulerRotation().asVector()
        
        cmds.move( trans.x, trans.y, trans.z, sel, ws=1 )
        cmds.rotate( math.degrees(rot.x), math.degrees(rot.y), math.degrees(rot.z), sel, ws=1 )
        
        
def mirrorObject( sels, evt=0 ):
    
    for sel in sels:
        matList = cmds.getAttr( sel + '.wm' )
        matList[1]  *= -1
        matList[2]  *= -1
        matList[4]  *= -1
        matList[8]  *= -1
        matList[12] *= -1
        
        cmds.xform( sel, ws=1, matrix= matList )
        


def duplicateMirror( sels, evt=0 ):
    
    duSels = []
    
    for sel in sels:
        duSel = cmds.duplicate( sel )
        duSel = cmds.rename( duSel[0], convert.sideString( sel ) )
        duSels.append( duSel )
    
    cmds.select( duSels )
    mirrorObject(duSels)
    
    
    
def setTransformAsTarget( src, trg, evt=0 ):
    
    trans = cmds.xform( trg, q=1, ws=1, t=1 )
    rots  = cmds.xform( trg, q=1, ws=1, ro=1 )
    
    cmds.move( trans[0], trans[1], trans[2], src, ws=1 )
    cmds.rotate( rots[0], rots[1], rots[2], src, ws=1 )




def createOrigPosition( dagNodes ):
    
    dagNodes = convert.singleToList( dagNodes )
    
    for dagNode in dagNodes:
        attribute.addAttr( dagNode, ln='origMatrix', dt='matrix')
        cmds.setAttr( dagNode + '.origMatrix', cmds.getAttr( dagNode + '.matrix' ), type='matrix' )


def goToOrigPosition( dagNodes ):
    
    dagNodes = convert.singleToList( dagNodes )
    
    for dagNode in dagNodes:
        if not cmds.attributeQuery( 'origMatrix', node=dagNode, ex=1 ): continue
        cmds.xform( dagNode, os=1, matrix = cmds.getAttr( dagNode + '.origMatrix' ) )


        
def setToDefault( dagNodes ):
    
    for dagNode in convert.singleToList( dagNodes ):
        mtx = convert.matrixToList( OpenMaya.MMatrix() )
        cmds.xform( dagNode, os=1, matrix=mtx )
        
