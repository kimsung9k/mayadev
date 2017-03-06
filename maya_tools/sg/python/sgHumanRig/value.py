import maya.OpenMaya as OpenMaya


def maxValue( valueList ):
    
    maxValue = -1000000000
    for value in valueList:
        if value > maxValue:
            maxValue = value
    
    return maxValue



def minValue( valueList ):
    
    minValue = 1000000000
    for value in valueList:
        if value < minValue:
            minValue = value
    
    return minValue



def maxSize( valueList ):
    
    import math
    maxValue = 0
    for value in valueList:
        absValue = math.fabs( value )
        if absValue > maxValue:
            maxValue = absValue
    
    return maxValue



def minSize( valueList ):
    
    import math
    minValue = 10000000000
    for value in valueList:
        absValue = math.fabs( value )
        if absValue < minValue:
            minValue = absValue
    
    return minValue



def maxDotIndexAndValue( direction, rotMatrix ):
    
    import math
    maxDotValue = 0
    maxDotIndex = 0
    
    for i in range( 3 ):
        vector = OpenMaya.MVector( rotMatrix[i] ).normal()
        dotValue = direction * vector
        
        if math.fabs( dotValue ) > math.fabs( maxDotValue ):
            maxDotValue = dotValue
            maxDotIndex = i
    
    return maxDotValue, maxDotIndex



def getValueFromDict( argDict, *dictKeys ):
    
    items = argDict.items()
    
    for item in items:
        if item[0] in dictKeys: return item[1]
    
    return None


