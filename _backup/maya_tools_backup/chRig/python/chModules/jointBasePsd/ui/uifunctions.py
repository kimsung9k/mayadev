import maya.cmds as cmds

def setWidthByPerList( perList, width ):
    
    allValue = 0
    
    for per in perList:
        allValue += per
        
    for i in range( len( perList ) ):
        perList[i] /= float( allValue )
    
    addedWidth = 0
    
    returnList = []
    for i in range( len( perList )-1 ):
        addedWidth += perList[i] * width
        
        returnList.append( perList[i]*width )
        
    returnList.append( width - addedWidth )
    
    return returnList


def setSpace( h=1 ):
    cmds.text( l='', h=h )