from sgModules.base import sgdata
from sgModules import sgcommands
from maya import cmds

sels  = cmds.ls( sl=1 )
mtx   = sgcommands.getMatrixFromSelection( sels )

circleR = sgcommands.makeController( sgdata.Controllers.circlePoints )
circleG = sgcommands.makeController( sgdata.Controllers.circlePoints )
circleB = sgcommands.makeController( sgdata.Controllers.circlePoints )
lineR   = sgcommands.makeController( sgdata.Controllers.linePoints )
lineG   = sgcommands.makeController( sgdata.Controllers.linePoints )
lineB   = sgcommands.makeController( sgdata.Controllers.linePoints )
base    = sgcommands.makeController( sgdata.Controllers.planPoints )

circleR.setAttr( 'shape_sx', 0.08 ).setAttr( 'shape_sy', 0.16 ).setAttr( 'shape_sz', 0.16 )
circleG.setAttr( 'shape_sx', 0.08 ).setAttr( 'shape_sy', 0.16 ).setAttr( 'shape_sz', 0.16 )
circleB.setAttr( 'shape_sx', 0.08 ).setAttr( 'shape_sy', 0.16 ).setAttr( 'shape_sz', 0.16 )
lineR.setAttr( 'shape_sz', 0.01 ).setAttr( 'tz', -0.5 )
lineG.setAttr( 'shape_sz', 0.01 ).setAttr( 'tz',  0.0 )
lineB.setAttr( 'shape_sz', 0.01 ).setAttr( 'tz',  0.5 )
base.setAttr( 'shape_sx', 1.5 )

pCircleR = sgcommands.makeParent( circleR ).setAttr( 'tx', -1 ).setAttr( 'tz', -0.5 ).setAttr( 'sx', 2 )
pCircleG = sgcommands.makeParent( circleG ).setAttr( 'tx', -1 ).setAttr( 'tz',  0.0 ).setAttr( 'sx', 2 )
pCircleB = sgcommands.makeParent( circleB ).setAttr( 'tx', -1 ).setAttr( 'tz',  0.5 ).setAttr( 'sx', 2 )

sgcommands.parent( pCircleR, pCircleG, pCircleB, lineR, lineG, lineB, base )

cmds.transformLimits( circleR.name(), tx=[0,1], etx=[1,1] )
cmds.transformLimits( circleG.name(), tx=[0,1], etx=[1,1] )
cmds.transformLimits( circleB.name(), tx=[0,1], etx=[1,1] )

sgcommands.select( base )