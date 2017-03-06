import shutil
import sgModelFileAndPath

localMayaPath = sgModelFileAndPath.getMayaDocPath()

localPath2013 = localMayaPath+'/2013-x64/scripts/userSetup_local.py'
localPath2015 = localMayaPath+'/2015-x64/scripts/userSetup_local.py'
serverPath2013 = 'X:/tools/maya/2013-x64/dist/userSetup.py'
serverPath2015 = 'X:/tools/maya/2015-x64/dist/userSetup.py'

targetPath2013 = localMayaPath+'/2013-x64/scripts/userSetup.py'
targetPath2015 = localMayaPath+'/2015-x64/scripts/userSetup.py'

#shutil.copy2( localPath2013, targetPath2013 )
shutil.copy2( serverPath2013, targetPath2013 )

print "excuted tool path"