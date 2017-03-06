import os
from sgModules import sgcommands



class ARAM_Set:
    
    defaultIgnore = ['SimulationOnOff']
    reverseAttrs = ['footTilt', 'ballSwivel']
    
    leftPrefix  = ['ARAM_l','Left']
    rightPrefix = ['ARAM_r','Right']
    
    data = [
            ['LfMouthSide_Ctrl', 'ARAM_HeadC', '', 'none'],
            ['MouthDir_Ctrl', 'ARAM_HeadC', '', 'none'],
            ['RtMouthSide_Ctrl', 'ARAM_HeadC', '', 'none'],
            ['ARAM_Nose_Skin_Ctrl', 'ARAM_HeadC', '', 'none'],
            ['ARAM_Eye_Right_Df_Ctrl', 'ARAM_HeadC', '', 'none'],
            ['ARAM_Eye_Left_Df_Ctrl', 'ARAM_HeadC', '', 'none'],
            ['ARAM_Left_EyeBlend_Ctrl', 'ARAM_HeadC', '', 'none'],
            ['ARAM_Right_EyeBlend_Ctrl', 'ARAM_HeadC', '', 'none'],
            ['ARAM_RightEyeBrowAll_Skin_Ctrl', 'ARAM_HeadC', '', 'none'],
            ['ARAM_RightEyeBrow2_Skin_Ctrl', 'ARAM_HeadC', '', 'none'],
            ['ARAM_RightEyeBrow1_Skin_Ctrl', 'ARAM_HeadC', '', 'none'],
            ['ARAM_RightEyeBrow_Skin_Ctrl', 'ARAM_HeadC', '', 'none'],
            ['ARAM_LeftEyeBrow_Skin_Ctrl', 'ARAM_HeadC', '', 'none'],
            ['ARAM_LeftEyeBrow1_Skin_Ctrl', 'ARAM_HeadC', '', 'none'],
            ['ARAM_LeftEyeBrowAll_Skin_Ctrl', 'ARAM_HeadC', '', 'none'],
            ['ARAM_LeftEyeBrow2_Skin_Ctrl', 'ARAM_HeadC', '', 'none'],
            ['ARAM_JawC', 'ARAM_HeadC', '', 'none'],
            ['ARAM_Tongue3_Ctrl', 'ARAM_HeadC', '', 'none'],
            ['ARAM_Tongue2_Ctrl', 'ARAM_HeadC', '', 'none'],
            ['ARAM_Tongue1_Ctrl', 'ARAM_HeadC', '', 'none'],
            ['ARAM_Tongue_Ctrl', 'ARAM_HeadC', '', 'none'],
            ['ARAM_DownJaw_Skin_Ctrl', 'ARAM_HeadC', '', 'none'],
            ['ARAM_Jaw', 'ARAM_HeadC', '', 'none'],
            ['ARAM_TongueRoot', 'ARAM_HeadC', '', 'none'],
            ['ARAM_TongueBend', 'ARAM_HeadC', '', 'none'],
            ['ARAM_TongueScale', 'ARAM_HeadC', '', 'none'],
            ['ARAM_RightUpDownLip2', 'ARAM_HeadC', '', 'none'],
            ['ARAM_RightUpDownLip1', 'ARAM_HeadC', '', 'none'],
            ['ARAM_DownLip', 'ARAM_HeadC', '', 'none'],
            ['ARAM_LeftUpDownLip1', 'ARAM_HeadC', '', 'none'],
            ['ARAM_LeftUpDownLip2', 'ARAM_HeadC', '', 'none'],
            ['ARAM_RightUpLip2', 'ARAM_HeadC', '', 'none'],
            ['ARAM_UpLip', 'ARAM_HeadC', '', 'none'],
            ['ARAM_LeftUpLip1', 'ARAM_HeadC', '', 'none'],
            ['ARAM_LeftUpLip2', 'ARAM_HeadC', '', 'none'],
            ['ARAM_RightUpLip1', 'ARAM_HeadC', '', 'none'],
            ['ARAM_Mouth', 'ARAM_HeadC', '', 'none'],
            ['ARAM_LeftEyeBrow', 'ARAM_HeadC', '', 'none'],
            ['ARAM_LeftEyeBrow1', 'ARAM_HeadC', '', 'none'],
            ['ARAM_LeftEyeBrow2', 'ARAM_HeadC', '', 'none'],
            ['ARAM_RightEyeBrow', 'ARAM_HeadC', '', 'none'],
            ['ARAM_RightEyeBrow1', 'ARAM_HeadC', '', 'none'],
            ['ARAM_RightEyeBrow2', 'ARAM_HeadC', '', 'none'],
                        
            ['ARAM_WorldRoot_Con','ARAM_WorldRoot_Zero', '', 'center'],
            ['ARAM_MainC','ARAM_WorldRoot_Con', '', 'center'],
            ['ARAM_Neck01FKC','ARAM_SpineTopIKC', '', 'center'],
            ['ARAM_Neck02FKC','ARAM_Neck01FKC', '', 'center'],
            ['ARAM_ROOTC','ARAM_MainC', '', 'center'],
            ['ARAM_MainHipC','ARAM_ROOTC', '', 'center'],
            ['ARAM_Spine01FKC','ARAM_ROOTC', '', 'center'],
            ['ARAM_Spine02FKC','ARAM_Spine01FKC', '', 'center'],
            ['ARAM_HeadC','ARAM_Neck02FKC', '', 'center'],
            ['ARAM_SpineTopIKC','ARAM_Spine02FKC', '', 'center'],
            ['ARAM_JawC','ARAM_HeadC', '', 'center'],
            
            ['TailA_Line5_Bake_Con','TailA_Line3_Bake_Con', '', 'center'],
            ['TailA_Line3_Bake_Con','TailA_Line_Con', '', 'center'],
            ['TailA_Line_Con','ARAM_MainHipC', '', 'center'],
            ['Cloth_Con','ARAM_SpineTopIKC', '', 'center'],
            ['ClothLeft_Con','ARAM_SpineTopIKC', '', 'center'],
            ['ClothRight_Con','ARAM_SpineTopIKC', '', 'center'],
            ['Cap_head_Con','ARAM_Neck02FKC', '', 'center'],
            
            ['ARAM_head_wire_Ctrl','ARAM_HeadC','','center'],
            ['ARAM_lLegSwitchC','ARAM_MainHipC', 'ARAM_rLegSwitchC', 'local'],
            ['ARAM_lFootIKC','ARAM_MainHipC', 'ARAM_rFootIKC', 'default,txm,rym,rzm'],
            ['ARAM_lKneeIKC','ARAM_MainHipC', 'ARAM_rKneeIKC', 'matrix,tx_r_0,ry_r_0,rz_r_0'],
            ['ARAM_lHipFKC','ARAM_MainHipC', 'ARAM_rHipFKC', 'local'],
            ['ARAM_lArmSwitchC','ARAM_lClavicleC', 'ARAM_rArmSwitchC', 'local'],
            ['ARAM_rArmSwitchC','ARAM_rClavicleC', 'ARAM_lArmSwitchC', 'local'],
            ['ARAM_lElbowIKC','ARAM_lClavicleC', 'ARAM_rElbowIKC', 'matrix,tx_r_0,ty_r_0,tz_r_0'],
            ['ARAM_lWristIKC','ARAM_lClavicleC', 'ARAM_rWristIKC', 'matrix,rx_d_180,tx_r_0,ty_r_0,tz_r_0'],
            ['ARAM_lClavicleC','ARAM_SpineTopIKC', 'ARAM_rClavicleC', 'local'],
            ['ARAM_lThumbJ1C','ARAM_lWristIKC,ARAM_lWristFKC', 'ARAM_rThumbJ1C', 'local'],
            ['ARAM_lThumbJ2C','ARAM_lThumbJ1C', 'ARAM_rThumbJ2C', 'local'],
            ['ARAM_lThumbJ3C','ARAM_lThumbJ2C', 'ARAM_rThumbJ3C', 'local'],
            ['ARAM_lPalmC','ARAM_lWristIKC,ARAM_lWristFKC', 'ARAM_rPalmC', 'local'],
            ['ARAM_lFinger1J1C','ARAM_lPalmC', 'ARAM_rFinger1J1C', 'local'],
            ['ARAM_lFinger1J2C','ARAM_lFinger1J1C', 'ARAM_rFinger1J2C', 'local'],
            ['ARAM_lFinger1J3C','ARAM_lFinger1J2C', 'ARAM_rFinger1J3C', 'local'],
            ['ARAM_lToeIKC','ARAM_lFootIKC', 'ARAM_rToeIKC', 'default,rym,rzm'],
            ['ARAM_rLegSwitchC','ARAM_MainHipC', 'ARAM_lLegSwitchC', 'local'],
            ['ARAM_rFootIKC','ARAM_MainHipC', 'ARAM_lFootIKC', 'default,txm,rym,rzm'],
            ['ARAM_rKneeIKC','ARAM_MainHipC', 'ARAM_lKneeIKC', 'matrix,tx_r_0,ry_r_0,rz_r_0'],
            ['ARAM_rHipFKC','ARAM_MainHipC', 'ARAM_lHipFKC', 'local'],
            ['ARAM_rElbowIKC','ARAM_rClavicleC', 'ARAM_lElbowIKC', 'matrix,tx_r_0,ty_r_0,tz_r_0'],
            ['ARAM_rWristIKC','ARAM_rClavicleC', 'ARAM_lWristIKC', 'matrix,rx_d_180,tx_r_0,ty_r_0,tz_r_0'],
            ['ARAM_rClavicleC','ARAM_SpineTopIKC', 'ARAM_lClavicleC', 'local'],
            ['ARAM_rThumbJ1C','ARAM_rWristIKC,ARAM_rWristFKC', 'ARAM_lThumbJ1C', 'local'],
            ['ARAM_rThumbJ2C','ARAM_rThumbJ1C', 'ARAM_lThumbJ2C', 'local'],
            ['ARAM_rThumbJ3C','ARAM_rThumbJ2C', 'ARAM_lThumbJ3C', 'local'],
            ['ARAM_rPalmC','ARAM_rWristIKC,ARAM_rWristFKC', 'ARAM_lPalmC', 'local'],
            ['ARAM_rFinger1J1C','ARAM_rPalmC', 'ARAM_lFinger1J1C', 'local'],
            ['ARAM_rFinger1J2C','ARAM_rFinger1J1C', 'ARAM_lFinger1J2C', 'local'],
            ['ARAM_rFinger1J3C','ARAM_rFinger1J2C', 'ARAM_lFinger1J3C', 'local'],
            ['ARAM_rToeIKC','ARAM_rFootIKC', 'ARAM_lToeIKC', 'default,rym,rzm'],

            ['LeftEarA_Line5_Bake_Con','LeftEarA_Line3_Bake_Con', 'RightEarA_Line5_Bake_Con', 'default,txm,rym,rzm'],
            ['LeftEarA_Line3_Bake_Con','LeftEarA_Line_Con', 'RightEarA_Line3_Bake_Con', 'default,txm,rym,rzm'],
            ['LeftEarA_Line_Con','Cap_head_Con', 'RightEarA_Line_Con', 'default,txm,rym,rzm'],
            ['RightEarA_Line5_Bake_Con','RightEarA_Line3_Bake_Con', 'LeftEarA_Line5_Bake_Con', 'default,txm,rym,rzm'],
            ['RightEarA_Line3_Bake_Con','RightEarA_Line_Con', 'LeftEarA_Line3_Bake_Con', 'default,txm,rym,rzm'],
            ['RightEarA_Line_Con','Cap_head_Con', 'LeftEarA_Line_Con', 'default,txm,rym,rzm'],

            ['ARAM_lShoulderFKC','ARAM_lClavicleC', 'ARAM_rShoulderFKC', 'local'],
            ['ARAM_lElbowFKC','ARAM_lShoulderFKC', 'ARAM_rElbowFKC', 'local'],
            ['ARAM_lWristFKC','ARAM_lElbowFKC', 'ARAM_rWristFKC', 'local'],
            ['ARAM_rShoulderFKC','ARAM_rClavicleC', 'ARAM_lShoulderFKC', 'local'],
            ['ARAM_rElbowFKC','ARAM_rShoulderFKC', 'ARAM_lElbowFKC', 'local'],
            ['ARAM_rWristFKC','ARAM_rElbowFKC', 'ARAM_lWristFKC', 'local']]
    
    
    mocCreatTarget = {
        'root' : 'ARAM_SH_ROOTJ',
        'spines' : ['ARAM_SH_Spine01J','ARAM_SH_Spine02J'],
        'chest' : 'ARAM_SH_SpineTopJ',
        'neck' : 'ARAM_SH_Neck02J',
        'head' : 'ARAM_SH_HeadJ',
        'headEnd' : 'ARAM_SH_HeadTipJ',
        
        'hip_L_' : 'ARAM_SH_lHipCurveJ',
        'knee_L_' : 'ARAM_SH_lKneeCurveJ',
        'ankle_L_' : 'ARAM_SH_lAnkleJ',
        'ball_L_'  : 'ARAM_SH_lBallJ',
        'ballEnd_L_'  : 'ARAM_SH_lToeJ',
        
        'clevicle_L_' : 'ARAM_SH_lClavicleJ',
        'shoulder_L_' : 'ARAM_SH_lShoulderCurveJ',
        'elbow_L_' : 'ARAM_SH_lElbowCurveJ',
        'wrist_L_' : 'ARAM_SH_lWristJ',
        
        'thumb_L_' : ['ARAM_SH_lThumbJ1', 'ARAM_SH_lThumbJ2', 'ARAM_SH_lThumbJ3', 'ARAM_SH_lThumbJTip' ],
        'index_L_' : ['ARAM_SH_lPalmJ', 'ARAM_SH_lFinger1J1', 'ARAM_SH_lFinger1J2', 'ARAM_SH_lFinger1J3', 'ARAM_SH_lFinger1JTip'],
        'middle_L_' : [],
        'ring_L_' : [],
        'pinky_L_' : [],
        
        'hip_R_' : 'ARAM_SH_rHipCurveJ',
        'knee_R_' : 'ARAM_SH_rKneeCurveJ',
        'ankle_R_' : 'ARAM_SH_rAnkleJ',
        'ball_R_'  : 'ARAM_SH_rBallJ',
        'ballEnd_R_'  : 'ARAM_SH_rToeJ',
        
        'clevicle_R_' : 'ARAM_SH_rClavicleJ',
        'shoulder_R_' : 'ARAM_SH_rShoulderCurveJ',
        'elbow_R_' : 'ARAM_SH_rElbowCurveJ',
        'wrist_R_' : 'ARAM_SH_rWristJ',
        
        'thumb_R_' : ['ARAM_SH_rThumbJ1', 'ARAM_SH_rThumbJ2', 'ARAM_SH_rThumbJ3', 'ARAM_SH_rThumbJTip'],
        'index_R_' : ['ARAM_SH_rPalmJ', 'ARAM_SH_rFinger1J1', 'ARAM_SH_rFinger1J2', 'ARAM_SH_rFinger1J3', 'ARAM_SH_rFinger1JTip' ],
        'middle_R_' : [],
        'ring_R_' : [],
        'pinky_R_' : [],
        
        'meshs' : ['ARAM_Geo_Grp']
    }



