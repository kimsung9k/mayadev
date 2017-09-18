import os, datetime


class FileUnit:
    
    def __init__(self, projectPath, taskPath, unitPath ):
        
        self.projectPath = projectPath
        self.taskPath = taskPath
        self.unitPath = unitPath




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
        
        



