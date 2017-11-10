from maya import cmds, OpenMaya
import random


class data:
    handles = []
    startWind = 123
    startWindDecrease = 173
    endWind = 180
    targetLocator = 'pointer'
    
    attachStrangthPointer = 'attachPointer'
    attachLengthPointer = 'attachLengthPointer'
    maxVelocityDist = 26
    maxDisAttachVelocityDist = 16
    disattachVelocityDrag = 0.8
    addVelocityDist = 5.6
    addVelocityDrag = 0.8
    gravity = -1
    gravityDrag = 0.8
    randomRotXSize = 10
    randomRotYSize = 15
    randomRotZSize = 10





def addAttrs():

    ctls = cmds.ls( 'CherryBlossomTree:Ctl_Flower*', type='transform' )
    
    def addVectorAttr( node, attrName ):
        cmds.addAttr( node, ln=attrName, at='double3' )
        cmds.addAttr( node, ln=attrName + 'X', at='double', p=attrName )
        cmds.addAttr( node, ln=attrName + 'Y', at='double', p=attrName )
        cmds.addAttr( node, ln=attrName + 'Z', at='double', p=attrName )
        cmds.setAttr( node + '.' + attrName, 0,0,0, type='double3' )
    
    
    for child in ctls:
        try:cmds.deleteAttr( child + '.poseBefore' )
        except:pass
        try:cmds.deleteAttr( child + '.pointWind' )
        except:pass
        try:cmds.deleteAttr( child + '.attached' )
        except:pass
        try:cmds.deleteAttr( child + '.randDirection1' )
        except:pass
        try:cmds.deleteAttr( child + '.randDirection2' )
        except:pass
        try:cmds.deleteAttr( child + '.randDirection3' )
        except:pass
        try:cmds.deleteAttr( child + '.randomV' )
        except:pass
        try:cmds.deleteAttr( child + '.addVelocityBefore' )
        except:pass
        try:cmds.deleteAttr( child + '.gravityVelocityBefore' )
        except:pass
        try:cmds.deleteAttr( child + '.disattachVelocityBefore' )
        except:pass
        try:cmds.deleteAttr( child + '.rotSpeed' )
        except:pass
        try:cmds.deleteAttr( child + '.windAttanuation' )
        except:pass
        try:cmds.deleteAttr( child + '.windStrangth' )
        except:pass
        cmds.addAttr( child, ln='randomV', dv=1.0 )
        addVectorAttr( child, 'addVelocityBefore' )
        addVectorAttr( child, 'gravityVelocityBefore' )
        addVectorAttr( child, 'disattachVelocityBefore' )
        addVectorAttr( child, 'poseBefore' )
        addVectorAttr( child, 'pointWind' )
        cmds.addAttr( child, ln='attached', dv=0 )
        addVectorAttr( child, 'randDirection1' )
        addVectorAttr( child, 'randDirection2' )
        addVectorAttr( child, 'rotSpeed' )
        cmds.addAttr( child, ln='windStrangth', dv=1 )







def clearHandles():

    print "reset data"    
    aninCurves = []
    data.handles = cmds.ls( 'CherryBlossomTree:Ctl_Flower*', type='transform' )
    for handle in data.handles:
        if not cmds.objExists( handle ): continue
        animCurves_cu= cmds.listConnections( handle, s=1, d=0, type='animCurve' )
        if not animCurves_cu: continue
        aninCurves += animCurves_cu
    
    for handle in data.handles:
        cmds.setAttr( handle + '.t', 0,0,0 )
        cmds.setAttr( handle + '.r', 0,0,0 )

    if aninCurves: cmds.delete( aninCurves )
    
    data.handles = []


