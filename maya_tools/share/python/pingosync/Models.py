#coding=utf8

import maya.cmds as cmds
from maya import OpenMayaUI
from __qtImport import *
import os



class ControlBase:
    
    mayawin = shiboken.wrapInstance( long( OpenMayaUI.MQtUtil.mainWindow() ), QWidget )
    
    mainui = QMainWindow()
    manageui = QMainWindow()
    uiTreeWidget = QWidget()
    
    infoBaseDir = cmds.about( pd=1 ) + "/pingowms"
    uiInfoPath = infoBaseDir + '/uiInfo.json'
    projectListPath = infoBaseDir + '/projectList.json'
    defaultInfoPath = infoBaseDir + '/defaultInfo.json'
    
    labelServerPath = 'serverPath'
    labelLocalPath = 'localPath'
    labelCurrentProject = 'currentProject'
    labelDefaultLocalPath = "defaultLocalFolder"
    labelDefaultServerPath = 'defaultServerPath'
    labelDefaultTaskFolder = 'defaultTaskFolder'
    labelDefaultTaskType = 'defaultTaskType'
    labelTasks    = 'tasks'
    labelTaskType = 'type'
    labelTaskPath = 'path'
    
    backupDirName = '_backup'
    backupFileName = 'backup_'
    
    editorInfoExtension = 'pingowmsEditorInfo'


class Colors:
    
    localOnly = QColor( 120, 180, 255 )
    serverOnly = QColor( 100, 100, 100 )
    localModified = QColor( 100, 255, 100 )
    serverModified = QColor( 255, 100, 100 )
    equar = QColor( 255, 255, 255 )




class WorkTreeWidget( QTreeWidget ):
    
    def __init__(self, *args, **kwargs ):
        
        QTreeWidget.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setColumnCount(3)
        headerItem = self.headerItem()
        headerItem.setText( 0, '작업이름'.decode('utf-8') )
        headerItem.setText( 1, '상태'.decode('utf-8') )
        headerItem.setText( 2, '경로'.decode('utf-8') )




class FileUnit:
    
    def __init__(self, projectPath, taskPath, unitPath ):
        
        self.projectPath = projectPath.replace( '\\', '/' )
        self.taskPath = taskPath.replace( '\\', '/' )
        self.unitPath = unitPath.replace( '\\', '/' )
    
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
        return time.localtime( os.path.getmtime( self.filePath ) )


    def stringTime(self):
        structTime = self.structTime()
        return '%04d.%02d.%02d.%02d%02d%02d' % (structTime.tm_year, structTime.tm_mon, structTime.tm_mday, structTime.tm_hour, structTime.tm_min, structTime.tm_sec)
        
        
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


    @staticmethod
    def getStrFromMTime( mtime ):
        
        import time
        st = time.localtime( mtime )
        return "%04d년 %02d월 %02d일 %02d:%02d:%02d".decode( 'utf-8' ) % (st.tm_year, st.tm_mon, st.tm_mday, st.tm_hour, st.tm_min, st.tm_sec )




class EditorInfo:

    def __init__(self, filePath, editorId="", host="" ):

        self.id = editorId
        self.host = host
        self.mtime = FileTime(filePath).mtime()
        self.references = EditorInfo.getReferenceList(filePath)


    def getDict(self):
        return {"id":self.id, "host":self.host, "mtime":self.mtime, "references":self.references }


    def setDict(self, dictObject ):
        inputId   = EditorInfo.getValueFromDict( dictObject, 'id' )
        inputHost = EditorInfo.getValueFromDict( dictObject, 'host' )
        inputTime = EditorInfo.getValueFromDict( dictObject, 'mtime' )
        inputReferences = EditorInfo.getValueFromDict( dictObject, 'references' )
        
        if inputTime == self.mtime:
            self.id = inputId
            self.host = inputHost
            self.references = inputReferences
        else:
            self.id = ""
            self.hist = ""
    
    
    @staticmethod
    def getValueFromDict( dictObj, key ):
        if dictObj.has_key( key ):
            return dictObj[ key ]
        else:
            return ""
        
    
    @staticmethod
    def getEditorInfoPath( filePath ):
        if os.path.isdir( filePath ):
            dirPath = filePath
        else:
            dirPath = os.path.dirname( filePath )
        onlyDirname = dirPath.replace( '\\', '/' ).split( '/' )[-1]
        return dirPath + '/' + onlyDirname + '.' + ControlBase.editorInfoExtension
    
    
    @staticmethod
    def getMyInfo( filePath ):
        newInstance = EditorInfo(filePath)
        newInstance.id = EditorInfo.getMyId()
        newInstance.host = EditorInfo.getMyHost()
        newInstance.mtime = FileTime( filePath ).mtime()
        return newInstance


    @staticmethod
    def getReferenceList( filePath ):
        import pymel.core
        refNodes = pymel.core.ls( type='reference' )
        refList = []
        for refNode in refNodes:
            if pymel.core.referenceQuery( refNode, inr=1 ): continue
            try:refList.append(  pymel.core.referenceQuery( refNode, filename=1 ) )
            except:continue
        return refList


    @staticmethod
    def getMyId():
        return ""


    @staticmethod
    def getMyHost():
        
        import socket
        return socket.gethostname()
    
    
    def __eq__(self, other ):
        
        hostIsSame = self.id == other.id and self.host == other.host
        if not hostIsSame: return False
        return self.mtime == other.mtime
    
    
    def __le__(self, other ):
        
        return self.mtime <= other.mtime
    
    
    def __lt__(self, other ):
        
        return self.mtime < other.mtime


    def __ne__(self, other ):
        
        hostIsSame = self.id == other.id and self.host == other.host
        if not hostIsSame: return True
        return self.mtime != other.mtime
    
    
    def __gt__(self, other ):
        
        return self.mtime > other.mtime
    
    
    def __ge__(self, other ):
        
        return self.mtime >= other.mtime
    
        


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


