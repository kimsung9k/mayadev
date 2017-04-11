import os
import shutil

def renameFile( targetPath, removeString ):
    
    targetPath = targetPath.replace( '\\', '/' )
    
    splits = targetPath.split( '/' )
    
    folderName = '/'.join( splits[:-1] )
    fileName   = splits[-1]
    
    fileName + fileName.replace( removeString, '' )
    
    renamedPath = folderName + '/' + fileName
    
    print targetPath
    print renamedPath
    shutil.move( targetPath, renamedPath )



targetPath = 'Z:/Deino/dpt_cgi/scenes/deino_walk/cache/master'

for root, dirs, names in os.walk( targetPath ):
    
    for name in names:
        try:renameFile( root + '/' + name, 'iguanodon_v01_' )
        except:pass
    
    break