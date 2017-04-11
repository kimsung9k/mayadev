import maya.cmds as cmds
import sgFunctionSet
import sgModelDag
import sgRigAttribute




def connectAttrCommon( first, second ):
    
    if not cmds.isConnected( first, second ):
        cmds.connectAttr( first, second, f=1 )




def constraintOrient( first, target ):
    
    mmdc = cmds.createNode( 'multMatrixDecompose' )
    
    cmds.connectAttr( first+'.wm', mmdc+'.i[0]' )
    cmds.connectAttr( target+'.pim', mmdc+'.i[1]' )
    
    cmds.connectAttr( mmdc+'.or', target+'.r' )




def constraintTrans( first, target ):
    
    mmdc = cmds.createNode( 'multMatrixDecompose' )
    
    cmds.connectAttr( first+'.wm', mmdc+'.i[0]' )
    cmds.connectAttr( target+'.pim', mmdc+'.i[1]' )
    
    cmds.connectAttr( mmdc+'.ot', target+'.t' )




def constraint( first, target ):
    
    mmdc = cmds.createNode( 'multMatrixDecompose' )
    
    cmds.connectAttr( first+'.wm', mmdc+'.i[0]' )
    cmds.connectAttr( target+'.pim', mmdc+'.i[1]' )
    
    cmds.connectAttr( mmdc+'.ot', target+'.t' )
    cmds.connectAttr( mmdc+'.or', target+'.r' )
    if cmds.nodeType( target ) == 'joint':
        cmds.setAttr( target+'.jo', 0,0,0 )



def constraintAll( first, target ):
    
    mmdc = cmds.createNode( 'multMatrixDecompose' )
    
    cmds.connectAttr( first+'.wm', mmdc+'.i[0]' )
    cmds.connectAttr( target+'.pim', mmdc+'.i[1]' )
    
    cmds.connectAttr( mmdc+'.ot', target+'.t' )
    cmds.connectAttr( mmdc+'.or', target+'.r' )
    cmds.connectAttr( mmdc+'.os', target+'.s' )
    cmds.connectAttr( mmdc+'.osh', target+'.sh' )
    if cmds.nodeType( target ) == 'joint':
        cmds.setAttr( target+'.jo', 0,0,0 )




def createLocalMMDC( childTarget, parentTarget ):
    
    mmdc = cmds.createNode( 'multMatrixDecompose' )
    
    cmds.connectAttr( childTarget+'.wm', mmdc+'.i[0]' )
    cmds.connectAttr( parentTarget+'.wim', mmdc+'.i[1]' )
    
    return mmdc




def blendTwoMatrixConnect( first, second, target ):
    
    blendTwoMatrix = cmds.createNode( 'blendTwoMatrix' )
    mmdc = cmds.createNode( 'multMatrixDecompose' )
    
    cmds.connectAttr( first+'.wm', blendTwoMatrix+'.inMatrix1' )
    cmds.connectAttr( second+'.wm', blendTwoMatrix+'.inMatrix2' )
    
    cmds.connectAttr( blendTwoMatrix+'.outMatrix', mmdc+'.i[0]' )
    cmds.connectAttr( target+'.pim', mmdc+'.i[1]' )
    
    cmds.connectAttr( mmdc+'.ot', target+'.t' )
    cmds.connectAttr( mmdc+'.or', target+'.r' )
    if cmds.nodeType( target ) == 'joint':
        cmds.setAttr( target+'.jo', 0,0,0 )
    
    if not cmds.attributeQuery( 'blend', node=target, ex=1 ):
        cmds.addAttr( target, ln='blend', min=0, max=1, dv=0.5 )
    
    cmds.connectAttr( target+'.blend', blendTwoMatrix+'.attributeBlender' )




