from maya import cmds
import sgPlugin

if not cmds.pluginInfo( 'sgPutFollicleContext', q=1, l=1 ):
    cmds.loadPlugin( 'sgPutFollicleContext' )
cmds.setToolTo( 'sgPutFollicleContext1' )