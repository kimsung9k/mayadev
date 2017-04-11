import maya.cmds as cmds
import maya.mel as mel
import os, sys


import sgBFunction_base
sgBFunction_base.autoLoadPlugin( 'HSBVC' )

        
selectEventId = None

app_dir = mel.eval( 'getenv( "MAYA_APP_DIR" )' )
    
if not os.path.exists( app_dir+"/LocusCommPackagePrefs/HSBVC_prefs"):
    os.makedirs( app_dir+"/LocusCommPackagePrefs/HSBVC_prefs" )
    
imagePath = ''

for j in sys.path:
    if not os.path.isdir( j ):
        continue
    dirList = os.listdir( j )
    
    if 'volumeHairTool' in dirList:
        imagePath = j+'/volumeHairTool/Icon'

