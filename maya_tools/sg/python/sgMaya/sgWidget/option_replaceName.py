from maya import cmds
import os


def makeFolder( pathName ):
    
    pathName = pathName.replace( '\\', '/' )
    splitPaths = pathName.split( '/' )
    
    cuPath = splitPaths[0]
    
    folderExist = True
    for i in range( 1, len( splitPaths ) ):
        checkPath = cuPath+'/'+splitPaths[i]
        if not os.path.exists( checkPath ):
            os.chdir( cuPath )
            os.mkdir( splitPaths[i] )
            folderExist = False
        cuPath = checkPath
        
    if folderExist: return None
        
    return pathName



def makeFile( filePath ):
    if os.path.exists( filePath ): return None
    filePath = filePath.replace( "\\", "/" )
    splits = filePath.split( '/' )
    folder = '/'.join( splits[:-1] )
    makeFolder( folder )
    f = open( filePath, "w" )
    f.close()



class Win_Global:
    
    winName = 'sg_option_replaceName'
    title   = 'Replace Name Option'
    width = 300
    height = 100
    
    data = cmds.about( pd=1 ) + '/sg/sgUIs/replaceName.txt'
    makeFile( data )
    



class Win:
    
    def __init__(self):

        pass
    
    
    def create(self):
        
        if cmds.window( Win_Global.winName, q=1, ex=1 ):
            cmds.deleteUI( Win_Global.winName )
        cmds.window( Win_Global.winName, title= Win_Global.title )
                
        cmds.window( Win_Global.winName, e=1, width= Win_Global.width, height= Win_Global.height )
        cmds.showWindow( Win_Global.winName )



def show():
    
    Win().create()



if __name__ == '__main__':
    show()