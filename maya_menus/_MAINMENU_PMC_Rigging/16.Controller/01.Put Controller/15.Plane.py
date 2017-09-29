from sgMaya import sgModel, sgCmds

sels = cmds.ls( sl=1 )
if not sels: sels = [None]
for sel in sels:
    sgCmds.putControllerToGeo( sel, sgModel.Controller.planePoints )