import maya.cmds as cmds



def uiCmd_connectMatrixToJointOrient( *args ):
    
    selections = cmds.ls( sl=1, transforms=1 )
    
    firsts = selections[::2]
    seconds = selections[1::2]
    
    for i in range( len( firsts ) ):
        decomposeMatrix = cmds.createNode( 'decomposeMatrix', n=seconds[i]+'_localConnect' )
        cmds.connectAttr( firsts[i]+'.m', decomposeMatrix+'.inputMatrix' )
        cmds.connectAttr( decomposeMatrix+'.or', seconds[i]+'.jointOrient' )
        
        


def uiCmd_openCreateMiddleJoint_ui( *args ):
    
    import addMiddleJoint.view
    
    addMiddleJoint.view.Window().create()