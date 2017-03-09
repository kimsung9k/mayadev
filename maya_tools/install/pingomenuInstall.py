import shutil, os


def makeFolder( pathName, rename=False ):
    
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
    
    if folderExist and rename:
        pathName = checkSamePathAndRenamePath( pathName )
        os.mkdir( pathName )
        
    return pathName
        


def makeFile( pathName ):
    
    pathName = pathName.replace( '\\', '/' )
    splitPaths = pathName.split( '/' )
    folderPath = '/'.join( splitPaths[:-1] )
    makeFolder( folderPath )
    
    if not os.path.exists( pathName ):
        f = open( pathName, 'w' )
        f.close()
    return pathName


sourcePath = 'D:/PINGO_SERVER/pingo_server1/@@DEV@@/maya_tools/userSetup.py'
targetPath = os.path.expanduser( '~/Documents/maya/scripts' ) + '/userSetup.py'

shutil.copy2( sourcePath, targetPath )

defaultMenuPath = 'D:/PINGO_SERVER/pingo_server1/@@DEV@@/maya_menus/_MAINMENU_Default'

menuList2015 = os.path.expanduser( '~/Documents/maya/2015-x64' ) + '/sgMenu/menuList.txt'
loadMenuList2015 = os.path.expanduser( '~/Documents/maya/2015-x64' ) + '/sgMenu/loadMenuList.txt'
menuList2016 = os.path.expanduser( '~/Documents/maya/2016' ) + '/sgMenu/menuList.txt'
loadMenuList2016 = os.path.expanduser( '~/Documents/maya/2016' ) + '/sgMenu/loadMenuList.txt'
targetFiles = [menuList2015,loadMenuList2015,menuList2016,loadMenuList2016]

for targetFile in targetFiles:
	makeFile( targetFile )
	f = open( targetFile, 'r' )
	data = f.read()
	f.close()

	paths = data.split( ';' )
	if defaultMenuPath in paths: continue
	paths.append( defaultMenuPath )
	data = ';'.join( paths )

	f = open( targetFile, 'w' )
	f.write( data )
	f.close()