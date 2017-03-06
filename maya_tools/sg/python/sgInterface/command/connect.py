from sgModules import sgcommands
import maya.cmds as cmds


def lookAt( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sgcommands.lookAtConnect( sels[0], sels[1] )
    


def getBlendTwoMatrixNode( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sgcommands.getBlendTwoMatrixNode(sels[0], sels[1])



def setBlendTwoMatrixConnection( evt=0 ):
    
    sels = sgcommands.listNodes( sl=1 )
    wtAddMtx = sgcommands.getBlendTwoMatrixNode( sels[0], sels[1] )
    mm = sgcommands.createNode( 'multMatrix' )
    dcmp = sgcommands.getDecomposeMatrix( mm )
    wtAddMtx.matrixSum >> mm.i[0]
    sels[2].pim >> mm.i[1]
    dcmp.ot >> sels[2].t
    dcmp.outputRotate >> sels[2].r



def addBlendMatrix( evt=0 ):
    sgcommands.addBlendMatrix( *cmds.ls( sl=1 ) )


def addBlendMatrix_mo( evt=0 ):
    sgcommands.addBlendMatrix( *cmds.ls( sl=1 ), mo=1 )



def constrain_point( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sgcommands.constrain_point( sels[0], sels[1] )
    
    

def constrain_orient( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sgcommands.constrain_rotate( sels[0], sels[1] )
    


def constrain_parent( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sgcommands.constrain_parent( sels[0], sels[1] )



def opptimizeConnection( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    for sel in sels:
        sgcommands.opptimizeConnection( sel )



def getLocalMatrix( evt=-0 ):
    
    sels = cmds.ls( sl=1 )
    node = sgcommands.getLocalMatrix( sels[0], sels[1] )
    sgcommands.select( node )


def getLocalMatrixDecompose( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    node = sgcommands.getLocalMatrix( sels[0], sels[1] )
    dcmp = sgcommands.getDecomposeMatrix(node)
    sgcommands.select( dcmp )




def getDecomposeMatrix( evt=0 ):
    
    sels = sgcommands.listNodes( sl=1 )
    nodes = []
    for sel in sels:
        node = sgcommands.getDecomposeMatrix( sel )
        nodes.append( node )
    sgcommands.select( nodes )




def getLocalDecomposeMatrix( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    localMatrix = sgcommands.getLocalMatrix( sels[0], sels[1] )
    return sgcommands.getDecomposeMatrix( localMatrix )




def getLookAtMatrix( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    lookAtMatrix = sgcommands.getLookAtMatrix( sels[0], sels[1] )
    sgcommands.select( lookAtMatrix )



def getDistance( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    distNodes = []
    for sel in sels:
        distNode = sgcommands.getDistance( sel )
        distNodes.append( distNode )
    sgcommands.select( distNodes )



def getAngle( evt=0 ):
    
    sels = sgcommands.listNodes( sl=1 )
    angleNodes = []
    for sel in sels:
        angleNode = sgcommands.getAngle( sel )
        angleNodes.append( angleNode )
    sgcommands.select( angleNodes )



def getRotationMatrix( evt=0 ):
    
    sels = sgcommands.listNodes( sl=1 )
    mtxNode = sgcommands.getFbfMatrix( sels[0], sels[1], sels[2] )
    sgcommands.select( mtxNode )



def getCrossVectorNode( evt=0 ):
    
    sels = sgcommands.listNodes( sl=1 )
    crossVectorNode = sgcommands.getCrossVectorNode( sels[0], sels[1] )
    sgcommands.select( crossVectorNode )



def replaceConnection( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    
    if len( sels ) < 3: return None
    
    first = sels[0]
    second = sels[1]
    third = sels[2]
    
    sgcommands.replaceConnection( first, second, third )



def getSourceConnection( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    
    if len( sels ) < 2: return None
    
    targets = sels[:-1]
    src = sels[-1]
    
    sgcommands.getSourceConnection( targets, src )


