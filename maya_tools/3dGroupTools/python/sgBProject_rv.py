import maya.cmds as cmds


def connectOriginalMOC_to_chMOC( source, target ):
    
    sourceNS = source.replace( 'Solving', '' )
    targetNS = target.replace( 'All_Moc', '' )
    
    l_collar = ['LeftShoulder','Collar_L_MOC', [90,0,0] ]
    l_shd = ['LeftArm','Shoulder_L_MOC', [90,0,0]]
    l_elbow = ['LeftForeArm','Elbow_L_MOC', [90,0,0]]
    l_hand = ['LeftHand','Wrist_L_MOC', [90,0,0]]
    
    l_hip =['LeftUpLeg','Hip_L_MOC', [90,0,0]]
    l_knee =  ['LeftLeg','Knee_L_MOC', [90,0,0]]
    l_foot = ['LeftFoot','Ankle_L_MOC', [90,0,70]]
    
    r_collar = ['RightShoulder','Collar_R_MOC', [90,0,180] ]
    r_shd = ['RightArm','Shoulder_R_MOC', [90,0,180]]
    r_elbow = ['RightForeArm','Elbow_R_MOC', [90,0,180]]
    r_hand = ['RightHand','Wrist_R_MOC', [90,0,180]]
    
    r_hip =['RightUpLeg','Hip_R_MOC', [90,0,180]]
    r_knee =  ['RightLeg','Knee_R_MOC', [90,0,180]]
    r_foot = ['RightFoot','Ankle_R_MOC', [90,0,-110]]
    
    root   = ['Hips', 'Root_MOC', [100,0,0]]
    Spine0 = ['Spine','Root_MOCSep', [110,0,0] ]
    Spine1 = ['Spine1', 'Waist_MOC', [90,0,0] ]
    Spine2 = ['Spine2', 'Chest_MOCSep', [90,0,0] ]
    Spine3 = ['Spine3', 'Chest_MOC', [90,0,0] ]
    
    neck   = ['Neck', 'Neck_MOC', [100,0,0] ]
    head   = ['Head', 'Head_MOC', [110,0,0] ]
    
    parts = [ l_collar, l_shd, l_elbow, l_hand, l_hip, l_knee, l_foot, 
              r_collar, r_shd, r_elbow, r_hand, r_hip, r_knee, r_foot,
              root, Spine0, Spine1, Spine2, Spine3, neck, head ]
    
    for srcPart, trgPart, rotate in parts:
        
        sourceJnt = sourceNS + srcPart
        targetJnt = targetNS + trgPart
        
        cmds.select( sourceJnt )
        connectionJnt = cmds.joint( n=targetNS + trgPart + '_connect' )
        cmds.setAttr( connectionJnt+'.r', *rotate )
        
        cmds.orientConstraint( connectionJnt, targetJnt )
        
    cmds.pointConstraint( targetNS + root[1] + '_connect', targetNS + root[1] )