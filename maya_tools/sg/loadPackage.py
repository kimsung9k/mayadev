import maya.cmds as cmds

try:
	cmds.evalDeferred( 'import sgMenu' )
	cmds.evalDeferred( 'sgMenu.MenuController().create()' )
except:pass

try:
	cmds.evalDeferred( 'import sgPlugin' )
except:pass

try:
	cmds.evalDeferred( 'from sgModules import sgcommands' )
	cmds.evalDeferred( 'sgcommands.DuplicateSourceObjectSet.createEvent()' )
except:pass