commandString = """
import maya.cmds
import maya.mel

if not maya.cmds.pluginInfo( "SGMPlugMod01", q=1, l=1 ):
    maya.cmds.loadPlugin("SGMPlugMod01")
maya.cmds.refresh()

maya.mel.eval( "SGMPlugMod01Command -st;select -cl;" )

exectarget = "%s"
f = open( exectarget, 'r' )
data = f.read()
f.close()

data = data.replace( 'MODULE_NAME', '%s' )

exec( data )
"""


import maya.cmds as cmds
import maya.mel as mel

def setTool( evt=0 ):
    import os
    
    pannel = cmds.getPanel( withFocus=True )
    
    try:mel.eval( 'setRendererInModelPanel base_OpenGL_Renderer %s;' % pannel )
    except:pass
    
    execpath = os.path.dirname( __file__ ).replace( '\\', '/' ) + '/execfunction.py'
    
    moduleName = '.'.join( __file__.split( '\\' )[1:-1] )
    
    replaceCommandString = (commandString % ( execpath, moduleName ) )
    cmds.evalDeferred( replaceCommandString )
