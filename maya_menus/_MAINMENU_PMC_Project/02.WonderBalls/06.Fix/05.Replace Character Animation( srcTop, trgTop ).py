import pymel.core
from maya import cmds
sels = pymel.core.ls( sl=1 )

src = sels[0]
trg = sels[1]

srcSplit = src.split( ':' )
trgSplit = trg.split( ':' )
srcNs = ':'.join( srcSplit[:-1] ) + ':'
trgNs = ':'.join( trgSplit[:-1] ) + ':'

srcCtls = pymel.core.ls( srcNs + '*Ctrl', type='transform' )
trgCtls = pymel.core.ls( trgNs + '*Ctrl', type='transform' )

for i in range( len( srcCtls ) ):
    attrs = cmds.listAttr( srcCtls[i].name(), k=1 )
    for attr in attrs:
        cons = srcCtls[i].attr( attr ).listConnections( s=1, d=0, p=1 )
        if not cons: continue
        try:cons[0] >> trgCtls[i].attr( attr )
        except:
            print attr