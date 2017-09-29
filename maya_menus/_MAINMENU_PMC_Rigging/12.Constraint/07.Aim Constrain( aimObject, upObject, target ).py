from sgMaya import sgCmds
import pymel.core
aimTarget, upTarget, rotTarget = pymel.core.ls( sl=1 )
sgCmds.aimConstraint( aimTarget, upTarget, rotTarget )