import maya.cmds as cmds
import maya.mel as mel
import os

plugList = cmds.pluginInfo( q=1, listPlugins=1 )

if not plugList:
    cmds.loadPlugin( 'locusFacial' )
else:
    if not 'locusFacial' in plugList:
        cmds.loadPlugin( 'locusFacial' )