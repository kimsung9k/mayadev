from maya import cmds
from sgMaya import sgPlugin

sgPlugin.appendPluginPath()

if not cmds.pluginInfo( 'sgPutInsideContext', q=1, l=1 ):
    cmds.loadPlugin( 'sgPutInsideContext' )
cmds.setToolTo( 'sgPutInsideContext1' )