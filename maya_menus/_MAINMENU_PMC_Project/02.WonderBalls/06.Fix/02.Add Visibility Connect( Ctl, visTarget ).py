from sgMaya import sgCmds
import pymel.core
sels = pymel.core.ls( sl=1 )
sgCmds.addOptionAttribute( sels[0], 'options' )
sgCmds.addAttr( sels[0], ln='hide', min=0, max=1, k=1, at='long' )
revNode = pymel.core.createNode( 'reverse' )
sels[0].attr( 'hide' ) >> revNode.inputX
revNode.outputX >> sels[1].v