class CH_Pipi:
    
    defaultIgnore = []
    reverseAttrs = []
    
    leftPrefix  = ['Lf']
    rightPrefix = ['Rt']
    
    data = [
            ['LfEye_Ctrl', 'Head_Ctrl', '', 'none'],
            ['RtEye_Ctrl', 'Head_Ctrl', '', 'none'],
            ['Ctl_eye_R_', 'Head_Ctrl', '', 'none'],
            ['Ctl_eye_L_', 'Head_Ctrl', '', 'none'],
        
            ['Chest_Ctrl','SpineFk2_Ctrl','','center'],
            ['Fly_Ctrl','Move_Ctrl','','center'],
            ['HairA1_Ctrl','Head_Ctrl','','default'],
            ['HairA2_Ctrl','HairA1_Ctrl','','default'],
            ['HairA3_Ctrl','HairA2_Ctrl','','default'],
            ['HariB1_Ctrl','Head_Ctrl','','default'],
            ['HariB2_Ctrl','HariB1_Ctrl','','default'],
            ['Head_Ctrl','Chest_Ctrl','','center'],
            ['Hip_Ctrl','Root_Ctrl','','center'],
            ['LfArm1Fk_Ctrl','LfClavicle_Ctrl','RtArm1Fk_Ctrl','local'],
            ['LfArm2Fk_Ctrl','LfArm1Fk_Ctrl','RtArm2Fk_Ctrl','local'],
            ['LfArm3Fk_Ctrl','LfArm2Fk_Ctrl','RtArm3Fk_Ctrl','local'],
            ['LfArmIk_Ctrl','LfClavicle_Ctrl','RtArmIk_Ctrl','matrix,tx_r_0,ty_r_0,tz_r_0,rx_d_180'],
            ['LfArmPv_Ctrl','LfClavicle_Ctrl','RtArmPv_Ctrl','default,txm'],
            ['LfArmSwitch_Ctrl','LfClavicle_Ctrl','RtArmSwitch_Ctrl','default'],
            ['LfBall_Ctrl','LfLeg3Fk_Ctrl','RtBall_Ctrl','local'],
            ['LfClavicle_Ctrl','Chest_Ctrl','RtClavicle_Ctrl','local'],
            ['LfEar1_Ctrl','Head_Ctrl','RtEar1_Ctrl','local'],
            ['LfEar2_Ctrl','LfEar1_Ctrl','RtEar2_Ctrl','local'],
            ['LfEar3_Ctrl','LfEar2_Ctrl','RtEar3_Ctrl','local'],
            ['LfEar4_Ctrl','LfEar3_Ctrl','RtEar4_Ctrl','local'],
            ['LfFinger_Ctrl','LfArm3Fk_Ctrl,LfArmIk_Ctrl','RtFinger_Ctrl',''],
            ['LfIndex1_Ctrl','LfIndexRoot_Ctrl','RtIndex1_Ctrl','local'],
            ['LfIndex2_Ctrl','LfIndex1_Ctrl','RtIndex2_Ctrl','local'],
            ['LfIndexRoot_Ctrl','LfFinger_Ctrl','RtIndexRoot_Ctrl','local'],
            ['LfIndex_Ctrl','LfIndexRoot_Ctrl','RtIndex_Ctrl','local,tym,tzm'],
            ['LfLeg1Fk_Ctrl','LfUpLeg_Ctrl','RtLeg1Fk_Ctrl','local'],
            ['LfLeg2Fk_Ctrl','LfLeg1Fk_Ctrl','RtLeg2Fk_Ctrl','local'],
            ['LfLeg3Fk_Ctrl','LfLeg2Fk_Ctrl','RtLeg3Fk_Ctrl','local'],
            ['LfLegIk_Ctrl','LfUpLeg_Ctrl','RtLegIk_Ctrl','matrix,tx_r_0,ry_r_0,rz_r_0'],
            ['LfLegPv_Ctrl','LfUpLeg_Ctrl','RtLegPv_Ctrl','default,txm'],
            ['LfLegSwitch_Ctrl','LfUpLeg_Ctrl','RtLegSwitch_Ctrl',''],
            ['LfMiddle1_Ctrl','LfMiddleRoot_Ctrl','RtMiddle1_Ctrl','local'],
            ['LfMiddle2_Ctrl','LfMiddle1_Ctrl','RtMiddle2_Ctrl','local'],
            ['LfMiddleRoot_Ctrl','LfFinger_Ctrl','RtMiddleRoot_Ctrl','local'],
            ['LfMiddle_Ctrl','LfFinger_Ctrl','RtMiddle_Ctrl','local,tym,tzm'],
            ['LfPinky1_Ctrl','LfPinkyRoot_Ctrl','RtPinky1_Ctrl','local'],
            ['LfPinky2_Ctrl','LfPinky1_Ctrl','RtPinky2_Ctrl','local'],
            ['LfPinkyRoot_Ctrl','LfFinger_Ctrl','RtPinkyRoot_Ctrl','local'],
            ['LfPinky_Ctrl','LfPinkyRoot_Ctrl','RtPinky_Ctrl','local,tym,tzm'],
            ['LfThumb1_Ctrl','LfThumbRoot_Ctrl','RtThumb1_Ctrl','local'],
            ['LfThumb2_Ctrl','LfThumb1_Ctrl','RtThumb2_Ctrl','local'],
            ['LfThumbRoot_Ctrl','LfFinger_Ctrl','RtThumbRoot_Ctrl','local'],
            ['LfThumb_Ctrl','LfThumbRoot_Ctrl','RtThumb_Ctrl','local,tym,tzm'],
            ['LfUpLeg_Ctrl','Hip_Ctrl','RtUpLeg_Ctrl','txm,rym,rzm'],
            ['Mouth1_Ctrl','Head_Ctrl','','center'],
            ['Mouth2_Ctrl','Mouth1_Ctrl','','center'],
            ['Move_Ctrl','World_Ctrl','','center'],
            ['Nose_Ctrl','Mouth2_Ctrl','','center'],
            ['Root_Ctrl','Fly_Ctrl','','center'],
            ['RtArm1Fk_Ctrl','RtClavicle_Ctrl','LfArm1Fk_Ctrl','local'],
            ['RtArm2Fk_Ctrl','RtArm1Fk_Ctrl','LfArm2Fk_Ctrl','local'],
            ['RtArm3Fk_Ctrl','RtArm2Fk_Ctrl','LfArm3Fk_Ctrl','local'],
            ['RtArmIk_Ctrl','RtClavicle_Ctrl','LfArmIk_Ctrl','matrix,tx_r_0,ty_r_0,tz_r_0,rx_d_180'],
            ['RtArmPv_Ctrl','RtClavicle_Ctrl','LfArmPv_Ctrl','default,txm'],
            ['RtArmSwitch_Ctrl','RtClavicle_Ctrl','LfArmSwitch_Ctrl','default'],
            ['RtBall_Ctrl','RtLeg3Fk_Ctrl','LfBall_Ctrl','local'],
            ['RtClavicle_Ctrl','Chest_Ctrl','LfClavicle_Ctrl','local'],
            ['RtEar1_Ctrl','Head_Ctrl','LfEar1_Ctrl','local'],
            ['RtEar2_Ctrl','RtEar1_Ctrl','LfEar2_Ctrl','local'],
            ['RtEar3_Ctrl','RtEar2_Ctrl','LfEar3_Ctrl','local'],
            ['RtEar4_Ctrl','RtEar3_Ctrl','LfEar4_Ctrl','local'],
            ['RtFinger_Ctrl','RtArm3Fk_Ctrl,RtArmIk_Ctrl','LfFinger_Ctrl',''],
            ['RtIndex1_Ctrl','RtIndexRoot_Ctrl','LfIndex1_Ctrl','local'],
            ['RtIndex2_Ctrl','RtIndex1_Ctrl','LfIndex2_Ctrl','local'],
            ['RtIndexRoot_Ctrl','RtFinger_Ctrl','LfIndexRoot_Ctrl','local'],
            ['RtIndex_Ctrl','RtIndexRoot_Ctrl','LfIndex_Ctrl','local,tym,tzm'],
            ['RtLeg1Fk_Ctrl','RtUpLeg_Ctrl','LfLeg1Fk_Ctrl','local'],
            ['RtLeg2Fk_Ctrl','RtLeg1Fk_Ctrl','LfLeg2Fk_Ctrl','local'],
            ['RtLeg3Fk_Ctrl','RtLeg2Fk_Ctrl','LfLeg3Fk_Ctrl','local'],
            ['RtLegIk_Ctrl','RtUpLeg_Ctrl','LfLegIk_Ctrl','matrix,tx_r_0,ry_r_0,rz_r_0'],
            ['RtLegPv_Ctrl','RtUpLeg_Ctrl','LfLegPv_Ctrl','default,txm'],
            ['RtLegSwitch_Ctrl','RtUpLeg_Ctrl','LfLegSwitch_Ctrl',''],
            ['RtMiddle1_Ctrl','RtMiddleRoot_Ctrl','LfMiddle1_Ctrl','local'],
            ['RtMiddle2_Ctrl','RtMiddle1_Ctrl','LfMiddle2_Ctrl','local'],
            ['RtMiddleRoot_Ctrl','RtFinger_Ctrl','LfMiddleRoot_Ctrl','local'],
            ['RtMiddle_Ctrl','RtMiddleRoot_Ctrl','LfMiddle_Ctrl','local,tym,tzm'],
            ['RtPinky1_Ctrl','RtPinkyRoot_Ctrl','LfPinky1_Ctrl','local'],
            ['RtPinky2_Ctrl','RtPinky1_Ctrl','LfPinky2_Ctrl','local'],
            ['RtPinkyRoot_Ctrl','RtFinger_Ctrl','LfPinkyRoot_Ctrl','local'],
            ['RtPinky_Ctrl','RtPinkyRoot_Ctrl','LfPinky_Ctrl','local,tym,tzm'],
            ['RtThumb1_Ctrl','RtThumbRoot_Ctrl','LfThumb1_Ctrl','local'],
            ['RtThumb2_Ctrl','RtThumb1_Ctrl','LfThumb2_Ctrl','local'],
            ['RtThumbRoot_Ctrl','RtFinger_Ctrl','LfThumbRoot_Ctrl','local'],
            ['RtThumb_Ctrl','RtThumbRoot_Ctrl','LfThumb_Ctrl','local,tym,tzm'],
            ['RtUpLeg_Ctrl','Hip_Ctrl','LfUpLeg_Ctrl','txm,rym,rzm'],
            ['SpineFk1_Ctrl','Root_Ctrl','','center'],
            ['SpineFk2_Ctrl','SpineFk1_Ctrl','','center'],
            ['SquashBend1Detail_Ctrl','Head_Ctrl','','center'],
            ['SquashBend2Detail_Ctrl','Head_Ctrl','','center'],
            ['SquashBend3Detail_Ctrl','Head_Ctrl','','center'],
            ['SquashBend4Detail_Ctrl','Head_Ctrl','','center'],
            ['SquashBend5Detail_Ctrl','Head_Ctrl','','center'],
            ['SquashBendDirection_Ctrl','Head_Ctrl','','center'],
            ['SquashBend_Ctrl','Head_Ctrl','','center'],
            ['Tail1_Ctrl','Hip_Ctrl','','center'],
            ['Tail2_Ctrl','Tail1_Ctrl','','center'],
            ['World_Ctrl','WorldCtrl_Grp','','center']]
    
    mocCreatTarget = {
        'root' : 'Root_Jnt',
        'spines' : ['Spine1_Jnt','Spine2_Jnt'],
        'chest' : 'ChestFix_Jnt',
        'neck' : 'Head_Jnt',
        'head' : 'Head_Jnt',
        'headEnd' : 'HeadEnd_Jnt',
        
        'hip_L_' : 'LfHip_Jnt',
        'knee_L_' : 'LfKnee_Jnt',
        'ankle_L_' : 'LfAnkle_Jnt',
        'ball_L_'  : 'LfBall_Jnt',
        'ballEnd_L_'  : 'LfToe_Jnt',
        
        'clevicle_L_' : 'LfClavicle_Jnt',
        'shoulder_L_' : 'LfShoulder_Jnt',
        'elbow_L_' : 'LfElbow_Jnt',
        'wrist_L_' : 'LfWrist_Jnt',
        
        'thumb_L_' : ['LfThumbRoot_Jnt', 'LfThumb1_Jnt', 'LfThumb2_Jnt', 'LfThumb3_Jnt' ],
        'index_L_' : ['LfIndexRoot_Jnt', 'LfIndex1_Jnt', 'LfIndex2_Jnt', 'LfIndex3_Jnt'],
        'middle_L_' : ['LfMiddleRoot_Jnt','LfMiddle1_Jnt','LfMiddle2_Jnt', 'LfMiddle3_Jnt'],
        'ring_L_' : ['LfPinkyRoot_Jnt','LfPinky1_Jnt','LfPinky2_Jnt', 'LfPinky3_Jnt'],
        'pinky_L_' : [],
        
        'hip_R_' : 'RtHip_Jnt',
        'knee_R_' : 'RtKnee_Jnt',
        'ankle_R_' : 'RtAnkle_Jnt',
        'ball_R_'  : 'RtBall_Jnt',
        'ballEnd_R_'  : 'RtToe_Jnt',
        
        'clevicle_R_' : 'RtClavicle_Jnt',
        'shoulder_R_' : 'RtShoulder_Jnt',
        'elbow_R_' : 'RtElbow_Jnt',
        'wrist_R_' : 'RtWrist_Jnt',
        
        'thumb_R_' : ['RtThumbRoot_Jnt', 'RtThumb1_Jnt', 'RtThumb2_Jnt', 'RtThumb3_Jnt' ],
        'index_R_' : ['RtIndexRoot_Jnt', 'RtIndex1_Jnt', 'RtIndex2_Jnt', 'RtIndex3_Jnt'],
        'middle_R_' : ['RtMiddleRoot_Jnt','RtMiddle1_Jnt','RtMiddle2_Jnt', 'RtMiddle3_Jnt'],
        'ring_R_' : ['RtPinkyRoot_Jnt','RtPinky1_Jnt','RtPinky2_Jnt', 'RtPinky3_Jnt'],
        'pinky_R_' : [],
        
        'meshs' : ['Mod_Grp']
    }



