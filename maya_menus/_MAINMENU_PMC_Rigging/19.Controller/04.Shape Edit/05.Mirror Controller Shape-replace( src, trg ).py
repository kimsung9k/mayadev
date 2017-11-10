from sgMaya import sgCmds
import pymel.core
sels = pymel.core.ls( sl=1 )

pymel.core.delete( sels[1].listRelatives( s=1 ) )
newObj = pymel.core.createNode( 'transform' )
pymel.core.parent( sels[0].listRelatives( s=1 ), newObj, add=1, shape=1 )
duNewObj = pymel.core.duplicate( newObj )[0]
pymel.core.parent( duNewObj.listRelatives( s=1 ), sels[1], add=1, shape=1 )
pymel.core.delete( newObj, duNewObj )
sgCmds.mirrorControllerShape( sels[1] )