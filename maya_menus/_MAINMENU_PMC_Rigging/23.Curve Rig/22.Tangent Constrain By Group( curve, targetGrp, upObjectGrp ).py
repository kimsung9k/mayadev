import pymel.core
from maya import cmds
from sgMaya import sgCmds

curve = 'curve3'
targets = cmds.ls( sl=1 )
upObjects = cmds.ls( 'Ctl_dt_*', type='transform' )

sgCmds.tangentContraintByGroup( curve, targets, upObjects, [0,1,0] )