import pymel.core
sels = pymel.core.listRelatives( pymel.core.ls( sl=1 ), c=1, ad=1, type='transform' )
sels += pymel.core.ls( sl=1 )

shadingEngines = []

for sel in sels:
    selShape = sel.getShape()
    if not selShape: continue
    shadingEngines += selShape.listConnections( s=0, d=1, type='shadingEngine' )

if shadingEngines:
    
    shadingEngines = list( set( shadingEngines ) )
    
    for shadingEngine in shadingEngines:
        cons = shadingEngines[0].surfaceShader.listConnections( s=1, d=0 )
        pymel.core.defaultNavigation( ce=1, source = cons[0], destination = shadingEngines[0].rsSurfaceShader )
        blinn = pymel.core.shadingNode( 'blinn', asShader=1 )
        blinn.outColor >> shadingEngines[0].surfaceShader
        blinn.specularColor.set( 0,0,0 )
        
        attrList = [ 'diffuse_color', 'diffuse', 'facing_color']
        for attr in attrList:
            try:
                colorNodeCon = cons[0].attr( attr ).listConnections( s=1, d=0, p=1 )
                break
            except: continue
        
        if not colorNodeCon: continue
        if colorNodeCon[0].node().nodeType()[:2] != 'Re':
            colorNodeCon[0] >> blinn.attr( 'color' )
        else:
            cons = colorNodeCon[0].node().listConnections( s=1, d=0, p=1 )
            if not cons: continue
            if cons[0].node().nodeType() != 'Re':
                cons[0] >> blinn.attr( 'color' )
                print blinn
            else:
                con_ = cons[0].node().listConnections( s=1, d=0, p=1 )
                con_[0] >> blinn.attr( 'color' )