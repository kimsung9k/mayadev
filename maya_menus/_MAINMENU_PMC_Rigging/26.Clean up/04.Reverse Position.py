from sgModules import sgcommands
from sgModules import sgbase

for sel in sgcommands.listNodes( sl=1 ):
    tr = sel.t.get()[0]
    sel.t.set( -tr[0], -tr[1], -tr[2] )