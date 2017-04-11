import chModules.driverSet.drvSetInfo as drvSetInfo
import chModules.driverSet.constSet as constSet
import chModules.driverSet.bjtDriverSet as bjtDrvSet
import maya.cmds as cmds



def getTargetCls():

    targetCls = []
    for i in dir( drvSetInfo ):
        if i.find( '_DRV' ):
            targetCls.append( i )
    
    return targetCls



def isConnected( bjtWorld ):
    
    children = cmds.listRelatives( bjtWorld, c=1, ad=1, type='joint' )
    
    for child in children:
        dcmpCons = cmds.listConnections( child, s=1, d=0, type='multMatrixDecompose' )
        
        if not dcmpCons: continue
        
        constCons = cmds.listConnections( dcmpCons[0]+'.matrixIn[0]' )
        
        if constCons:
            if child.replace( '_BJT', '_CONST' ) == constCons[0]:
                return True
        else:
            continue

    return False



def buildDrvJoints( ns='' ):
    
    targetCls = getTargetCls()
    
    cmds.createNode( 'transform', n= ns+'DRV_JNT_GRP')
    
    for target in targetCls:
        
        if target.find( '_DRV' ) == -1: continue
        
        poseTarget =None
        exec( "poseTarget = drvSetInfo.%s.poseTarget" % target )
        
        poseTarget = poseTarget.replace( 'LAST', '*' )
        
        poseTargetList = []
        
        if poseTarget.find( '_SIDE_' ) != -1:
            left  = poseTarget.replace( '_SIDE_', '_L_' )
            right = poseTarget.replace( '_SIDE_', '_R_' )
            poseTargetList += [ left, right ]
        else:
            poseTargetList.append( poseTarget )
            
        for i in range( len( poseTargetList ) ):
            
            if poseTargetList[i].find( 'ENUM' ) != -1:
                targetSels= poseTargetList[i].replace( 'ENUM', '*' )
                targetSels = cmds.ls( targetSels )
                poseTargetList[i] = targetSels[-1]
        
        for i in range( len( poseTargetList ) ):
            poseTargetList[i] = cmds.ls( poseTargetList[i], type='joint' )[-1]
            
        if len( poseTargetList ) == 2:
            left = target.replace( '_SIDE_', '_L_' )
            right = target.replace( '_SIDE_', '_R_' )
            
            left = cmds.createNode( 'joint', n=left )
            right = cmds.createNode( 'joint', n=right )
            
            leftMtx = cmds.getAttr( poseTargetList[0]+'.wm' )
            rightMtx = cmds.getAttr( poseTargetList[1]+'.wm' )
            
            cmds.xform( left, matrix=leftMtx )
            cmds.xform( right, matrix=rightMtx )
            
            cmds.setAttr( left +'.radius', cmds.getAttr( poseTargetList[0]+'.radius' )*1.5 )
            cmds.setAttr( right+'.radius', cmds.getAttr( poseTargetList[1]+'.radius' )*1.5 )
            
        else:
            center = cmds.createNode( 'joint', n=target )
            mtx = cmds.getAttr( poseTargetList[0]+'.wm' )
            rad = cmds.getAttr( poseTargetList[0]+'.radius' )
            cmds.xform( center, matrix=mtx )
            cmds.setAttr( center+'.radius', rad*1.5 )
            
            
    for target in targetCls:
        
        if target.find( '_DRV' ) == -1: continue
        
        parentTarget =None
        exec( "parentTarget = drvSetInfo.%s.parent" % target )
        
        parentTargetList = []
        
        if parentTarget.find( '_SIDE_' ) != -1:
            left  = parentTarget.replace( '_SIDE_', '_L_' )
            right = parentTarget.replace( '_SIDE_', '_R_' )
            parentTargetList += [ left, right ]
        else:
            parentTargetList.append( parentTarget )
        
        if len( parentTargetList ) == 2:
            left = target.replace( '_SIDE_', '_L_' )
            right = target.replace( '_SIDE_', '_R_' )
            
            wmL = cmds.getAttr( left+'.wm' )
            wmR = cmds.getAttr( right+'.wm' )
            
            cmds.parent( left,  parentTargetList[0], r=1 )
            cmds.parent( right, parentTargetList[1], r=1 )
            
            cmds.xform( left , ws=1, matrix=wmL )
            cmds.xform( right, ws=1, matrix=wmR )
        else:
            if target.find( '_SIDE_' ) != -1:
                left = target.replace( '_SIDE_', '_L_' )
                right = target.replace( '_SIDE_', '_R_' )
                
                wmL = cmds.getAttr( left+'.wm' )
                wmR = cmds.getAttr( right+'.wm' )
                
                cmds.parent( left, right, parentTargetList[0], r=1 )
                
                cmds.xform( left , ws=1, matrix=wmL )
                cmds.xform( right, ws=1, matrix=wmR )
            else:
                wm = cmds.getAttr( target+'.wm' )
                cmds.parent( target, parentTargetList[0], r=1 )
                cmds.xform( target, ws=1, matrix=wm )
                
                
