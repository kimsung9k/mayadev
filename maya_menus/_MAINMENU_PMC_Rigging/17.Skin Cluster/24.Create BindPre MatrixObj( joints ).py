import pymel.core

sels = pymel.core.ls( sl=1 )

for sel in sels:
    tr = pymel.core.createNode( 'transform' )
    tr.dh.set( 1 )
    
    pymel.core.xform( tr, ws=1, matrix= sel.wm.get() )
    
    tr.addAttr( 'bindPre', at='message' )
    sel.message >> tr.bindPre