import maya.cmds as cmds
import maya.OpenMaya as om



def getMatrixFromPlugMatrix( plugMatrix ):
    
    mObj = plugMatrix.asMObject()
    mtxData = om.MFnMatrixData()
    mtxData.create( mObj )
    return mtxData.matrix()



def getMPointFromMMatrix( mmtx ):
    
    return om.MPoint( mmtx(3,0), mmtx(3,1), mmtx(3,2) )



def getDefaultMatrix():
    
    return [ i%5 == 0 for i in range( 16 ) ]



def getValueFromDict( argDict, dictKey ):
    
    if not type( dictKey ) in [type( [] ), type( () )]:
        dictKey = [dictKey]
    
    items = argDict.items()
    
    for item in items:
        if item[0] in dictKey: return item[1]
    
    return None



def getArragnedList( inputList ):
    
    if not type( inputList ) in [ type([]), type(()) ]:
        inputList = [inputList]
    
    arrangedList = []
    for inputs in inputList:
        if type( inputs ) in [ type([]), type(()) ]:
            arrangedList += getArragnedList( inputs )
        else:
            arrangedList.append( inputs )
    
    return arrangedList


def getCurrentUnitFrameRate():
    
    timeUnitDict = { 'game':15, 'film':24, 'pal':25, 'ntsc':30, 'show':48, 'palf':50, 'ntscf':60 }
    currentTimeUnit = cmds.currentUnit( q=1, time=1 )
    
    return float( timeUnitDict[ currentTimeUnit ] )


def getStartAndEndFrameFromXmlFile( xmlFilePath ):
    
    import xml.etree.ElementTree as ET
    
    root = ET.parse( xmlFilePath ).getroot()
    timeRange= root.find( 'time' ).attrib['Range']
    perFrame = root.find( 'cacheTimePerFrame' ).attrib['TimePerFrame']
    
    startFrame = 1
    endFrame   = 1
    perFrame = int( perFrame )
    
    startFrameAssigned = False
    
    for str1 in timeRange.split( '-' ):
        if not startFrameAssigned:
            if str1 == '':
                startFrame *= -1
                continue
            else:
                startFrame *= int( str1 )
                startFrameAssigned = True
                continue
        
        if str1 == '':
            endFrame *= -1
        else:
            endFrame *= int( str1 )
            
    startFrame /= perFrame
    endFrame /= perFrame
    
    return startFrame, endFrame