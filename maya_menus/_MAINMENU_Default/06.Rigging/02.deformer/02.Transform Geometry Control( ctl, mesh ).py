from sgModules import sgcommands

sels = sgcommands.listNodes( sl=1 )

ctl = sels[0]
meshs = sels[1:]

for mesh in meshs:
    sgcommands.transformGeometryControl( ctl, mesh )