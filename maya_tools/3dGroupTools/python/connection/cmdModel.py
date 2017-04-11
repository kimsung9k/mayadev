import connectionUI.view
import maya.cmds as cmds


def uiCmd_OpenConnectionUI( *args ):
    
    connectionUI.view.Window().create()
    
    
    

def uiCmd_blendTwoMatrixConnectWorld( *args ):
    
    sels = cmds.ls( sl=1 )
    
    first = sels[0]
    second = sels[1]
    
    others = sels[2:]
    
    for other in others:
        
        if not cmds.attributeQuery( 'blendRate', node=other, ex=1 ):
            cmds.addAttr( other, ln='blendRate', min=0, max=1, dv=0.5 )
            cmds.setAttr( other+'.blendRate', e=1, k=1 )
        
        blendNode = cmds.createNode( 'blendTwoMatrix' )
        dcmp      = cmds.createNode( 'multMatrixDecompose' )
        
        cmds.connectAttr( first+'.wm', blendNode+'.inMatrix1' )
        cmds.connectAttr( second+'.wm', blendNode+'.inMatrix2' )
        cmds.connectAttr( blendNode+'.outMatrix', dcmp+'.i[0]' )
        cmds.connectAttr( other+'.pim', dcmp+'.i[1]' )
        
        cmds.connectAttr( dcmp+'.or', other+'.r' )
        cmds.connectAttr( other+'.blendRate', blendNode+'.attributeBlender' )