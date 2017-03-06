import maya.cmds as cmds
import maya.OpenMaya as om


def createControlAbleJoint( topJoint ):
    
    import sgBFunction_dag
    
    parents = sgBFunction_dag.getParents( topJoint )
    
    targetParent = None
    if parents: targetParent = parents[-1]
    
    children = sgBFunction_dag.getDirectChildren( topJoint )
    
    firstJnt = None
    if targetParent:
        cmds.select( targetParent )
        firstJnt = cmds.joint()
    else:
        firstJnt = cmds.createNode( 'joint' )
    
    dcmp = cmds.createNode( 'decomposeMatrix' )
    cmds.connectAttr( topJoint+'.m', dcmp+'.imat' )
    cmds.connectAttr( dcmp+'.ot', firstJnt+'.t' )
    cmds.connectAttr( dcmp+'.or', firstJnt+'.jo' )
    cmds.connectAttr( dcmp+'.os', firstJnt+'.s' )
    cmds.connectAttr( dcmp+'.osh', firstJnt+'.sh' )
    
    jnts = [firstJnt]
    for child in children:
        cmds.select( firstJnt )
        cuJnt = cmds.joint()
        dcmp = cmds.createNode( 'decomposeMatrix' )
        cmds.connectAttr( child+'.m', dcmp+'.imat' )
        cmds.connectAttr( dcmp+'.ot', cuJnt+'.t' )
        cmds.connectAttr( dcmp+'.or', cuJnt+'.jo' )
        cmds.connectAttr( dcmp+'.os', cuJnt+'.s' )
        cmds.connectAttr( dcmp+'.osh', cuJnt+'.sh' )
        firstJnt = cuJnt
        jnts.append( firstJnt )
        
    return jnts




def pickOutJoint( targets ):
    
    import sgBFunction_dag
    
    for target in targets:
        targetH = sgBFunction_dag.getParents( target )
        targetH.append( target )
        children = cmds.listRelatives( target, c=1, ad=1 )
        children.reverse()
        targetH += children
        
        oTargetH = []
        oTarget = om.MObject()
        for h in targetH:
            oTargetH.append( sgBFunction_dag.getMObject( h ) )
            if h == target: oTarget = oTargetH[-1]
        
        for i in range( len( oTargetH ) ):
            if oTarget == oTargetH[i]:
                fnChild = None
                fnParent = None
                fnTarget = om.MFnDagNode( oTargetH[i] )
                if not i == 0:
                    fnParent = om.MFnDagNode( oTargetH[i-1] )
                if not i == len( oTargetH ):
                    fnChild = om.MFnDagNode( oTargetH[i+1] )
                
                if fnChild:
                    if fnParent:
                        cmds.parent( fnChild.fullPathName(), fnParent.fullPathName() )
                    else:
                        cmds.parent( fnChild.fullPathName(), w=1 )
                
                cmds.delete( fnTarget.fullPathName() )





def makeControlJointFromCurve( sels ):
    
    import sgBFunction_dag
    for sel in sels:
        origShape = sgBFunction_dag.getOrigShape( sel )
        
        if not origShape: continue
        
        cvs = cmds.ls( origShape+'.cv[*]', fl=1 )
        cmds.select( d=1 )
        jnts = []
        for i in range( len( cvs ) ):
            cvPoint = cmds.xform( cvs[i], q=1, ws=1, t=1 )
            jnt = cmds.joint()
            cmds.move( cvPoint[0], cvPoint[1], cvPoint[2], jnt, ws=1 )
            jnts.append( jnt )
        
        pim = jnts[0]+'.pim'
        for i in range( len( jnts ) ):
            mmdc = cmds.createNode( 'multMatrixDecompose' )
            cmds.connectAttr( jnts[i]+'.wm', mmdc+'.i[0]' )
            cmds.connectAttr( pim, mmdc+'.i[1]' )
            cmds.connectAttr( mmdc+'.ot', origShape+'.controlPoints[%d]' % i )




