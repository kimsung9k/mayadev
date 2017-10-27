import maya.cmds as cmds

try:
	cmds.evalDeferred( 'import pmc' )
	cmds.evalDeferred( 'pmc.MenuController().create()' )
except:pass