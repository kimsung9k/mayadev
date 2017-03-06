from sgModules import sgcommands

sels = sgcommands.listNodes( sl=1 )

if isinstance( sels[0], sgcommands.SGDagNode ):
    firstName = sels[0].name()
else:
    firstName = sels[0].localName()

digitIndices = []
for i in range( len( firstName ) ):
    if firstName[i].isdigit():
        if len( digitIndices ):
            if i == digitIndices[-1]+1:
                digitIndices.append( i )
            else:
                digitIndices = [i]
        else:
            digitIndices.append( i )
if digitIndices:
    sepNameFront = firstName[:digitIndices[0]]
    sepNameBack  = firstName[digitIndices[-1]+1:]
    
    numFormat = "%0" + str(len( digitIndices )) + "d"
    
    startNum = int( firstName[digitIndices[0]:digitIndices[-1]+1] )
    fullNameFormat = sepNameFront + numFormat + sepNameBack
else:
    startNum = 0
    fullNameFormat = firstName + '%02d'
    
for sel in sels:
    sel.rename( fullNameFormat % startNum )
    startNum += 1