import maya.cmds as cmds
import sgModelDag
import sgModelCurve
import sgRigCurve


def createConveyerBeltSet( meshName, firstEdgeIndex, secondEdgeIndex ):
    
    firstEdges = cmds.polySelectSp( meshName+'.e[%d]' % firstEdgeIndex,  loop=1 )
    secondEdges = cmds.polySelectSp( meshName+'.e[%d]' % secondEdgeIndex, loop=1 )
    
    cmds.select( firstEdges )
    firstCurve  = cmds.polyToCurve( form=2, degree=3, n=meshName+'_loopCurve_First' )[0]
    cmds.select( secondEdges )
    secondCurve = cmds.polyToCurve( form=2, degree=3, n=meshName+'_loopCurve_Second' )[0]
    
    firstCurveShape = sgModelDag.getShape( firstCurve )
    secondCurveShape = sgModelDag.getShape( secondCurve )
    
    firstSpans  = cmds.getAttr( firstCurveShape +'.spans' )
    secondSpans = cmds.getAttr( secondCurveShape+'.spans' )
    
    firstTangent = sgModelCurve.getTangentAtParam( firstCurveShape, 0.0 )
    firstParamPoint = sgModelCurve.getPointAtParam( firstCurveShape, 0.0 )
    secondParam = sgModelCurve.getParamAtPoint( secondCurveShape, firstParamPoint )
    secondTangent = sgModelCurve.getTangentAtParam( secondCurveShape, secondParam )
    
    if firstTangent * secondTangent < 0:
        cmds.reverseCurve( secondCurve, ch = 1, rpo = 1 )
    
    firstPointers = sgRigCurve.createRoofPointers( firstCurve, firstSpans )
    secondPointers = sgRigCurve.createRoofPointers( secondCurve, secondSpans )
    
    fPos = cmds.xform( firstPointers[0], q=1, ws=1, t=1 )
    
    minDistPointer = secondPointers[0]
    minDist = 1000000000.0
    for secondPointer in secondPointers:
        sPos = cmds.xform( secondPointer, q=1, ws=1, t=1 )
        dist = (fPos[0]-sPos[0])**2+(fPos[1]-sPos[1])**2+(fPos[2]-sPos[2])**2
        if dist < minDist:
            minDistPointer = secondPointer
            minDist = dist
    
    offset = int( minDistPointer.split( '_' )[-1] )
    
    crvs = []
    for i in range( len( firstPointers ) ):
        firstPointer = firstPointers[i]
        secondPointer = '_'.join( secondPointers[i].split( '_' )[:-1] ) + '_%d' %( (i + offset)%firstSpans )
        
        crv = sgRigCurve.createCurveOnTargetPoints( [firstPointer, secondPointer] )
        crv = cmds.rename( crv, meshName+'_line_%d' % i )
        crvs.append( crv )
        
    cmds.select( crvs )
    loftSurf = cmds.loft( n=meshName+'_loft' )[0]
    resultObject = cmds.nurbsToPoly( loftSurf ,mnd=1 ,ch=1,f=3,pt=0,pc=200,chr=0.9,ft=0.01,mel=0.001, d=0.1, 
                                    ut=1, un=3, vt=1, vn=3, uch=0, ucr=0, cht=0.2, es=0,ntr=0,mrt=0, uss=1, n=meshName+'_conveyorBelt' )
    crvGrp = cmds.group( crvs, n=meshName+'_lines' )
    conveyorRig = cmds.group( firstCurve, secondCurve, crvGrp, loftSurf, resultObject, meshName, n=meshName+'_conveyorRig' )
    
    import sgRigAttribute
    sgRigAttribute.addAttr( conveyorRig, ln='offset', k=1 )
    cmds.connectAttr( conveyorRig+'.offset', firstCurve+'.roofValue' )
    cmds.connectAttr( conveyorRig+'.offset', secondCurve+'.roofValue' )

    cmds.setAttr( conveyorRig+'.v', 0 )