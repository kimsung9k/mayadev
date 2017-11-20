from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )
targets = []
for sel in sels:
    putTarget = sgCmds.putObject( sel, 'joint' ) 
    putTarget.setParent( sel )
    
    selName = sel.split('|')[-1]
    childName = ''
    if selName[-1] == '_':
        childName = sel.nodeName() + 'child'
    else:
        childName = sel.nodeName() + '_child'
    putTarget.rename( childName )
    targets.append( putTarget )

pymel.core.select( targets )