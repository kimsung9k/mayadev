from sgMaya import sgCmds
import pymel.core
sels = pymel.core.ls( sl=1 )

curves = sels[:-2]
wire = sels[-2]
wireBase = sels[-1]

sgCmds.setWire( curves, wire, wireBase )