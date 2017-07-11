from sgMaya import sgCmds
import pymel.core

meshGrps = pymel.core.ls( sl=1 )
children = pymel.core.listRelatives( meshGrps, c=1, ad=1, type='transform' )

for child in children:
    skinNode = sgCmds.getNodeFromHistory( child, 'skinCluster' )
    blendNode = sgCmds.getNodeFromHistory( child, 'blendShape' )
    if skinNode:
        skinNode[0].rename( 'sk_' + child.name() )
        print skinNode[0].name()
    if blendNode:
        blendNode[0].rename( 'bl_' + child.name() )
        print blendNode[0].name()