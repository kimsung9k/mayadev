#coding=utf8

import maya.cmds as cmds
from maya import OpenMayaUI
from PySide import QtGui, QtCore
import shiboken
import os, sys
import json



class FileAndPaths:

    @staticmethod
    def getArrangedPathString( path ):
        return path.replace( '\\', '/' ).replace( '//', '/' ).replace( '//', '/' )



    @staticmethod
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



    @staticmethod
    def makeFile( filePath ):
        
        if os.path.exists( filePath ): return None
        filePath = filePath.replace( "\\", "/" )
        splits = filePath.split( '/' )
        folder = '/'.join( splits[:-1] )
        FileAndPaths.makeFolder( folder )
        f = open( filePath, "w" )
        json.dump( {}, f )
        f.close()
    


    @staticmethod
    def getFileFromBrowser( parent, defaultPath = '' ):
        
        dialog = QtGui.QFileDialog( parent )
        dialog.setDirectory( defaultPath )
        fileName = dialog.getOpenFileName()[0]
        return fileName.replace( '\\', '/' )
    
    
    
    @staticmethod
    def getFolderFromBrowser( parent, defaultPath = '' ):
        
        dialog = QtGui.QFileDialog( parent )
        dialog.setDirectory( defaultPath )
        choosedFolder = dialog.getExistingDirectory()
        return choosedFolder.replace( '\\', '/' )


    @staticmethod
    def getStringDataFromFile( filePath ):
        
        if not os.path.exists( filePath ): return ''
        f = open( filePath, 'r' )
        data = f.read()
        f.close()
        return data


    @staticmethod
    def setStringDataToFile( data, filePath ):
        
        if not os.path.exists( filePath ): return None
        f = open( filePath, 'w' )
        f.write( data )
        f.close()
        
        
        
        
class StringEdit:
    
    @staticmethod
    def convertFilenameToMenuname( filename, extlist=['txt','py','mel'] ):
        
        splits = filename.split( '.' )
        if not splits[0]: return None
        if splits[0].isdigit():
            targetName = '.'.join( splits[1:] )
        else:
            targetName = filename
        
        splits2 = targetName.split( '.' )
        if len( splits2 ) >= 2 and not splits2[-1] in extlist: return None
        
        return os.path.splitext( targetName.replace( '#', '' ).strip() )[0]
        
        
            
            
