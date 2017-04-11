import sys, os


class OpenFileTextureManagerInfo:
    
    _melScriptPath = ''
    
    for path in sys.path:
        if not os.path.isdir( path ):
            continue
        
        dirList = os.listdir( path )
        if 'shading' in dirList:
            _melScriptPath = path+'/shading/texture/FileTextureManager.mel'