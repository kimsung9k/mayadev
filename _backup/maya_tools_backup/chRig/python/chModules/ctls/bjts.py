globalOffsetValue = .001

class BJT:
    midAxis = 'z'
    midOffset = globalOffsetValue

class Arm_L( BJT ):
    midOffset = -globalOffsetValue
    
class Leg_R( BJT ):
    midOffset = -globalOffsetValue
    
class Leg_R_Lower4( BJT ):
    midOffset = globalOffsetValue
    
class Leg_R_Foot( BJT ):
    midOffset = globalOffsetValue
    
class Leg_L_Lower4( BJT ):
    midOffset = globalOffsetValue
    
class Leg_L_Foot( BJT ):
    midOffset = globalOffsetValue
    
class Collar_L( BJT ):
    midAxis = 'y'
    
class Collar_R( BJT ):
    midAxis = 'y'
    midOffset = -globalOffsetValue