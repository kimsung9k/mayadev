from sgModules.base import sgdata
from sgModules import sgRig

sels = cmds.ls( sl=1 )
if not sels: sels = [None]
for sel in sels:
    sgRig.putControllerToGeo( sel, sgdata.Controllers.movePoints, 1.1 )