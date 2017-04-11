import maya.cmds as cmds


def getSourceConnection( target, **options ):
    
    outputCons = []
    inputCons  = []
    
    if target.find( '.' ) != -1:
        splits = target.split( '.' )
        node = splits[0]
        attr = '.'.join( splits[1:] )
        attrs = [ attr ]
    else:
        node = target
        attrs = cmds.listAttr( target, **options )
    
    for attr in attrs:
        
        if attr.find( '.' ) != -1: continue
        parentAttr = cmds.attributeQuery( attr, node=node, listParent=1 )
        
        if parentAttr:
            cons = cmds.listConnections( node+'.'+parentAttr[0], s=1, d=0, p=1, c=1 )
            if cons:
                outputCons += cons[1::2]
                inputCons  += cons[::2]
    
        cons = cmds.listConnections( node + '.' + attr, s=1, d=0, p=1, c=1 )
        if cons:
            outputCons += cons[1::2]
            inputCons  += cons[::2]

    returnOutputs = []
    returnInputs  = []
    for outputCon in outputCons:
        if not outputCon in returnOutputs:
            returnOutputs.append( outputCon )
    for inputCon  in inputCons:
        if not inputCon in returnInputs:
            returnInputs.append( inputCon )
    
    return returnOutputs, returnInputs
