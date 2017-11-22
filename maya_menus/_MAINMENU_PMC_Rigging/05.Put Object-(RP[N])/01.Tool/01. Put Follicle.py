from maya import cmds
from sgMaya import sgPlugin

sgPlugin.appendPluginPath()

if not cmds.pluginInfo( 'sgPutFollicleContext', q=1, l=1 ):
    cmds.loadPlugin( 'sgPutFollicleContext' )
cmds.setToolTo( 'sgPutFollicleContext1' )