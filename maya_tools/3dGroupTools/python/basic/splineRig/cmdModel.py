import maya.cmds as cmds
import ui.view


def addConnectCurve( jnts ):
    
    crv = cmds.curve( p=[[0,0,0] for i in range( len( jnts ) ) ] )
    
    for i in range( len( jnts ) ):
        mmdc = cmds.createNode( 'multMatrixDecompose', n=jnts[i]+'_mmdc' )
        cmds.connectAttr( jnts[i]+'.wm', mmdc+'.i[0]' )
        cmds.connectAttr( crv+'.pim', mmdc+'.i[1]' )
        cmds.connectAttr( mmdc+'.ot', crv+'.cv[%d]' % i )
    
    return crv



def mmAddConnectCurve( *args ):
    
    sels = cmds.ls( sl=1 )
    crv = addConnectCurve( sels )
    cmds.select( crv )



def mmShowCurveInfoSetUI( *args ):
    
    ui.view.CurveInfoSetUI().show()