import maya.cmds as cmds
import maya.OpenMaya as om
import baseCommand as bc
import functions as fnc

import copy


def checkBlendMesh( targetMeshObj ):
    
    node = bc.getBlendAndFixedShape( targetMeshObj )
    
    fnNode = om.MFnDependencyNode( fnc.getMObject( node ) )
    
    blendMeshPlug = fnNode.findPlug( "blendMeshInfos" )
    
    addSpace = '    '
    for i in range( blendMeshPlug.numElements() ):
        
        inputMeshPlug = blendMeshPlug[i].child( 0 )
        targetWPlug   = blendMeshPlug[i].child( 2 )
        namePlug      = blendMeshPlug[i].child( 3 )
        
        cons = om.MPlugArray()
        inputMeshPlug.connectedTo( cons, True, False )
        
        print addSpace + "Input Mesh :",
        if cons.length():
            print cons[0].name()
        else:
            print namePlug.asString()
        
        print addSpace + "Target Weights :"
        for i in range( targetWPlug.numElements() ):
            loIndex = targetWPlug[i].logicalIndex()
            value   = targetWPlug[i].asDouble()
            
            print " "*20 + "[%d]" % loIndex + " : %3.2f" % value
            
            


def selectDeltaPoints( targetMeshObj, targetIndex ):
    
    nodeName = bc.getBlendAndFixedShape(targetMeshObj)
    
    fnNode = om.MFnDependencyNode( fnc.getMObject( nodeName ) )

    blendMeshInfosPlug = fnNode.findPlug( 'blendMeshInfos' )

    elementNum = blendMeshInfosPlug.numElements()
    
    if targetIndex >= elementNum: return None
    
    deltasPlug = blendMeshInfosPlug[targetIndex].child( 1 )
    
    vtxNames = []
    for i in range( deltasPlug.numElements() ):
        loIndex = deltasPlug[i].logicalIndex()
        vtxNames.append( targetMeshObj+'.vtx[%d]' % loIndex )
    
    cmds.select( vtxNames )

    
    
def setDeltaBySelected( targetMeshObj, targetIndex, deltaIndices ):
    
    if not deltaIndices: return None
    
    nodeName = bc.getBlendAndFixedShape(targetMeshObj)
    
    fnNode = om.MFnDependencyNode( fnc.getMObject( nodeName ) )

    blendMeshInfosPlug = fnNode.findPlug( 'blendMeshInfos' )

    elementNum = blendMeshInfosPlug.numElements()
    
    if targetIndex >= elementNum: return None
    
    deltasPlug = blendMeshInfosPlug[targetIndex].child( 1 )
    
    cuDeltaIndices = []
    for i in range( deltasPlug.numElements() ):
        cuDeltaIndices.append( deltasPlug[i].logicalIndex() )
    
    for deltaIndex in cuDeltaIndices:
        if not deltaIndex in deltaIndices:
            cmds.removeMultiInstance( blendMeshInfosPlug[targetIndex].name()+'.deltas[%d]' % deltaIndex )
        
            
            
def getShapeInfo( targetMeshObj ):
    
    shapeInfoList = []
    
    node = bc.getBlendAndFixedShape( targetMeshObj )
    
    if not cmds.objExists( targetMeshObj ):
        return None, None
    
    fnNode = om.MFnDependencyNode( fnc.getMObject( node ) )
    
    driverWeightPlug = fnNode.findPlug( "driverWeights" )
    blendMeshPlug = fnNode.findPlug( "blendMeshInfos" )
    
    for i in range( blendMeshPlug.numElements() ):
        
        shapeInfo = [None, None, blendMeshPlug[i].logicalIndex() ]
        
        inputMeshPlug = blendMeshPlug[i].child( 0 )
        targetWPlug   = blendMeshPlug[i].child( 2 )
        namePlug      = blendMeshPlug[i].child( 3 )
        
        cons = om.MPlugArray()
        inputMeshPlug.connectedTo( cons, True, False )
        
        if cons.length():
            conNode = om.MFnDependencyNode( cons[0].node() )
            shapeInfo[0] = cmds.listRelatives( conNode.name(), p=1 )[0].replace( '_inv', '' )
        else:
            shapeInfo[0] = namePlug.asString()
        
        angleInfos = []
        for i in range( targetWPlug.numElements() ):
            
            newAngleInfo = [None, 0, 0, 0]
            
            logicalIndex = targetWPlug[i].logicalIndex()
            targetDriverWPlug = driverWeightPlug.elementByLogicalIndex( logicalIndex )
            
            cons = om.MPlugArray()
            targetDriverWPlug.connectedTo( cons, True, False )
            if not cons.length(): continue
            
            angleNode, angleAttr = cons[0].name().split( '.' )
            value = targetWPlug[i].asDouble()
            
            appendIndex = None
            if angleAttr == 'outDriver0':
                appendIndex = 1
            elif angleAttr == 'outDriver1':
                appendIndex = 2
            elif angleAttr == 'outDriver2':
                appendIndex = 3
            newAngleInfo[0] = angleNode
            newAngleInfo[ appendIndex ] = value
            
            sameEx = False
            for angleInfo in angleInfos:
                if newAngleInfo[0] == angleInfo[0]:
                    if newAngleInfo[1]: angleInfo[1] = newAngleInfo[1]
                    if newAngleInfo[2]: angleInfo[2] = newAngleInfo[2]
                    if newAngleInfo[3]: angleInfo[3] = newAngleInfo[3]
                sameEx = True
            if not sameEx:
                angleInfos.append( newAngleInfo )
        
        shapeInfo[1] = angleInfos
        shapeInfoList.append( shapeInfo )
    
    return shapeInfoList, fnNode.name()


