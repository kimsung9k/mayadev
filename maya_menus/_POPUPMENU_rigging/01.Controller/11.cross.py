from sgModules import sgdata
from sgModules import sgRig

sels = cmds.ls( sl=1 )
for sel in sels:
    sgRig.putControllerToGeo( sel, sgdata.Controllers.crossPoints, 1.1 )