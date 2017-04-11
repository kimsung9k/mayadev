import maya.cmds as cmds


def getKeyAttrConnectedChildren( topObj ):
    
    children = cmds.listRelatives( topObj, c=1, ad=1, f=1 )
    children.append( topObj )
    
    targetChildren = []
    targetCons = []
    for child in children:
        if not cmds.nodeType( child ) in ['joint', 'transform']: continue
        listAttrs = cmds.listAttr( child, k=1 )
        for attr in listAttrs:
            cons = cmds.listConnections( child+'.'+ attr, s=1, d=0 )
            if cons:
                targetChildren.append( child )
                targetCons += cons
            else:
                parentAttrs = cmds.attributeQuery( attr, node=child, listParent = 1 )
                if parentAttrs:
                    cons= cmds.listConnections( child+'.'+parentAttrs[0], s=1, d=0 )
                    if cons:
                        targetChildren.append( child )
                        targetCons += cons
    
    targetChildren = list( set( targetChildren ) )
    targetCons = list( set( targetCons ) )
    return targetChildren, targetCons