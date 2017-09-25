import pymel.core

sels = pymel.core.ls( sl=1 )

firstName = sels[0].name()
firstLocalName = firstName.split( '|' )[-1]

digitIndices = []
for i in range( len( firstLocalName ) ):
    if firstLocalName[i].isdigit():
        if len( digitIndices ):
            if i == digitIndices[-1]+1:
                digitIndices.append( i )
            else:
                digitIndices = [i]
        else:
            digitIndices.append( i )

if digitIndices:
    sepNameFront = firstLocalName[:digitIndices[0]]
    sepNameBack  = firstLocalName[digitIndices[-1]+1:]
    
    numFormat = "%0" + str(len( digitIndices )) + "d"
    
    startNum = int( firstLocalName[digitIndices[0]:digitIndices[-1]+1] )
    fullNameFormat = sepNameFront + numFormat + sepNameBack
else:
    startNum = 0
    fullNameFormat = firstName.split( '|' )[-1] + '%02d'
    
for sel in sels:
    sel.rename( fullNameFormat % startNum )
    startNum += 1