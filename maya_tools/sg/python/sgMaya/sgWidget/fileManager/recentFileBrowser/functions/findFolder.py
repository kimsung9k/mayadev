import os, sys

class findPathInfo:
    
    findPath = '_3dGroupTools'
    addPath = '/functions/findFolder.py'
    
    for path in sys.path:
        
        path = path.replace( '\\', '/' )
        
        if not os.path.isdir( path ):
            continue
        
        dirList = os.listdir( path )
        
        if findPath in dirList:
            findPath = path+addPath