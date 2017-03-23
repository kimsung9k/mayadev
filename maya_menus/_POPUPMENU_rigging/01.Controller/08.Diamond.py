from sgModules import sgdata
from sgModules import sgRig

sels = cmds.ls( sl=1 )
if not sels: sels = [None]
for sel in sels:
    sgRig.putControllerToGeo( sel, sgdata.Controllers.diamondPoints, 1.1 )