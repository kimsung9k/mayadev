from sgModules import sgRig

sels = cmds.ls( 'Ctl_*', type='transform' )
for sel in sels:
    sgRig.cleanController( sel )