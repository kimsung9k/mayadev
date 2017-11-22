from sgMaya import sgCmds
import pymel.core
nodes = pymel.core.ls( sl=1 )
for node in nodes:
    md = pymel.core.createNode( 'multDoubleLinear' )
    node.scalarOutput() >> md.input1