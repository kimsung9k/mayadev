import maya.cmds as cmds
import baseFunctions

class Create:
    
    def __init__(self, fixTargetObj, baseObj, mainBlendShape, indies, weights ):
        
        origMesh = self.getOriginalMesh( mainBlendShape )
        
        targetGeoms = self.getConnectedMeshs( mainBlendShape, indies )
        
        fixEditMesh = self.createFixMesh( origMesh, fixTargetObj )
        
        targetGeoms.insert( 0, fixTargetObj )
        
        currentIndex = baseFunctions.getLastIndex( mainBlendShape+'.w' )+1
        
        cmds.blendShape( mainBlendShape, e=1, t=[ baseObj, currentIndex , fixEditMesh, 1] )
        
        itpNode = self.checkExistingItp( mainBlendShape, targetGeoms, indies )

        if not itpNode:
            fixShapeNode = self.fixShapeCreate( targetGeoms, fixEditMesh, weights )
            self.createItp( mainBlendShape, targetGeoms, fixEditMesh, fixShapeNode, indies )
        else:
            fixShapeNode = self.fixShapeCreate( targetGeoms, fixEditMesh, weights )
            self.appendItp( mainBlendShape, targetGeoms, fixEditMesh, fixShapeNode, indies, itpNode )
        

        
    def getOriginalMesh( self, deformNode ):
    
        cons = cmds.listConnections( deformNode, s=1, d=0, c=1, p=1 )
        
        inCons = cons[::2]
        outCons = cons[1::2]
        
        for i in range( len( inCons ) ):
            if inCons[i].find( 'inputGeometry' ) != -1:
                goConObj = outCons[i].split( '.' )[0]
                
                if cmds.nodeType( goConObj ) == 'mesh':
                    return goConObj
                else:
                    return self.getOriginalMesh( goConObj )
                
        
        
    def getConnectedMeshs( self, mainBlendShape, indies ):
        
        targetGeoms = []
        
        for i in indies:
            targetGeom = cmds.listConnections( mainBlendShape+'.inputTarget[0].inputTargetGroup[%d].inputTargetItem[6000].inputGeomTarget' % i )[0]
            targetGeoms.append( targetGeom )
            
        return targetGeoms
            
        
        
    def createFixMesh( self, origMesh, fixTargetObj ):
        
        meshNode = cmds.createNode( 'mesh' )
        meshObj = cmds.listRelatives( meshNode, p=1 )[0]
        
        cmds.connectAttr( origMesh+'.outMesh', meshNode+'.inMesh' )
        
        duMesh = cmds.duplicate( meshObj )[0]
        fixEditMesh = cmds.rename( duMesh, fixTargetObj+'_Fix' )
        cmds.setAttr( fixEditMesh+'.v', 0 )
        
        fixMeshShape = cmds.listRelatives( fixEditMesh, s=1 )[0]
        cmds.addAttr( fixMeshShape, ln='isFixEditMesh', at='bool' )
        
        cmds.delete( meshObj )
        
        return fixEditMesh
    
    
    
    def fixShapeCreate(self, targetGeoms, fixEditMesh, weights ):
        
        targetGeoms.append( fixEditMesh )
        
        fixEditNode = cmds.blendShape( *targetGeoms, n= fixEditMesh+'_FixEditNode' )[0]
        
        cmds.setAttr( fixEditNode+'.w[0]', 1 )
        
        for i in range( len( weights ) ):
            cmds.setAttr( fixEditNode+'.w[%d]' % (i+1), -weights[i] )
        
        return fixEditNode
    
    
    
    def checkExistingItp( self, mainBlendShape, targetGeoms, indies ):
        
        neadIndies = []
        
        for i in range( len( indies ) ):
            index  = indies[i]
            targetGeomShape = cmds.listRelatives( targetGeoms[i+1], s=1 )[0]
            if cmds.attributeQuery( 'isFixEditMesh', node=targetGeomShape, ex=1 ): continue
            neadIndies.append( index )
        
        itpNodes = cmds.listConnections( mainBlendShape, type='vectorInterpolation' )
        if not itpNodes: return None
        itpNodes = list( set( itpNodes ) )

        for itpNode in itpNodes:
            inputs = cmds.listConnections( itpNode, s=1, d=0, c=1, type='blendShape' )[::2]
            
            if len( inputs ) != len( neadIndies ):
                continue
            
            inputConnected = True
            for inputValue in inputs:
                
                connected = False
                for index in indies:
                    if cmds.isConnected( mainBlendShape+'.w[%d]' % index, inputValue ): connected=True
                
                if not connected:
                    inputConnected = False
            
            if inputConnected: return itpNode
            
        return None
                    
        
        
    def createItp(self, mainBlendShape, targetGeoms, fixEditMesh, fixEditNode, indies ):
        
        itpNode = cmds.createNode( 'vectorInterpolation', n= fixEditMesh+'_ItpNode'  )
        
        for i in range( len( indies ) ):
            index  = indies[i]
            
            targetGeomShape = cmds.listRelatives( targetGeoms, s=1 )[0]
            
            if cmds.attributeQuery( 'isFixEditMesh', node=targetGeomShape, ex=1 ): continue
            
            weightRev = cmds.createNode( 'multDoubleLinear', n= fixEditNode+'_weightRev%d' % index )
            cmds.setAttr( weightRev+'.input2', -1 )
            
            cmds.connectAttr( fixEditNode+'.w[%d]' % (i+1),  weightRev+'.input1' )
            cmds.connectAttr( weightRev+'.output',  itpNode+'.staticVectors[0].staticVector[%d]' % i )
            
            cmds.connectAttr( mainBlendShape+'.w[%d]' % index, itpNode+'.inputVector[%d]' % i )
            
        
        lastIndex = baseFunctions.getLastIndex( mainBlendShape+'.w' )
        
        cmds.connectAttr( itpNode+'.outputWeight[0]', mainBlendShape+'.w[%d]' % lastIndex )
        cmds.connectAttr( itpNode+'.envelope', fixEditNode+'.envelope' )

        
    def appendItp(self, mainBlendShape, targetGeoms, fixEditMesh, fixEditNode, indies, itpNode ):
        
        itplastIndex = baseFunctions.getLastIndex( itpNode+'.staticVectors' )
        
        cuItpNode = cmds.createNode( 'vectorInterpolation', n= fixEditMesh+'_ItpNode'  )
        
        cons = cmds.listConnections( itpNode, s=1, d=0, p=1, c=1, type='multDoubleLinear' )
        cons += cmds.listConnections( itpNode, s=1, d=0, p=1, c=1, type='blendShape' )
        
        outputs = cons[1::2]
        inputs  = cons[::2]
        
        for i in range( len( outputs )):
            cmds.connectAttr( outputs[i], inputs[i].replace( itpNode, cuItpNode ) )
        
        for i in range( len( indies ) ):
            index  = indies[i]
            
            targetGeomShape = cmds.listRelatives( targetGeoms[i+1], s=1 )[0]
            
            if cmds.attributeQuery( 'isFixEditMesh', node=targetGeomShape, ex=1 ): continue
            
            weightRev = cmds.createNode( 'multDoubleLinear', n= fixEditNode+'_weightRev%d' % index )
            cmds.setAttr( weightRev+'.input2', -1 )
            
            cmds.connectAttr( fixEditNode+'.w[%d]' % (i+1),  weightRev+'.input1' )
            
            cmds.connectAttr( weightRev+'.output',  cuItpNode+'.staticVectors[%d].staticVector[%d]' % (itplastIndex+1, i ) )
            
        lastIndex = baseFunctions.getLastIndex( mainBlendShape+'.w' )
        
        cmds.connectAttr( cuItpNode+'.outputWeight[%d]' % (itplastIndex+1), mainBlendShape+'.w[%d]' % lastIndex )
        cmds.connectAttr( cuItpNode+'.envelope', fixEditNode+'.envelope' )