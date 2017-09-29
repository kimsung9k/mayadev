from sgMaya import sgCmds
import pymel.core
sels = pymel.core.ls( sl=1 )

for sel in sels:
    conditions = sel.listConnections( s=0, d=1, type='condition' )
    
    condition1 = None
    condition2 = None
    for condition in conditions:
        if condition.secondTerm.get() == 0:
            condition1 = condition
        elif condition.secondTerm.get() == 1:
            condition2 = condition
    
    con1Dests = condition1.listConnections( s=0, d=1, type='transform', p=1, c=1 )
    con2Dests = condition2.listConnections( s=0, d=1, type='transform', p=1, c=1 )
    if not con1Dests: continue
    
    add1 = pymel.core.createNode( 'addDoubleLinear' )
    add2 = pymel.core.createNode( 'addDoubleLinear' )
    
    setRange1 = pymel.core.createNode( 'setRange' )
    setRange2 = pymel.core.createNode( 'setRange' )
    
    con1Dests[0][0] >> add1.input1
    con2Dests[0][0] >> add2.input1
    
    sgCmds.addAttr( sel, ln='origVis', min=-1, max=1, at='long', k=1 )
    sgCmds.addAttr( sel, ln='paintedVis', min=-1, max=1, at='long', k=1 )
    
    sel.attr( 'origVis' ) >> add1.input2
    sel.attr( 'paintedVis' ) >> add2.input2
    
    add1.output >> setRange1.valueX
    add2.output >> setRange2.valueX
    
    setRange1.maxX.set( 1 )
    setRange1.oldMaxX.set( 1 )
    setRange2.maxX.set( 1 )
    setRange2.oldMaxX.set( 1 )
    
    setRange1.outValueX >> con1Dests[0][1]
    setRange2.outValueX >> con2Dests[0][1]    
    
