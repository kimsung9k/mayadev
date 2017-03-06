from maya import cmds
from sgModules import sgcommands

sels = cmds.ls( sl=1 )

for sel in sels:
    attrs = cmds.channelBox( 'mainChannelBox', q=1, sma=1 )
    for attr in attrs:
        sgcommands.addMultDoubleLinearConnection( sel, attr )

cmds.select( sels )