import maya.cmds as cmds
import maya.mel as mel
import os, sys
import chModules.basecode as basecode

plugList = cmds.pluginInfo( q=1, listPlugins=1 )

autoLoadPlugin = basecode.AutoLoadPlugin()

autoLoadPlugin.load( 'sgRetargetNodes' )

app_dir = mel.eval( 'getenv( "MAYA_APP_DIR" )' )
    
if not os.path.exists( app_dir+"/LocusCommPackagePrefs/Retargeting_prefs"):
    os.makedirs( app_dir+"/LocusCommPackagePrefs/Retargeting_prefs" )