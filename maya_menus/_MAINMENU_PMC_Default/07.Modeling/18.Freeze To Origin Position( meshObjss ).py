import maya.cmds as cmds
sels = cmds.ls( sl=1 )
for sel in sels:
    cmds.move( 0,0,0, sel + '.rotatePivot', sel + '.scalePivot', rpr=1 )
    cmds.makeIdentity( sel, apply=1, t=1, r=1, s=1, n=0, pn=1 )