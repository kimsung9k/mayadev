from maya import cmds
plugins = cmds.unknownPlugin( q=1, list=1 )
if not plugins: plugins = []
for plugin in plugins:
    cmds.unknownPlugin( plugin, remove=1 )