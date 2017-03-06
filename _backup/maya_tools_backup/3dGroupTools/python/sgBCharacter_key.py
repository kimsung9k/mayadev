import maya.cmds as cmds


def convertKey_LocalToWorld( worldCtl, minFrame=None, maxFrame=None ):
    
    import sgBFunction_scene
    
    if worldCtl[-9:] != 'World_CTL': 
        cmds.warning( "Select World_CTL")
        return None

    if not minFrame:
        minFrame = int( cmds.playbackOptions( q=1, min=1 ) )
    if not maxFrame:
        maxFrame = int( cmds.playbackOptions( q=1, max=1 ) )

    targetCtls = [ 'Fly_CTL', 'Root_CTL',
                   'Leg_L_FK0_CTL', 'Leg_R_FK0_CTL',
                   'Leg_L_IK_CTL', 'Leg_R_IK_CTL',
                   'Leg_L_PoleV_CTL', 'Leg_R_PoleV_CTL',
                   'Arm_L_FK0_CTL', 'Arm_R_FK0_CTL', 
                   'Arm_L_PoleV_CTL', 'Arm_R_PoleV_CTL',
                   'Arm_L_IK_CTL', 'Arm_R_IK_CTL',
                   'Head_CTL']
    
    ns = worldCtl.replace( 'World_CTL', '' )
    
    worldPositions = []
    
    sgBFunction_scene.hideTopTransforms()
    cmds.showHidden( worldCtl, a=1 )
    
    cmds.undoInfo( swf=0 )
    for i in range( minFrame, maxFrame + 1 ):

        cmds.currentTime( i )
        
        worldTranslates = []
        worldRotates = []
        for j in range( len( targetCtls ) ):
            targetCtl = ns+targetCtls[j]
            
            trans = cmds.xform( targetCtl, q=1, ws=1, t=1 )
            rot  = cmds.xform( targetCtl, q=1, ws=1, ro=1 )
            worldTranslates.append( trans )
            worldRotates.append( rot )
        
        worldPositions.append( [worldTranslates, worldRotates] )
    cmds.undoInfo( swf=1 )
    
    autoKeyframe = cmds.autoKeyframe( q=1, state=1 )
    cmds.autoKeyframe( state=1 )
    for i in range( minFrame, maxFrame + 1 ):
        
        cmds.currentTime( i )
        
        worldTranslates, worldRotates = worldPositions[i-minFrame]
        
        cmds.setAttr( worldCtl+'.t', 0,0,0 )
        cmds.setAttr( worldCtl+'.r', 0,0,0 )
        
        for j in range( len( targetCtls ) ):
            targetCtl = ns + targetCtls[j]
            
            attrs = cmds.listAttr( targetCtl, k=1 )
            
            translateOn = False
            rotateOn = False
            
            for attr in attrs:
                if attr == 'translateX':
                    translateOn = True
                elif attr == 'rotateX':
                    rotateOn = True
            
            if translateOn:
                wt = worldTranslates[j]
                cmds.move( wt[0], wt[1], wt[2], targetCtl, ws=1 )
            if rotateOn:
                wr = worldRotates[j]
                cmds.rotate( wr[0], wr[1], wr[2], targetCtl, ws=1 )
    cmds.autoKeyframe( state= autoKeyframe )
    sgBFunction_scene.showTopTransforms()

    