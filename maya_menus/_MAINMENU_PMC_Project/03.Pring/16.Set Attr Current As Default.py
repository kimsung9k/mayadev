from sgMaya import sgCmds

for sel in cmds.ls( 'Ctl_*', type='transform' ):
    sgCmds.setAttrCurrentAsDefault( sel )