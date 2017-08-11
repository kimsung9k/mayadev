import maya.cmds as cmds

allCtls = []
for finger in ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']:
    ctlName = 'Ctl_%s_*_*' % finger
    ctls = cmds.ls( ctlName, type='transform' )
    if not ctls: continue
    allCtls += ctls

cmds.select( allCtls )