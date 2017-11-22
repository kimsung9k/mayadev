from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )

ctl = sels[0]
meshs = sels[1:]

for mesh in meshs:
    sgCmds.transformGeometryControl( ctl, mesh )