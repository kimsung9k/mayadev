import maya.cmds as cmds


def replaceObject( source, target ):
    
    import sgRigDag
    import sgRigSkinCluster
    import sgBFunction_dag
    
    skinClusters = sgBFunction_dag.getNodeFromHistory( target, 'skinCluster' )
    
    if skinClusters:
        sgRigSkinCluster.replaceObjectSkined( source, target )
    else:
        sgRigDag.replaceObject( source, target )