import maya.cmds as cmds

def getTopJointChildren( topNodes ):

    if not topNodes: return []

    returnList = []
    for topNode in topNodes:
        if cmds.nodeType( topNode ) == 'joint':
            returnList.append( topNode )
            continue
        returnList += getTopJointChildren( cmds.listRelatives( topNode, c=1, f=1 ) )
    return returnList

cmds.select( getTopJointChildren( cmds.ls( sl=1 ) ) )