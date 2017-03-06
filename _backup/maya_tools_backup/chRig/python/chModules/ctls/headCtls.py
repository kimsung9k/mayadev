import allCtls

class Head_CTL( allCtls.AllCtls ):
    mirrorType = 'center'
    mirrorP = 'Neck_CTL'
    
class NeckMiddle_CTL( allCtls.AllCtls ):
    mirrorType = 'center'
    mirrorP = 'Neck_CTL'

class Neck_CTL( allCtls.AllCtls ):
    mirrorType = 'center'
    mirrorP = 'Chest_CTL'
    
class EyeAim_CTL( allCtls.AllCtls ):
    mirrorType = 'position'
    
class Eye_CTL( allCtls.AllCtls ):
    mirrorType = 'center'
    mirrorP = 'Head_CTL'