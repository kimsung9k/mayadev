from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )

minusGrp = sels[0]
plusGrp  = sels[1]
target = sels[-1]

minChildren  = minusGrp.listRelatives( c=1 )
plusChildren = plusGrp.listRelatives( c=1 )

for i in range( len( minChildren ) ):
    duTarget = pymel.core.duplicate( target )[0]
    duTarget.setParent( w=1 )
    blendNode = pymel.core.blendShape( minChildren[i], plusChildren[i], duTarget )[0]
    blendNode.w[0].set( -1 )
    blendNode.w[1].set( 1 )
    duTarget.rename( 'fix_' + plusChildren[i] )