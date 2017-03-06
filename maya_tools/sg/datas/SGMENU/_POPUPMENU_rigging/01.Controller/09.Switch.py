from sgModules import sgdata
from sgModules import sgcommands
from maya import cmds

sels = cmds.ls( sl=1 )
mtx = sgcommands.getMatrixFromSelection( sels )
curve = sgcommands.makeController( sgdata.Controllers.switchPoints )
curve.xform( ws=1, matrix=mtx )
sgcommands.select( curve )