from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )

attrList = ['ot','otx','oty','otz']
for sel in sels:
    for attr in attrList:
        sgCmds.convertDestinationConnectionsToReverse( sel.attr( attr ) )