'''
def setGlobalInfoIndices( node ):
    
    fnNode = om.MFnDependencyNode( fnc.getMObject( node ) )
    
    blendMeshInfoPlugs = fnNode.findPlug( "blendMeshInfos" )
    
    numElements = blendMeshInfoPlugs.numElements()
    
    numberList  = []
    
    globalInfo.overIndices = []
    for i in range( numElements ):
        logicalIndex = blendMeshInfoPlugs[i].logicalIndex()
        numberList.append( logicalIndex )
        if logicalIndex >= numElements:
            globalInfo.overIndices.append( logicalIndex )
            
    globalInfo.emptyIndices = []
    
    for i in range( numElements ):
        if not i in numberList:
            globalInfo.emptyIndices.append( i )



def getGlobalInfoIndices():
    
    tempOverIndices = copy.copy( globalInfo.overIndices )
    tempEmptyIndices = copy.copy( globalInfo.emptyIndices )

    globalInfo.overIndices = tempEmptyIndices
    globalInfo.emptyIndices = tempOverIndices



def reOrderBlendMesh( node ):
    
    fnNode = om.MFnDependencyNode( fnc.getMObject( node ) )
    
    blendMeshInfoPlugs = fnNode.findPlug( "blendMeshInfos" )
    
    dgMode = om.MDGModifier()
    
    for i in range( len( globalInfo.emptyIndices ) ):
        sIndex = globalInfo.overIndices[i]
        dIndex = globalInfo.emptyIndices[i]
        
        sElement = blendMeshInfoPlugs.elementByLogicalIndex( sIndex )
        dElement = blendMeshInfoPlugs.elementByLogicalIndex( dIndex )
        
        sInputMeshPlug = sElement.child( 0 )
        cons = om.MPlugArray()
        sInputMeshPlug.connectedTo( cons, True, False )
        
        if cons:
            dgMode.connect( cons[0], dElement.child(0) )
            dgMode.disconnect( cons[0], sInputMeshPlug )
            dgMode.doIt()
        else:
            sDeltas = sElement.child( 1 )
            dDeltas = dElement.child( 1 )
            
            for j in range( sDeltas.elementCount() ):
                deltaLoIndex = sDeltas[j].logicalIndex()
                sDeltaX = sDeltas[j].child(0)
                sDeltaY = sDeltas[j].child(1)
                sDeltaZ = sDeltas[j].child(2)
                
                dDelta = dDeltas.elementByLogicalIndex( deltaLoIndex )
                dDelta.child(0).setDouble( sDeltaX.asDouble() )
                dDelta.child(1).setDouble( sDeltaY.asDouble() )
                dDelta.child(2).setDouble( sDeltaZ.asDouble() )
        
        sTargetWPlug = sElement.child( 2 )
        dTargetWPlug = dElement.child( 2 )
        
        for j in range( sTargetWPlug.numElements() ):
            loIndex = sTargetWPlug[j].logicalIndex()
            dTargetWElement = dTargetWPlug.elementByLogicalIndex( loIndex )
            dTargetWElement.setFloat( sTargetWPlug[j].asFloat() )'''