import maya.cmds as cmds

chAttrs = cmds.channelBox( 'mainChannelBox', q=1, sma=1 )
exString =''

for attr in chAttrs:
    sels = cmds.ls( sl=1 )

    allAttrs = []
    for sel in sels:
        attr = sel + '.' + attr
        allAttrs.append( attr )
    
    for attr in allAttrs:
        exString += attr + " = frame;\n"
    
cmds.expression( s=exString, ae=1, uc='all' )