def blendTwoMatrixConnect_keepPosition( first, second, target ):
    
    targetPos = cmds.getAttr( target+'.wm' )
    
    firstChild = cmds.createNode( 'transform' )
    secondChild = cmds.createNode( 'transform' )
    
    cmds.xform( firstChild,  ws=1, matrix=targetPos )
    cmds.xform( secondChild, ws=1, matrix=targetPos )
    
    cmds.parent( firstChild, first )
    cmds.parent( secondChild, second )
    
    blendTwoMatrix = cmds.createNode( 'blendTwoMatrix' )
    mmdc = cmds.createNode( 'multMatrixDecompose' )
    
    cmds.connectAttr( firstChild+'.wm', blendTwoMatrix+'.inMatrix1' )
    cmds.connectAttr( secondChild+'.wm', blendTwoMatrix+'.inMatrix2' )
    
    cmds.connectAttr( blendTwoMatrix+'.outMatrix', mmdc+'.i[0]' )
    cmds.connectAttr( target+'.pim', mmdc+'.i[1]' )
    
    cmds.connectAttr( mmdc+'.ot', target+'.t' )
    cmds.connectAttr( mmdc+'.or', target+'.r' )
    if cmds.nodeType( target ) == 'joint':
        cmds.setAttr( target+'.jo', 0,0,0 )
    
    if not cmds.attributeQuery( 'blend', node=target, ex=1 ):
        cmds.addAttr( target, ln='blend', min=0, max=1, dv=0.5 )
        cmds.setAttr( target+'.blend', e=1, k=1 )
    
    cmds.connectAttr( target+'.blend', blendTwoMatrix+'.attributeBlender' )
    
    return firstChild, secondChild




def blendShapeConnectWidthController( ctl, blendShapeObjs, target ):

    cmds.select( blendShapeObjs, target )
    blendShape = cmds.blendShape( tc=0 )[0]

    for i in range( len( blendShapeObjs ) ):
        name = blendShapeObjs[i]

        if not cmds.attributeQuery( name, node = ctl, ex=1 ):
            cmds.addAttr( ctl, ln=name, min=0, max=1 )
            cmds.setAttr( ctl+'.'+name, e=1, k=1 )

        cmds.connectAttr( ctl+'.'+name, blendShape+'.w[%d]' % i )




def copyAttribute( firstAttr, second ):
    
    first, attr = firstAttr.split( '.' )
    
    keyAttrs = cmds.listAttr( firstAttr, k=1 )
    cbAttrs  = cmds.listAttr( firstAttr, k=1 )
    
    if not cmds.attributeQuery( attr, node=second, ex=1 ):
        attrType = cmds.attributeQuery( attr, node=first, at=1 )
        
        if attrType == 'enum':
            enumList = cmds.attributeQuery( attr, node=first, le=1 )
            cmds.addAttr( second, ln=attr, at=attrType, en= ':'.join( enumList ) + ':' )
        else:
            minValue = None
            maxValue = None
            if cmds.attributeQuery( attr, node=first, mne=1 ):
                minValue = cmds.attributeQuery( attr, node=first, min=1 )[0]
            if cmds.attributeQuery( attr, node=first, mxe=1 ):
                maxValue = cmds.attributeQuery( attr, node=first, max=1 )[0]
            if minValue != None and maxValue == None:
                cmds.addAttr( second, ln=attr, at=attrType, min=minValue )
            elif minValue == None and maxValue != None :
                cmds.addAttr( second, ln=attr, at=attrType, max=maxValue )
            elif minValue != None and maxValue != None :
                cmds.addAttr( second, ln=attr, at=attrType, min=minValue, max=maxValue )
            else:
                cmds.addAttr( second, ln=attr, at=attrType )
        
        if attr in keyAttrs:
            cmds.setAttr( second+'.'+attr, e=1, k=1 )
        elif attr in cbAttrs:
            cmds.setAttr( second+'.'+attr, e=1, cb=1 )



def optimizeConnection( target ):
    
    srcCons = cmds.listConnections( target, s=1, d=0, p=1, c=1 )
    dstCons = cmds.listConnections( target, s=0, d=1, p=1, c=1 )
    
    if not srcCons or not dstCons: return None
    
    for dstCon in dstCons[1::2]:
        try: cmds.connectAttr( srcCons[1], dstCon, f=1 )
        except:pass



def copyShader( first, second ):
    
    if not cmds.objExists( first ): return None
    if not cmds.objExists( second ): return None
    
    first = sgModelDag.getTransform( first )
    second = sgModelDag.getTransform( second )
    firstShape = sgModelDag.getShape( first )
    secondShape = sgModelDag.getShape( second )
    
    print firstShape
    engines = cmds.listConnections( firstShape, type='shadingEngine' )
    
    print engines
    if not engines: return None
    
    engines = list( set( engines ) )
    
    for engine in engines:
        shaders = cmds.listConnections( engine+'.surfaceShader', s=1, d=0 )
        if not shaders: continue
        shader = shaders[0]
        cmds.hyperShade( objects = shader )
        selObjs = cmds.ls( sl=1, l=1 )
        
        targetObjs = []
        for selObj in selObjs:
            if selObj.find( '.' ) != -1:
                trNode, components = selObj.split( '.' )
                if trNode == first:
                    targetObjs.append( second+'.'+components )
            elif selObj == firstShape:
                targetObjs.append( secondShape )
        
        if not targetObjs: continue
        
        for targetObj in targetObjs:
            cmds.sets( targetObj, e=1, forceElement=engine )


