import maya.cmds as cmds


def convertLocalKeyToWorldKey_basedOnWorld( worldCtl ):
    
    import sgBFunction_dag
    import sgBModel_data
    
    if worldCtl[-9:] != 'World_CTL': 
        cmds.warning( "Select World_CTL")
        return None
    
    targetCtls = [ 'Fly_CTL', 'Root_CTL',
                   'Leg_L_FK0_CTL', 'Leg_R_FK0_CTL',
                   'Leg_L_PoleV_CTL', 'Leg_R_PoleV_CTL',
                   'Leg_L_IK_CTL', 'Leg_R_IK_CTL',
                   'Arm_L_IK_CTL', 'Arm_R_IK_CTL', 
                   'Arm_L_PoleV_CTL', 'Arm_R_PoleV_CTL',
                   'Arm_L_FK0_CTL', 'Arm_R_FK0_CTL']
    
    ns = worldCtl.replace( 'World_CTL', '' )
    
    worldTranslates = []
    worldRotates = []
    for targetCtl in targetCtls:
        trans = cmds.xform( targetCtl, q=1, ws=1, t=1 )
        rot  = cmds.xform( targetCtl, q=1, ws=1, ro=1 )
        worldTranslates.append( trans )
        worldRotates.append( rot )

    cmds.setAttr( worldCtl+'.t', 0,0,0 )
    cmds.setAttr( worldCtl+'.r', 0,0,0 )
    
    for i in range( len( targetCtls ) ):
        targetCtl = targetCtls[i]
        
        attrs = cmds.listAttr( targetCtl, k=1 )
        
        translateOn = False
        rotateOn = False
        
        for attr in attrs:
            if attr == 'translateX':
                translateOn = True
            elif attr == 'rotateX':
                rotateOn = True
        
        if translateOn:
            wt = worldTranslates[i]
            cmds.move( wt[0], wt[1], wt[2], targetCtl, ws=1 )
        if rotateOn:
            wr = worldRotates[i]
            cmds.rotate( wr[0], wr[1], wr[2], targetCtl, ws=1 )