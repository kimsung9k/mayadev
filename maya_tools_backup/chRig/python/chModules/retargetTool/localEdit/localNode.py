import maya.cmds as cmds
import maya.OpenMaya as om
import chModules.retargetTool.functions as fnc


class MeshShapeLocator:
    
    def __init__(self, name=None):
        
        self._name = name
        self.createControler()
    
    
    def createControler(self):
        
        node = cmds.createNode( "meshShapeLocator" )
        nodeTrans = cmds.listRelatives( node, p=1 )[0]
        
        if self._name: 
            nodeTrans = cmds.rename( nodeTrans, self._name )
            node = cmds.listRelatives( nodeTrans, s=1 )[0]
        
        cmds.connectAttr( node+'.output', nodeTrans+'.v' )
        
        self._node = node
        self._nodeTrans = nodeTrans


    def create3Torus(self):
        
        axisList = [ 'axisX', 'axisY', 'axisZ' ]
        
        fnc.clearArrayElement( self._node+'.shapes' )
        elementNum = fnc.getLastIndex( self._node+'.shapes' )+1
        
        for i in range( 3 ):
            torus = cmds.createNode( "polyTorus" )
            
            cmds.setAttr( torus+'.sectionRadius', 0.05 )
            cmds.setAttr( torus+'.subdivisionsHeight', 8 )
            cmds.setAttr( torus+'.subdivisionsAxis', 32 )
            
            cmds.setAttr( torus+'.'+axisList[i], .9 )
            cmds.setAttr( torus+'.'+axisList[(i+1)%3], 0 )
            cmds.setAttr( torus+'.'+axisList[(i+2)%3], 0 )
            
            cmds.connectAttr( torus+'.output', self._node+'.shapes[%d].inputMesh' % (elementNum+i) )


           

class RetargetLocator:
    
    def __init__(self, name=None ):
        
        self._name = name
        
        self.createLocator()
        
        
    def createLocator(self ):
        
        node = cmds.createNode( 'retargetLocator' )
        nodeTrans = cmds.listRelatives( node, p=1 )[0]
        
        if self._name: 
            nodeTrans = cmds.rename( nodeTrans, self._name )
            node = cmds.listRelatives( nodeTrans, s=1 )[0]
        
        cmds.connectAttr( node+'.output', nodeTrans+'.v' )
        cmds.connectAttr( nodeTrans+'.worldMatrix', nodeTrans+'.discMatrix' )
        
        self._node = node
        self._nodeTrans = nodeTrans
        
        
    def createSphere(self):
        
        sphereNode = cmds.createNode( "polySphere" )
        
        cmds.setAttr( sphereNode+'.subdivisionsAxis', 32 )
        cmds.setAttr( sphereNode+'.subdivisionsHeight', 16 )
        
        fnc.clearArrayElement( self._node+'.arrow' )
        elementNum = fnc.getLastIndex( self._node+'.arrow' )+1
        
        cmds.connectAttr( sphereNode+'.output', self._node+'.arrow[%d].inputMesh' % elementNum )
        
        