def copyShaderHierarchy( firstTopObj, secondTopObj ):
    
    replaceName = secondTopObj.replace( firstTopObj, '^' )
    
    targetIsSecond = False
    if replaceName == secondTopObj:
        replaceName = firstTopObj.replace( secondTopObj, '^' )
        targetIsSecond = True
    
    if targetIsSecond:
        secondShapes = cmds.listRelatives( secondTopObj, c=1, ad=1, type='shape', f=1 )
        for shape in secondShapes:
            second = cmds.listRelatives( shape, p=1 )[0]
            first = replaceName.replace( '^', second )
            if not cmds.objExists( second ): continue
            copyShader( first, second )
    else:
        firstShapes = cmds.listRelatives( firstTopObj, c=1, ad=1, type='shape', f=1 )
        for shape in firstShapes:
            first = cmds.listRelatives( shape, p=1 )[0]
            second = replaceName.replace( '^', first )
            if not cmds.objExists( second ): continue
            copyShader( first, second )
        
        
        
        
def duplicateShaderToOther( first, second ):
    
    import maya.mel as mel
    
    if not cmds.objExists( first ): return None
    if not cmds.objExists( second ): return None
    
    first = sgModelDag.getTransform( first )
    second = sgModelDag.getTransform( second )
    firstShape = sgModelDag.getShape( first )
    secondShape = sgModelDag.getShape( second )
    
    engines = cmds.listConnections( firstShape, type='shadingEngine' )
    
    if not engines: return None
    
    engines = list( set( engines ) )
    
    for engine in engines:
        shaders = cmds.listConnections( engine+'.surfaceShader', s=1, d=0 )
        if not shaders: continue
        shader = shaders[0]
        
        cmds.hyperShade( objects = shader )
        selObjs = cmds.ls( sl=1, l=1 )
        
        targetObjs = []
        for selObj in selObjs:
            if selObj.find( '.' ) != -1:
                trNode, components = selObj.split( '.' )
                if trNode == first:
                    targetObjs.append( second+'.'+components )
            elif selObj == firstShape:
                targetObjs.append( secondShape )
        
        cmds.select( shader )
        mel.eval( 'hyperShadePanelMenuCommand("hyperShadePanel1", "duplicateShadingNetwork")' )
        shader = cmds.ls( sl=1 )[0]
        engine = cmds.duplicate( engine, n=shader+'_engine' )[0]
        cmds.connectAttr( shader+'.outColor', engine+'.surfaceShader' )
        
        for targetObj in targetObjs:
            cmds.sets( targetObj, e=1, forceElement=engine )
            
            

def duplicateShaderToOtherHierarchy( firstTopObj, secondTopObj ):
    
    fNamespace = firstTopObj.replace( 'MOD', '' )
    sNamespace = secondTopObj.replace( 'MOD', '' )
    
    firstShapes = cmds.listRelatives( firstTopObj, c=1, ad=1, type='shape', f=1 )
    
    for shape in firstShapes:
        first = cmds.listRelatives( shape, p=1 )[0]
        second = first.replace( fNamespace, sNamespace )
        if not cmds.objExists( second ): continue
        duplicateShaderToOther( first, second )



def duplicateShaderTogether( topObjs ):
    
    for topObj in topObjs[1:]:
        duplicateShaderToOtherHierarchy( topObjs[0], topObj )



