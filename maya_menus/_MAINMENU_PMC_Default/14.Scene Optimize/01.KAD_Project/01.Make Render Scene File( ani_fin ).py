from maya import cmds
import os, ntpath
filePath = cmds.file( q=1, sceneName=1 )

folder, fileName = ntpath.split( filePath )
fileName = fileName.replace( 'EP0', 'EP1' ).replace( 'ep0', 'EP1' )

replaceSrcs = ['03_Main-Production/05_Animation', 'scene/fin', 'scene' ]
replaceDsts = ['04_Shot-Production/05_RenderScenes', '', '' ]
for i in range( len( replaceSrcs ) ):
    folder = folder.replace( replaceSrcs[i], replaceDsts[i] )

shotFolderName = '_'.join( fileName.split( '_' )[:2] ).upper()
shotFolderPath = folder + '/' + shotFolderName
shotFilePath = shotFolderPath + '/' + shotFolderName + '_OPTIMIZED.mb'

if not os.path.exists( shotFolderPath ):
    os.mkdir( shotFolderPath )

cmds.file( rename=shotFilePath )
cmds.file( s=1, f=1 )