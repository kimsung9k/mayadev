import pymel.core

colorCtls = pymel.core.ls( sl=1 )

rgbCtls = []
for colorCtl in colorCtls:
    children = colorCtl.listRelatives( c=1, type='transform' )
    transforms = []
    for child in children:
        if child.listRelatives( s=1 ): continue
        transforms.append( child )
    
    if not len( transforms ) == 3: continue
    ctls = []
    for transform in transforms:
        cTransform = transform.listRelatives( c=1, type='transform' )
        if not cTransform: continue
        ctls.append( cTransform[0] )
    
    if not len( ctls ) == 3: continue
    
    rValue = ctls[0].tx.get()
    gValue = ctls[1].tx.get()
    bValue = ctls[2].tx.get()
    
    rgbCtls.append( ctls )

if rgbCtls:
    
    cmds.colorEditor( rgb=[rValue, gValue, bValue] )
    
    if cmds.colorEditor(query=True, result=True):
        rValue, gValue, bValue = cmds.colorEditor( q=1, rgb=1 )
        
        for rCtl, gCtl, bCtl in rgbCtls:
            rCtl.tx.set( rValue )
            gCtl.tx.set( gValue )
            bCtl.tx.set( bValue )

else:
    cmds.warning( "Select rgb controller" )