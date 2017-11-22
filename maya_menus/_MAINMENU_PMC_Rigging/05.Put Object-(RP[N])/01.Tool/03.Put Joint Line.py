from maya import cmds
from sgMaya import sgPlugin

if not cmds.pluginInfo( 'sgPutJointLineContext', q=1, l=1 ):
    cmds.loadPlugin( 'sgPutJointLineContext' )
cmds.setToolTo( 'sgPutJointLineContext1' )