class Bu:

    defaultIgnore = ['Follow', 'DirectionCtrlVisibility', 'DetailCtrlVisibility']
    reverseAttrs = []
    
    leftPrefix  = ['Lf', 'Left', '_L_']
    rightPrefix = ['Rt', 'Right', '_R_']
    
    data = [['SquashBend1DetailCtrl', 'SquashBendCtrl', 'SquashBend1DetailCtrl', 'center'],
            ['SquashBend2DetailCtrl', 'SquashBendCtrl', 'SquashBend2DetailCtrl', 'center'],
            ['SquashBend3DetailCtrl', 'SquashBendCtrl', 'SquashBend3DetailCtrl', 'center'],
            ['SquashBend4DetailCtrl', 'SquashBendCtrl', 'SquashBend4DetailCtrl', 'center'],
            ['SquashBend5DetailCtrl', 'SquashBendCtrl', 'SquashBend5DetailCtrl', 'center'],
            ['SquashBendCtrl', 'RootCtrl', 'SquashBendCtrl', 'center'],
            ['LfBckWheelPush2Ctrl', 'LfBckWheelCtrl', 'RtBckWheelPush2Ctrl', 'local'],
            ['LfBckWheelPush1Ctrl', 'LfBckWheelCtrl', 'RtBckWheelPush1Ctrl', 'local'],
            ['LfBckWheelPush4Ctrl', 'LfBckWheelCtrl', 'RtBckWheelPush4Ctrl', 'local'],
            ['LfBckWheelPush3Ctrl', 'LfBckWheelCtrl', 'RtBckWheelPush3Ctrl', 'local'],
            ['LfBckWheelCtrl', 'HipCtrl', 'RtBckWheelCtrl', 'default'],
            ['RtBckWheelPush2Ctrl', 'RtBckWheelCtrl', 'LfBckWheelPush2Ctrl', 'local'],
            ['RtBckWheelPush1Ctrl', 'RtBckWheelCtrl', 'LfBckWheelPush1Ctrl', 'local'],
            ['RtBckWheelPush3Ctrl', 'RtBckWheelCtrl', 'LfBckWheelPush3Ctrl', 'local'],
            ['RtBckWheelPush4Ctrl', 'RtBckWheelCtrl', 'LfBckWheelPush4Ctrl', 'local'],
            ['RtBckWheelCtrl', 'HipCtrl', 'LfBckWheelCtrl', 'default'],
            ['HipCtrl', 'RaiseRotCtrl', 'HipCtrl', 'center'],
            ['SpineCtrl', 'RaiseRotCtrl', 'SpineCtrl', 'center'],
            ['LfFrtWheelPush1Ctrl', 'LfFrtWheelCtrl', 'RtFrtWheelPush1Ctrl', 'local'],
            ['LfFrtWheelPush3Ctrl', 'LfFrtWheelCtrl', 'RtFrtWheelPush3Ctrl', 'local'],
            ['LfFrtWheelPush2Ctrl', 'LfFrtWheelCtrl', 'RtFrtWheelPush2Ctrl', 'local'],
            ['LfFrtWheelPush4Ctrl', 'LfFrtWheelCtrl', 'RtFrtWheelPush4Ctrl', 'local'],
            ['LfFrtWheelCtrl', 'HeadCtrl', 'RtFrtWheelCtrl', 'default'],
            ['RtFrtWheelPush2Ctrl', 'RtFrtWheelCtrl', 'LfFrtWheelPush2Ctrl', 'local'],
            ['RtFrtWheelPush1Ctrl', 'RtFrtWheelCtrl', 'LfFrtWheelPush1Ctrl', 'local'],
            ['RtFrtWheelPush3Ctrl', 'RtFrtWheelCtrl', 'LfFrtWheelPush3Ctrl', 'local'],
            ['RtFrtWheelPush4Ctrl', 'RtFrtWheelCtrl', 'LfFrtWheelPush4Ctrl', 'local'],
            ['RtFrtWheelCtrl', 'HeadCtrl', 'LfFrtWheelCtrl', 'default'],
            ['NoseCtrl', 'HeadCtrl', 'NoseCtrl', 'center'],
            ['BaseCtl_eyeSlider_L_', 'LeftEyeCtrl', 'BaseCtl_eyeSlider_L_', 'default'],
            ['LeftEyeCtrl', 'HeadCtrl', 'RightEyeCtrl', 'default'],
            ['BaseCtl_eyeSlider_R_', 'RightEyeCtrl', 'BaseCtl_eyeSlider_R_', 'default'],
            ['RightEyeCtrl', 'HeadCtrl', 'LeftEyeCtrl', 'default'],
            ['GlassCtrl', 'HeadCtrl', 'GlassCtrl', 'default'],
            ['HeadSqxB1DetailCtrl', 'HeadSqxBCtrl', 'HeadSqxB1DetailCtrl', 'center'],
            ['HeadSqxB2DetailCtrl', 'HeadSqxBCtrl', 'HeadSqxB2DetailCtrl', 'center'],
            ['HeadSqxB3DetailCtrl', 'HeadSqxBCtrl', 'HeadSqxB3DetailCtrl', 'center'],
            ['HeadSqxB4DetailCtrl', 'HeadSqxBCtrl', 'HeadSqxB4DetailCtrl', 'center'],
            ['HeadSqxB5DetailCtrl', 'HeadSqxBCtrl', 'HeadSqxB5DetailCtrl', 'center'],
            ['HeadSqxBCtrl', 'HeadCtrl', 'HeadSqxBCtrl', 'center'],
            ['HandleCtrl', 'HandleMoveCtrl', 'HandleCtrl', 'default'],
            ['HandleMoveCtrl', 'HeadCtrl', 'HandleMoveCtrl', 'default'],
            ['HairLumpCtrl', 'HeadCtrl', 'HairLumpCtrl', 'center'],
            ['HeadSqxBDirectionCtrl', 'HeadCtrl', 'HeadSqxBDirectionCtrl', 'center'],
            ['LfFrtWheelCoverCtrl', 'HeadCtrl', 'RtFrtWheelCoverCtrl', 'local'],
            ['RtFrtWheelCoverCtrl', 'HeadCtrl', 'LfFrtWheelCoverCtrl', 'local'],
            ['HeadCtrl', 'RaiseRotCtrl', 'HeadCtrl', 'center'],
            ['LfBckWheelCoverCtrl', 'RaiseRotCtrl', 'RtBckWheelCoverCtrl', 'local'],
            ['RtBckWheelCoverCtrl', 'RaiseRotCtrl', 'LfBckWheelCoverCtrl', 'local'],
            ['RaiseRotCtrl', 'RootCtrl', 'RaiseRotCtrl', 'center'],
            ['SquashBendDirectionCtrl', 'RootCtrl', 'SquashBendDirectionCtrl', 'center'],
            ['RootCtrl', 'MoveCtrl', 'RootCtrl', 'center'],
            ['RotCtrl', 'MoveCtrl', 'RotCtrl', 'center'],
            ['MoveCtrl', 'WorldCtrl', 'MoveCtrl', 'center'],
            ['WorldCtrl', 'WorldCtrlGrp', 'WorldCtrl', 'center']]




