import maya.mel as mel
import os


appdir = mel.eval( 'getenv MAYA_APP_DIR' )
tempCharacterPath = appdir + '/LocusCommPackagePrefs/tempData'


def createPath():
        
    if not "LocusCommPackagePrefs" in os.listdir( appdir ):
        os.chdir( appdir )
        os.mkdir( "LocusCommPackagePrefs" )
    if not "tempData" in os.listdir( appdir+'/LocusCommPackagePrefs' ):
        os.chdir( appdir+'/LocusCommPackagePrefs' )
        os.mkdir( "tempData" )

createPath()


class DummyInfo:
    
    _pathSrc  = 'M:/tools/cgi/maya/2013-x64/database/character'
    _pathDest = tempCharacterPath