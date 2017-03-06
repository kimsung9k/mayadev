import maya.cmds as cmds
import maya.OpenMaya as om
import functions as fnc


def cutCurve( surfShape, constStart, constEnd, applyUV ):
        
    volumeCrvNodeCons = cmds.listConnections( surfShape+'.local', type='volumeCurvesOnSurface' )
    
    if volumeCrvNodeCons:
        
        for volumeCrvNode in volumeCrvNodeCons:
            
            if applyUV:
                cmds.setAttr( volumeCrvNode+'.byUv', 1 )
            else:
                cmds.setAttr( volumeCrvNode+'.byUv', 0 )
            
            cmds.setAttr( volumeCrvNode+'.cutAble', 1 )
            cmds.setAttr( volumeCrvNode+'.refresh', 1 )
            cmds.setAttr( volumeCrvNode+'.constStart', constStart )
            cmds.setAttr( volumeCrvNode+'.constEnd', constEnd )