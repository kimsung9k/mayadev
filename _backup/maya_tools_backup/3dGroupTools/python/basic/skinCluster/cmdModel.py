import maya.cmds as cmds
import maya.OpenMaya as om

import basic.baseFunctions as baseFunctions


def mmSetBindPre( *args ):
    
    sels = cmds.ls( sl=1 )
    
    for sel in sels:
        cons = cmds.listConnections( sel+'.wm', d=1, s=0, p=1, c=1, type='skinCluster' )
        selP = cmds.listRelatives( sel, p=1 )[0]
        
        inputCons = cons[1::2]
        
        for inputCon in inputCons:
            bindPreAttr = inputCon.replace( 'matrix[', 'bindPreMatrix[' )
            cmds.connectAttr( selP+'.wim', bindPreAttr )
            
            


def mmSetBindDefault( *args ):
    
    sels = cmds.ls( sl=1 )
    
    for sel in sels:
        hists = cmds.listHistory( sel )
        
        skinNode = None
        for hist in hists:
            if cmds.nodeType( hist ) == 'skinCluster':
                skinNode = hist
                break
        
        fnSkinNode = om.MFnDependencyNode( baseFunctions.getMObject( skinNode ) )
        
        plugMatrix = fnSkinNode.findPlug( 'matrix' )
        plugBindPre = fnSkinNode.findPlug( 'bindPreMatrix' )
        
        for i in range( plugMatrix.numElements() ):
            loIndex = plugMatrix[i].logicalIndex()
            oMtx = plugMatrix[i].asMObject()
            mtxData = om.MFnMatrixData( oMtx )
            mtx = mtxData.matrix()
            invData = om.MFnMatrixData()
            oInv = invData.create( mtx.inverse() )
            plugBindPre.elementByLogicalIndex( loIndex ).setMObject( oInv )




mmShowSkinWeightEditUI = """import basic.skinCluster.ui.view
inst = basic.skinCluster.ui.view.ShowSkinWeightEditUIControl()
inst.setCmd()
inst.showUI()
"""