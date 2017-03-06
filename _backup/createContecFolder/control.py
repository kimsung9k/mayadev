#-*- coding:cp949 -*-
#-*- coding:utf-8 -*-

from model import *

import os, shutil

def pictureElseSet():
    
    for num in Info._pictureNums2:
        if not num in Info._pictureNums1:
            Info._pictureNums3.append( num )
    print len( Info._pictureNums3 )



def pictureElseSet2():
    
    for num in Info2._pictureNums:
        if not num in Info._pictureNums1 and not num in Info._pictureNums2:
            Info2._pictureNums2.append( num )

  
            
def addDefaultFolders( path ):
    for addFolder in [ Info._beforeJpec,
                       Info._afterJpec,
                       Info._raw,
                       Info._psd ]:
        addPath = path + '/' + addFolder
        if not os.path.exists( addPath ):
            os.mkdir( addPath )
            

def setFiles( folderName, pictureNums ):
    
    folderPath = Info._mainPath + '/' + Info._setFolder
    
    if not os.path.exists( folderPath ):
        os.mkdir( folderPath )
        
    folderPath += "/" + folderName
    
    if not os.path.exists( folderPath ):
        os.mkdir( folderPath )
        
    print folderPath
    
    for root, dirs, names in os.walk( Info._mainPath ):
        root = root.replace( '\\', '/' ).replace( '굚', '/' )
        if root.find( folderPath ) != -1:
            continue
        
        for fileName in names:
            
            name, ext = fileName.split( '.' )
            
            numStr = name[-4:]
            if not numStr.isdigit(): continue
            num = int( numStr )
            
            splits = root.replace( Info._mainPath, '' ).split( '/' )
            
            if splits[0]:
                clientFolderName = splits[0]
            else:
                clientFolderName = splits[1]

            if num in pictureNums:
                clientPath = folderPath + '/' + clientFolderName
                if not os.path.exists( clientPath ):
                    os.mkdir( clientPath )
                addDefaultFolders( clientPath )
                
                jpgPath = clientPath + '/' + Info._beforeJpec
                rawPath = clientPath + '/' + Info._raw
                
                beforePath = root + '/' + fileName
                if ext.lower() == Info._extJpec:
                    afterPath = jpgPath + '/' + fileName
                    if not os.path.exists( afterPath ):
                        shutil.copy2( beforePath, afterPath )
                elif ext.lower() == Info._extRaw:
                    afterPath = rawPath + '/' + fileName
                    if not os.path.exists( afterPath ):
                        shutil.copy2( beforePath, afterPath )