class minion_A:
    
    defaultIgnore = ['Follow', 'DirectionCtrlVisibility', 'DetailCtrlVisibility']
    reverseAttrs = []
    
    leftPrefix  = ['Lf', 'Left', '_L_']
    rightPrefix = ['Rt', 'Right', '_R_']
    
    data = [['head_A_ctr', 'body_ctr', 'head_A_ctr', 'center'],
            ['head_B_ctr', 'body_ctr', 'head_B_ctr', 'center'],
            ['head_C_ctr', 'body_ctr', 'head_C_ctr', 'center'],
            ['Ctl_Mouth', 'body_ctr', 'Ctl_Mouth', 'center'],
            ['body_ctr', 'walk_ctr', 'body_ctr', 'center'],
            ['walk_ctr', 'world_ctr', 'walk_ctr', 'center'],
            ['world_ctr', 'world_ctrGrp', 'world_ctr', 'center'],
            ['Ctl_Leg_L_01', 'Ctl_Leg_L_00', 'Ctl_Leg_R_01', 'center'],
            ['Ctl_Leg_L_00', 'head_C_ctr', 'Ctl_Leg_R_00', 'center'],
            ['Ctl_Leg_R_01', 'Ctl_Leg_R_00', 'Ctl_Leg_L_01', 'center'],
            ['Ctl_Leg_R_00', 'head_C_ctr', 'Ctl_Leg_L_00', 'center']]