def freezDRV( ns='' ):
    
    consts = cmds.ls( ns+'*_DRV' )

    for const in consts:
        
        rValue = cmds.getAttr( const+'.r' )[0]
        
        cmds.setAttr( const+'.r', 0,0,0 )
        cmds.setAttr( const+'.jo', *rValue )
    
    for const in consts:
        cmds.setAttr( const+'.t', lock=1, cb=0 )
        cmds.setAttr( const+'.s', lock=1, cb=0 )
        cmds.setAttr( const+'.v', lock=1, cb=0 )

                

def setConnect( ns='', *args ):
    
    buildDrvJoints()
    
    constSet.Hip_SIDE_DRV()
    constSet.Knee_SIDE_DRV()
    constSet.Ankle_SIDE_DRV()
    constSet.Ball_SIDE_DRV()
    constSet.BodyRot_DRV()
    constSet.Chest_DRV()
    constSet.Neck_DRV()
    constSet.Head_DRV()
    constSet.Collar_SIDE_DRV()
    constSet.Shoulder_SIDE_DRV()
    constSet.Elbow_SIDE_DRV()
    constSet.Hand_SIDE_DRV()
    
    constSet.constConnect()
    freezDRV()
    

def setDisconnect( ns='', *args ):
    
    drvs = cmds.ls( ns+'*_DRV', type='joint' )
    
    for drv in drvs:
        cmds.setAttr( drv+'.r', 0,0,0 )
    
    bjts = cmds.ls( ns+'*_BJT' )
    
    for bjt in bjts:
        joValues = cmds.getAttr( bjt+'.jo' )[0]
        mtxDcmpCons = cmds.listConnections( bjt+'.jo', type='multMatrixDecompose' )
        
        if mtxDcmpCons:
            cmds.delete( mtxDcmpCons )
            
        cmds.setAttr( bjt+'.jo', *joValues )
            
    cmds.delete( ns+'DRV_JNT_GRP' )
    
    
            
            
def bjtDriverSet( ns='', *args ):
    
    bjtDrvSet.UpperSplineSet( ns+'Arm_SIDE_Upper0_BJT', ns+'Arm_SIDE_Lower0_BJT' )
    bjtDrvSet.UpperSplineSet( ns+'Leg_SIDE_Upper0_BJT', ns+'Leg_SIDE_Lower0_BJT' )
    bjtDrvSet.MiddleSplineSet( ns+'Arm_SIDE_Lower0_BJT' )
    bjtDrvSet.MiddleSplineSet( ns+'Leg_SIDE_Lower0_BJT' )
    bjtDrvSet.LowerSplineSet( ns+'Arm_SIDE_Lower0_BJT', ns+'Arm_SIDE_LowerLAST_BJT' )
    bjtDrvSet.LowerSplineSet( ns+'Leg_SIDE_Lower0_BJT', ns+'Leg_SIDE_LowerLAST_BJT' )
    
    bjtDrvSet.BodyLineSet( ns+'SplineNUM_BJT' )
    bjtDrvSet.DirectSet( ns+'Collar0_SIDE_BJT' )
    bjtDrvSet.DirectSet( ns+'Leg_SIDE_Foot0_BJT' )
    bjtDrvSet.DirectSet( ns+'SplineENDNUM_BJT' )
    bjtDrvSet.DirectSet( ns+'Neck_Spline0_BJT' )
    bjtDrvSet.DirectSet( ns+'Neck_Spline3_BJT' )