def createEditableJoints( sels ):
    
    import sgBFunction_dag
    import sgBFunction_connection
    
    for sel in sels:
        jnts = createControlAbleJoint( sel )
        selP = cmds.listRelatives( sel, p=1, f=1 )[0]
        
        targetClone = sgBFunction_dag.makeCloneObject( selP, '_controlable' )
        cmds.parent( jnts[0], targetClone )
        
        sgBFunction_connection.constraintAll( selP, targetClone )
        
        skinClusterNodes = cmds.listConnections( sel+'.worldMatrix', d=1, s=0, type='skinCluster' )
        if not skinClusterNodes: continue
        
        for skinClusterNode in skinClusterNodes:
            matrixCons = cmds.listConnections( skinClusterNode+'.matrix', p=1, c=1 )
            
            srcCons = matrixCons[1::2]
            dstCons = matrixCons[::2]
            
            for i in range( len( srcCons ) ):
                srcCon = srcCons[i]
                dstCon = dstCons[i]
                
                srcNode, attrName = srcCon.split( '.' )
                dcmps = cmds.listConnections( srcNode+'.m', d=1, s=0, type='decomposeMatrix' )
                if not dcmps: continue
                jnt  = cmds.listConnections( dcmps[0]+'.or', s=0, d=1 )[0]

                cmds.connectAttr( jnt+'.'+attrName, dstCon, f=1 )