def getHandles():
    if data.handles: return None
    
    data1 = []
    data2 = []
    data3 = []
    data4 = []
    data5 = []
    data6 = []
    data7 = []
    data8 = []
    data9 = []
    data10 = []
    
    flowerHandles = cmds.ls( 'CherryBlossomTree:Ctl_Flower*', type='transform' )
    targetLocatorPos = cmds.xform( data.targetLocator, q=1, ws=1, t=1 )
    
    data.handles = []
    
    attachPointer       = data.attachStrangthPointer
    attachLengthPointer = data.attachLengthPointer
    
    pAttach = OpenMaya.MPoint( *cmds.xform( attachPointer, q=1, ws=1, t=1 ) )
    pAttachLength =OpenMaya.MPoint( *cmds.xform( attachLengthPointer, q=1, ws=1, t=1 ) )
    
    attachMaxDist = pAttach.distanceTo( pAttachLength )
    
    for handle in flowerHandles:
        randValue = random.uniform( 0, 10 )
        
        mm = cmds.listConnections( handle + '.wm', s=0, d=1, type='multMatrix' )[0]
        gpuTarget = cmds.listConnections( mm + '.i[1]', s=1, d=0 )[0]
        
        if randValue < -1:
            cmds.setAttr( handle + '.v', 0 )
            cmds.setAttr( gpuTarget + '.v', 0 )
            continue
        else:
            cmds.setAttr( handle + '.v', 1 )
            cmds.setAttr( gpuTarget + '.v', 1 )
        
        handlePos = cmds.xform( handle, q=1, ws=1, t=1 )
        handlePos[0] += random.uniform( -15, 15 )
        handlePos[1] += random.uniform( -15, 15 )
        handlePos[2] += random.uniform( -15, 15 )
        pHandle = OpenMaya.MPoint( *handlePos )
        distanceFromWind = pAttach.distanceTo( pHandle ) / attachMaxDist
        
        if distanceFromWind > 0.92:
            distanceFromWind = 0.92
        
        resultValue = distanceFromWind * ( random.uniform( 0, 1 ) ** 1.2 )
        
        import math
        randVValue = ( math.fabs(1-distanceFromWind) * 0.3) + 0.7
        cmds.setAttr( handle + '.randomV', random.uniform( randVValue - 0.1, randVValue + 0.1 ) )
        
        #resultValue = closeFromWind
        if resultValue < 0.1:
            data1.append( handle )
        elif resultValue < 0.2:
            data2.append( handle )
        elif resultValue < 0.3:
            data3.append( handle )
        elif resultValue < 0.4:
            data4.append( handle )
        elif resultValue < 0.5:
            data5.append( handle )
        elif resultValue < 0.6:
            data6.append( handle )
        elif resultValue < 0.7:
            data7.append( handle )
        elif resultValue < 0.8:
            data8.append( handle )
        elif resultValue < 0.9:
            data9.append( handle )
        elif resultValue < 1.0:
            data10.append( handle )
        
        randX = random.uniform( -400, 400 )
        randY = random.uniform( -400, 400 )
        randZ = random.uniform( -400, 400 )
        randedPos = [targetLocatorPos[0] + randX, targetLocatorPos[1] + randY, targetLocatorPos[2] + randZ]
        cmds.setAttr( handle + '.attached', resultValue )
        cmds.setAttr( handle + '.pointWind', *randedPos, type='double3' )
        cmds.setAttr( handle + '.rotSpeedX', random.uniform( -data.randomRotXSize, data.randomRotXSize ) )
        cmds.setAttr( handle + '.rotSpeedY', random.uniform( -data.randomRotYSize, data.randomRotYSize ) )
        cmds.setAttr( handle + '.rotSpeedZ', random.uniform( -data.randomRotZSize, data.randomRotZSize ) )
        cmds.setAttr( handle + '.windStrangth', 1 )
        data.handles.append( handle )
    
    print len( data1 )
    print len( data2 )
    print len( data3 )
    print len( data4 )
    print len( data5 )
    print len( data6 )
    print len( data7 )
    print len( data8 )
    print len( data9 )
    print len( data10 )
    


def listToMatrix( mtxList ):
    if type( mtxList ) == OpenMaya.MMatrix:
        return mtxList
    matrix = OpenMaya.MMatrix()
    if type( mtxList ) == list:
        resultMtxList = mtxList
    else:
        resultMtxList = []
        for i in range( 4 ):
            for j in range( 4 ):
                resultMtxList.append( mtxList[i][j] )
    
    OpenMaya.MScriptUtil.createMatrixFromList( resultMtxList, matrix )
    return matrix



