import maya.cmds as cmds


def mmCreateSlidingDeformer( *args ):
    
    sels = cmds.ls( sl=1 )
    
    if len( sels ) == 1:
        selShapes = cmds.listRelatives( sels[0], s=1 )
        
        srcCons = []
        for shape in selShapes:
            if not cmds.getAttr( shape+'.io' ):
                cons = cmds.listConnections( shape+'.inMesh', s=1, d=0, p=1, c=1 )
                if cons:
                    srcCons = cons[1::2]
                break
        deformer = cmds.deformer( sels[0], type='slidingDeformer' )[0]
        
        if srcCons:
            cmds.connectAttr( srcCons[0], deformer+'.baseMesh' )
            cmds.connectAttr( srcCons[0], deformer+'.origMesh' )
        else:
            selShapes = cmds.listRelatives( sels[0], s=1 )
            for shape in selShapes:
                if cmds.getAttr( shape+'.io' ):
                    cmds.connectAttr( shape+'.outMesh', deformer+'.baseMesh' )
                    cmds.connectAttr( shape+'.outMesh', deformer+'.origMesh' )
    if len( sels ) > 1:
        
        last = sels[-1]
        others = sels[:-1]
        
        lastShape = cmds.listRelatives( last, s=1 )[0]
        
        for other in others:
            selShapes = cmds.listRelatives( other, s=1 )
            
            mmtxNode  = cmds.createNode( 'multMatrix' )
            trGeoNode = cmds.createNode( 'transformGeometry' )
            
            cmds.connectAttr( last+'.wm', mmtxNode+'.i[0]' )
            cmds.connectAttr( other+'.wim', mmtxNode+'.i[1]' )
        
            cmds.connectAttr( lastShape+'.outMesh', trGeoNode+'.inputGeometry' )
            cmds.connectAttr( mmtxNode+'.o', trGeoNode+'.transform' )
        
            srcCons = []
            for shape in selShapes:
                if not cmds.getAttr( shape+'.io' ):
                    cons = cmds.listConnections( shape+'.inMesh', s=1, d=0, p=1, c=1 )
                    if cons:
                        srcCons = cons[1::2]
                    break
            deformer = cmds.deformer( other, type='slidingDeformer' )[0]
            
            if srcCons:
                cmds.connectAttr( srcCons[0], deformer+'.baseMesh' )
                cmds.connectAttr( trGeoNode+'.outputGeometry', deformer+'.origMesh' )
            else:
                selShapes = cmds.listRelatives( other, s=1 )
                for shape in selShapes:
                    if cmds.getAttr( shape+'.io' ):
                        cmds.connectAttr( shape+'.outMesh', deformer+'.origMesh' )
                        cmds.connectAttr( trGeoNode+'.outputGeometry', deformer+'.baseMesh' )