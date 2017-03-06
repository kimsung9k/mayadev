import sys

import sgFunctionFileAndPath


fromPath = 'D:/tools/sgTools/packages/3dGroupTools/pythons/mayaWindow'
toPath1  = 'X:/tools/maya/2013-x64/packages/3dGroup/pythons/mayaWindow'
toPath2  = 'X:/tools/maya/2015-x64/packages/3dGroup/pythons/mayaWindow'

sgFunctionFileAndPath.copyFilesToTargetPath(fromPath, toPath1)
print "2013 update success"
sgFunctionFileAndPath.copyFilesToTargetPath(fromPath, toPath2)
print "2015 update success"