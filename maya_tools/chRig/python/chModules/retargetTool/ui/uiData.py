import maya.cmds as cmds
import maya.mel as mel
import os, sys
import chModules.retargetTool as main

winWidth  = 400
winHeight = 70

exportData_height = 294
retargeting_height = 301
timeControl_height = 301
editTransform_height = 339
bake_height = 261

winName = 'retarget_mainUi'

targetWorldCtl = ''

updateFunctionList = []

folderPath = mel.eval( 'getenv MAYA_APP_DIR' )+'/LocusCommPackagePrefs/Character_Rig/Retargeting'

eventAble = False

exportDataFolderImagePath = ''

for j in sys.path:
    if not os.path.isdir( j ):
        continue
    dirList = os.listdir( j )
    
    if 'chModules' in dirList and 'files' in dirList:
        exportDataFolderImagePath = j+'/files/image/folder.png'


def eventAbleTrue( *args ):
    global eventAble
    eventAble = True
    
def eventAbleFalse( *args ):
    global eventAble
    eventAble = False


if not os.path.exists( folderPath ):
    os.makedirs( folderPath )


def setSpace( h=5 ):
    cmds.text( l='', h=h )


def addFrameLayout( uiName, label, vis=0, collapseAble=0, collapse=0 ):
    
    frame = cmds.frameLayout( uiName, l=label, vis=vis, cll=collapseAble, cl=collapse )
    cmds.frameLayout( lv=0, bs='out' )
    return frame


def saveData( fileName, writeString, *args ):

    app_dir = main.app_dir+"/LocusCommPackagePrefs"

    path = app_dir+"/Retargeting_prefs/%s.txt" % fileName
    
    fileTextSpace = open( path, 'w' )
    fileTextSpace.write( writeString )
    fileTextSpace.close()
        
    
def openText( fileName, *args ):
    
    app_dir = main.app_dir+"/LocusCommPackagePrefs"

    path = app_dir+"/Retargeting_prefs/%s.txt" % fileName
    
    if not os.path.exists( path ):
        return None
    
    fileTextSpace = open( path, 'r' )
    text = fileTextSpace.read()
    fileTextSpace.close()
    
    return text