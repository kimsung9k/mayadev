import maya.cmds as cmds



def selectCtls( setNode ):
    
    ns = setNode.replace( 'SET', '' )
    ctls = cmds.ls( ns + 'Ctl_*', type='transform' )
    
    targetCtls = []
    for ctl in ctls:
        if not cmds.nodeType( ctl ) in ['joint', 'transform']: continue
        targetCtls.append( ctl )
    cmds.select( targetCtls )




def selectBakedCtls( setNode ):
    
    ns = setNode.replace( 'SET', '' )
    ctls = cmds.ls( ns + 'Ctl_*', type='transform' )
    
    targetCtls = []
    for ctl in ctls:
        if not cmds.nodeType( ctl ) in ['joint', 'transform']: continue
        cons = cmds.listConnections( ctl, s=1, d=0, p=1, c=1 )
        if not cons: continue
        targetCtls.append( ctl )
    cmds.select( targetCtls )




def bakeController( setNode ):
    
    ns = setNode.replace( 'SET', '' )
    
    ctls = cmds.ls( ns + 'Ctl_*', type='transform' )
    
    targetCtls = []
    ctlCons = []
    for ctl in ctls:
        if not cmds.nodeType( ctl ) in ['joint', 'transform']: continue
        cons = cmds.listConnections( ctl, s=1, d=0, p=1, c=1 )
        if not cons: continue
        ctlCons += cons
        targetCtls.append( ctl )
    
    cmds.select( targetCtls )
    
    minFrame = cmds.playbackOptions( q=1, min=1 )
    maxFrame = cmds.playbackOptions( q=1, max=1 )
    
    cmds.bakeResults( simulation=1, t=( minFrame, maxFrame ), sampleBy=1,
                       disableImplicitControl=True, preserveOutsideKeys=False, sparseAnimCurveBake=False,
                       removeBakedAttributeFromLayer=False, removeBakedAnimFromLayer=False, bakeOnOverrideLayer=False,
                       minimizeRotation=True, controlPoints=False, shape=False )
    
    for i in range( 0, len( ctlCons ), 2 ):
        srcCon = ctlCons[i+1]
        dstCon = ctlCons[i]
        
        if cmds.isConnected( srcCon, dstCon ):
            cmds.disconnectAttr( srcCon, dstCon )
    
    