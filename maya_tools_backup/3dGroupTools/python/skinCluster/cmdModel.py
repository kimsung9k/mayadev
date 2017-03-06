import maya.cmds as cmds


def uiCmd_connectBindPreMatrix( *args ):
    
    selections = cmds.ls( sl=1 )
    
    firsts = selections[:-1][::2]
    seconds = selections[:-1][1::2]
    last = selections[-1]
    
    for i in range( len( firsts ) ):
        
        first = firsts[i]
        second = seconds[i]
        
        cons = cmds.listConnections( first, type='skinCluster', d=1, s=0, c=1, p=1 )
        
        outputs = cons[0::2]
        inputs  = cons[1::2]
        
        for ii in range( len( outputs ) ):
            
            if inputs[ii].find( 'matrix' ) == -1: continue
            
            outputAttr = outputs[ii].replace( first, second ).replace( 'worldMatrix', 'worldInverseMatrix' )
            inputAttr = inputs[ii].replace( 'matrix', 'bindPreMatrix' )
            
            if inputAttr.find( last ) == -1: continue
            
            if not cmds.isConnected( outputAttr, inputAttr ):
                cmds.connectAttr( outputAttr, inputAttr, f=1 )
                


mc_replaceObjectSkined = """import maya.cmds as cmds
import sgRigSkinCluster
sels = cmds.ls( sl=1 )
sgRigSkinCluster.replaceObjectSkined(sels[0], sels[1])"""