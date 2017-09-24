from maya import cmds
import sgPlugin

if not cmds.pluginInfo( 'sgPutInsideContext', q=1, l=1 ):
    cmds.loadPlugin( 'sgPutInsideContext' )
cmds.setToolTo( 'sgPutInsideContext1' )