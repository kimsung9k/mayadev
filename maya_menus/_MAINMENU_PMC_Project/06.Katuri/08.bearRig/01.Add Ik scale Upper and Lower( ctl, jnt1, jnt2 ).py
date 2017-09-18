import pymel.core
sels = pymel.core.ls( sl=1 )

firstCtl = sels[0]
others = sels[1:]

clampNodes = []
for other in others:
    cons = other.sx.listConnections( s=1, d=0, type='clamp' )
    if not cons: continue
    clampNodes += cons

attrs = ['ikScaleUpper', 'ikScaleLower' ]

for i in range( 2 ):
    attr = attrs[i]
    multNode = pymel.core.createNode( 'multDoubleLinear' )
    addNode = pymel.core.createNode( 'addDoubleLinear' )
    try:
        firstCtl.addAttr( attrs[i], k=1 )
    except:
        pass
    firstCtl.attr( attrs[i] ) >> multNode.input1
    multNode.input2.set( 0.1 )
    clampNodes[0].outputR >> addNode.input1
    multNode.output >> addNode.input2
    addNode.output >> others[i].scaleX