class JointLineSet:
    

    def __init__(self, topJoint ):
        
        import maya.OpenMaya
        import math
        
        self.openMaya = maya.OpenMaya
        self.oCurve = None
        self.numPoints = 0
        self.jntH = []
        self.sin  = math.sin
        self.maxRadValue = math.pi / 2.0
        
        self.updateJointH( topJoint )
    
    

    def updateJointH(self, topJoint ):
        
        self.jntH = cmds.listRelatives( topJoint, c=1, ad=1, f=1, type='joint' )
        self.jntH.append( topJoint )
        self.jntH.reverse()



    def getCurveLength(self):
        
        self.editCurveByJoints()
        return self.fnCurve.length()
    
    
    def getLength(self):
        
        self.editCurveByJoints()
        return self.fnCurve.length()
    
    

    def editCurveByJoints(self):
        
        fnCurve = self.openMaya.MFnNurbsCurve()
        fnCurveData = self.openMaya.MFnNurbsCurveData()
        self.oCurve = fnCurveData.create()
        
        points = self.openMaya.MPointArray()
        points.setLength( len( self.jntH ) )
        for i in range( len( self.jntH ) ):
            points.set( self.openMaya.MPoint( *cmds.xform( self.jntH[i], q=1, ws=1, t=1 ) ), i )
        
        fnCurve.createWithEditPoints( points, 3, 1, 0, 0, 1, self.oCurve )
        fnCurve.setObject( self.oCurve )
        
        self.fnCurve = fnCurve
    


    def getPositionFromCurve(self, numPoint, equally=False ):
        
        crvLength = self.fnCurve.length()
        originParam = self.fnCurve.findParamFromLength( crvLength )
        
        points = []
        
        if equally:
            eacheLengthValue = crvLength / float( numPoint-1 )
            
            for i in range( numPoint ):
                point = self.openMaya.MPoint()
                paramValue = self.fnCurve.findParamFromLength( eacheLengthValue * i )
                self.fnCurve.getPointAtParam( paramValue, point )
                points.append( point )
        else:
            eacheParamValue = originParam / float( numPoint-1 )    
            
            for i in range( numPoint ):
                point = self.openMaya.MPoint()
                paramValue = eacheParamValue * i
                self.fnCurve.getPointAtParam( paramValue, point )
                points.append( point )
        
        return points
    
    

    def setJointNum( self, topJoint, endJoint, num, equally=True ):
        
        import sgBFunction_dag
        
        self.editCurveByJoints()
        
        jntFnH = [ None for i in self.jntH ]
        
        originLength = len( jntFnH )
        for i in range( originLength ):
            jntFnH[i] = om.MFnDagNode( sgBFunction_dag.getMObject( self.jntH[i] ) )
        
        diff = num - originLength
        if diff < 0:
            for jntFn in jntFnH[diff-1:-1]:
                jntChildren = cmds.listRelatives( jntFn.fullPathName(), c=1, f=1 )
                if not jntChildren: continue
                for child in jntChildren:
                    cmds.parent( child, w=1 )
                cmds.delete( jntFn.fullPathName() )
            jntFnH = jntFnH[:diff-1]+[jntFnH[-1]]
            cmds.parent( jntFnH[-1].fullPathName(), jntFnH[-2].fullPathName() )
        elif diff > 0:
            cmds.select( jntFnH[-2].fullPathName() )
            rad = cmds.getAttr( jntFnH[-2].fullPathName()+'.radius' )
            for i in range( diff ):
                jntFnH.insert( -1, om.MFnDagNode(sgBFunction_dag.getMObject( cmds.joint( rad=rad ) )) )
            cmds.parent( jntFnH[-1].fullPathName(), jntFnH[-2].fullPathName() )
        
        positions = self.getPositionFromCurve( num, equally )
        
        for i in range( 1, len( jntFnH )-1 ):
            cmds.move( positions[i].x, positions[i].y, positions[i].z, jntFnH[i].fullPathName(), ws=1, pcp=1 )
        
        self.updateJointH( topJoint )
        
        return topJoint



    def setPositionByValue(self, value, drag=False ):
        
        #poweredValues.append( self.numPoints-1 )
        if drag and not self.dragOn:
            self.dragOn = True
            cmds.undoInfo( swf=0 )
        
        if not drag and self.dragOn:
            self.setValueOlny( self.getGlobalValue() )
            self.dragOn = False
            cmds.undoInfo( swf=1 )
            self.setGlobalValue( value )
        
        self.setValueOlny( value )
        


    def setValueOlny( self, value ):
        
        divValue = float(self.numPoints-1)
        eacheRadValue = self.maxRadValue / divValue
        
        poweredValues = []
        
        for i in range( self.numPoints ):
            cuRadValue = i * eacheRadValue
            eacheValue   = self.sin( cuRadValue ) * divValue
            origValue    = i
            poweredValues.append( eacheValue * value + origValue *( 1-value ) )
        
        for i in range( 1, self.numPoints-1 ):
            point = self.openMaya.MPoint()
            self.fnCurve.getPointAtParam( poweredValues[i], point )
            cmds.move( point.x, point.y, point.z, self.jntH[i], ws=1, pcp=1 )


