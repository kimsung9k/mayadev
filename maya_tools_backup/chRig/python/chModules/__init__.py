import maya.cmds as cmds
import maya.mel as mel
import os, sys, glob

import basecode

autoLoadPlugin = basecode.AutoLoadPlugin()

autoLoadPlugin.load( 'sgLocusChRig' )
autoLoadPlugin.load( 'sgLocusChRig_t2' )
autoLoadPlugin.load( 'sgPsdNodes' )
autoLoadPlugin.load( 'sgEpCurveNode' )
autoLoadPlugin.load( 'mayaCharacterization' )
autoLoadPlugin.load( 'mayaHIK' )
autoLoadPlugin.load( 'sgIkSmoothStretch2' )
autoLoadPlugin.load( 'matrixNodes' )
autoLoadPlugin.load( 'decomposeMatrix' )
autoLoadPlugin.load( 'composeMatrix' )


chRiggingImagePath = ''
retargetingCmdImagePath = ''

for j in sys.path:
    if not os.path.isdir( j ):
        continue
    dirList = os.listdir( j )
    
    if 'chModules' in dirList and 'files' in dirList:
        chRiggingImagePath = j+'/files/image/base.png'
        retargetingCmdImagePath = j+'/files/image/retargetingImage.png'