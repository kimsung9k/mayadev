import chModules.basecode as basecode
    
class BodyNameData( basecode.ItemBase ):
    def __init__(self, objectNameList ):
        self.objectNameList = objectNameList
        
    def getList(self, side='' ):
        returnList = []
        itemList = self.getItemList()
        
        for objectName in self.objectNameList:
            if objectName.find( side ) == -1:
                continue
            
            for itemName in itemList:
                if objectName.split('_')[0] == itemName:
                    returnList.append( objectName )
                    continue
        return returnList
    
    def getOneByName( self, name, side='' ):
        for objectName in self.objectNameList:
            if objectName.find( side ) == -1:
                continue
            if objectName.find( name ) != -1:
                return objectName
    
    def getSortList(self, side='' ):
        returnList = []
        itemList = self.getSortItemList()
        
        for itemName in itemList:
            for objectName in self.objectNameList:
                if objectName.find( side ) == -1:
                    continue
                if objectName.split('_')[0] == itemName:
                    returnList.append( objectName )
        return returnList

class FingerNameData( BodyNameData ):
    Thumb = 0
    Index = 1
    Middle = 2
    Ring = 3
    Pinky = 4

    def __init__(self, objectNameList ):
        BodyNameData.__init__(self, objectNameList )
    
    def getEachFingerList( self, index, side='' ):
        fingerList = []
        
        itemName = self.getItemName( index )
        for objectName in self.objectNameList:
            if objectName.find( side ) == -1:
                continue
            
            if objectName.find( itemName ) != -1:
                fingerList.append( objectName )
        
        return fingerList
    
class ArmNameData( BodyNameData ):
    Shoulder = 0
    Elbow = 1
    Wrist = 2
    ArmPoleV = 3
    
    def __init__(self, objectNameList ):
        BodyNameData.__init__(self, objectNameList)
        
class ArmAddNameData( BodyNameData ):
    UpperArm = 0
    LowerArm = 1
    
    def __init__(self, objectNameList ):
        BodyNameData.__init__(self, objectNameList)
        
class LegNameData( BodyNameData ):
    Hip = 0
    Knee = 1
    Ankle = 2
    LegPoleV = 3
    Ball = 4
    Toe = 5
    Heel = 6
    BallPiv = 7
    BankIn = 8
    BankOut = 9
    ToePiv = 10

    def __init__(self, objectNameList ):
        BodyNameData.__init__(self, objectNameList)
        
class LegAddNameData( BodyNameData ):
    UpperLeg = 0
    LowerLeg = 1
    
    def __init__(self, objectNameList ):
        BodyNameData.__init__(self, objectNameList)
        
class TorsoNameData( BodyNameData ):
    Root = 0
    WaistP = 1
    Waist = 2
    ChestP = 3
    Chest = 4
    Collar = 5
    
    def __init__(self, objectNameList ):
        BodyNameData.__init__(self, objectNameList)
        
class HeadNamdData( BodyNameData ):
    Neck = 0
    NeckMiddle = 1
    Head = 2
    Eye = 3
    EyeAimPiv = 4
    
    def __init__(self, objectNameList ):
        BodyNameData.__init__(self, objectNameList)