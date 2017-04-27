import maya.cmds as cmds
from sgModules import sgdata


for defaultPluginName in sgdata.Plugins.defaultPlugins:
    if not cmds.pluginInfo( defaultPluginName, q=1, l=1 ):
        cmds.loadPlugin( defaultPluginName )