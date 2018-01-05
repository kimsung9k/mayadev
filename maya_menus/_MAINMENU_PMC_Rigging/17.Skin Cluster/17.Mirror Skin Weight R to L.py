import pymel.core
from sgMaya import sgCmds
from maya import cmds

sels = pymel.core.ls( sl=1 )

def mirrorSkinCluster( targets, inverse = False ):
    if len( sels ) == 1:
        srcSkin = sgCmds.getNodeFromHistory( sels[0], 'skinCluster' )[0]
        dstSkin = srcSkin
    elif len( sels ) == 2:
        srcSkin = sgCmds.getNodeFromHistory( sels[0], 'skinCluster' )[0]
        dstSkin = sgCmds.getNodeFromHistory( sels[1], 'skinCluster' )[0]
    else:
        return None

    cmds.copySkinWeights( ss=srcSkin.name(), ds=dstSkin.name(), mirrorMode='YZ', surfaceAssociation = 'closestPoint', 
                          influenceAssociation=['oneToOne','closestJoint'], mirrorInverse=inverse )

mirrorSkinCluster( sels, True )