import maya.cmds as cmds
import chModules.retargetTool.functions as fnc

def clearLocalData( target ):
    
    orientNodeCons = cmds.listConnections( target, type='retargetOrientNode' )
    transNodeCons = cmds.listConnections( target, type='retargetTransNode' )
    
    retargetNodes = []
    
    if orientNodeCons:
        retargetNodes.append( orientNodeCons[0] )
    if transNodeCons:
        retargetNodes.append( transNodeCons[0] )
        
    if retargetNodes:
        
        for retargetNode in retargetNodes:
            fnc.clearArrayElement( retargetNode+'.localData' )