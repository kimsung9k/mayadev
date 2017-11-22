from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )
newObjs = []
for sel in sels:
    newObj = sgCmds.putObject( sel, 'joint' )
    sgCmds.constrain_parent( sel, newObj )
    newObjs.append( newObj )
pymel.core.select( newObjs )