class minion_B:
    
    defaultIgnore = ['Follow', 'DirectionCtrlVisibility', 'DetailCtrlVisibility']
    reverseAttrs = []
    
    leftPrefix  = ['Lf', 'Left', '_L_']
    rightPrefix = ['Rt', 'Right', '_R_']
    
    data = [['head_A_ctr', 'body_ctr', 'head_A_ctr', 'center'],
            ['head_B_ctr', 'body_ctr', 'head_B_ctr', 'center'],
            ['head_C_ctr', 'body_ctr', 'head_C_ctr', 'center'],
            ['Ctl_Mouth', 'body_ctr', 'Ctl_Mouth', 'center'],
            ['body_ctr', 'walk_ctr', 'body_ctr', 'center'],
            ['walk_ctr', 'world_ctr', 'walk_ctr', 'center'],
            ['world_ctr', 'world_ctrGrp', 'world_ctr', 'center'],
            ['Ctl_Leg_L_01', 'Ctl_Leg_L_00', 'Ctl_Leg_R_01', 'center'],
            ['Ctl_Leg_L_00', 'head_C_ctr', 'Ctl_Leg_R_00', 'center'],
            ['Ctl_Leg_R_01', 'Ctl_Leg_R_00', 'Ctl_Leg_L_01', 'center'],
            ['Ctl_Leg_R_00', 'head_C_ctr', 'Ctl_Leg_L_00', 'center']]




