from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )

worldGeos = []
for sel in sels:
    worldGeos.append( sgCmds.getWorldGeometry( sel ) )
pymel.core.select( worldGeos )