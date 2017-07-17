import pymel.core
for sel in pymel.core.ls( sl=1 ):
    pconst = sel.getParent().listConnections( s=1, d=0, type='parentConstraint' )
    pymel.core.delete( pconst )