import maya.cmds as cmds
import os
baseDir = os.path.dirname( cmds.file( q=1, sceneName=1 ) )
refNodes = cmds.ls( type='reference' )
for refNode in refNodes:
    fileName = cmds.referenceQuery( refNode, filename=1 ) 
    refTarget = baseDir + '/' + os.path.basename( fileName )
    if not os.path.exists( refTarget ): continue
    cmds.file( refTarget, loadReference = refNode )