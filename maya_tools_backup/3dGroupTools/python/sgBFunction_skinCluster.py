import sgBFunction_dag
import maya.OpenMaya as om
import maya.cmds as cmds

def getSkinClusterFromMesh( mesh ):
   
    return sgBFunction_dag.getNodeFromHistory( mesh, 'skinCluster' )


def getPlugMatrix( mesh ):
    
    skinCluster = getSkinClusterFromMesh( mesh )
    if not skinCluster: return None
    skinCluster = skinCluster[0]
    fnSkinCluster = om.MFnDependencyNode( sgBFunction_dag.getMObject( skinCluster ) )
    
    return fnSkinCluster.findPlug( 'matrix' )



def getPlugBindPre( mesh ):
    
    skinCluster = getSkinClusterFromMesh( mesh )
    if not skinCluster: return None
    skinCluster = skinCluster[0]
    fnSkinCluster = om.MFnDependencyNode( sgBFunction_dag.getMObject( skinCluster ) )
    
    return fnSkinCluster.findPlug( 'bindPreMatrix' )



def getInfluenceAndWeightList( mesh, vertices = [] ):

    skinClusters = sgBFunction_dag.getNodeFromHistory( mesh, 'skinCluster' )
    if not skinClusters: return None
    
    skinCluster = skinClusters[0]
    
    fnSkinCluster = om.MFnDependencyNode( sgBFunction_dag.getMObject( skinCluster ) )
    plugWeightList = fnSkinCluster.findPlug( 'weightList' )
    
    if not vertices: vertices = [ i for i in range( plugWeightList.numElements() ) ]
    influenceAndWeightList = [ [] for i in range( len( vertices ) ) ]
    phygicalMap = [ 0 for i in range( plugWeightList.numElements() ) ]
    
    for i in range( len( vertices ) ):
        logicalIndex = vertices[i]
        plugWeights = plugWeightList[ logicalIndex ].child( 0 )
        influenceNums = []
        values = []
        for j in range( plugWeights.numElements() ):
            influenceNum = plugWeights[j].logicalIndex()
            value = plugWeights[j].asFloat()
            influenceNums.append( influenceNum )
            values.append( value )
        
        influenceAndWeightList[i] = [ influenceNums, values ]
        phygicalMap[ logicalIndex ] = i
        
    return influenceAndWeightList, phygicalMap




def autoCopyWeight( first, second ):
    
    import maya.cmds as cmds
    hists = cmds.listHistory( first, pdo=1 )
    
    skinNode = None
    for hist in hists:
        if cmds.nodeType( hist ) == 'skinCluster':
            skinNode = hist
    
    if not skinNode: return None
    
    targetSkinNode = None
    targetHists = cmds.listHistory( second, pdo=1 )
    if targetHists:
        for hist in targetHists:
            if cmds.nodeType( hist ) == 'skinCluster':
                targetSkinNode = hist

    if not targetSkinNode:
        bindObjs = cmds.listConnections( skinNode+'.matrix', s=1, d=0, type='joint' )
        bindObjs.append( second )
        cmds.skinCluster( bindObjs, tsb=1 )
    
    cmds.copySkinWeights( first, second, noMirror=True, surfaceAssociation='closestPoint', influenceAssociation ='oneToOne' )



def setBindPreMatrix( joint, bindPreObj, targetMesh ):
    
    skinNodes = sgBFunction_dag.getNodeFromHistory( targetMesh, 'skinCluster' )
    
    if not skinNodes: return None
    
    cons = cmds.listConnections( joint+'.wm', type='skinCluster', p=1, c=1 )
    
    for con in cons[1::2]:
        skinCluster = con.split( '.' )[0]
        if skinCluster != skinNodes[0]: continue
        
        index = int( con.split( '[' )[-1].replace( ']', '' ) )
        if not cmds.isConnected( bindPreObj+'.wim', skinCluster+'.bindPreMatrix[%d]' % index ):
            cmds.connectAttr( bindPreObj+'.wim', skinCluster+'.bindPreMatrix[%d]' % index, f=1 )



