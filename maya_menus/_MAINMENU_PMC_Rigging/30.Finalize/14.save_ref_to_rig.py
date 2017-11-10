from maya import cmds
import ntpath, os

scenePath = cmds.file( q=1, sceneName=1 )
folderPath, sceneName = ntpath.split( scenePath )
name, ext = os.path.splitext( sceneName )
rigName = name.replace( '_ref', '' )
newScenePath = folderPath + '/' + rigName + ext

cmds.file( rename=newScenePath )
cmds.file( save=1, f=1 )