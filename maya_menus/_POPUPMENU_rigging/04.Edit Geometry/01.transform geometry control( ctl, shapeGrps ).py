from sgModules import sgcommands

sels = sgcommands.listNodes( sl=1 )

ctl = sels[0]
shapeGrps = sels[1:]
shapes = []
for shapeGrp in shapeGrps:
    shapeTrs = shapeGrp.listRelatives( c=1, ad=1, type='transform' )
    shapeTrs.append( shapeGrp )
    for shapeTr in shapeTrs:
        shape = shapeTr.shape()
        if not shape: continue
        shapes.append( shape )

for shape in shapes:
    sgcommands.transformGeometryControl( ctl, shape )