from sgMaya import sgCmds
sels = pymel.core.ls( sl=1 )

firstGrp = sels[0]
secondGrp = sels[1]

firstChildren = firstGrp.listRelatives( c=1, ad=1, type='transform' )
secondChildren = secondGrp.listRelatives( c=1, ad=1, type='transform' )

for i in range( len( firstChildren ) ):
    if not firstChildren[i].getShape(): continue
    try:sgCmds.autoCopyWeight( firstChildren[i], secondChildren[i] )
    except:pass