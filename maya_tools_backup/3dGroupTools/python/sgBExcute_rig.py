import sgBFunction_attribute
import maya.cmds as cmds


def translateBlend_toAimTarget( target, aimTarget ):
    
    targetP = cmds.listRelatives( target, p=1, f=1 )[0]
    
    
    blendNode = cmds.createNode( 'blendTwoAttr' )
    mmdc      = cmds.createNode( 'multMatrixDecompose' )
    cmds.connectAttr( aimTarget+'.wm', mmdc+'.i[0]' )
    cmds.connectAttr( targetP+'.pim',  mmdc+'.i[1]' )
    
    sgBFunction_attribute.addAttr( target, ln='origTx', k=1, dv= cmds.getAttr( mmdc+'.otx' ) )
    sgBFunction_attribute.addAttr( targetP, ln='blend', min=0, max=1, dv=0.5, k=1 )
    
    cmds.connectAttr( target+'.origTx', blendNode+'.input[0]' )
    cmds.connectAttr( mmdc+'.otx', blendNode+'.input[1]' )
    cmds.connectAttr( targetP+'.blend', blendNode+'.attributesBlender' )
 
    cmds.connectAttr( blendNode+'.output', target+'.tx' )




def copySkinWeightFromSelection():
    
    import sgBFunction_dag
    import sgBFunction_skinCluster
    
    sels = cmds.ls( sl=1 )
    
    source = ''
    target = ''
    for sel in sels:
        skinNodes = sgBFunction_dag.getNodeFromHistory( sel, 'skinCluster' )
        if skinNodes: source = sel
        else: target = sel
    
    if not source or not target: return None
    sgBFunction_skinCluster.autoCopyWeight( source, target )
    
    return source, target



def meshSnap( base, others ):
    
    import sgBFunction_base
    sgBFunction_base.autoLoadPlugin( 'meshSnap' )
    for sel in others:
        
        cmds.select( base, sel )
        cmds.meshSnap()




def pointOnCurveInfoDistanceReconnect( targetCurve, worldCtl ):
    
    infos = cmds.listConnections( targetCurve, d=1, s=0, type='pointOnCurveInfo' )
    
    trGeo = cmds.createNode( 'transformGeometry' )
    cmds.connectAttr( targetCurve+'.local', trGeo+'.inputGeometry' )
    cmds.connectAttr( worldCtl+'.wim', trGeo+'.transform' )
    
    for info in infos:
        if cmds.isConnected( trGeo+'.outputGeometry', info+'.inputCurve' ): continue
        cmds.connectAttr( trGeo+'.outputGeometry', info+'.inputCurve', f=1 )



def displayModConnect( displayMods ):
    
    import sgBFunction_dag
    import sgBFunction_convert
    import sgBFunction_connection
    
    displayMods = sgBFunction_convert.singleToList( displayMods )
    
    for displayMod in displayMods:
        origMod = displayMod.replace( 'display_', '' )
        
        sgBFunction_connection.constraintAll( origMod, displayMod )
        
        displayModShape = sgBFunction_dag.getShape( displayMod )
        origModShape = sgBFunction_dag.getShape( origMod )
        cmds.connectAttr( origModShape+'.outMesh', displayModShape+'.inMesh' )



def makeDisplayMod( origMods ):
    
    import sgBFunction_convert
    origMods = sgBFunction_convert.singleToList( origMods )
    
    displayMods = []
    for origMod in origMods:
        displayMod = cmds.duplicate( origMod, n='display_'+origMod )[0]
        displayMods.append( displayMod )
    
    cmds.select( displayMods )
    return displayMods