class ControlType1:
    
    
    def __init__(self, target, sourceWorld, targetWorld ):
        
        self._sourceNS = sourceWorld.replace( 'World_CTL', '' )
        self._targetNS = targetWorld.replace( 'World_CTL', '' )
        
        ctl = MeshShapeLocator()
        base = RetargetLocator()
        
        ctl.create3Torus()
        base.createSphere()
        base.createSphere()
        
        targetP = cmds.listRelatives( target, p=1 )[0]
        cmds.parent( ctl._nodeTrans, base._nodeTrans )
        cmds.parent( base._nodeTrans, targetP )
        
        cmds.setAttr( ctl._nodeTrans+'.t', 0,0,0 )
        cmds.setAttr( ctl._nodeTrans+'.r', 0,0,0 )
        cmds.setAttr( base._nodeTrans+'.t', 0,0,0 )
        cmds.setAttr( base._nodeTrans+'.r', 0,0,0 )
        
        self.targetConnect( target, ctl._nodeTrans, base._nodeTrans )
        
        self.setAttrBase( ctl._node, base._node )
        
        
        
    def targetConnect(self, target, ctl, base ):
        
        cmds.connectAttr( target+'.wm', base+'.arrow[1].aimMatrix' )
        
        beforeMatrixDcmpNode = self.getBeforeMatrixDcmpNode( target )
        
        if beforeMatrixDcmpNode:
            fnc.tryConnect( beforeMatrixDcmpNode+'.ot', base+'.t' )
            fnc.tryConnect( beforeMatrixDcmpNode+'.or', base+'.r' )
            cmds.connectAttr( base+'.wm', base+'.arrow[0].aimMatrix' )
            
        cmds.connectAttr( ctl+'.t', base+'.arrow[1].offset' )
        
        retargetNodes = self.getRetargetNodes( target )
        
        for retargetNode in retargetNodes:
            
            fnc.clearArrayElement( retargetNode+'.localData' )
            index = fnc.getLastIndex( retargetNode+'.localData' )+1
            
            cmds.connectAttr( base+'.wm', retargetNode+'.localData[%d].localMatrix' % index )
            try:
                cmds.connectAttr( ctl+'.m', retargetNode+'.localData[%d].localInOffset' % index )
            except:
                cmds.connectAttr( ctl+'.m', retargetNode+'.localData[%d].localOffset' % index )
            
            
            
    def setAttrBase(self, ctl, base ):
        
        for i in range( 3 ):
            cmds.setAttr( ctl+'.shapes[%d].meshSize' % i, 1.5 )
            cmds.setAttr( ctl+'.shapes[%d].fillAlpha' % i, 1 )
            cmds.setAttr( ctl+'.shapes[%d].lineAlpha' % i, 0 )
            cmds.setAttr( ctl+'.shapes[%d].defaultColor' % i , 0.2,1.0,0.976 )
        
        cmds.setAttr( base+'.discSize', 5,5,5 )
        cmds.setAttr( base+'.discFillAlpha', 0 )
        cmds.setAttr( base+'.discDefaultColor', 1,0,0 )
        cmds.setAttr( base+'.discDivision', 1 )
        
        cmds.setAttr( base+'.arrow[0].defaultColor', 1,0,0 )
        cmds.setAttr( base+'.arrow[0].fillAlpha', 1.0 )
        cmds.setAttr( base+'.arrow[0].lineAlpha', 0.0 )
        cmds.setAttr( base+'.arrow[0].startSize', 0.5 )
        cmds.setAttr( base+'.arrow[0].size', 0.0 )
        cmds.setAttr( base+'.arrow[1].defaultColor', 0,0,1 )
        cmds.setAttr( base+'.arrow[1].fillAlpha', 1.0 )
        cmds.setAttr( base+'.arrow[1].lineAlpha', 0.0 )
        cmds.setAttr( base+'.arrow[1].startSize', 0.5 )
        cmds.setAttr( base+'.arrow[1].size', 0.0 )
        
        
        
    def getRetargetNodes(self, target ):
        
        retargetBlender = cmds.listConnections( target, type='retargetBlender' )
        
        retargetTransCons = cmds.listConnections( retargetBlender, type='retargetTransNode', s=1, d=0 )
        retargetOrientCons = cmds.listConnections( retargetBlender, type='retargetOrientNode', s=1, d=0 )
        
        retargetNodes = []
        
        origName = target.replace( self._targetNS, '' )
        
        if retargetTransCons:
            if retargetTransCons[0].split( origName )[0] == self._sourceNS:
                retargetNodes.append( retargetTransCons[0] )
        if retargetOrientCons:
            if retargetOrientCons[0].split( origName )[0] == self._sourceNS:
                retargetNodes.append( retargetOrientCons[0] )
            
        return retargetNodes
    
        
        
    def getBeforeMatrixDcmpNode(self, target ):
        
        retargetNodes = self.getRetargetNodes( target )
            
        duRetargetNodes = []
        
        for retargetNode in retargetNodes:
            duRetargetNode= cmds.duplicate( retargetNode )[0]
            
            cons = cmds.listConnections( retargetNode, s=1, d=0, p=1, c=1 )
            
            outputs= cons[1::2]
            inputs = cons[::2]
            
            for i in range( len( outputs ) ):
                inputAttr = inputs[i].replace( retargetNode, duRetargetNode )
                cmds.connectAttr( outputs[i], inputAttr )
                
            duRetargetNodes.append( duRetargetNode )
                
        if duRetargetNodes:
        
            composeNode = cmds.createNode( 'composeMatrix' )
            beforeMatrixDcmpNode = cmds.createNode( 'multMatrixDecompose' )
        
            for duRetargetNode in duRetargetNodes:
                
                fnc.clearArrayElement( duRetargetNode+'.localData' )
                
                if cmds.nodeType( duRetargetNode ) == 'retargetTransNode':
                    cmds.connectAttr( duRetargetNode+'.output', composeNode+'.it' )
                if cmds.nodeType( duRetargetNode ) == 'retargetOrientNode':
                    cmds.connectAttr( duRetargetNode+'.outputRotate', composeNode+'.ir' )
            
            cmds.connectAttr( composeNode+'.outputMatrix', beforeMatrixDcmpNode+'.i[0]' )
                    
            return beforeMatrixDcmpNode


        

