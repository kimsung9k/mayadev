import os

fromFile  = ''
toFile    = ''
setNames  = ['cache_set']
targetGeos= []

namespaceList = []

mayaDocPath = os.path.expanduser('~\\maya').replace( '\\', '/' )

setInfoPath         = mayaDocPath+'/LocusCommPackagePrefs/buildCache/pathInfo.txt'
geoPath             = mayaDocPath+'/LocusCommPackagePrefs/buildCache/setAndMeshInfo.txt'
timeUnitPath        = mayaDocPath+'/LocusCommPackagePrefs/buildCache/timeUnit.txt'