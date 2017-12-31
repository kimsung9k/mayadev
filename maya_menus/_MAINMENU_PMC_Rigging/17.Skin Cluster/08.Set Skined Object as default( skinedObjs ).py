from sgMaya import sgPlugin

sgPlugin.appendPluginPath()

if not cmds.pluginInfo( 'sgCmdSkinCluster', q=1, l=1 ):
    cmds.loadPlugin( 'sgCmdSkinCluster' )

cmds.sgCmdSkinClustser( cmds.ls( sl=1 ), d=1 )