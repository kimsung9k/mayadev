from chModules import basecode


class AllCtls( object ):
    mirrorAxis = 'x'
    mirrorType = 'object'
    transformAttrs = []


class CtlsHierarchy( basecode.CtlItemBase ):
    World = ['Move']
    Move = ['Fly']
    Fly  = ['Root']
    Root = ['TorsoRotate','Hip']
    Hip  = ['Leg__FK0', 'Leg__IK','Leg__PoleV','Leg__Switch']
    Leg__Switch = ['Leg__UpperFlex','Leg__LowerFlex']
    Leg__FK0 = ['Leg__FK1']
    Leg__FK1 = ['Leg__FK2']
    Leg__FK2 = ['Leg__FK3']
    Leg__IK  = ['Leg__Foot_IK','Leg__IkItp']
    
    TorsoRotate = ['Chest']
    Chest = ['ChestMove', 'Waist']
    ChestMove = ['Collar__','Neck']
    Waist = ['WaistItp1']
    Neck  = ['NeckMiddle', 'Head']
    Head  = ['Eye']
    Eye   = ['EyeAim__']
    
    Collar__ = ['Shoulder__']
    Shoulder__  = ['Arm__FK0', 'Arm__IK','Arm__PoleV','Arm__Switch']
    Arm__Switch = ['Arm__UpperFlex','Arm__LowerFlex']
    Arm__FK0 = ['Arm__FK1']
    Arm__FK1 = ['Arm__FK2']
    Arm__FK2 = ['Thumb0__','Index0__','Middle0__','Ring0__','Pinky0__']
    Arm__IK  = ['Arm__IkItp','Thumb0__','Index0__','Middle0__','Ring0__','Pinky0__']
    Thumb0__ = ['Thumb1__']
    Thumb1__ = ['Thumb2__']
    Index0__ = ['Index1__']
    Index1__ = ['Index2__']
    Index2__ = ['Index3__']
    Middle0__ = ['Middle1__']
    Middle1__ = ['Middle2__']
    Middle2__ = ['Middle3__']
    Ring0__ = ['Ring1__']
    Ring1__ = ['Ring2__']
    Ring2__ = ['Ring3__']
    Pinky0__ = ['Pinky1__']
    Pinky1__ = ['Pinky2__']
    Pinky2__ = ['Pinky3__']
    

    def getHierarchy(self, target ):
        returnList = []
        def doIt( target ):
            if target in returnList:
                return []
            returnList.append( target )
            
            sideName = ''
            if target.find( '_L_' ) != -1:
                sideName = '_L_'
            elif target.find( '_R_' ) != -1:
                sideName = '_R_'
                
            itemName = target.replace( '_L_', '__' ).replace( '_R_', '__' ).replace( 'CTL', '' )
            if itemName[-2] != '_' and itemName[-1] == '_':
                itemName = itemName[:-1]
            
            try:
                items = self.getItemIndex( itemName )
            except: return []
            
            children = []
            
            for item in items:
                if not sideName:
                    item1 = item.replace( '__', '_L_' )
                    item2 = item.replace( '__', '_R_' )
                    if item1[-1] == '_':
                        children += [item1+'CTL', item2+'CTL']
                    else:
                        children += [item1+'_CTL', item2+'_CTL']
                else:
                    item = item.replace( '__', sideName )
                    if item[-1] == '_':
                        children.append( item +'CTL' )
                    else:
                        children.append( item +'_CTL')

            if children:
                for child in children:
                    doIt( child )
        doIt( target )
        returnList.remove( target )
        
        return returnList