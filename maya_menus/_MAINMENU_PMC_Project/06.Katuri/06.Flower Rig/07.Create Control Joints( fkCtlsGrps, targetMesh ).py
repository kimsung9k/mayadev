import pymel.core
from sgMaya import sgCmds

sels = pymel.core.ls( sl=1 )
transforms = pymel.core.listRelatives( sels[:-1], c=1, type='transform' )
topGrp = sels[-1].getAllParents()[-1]

topJoints = []
for tr in transforms:
    joints = sgCmds.createFkControlJoint( tr )
    topJoints.append( joints[0] )

topJntGrp = pymel.core.group( topJoints, n='cj_'+topGrp )