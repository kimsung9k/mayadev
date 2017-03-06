import maya.cmds as cmds



def copyKeyframe( sourceAnimCurve, targetAnimCurve ):
    
    srcCons = cmds.listConnections( targetAnimCurve, s=1, d=0, p=1, c=1 )
    dstCons = cmds.listConnections( targetAnimCurve, s=0, d=1, p=1, c=1 )
    
    if srcCons:
        cmds.disconnectAttr( srcCons[1], srcCons[0] )
    if dstCons:
        cmds.disconnectAttr( dstCons[0], dstCons[1] )
    
    duAnimCurve = cmds.duplicate( sourceAnimCurve )
    cmds.delete( targetAnimCurve )
    
    duAnimCurve = cmds.rename( duAnimCurve, targetAnimCurve )
    if srcCons:
        cmds.connectAttr( srcCons[1], duAnimCurve+'.input' )
    if dstCons:
        cmds.connectAttr( duAnimCurve+'.output', dstCons[1] )



def mirrorCopyConvertedChannel( first, second, attrs = None ):
    
    import sgBFunction_connection
    
    if not attrs:
        attrs = cmds.listAttr( first, k=1 )
    
    for attr in attrs:
        sgBFunction_connection.separateParentConnection( second, attr )
        animCurves = cmds.listConnections( first+'.'+attr, s=1, d=0, type='animCurve' )
        multNodes  = cmds.listConnections( first+'.'+attr, s=1, d=0, type='multDoubleLinear' )
        
        if animCurves:
            sourceCons = cmds.listConnections( second+'.'+attr, s=1, d=0, p=1 )
            print sourceCons
            if sourceCons:
                sourceCon = sourceCons[0]
                if cmds.nodeType( sourceCon.split( '.' )[0] )[:-2] == 'animCurve':
                    copyKeyframe( animCurves[0], sourceCon.split( '.' )[0] )
                    continue
                elif cmds.nodeType( sourceCon.split( '.' )[0] ) == 'unitConversion':
                    sourceCon = cmds.listConnections( sourceCon.split( '.' )[0]+'.input', s=1, p=1 )[0]
                    continue
                otherAnimCurve = cmds.duplicate( animCurves[0] )[0]
                cmds.connectAttr( sourceCon, otherAnimCurve+'.input' )
            cmds.connectAttr( otherAnimCurve+'.output', second+'.'+attr, f=1 )