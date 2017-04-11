import maya.cmds as cmds
import sgRigConnection
import sgFunctionSet
import sgFunctionDag



def createControlInJointLine( topJnt ):
    
    jnts = cmds.listRelatives( topJnt, c=1, ad=1, type='joint' )
    jnts.append( topJnt )
    
    jnts.reverse()
    
    
    topCtl = cmds.circle()[0]
    sgFunctionSet.goToObject( topCtl, jnts[0] )
    pTopCtl = sgFunctionDag.makeParent( topCtl )
    sgRigConnection.constraint( jnts[0], pTopCtl )
    
    for i in range( 0, len( jnts )-2, 2 ):
        first = jnts[i]
        second = jnts[i+2]
        middle = jnts[i+1]
        
        middleObj = cmds.createNode( 'transform' )
        sgFunctionSet.goToObject( middleObj, middle )
        
        ctl = cmds.circle()[0]
        sgFunctionSet.goToObject( ctl, second )
        pCtl = sgFunctionDag.makeParent( ctl )
        sgRigConnection.constraint( second, pCtl )
        
        cmds.select( first, second, middleObj )
        firstChildren, secondChildren = sgRigConnection.mc_connectBlendTwoMatrix_keepPositionAndSkipSecondTrans()




def createSplineCurveInfo( curve, number, **options ):
    
    crvShape = cmds.listRelatives( curve, s=1 )
    if not crvShape: return None
    crvShape = crvShape[0]
    
    splineNode = cmds.createNode( 'splineCurveInfo', n=curve+'_spline' )
    cmds.connectAttr( crvShape+'.local', splineNode+'.inputCurve' )
    
    if number <= 1:
        return None
    elif number > 1:
        eachRate = 1.0/(number-1)
        for i in range( number ):
            cmds.setAttr( splineNode+'.parameter[%d]' % i, eachRate*i+0.001 )
            
    for i in range( number-1 ):
        trNode = cmds.createNode( 'transform' )
        cmds.connectAttr( splineNode+'.output[%d].position' % i, trNode+'.t' )
        cmds.connectAttr( splineNode+'.output[%d].rotate' % i, trNode+'.r' )
        cmds.parent( trNode, curve )
        cmds.setAttr( trNode+'.dh', 1 )
        cmds.setAttr( trNode+'.dla', 1 )
    
    return splineNode




def mc_createControlInJointLine( *args ):
    
    sels = cmds.ls( sl=1 )
    
    for sel in sels:
        createControlInJointLine( sel )