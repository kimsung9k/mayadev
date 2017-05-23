from sgModules import sgProjectCommands
import pymel.core

sels = pymel.core.ls( sl=1 )

ctls = sels[:-2]
srcMesh = sels[-2]
dstMesh = sels[-1]

sgProjectCommands.DuplicateBlendShapeByCtl( ctls, srcMesh, dstMesh )