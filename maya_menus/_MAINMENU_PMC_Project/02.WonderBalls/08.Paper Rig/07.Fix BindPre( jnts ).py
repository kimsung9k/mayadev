import pymel.core
sels = pymel.core.ls( sl=1 )
for sel in sels:
    bindPre = pymel.core.ls( sel + '_bindPre' )[0]
    cons = bindPre.wim.listConnections( type='skinCluster', p=1 )
    
    bindPreP = bindPre.getParent()
    bindPrePP = bindPreP.getParent()
    newBindPre = pymel.core.createNode( 'transform' )
    pymel.core.xform( newBindPre, ws=1, matrix= bindPre.wm.get() )
    newBindPre.setParent( bindPrePP )
    
    bindPre.t >> newBindPre.t
    bindPre.r >> newBindPre.r
    bindPre.s >> newBindPre.s
 
    origName = bindPre.name()
    bindPre.rename( 'old_' + origName )
    newBindPre.rename( origName )   
    
    for con in cons:
        newBindPre.wim >> con