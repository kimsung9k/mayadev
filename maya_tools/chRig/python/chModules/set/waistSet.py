import maya.cmds as cmds

def addDecompose( sels ):
    dcmps = []
    for sel in sels:
        dcmp = cmds.createNode( 'decomposeMatrix' , n=sel+'_dcmp' )
        cmds.connectAttr( sel+'.wm', dcmp+'.imat' )
        dcmps.append( dcmp )
    return dcmps

def connectPointToEpBindNode( dcmps, epNode ):
    for i in range( len( dcmps ) ):
        cmds.connectAttr( dcmps[i]+'.ot', epNode+'.ip[%d]' % i )
        
def epNodeToCurve( epNode ):
    crvNode = cmds.createNode( 'nurbsCurve' )
    cmds.connectAttr( epNode+'.outputCurve', crvNode+'.create')
        
sels =cmds.ls( sl=1 )

jnts = sels[:-1]
epNode = sels[-1]
dcmps = addDecompose( jnts )

connectPointToEpBindNode( dcmps, epNode )

epNodeToCurve( epNode )