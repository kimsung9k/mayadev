import maya.cmds as cmds


def getBaseShape( target ):
    
    attrName = 'baseShape'
    if not cmds.attributeQuery( attrName, node=target, ex=1 ):
        cmds.addAttr( target, ln=attrName, at='message' )
    
    baseShapeCons = cmds.listConnections( target+'.'+attrName, s=1, d=0 )
    if not baseShapeCons:
        duTarget = cmds.duplicate( target )[0]
        cmds.connectAttr( duTarget+'.message', target+'.'+attrName )
        cmds.setAttr( duTarget+'.v', 0 )
    else:
        duTarget = baseShapeCons[0]
    
    return cmds.listRelatives( duTarget, s=1 )[0]
        


def makeWire( dropoffDistance ):
    
    sels = cmds.ls( sl=1 )
    
    last = sels[-1]
    lastShape = cmds.listRelatives( last, s=1 )[0]
    baseShape = getBaseShape( last )
    
    for sel in sels[:-1]:
        wireExists = False
        hists = cmds.listHistory( sel, pdo=1 )
        if not hists: hists = []
        for hist in hists:
            if cmds.nodeType( hist ) == 'wire':
                wireExists = True
                break
        if wireExists:
            wire = hist
        else:
            wire = cmds.deformer( sel, type='wire' )[0]
            cmds.connectAttr( baseShape+'.local', wire+'.baseWire[0]' )
            cmds.connectAttr( lastShape+'.local', wire+'.deformedWire[0]' )
        cmds.setAttr( wire+'.dropoffDistance[0]', dropoffDistance )

    cmds.select( sels )