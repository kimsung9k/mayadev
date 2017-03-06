import model
import maya.cmds as cmds
import os

import shutil



def getFileList():
    
    sourceFolderPath = model.DummyInfo._pathSrc
    
    fileNames = []
    for root, dirs, names in os.walk( sourceFolderPath ):
        names.reverse()
        
        for name in names:
            fileNames.append( name.split( '.' )[0] )
        break

    return fileNames



def mmOpenDummyCharacter( index, *args ):
    
    sourceFolderPath = model.DummyInfo._pathSrc
    destFolderPath   = model.DummyInfo._pathDest
    
    for root, dirs, names in os.walk( sourceFolderPath ):
        names.reverse()
        break
    
    if not names: return None
    targetFile = ''
    if len( names ) <= index:
        targetFile = names[-1]
    else:
        targetFile = names[index]
    
    shutil.copy2( sourceFolderPath +'/'+ targetFile, destFolderPath +'/'+ targetFile )
    
    cmds.file( destFolderPath +'/'+ targetFile, f=1, options="v=0", ignoreVersion=1, typ="mayaBinary", o=1 )