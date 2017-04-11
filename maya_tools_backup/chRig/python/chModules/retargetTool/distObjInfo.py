leg_distObj  = ['Knee_*_Init', 'Ankle_*_Init']
arm_distObj  = ['Elbow_*_Init', 'Wrist_*_Init']
body_distObj = ['Waist_Init', 'Chest_Init']
head_distObj = ['NeckMiddle_Init', 'Head_Init']

distObjs = [ leg_distObj, arm_distObj, body_distObj, head_distObj ]

legTargets = ['Leg_*_IK_CTL','Leg_*_PoleV_CTL','Leg_*_FK0_CTL','Leg_*_FK1_CTL','Leg_*_FK2_CTL','Leg_*_FK3_CTL','Leg_*_IK_Pin_CTL', 'Leg_*_IkItp_CTL', 
              'Root_CTL', 'Fly_CTL', 'Move_CTL', 'Leg_*_UpperFlex_CTL', 'Leg_*_LowerFlex_CTL', 'Leg_*_PoleV_CTL' , 'Leg_*_Switch_CTL' ]
armTargets = ['Arm_*_IK_CTL','Arm_*_PoleV_CTL','Arm_*_FK0_CTL','Arm_*_FK1_CTL','Arm_*_FK2_CTL', 'Arm_*_IK_Pin_CTL', 'Arm_*_IkItp_CTL',
              'Arm_*_UpperFlex_CTL', 'Arm_*_LowerFlex_CTL', 'Arm_*_PoleV_CTL', 'Arm_*_Switch_CTL', 'Collar_*_CTL' ]
bodyTargets = [ 'Chest_CTL', 'ChestMove_CTL', 'Hip_CTL', 'TorsoRotate_CTL', 'Waist_CTL', 'Root_CTL', 'Neck_CTL' ]
headTargets = [ 'NeckMiddle_CTL', 'Head_CTL', 'Eye_CTL', 'EyeAim_*_CTL' ]

centerLegs = ['Root_CTL', 'Fly_CTL', 'Move_CTL']

targets = [ legTargets, armTargets, bodyTargets, headTargets ]


def getDistObjByName( origName ):
    
    side = ''
    
    if origName.find( '_L_' ) != -1:
        allSideName = origName.replace( '_L_', '_*_' )
        side = 'L'
    elif origName.find( '_R_' ) != -1:
        allSideName = origName.replace( '_R_', '_*_' )
        side = 'R'
    else:
        allSideName = origName
    
    for target in targets:
            index = targets.index( target )
            
            if allSideName in target:
                distTarget = distObjs[index]
                
                part = ['leg', 'arm', 'body', 'head'][index]
                
                if allSideName in centerLegs:
                    return distTarget[0].replace( '*', 'R' ), distTarget[1].replace( '*', 'R' ), part
                
                if side:
                    part = part +'_%s' % side
                
                return distTarget[0].replace( '*', side ), distTarget[1].replace( '*', side ), part