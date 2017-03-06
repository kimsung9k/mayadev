from sgModules import sgcommands
from sgModules import sgbase

for sel in sgcommands.listNodes( sl=1 ):
    sgcommands.setAngleReverse( sel )