import maya.cmds as cmds

try:
	cmds.evalDeferred( 'import sgMenu' )
	cmds.evalDeferred( 'sgMenu.MenuController().create()' )
except:pass