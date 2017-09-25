import maya.cmds as cmds

for jnt in cmds.ls( type='joint' ):
    if not cmds.attributeQuery( 'lockInfluenceWeights', node=jnt, ex=1 ): continue
    cmds.setAttr( jnt+'.lockInfluenceWeights', 0 )