def setBindPreMatrixSelf( joint, targetMesh ):
    
    skinNodes = sgBFunction_dag.getNodeFromHistory( targetMesh, 'skinCluster' )
    
    if not skinNodes: return None
    
    cons = cmds.listConnections( joint+'.wm', type='skinCluster', p=1, c=1 )
    
    for con in cons[1::2]:
        skinCluster = con.split( '.' )[0]
        if skinCluster != skinNodes[0]: continue
        
        index = int( con.split( '[' )[-1].replace( ']', '' ) )
        if not cmds.isConnected( joint+'.wim', skinCluster+'.bindPreMatrix[%d]' % index ):
            cmds.connectAttr( joint+'.wim', skinCluster+'.bindPreMatrix[%d]' % index, f=1 )



def weightHammerCurve( targets ):
    import maya.OpenMaya as om
    import sgBFunction_dag
    import sgCFnc_dag
    import sgModelDg
    
    def getWeights( plug ):
        childPlug = plug.child(0)
        numElements = childPlug.numElements()
        indicesAndValues = []
        for i in range( numElements ):
            logicalIndex = childPlug[i].logicalIndex()
            value        = childPlug[i].asFloat()
            indicesAndValues.append( [ logicalIndex, value ] )
        return indicesAndValues
    
    def getMixWeights( first, second, rate ):
        
        invRate = 1.0-rate
        
        print first
        print second
        
        firstMaxIndex = first[-1][0]
        secondMaxIndex = second[-1][0]
        maxIndex = firstMaxIndex+1
        
        if firstMaxIndex < secondMaxIndex:
            maxIndex = secondMaxIndex+1
        
        firstLogicalMap  = [ False for i in range( maxIndex ) ]
        secondLogicalMap = [ False for i in range( maxIndex ) ]
        
        for index, value in first:
            firstLogicalMap[ index ] = True
            
        for index, value in second:
            secondLogicalMap[ index ] = True
        
        returnTargets = []
        
        for index, value in first:
            returnTargets.append( [index, invRate * value] )
        for index, value in second:
            if firstLogicalMap[ index ]:
                for i in range( len( returnTargets ) ):
                    wIndex = returnTargets[i][0]
                    if wIndex == index:
                        returnTargets[i][1] += rate * value
                        break
            else:
                returnTargets.append( [index, rate * value] )
        return returnTargets
    
    def clearArray( targetPlug ):
        plugChild = targetPlug.child( 0 )
        targetInstances = []
        for i in range( plugChild.numElements() ):
            targetInstances.append( plugChild[i].name() )
        targetInstances.reverse()
        for i in range( len( targetInstances ) ):
            cmds.removeMultiInstance( targetInstances[i] )
        
    
    node = targets[0].split( '.' )[0]
    
    skinClusterNodes = sgBFunction_dag.getNodeFromHistory( node, 'skinCluster' )
    if not skinClusterNodes: return None
    
    fnSkinCluster = om.MFnDependencyNode( sgBFunction_dag.getMObject( skinClusterNodes[0] ) )
    plugWeightList = fnSkinCluster.findPlug( 'weightList' )
    
    cmds.select( targets )
    for dagPath, uArr, vArr, wArr in sgCFnc_dag.getMDagPathAndComponent():
        
        fnCurve = om.MFnNurbsCurve( dagPath )
        startNum = 0
        lastNum = fnCurve.numCVs()-1
        
        if uArr[-1] == lastNum:
            pass
        elif uArr[0] == startNum:
            pass
        elif uArr[0] == startNum and uArr[-1] == lastNum:
            pass
        else:
            weightStart = getWeights( plugWeightList[ uArr[0]-1 ] )
            weightEnd   = getWeights( plugWeightList[ uArr[-1]+1 ] )
            
            length = uArr.length()
            for i in range( uArr.length() ):
                clearArray( plugWeightList[ uArr[i] ] )
                plugWeightListEmelent = plugWeightList.elementByLogicalIndex( uArr[i] )
                
                rate = float( i+1 ) / (length+2)
                weights = getMixWeights( weightStart, weightEnd, rate )
                for index, value in weights:
                    targetPlug = plugWeightListEmelent.child(0).elementByLogicalIndex( index )
                    cmds.setAttr( targetPlug.name(), value )
        cmds.skinPercent( skinClusterNodes[0], normalize=1 )
    
    

