import maya.cmds as cmds

sels = cmds.ls( sl=1 )
ctl = sels[0]
fCtl = sels[1]

if not cmds.attributeQuery( 'showFacial', node= ctl, ex=1 ):
    cmds.addAttr( ctl, ln='showFacial', at='long', min=0, max=1, dv=1 )
    cmds.setAttr( ctl + '.showFacial', e=1, cb=1 )
cmds.connectAttr( ctl + '.showFacial', fCtl + '.v', f=1 )