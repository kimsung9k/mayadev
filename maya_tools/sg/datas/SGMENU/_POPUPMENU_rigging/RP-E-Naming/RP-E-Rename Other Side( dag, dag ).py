from sgModules import sgcommands

sels = sgcommands.listNodes( sl=1 )
    
if sels[0].name().find( '_L_' ) != -1:
    sels[1].rename( sels[0].localName().replace( '_L_', '_R_' ) )
elif sels[0].name().find( '_R_' ) != -1:
    sels[1].rename( sels[0].localName().replace( '_R_', '_L_' ) )