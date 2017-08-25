import datetime


class Task:
    
    def __init__(self, projectPath, localPath, taskPath ):
        
        self.projectPath = projectPath
        self.localPath   = localPath
        self.taskPath = taskPath



class Unit( Task ):
    
    def __init__(self, instTask, unitPath ):
        
        Task.__init__( self, instTask.projectPath, instTask.localPath, instTask.taskPath )
        self.unitPath = unitPath