def combineSkinCluster( skinedObjs ):
    
    import sgBFunction_dag
    
    numVertices = None
    for skinedObj in skinedObjs:
        objShape = sgBFunction_dag.getShape( skinedObj )
        fnMesh = om.MFnMesh( sgBFunction_dag.getMDagPath( objShape ) )
        if not numVertices:
            numVertices = fnMesh.numVertices()
        else:
            if numVertices != fnMesh.numVertices():
                cmds.error( "Selected meshs not same objects" )
    
    skinJoints = []
    weightList = [ [] for i in range( numVertices ) ]
    for skinedObj in skinedObjs:
        
        skinCluster = sgBFunction_dag.getNodeFromHistory( skinedObj, 'skinCluster' )
        if not skinCluster: continue
        
        skinCluster = skinCluster[0]
        
        fnNode = om.MFnDependencyNode( sgBFunction_dag.getMObject( skinCluster ) )
        
        plugMatrix = fnNode.findPlug( 'matrix' )
        
        plugMatrixMaxLogicalIndex = 0
        for i in range( plugMatrix.numElements() ):
            logicalIndex = plugMatrix[i].logicalIndex()
            if logicalIndex > plugMatrixMaxLogicalIndex:
                plugMatrixMaxLogicalIndex = logicalIndex 
        
        connections = om.MPlugArray()
        skinedJointIndices = []
        origSkinedJointIndicesMap = [ -1 for i in range( plugMatrixMaxLogicalIndex+1 ) ]
        for i in range( plugMatrix.numElements() ):
            
            plugMatrix[i].connectedTo( connections, True, False )
            if not connections.length():
                continue
            
            skinJointName = om.MFnDagNode( connections[0].node() ).fullPathName()
            
            if not skinJointName in skinJoints:
                skinJoints.append( skinJointName )
            
            jntIndex = skinJoints.index( skinJointName )
            origSkinedJointIndicesMap[ plugMatrix[i].logicalIndex() ] = jntIndex
            skinedJointIndices.append( jntIndex )
    
        plugWeightList = fnNode.findPlug( 'weightList' )
        
        for i in range( plugWeightList.numElements() ):
            
            plugWeights = plugWeightList[i].child( 0 )
            for j in range( plugWeights.numElements() ):
                
                logicalIndex = plugWeights[j].logicalIndex()
                weightValue = plugWeights[j].asFloat()
                jntIndex = origSkinedJointIndicesMap[ logicalIndex ]
                
                weightList[i].append( [jntIndex, weightValue] )
    
    newMesh = cmds.createNode( 'mesh' )
    srcShape = sgBFunction_dag.getShape( skinedObjs[0] )
    newMeshObj = sgBFunction_dag.getParent( newMesh )
    cmds.connectAttr( srcShape+'.outMesh', newMesh+'.inMesh' )
    cmds.refresh()
    cmds.disconnectAttr( srcShape+'.outMesh', newMesh+'.inMesh' )
    node = cmds.deformer( newMeshObj, type='skinCluster' )[0]
    
    for i in range( len( skinJoints ) ):
        cmds.connectAttr( skinJoints[i]+'.wm', node+'.matrix[%d]' % i )
        bindPreMatrix = cmds.getAttr( skinJoints[i]+'.wim' )
        cmds.setAttr( node+'.bindPreMatrix[%d]' % i, bindPreMatrix, type='matrix' )
    
    for i in range( len( weightList ) ):
        for logicalIndex, value in weightList[i]:
            cmds.setAttr( node+'.weightList[%d].weights[%d]' %( i, logicalIndex ), value )
    
    cmds.skinPercent( node, normalize=True )