def followMatrixConnection( ctl, others ):
    
    ctlP = cmds.listRelatives( ctl, p=1 )[0]
    
    followMatrix = cmds.createNode( 'followMatrix' )
    mmdc = cmds.createNode( 'multMatrixDecompose' )
    
    cmds.connectAttr( others[0]+'.wm', followMatrix+'.originalMatrix' )
    
    sgRigAttribute.addAttr( ctl, ln='_______', at='enum', en='Parent:', cb=1 )
    
    for other in others[1:]:
        i = others.index( other ) - 1
        cmds.connectAttr( other+'.wm', followMatrix+'.inputMatrix[%d]' % i )
        
        attrName = 'parent' + other.split( '_' )[-1][2:]
        sgRigAttribute.addAttr( ctl, ln= attrName, min=0, max=10, k=1 )
        cmds.connectAttr( ctl+'.'+attrName, followMatrix+'.inputWeight[%d]' % i )
    
    cmds.connectAttr( followMatrix+'.outputMatrix', mmdc+'.i[0]' )
    cmds.connectAttr( ctlP+'.pim', mmdc+'.i[1]' )
    cmds.connectAttr( mmdc+'.ot', ctlP+'.t' )
    cmds.connectAttr( mmdc+'.or', ctlP+'.r' )
        



mc_copyShader='''import maya.cmds as cmds
import sgRigConnection

sels = cmds.ls( sl=1 )
sgRigConnection.copyShader( sels[0], sels[1] )
'''


mc_copyShaderHierarchy='''import maya.cmds as cmds
import sgRigConnection

sels = cmds.ls( sl=1 )
sgRigConnection.copyShaderHierarchy( sels[0], sels[1] )
'''


def connectHairControl( ctl, hairSystem ):
    
    hairSystem = sgModelDag.getNodeFromHistory( hairSystem, 'hairSystem' )[0]
    
    try:sgRigAttribute.addAttr( ctl, ln='________', en='Hair:', at='enum', cb=1 )
    except:pass
    sgRigAttribute.addAttr( ctl, ln='dynamicOn', min=0, max=1, at='long', cb=1 )
    sgRigAttribute.addAttr( ctl, ln='startFrame', dv=1, at='long', cb=1 )
    sgRigAttribute.addAttr( ctl, ln='attraction', min=0, max=1, dv=1, k=1 )
    sgRigAttribute.addAttr( ctl, ln='attractionDamp', min=0, dv=0.5, k=1 )
    sgRigAttribute.addAttr( ctl, ln='stiffness', min=0, max=1, dv=0.15, k=1 )
    sgRigAttribute.addAttr( ctl, ln='mass', min=0.1, dv=1, k=1 )
    sgRigAttribute.addAttr( ctl, ln='drag', min=0, dv=0.05, k=1 )
    
    condition = cmds.createNode( 'condition' )
    cmds.setAttr( condition+'.secondTerm', 0 )
    cmds.setAttr( condition+'.colorIfTrueR', 1 )
    cmds.setAttr( condition+'.colorIfFalseR', 3 )
    
    connectAttrCommon( ctl+'.dynamicOn', condition+'.firstTerm' )
    connectAttrCommon( ctl+'.startFrame', hairSystem+'.startFrame' )
    connectAttrCommon( condition+'.outColorR', hairSystem+'.simulationMethod' )
    connectAttrCommon( ctl+'.attraction', hairSystem+'.startCurveAttract' )
    connectAttrCommon( ctl+'.stiffness', hairSystem+'.stiffness' )
    connectAttrCommon( ctl+'.attractionDamp', hairSystem+'.attractionDamp' )
    connectAttrCommon( ctl+'.mass', hairSystem+'.mass' )
    connectAttrCommon( ctl+'.drag', hairSystem+'.drag' )






def selectConnectedNodes( ctl ):
    
    import sgBFunction_attribute
    attrs = sgBFunction_attribute.getChannelAttributeFromSelection()
    
    targets = []
    for attr in attrs:
        cons = cmds.listConnections( ctl+'.'+attr, d=1, s=0 )
        targets += cons
    
    cmds.select( targets )
    
    
    


def modelAsReference( worldCtl, model ):
    
    sgRigAttribute.addAttr( worldCtl, ln='modelAsReference', at='long', min=0, max=1, cb=1, dv=1 )
    
    cmds.setAttr( model+'.overrideEnabled', 1 )
    
    condition = cmds.createNode( 'condition' )
    
    cmds.connectAttr( worldCtl+'.modelAsReference', condition+'.firstTerm' )
    
    cmds.setAttr( condition+'.colorIfTrueR', 0 )
    cmds.setAttr( condition+'.colorIfFalseR', 2 )
    
    cmds.connectAttr( condition+'.outColorR', model+'.overrideDisplayType')


    

mc_selectConnectedNodes = """import maya.cmds as cmds
import sgRigConnection

for sel in cmds.ls( sl=1 ):
    sgRigConnection.selectConnectedNodes( sel )"""





