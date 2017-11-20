import maya.cmds as cmds


def getMessageConnection( target, attrName ):
    
    if not cmds.attributeQuery( target, attrName ):
        pass