def followFlower():
    
    cuFrame = cmds.currentTime( q=1 )
    forceAttachPercent = 0.21
    
    eachValue = 1.0/(data.startWindDecrease - data.startWind) * (1-forceAttachPercent)
    
    forceDisAttachValues = { 125:forceAttachPercent*0.11,  126:forceAttachPercent*0.20, 127:forceAttachPercent*0.09, 
                             140:forceAttachPercent*0.10,  141:forceAttachPercent*0.15, 142:forceAttachPercent*0.10,
                             156:forceAttachPercent*0.09,  157:forceAttachPercent*0.13, 158:forceAttachPercent*0.08 }
    
    translatedMtxPointer = listToMatrix( [1,0,0,0, 0,1,0,0, 0,0,1,0] + cmds.xform( data.targetLocator, q=1, ws=1, t=1 ) + [1] )
    rotatedMtxPointer = listToMatrix( cmds.xform( data.targetLocator, q=1, ws=1, t=1 ) )
    
    mtxPointer = translatedMtxPointer.inverse() * rotatedMtxPointer
    
    multVelocity = 1
    if data.startWindDecrease < cuFrame:
        multVelocity = ( cuFrame - data.startWindDecrease )/( data.endWind - data.startWindDecrease )
    
    for handle in data.handles:
        vPointWind = OpenMaya.MVector( *cmds.getAttr( handle + '.pointWind' )[0] ) * mtxPointer
        windStrangth = cmds.getAttr( handle + '.windStrangth' )
        if windStrangth < 0.30:
            windStrangth = 0.30
        
        currentAttachedValue = cmds.getAttr( handle + '.attached' )
        if cuFrame > data.startWind:
            cmds.setAttr( handle + '.attached', currentAttachedValue - eachValue )
        
        if forceDisAttachValues.has_key( int(cuFrame) ):
            cmds.setAttr( handle + '.attached', currentAttachedValue - eachValue - forceDisAttachValues[int(cuFrame)] )

        addVBefore = cmds.getAttr( handle + '.addVelocityBefore' )[0]
        gravityVBefore = cmds.getAttr( handle + '.gravityVelocityBefore' )[0]
        disattachVBefore = cmds.getAttr( handle + '.disattachVelocityBefore' )[0]
        randomVDist = cmds.getAttr( handle + '.randomV' )
        
        if currentAttachedValue > 0:
            posBefore = cmds.getAttr( handle + '.poseBefore' )[0]
            posAfter = cmds.xform( handle, q=1, ws=1, t=1 )
            
            velocity = OpenMaya.MVector( posAfter[0] - posBefore[0], posAfter[1] - posBefore[1], posAfter[2] - posBefore[2] )
            if velocity.length() > data.maxDisAttachVelocityDist:
                velocity = velocity.normal() * data.maxDisAttachVelocityDist
            
            cmds.setAttr( handle + '.disattachVelocityBefore', velocity.x, velocity.y, velocity.z )
            cmds.setAttr( handle + '.addVelocityBefore', 0,0,0 )
            cmds.setAttr( handle + '.gravityVelocityBefore', 0,0,0 )
            cmds.setAttr( handle + '.poseBefore', *posAfter )
        else:
            cmds.setKeyframe( handle + '.t' )
            cmds.setKeyframe( handle + '.r' )
            
            posBefore = cmds.getAttr( handle + '.poseBefore' )[0]
            vPosBefore = OpenMaya.MVector( *posBefore )
            
            vAddVBefore      = OpenMaya.MVector( addVBefore[0], addVBefore[1], addVBefore[2] )
            vDisattachBefore = OpenMaya.MVector( *disattachVBefore )
            vGravityBefore   = OpenMaya.MVector( gravityVBefore[0], gravityVBefore[1], gravityVBefore[2] )
            
            vAddVAfter = ( ( vPointWind - vPosBefore ).normal() * data.addVelocityDist * randomVDist * windStrangth * multVelocity )
            vDisattachAfter = OpenMaya.MVector( 0,0,0 )
            vGravityAfter = OpenMaya.MVector(  0, data.gravity, 0  )
            
            vAddV = vAddVBefore * data.addVelocityDrag + vAddVAfter
            vDisattachV = vDisattachBefore * data.disattachVelocityDrag + vDisattachAfter
            vGravityV = vGravityBefore * data.gravityDrag + vGravityAfter

            addVector = vAddV + vGravityV + vDisattachV
            
            if addVector.length() > data.maxVelocityDist:
                addVector = addVector.normal() * data.maxVelocityDist
            
            vPosAfter  = vPosBefore + addVector
            
            if vPosAfter.y < 0:
                vPosAfter = OpenMaya.MVector( vPosAfter.x, 0, vPosAfter.z )

            rotX = cmds.getAttr( handle + '.rotSpeedX' )
            rotY = cmds.getAttr( handle + '.rotSpeedY' )
            rotZ = cmds.getAttr( handle + '.rotSpeedZ' )
        
            cmds.rotate( rotX, rotY, rotZ, handle, ws=1, r=1 )
            
            cmds.move( vPosAfter.x, vPosAfter.y, vPosAfter.z, handle, ws=1 )
            cmds.setAttr( handle + '.addVelocityBefore', vAddV.x, vAddV.y, vAddV.z )
            cmds.setAttr( handle + '.disattachVelocityBefore', vDisattachV.x, vDisattachV.y, vDisattachV.z )
            cmds.setAttr( handle + '.gravityVelocityBefore', vGravityV.x, vGravityV.y, vGravityV.z )
            
            cmds.setAttr( handle + '.poseBefore', vPosAfter.x, vPosAfter.y, vPosAfter.z )
            cmds.setAttr( handle + '.windStrangth', (windStrangth-0.05)*0.8 )
            
            cmds.setKeyframe( handle + '.t' )
            cmds.setKeyframe( handle + '.r' )
            


expressionString = '''
float $startframe = `playbackOptions -q -min`;

python( "from sgModules import wonderBalls_tree" );

if( frame == $startframe )
{
    python( "wonderBalls_tree.clearHandles()" );
    python( "wonderBalls_tree.getHandles()" );
    python( "wonderBalls_tree.followFlower()" );
}
else
{
    python( "wonderBalls_tree.followFlower()" );
}
'''
            

def createExpression():
    
    exname = 'expression_wonderBalls_tree'
    if cmds.objExists( exname ): cmds.delete( exname )
    cmds.expression( s=expressionString,  o="", ae=1, uc='all', n=exname )


    

def deleteExpression():
    
    exname = 'expression_wonderBalls_tree'
    cmds.delete( exname )