def animCurveReplaceFloatInput( target ):
    
    animCurves = cmds.listConnections( target, s=1, d=0, type='animCurve' )
    
    newAnimCurves = []
    for animCurve in animCurves:
        nodeType = cmds.nodeType( animCurve )
        if cmds.nodeType( animCurve )[:-1] != "animCurveT": continue
        
        newAnimCurveNodeType = nodeType.replace( 'animCurveT', 'animCurveU' )
        
        newAnimCurve = cmds.createNode( newAnimCurveNodeType )
        
        tc = cmds.keyframe( animCurve, q=1, tc=1 )
        vc = cmds.keyframe( animCurve, q=1, vc=1 )
        
        for i in range( len( tc ) ):
            cmds.setKeyframe( newAnimCurve, f=tc[i], v=vc[i] )
        
        outputCon, inputCon = cmds.listConnections( animCurve+'.output', p=1, c=1, d=1, s=0 )
        cmds.connectAttr( newAnimCurve+'.output', inputCon, f=1 )
        cmds.delete( animCurve )
        newAnimCurves.append( newAnimCurve )
    
    print newAnimCurves
    cmds.select( newAnimCurves )



def replaceConnection( first, second ):
    
    fSrcCons = cmds.listConnections( first, s=1, d=0, p=1, c=1 )
    
    outputs = fSrcCons[1::2]
    inputs  = fSrcCons[::2]
    
    for i in range( len( outputs ) ):
        try:
            cmds.connectAttr( outputs[i], inputs[i].replace( first, second ), f=1 )
            cmds.disconnectAttr( outputs[i], inputs[i] )
        except: pass
    
    fDesCons = cmds.listConnections( first, s=0, d=1, p=1, c=1 )
    
    outputs = fDesCons[::2]
    inputs  = fDesCons[1::2]
    
    for i in range( len( outputs ) ):
        try:
            cmds.connectAttr( outputs[i].replace( first, second ), inputs[i], f=1 )
            cmds.disconnectAttr( outputs[i], inputs[i] )
        except:pass



def connectHairSystemAttr( first, second ):
    
    import sgModelAttribute
    
    first = sgModelDag.getShape( first )
    second = sgModelDag.getShape( second )
    
    connectAttrList = ['startFrame', 'active', 'simulationMethod',
                       'iterations', 'lengthFlex',
                       'startCurveAttract', 'attractionDamp', 'attractionScale', 
                       'stiffness', 'stiffnessScale',
                       'mass', 'drag', 'tangentialDrag', 'motionDrag', 'damp', 'gravity', 'dynamicsWeight',
                       'turbulenceStrength', 'turbulenceFrequency', 'turbulenceSpeed' ]
    
    for attr in connectAttrList:
        print attr, first
        if cmds.attributeQuery( attr, node=first, usesMultiBuilder=1 ):
            sgRigAttribute.removeMultiInstances( second, attr )
            indices = sgModelAttribute.getMultiAttrIndices(first, attr)
            for index in indices:
                connectAttrCommon( first+'.'+attr+'[%d]' % index, second+'.'+attr+'[%d]' % index )
        else:
            connectAttrCommon( first+'.'+attr, second+'.'+attr )




def mc_connectLocalMMDC_toTarget( *args ):
    
    sels = cmds.ls( sl=1 )
    
    childTargets = sels[::3]
    parentTargets = sels[1::3]
    connectTargets = sels[2::3]
    
    for i in range( len( connectTargets ) ):
        mmdc = createLocalMMDC( childTargets[i], parentTargets[i] )
        cmds.connectAttr( mmdc+'.ot', connectTargets[i]+'.t' )
        cmds.connectAttr( mmdc+'.or', connectTargets[i]+'.r' )
    
    cmds.select( connectTargets )



def mc_connectLocalMMDC_toParent( *args ):
    
    sels = cmds.ls( sl=1 )
    
    childTargets = sels[::3]
    parentTargets = sels[1::3]
    connectTargets = sels[2::3]
    
    connectTargetParents = []
    for i in range( len( connectTargets ) ):
        connectTargetParent = cmds.listRelatives( connectTargets[i], p=1 )[0]
        mmdc = createLocalMMDC( childTargets[i], parentTargets[i] )
        cmds.connectAttr( mmdc+'.ot', connectTargetParent+'.t' )
        cmds.connectAttr( mmdc+'.or', connectTargetParent+'.r' )
        
        connectTargetParents.append( connectTargetParent )
    
    cmds.select( connectTargetParents )



