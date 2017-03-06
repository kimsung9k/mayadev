
import maya.standalone
import maya.cmds as cmds
import sys
maya.standalone.initialize( name='python' )

sys.path.append( 'D:/Github/private/maya_tools/sg/python\sgUIs\sceneExport' )

import exportTarget
exportTarget.makeCamScene( "D:/PRIVATE/scenes/pingo_ep008_c007/ch_100_aram_rig_ARAM_Set.ma", "D:/PRIVATE/scenes/pingo_ep008_c007_caminfomation.txt" )
