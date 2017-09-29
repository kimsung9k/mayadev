#coding=utf8

import os
from PySide import QtGui
import json




class WorkTreeWidget( QtGui.QTreeWidget ):
    
    def __init__(self, *args, **kwargs ):
        
        QtGui.QTreeWidget.__init__( self, *args, **kwargs )
        self.setColumnCount(2)
        headerItem = self.headerItem()
        headerItem.setText( 0, '작업이름'.decode('utf-8') )
        headerItem.setText( 1, '상태'.decode('utf-8') )




class FileUnit:
    
    def __init__(self, projectPath, taskPath, unitPath ):
        
        self.projectPath = projectPath
        self.taskPath = taskPath
        self.unitPath = unitPath
    
    def fullPath(self):
        
        return self.projectPath + self.taskPath + self.unitPath





class FileTime:

    sizeMin = 60
    sizeHour = sizeMin*60
    sizeDay  = sizeHour*24
    sizeMon  = sizeDay*30
    sizeYear = sizeMon*12

    def __init__( self, filePath ):
        
        self.filePath = filePath
    
    
    def mtime(self):
        if not os.path.exists( self.filePath ): return 0
        return int( os.path.getmtime( self.filePath ) )
    
    
    def structTime(self):
        import time
        return time.gmtime( self.mtime() )
    
    
    def __lt__(self, other):

        return self.mtime() < other.mtime()
    
    
    def __le__(self, other ):

        return self.mtime() <= other.mtime()
    
    def __eq__(self, other ):

        return self.mtime() <= other.mtime()
    
    
    def __ne__(self, other ):

        return self.mtime() != other.mtime()
    
    
    def __gt__(self, other ):

        return self.mtime() > other.mtime()


    def __ge__(self, other ):

        return self.mtime() >= other.mtime()


    def __sub__(self, other ):
        
        selfStruct = self.structTime()
        otherStruct = other.structTime()
        
        diffYear = selfStruct.tm_year - otherStruct.tm_year
        diffMon  = selfStruct.tm_mon - otherStruct.tm_mon
        diffDay  = selfStruct.tm_mday - otherStruct.tm_mday
        diffHour = selfStruct.tm_hour - otherStruct.tm_hour
        diffMin  = selfStruct.tm_min - otherStruct.tm_min
        diffsec  = selfStruct.tm_sec - otherStruct.tm_sec
        
        diffTotal = diffYear * FileTime.sizeYear + diffMon * FileTime.sizeMon + \
        diffDay * FileTime.sizeDay + diffHour * FileTime.sizeHour + diffMin * FileTime.sizeMin + diffsec
        
        return diffTotal


    @staticmethod
    def getStrFromMTime( mtime ):
        
        import time
        st = time.gmtime( mtime )
        return "%d년 %d월 %d일 %d:%d:%d".decode( 'utf-8' ) % (st.tm_year, st.tm_mon, st.tm_mday, st.tm_hour, st.tm_min, st.tm_sec )




class EditorInfo:

    def __init__(self, editorId="", host="", mtime=None ):

        self.id = editorId
        self.host = host
        self.mtime = mtime


    def getDict(self):
        return {"id":self.id, "host":self.host, "mtime":self.mtime }


    def setDict(self, dictObject ):
        self.id   = dictObject["id"]
        self.host = dictObject["host"]
        self.mtime = dictObject["mtime"]


    @staticmethod
    def getFromFile( filePath, editorInfoPath ):

        try:
            newInstance = EditorInfo()
            f = open( editorInfoPath, 'r' )
            data = json.load( f )
            f.close()
            newInstance.setDict( data )
        except:
            newInstance = EditorInfo.getMyInfo(filePath)       
            f = open( editorInfoPath, 'w' )
            json.dump( newInstance.getDict(), f )
            f.close()
        return newInstance


    @staticmethod
    def setToFile( editorInfo, filePath ):
        
        f = open( filePath, 'w' )
        json.dump( editorInfo.getDict(), f )
        f.close()
    
    
    @staticmethod
    def getMyInfo( filePath ):
        newInstance = EditorInfo()
        newInstance.id = EditorInfo.getMyId()
        newInstance.host = EditorInfo.getMyHost()
        newInstance.mtime = FileTime( filePath ).mtime()
        return newInstance



    @staticmethod
    def getMyId():
        return ""


    @staticmethod
    def getMyHost():
        
        import socket
        return socket.gethostname()
    
    
    def __eq__(self, other ):
        
        if self.id and other.id:
            return self.id == other.id
        return self.host == other.host



class CompairTwoPath:

    targetOnly  = 0
    baseOnly    = 1
    targetIsNew  = 2
    baseIsNew = 3
    same = 4


    def __init__(self, basePath, targetPath ):
        
        self.basePath = basePath
        self.targetPath = targetPath


    def basePathExists(self):
        return (lambda a: os.path.exists( a ))( self.basePath )
    
    
    def targetPathExists(self):
        return (lambda a: os.path.exists( a ))( self.targetPath )
    

    def baseTime(self):
        return int(os.path.getmtime( self.basePath ))
    
    
    def targetTime(self):
        return int(os.path.getmtime( self.targetPath ))
    
    
    def targetIsNewer(self):
        return self.targetTime() > self.baseTime()
    
    
    def targetIsOlder(self):
        return self.targetTime() < self.baseTime()
    
    
    def isSame(self):
        return self.targetTime() == self.baseTime()
    
    
    def baseIsNewer(self):
        return self.baseTime() > self.targetTime()
    
    
    def baseIsOlder(self):
        return self.baseTime() < self.targetTime()


    def getCompairResult(self):
        
        if os.path.isdir( self.basePath ):
            if not self.basePathExists():
                return CompairTwoPath.targetOnly
            if not self.targetPathExists():
                return CompairTwoPath.baseOnly
            return CompairTwoPath.same
        else:
            if not self.basePathExists():
                return CompairTwoPath.targetOnly
            if not self.targetPathExists():
                return CompairTwoPath.baseOnly
            if self.targetIsNewer():
                return CompairTwoPath.targetIsNew
            if self.baseIsNewer():
                return CompairTwoPath.baseIsNew
            return CompairTwoPath.same
        
        