def mc_connectBlendTwoMatrix( *args ):
    
    sels = cmds.ls( sl=1 )
    
    firstTargets = sels[::3]
    secondTargets = sels[1::3]
    connectTargets = sels[2::3]
    
    for i in range( len( connectTargets ) ):
        blendTwoMatrixConnect( firstTargets[i], secondTargets[i], connectTargets[i] )
    
    cmds.select( connectTargets )


def mc_connectBlendTwoMatrix_keepPosition( *args ):
    
    sels = cmds.ls( sl=1 )
    
    firstTargets = sels[::3]
    secondTargets = sels[1::3]
    connectTargets = sels[2::3]
    
    firstChildren = [] 
    secondChildren = []
    for i in range( len( connectTargets ) ):
        firstChild, secondChild = blendTwoMatrixConnect_keepPosition( firstTargets[i], secondTargets[i], connectTargets[i] )
        firstChildren.append( firstChild )
        secondChildren.append( secondChild )
    
    cmds.select( connectTargets )
    
    return firstChildren, secondChildren
    


def mc_connectBlendTwoMatrix_keepPositionAndSkipSecondTrans( *args ):
    
    sels = cmds.ls( sl=1 )
    
    firstTargets = sels[::3]
    secondTargets = sels[1::3]
    connectTargets = sels[2::3]
    
    firstChildren = []
    secondChildren = []
    for i in range( len( connectTargets ) ):
        firstChild, secondChild = blendTwoMatrixConnect_keepPosition( firstTargets[i], secondTargets[i], connectTargets[i] )
    
        secondChildGrp = cmds.group( secondChild )
        cmds.xform( secondChildGrp, os=1, piv=[0,0,0] )
        secondParent = cmds.listRelatives( secondTargets[i], p=1 )[0]
        constraintOrient( secondParent, secondChildGrp )
        
        sgFunctionSet.goToObject( secondChild, firstChild )
        
        firstChildren.append( firstChild )
        secondChildren.append( secondChild )
    
    cmds.select( connectTargets )
    
    return firstChildren, secondChildren




mc_constraint ="""import maya.cmds as cmds
import sgRigConnection

sels = cmds.ls( sl=1 )

firstTargets = sels[::2]
secondTargets = sels[1::2]

for i in range( len( firstTargets ) ):
    sgRigConnection.constraint( firstTargets[i], secondTargets[i] )

cmds.select( secondTargets )"""
    


mc_constraintAll = """import maya.cmds as cmds
import sgRigConnection

sels = cmds.ls( sl=1 )

firstTargets = sels[::2]
secondTargets = sels[1::2]

for i in range( len( firstTargets ) ):
    sgRigConnection.constraintAll( firstTargets[i], secondTargets[i] )

cmds.select( secondTargets )"""


mc_constraintToParent = """import maya.cmds as cmds
import sgRigConnection
    
sels = cmds.ls( sl=1 )

firstTargets = sels[::2]
secondTargets = sels[1::2]

secondParents = []
for i in range( len( firstTargets ) ):
    secondParent = cmds.listRelatives( secondTargets[i], p=1 )[0]
    sgRigConnection.constraint( firstTargets[i], secondParent )
    secondParents.append( secondParent )

cmds.select( secondParents )"""




mc_copyAttributeAndConnect = """import maya.cmds as cmds
import sgRigConnection
import sgBFunction_attribute
sels = cmds.ls( sl=1 )

first = sels[0]
others = sels[1:]

selectedAttrs = sgBFunction_attribute.getChannelAttributeFromSelection()

for other in others:
    for attr in selectedAttrs:
        sgRigConnection.copyAttribute( other+'.'+attr, first )
        cmds.connectAttr( first+'.'+attr, other+'.'+attr )"""


mc_optimizeConnection = """import maya.cmds as cmds
import sgRigConnection

sels = cmds.ls( sl=1 )

for sel in sels:
    sgRigConnection.optimizeConnection( sel )"""



mc_connectHairAttribute = """import maya.cmds as cmds
import sgRigConnection

sels = cmds.ls( sl=1 )

ctl = sels[0]
hairSystems = sels[1:]

for hairSystem in hairSystems:
    sgRigConnection.connectHairAttribute( ctl, hairSystem )"""