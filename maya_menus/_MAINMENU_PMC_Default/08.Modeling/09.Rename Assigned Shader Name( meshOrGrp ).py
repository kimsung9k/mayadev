import maya.cmds as cmds

def getSourceList( target ):
    srcCons = cmds.listConnections( target, s=1, d=0 )
    if not srcCons: return []
    srcCons = list( set( srcCons ) )
    returns = [target]
    for srcCon in srcCons:
        if cmds.attributeQuery( 'worldMatrix', node=srcCon, ex=1 ): continue
        returns += getSourceList( srcCon )
        returns = list( set( returns ) )
    return returns

def renameShader( targetObj ):
    
    targetName = targetObj.split( '|' )[-1]
    if cmds.nodeType( targetObj ) == 'transform':
        targetShapes = cmds.listRelatives( targetObj, s=1, f=1 )
        if not targetShapes:targetShapes = []
    else:
        targetShapes = [targetObj]
    
    for targetShape in targetShapes:   
        if cmds.getAttr( targetShape + '.io' ): continue 
        engines = cmds.listConnections( targetShape, s=0, d=1, type='shadingEngine' )
        if not engines: continue
        engines = list( set( engines ) )
        for engine in engines:
            srcNodes = getSourceList( engine )
            if not srcNodes: continue
            for srcNode in srcNodes:
                print srcNode
                typeName = cmds.nodeType( srcNode )
                surfShader = cmds.rename( srcNode, targetName + '_' + typeName )
            if cmds.objExists( engine ):
                try:engine = cmds.rename( engine, targetName + '_shadingEngine' )
                except:pass


sels = cmds.ls( sl=1 )
selChildren = cmds.listRelatives( sels, c=1, ad=1, type='shape', f=1 )
if not selChildren: selChildren = []
selChildren += sels

children = []
for child in selChildren:
    childP = cmds.listRelatives( child, p=1, f=1 )
    if not childP: continue
    if not childP[0] in children:
        children.append( childP[0] )

for child in children:
    renameShader( child )