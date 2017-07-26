import sgPlugin
from sgMaya import sgCmds

if not cmds.pluginInfo( 'sgCmdSkinCluster', q=1, l=1 ):
    cmds.loadPlugin( 'sgCmdSkinCluster' )

targets = []
for mesh in pymel.core.ls( type='mesh' ):
    if not sgCmds.getNodeFromHistory( mesh, 'skinCluster' ): continue
    targets.append( mesh.name() )

for target in targets:
    cmds.select( target )
    cmds.sgCmdSkinClustser( cmds.ls( sl=1 ), d=1 )
cmds.select( d=1 )