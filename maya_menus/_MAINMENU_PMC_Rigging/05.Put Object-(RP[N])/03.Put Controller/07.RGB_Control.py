from sgMaya import sgModel, sgCmds
import pymel.core

sels  = pymel.core.ls( sl=1 )
mtx   = sgCmds.getMatrixFromSelection( sels )

circleR = sgCmds.makeController( sgModel.Controller.circlePoints )
circleG = sgCmds.makeController( sgModel.Controller.circlePoints )
circleB = sgCmds.makeController( sgModel.Controller.circlePoints )
lineR   = sgCmds.makeController( sgModel.Controller.linePoints )
lineG   = sgCmds.makeController( sgModel.Controller.linePoints )
lineB   = sgCmds.makeController( sgModel.Controller.linePoints )
base    = sgCmds.makeController( sgModel.Controller.planPoints )

circleR.setAttr( 'shape_sx', 0.08 );circleR.setAttr( 'shape_sy', 0.16 );circleR.setAttr( 'shape_sz', 0.16 )
circleG.setAttr( 'shape_sx', 0.08 );circleG.setAttr( 'shape_sy', 0.16 );circleG.setAttr( 'shape_sz', 0.16 )
circleB.setAttr( 'shape_sx', 0.08 );circleB.setAttr( 'shape_sy', 0.16 );circleB.setAttr( 'shape_sz', 0.16 )
lineR.setAttr( 'shape_sz', 0.01 );lineR.setAttr( 'tz', -0.5 )
lineG.setAttr( 'shape_sz', 0.01 );lineG.setAttr( 'tz',  0.0 )
lineB.setAttr( 'shape_sz', 0.01 );lineB.setAttr( 'tz',  0.5 )
base.setAttr( 'shape_sx', 1.5 )

pCircleR = sgCmds.makeParent( circleR );pCircleR.setAttr( 'tx', -1 );pCircleR.setAttr( 'tz', -0.5 );pCircleR.setAttr( 'sx', 2 )
pCircleG = sgCmds.makeParent( circleG );pCircleG.setAttr( 'tx', -1 );pCircleG.setAttr( 'tz',  0.0 );pCircleG.setAttr( 'sx', 2 )
pCircleB = sgCmds.makeParent( circleB );pCircleB.setAttr( 'tx', -1 );pCircleB.setAttr( 'tz',  0.5 );pCircleB.setAttr( 'sx', 2 )

pymel.core.parent( pCircleR, pCircleG, pCircleB, lineR, lineG, lineB, base )

cmds.transformLimits( circleR.name(), tx=[0,1], etx=[1,1] )
cmds.transformLimits( circleG.name(), tx=[0,1], etx=[1,1] )
cmds.transformLimits( circleB.name(), tx=[0,1], etx=[1,1] )

pymel.core.select( base )