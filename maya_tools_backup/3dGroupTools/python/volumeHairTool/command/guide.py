import maya.cmds as cmds


def getAllChildren( sels ):
    
    allShapes = cmds.listRelatives( sels, ad=1, s=1, f=1 )
    allTransforms = cmds.listRelatives( sels, ad=1, c=1, f=1 )
    
    returnChildren = []
    
    if allShapes:
        for shape in allShapes:
            if cmds.getAttr( shape+'.io' ) == False:
                returnChildren.append( shape )
    
    for tr in allTransforms:
        shapes = cmds.listRelatives( tr, s=1 )
        
        if not shapes:
            continue
        else:
            for shape in shapes:
                if cmds.getAttr( shape+'.io' ) == False:
                    returnChildren.append( shape )
    
    return returnChildren


def attrNameToDisplayName( name ):
    
    rename = name[0].upper()
    for char in name[1:]:
        if char.isupper():
            rename += ' '+char
        else:
            rename += char
    
    return rename