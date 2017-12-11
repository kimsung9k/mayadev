from sgMaya import sgCmds
import maya.cmds as cmds
sels = pymel.core.ls( sl=1 )

jntGrp     = sels[0]
bindPreGrp = sels[1]
targetSkin = sels[2]

chJnts = jntGrp.listRelatives( c=1, type='transform' )
chBindPres = bindPreGrp.listRelatives( c=1, type='transform' )

for i in range( len( chJnts ) ):
    sgCmds.connectBindPreMatrix( chJnts[i], chBindPres[i], targetSkin )