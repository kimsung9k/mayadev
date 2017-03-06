import cmdModel
import model
import os


def makePath( pathName ):
    splitPaths = pathName.split( '/' )
    
    cuPath = splitPaths[0]
    
    for i in range( 1, len( splitPaths ) ):
        checkPath = cuPath+'/'+splitPaths[i]
        if not os.path.exists( checkPath ):
            os.chdir( cuPath )
            os.mkdir( splitPaths[i] )
        cuPath = checkPath
        
        
        
def makeFile( pathName ):
    splitPaths = pathName.split( '/' )
    
    folderPath = '/'.join( splitPaths[:-1] )
    
    makePath( folderPath )
    
    if not os.path.exists( pathName ):
        f = open( pathName, 'w' )
        f.close()

cmdModel.setCacheInfoFromText( model.setInfoPath, model.geoPath )

f = open( model.setInfoPath, 'r' )
paths = f.read()
f.close()
path = paths.split( '\n' )[1].strip().replace( '\\', '/' )+'/meshData.bat'

makeFile( path )
cmdModel.createCachePerGeometry( path )