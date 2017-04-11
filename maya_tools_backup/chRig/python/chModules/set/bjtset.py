import maya.cmds as cmds
import chModules.rigbase as rigbase

def lockAttrs( node, *attrs ):
    for attr in attrs:
        cmds.setAttr( node+'.'+attr, e=1, lock=1 )
            
def unlockAttrs( node, *attrs ):
    for attr in attrs:
        cmds.setAttr( node+'.'+attr, e=1, lock=0 )

def createBjt( topRjt ):
    topBjt = rigbase.hierarchyCopyConnections( topRjt, typ='joint', replaceTarget='_RJT', replace='_BJT', t=0, r=0 )
    
    bjts = cmds.listRelatives( topBjt, c=1, ad=1 )
    bjts.append( topBjt )
    
    for bjt in bjts:
        rjt = bjt.replace( '_BJT', '_RJT' )
        #cmds.setAttr( bjt+'.r', 0,0,0 )
        #cmds.setAttr( bjt+'.jox', e=1, k=1 )
        #cmds.setAttr( bjt+'.joy', e=1, k=1 )
        #cmds.setAttr( bjt+'.joz', e=1, k=1 )
        #cmds.connectAttr( rjt+'.rx', bjt+'.rx' )
        #cmds.connectAttr( rjt+'.ry', bjt+'.ry' )
        #cmds.connectAttr( rjt+'.rz', bjt+'.rz' )
        
        conSameAttr = rigbase.connectSameAttr( rjt, bjt )
        conSameAttr.doIt( 't', 'r', 's' )
        
        if rjt.find( 'Leg_L_Lower4' ) != -1 or rjt.find( 'Leg_R_Lower4' ) != -1:
            conSameAttr.doIt( 'sh' )
        
        cmds.setAttr( bjt+'.ssc', cmds.getAttr( rjt+'.ssc' ) )
        
        if cmds.attributeQuery( 'parameter', node=rjt, ex=1 ):
            rigbase.AttrEdit( bjt ).addAttr( ln='parameter', min=-.001, max=1.001, dv=cmds.getAttr( rjt+'.parameter' ), cb=1 )
            cmds.connectAttr( bjt+'.parameter', rjt+'.parameter' )
            
        bjtP = cmds.listRelatives( bjt, p=1 )
        
        if not bjtP: continue
    
        try:
            cmds.connectAttr( bjtP[0]+'.scale', bjt+'.inverseScale' )
        except: pass
    
    topRjtGrp = cmds.listRelatives( topRjt, p=1 )[0]
    topBjtGrp = cmds.group( em=1, n='Root_BJT_GRP' )
    
    rigbase.transformSetColor( topRjtGrp, 11 )
    rigbase.transformSetColor( topBjtGrp, 29 )
    
    bjtWorld   = cmds.group( n='BJT_World' )
    rigbase.addControlerShape( bjtWorld, typ='circle', normal=[0,1,0], radius=5.5 )
    rigbase.controlerSetColor( bjtWorld, 29 )
    bjtWorldGrp   = cmds.group( bjtWorld, n='BJT_World_GRP' )
    cmds.connectAttr( topRjtGrp+'.t', topBjtGrp+'.t' )
    cmds.connectAttr( topRjtGrp+'.r', topBjtGrp+'.r' )
    cmds.parent( topBjt, topBjtGrp  )
    
    rigbase.connectSameAttr( 'World_CTL_GRP', 'BJT_World_GRP' ).doIt( 't', 'r', 's' )
    rigbase.connectSameAttr( 'World_CTL', 'BJT_World' ).doIt( 't', 'r', 's' )
    #rigbase.AttrEdit( 'BJT_World' ).addAttr( ln='World_CTL', at='message' )
    #cmds.connectAttr( 'World_CTL.message', 'BJT_World.World_CTL' )
    
    RIG = cmds.group( em=1, n='RIG' )
    cmds.parent( 'World_CTL_GRP', 'All_Init', RIG )
    SKIN = cmds.group( em=1, n='SKIN' )
    cmds.parent( 'BJT_World_GRP', SKIN )
    
    cmds.setAttr( topRjt+'.v', 0 )

