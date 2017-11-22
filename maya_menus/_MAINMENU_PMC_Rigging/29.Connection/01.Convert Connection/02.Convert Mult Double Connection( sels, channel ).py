from maya import cmds
from sgMaya import sgCmds

sels = cmds.ls( sl=1 )

for sel in sels:
    attrs1 = cmds.channelBox( 'mainChannelBox', q=1, sma=1 )
    attrs2 = cmds.channelBox( 'mainChannelBox', q=1, sha=1 )
    attrs3 = cmds.channelBox( 'mainChannelBox', q=1, ssa=1 )
    
    attrs = []
    if attrs1: attrs += attrs1
    if attrs2: attrs += attrs2
    if attrs3: attrs += attrs3
    
    for attr in attrs:
        sgCmds.addMultDoubleLinearConnection( sel, attr )

cmds.select( sels )