class minion_C:
    
    defaultIgnore = ['Follow', 'DirectionCtrlVisibility', 'DetailCtrlVisibility']
    reverseAttrs = []
    
    leftPrefix  = ['Lf', 'Left', '_L_']
    rightPrefix = ['Rt', 'Right', '_R_']
    
    data = [['head_A_ctr', 'body_ctr', 'head_A_ctr', 'center'],
            ['head_B_ctr', 'body_ctr', 'head_B_ctr', 'center'],
            ['head_C_ctr', 'body_ctr', 'head_C_ctr', 'center'],
            ['Ctl_Mouth', 'body_ctr', 'Ctl_Mouth', 'center'],
            ['body_ctr', 'walk_ctr', 'body_ctr', 'center'],
            ['walk_ctr', 'world_ctr', 'walk_ctr', 'center'],
            ['world_ctr', 'world_ctrGrp', 'world_ctr', 'center'],
            ['Ctl_Leg_L_01', 'Ctl_Leg_L_00', 'Ctl_Leg_R_01', 'center'],
            ['Ctl_Leg_L_00', 'head_C_ctr', 'Ctl_Leg_R_00', 'center'],
            ['Ctl_Leg_R_01', 'Ctl_Leg_R_00', 'Ctl_Leg_L_01', 'center'],
            ['Ctl_Leg_R_00', 'head_C_ctr', 'Ctl_Leg_L_00', 'center']]




