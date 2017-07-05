import maya.cmds as cmds
sceneName = cmds.file( q=1, sceneName=1 )
sceneFolder = os.path.dirname( sceneName )
sceneFileName = sceneName.split( '/' )[-1].split( '.' )[0]
proxyname = sceneFileName.replace( 'SET_', '' )
proxyFolder = sceneFolder + '/' + proxyname
try:os.mkdir( proxyFolder )
except:pass

startFrame = cmds.playbackOptions( q=1, min=1 )
endFrame = cmds.playbackOptions( q=1, max=1 )

proxyPath = sceneFolder + '/' + proxyname + '/' + proxyname + '.rs'
cmds.rsProxy( 'SET', fp=proxyPath, s=startFrame, e=endFrame, b=1 )