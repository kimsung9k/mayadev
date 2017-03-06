import os, shutil
import functions.path


def copyFilesToTargetPath( fromPath, toPath ):
    
    fromPath = fromPath.replace( '\\', '/' )
    toPath = toPath.replace( '\\', '/' )
    
    try:functions.path.deletePathHierarchy( toPath )
    except: pass
    
    for root, dirs, names in os.walk( fromPath ):
        
        toRoot = root.replace( '\\', '/' ).replace( fromPath, toPath )
        
        for dir in dirs:
            functions.path.makeFolder( toRoot+'/'+dir )
        for name in names:
            if name.split('.')[1].lower() == 'pyc': continue
            shutil.copy2( root+'/'+name, toRoot+'/'+name )
    
    print "Is Done"


fromPath = 'D:/tools/maya/2013-x64/packages/3dGroup/pythons'
toPath1  = 'X:/tools/maya/2015-x64/packages/3dGroup/pythons'

copyFilesToTargetPath( fromPath, toPath1 )

'''
fromPath = 'D:/01.codeArea/03.autoRig'
toPath1 = 'X:/tools/maya/2015-x64/packages/chRig/pythons'

copyFilesToTargetPath( fromPath, toPath1 )'''