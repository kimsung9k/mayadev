import maya.cmds as cmds
import maya.OpenMaya as om



def copyFollicleAttribute( *args ):
    
    sels = cmds.ls( sl=1 )
    
    others = sels[:-1]
    first = sels[-1]
    
    import sgBModel_attribute
    import sgBFunction_dag
    import sgBFunction_attribute
    
    first = sgBFunction_dag.getShape( first )
    if cmds.nodeType( first ) == 'nurbsCurve':
        first = sgBFunction_dag.getFollicleFromCurve( first )

    for i in range( len( others ) ):
        other = sgBFunction_dag.getShape( others[i] )
        if cmds.nodeType( other ) == 'nurbsCurve':
            other = sgBFunction_dag.getFollicleFromCurve( other )
        others[i] = other
    
    follicleRampAttrList = sgBModel_attribute.follicleRampAttrList

    follicleNormalAttrList = sgBModel_attribute.follicleNormalAttrList
    
    fnNode = om.MFnDependencyNode( sgBFunction_dag.getMObject( first ) )
    
    rampAttrNames = []
    rampValues    = []
    
    for rampAttr in follicleRampAttrList:
        print "node name : ", fnNode.name()
        plugAttr = fnNode.findPlug( rampAttr )
        print rampAttr
        
        for other in others:
            sgBFunction_attribute.removeMultiInstances( other, rampAttr )
         
        for j in range( plugAttr.numElements() ):
            rampAttrNames.append( plugAttr[j].name().split( '.' )[-1] )
            rampValues.append( cmds.getAttr( plugAttr[j].name() )[0] )
    
    for other in others:
        for i in range( len( rampAttrNames ) ):
            cmds.setAttr( other+'.'+rampAttrNames[i], *rampValues[i] )
    
    for normalAttr in follicleNormalAttrList:
        attrValue = cmds.getAttr( first+'.'+normalAttr )
        for other in others:
            try:cmds.setAttr( other+'.'+normalAttr, attrValue )
            except:pass