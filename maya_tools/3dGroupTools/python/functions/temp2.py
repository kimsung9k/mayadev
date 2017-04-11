import maya.standalone
import maya.cmds as cmds
import sys

maya.standalone.initialize( name='python' )

scenePath = 'C:/Users/skkim/Documents/maya/projects/20140514/EPA0040_ani_v01_r11.ma'
cmds.file( scenePath, force=True, open=True )
cmds.refresh()

sys.path.append( 'D:/01.codeArea/06.maya_tools' )
import animation.playblast.cmdModel as playModel

camera = 'camera1'
imageFolderPath = 'D:/retargetingData/capture1'
playModel.CommandBase().playblast( camera, imageFolderPath, -1, 266, 192, 108 )