def orientJointRelatives( topJnt, aimIndex=0, upIndex=1 ):
    
    import sgBModel_data
    import sgBFunction_convert
    
    childJnt = cmds.listRelatives( topJnt, c=1, type='joint', f=1 )
    if not childJnt: 
        cmds.setAttr( topJnt+'.jo', 0,0,0 )
        cmds.setAttr( topJnt+'.r', 0,0,0 )
        return None
    childJnt = childJnt[0]
    childJntMtx = cmds.getAttr( childJnt+'.wm' )
    
    topJntParent = cmds.listRelatives( topJnt, p=1 )
    
    if not topJntParent: 
        parentMtx = sgBFunction_convert.convertMatrixToMMatrix( sgBModel_data.getDefaultMatrix() )
        upVector = om.MVector( 0, 1, 0 )
    else:
        parentMtx = sgBFunction_convert.convertMatrixToMMatrix( cmds.getAttr( topJntParent[0]+'.wm' ) )
        upVector = om.MVector( parentMtx( upIndex, 0 ), parentMtx( upIndex, 1 ), parentMtx( upIndex, 2 ) )
    
    topJntPos = om.MVector( *cmds.xform( topJnt, q=1, ws=1, t=1 ) )
    childJntPos = om.MVector( *cmds.xform( childJnt, q=1, ws=1, t=1 ) )
    aimVector = childJntPos - topJntPos
    
    crossVector = aimVector ^ upVector
    upVector = crossVector ^ aimVector
    
    upVector.normalize()
    aimVector.normalize()
    crossVector.normalize()
    
    crossIndex = 3 - ( aimIndex + upIndex )
    
    defaultMtx = sgBModel_data.getDefaultMatrix()
    defaultMtx[ aimIndex * 4 + 0 ] = aimVector.x
    defaultMtx[ aimIndex * 4 + 1 ] = aimVector.y
    defaultMtx[ aimIndex * 4 + 2 ] = aimVector.z
    defaultMtx[ upIndex * 4 + 0 ] = upVector.x
    defaultMtx[ upIndex * 4 + 1 ] = upVector.y
    defaultMtx[ upIndex * 4 + 2 ] = upVector.z
    defaultMtx[ crossIndex * 4 + 0 ] = crossVector.x
    defaultMtx[ crossIndex * 4 + 1 ] = crossVector.y
    defaultMtx[ crossIndex * 4 + 2 ] = crossVector.z

    orientMtx = sgBFunction_convert.convertMatrixToMMatrix( defaultMtx ) * parentMtx.inverse()
    
    trMtx = om.MTransformationMatrix( orientMtx )
    
    rot = trMtx.eulerRotation().asVector()
    
    import math
    cmds.setAttr( topJnt+'.jox', math.degrees( rot.x ) )
    cmds.setAttr( topJnt+'.joy', math.degrees( rot.y ) )
    cmds.setAttr( topJnt+'.joz', math.degrees( rot.z ) )
    cmds.setAttr( topJnt+'.r', 0,0,0 )
    
    cmds.xform( childJnt, ws=1, matrix=childJntMtx )
    
    orientJointRelatives( childJnt, aimIndex, upIndex )



def angleDriverBlendMatrixSetting( firstObject, secondObject, angleTarget, angleIndex=1 ):
    
    def getAngleDriverAttr( angleTarget, angleIndex ):
        
        driverCons = cmds.listConnections( angleTarget+'.m', type='angleDriver' )
        
        if driverCons:
            targetDriver = driverCons[0]
        else:
            targetDriver = cmds.createNode( 'angleDriver' )
            cmds.connectAttr( angleTarget+'.m', targetDriver+'.angleMatrix' )
        
        return targetDriver+'.outDriver%d' % angleIndex
    
    angleDriverAttr = getAngleDriverAttr( angleTarget, angleIndex )
    
    animCurve = cmds.createNode( 'animCurveUU' )
    blendMtxDcmp = cmds.createNode( 'blendTwoMatrixDecompose' )
    
    cmds.setKeyframe( animCurve, f=0, v=0 )
    cmds.setKeyframe( animCurve, f=1, v=1 )
    
    cmds.connectAttr( firstObject+'.m', blendMtxDcmp+'.inMatrix1' )
    cmds.connectAttr( secondObject+'.m', blendMtxDcmp+'.inMatrix2' )
    cmds.connectAttr( angleDriverAttr, animCurve+'.input' )
    cmds.connectAttr( animCurve+'.output', blendMtxDcmp+'.attributeBlender' )
    
    firstObjectParent = cmds.listRelatives( firstObject, p=1, f=1 )[0]
    cmds.select( firstObjectParent )
    jnt = cmds.joint()
    
    cmds.connectAttr( blendMtxDcmp+'.ot', jnt+'.t' )
    cmds.connectAttr( blendMtxDcmp+'.or', jnt+'.jo' )




def replaceConnectionToChildJoint( joint ):
    
    import sgBFunction_connection
    
    cmds.select( joint )
    jntName = joint.split( '|' )[-1]
    jntRad  = cmds.getAttr( joint + '.radius' )
    jnt = cmds.joint( n='Cjnt_' + jntName, rad = jntRad * 1.5 )
    
    sgBFunction_connection.replaceDestConnection( joint , jnt , 'skinCluster' )
    return jnt