class ControlType2:
    
    
    def __init__(self, piv, *targets ):
        
        base = RetargetLocator()
        ctl = MeshShapeLocator()
        
        ctl.create3Torus()
        base.createSphere()
        base.createSphere()
        
        cmds.parent( base._nodeTrans, piv )
        cmds.parent( ctl._nodeTrans, base._nodeTrans )
        
        cmds.setAttr( base._nodeTrans+'.t', 0,0,0 )
        cmds.setAttr( base._nodeTrans+'.r', 0,0,0 )
        cmds.setAttr( ctl._nodeTrans+'.t', 0,0,0 )
        cmds.setAttr( ctl._nodeTrans+'.r', 0,0,0 )
        
        for i in range( len( targets ) ):
            self.targetConnect( targets[i], ctl._nodeTrans, base._nodeTrans, i )
            self.setAttrBase( ctl._node, base._node, i )
        
        
    def targetConnect(self, target, ctl, base, targetIndex ):
        
        cmds.connectAttr( target+'.wm', base+'.arrow[%d].aimMatrix' % (targetIndex*2+1) )
        
        beforeMatrixNode = self.getBeforeMatrixNode( target )
        
        if beforeMatrixNode:
            cmds.connectAttr( beforeMatrixNode+'.o', base+'.arrow[%d].aimMatrix' % (targetIndex*2) )
            
        cmds.connectAttr( ctl+'.t', base+'.arrow[%d].offset' % (targetIndex*2+1) )
        retargetNodes = self.getRetargetNodes( target )
        
        for retargetNode in retargetNodes:
            
            fnc.clearArrayElement( retargetNode+'.localData' )
            index = fnc.getLastIndex( retargetNode+'.localData' )+1
            
            cmds.connectAttr( base+'.wm', retargetNode+'.localData[%d].localMatrix' % index )
            try:
                cmds.connectAttr( ctl+'.m', retargetNode+'.localData[%d].localOutOffset' % index )
            except:
                cmds.connectAttr( ctl+'.m', retargetNode+'.localData[%d].localOffset' % index )
            
            if not cmds.attributeQuery( 'localMult', node=base, ex=1 ):
                selList = om.MSelectionList()
                selList.add( base )
                
                mObj = om.MObject()
                selList.getDependNode( 0, mObj )

                nAttr = om.MFnNumericAttribute()
                
                aAttrX = nAttr.create( "localMultX", "localMultX", om.MFnNumericData.kDouble, 1.0 )
                nAttr.setMin( 0.0 )
                aAttrY = nAttr.create( "localMultY", "localMultY", om.MFnNumericData.kDouble, 1.0 )
                nAttr.setMin( 0.0 )
                aAttrZ = nAttr.create( "localMultZ", "localMultZ", om.MFnNumericData.kDouble, 1.0 )
                nAttr.setMin( 0.0 )
                aAttr = nAttr.create( 'localMult','localMult', aAttrX, aAttrY, aAttrZ )
                nAttr.setKeyable( True )
                nAttr.setStorable( True )
            
                modify = om.MDGModifier()
                modify.addAttribute( mObj, aAttr )
                modify.doIt()
                
            if not cmds.attributeQuery( 'localMultOrient', node=base, ex=1 ):
                cmds.addAttr( base, ln='localMultOrient', min=0, dv=1 )
                cmds.setAttr( base+'.localMultOrient', e=1, k=1 )
            
            try: 
                cmds.connectAttr( base+'.localMult', retargetNode+'.localData[%d].localMult' % index )
            except:
                cmds.connectAttr( base+'.localMultOrient', retargetNode+'.localData[%d].localMult' % index )
            
            
    def setAttrBase(self, ctl, base, targetIndex ):
        
        for i in range( 3 ):
            cmds.setAttr( ctl+'.shapes[%d].meshSize' % i, 1.5 )
            cmds.setAttr( ctl+'.shapes[%d].fillAlpha' % i, 1 )
            cmds.setAttr( ctl+'.shapes[%d].lineAlpha' % i, 0 )
            cmds.setAttr( ctl+'.shapes[%d].defaultColor' % i , 0.2,1.0,0.976 )
        
        cmds.setAttr( base+'.discSize', 5,5,5 )
        cmds.setAttr( base+'.discFillAlpha', 0 )
        
        cmds.setAttr( base+'.discDefaultColor', 1,0,0 )
        
        cmds.setAttr( base+'.arrow[%d].defaultColor' % targetIndex, 1,0,0 )
        cmds.setAttr( base+'.arrow[%d].fillAlpha' % targetIndex, 1.0 )
        cmds.setAttr( base+'.arrow[%d].lineAlpha' % targetIndex, 0.0 )
        cmds.setAttr( base+'.arrow[%d].defaultColor' % (targetIndex+1), 0,0,1 )
        cmds.setAttr( base+'.arrow[%d].fillAlpha' % (targetIndex+1), 1.0 )
        cmds.setAttr( base+'.arrow[%d].lineAlpha' % (targetIndex+1), 0.0 )
        
        
        
    def getRetargetNodes(self, target ):
        
        retargetTransCons = cmds.listConnections( target, type='retargetTransNode', s=1, d=0 )
        retargetOrientCons = cmds.listConnections( target, type='retargetOrientNode', s=1, d=0 )
        
        retargetNodes = []
        
        if retargetTransCons:
            retargetNodes.append( retargetTransCons[0] )
        if retargetOrientCons:
            retargetNodes.append( retargetOrientCons[0] )
            
        return retargetNodes
    
        
        
    def getBeforeMatrixNode(self, target ):
        
        retargetNodes = self.getRetargetNodes( target )
            
        duRetargetNodes = []
        
        for retargetNode in retargetNodes:
            duRetargetNode= cmds.duplicate( retargetNode )[0]
            
            cons = cmds.listConnections( retargetNode, s=1, d=0, p=1, c=1 )
            
            outputs= cons[1::2]
            inputs = cons[::2]
            
            for i in range( len( outputs ) ):
                inputAttr = inputs[i].replace( retargetNode, duRetargetNode )
                cmds.connectAttr( outputs[i], inputAttr )
                
            duRetargetNodes.append( duRetargetNode )
                
        if duRetargetNodes:
        
            composeNode = cmds.createNode( 'composeMatrix' )
            beforeMatrixNode = cmds.createNode( 'multMatrix' )
        
            for duRetargetNode in duRetargetNodes:
                
                fnc.clearArrayElement( duRetargetNode+'.localData' )
                
                if cmds.nodeType( duRetargetNode ) == 'retargetTransNode':
                    cmds.connectAttr( duRetargetNode+'.output', composeNode+'.it' )
                if cmds.nodeType( duRetargetNode ) == 'retargetOrientNode':
                    cmds.connectAttr( duRetargetNode+'.outputRotate', composeNode+'.ir' )
            
            targetP = cmds.listRelatives( target, p=1 )[0]
            cmds.connectAttr( composeNode+'.outputMatrix', beforeMatrixNode+'.i[0]' )
            cmds.connectAttr( targetP+'.wm', beforeMatrixNode+'.i[1]' )
                    
            return beforeMatrixNode
    
    
