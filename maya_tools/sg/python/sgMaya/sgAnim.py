from maya import OpenMaya
from maya import cmds
import pymel.core
from sgMaya import sgCmds
import random



def createXLookAtJointLine( inputTargets ):
    
    targets = []
    for inputTarget in inputTargets:
        targets.append( pymel.core.ls( inputTarget )[0] )
    
    beforeJnt = None
    baseMatrix = None
    joints = []
    for i in range( len( targets )-1 ):
        if not baseMatrix:
            baseMatrix = sgCmds.listToMatrix( cmds.getAttr( targets[i].wm.name() ) )
        else:
            baseMatrixList = sgCmds.matrixToList( baseMatrix )
            targetPos = pymel.core.xform( targets[i], q=1, ws=1, t=1 )
            baseMatrixList[12] = targetPos[0]
            baseMatrixList[13] = targetPos[1]
            baseMatrixList[14] = targetPos[2]
            baseMatrix = sgCmds.listToMatrix( baseMatrixList )

        targetPos = OpenMaya.MPoint( *pymel.core.xform( targets[i+1], q=1, ws=1, t=1 ) )
        localPos = targetPos * baseMatrix.inverse()
        
        angleValues = pymel.core.angleBetween( v1=[1,0,0], v2=[localPos.x, localPos.y, localPos.z], er=1 )
        rotMtx = sgCmds.rotateToMatrix( angleValues )
        
        jointMatrix = sgCmds.matrixToList( rotMtx * baseMatrix )
        if beforeJnt:
            pymel.core.select( beforeJnt )
        else:
            pymel.core.select( d=1 )
        cuJoint = pymel.core.joint()
        pymel.core.xform( cuJoint, ws=1, matrix=jointMatrix )
        baseMatrix = sgCmds.listToMatrix( jointMatrix )
        joints.append( cuJoint )
        beforeJnt = cuJoint
    
    pymel.core.select( beforeJnt )
    endJnt = pymel.core.joint()
    pymel.core.xform( endJnt, ws=1, matrix= targets[-1].wm.get() )
    endJnt.r.set( 0,0,0 )
    joints.append( endJnt )
    
    return joints
    


