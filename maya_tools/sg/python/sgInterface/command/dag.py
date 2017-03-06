import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
from sgModules import sgcommands
from sgModules import sgobject
from sgModules import sgbase



def putNull( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sgcommands.putObject( sels, 'null' )
    


def putJoint( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sgcommands.putObject( sels, 'joint' )



def putLocator( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sgcommands.putObject( sels, 'locator' )



def putNulls( evt=0 ):
    
    sels = sgcommands.listNodes( sl=1 )
    newObjects = sgcommands.putObject( sels, 'null', 'transform' )
    sgcommands.select( newObjects )


def putJoints( evt=0 ):
    
    sels = sgcommands.listNodes( sl=1 )
    newObjects = sgcommands.putObject( sels, 'joint', 'transform' )
    sgcommands.select( newObjects )



def putLocators( evt=0 ):
    
    sels = sgcommands.listNodes( sl=1 )
    newObjects = sgcommands.putObject( sels, 'locator', 'transform' )
    sgcommands.select( newObjects )




def putAndConstraintJoints( evt=0 ):
    
    sels = sgcommands.listNodes( sl=1 )
    newObjects = []
    for sel in sels:
        newObject = sgcommands.putObject( [sel], 'joint', 'transform' )[0]
        sgcommands.constrain_parent( sel, newObject )
        newObjects.append( newObject )
    sgcommands.select( newObjects )




def putChild( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    
    for sel in sels:
        putTarget = sgcommands.putObject( [sel], 'transform' )
        putTarget = cmds.parent( putTarget, sel )[0]
        
        selName = sel.split('|')[-1]
        childName = ''
        if selName[-1] == '_':
            childName = sel.split('|')[-1] + 'child'
        else:
            childName = sel.split('|')[-1] + '_child'
            
        putTarget = cmds.rename( putTarget, childName )
        



def putChildJoint( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    
    for sel in sels:
        putTarget = sgcommands.putObject( [sel], 'joint' )
        putTarget = cmds.parent( putTarget, sel )
        
        selName = sel.split('|')[-1]
        childName = ''
        if selName[-1] == '_':
            childName = sel.split('|')[-1] + 'child'
        else:
            childName = sel.split('|')[-1] + '_child'
            
        putTarget = cmds.rename( putTarget, childName )




def putChildLocator( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    
    for sel in sels:
        putTarget = sgcommands.putObject( [sel], 'locator' )
        putTarget = cmds.parent( putTarget, sel )
        
        selName = sel.split('|')[-1]
        childName = ''
        if selName[-1] == '_':
            childName = sel.split('|')[-1] + 'child'
        else:
            childName = sel.split('|')[-1] + '_child'
            
        putTarget = cmds.rename( putTarget, childName )



def renameOtherSide( evt=0 ):
    
    sels = sgcommands.listNodes( sl=1 )
    
    if sels[0].name().find( '_L_' ) != -1:
        sels[1].rename( sels[0].localName().replace( '_L_', '_R_' ) )
    elif sels[0].name().find( '_R_' ) != -1:
        sels[1].rename( sels[0].localName().replace( '_R_', '_L_' ) )



def renameParent( evt=0 ):
    
    sels = sgcommands.listNodes( sl=1 )
    for sel in sels:
        selP = sel.parent()
        if not selP: continue
        selP.rename( 'P' + sel.localName() )



def makeParent( evt=0 ):
    
    sels = sgcommands.listNodes( sl=1 )
    for sel in sels:
        selP = sel.parent()
        transform = sgcommands.createNode( 'transform', n= 'P'+ sel.localName() )
        if selP:
            sgcommands.parent( transform, selP )
        transform.xform( ws=1, matrix= sel.wm.get() )
        sgcommands.parent( sel, transform )
            



def parentSelectedOlder( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    
    for i in range( len( sels ) -1 ):
        sels[i] = cmds.parent( sels[i], sels[i+1] )[0]
        if cmds.nodeType( sels[i] ) == 'joint':
            cmds.setAttr( sels[i] + '.jo', 0,0,0 )




def copyChildren( evt=0 ):
    
    sels = sgcommands.listNodes( sl=1 )
    sgcommands.copyChildren( sels[0], sels[1] )
    


