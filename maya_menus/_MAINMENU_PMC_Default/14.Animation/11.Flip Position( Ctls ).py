from sgModules import sgHumanRigCommands
sels = cmds.ls( sl=1 )
for sel in sels:
    rigControl = sgHumanRigCommands.RigControllerControl( sel )
    rigControl.setFlip()