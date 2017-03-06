import maya.cmds as cmds



def mmPutNull( *args ):
    sels = cmds.ls( sl=1 )
    
    grps = []
    for sel in sels:
        mtx = cmds.getAttr( sel+'.wm' )
        trObj = cmds.createNode( 'transform', n=sel+'_putObj' )
        cmds.xform( trObj, ws=1, matrix=mtx )
        grps.append( trObj )
    
    return grps



def mmPutJoint( *args ):
    
    sels = cmds.ls( sl=1 )
    
    grps = []
    for sel in sels:
        mtx = cmds.getAttr( sel+'.wm' )
        trObj = cmds.createNode( 'joint', n=sel+'_putObj' )
        cmds.xform( trObj, ws=1, matrix=mtx )
        grps.append( trObj )
    
    return grps




def mmPutChild( *args ):
    sels = cmds.ls( sl=1 )
    
    targets = []
    for sel in sels:
        if not cmds.ls( sel+'.translateX' ): continue
        trNode = cmds.createNode( 'transform' )
        trNode = cmds.parent( trNode, sel )
        if sel.find( '_GRP' ) != -1:
            trNode = cmds.rename( trNode, sel.replace( '_GRP', '' ) )
        else:
            trNode = cmds.rename( trNode, sel + '_child' )
        cmds.setAttr( trNode+'.t', 0,0,0 )
        cmds.setAttr( trNode+'.r', 0,0,0 )
        targets.append( trNode )
    cmds.select( targets )
    



def mmPutChildJoint( *args ):
    sels = cmds.ls( sl=1 )
    
    targets = []
    for sel in sels:
        if not cmds.ls( sel+'.translateX' ): continue
        cmds.select( sel )
        trNode = cmds.joint()
        if sel.find( '_GRP' ) != -1:
            trNode = cmds.rename( trNode, sel.replace( '_GRP', '' ) )
        cmds.setAttr( trNode+'.t', 0,0,0 )
        cmds.setAttr( trNode+'.jo', 0,0,0 )
        targets.append( trNode )
    cmds.select( targets )
    
    
    

def putJointBBC( target, typ='joint' ):
    
    bbmin = cmds.getAttr( target + '.boundingBoxMin' )[0]
    bbmax = cmds.getAttr( target + '.boundingBoxMax' )[0]
    
    bbcenter = []
    for i in range( 3 ):
        bbcenter.append( (bbmin[i] + bbmax[i])/2.0 )
    
    if typ == 'joint':
        jnt = cmds.createNode( 'joint' )
        cmds.setAttr( jnt+'.t', *bbcenter )
        return jnt
    else:
        trNode = cmds.createNode( 'transform' )
        cmds.setAttr( trNode+'.t', *bbcenter )
        return trNode
    


def mmPutJointBBC( *args ):
    
    sels = cmds.ls( sl=1 )
    if not sels: return None
    
    jnts = []
    for target in sels:
        
        if not cmds.ls( target+'.translateX' ): continue
        
        jnt = putJointBBC( target )
        jnts.append( jnt )
    
    cmds.select( jnts )
    
    
    
def mmPutNullBBC( *args ):
    
    sels = cmds.ls( sl=1 )
    if not sels: return None
    
    jnts = []
    for target in sels:
        
        if not cmds.ls( target+'.translateX' ): continue
        
        jnt = putJointBBC( target, 'transform' )
        jnts.append( jnt )
    
    cmds.select( jnts )