from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )

curve = sels[0]
upObject = sels[1]
targets = sels[2:]

for target in targets:
    pymel.core.tangentConstraint( curve, target, aim=[0,1,0], u=[1,0,0], wu=[1,0,0], wut='objectrotation', wuo=upObject )