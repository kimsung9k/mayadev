from sgMaya import sgCmds, sgModel

import pymel.core

for target in pymel.core.ls( sl=1 ):
    if not pymel.core.attributeQuery( 'origObjectPath', node=target, ex=1 ): continue
    origObjectPath = target.attr( 'origObjectPath' ).get()
    namespace = 'sceneOptimizeElement'
    cmds.file( origObjectPath, i=1, type="mayaBinary", ignoreVersion=1, ra=True, mergeNamespacesOnClash=False, namespace=namespace, options="v=0;", pr=1 )
    pymel.core.refresh()
    
    topTrNodes = sgCmds.getTopTransformNodes()
    for topTrNode in topTrNodes:
        if topTrNode.find( namespace ) == -1: continue
        break
    if target.getParent():
        topTrNode.setParent( target.getParent() )

    trKeep = sgModel.TransformKeep( target )    
    trKeep.setToOther( topTrNode )

    pymel.core.delete( target )    
    namespace = ':'.join( topTrNode.split( ':' )[:-1] )
    for nstarget in pymel.core.ls( namespace + ':*' ):
        nstarget.rename( nstarget.replace( namespace + ':', '' ) )
    cmds.namespace( removeNamespace = namespace )