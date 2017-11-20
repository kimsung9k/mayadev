from sgMaya import sgCmds
from maya import cmds

sels = cmds.ls( sl=1 )
sgCmds.putObject( sels, 'joint' )