import pymel.core
import os, json
import maya.cmds as cmds
recentInfoPath = os.path.dirname( __file__ ) + '/recentExportPath.txt'


def exportShadingNetwork( targetNode, exportPath ):
    
    targetNode = pymel.core.ls( targetNode )[0]
    hists = targetNode.history()
    
    connectionList = []
    for hist in hists:
        if not hasattr( hist, 'worldMatrix' ): continue
        connections = hist.listConnections( s=0, d=1, p=1, c=1 )
        for origAttr, dstAttr in connections:
            origAttr // dstAttr
            connectionList.append( [origAttr, dstAttr] )
    
    cmds.file( exportPath, op='v=0', typ="mayaBinary" ,pr=1 ,es=1 )
    
    for srcAttr, dstAttr in connectionList:
        srcAttr >> dstAttr