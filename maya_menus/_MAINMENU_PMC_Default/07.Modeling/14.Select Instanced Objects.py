import maya.OpenMaya as om

def getInstances():
    instances = []
    iterDag = om.MItDag(om.MItDag.kBreadthFirst)
    while not iterDag.isDone():
        instanced = om.MItDag.isInstanced(iterDag)
        if instanced:
            instances.append(iterDag.fullPathName())
        iterDag.next()
    return instances

instances = []
for i in getInstances():
    tr = cmds.listRelatives( i, p=1, f=1 )[0]
    instances.append( tr )

removeTargets = []

for i in range( len( instances ) ):
    parentObjs = cmds.listRelatives( instances[i], p=1, f=1 )
    if not parentObjs: continue
    if parentObjs[0] in instances:
        removeTargets.append(instances[i])

for i in range( len(removeTargets) ):
    instances.remove( removeTargets[i] )

targets = []

for instance in instances:
    if instance.find( '_proxy' ) != -1: continue
    targets.append( instance )

cmds.select( instances )