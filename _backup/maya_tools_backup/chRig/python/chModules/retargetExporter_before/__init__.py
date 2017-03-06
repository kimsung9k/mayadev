import maya.mel as mel
import os

import mainInfo

maya_app_dir = mel.eval( "getenv MAYA_APP_DIR" )
settingInfoPath = maya_app_dir + '/LocusCommPackagePrefs/RetargetExporter_prefs'

if not os.path.exists( settingInfoPath ):
    os.makedirs( settingInfoPath )

pathInfoPath = settingInfoPath+'/exportOptionData.txt'
uiInfoPath   = settingInfoPath+'/exportUiData.txt'
mainInfo.pathInfoPath = pathInfoPath
mainInfo.uiInfoPath   = uiInfoPath

if os.path.exists( pathInfoPath ):
    f = open( pathInfoPath, 'r' )
    fileStr = ''
    fileStr = f.read( )
    f.close()
    
    mainInfo.motionExportPath, mainInfo.hikExportPath = fileStr.split( '\n' )
else:
    fileStr = maya_app_dir+'\n'+maya_app_dir
    
    f = open( pathInfoPath, 'w' )
    f.write( fileStr )
    f.close()
    
    mainInfo.motionExportPath = maya_app_dir
    mainInfo.hikExportPath    = maya_app_dir
    
if os.path.exists( uiInfoPath ):
    f = open( uiInfoPath, 'r' )
    fileStr = ''
    fileStr = f.read( )
    f.close()
    
    mainInfo.fileTypeOption, mainInfo.namespaceOption, mainInfo.frontNameOption, mainInfo.thisString = fileStr.split( '\n' )
else:
    fileStr = 'all'+'\n'+'prefix'+'\n'+'fileName'+'\n'
    
    f = open( uiInfoPath, 'w' )
    f.write( fileStr )
    f.close()
    
    mainInfo.fileTypeOption   = 'all'
    mainInfo.namespaceOption  = 'prefix'
    mainInfo.frontNameOption  = 'fileName'
    mainInfo.thisString = ''