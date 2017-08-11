import pymel.core
from sgMaya import sgCmds
sels = pymel.core.ls( sl=1 )

blendMesh = sels[0]
resultMesh = pymel.core.duplicate( sels[0] )[0]
detailSkinedMesh = pymel.core.duplicate( sels[0] )[0]

sgCmds.autoCopyWeight( sels[0], resultMesh )
pymel.core.skinCluster( sels[0], e=1, ub=1 )

blendMesh.rename( 'facialBase_blendMesh' )
detailSkinedMesh.rename( 'facialBase_detailSkinedMesh' )
resultMesh.rename( 'face' )

bl = pymel.core.blendShape( blendMesh, detailSkinedMesh, resultMesh )[0]
bl.w[0].set( 1 )
bl.w[1].set( 1 )

grp = pymel.core.group( em=1, n='facialBase' )
pymel.core.xform( grp, ws=1, matrix= blendMesh.wm.get() )

blendMesh.setParent( grp )
detailSkinedMesh.setParent( grp )