def makeWaveJoint( inputTopJoint ): 
    
    topJoint = pymel.core.ls( inputTopJoint )[0]
    children = topJoint.listRelatives( c=1, type='transform' )
    joints = [topJoint]
    
    while children:
        joints.append( children[0] )
        children = children[0].listRelatives( c=1, type='transform' )
    
    joints = list( filter( lambda x : x.nodeType() == 'joint', joints ) )
    
    methodList = ['Sine', 'Rand', 'RandBig']
    axisList   = ['X', 'Y', 'Z']
    
    firstJnt = joints[0]
    sgCmds.addOptionAttribute( firstJnt, 'All' )
    sgCmds.addAttr( firstJnt, ln='move', k=1 )
    sgCmds.addAttr( firstJnt, ln='allWeight', min=0, dv=1, k=1 )
    sgCmds.addAttr( firstJnt, ln='allSpeed', min=0, dv=1, k=1 )
    for method in methodList:
        sgCmds.addOptionAttribute( firstJnt, '%s' % method )
        sgCmds.addAttr( firstJnt, ln='all%sWeight' % method, min=0, dv=1, k=1 )
        sgCmds.addAttr( firstJnt, ln='all%sSpeed' % method, min=0, dv=1, k=1 )
    sgCmds.addOptionAttribute( firstJnt, 'intervalValueAdd' )
    sgCmds.addAttr( firstJnt, ln='intervalValueAdd', min=0, dv=15, k=1 )
    
    for joint in joints:
        try:sgCmds.freezeJoint( joint )
        except:pass
    
    for method in methodList:
        dvOffset = 0
        dvInterval = -2
        
        sgCmds.addOptionAttribute( firstJnt, 'control%s' % method )
        sgCmds.addAttr( firstJnt, ln='interval%s' %(method), k=1, dv=dvInterval )
        sgCmds.addAttr( firstJnt, ln='offset%s' %(method), k=1, dv=dvOffset )
        for axis in axisList:    
            dvValue = 5
            sgCmds.addAttr( firstJnt, ln='value%s%s' %(method,axis), min=-90, max=90, k=1, dv = dvValue )
        for axis in axisList:
            if axis == 'Y':
                dvSpeed = 1.2
            else:
                dvSpeed = 0.8
            sgCmds.addAttr( firstJnt, ln='speed%s%s' %(method,axis), k=1, dv=dvSpeed )
            
    
    for axis in axisList:  
        randValues = []
        for j in range( 100 ):
            randValue = random.uniform( -1, 1 )
            randValues.append( randValue )
        
        for i in range( 1, len(joints)-1 ):
            methodAdd = pymel.core.createNode( 'plusMinusAverage' )
            globalAllMult = pymel.core.createNode( 'multDoubleLinear' )
            firstJnt.attr( 'allWeight' ) >> globalAllMult.input1
            methodAdd.output1D >> globalAllMult.input2
            
            joint = joints[i]
            methodIndex = 0
            
            for method in methodList:
                globalAllSpeedMult = pymel.core.createNode( 'multDoubleLinear' )
                firstJnt.attr( 'allSpeed' ) >> globalAllSpeedMult.input1
                globalSpeedMult = pymel.core.createNode( 'multDoubleLinear' )
                firstJnt.attr( 'all%sSpeed' % method ) >> globalSpeedMult.input1
                globalSpeedMult.output >> globalAllSpeedMult.input2
                
                animCurve = pymel.core.createNode( 'animCurveUU' )
                animCurve.preInfinity.set( 3 )
                animCurve.postInfinity.set( 3 )
                if method in ['Rand','RandBig']:
                    for j in range( len( randValues ) ):
                        randValue = randValues[j]
                        if j == 0 or j == 99:
                            pymel.core.setKeyframe( animCurve, f=j*10, v=0 )
                        else:
                            pymel.core.setKeyframe( animCurve, f=j*10, v=randValue )
                elif method == 'Sine':
                    pymel.core.setKeyframe( animCurve, f=0,  v= 1 )
                    pymel.core.setKeyframe( animCurve, f=5, v=-1 )
                    pymel.core.setKeyframe( animCurve, f=10, v= 1 )
                
                valueMult = pymel.core.createNode( 'multDoubleLinear' )
                speedMult = pymel.core.createNode( 'multDoubleLinear' )
                intervalMult = pymel.core.createNode( 'multDoubleLinear' )
                inputSum = pymel.core.createNode( 'plusMinusAverage' )
                firstJnt.attr( 'offset%s' %( method ) ) >> inputSum.input1D[0]
                firstJnt.attr( 'move' ) >> speedMult.input1
                firstJnt.attr( 'speed%s%s' %( method, axis ) ) >> speedMult.input2
                speedMult.output >> globalSpeedMult.input2
                globalAllSpeedMult.output >> inputSum.input1D[1]
                intervalMult.input1.set( i )
                firstJnt.attr( 'interval%s' %( method ) ) >> intervalMult.input2
                intervalMult.output >> inputSum.input1D[2]
                inputSum.output1D >> animCurve.input
                animCurve.output >> valueMult.input1
                firstJnt.attr( 'value%s%s' %(method,axis) ) >> valueMult.input2
                
                globalWeightMult = pymel.core.createNode( 'multDoubleLinear' )
                firstJnt.attr( 'all%sWeight' % method ) >> globalWeightMult.input1
                valueMult.output >> globalWeightMult.input2
                globalWeightMult.output >> methodAdd.input1D[methodIndex]
                methodIndex+=1
            
            intervalValueAddPercent = pymel.core.createNode( 'multDoubleLinear' )
            intervalValueAddMult = pymel.core.createNode( 'multDoubleLinear' )
            intervalValueAddAdd  = pymel.core.createNode( 'addDoubleLinear' )
            
            intervalValueAddPercent.input1.set( 0.01 * i )
            firstJnt.attr('intervalValueAdd') >> intervalValueAddPercent.input2
            intervalValueAddPercent.output >> intervalValueAddMult.input1
            globalAllMult.output >> intervalValueAddMult.input2
            globalAllMult.output >>intervalValueAddAdd.input1
            intervalValueAddMult.output >> intervalValueAddAdd.input2
            
            intervalValueAddAdd.output >> joint.attr( 'rotate%s' % axis )
            
            
                


def makeWaveGlobal( inputTopJoints, inputCtl ):
    
    topJoints = []
    for inputTopJoint in inputTopJoints:
        topJoints.append( pymel.core.ls( inputTopJoint )[0] )

    ctl = pymel.core.ls( inputCtl )[0]

    sgCmds.addOptionAttribute( ctl, 'control_offset' )
    sgCmds.addAttr( ctl, ln='offsetGlobalInterval', k=1, dv=1 )
    sgCmds.addAttr( ctl, ln='offsetGlobalRand', k=1, dv=1 )

    attrs = topJoints[0].listAttr( ud=1 )
    sgCmds.addOptionAttribute( ctl, 'wave' )
    for attr in attrs:
        sgCmds.copyAttribute( topJoints[0], ctl, attr.longName() )
    
    circleAttrs = ctl.listAttr( ud=1, k=1 )
    
    for topJoint in topJoints:
        for circleAttr in circleAttrs:
            if not pymel.core.attributeQuery( circleAttr.longName(), node=topJoint, ex=1 ): continue
            circleAttr >> topJoint.attr( circleAttr.longName() )
    
    index = 0
    for topJoint in topJoints:
        offsetRand = pymel.core.createNode( 'multDoubleLinear' )
        offsetInterval = pymel.core.createNode( 'multDoubleLinear' )
        offsetAll = pymel.core.createNode( 'addDoubleLinear' )
        offsetRand.input1.set( random.uniform( -5, 5 ) )
        ctl.attr( 'offsetGlobalRand' ) >> offsetRand.input2
        offsetInterval.input1.set( index )
        ctl.attr( 'offsetGlobalInterval' ) >> offsetInterval.input2
        offsetRand.output >> offsetAll.input1
        offsetInterval.output >> offsetAll.input2
        offsetAll.output >> topJoint.attr( 'offsetSine' )
        index += 1
        allWeightPlug = topJoint.allWeight.listConnections( s=1, d=0, p=1 )[0]
        sgCmds.addAttr( topJoint, ln='globalWeight', min=0, max=1, k=1, dv=1 )
        multGlobal = pymel.core.createNode( 'multDoubleLinear' )
        topJoint.globalWeight >> multGlobal.input1
        allWeightPlug >> multGlobal.input2
        multGlobal.output >> topJoint.allWeight



