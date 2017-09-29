from sgMaya import sgCmds
from sgMaya import sgAnim
sels = cmds.ls( sl=1 )
sgAnim.createXLookAtJointLine( sels )