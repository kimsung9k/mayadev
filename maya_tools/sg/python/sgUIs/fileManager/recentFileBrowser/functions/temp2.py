import maya.standalone
import maya.cmds as cmds
import sys

maya.standalone.initialize( name='python' )

scenePath = 'C:/Users/skkim/Documents/maya/projects/20140514/EPA0040_ani_v01_r11.ma'
cmds.file( scenePath, force=True, open=True )
cmds.refresh()