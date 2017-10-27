from sgMaya import sgCmds
import pymel.core

for sel in pymel.core.ls( sl=1 ):
    tr = sel.t.get()[0]
    sel.t.set( -tr[0], -tr[1], -tr[2] )