import pymel.core

sels = pymel.core.ls( type='mesh' )
targets = []
for sel in sels:
    blendShapes = sel.listConnections( s=0, d=1, type='blendShape' )
    if not blendShapes: continue
    if sel.listConnections( s=1, d=0 ): continue
    targets.append( sel.getParent() )
pymel.core.delete( targets )