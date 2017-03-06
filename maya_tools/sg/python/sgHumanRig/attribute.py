import maya.OpenMaya as OpenMaya
import maya.cmds as cmds
from sgModules import sgbase


def addAttr( target, **options ):
    
    items = options.items()
    
    attrName = ''
    channelBox = False
    keyable = False
    for key, value in items:
        if key in ['ln', 'longName']:
            attrName = value
        elif key in ['cb', 'channelBox']:
            channelBox = True
            options.pop( key )
        elif key in ['k', 'keyable']:
            keyable = True 
            options.pop( key )
    
    if cmds.attributeQuery( attrName, node=target, ex=1 ): return None
    
    cmds.addAttr( target, **options )
    
    if channelBox:
        cmds.setAttr( target+'.'+attrName, e=1, cb=1 )
    elif keyable:
        cmds.setAttr( target+'.'+attrName, e=1, k=1 )
        

def removeMultiInstances( nodeAttrName ):
    
    attrs = cmds.ls( nodeAttrName + '[*]' )
    
    for attr in attrs:
        if not cmds.listConnections( attr, s=1, d=0 ):
            cmds.removeMultiInstance( attr )


def getLastElementIndex( fullAttr ):
    
    splits = fullAttr.split( '.' )
    node = splits[0]
    attr = '.'.join( splits[1:] )
    
    fnNode = OpenMaya.MFnDependencyNode( sgbase.getMObject( node ) )
    plugAttr = fnNode.findPlug( attr )
    
    return plugAttr[plugAttr.numElements()-1].logicalIndex()
    


def getOutputMatrixAttributeFromNode( node ):
    
    if cmds.nodeType( node ) == 'composeMatrix':
        return node + '.outputMatrix'
    if cmds.nodeType( node ) in ['multMatrix', 'wtAddMatrix']:
        return node + '.matrixSum'
    if cmds.nodeType( node ) in ['transform', 'joint']:
        return node + '.wm'


def getOutputMatrixInvAttributeFromNode( node ):
    
    if cmds.nodeType( node ) == 'composeMatrix':
        attr = node + '.outputMatrix'
    elif cmds.nodeType( node ) in ['multMatrix', 'wtAddMatrix']:
        attr = node + '.matrixSum'
    if cmds.nodeType( node ) in ['transform', 'joint']:
        return node + '.wim'

    invMtx = cmds.createNode( 'inverseMatrix' )
    cmds.connectAttr( attr, invMtx + '.inputMatrix' )
    
    return invMtx + '.outputMatrix'




