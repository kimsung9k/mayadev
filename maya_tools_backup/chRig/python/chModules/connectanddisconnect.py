import maya.cmds as cmds


def disconnectInit( Root_InitJnt ):
    def doit( obj ):
        tcons = cmds.listConnections( obj+'.t', d=1, s=0, c=1, p=1 )
        rcons = cmds.listConnections( obj+'.r', d=1, s=0, c=1, p=1 )
        
        if tcons:
            cmds.disconnectAttr( tcons[0], tcons[1] )
        if rcons:
            cmds.disconnectAttr( rcons[0], rcons[1] )
            
        children = cmds.listRelatives( obj, c=1 )
        if children:
            for child in children:
                doit( child )
                
    doit( Root_InitJnt )


def connectInit( Root_InitJnt ):
    def doit( initJnt ):
        init = initJnt.replace( 'InitJnt', 'Init' )
        
        if not cmds.listConnections( init, s=1, d=0 ):
            cmds.connectAttr( initJnt+'.t', init+'.t' )
            cmds.connectAttr( initJnt+'.r', init+'.r' )
            
        children = cmds.listRelatives( initJnt, c=1 )
        if children:
            for child in children:
                doit( child )
                
    doit( Root_InitJnt )