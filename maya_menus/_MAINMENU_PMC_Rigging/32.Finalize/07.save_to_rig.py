import os
from maya import cmds
import ntpath

sceneName = cmds.file( q=1, sceneName=1 )
dirPath, fileName = ntpath.split( sceneName )

name, ext = os.path.splitext( fileName )

if name[-4:] == '_ref':
    name = name[:-4]

if name[-4:] != '_rig':
    rigPath = dirPath + '/' + name + '_rig' + ext
    cmds.file( rename=rigPath )

cmds.file( save=1 )