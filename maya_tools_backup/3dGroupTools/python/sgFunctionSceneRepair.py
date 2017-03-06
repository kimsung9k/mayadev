import maya.cmds as cmds


def noNamespaceAssetConnectionToNamespaceAsset( first, second ):
    
    firstChildren = cmds.listRelatives( first, c=1, ad=1, type='transform', f=1 )
    
    secondNamespace = second.replace( 'SET', '' )
    
    for fChild in firstChildren:
        
        childName = fChild.split( '|' )[-1]
        if childName[:4] != 'Ctl_': continue
        
        if not cmds.nodeType( fChild ) in ['joint', 'transform']: continue
        
        sChild = secondNamespace + childName
        
        tValue = cmds.getAttr( fChild+'.t' )[0]
        rValue = cmds.getAttr( fChild+'.r' )[0]
        sValue = cmds.getAttr( fChild+'.s' )[0]
        try:cmds.setAttr( sChild+'.tx', tValue[0] )
        except:pass
        try:cmds.setAttr( sChild+'.ty', tValue[1] )
        except:pass
        try:cmds.setAttr( sChild+'.tz', tValue[2] )
        except:pass
        try:cmds.setAttr( sChild+'.rx', rValue[0] )
        except:pass
        try:cmds.setAttr( sChild+'.ry', rValue[1] )
        except:pass
        try:cmds.setAttr( sChild+'.rz', rValue[2] )
        except:pass
        try:cmds.setAttr( sChild+'.sx', sValue[0] )
        except:pass
        try:cmds.setAttr( sChild+'.sy', sValue[1] )
        except:pass
        try:cmds.setAttr( sChild+'.sz', sValue[2] )
        except:pass
        
        animCurves = cmds.listConnections( fChild, s=1, d=0, type='animCurve', p=1, c=1 )
        
        if not animCurves: continue
        
        for i in range( 0, len( animCurves ), 2 ):
            if cmds.referenceQuery( animCurves[i+1], inr=1 ):
                continue
            inputTarget = secondNamespace + animCurves[i].split( '|' )[-1] 
            try:cmds.connectAttr( animCurves[i+1], inputTarget )
            except: pass