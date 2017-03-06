from sgModules import sgcommands

sels = sgcommands.listNodes( sl=1 )

lookTarget = sels[0]
base = sels[1]

baseChild = base.makeChild('_child' )
splitsBase = base.localName().split( '_' )
if len( splitsBase ) >= 2:
    splitsChild = baseChild.localName().split( '_' )
    splits = [ 'LookAt' + splitsBase[0].capitalize() ]
    splits += splitsBase[1:]
    newName = '_'.join( splits )
    baseChild.rename( newName )

sgcommands.lookAtConnect( lookTarget, baseChild )
sgcommands.select( baseChild )