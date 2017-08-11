from sgMaya import sgCmds, sgModel
import pymel.core

sels = pymel.core.ls( sl=1 )
target = sels[0]
pymel.core.delete( target.getShape() )

circle = sgCmds.makeController( sgModel.Controller.circlePoints, 5 )
circle.shape_rz.set( 90 )
pymel.core.parent( circle.getShape(), target, add=1, shape=1 )
sgCmds.setIndexColor( target, 13 )
pymel.core.refresh()
pymel.core.delete( circle )
pymel.core.select( target )