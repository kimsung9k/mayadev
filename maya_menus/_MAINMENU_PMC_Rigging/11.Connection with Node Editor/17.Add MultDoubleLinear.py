from sgMaya import sgCmds
from sgMaya import sgCmds
import pymel.core

nodes = pymel.core.ls( sl=1 )
for node in nodes:
    md = pymel.core.createNode( 'multDoubleLinear' )
    outputAttr = sgCmds.scalarOutput( node )
    if outputAttr:
    	outputAttr >> md.input1