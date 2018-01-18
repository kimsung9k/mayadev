

def makeFile():
    
    import os, ntpath
    
    def getStringFromFile( filePath ):
        f = open( filePath, 'r' )
        data = f.read()
        f.close()
        return data
    
    dirPath = os.path.dirname( __file__ )
    dirPath = dirPath.replace( '\\', '/' )
    filePath = dirPath + '/' + dirPath.split( '/' )[-2] + '.py'
    
    initFile = ntpath.split( dirPath )[0] + '/__init__.py'
    commandsFile = ntpath.split( dirPath )[0] + '/commands.py'
    modelFile = ntpath.split( dirPath )[0] + '/Model.py'
    
    data = getStringFromFile( initFile )
    
    f = open( filePath, 'w' )
    f.write( data )
    f.close()