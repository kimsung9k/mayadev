import allCtls

class Arm_IK_CTL( allCtls.AllCtls ):
    mirrorType = 'objP'
    mirrorP = 'Collar__CTL'
    transformAttrs = ['poleTwist', 'length', 'bias']
    
class Leg_IK_CTL( allCtls.AllCtls ):
    mirrorType = 'axis'
    mirrorP = 'Hip_CTL'
    mirrorBaseVector = [1,0,0]
    transformAttrs = ['poleTwist', 'length', 'bias', 'tapToe', 'heelLift', 'walkRoll', 'toeRot', 'kneeAutoAngle' ]

class PoleV_CTL( allCtls.AllCtls ):
    transformAttrs = ['positionAttach']
    
class Leg_Foot_IK_CTL( allCtls.AllCtls ):
    transformAttrs = ['heelRot', 'ballRot', 'heelTwist', 'ballTwist', 'toeTwist' ]
    
class Switch_CTL( allCtls.AllCtls ):
    transformAttrs = ['twist', 'interpoleSwitch']