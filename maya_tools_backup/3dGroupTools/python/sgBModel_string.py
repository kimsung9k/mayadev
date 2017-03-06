


class StringLines:
    
    def __init__(self):
        
        self.commandString = ''
    
    
    def addLine( self, string ):
        self.commandString += string + "\n"
    
    
    def getString(self):
        return self.commandString