class FacialLayeredTextureConnection:
    
    def __init__(self, facialRootPath=None ):

        self.__rootPath = facialRootPath
        
    
    
    def sliderConnection(self, sliderAttr, layeredNode, **options ):
        
        import maya.cmds as cmds
        
        offset = 0
        if options.has_key( 'offset' ):
            offset = options[ 'offset' ]
        
        layeredNode = sgcommands.convertSg( layeredNode )
        sliderAttr = sgcommands.convertSg( sliderAttr )
        
        plug = layeredNode.inputs.getPlug()
        
        for i in range( plug.numElements() ):
            setRange = sgcommands.createNode( 'setRange' )
            multNode = sgcommands.createNode( 'multDoubleLinear' )
            setRange.oldMinX.set( offset + i-0.5 )
            setRange.oldMaxX.set( offset + i+0.5 )
            setRange.oldMinY.set( offset + i+0.5 )
            setRange.oldMaxY.set( offset + i+1.4999 )
            setRange.maxX.set( 1 )
            setRange.minY.set( 1 )
            sliderAttr >> setRange.valueX
            sliderAttr >> setRange.valueY
            setRange.outValueX >> multNode.input1
            setRange.outValueY >> multNode.input2
            if not cmds.isConnected( multNode.output.name(), plug[i].name() + '.isVisible' ):
                cmds.connectAttr( multNode.output.name(), plug[i].name() + '.isVisible', f=1 )
    


    def facialTextureToLayerNode(self, facialName, layerNode, **options ):
        
        facialPath = self.__rootPath + '/' + facialName
        
        sliderAttr = ''
        offset = 0
        if options.has_key( 'sliderAttr' ):
            sliderAttr = options['sliderAttr']
        if options.has_key( 'offset' ):
            offset = options[ 'offset' ]
        
        for root, dirs, imageList in os.walk( facialPath ):
            break

        FPath = ''
        PPath = ''
        SPath = ''
        
        for image in imageList:
            splits = image.split( '.' )[0].split( '_' )
            if splits[-1].lower() == 'f':
                FPath = facialPath + '/' + image
            elif splits[-1].lower() == 'p':
                PPath = facialPath + '/' + image
            elif splits[-1].lower() == 's':
                SPath = facialPath + '/' + image

        fNode,  fPlace2d = sgcommands.createTextureFileNode( FPath )
        pmNode, pmPlace2d = sgcommands.createTextureFileNode( PPath )
        ppNode, ppPlace2d = sgcommands.createTextureFileNode( PPath )
        smNode, smPlace2d = sgcommands.createTextureFileNode( SPath )
        spNode, spPlace2d = sgcommands.createTextureFileNode( SPath )
        
        pmPlace2d.repeatU.set( -1 )
        smPlace2d.repeatU.set( -1 )
        
        sgcommands.assignToLayeredTexture( smNode, layerNode, index=0, blendMode=0 )
        sgcommands.assignToLayeredTexture( pmNode, layerNode, index=1, blendMode=0 )
        sgcommands.assignToLayeredTexture( fNode , layerNode, index=2, blendMode=0 )
        sgcommands.assignToLayeredTexture( ppNode, layerNode, index=3, blendMode=0 )
        sgcommands.assignToLayeredTexture( spNode, layerNode, index=4, blendMode=0 )
        
        if sliderAttr:
            self.sliderConnection( sliderAttr, layerNode, offset=offset )
        



