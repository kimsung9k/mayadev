from sgModules import sgcommands

for sel in sgcommands.listNodes( sl=1 ):
    sgcommands.setAngleReverse( sel )