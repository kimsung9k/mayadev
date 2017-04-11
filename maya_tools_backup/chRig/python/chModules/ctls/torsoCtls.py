import allCtls

class Chest_CTL( allCtls.AllCtls ):
    mirrorType = 'center'
    mirrorP = 'TorsoRotate_CTL'
    
class ChestMove_CTL( allCtls.AllCtls ):
    mirrorType = 'center'
    mirrorP = 'Chest_CTL'

class Waist_CTL( allCtls.AllCtls ):
    mirrorType = 'center'
    mirrorP = 'Waist_CTL_GRP'
    
class TorsoRotate_CTL( allCtls.AllCtls ):
    mirrorType = 'center'
    mirrorP = 'Root_CTL'
    
class Hip_CTL( allCtls.AllCtls ):
    mirrorType = 'center'
    mirrorP = 'Root_CTL'
    
class Root_CTL( allCtls.AllCtls ):
    mirrorType = 'center'
    mirrorP = 'Fly_CTL'
    
class Fly_CTL( allCtls.AllCtls ):
    mirrorType = 'center'
    mirrorP = 'Move_CTL'
    transformAttrs = ['pivTx', 'pivTy', 'pivTz', 'pivRx', 'pivRy', 'pivRz' ]
    
class Move_CTL( allCtls.AllCtls ):
    mirrorType = 'center'
    mirrorP = 'World_CTL'