class CurveType:
    
    def __init__( self, target, sourceCrv, targetCrv, retargetNamespace ):
        
        self._target = target
        self._sourceCrv = sourceCrv
        self._targetCrv = targetCrv
        self._namespace = retargetNamespace
    
    
    def connect(self):
        
        retargetBlenderCons = cmds.listConnections( self._target, s=1, d=0, type='retargetBlender' )

        if not retargetBlenderCons: return None
        
        retargetBlender = retargetBlenderCons[0]
        
        connectedIndex = self.getConnectedIndex( retargetBlender, self._namespace )
        
        if connectedIndex == -1: return None
        
        if self.isCurveConnected( retargetBlender, self._namespace ):
            self.replaceSourceAndDestCurve( retargetBlender, self._namespace, self._sourceCrv, self._targetCrv )
            return None
        
        retargetTrans = cmds.listConnections( retargetBlender+'.input[%d].transMatrix' % connectedIndex )[0]
        retargetOrient = cmds.listConnections( retargetBlender+'.input[%d].orientMatrix' % connectedIndex )[0]
        
        duTrans = cmds.duplicate( retargetTrans, inputConnections=1, n=self._target+'_duTransForLocalCrv' )[0]
        duOrient = cmds.duplicate( retargetOrient, inputConnections=1, n=self._target+'_duOrientForLocalCrv' )[0]
        
        combineMatrix = cmds.createNode( 'transRotateCombineMatrix', n=self._target+'_combineMtxForLocalCrv' )
        
        cmds.connectAttr( duTrans+'.transMatrix', combineMatrix+'.inputTransMatrix' )
        cmds.connectAttr( duOrient+'.orientMatrix', combineMatrix+'.inputRotateMatrix' )
        
        multMatrix = cmds.createNode( 'multMatrix', n=self._target+'_multForLocalCrv' )
        
        targetP = cmds.listRelatives( self._target, p=1 )[0]
        cmds.connectAttr( combineMatrix+'.outputMatrix', multMatrix+'.i[0]' )
        cmds.connectAttr( targetP+'.wm', multMatrix+'.i[1]' )
        
        sourceShape = cmds.listRelatives( self._sourceCrv, s=1 )[0]
        targetShape = cmds.listRelatives( self._targetCrv, s=1 )[0]
        sourceWorldShape = cmds.createNode( 'transformGeometry', n=self._target+'_sourceWorldShape' )
        targetWorldShape = cmds.createNode( 'transformGeometry', n=self._target+'_targetWorldShape' )
        cmds.connectAttr( self._sourceCrv+'.wm', sourceWorldShape+'.transform' )
        cmds.connectAttr( self._targetCrv+'.wm', targetWorldShape+'.transform' )
        cmds.connectAttr( sourceShape+'.local', sourceWorldShape+'.inputGeometry' )
        cmds.connectAttr( targetShape+'.local', targetWorldShape+'.inputGeometry' )
        
        editMtxByCurve = cmds.createNode( 'editMatrixByCurve', n=self._target+'_editMtx' )
        
        cmds.connectAttr( sourceWorldShape+'.outputGeometry', editMtxByCurve+'.sourceCurve' )
        cmds.connectAttr( targetWorldShape+'.outputGeometry', editMtxByCurve+'.destCurve' )
        cmds.connectAttr( multMatrix+'.matrixSum', editMtxByCurve+'.sourceMatrix' )
        cmds.connectAttr( targetP+'.wm', editMtxByCurve+'.upMatrix' )
        
        cuIndex = fnc.getLastIndex( retargetTrans+'.localData' )+1
        cmds.connectAttr( editMtxByCurve+'.outSourceMatrix', retargetTrans+'.localData[%d].localMatrix' % cuIndex )
        cmds.connectAttr( editMtxByCurve+'.outOffsetMatrix', retargetTrans+'.localData[%d].localOffset' % cuIndex )
        cmds.connectAttr( editMtxByCurve+'.outSourceMatrix', retargetOrient+'.localData[%d].localMatrix' % cuIndex )
        cmds.connectAttr( editMtxByCurve+'.outOffsetMatrix', retargetOrient+'.localData[%d].localOutOffset' % cuIndex )
        
        
    def getConnectedIndex(self, blender, namespace ):
        
        retargetCons = cmds.listConnections( blender, s=1, d=0, p=1, c=1, type='retargetTransNode' )
        
        outputs = retargetCons[1::2]
        
        for i in range( len( outputs ) ):
            if outputs[i].find( namespace ) == 0:
                return i
            
        return -1
    


    def isCurveConnected(self, blender, namespace ):
        
        index = self.getConnectedIndex( blender, namespace )
        
        retargetTrans = cmds.listConnections( blender+'.input[%d].transMatrix' % index )[0]
        
        if cmds.listConnections( retargetTrans, s=1, d=0, type='editMatrixByCurve' ):
            return True
        
        return False
    


    def getEditMatrixNode(self, blender, namespace ):
        
        index = self.getConnectedIndex( blender, namespace )
        
        retargetTrans = cmds.listConnections( blender+'.input[%d].transMatrix' % index )[0]
        
        cons = cmds.listConnections( retargetTrans, s=1, d=0, type='editMatrixByCurve' )
        
        if not cons: return None
        
        return cons[0]

    

    def replaceSourceAndDestCurve(self, blender, namespace, source, dest ):
        
        self.getConnectedIndex( blender, namespace )
        
        editMtxNode = self.getEditMatrixNode( blender, namespace )
        
        sourceGeo = cmds.listConnections( editMtxNode+'.sourceCurve' )[0]
        destGeo   = cmds.listConnections( editMtxNode+'.destCurve' )[0]
        
        sourceShape = cmds.listRelatives( source, s=1 )[0]
        destShape   = cmds.listRelatives( dest, s=1 )[0]
        
        fnc.tryConnect( source+'.wm', sourceGeo+'.transform')
        fnc.tryConnect( sourceShape+'.local', sourceGeo+'.inputGeometry')
        fnc.tryConnect( dest+'.wm', destGeo+'.transform')
        fnc.tryConnect( destShape+'.local', destGeo+'.inputGeometry')
        