import maya.cmds as cmds

try:cmds.evalDeferred( 'import _3dGroupTools' )
except:pass
try:cmds.evalDeferred( "import sgBExcute_startup" )
except:pass
try:
	cmds.evalDeferred( "import sgCFnc_ui" )
except:
	print "local maya menu create is failed"
	pass