from sgModules import sgcommands
from sgModules import sgbase



def freezeJoint( evt=0 ):
    
    sels = sgcommands.listNodes( sl=1 )
    for sel in sels:
        sgcommands.freezeJoint( sels )



def freezeByParent( evt=0 ):
    
    sels = sgcommands.listNodes( sl=1 )
    sgcommands.freezeByParent( sels )




def setJointOrientZero( evt=0 ):
    
    sels = sgcommands.listNodes( sl=1 )
    for sel in sels:
        if sel.nodeType() != 'joint': continue
        sel.attr( 'jo' ).set( 0,0,0 )



def setCenter( evt=0 ):
    
    sels = sgcommands.listNodes( sl=1 )
    for sel in sels:
        sgcommands.setCenter( sel )



def setMirror( evt=0 ):
    
    sels = sgcommands.listNodes( sl=1 )
    for sel in sels:
        sgcommands.setMirrorLocal( sel )



def setOrientAsTarget( evt=0 ):
    
    sels = sgcommands.listNodes( sl=1 )
    rotValue = sels[-1].xform( q=1, ws=1, ro=1 )[:3]
    for sel in sels[:-1]:
        sel.setOrient( *rotValue, ws=1 )


def setTransformAsTarget( evt=0 ):
    
    sels = sgcommands.listNodes( sl=1 )
    transValue = sels[-1].xform( q=1, ws=1, t=1 )[:3]
    rotValue = sels[-1].xform( q=1, ws=1, ro=1 )[:3]
    for sel in sels[:-1]:
        sel.setPosition( *transValue, ws=1 )
        sel.setOrient( *rotValue, ws=1 )


def setOrientByChild( evt=0 ):
    
    sels = sgcommands.listNodes( sl=1 )
    for sel in sels:
        children = sel.listRelatives( c=1, type='transform' )
        if not children: return None
        print children[0].name()
        sgcommands.lookAt( children[0], sel, pcp=1 )
        
        
        
        