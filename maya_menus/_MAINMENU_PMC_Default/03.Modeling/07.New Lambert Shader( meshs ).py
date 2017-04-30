import maya.cmds as cmds

sels = cmds.ls( sl=1 )
newLambShader = cmds.shadingNode( 'lambert', asShader=1, n='diplayLamber' )
newEngine = cmds.sets( renderable=1, noSurfaceShader=1, empty=1, n=newLambShader + 'SE' )
cmds.connectAttr( newLambShader + '.outColor', newEngine + '.surfaceShader' )
cmds.sets( sels, e=1, forceElement=newEngine )
cmds.select( newLambShader )