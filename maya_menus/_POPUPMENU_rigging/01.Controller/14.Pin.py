from sgModules import sgdata
from sgModules import sgRig

sels = cmds.ls( sl=1 )
for sel in sels:
    sgRig.putControllerToGeo( sel, sgdata.Controllers.pinPoints, 1.1 )
sgcommands.select( curve )