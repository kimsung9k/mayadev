from sgModules import sgHumanRigCommands
sels = cmds.ls( sl=1 )
for sel in sels:
    try:
        rigControl = sgHumanRigCommands.RigControllerControl( sel )
        rigControl.flipH()
        break
    except:
        continue