import maya.cmds as cmds
import maya.OpenMaya as om



def getMObject( target ):
    
    selList = om.MSelectionList()
    selList.add( target )
    mObj = om.MObject()
    selList.getDependNode( 0, mObj )
    return mObj
    


def copyWeight( first, second ):
    
    hists = cmds.listHistory( first, pdo=1 )
    
    skinNode = None
    for hist in hists:
        
        if cmds.nodeType( hist ) == 'skinCluster':
            skinNode = hist
            
    if not skinNode: return None
    
    targetSkinNode = None
    targetHists = cmds.listHistory( second, pdo=1 )
    if targetHists:
        for hist in targetHists:
            if cmds.nodeType( hist ) == 'skinCluster':
                targetSkinNode = hist

    if not targetSkinNode:
        bindObjs = cmds.listConnections( skinNode+'.matrix', s=1, d=0, type='joint' )
        bindObjs.append( second )
        print bindObjs
        cmds.skinCluster( bindObjs )
    
    cmds.copySkinWeights( first, second, noMirror=True, surfaceAssociation='closestPoint', influenceAssociation ='oneToOne' )
    
    
    
def ucCopyWeight( *args ):
    
    sels = cmds.ls( sl=1 )
    
    firsts = sels[::2]
    seconds = sels[1::2]
    
    for i in range( len( firsts ) ):
        copyWeight( firsts[i], seconds[i] )