def flyFollowRepair():
    flyFps = cmds.ls( '*_FP_inFly', tr=1 )
    moveCtl = 'Move_CTL'
    rootInit = 'Root_Init'
    flyCtlGrp = 'Fly_CTL_GRP'
    rootMtxDcmp = 'Root_CTL_GRP__mtxDcmp'
    followMtx = 'Root_CTL_GRP_followMtx'
    rootCtlGrp = 'Root_CTL_GRP'
    
    fpsGrp = cmds.createNode( 'transform', n='Fps_inFly' )
    rootSample = cmds.createNode( 'transform', n='Root_Sample_Null' )
    
    cmds.parent( rootSample, fpsGrp, moveCtl )
    
    cmds.setAttr( rootSample+'.t', 0,0,0 )
    cmds.setAttr( rootSample+'.r', 0,0,0 )
    cmds.setAttr( rootSample+'.s', 1,1,1 )
    
    cmds.connectAttr( rootMtxDcmp+'.ot', fpsGrp+'.t' )
    cmds.connectAttr( rootMtxDcmp+'.or', fpsGrp+'.r' )
    
    cmds.parent( flyFps, fpsGrp )
    
    cmds.connectAttr( rootInit+'.t', rootSample+'.t' )
    cmds.connectAttr( rootInit+'.r', rootSample+'.r' )
    cmds.disconnectAttr( rootInit+'.r', flyCtlGrp+'.r' )
    cmds.setAttr( flyCtlGrp+'.r', 0,0,0 )
    
    cmds.connectAttr( rootSample+'.wm', rootMtxDcmp+'.i[0]', f=1 )
    cmds.connectAttr( flyCtlGrp+'.wim', rootMtxDcmp+'.i[1]', f=1 )
    cmds.connectAttr( followMtx+'.outputMatrix', rootMtxDcmp+'.i[2]' )
    cmds.connectAttr( rootCtlGrp+'.pim', rootMtxDcmp+'.i[3]' )
    
    ctlGrps = cmds.ls( '*CTL_GRP' )
    
    for grp in ctlGrps:
        rigbase.lockAttrs( grp, 't', 'r', 's' )

def markingMenuSet( rigInstance ):
    ctls = cmds.ls( '*_CTL' )
    
    rObj = cmds.createNode( 'multDoubleLinear', n='RightClickObj_Rigs' )
    attrEdit = rigbase.AttrEdit( rObj )
    attrEdit.addAttr( ln='originalName', dt='string' )
    cmds.setAttr( rObj+'.originalName', rObj, type='string' )
    
    attrEdit = rigbase.AttrEdit( rObj )
    
    for ctl in ctls:
        attrEdit.addAttr( ln=ctl, at='message' )
        cmds.connectAttr( ctl+'.message', rObj+'.'+ctl )
    rigbase.AttrEdit( 'World_CTL' ).addAttr( ln=rObj, at='message' )
    cmds.connectAttr( rObj+'.message', 'World_CTL.'+rObj )
    
    bjts = cmds.ls( '*_BJT' )
    bjts.append( 'BJT_World' )
    
    rObj = cmds.createNode( 'multDoubleLinear', n='RightClickObj_Bjts' )
    attrEdit = rigbase.AttrEdit( rObj )
    attrEdit.addAttr( ln='originalName', dt='string' )
    cmds.setAttr( rObj+'.originalName', rObj, type='string' )
    
    attrEdit = rigbase.AttrEdit( rObj )
    
    for bjt in bjts:
        attrEdit.addAttr( ln=bjt, at='message' )
        cmds.connectAttr( bjt+'.message', rObj+'.'+bjt )
    rigbase.AttrEdit( 'BJT_World' ).addAttr( ln=rObj, at='message' )
    cmds.connectAttr( rObj+'.message', 'BJT_World.'+rObj )