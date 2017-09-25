import pymel.core
sels = pymel.core.ls( sl=1 )
selAttrs = pymel.core.channelBox( 'mainChannelBox', q=1, sma=1 )
targets = []
for sel in sels:
    for attr in selAttrs:
        targets += sel.attr( attr ).listConnections( s=0, d=1 )
pymel.core.select( targets )