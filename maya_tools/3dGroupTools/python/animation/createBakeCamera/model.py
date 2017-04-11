import os, sys

mayaDocPath = os.path.expanduser('~\\maya').replace( '\\', '/' )
defaultFileBrowserPath = mayaDocPath+'/projects'
infoPath = mayaDocPath+'/LocusCommPackagePrefs/hgCameraBake/pathInfo.txt'
lastInfoPath = mayaDocPath+'/LocusCommPackagePrefs/hgCameraBake/lastInfo.txt'
cameraListPath = mayaDocPath+'/LocusCommPackagePrefs/hgCameraBake/cameraList.txt'

for path in sys.path:
    path = path.replace( '\\', '/' )
    
    if not os.path.isdir( path ):
        continue
    dirList = os.listdir( path )
    if 'CER' in dirList and 'Symbol' in dirList:
        mayapyPath = path+'/mayapy.exe'
    elif 'standalone' in dirList and 'animation' in dirList:
        launchPath = path+"/standalone/hgCameraBake/launch.py"