def createRandomTranslate( inputCtl, inputTarget ):
    
    ctl    = pymel.core.ls( inputCtl )[0]
    target = pymel.core.ls( inputTarget )[0]
    
    sgCmds.addOptionAttribute( ctl, 'translateRandom' )
    sgCmds.addAttr( ctl, ln='move', k=1 )
    sgCmds.addAttr( ctl, ln='speed', k=1, min=0, dv=1 )
    multMove = pymel.core.createNode( 'multDoubleLinear' )
    ctl.attr( 'move' )  >> multMove.input1
    ctl.attr( 'speed' ) >> multMove.input2
    
    for axis in ['X', 'Y', 'Z']:
        animCurve = pymel.core.createNode( 'animCurveUU' )
        animCurve.preInfinity.set( 3 )
        animCurve.postInfinity.set( 3 )
        for j in range( 100 ):
            randValue = random.uniform( -1, 1 )
            if j == 0 or j == 99:
                pymel.core.setKeyframe( animCurve, f=j*10, v=0 )
            else:
                pymel.core.setKeyframe( animCurve, f=j*10, v=randValue )
                print "set rand value : %f" % randValue

        multMove.output >> animCurve.input
        sgCmds.addAttr( ctl, ln='weight_%s' % axis, min=0, dv=0.5, k=1 )
        multWeight = pymel.core.createNode( 'multDoubleLinear' )
        ctl.attr( 'weight_%s' % axis ) >> multWeight.input1
        animCurve.output >> multWeight.input2
        multWeight.output >> target.attr( 'translate%s' % axis )



def makeUdAttrGlobal( inputTargets, inputCtl ):

    targets = []
    for inputTarget in inputTargets:
        targets.append( pymel.core.ls( inputTarget )[0] )

    ctl = pymel.core.ls( inputCtl )[0]

    attrs = targets[0].listAttr( ud=1 )
    for attr in attrs:
        sgCmds.copyAttribute( targets[0], ctl, attr.longName() )
    
    circleAttrs = ctl.listAttr( ud=1, k=1 )
    
    for target in targets:
        for circleAttr in circleAttrs:
            if not pymel.core.attributeQuery( circleAttr.longName(), node=target, ex=1 ): continue
            circleAttr >> target.attr( circleAttr.longName() )



def buildJointLineByVtxNum( mesh, vtxList, numJoints ):
    
    points = OpenMaya.MPointArray()
    
    for vtxIndex in vtxList:
        vtxPos = OpenMaya.MPoint( *cmds.xform( mesh + '.vtx[%d]' % vtxIndex, q=1, ws=1, t=1 )[:3] )
        points.append( vtxPos )
        #print "vtx pos[%d] : %5.3f, %5.3f, %5.3f " %( vtxIndex, vtxPos.x, vtxPos.y, vtxPos.z )
    
    curveData = OpenMaya.MFnNurbsCurveData()
    oData = curveData.create()
    fnCurve = OpenMaya.MFnNurbsCurve()
    
    fnCurve.createWithEditPoints( points, 3, fnCurve.kOpen, False, True, True, oData )
    
    newFnCurve = OpenMaya.MFnNurbsCurve( oData )
    
    eachLength = newFnCurve.length()/numJoints
    parentObj = None
    joints = []
    for i in range( numJoints+1 ):
        paramValue = newFnCurve.findParamFromLength( eachLength * i )
        point = OpenMaya.MPoint()
        newFnCurve.getPointAtParam( paramValue, point )
        
        if not parentObj:
            pymel.core.select( d=1 )
        else:
            pymel.core.select( parentObj )

        joint = pymel.core.joint()
        joints.append( joint )
        pymel.core.move( point.x, point.y, point.z, joint, ws=1 )
        parentObj = joint
    return joints[0]
        
        



