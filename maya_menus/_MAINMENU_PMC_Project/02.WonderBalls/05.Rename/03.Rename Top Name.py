import pymel.core

numJoints = len( pymel.core.ls( type='joint' ) )

prefix = '_PR'
if numJoints > 300:
    prefix = '_CH'    

topTransforms = [ target for target in pymel.core.ls( tr=1 ) if len( target.longName().split( '|' ) ) == 2 and not target.longName() in ['|front', '|persp', '|side', '|top'] ]
assetName = cmds.file( q=1, sceneName=1 ).split( '/' )[-1].split( '.' )[0]
topTransforms[0].rename( assetName + prefix )