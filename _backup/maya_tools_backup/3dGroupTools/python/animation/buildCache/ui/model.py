import sys, os


class CacheDataPathInfo:

    mayaDocPath = os.path.expanduser('~\\maya').replace( '\\', '/' )
    
    _setInfoPath  = mayaDocPath+'/LocusCommPackagePrefs/buildCache/pathInfo.txt'
    _meshInfoPath = mayaDocPath+'/LocusCommPackagePrefs/buildCache/setAndMeshInfo.txt'
    _timeUnitPath = mayaDocPath+'/LocusCommPackagePrefs/buildCache/timeUnit.txt'
    
    _defaultSetName = 'cache_set'



class BuildCacheInfo:
    
    _mayapyPath = ''
    _launchPath = ''
    
    for path in sys.path:
        
        path = path.replace( '\\', '/' )
        
        if not os.path.isdir( path ):
            continue
        dirList = os.listdir( path )
        if 'CER' in dirList and 'Symbol' in dirList:
            _mayapyPath = path+'/mayapy.exe'
        elif 'standalone' in dirList and 'animation' in dirList:
            _launchPath = path+"/standalone/cache/launch.py"