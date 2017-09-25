from sgModules import sgcommands

sels = sgcommands.listNodes( sl=1 )
for sel in sels:
    if sel.nodeType() != 'joint': continue
    try:sel.jo.set( 0,0,0 )
    except:pass