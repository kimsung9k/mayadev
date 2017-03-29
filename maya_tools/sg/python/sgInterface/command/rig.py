from sgModules import sgcommands
from sgModules import sgbase


def makeMirror( evt=0 ):
    
    sels = sgcommands.listNodes( sl=1 )
    for sel in sels:
        node = sgcommands.createNode( sel.nodeType() )
        node.xform( ws=1, matrix= sel.wm.get() )
        sgcommands.setMirror( node )
        node.rename( sgbase.getOtherSideName( sel.localName() ) )
        node.attr( 'dh' ).set( sel.attr('dh').get() )



def copyRig( evt=0 ):
    
    sels = sgcommands.listNodes( sl=1 )
    sgcommands.copyRig( sels[0], sels[1] )



def reverseAngle( evt=0 ):
    
    for sel in sgcommands.listNodes( sl=1 ):
        sgcommands.setAngleReverse( sel )




def reversePosition( evt=0 ):
    
    for sel in sgcommands.listNodes( sl=1 ):
        tr = sel.t.get()
        sel.t.set( -tr[0], -tr[1], -tr[2] )