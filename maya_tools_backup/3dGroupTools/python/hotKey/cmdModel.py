import maya.cmds as cmds



def setDefaultValue( **options ):
    
    sels = cmds.ls( sl=1 )
    
    trEnable = False
    roEnable = False
    sEnable  = False
    allEnable = False
    
    items = options.items()
    
    for key, value in items:
        if key in ['t', 'translate']: trEnable = value
        elif key in ['r', 'rotate' ]: roEnable = value
        elif key in ['s', 'scale']:   sEnable  = value
        elif key in ['a', 'all']:     allEnable = value

    listAttrs = []
    if trEnable:
        listAttrs = ['tx', 'ty', 'tz']
    elif roEnable:
        listAttrs = ['rx','ry','rz']
    elif sEnable:
        listAttrs = ['sx', 'sy', 'sz' ]
    
    for sel in sels:
        if not cmds.nodeType( sel ) in ['joint', 'transform']: continue
        for attr in listAttrs:
            isLock = cmds.getAttr( sel+'.'+attr, lock=1 )
            if isLock: continue
            dv = cmds.attributeQuery( attr, node=sel, ld=1 )[0]
            cmds.setAttr( sel+'.'+attr, dv )
            
    if allEnable:
        for sel in sels:
            listAttrs = cmds.listAttr( sel, k=1 )
            for attr in listAttrs:
                isLock = cmds.getAttr( sel+'.'+attr, lock=1 )
                if isLock: continue
                dv = cmds.attributeQuery( attr, node=sel, ld=1 )[0]
                cmds.setAttr( sel+'.'+attr, dv )
                
                
                
def lockSelected():
    
    sels = cmds.ls( sl=1 )
    
    channels = cmds.channelBox( 'mainChannelBox', q=1, sma=1 )
    
    for channel in channels:
        for sel in sels:
            if not cmds.getAttr( sel+'.'+channel, lock=1 ):
                cmds.setAttr( sel+'.'+channel, e=1, lock=True )
            else:
                cmds.setAttr( sel+'.'+channel, e=1, lock=False )
            
            
def hideSelected():
    
    sels = cmds.ls( sl=1 )
    
    channels = cmds.channelBox( 'mainChannelBox', q=1, sma=1 )
    
    for channel in channels:
        for sel in sels:
            cmds.setAttr( sel+'.'+channel, e=1, k=0, cb=0 )
        