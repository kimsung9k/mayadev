import maya.cmds as cmds
import maya.OpenMaya as om
import topInfo
import distObjInfo
import functions as fnc


class TopInfo:
    
    def __init__(self):
        
        self._origin = topInfo.orientOrigin
        self._transDirect = topInfo.transDirect
        self._orientOrigin = topInfo.orientOriginRate
        self._transOrigin = topInfo.transOriginRate
        self._target = topInfo.target
        self._targetNS = topInfo.targetNS
        self._sourceNS = topInfo.sourceNS
        self._parentList = topInfo.parentList
        self._transParent = topInfo.transParent
        self._udAttrs = topInfo.udAttrs
        
        
    def blenderToControl( self, blender, controler ):

        keyAttrs = cmds.listAttr( controler, k=1 )
        
        outAttrs = ['outTransX', 'outTransY', 'outTransZ', 'outOrientX', 'outOrientY', 'outOrientZ' ]
        inAttrs = ['translateX','translateY','translateZ','rotateX','rotateY','rotateZ']
        
        for i in range( len( outAttrs ) ):
            inAttr = inAttrs[i]
            outAttr = outAttrs[i]
            
            if inAttr in keyAttrs:
                fnc.tryConnect( blender+'.'+outAttr, controler+'.'+inAttr )

        
class getTransRetargetNode( TopInfo ):
    
    def __init__(self):
        
        TopInfo.__init__(self)
        
        node = self.getRetargetNode_for( self._target )
        
        self.originRate = node+'.originalRate'
        self.source = node+'.sourceMatrix'
        self.sourceOrig = node+'.sourceOrigMatrix'
        self.sourceParent = node+'.sourceParentMatrix'
        self.targetOrig = node+'.targetOrigMatrix'
        self.targetParent = node+'.targetParentMatrix'
        self.distRate = node+'.distanceRate'
        self.localData = [ node+'.localData[0].localMatrix', node+'.localData[0].localOffset' ]
        
        
        if self._transDirect:
            transDirect = cmds.createNode( "multMatrixDecompose", n= self._target+'_transDirect' )
            invNode = cmds.createNode( 'inverseMatrix', n= self._target+'_transDirect_origInv' )
            multNode = cmds.createNode( 'multiplyDivide', n=self._target+'_transDirect_mult' )
            cmds.connectAttr( self.source, transDirect+'.i[0]' )
            cmds.connectAttr( self.sourceOrig, invNode+'.inputMatrix' )
            cmds.connectAttr( invNode+'.outputMatrix', transDirect+'.i[1]' )
            cmds.connectAttr( transDirect+'.ot', multNode+'.input1' )
            cmds.connectAttr( self.distRate, multNode+'.input2X' )
            cmds.connectAttr( self.distRate, multNode+'.input2Y' )
            cmds.connectAttr( self.distRate, multNode+'.input2Z' )
            cmds.connectAttr( multNode+'.outputX', self._target+'.tx', f=1 )
            cmds.connectAttr( multNode+'.outputY', self._target+'.ty', f=1 )
            cmds.connectAttr( multNode+'.outputZ', self._target+'.tz', f=1 )
            
    
    def getRetargetNode_for( self, target ):
        
        retargetBlenderCons = cmds.listConnections( target, s=1, d=0, type='retargetBlender' )
        
        if not retargetBlenderCons:
            retargetBlender = cmds.createNode( 'retargetBlender', n= target+'_retargetBlender' )
            
            sourceName = target.replace( self._targetNS, self._sourceNS )
            retargetNode = cmds.createNode( 'retargetTransNode', n= sourceName+'_RTTrans' )
            
            self.blenderToControl( retargetBlender, target )
            
            if cmds.nodeType( target ) == 'joint':
                fnc.tryConnect( target+'.jo', retargetBlender+'.orient' )
            
            cmds.connectAttr( retargetNode+'.transMatrix', retargetBlender+'.input[0].transMatrix' )
        
        else:
            retargetBlender = retargetBlenderCons[0]
            fnc.clearArrayElement( retargetBlender+'.input' )
            cuIndex = fnc.getLastIndex( retargetBlender+'.input' )
            
            if cuIndex == -1: cuIndex = 0
            retargetTransCons = cmds.listConnections( retargetBlender+'.input[%d].transMatrix ' % cuIndex )
            
            if retargetTransCons: cuIndex += 1
            
            sourceName = target.replace( self._targetNS, self._sourceNS )
            retargetNode = cmds.createNode( 'retargetTransNode', n= sourceName+'_RTTrans' )
            
            cmds.connectAttr( retargetNode+'.transMatrix', retargetBlender+'.input[%d].transMatrix' % cuIndex )
        
        return retargetNode
            


       
class getOrientRetargetNode( TopInfo ):
    
    def __init__(self):
        
        TopInfo.__init__(self)
        
        node = self.getRetargetNode_for( self._target )
        
        self.originRate = node+'.originalRate'
        self.source = node+'.sourceMatrix'
        self.sourceOrig = node+'.sourceOrigMatrix'
        self.sourceParent = node+'.sourceParentMatrix'
        self.targetOrig = node+'.targetOrigMatrix'
        self.targetParent = node+'.targetParentMatrix'
        
        
    def getRetargetNode_for( self, target ):
        
        retargetBlenderCons = cmds.listConnections( target, s=1, d=0, type='retargetBlender' )
        
        if not retargetBlenderCons:
            retargetBlender = cmds.createNode( 'retargetBlender', n= target+'_retargetBlender' )
            
            self.blenderToControl( retargetBlender, target )
            
            sourceName = target.replace( self._targetNS, self._sourceNS )
            retargetNode = cmds.createNode( 'retargetOrientNode', n= sourceName+'_RTOrient' )
            
            if cmds.nodeType( target ) == 'joint':
                cmds.connectAttr( target+'.jo', retargetBlender+'.orient' )
            
            cmds.connectAttr( retargetNode+'.orientMatrix', retargetBlender+'.input[0].orientMatrix' )
        
        else:
            retargetBlender = retargetBlenderCons[0]
            fnc.clearArrayElement( retargetBlender+'.input' )
            cuIndex = fnc.getLastIndex( retargetBlender+'.input' )
            
            if cuIndex < 0: cuIndex = 0
            
            retargetOrientCons = cmds.listConnections( retargetBlender+'.input[%d].orientMatrix ' % cuIndex )
            
            if retargetOrientCons: cuIndex += 1
            
            sourceName = target.replace( self._targetNS, self._sourceNS )
            retargetNode = cmds.createNode( 'retargetOrientNode', n= sourceName+'_RTOrient' )
            
            cmds.connectAttr( retargetNode+'.orientMatrix', retargetBlender+'.input[%d].orientMatrix' % cuIndex )

        return retargetNode

        

class transOriginRate:
    
    def __init__(self, pointer ):
        
        self._pointer = pointer
    
    def __rshift__(self, retargetInst ):
        
        cmds.setAttr( retargetInst.originRate , self._pointer._transOrigin )

        
        
class orientOriginRate:
    
    def __init__(self, pointer ):
        
        self._pointer = pointer
    
    def __rshift__(self, retargetInst ):
        
        cmds.setAttr( retargetInst.originRate, self._pointer._orientOrigin )
        
        
        
class getOriginRate( TopInfo ):
    
    def __init__(self):
        
        TopInfo.__init__(self)
        
        self.trans  = transOriginRate(self)
        self.orient = orientOriginRate(self)


class getTransSource:
    
    def __init__( self, pointer ):
        
        if pointer._targetNS:
            self._name = pointer._target.replace( pointer._targetNS, pointer._sourceNS )
        else:
            self._name = pointer._target
        
    
    def __rshift__( self, retargetInst ):

        fnc.tryConnect( self._name+'.wm', retargetInst.source )


class getOrientSource:
    
    def __init__( self, pointer ):
        
        if pointer._targetNS:
            self._name = pointer._target.replace( pointer._targetNS, pointer._sourceNS )
        else:
            self._name = pointer._target
        
    
    def __rshift__( self, retargetInst ):

        fnc.tryConnect( self._name+'.wm', retargetInst.source )
                
                
class getSource( TopInfo ):
    
    def __init__(self):
        
        TopInfo.__init__(self )
        
        self.trans = getTransSource( self )
        self.orient = getOrientSource( self )
    


class getSourceOrig( TopInfo ):
    
    def __init__( self ):
        
        TopInfo.__init__( self )
        
        if self._targetNS:
            source = self._target.replace( self._targetNS, self._sourceNS )
        else:
            source = self._target
        
        
        if cmds.nodeType( source ) == 'dgTransform':
            self._name = source
        else:
            self._name = cmds.listRelatives( source, p=1 )[0]
        
    def __rshift__( self, retargetInst ):
        
        if cmds.nodeType( self._name ) == 'dgTransform':
            fnc.tryConnect( self._name+'.pm', retargetInst.sourceOrig )
        else:
            fnc.tryConnect( self._name +'.wm', retargetInst.sourceOrig )
    
    

class getTargetOrig( TopInfo ):
    
    
    def __init__( self ):
        
        TopInfo.__init__( self )
        
        if self._origin:
            self._name = self._targetNS+self._origin
        else:
            if cmds.nodeType( self._target ) == 'dgTransform':
                self._name = self._target
            else:
                self._name = cmds.listRelatives( self._target, p=1 )[0]

    def __rshift__( self, retargetInst ):
        
        if cmds.nodeType( self._name ) == 'dgTransform':
            fnc.tryConnect( self._name+'.pm', retargetInst.targetOrig )
        else:
            fnc.tryConnect( self._name +'.wm', retargetInst.targetOrig )
    


class getDistNode( TopInfo ):
    
    
    def __init__( self ):

        TopInfo.__init__( self )

        origName = self._target.replace( self._targetNS, '' )

        distObjInfos = distObjInfo.getDistObjByName( origName )

        if distObjInfos:
            upperObj, lowerObj, part = distObjInfos

            worldCtl = self._targetNS+'World_CTL'
            worldShape = cmds.listRelatives( worldCtl, s=1 )[0]

            if not cmds.attributeQuery( part, node=worldShape, ex=1 ):
                msgAttr = om.MFnMessageAttribute()
                attr = msgAttr.create( part, part )
                msgAttr.setArray( True )
                selList = om.MSelectionList()
                selList.add( worldShape )
                mObj = om.MObject()
                selList.getDependNode( 0,mObj )
                fnNode = om.MFnDependencyNode( mObj )
                fnNode.addAttribute( attr )
            
            fnc.clearArrayElement( worldShape+'.%s' % part )
            cons = cmds.listConnections( worldShape+'.%s' % part )
            
            distNodeExist = False
            
            if cons:
                for con in cons:
                    if con.find( self._sourceNS ) != -1:
                        self._name = con
                        distNodeExist = True
                        break
            
            if not distNodeExist:
                sUpperDist = cmds.createNode( 'distanceBetween', n= part+'_sUpperDist' )
                sLowerDist = cmds.createNode( 'distanceBetween', n= part+'_sLowerDist' )
                tUpperDist = cmds.createNode( 'distanceBetween', n= part+'_tUpperDist' )
                tLowerDist = cmds.createNode( 'distanceBetween', n= part+'_tLowerDist' )
                
                sDistAll = cmds.createNode( 'addDoubleLinear', n=part+'_sDistAll' )
                tDistAll = cmds.createNode( 'addDoubleLinear', n=part+'_tDistAll' )
                
                distRateNode = cmds.createNode( 'multiplyDivide', n=self._sourceNS+part+'_distRate' )
                cmds.setAttr( distRateNode+'.op', 2 )
                
                cmds.connectAttr( self._sourceNS+upperObj+'.t', sUpperDist+'.point1' )
                cmds.connectAttr( self._sourceNS+lowerObj+'.t', sLowerDist+'.point1' )
                cmds.connectAttr( self._targetNS+upperObj+'.t', tUpperDist+'.point1' )
                cmds.connectAttr( self._targetNS+lowerObj+'.t', tLowerDist+'.point1' )
                
                cmds.connectAttr( sUpperDist+'.distance', sDistAll+'.input1' )
                cmds.connectAttr( sLowerDist+'.distance', sDistAll+'.input2' )
            
                cmds.connectAttr( tUpperDist+'.distance', tDistAll+'.input1' )
                cmds.connectAttr( tLowerDist+'.distance', tDistAll+'.input2' )
            
                cmds.connectAttr( sDistAll+'.output', distRateNode+'.input2X' )
                cmds.connectAttr( tDistAll+'.output', distRateNode+'.input1X' )
                
                connectIndex = fnc.getLastIndex( worldShape+'.%s' % part )+1
                cmds.connectAttr( distRateNode+'.message', worldShape+'.%s[%d]' % (part,connectIndex) )
                
                self._name = distRateNode
        else:
            self._name = None
        
        
    def __rshift__( self, retargetInst ):
        
        if not self._name: return None
        
        fnc.tryConnect( self._name +'.outputX', retargetInst.distRate )
        
        
        
class getUdAttrs( TopInfo ):

    def __init__(self):
        
        TopInfo.__init__( self )
        
        self._source = self._target.replace( self._targetNS, self._sourceNS )
        
        udAttrBlenderCons = cmds.listConnections( self._target, s=1, d=0, type='udAttrBlender' )
        
        if udAttrBlenderCons:
            self._udAttrNode = udAttrBlenderCons[0]
            fnc.clearArrayElement( self._udAttrNode+'.input' )
            self._cuIndex    = fnc.getLastIndex( self._udAttrNode+'.input' )+1
        else:
            self._udAttrNode = cmds.createNode( 'udAttrBlender', n= self._target+'_udAttrBl' )
            self._cuIndex    = 0
        
        
    def __rshift__( self, retargetInst ):
        
        for i in range( len( self._udAttrs ) ):
            
            udAttrInput = self._udAttrNode+'.input[%d].udAttr[%d]' %( self._cuIndex, i )
            udAttrOutput = self._udAttrNode+'.outUdAttr[%d]' % i
            
            if not cmds.attributeQuery( self._udAttrs[i], node= self._source, ex=1 ): break
            
            cons = cmds.listConnections( self._source+'.'+self._udAttrs[i], s=1, d=0, p=1, c=1 )
            if not cons:
                cmds.setAttr( udAttrInput, cmds.getAttr( self._source+'.'+self._udAttrs[i] ) )
            else:
                output= cons[1]
                cmds.connectAttr( output, udAttrInput, f=1 )
            
            if not cmds.isConnected( udAttrOutput, self._target+'.'+self._udAttrs[i] ):
                try:cmds.connectAttr( udAttrOutput, self._target+'.'+self._udAttrs[i], f=1 )
                except: pass



class getSourceFollow( TopInfo ):
    
    def __init__( self ):
        
        TopInfo.__init__(self)
        
        originalParent = self._sourceNS+self._parentList[0]
        
        followMtx = cmds.createNode( 'followMatrix', n=self._target+'_sourceFollow' )
        
        if self._transParent:
            combineNode = fnc.getCombineNode_from( self._sourceNS+self._transParent, originalParent )
            cmds.connectAttr( combineNode+'.outputMatrix', followMtx+'.originalMatrix' )
        else:
            cmds.connectAttr( originalParent+'.wm', followMtx+'.originalMatrix' )
        for i in range( 1, len( self._parentList ) ):
            parent = self._sourceNS+self._parentList[i]
            
            if self._transParent:
                combineNode = fnc.getCombineNode_from( self._sourceNS+self._transParent, parent )
                cmds.connectAttr( combineNode+'.outputMatrix', followMtx+'.inputMatrix[%d]' % ( i-1 ) )
            else:
                cmds.connectAttr( parent+'.wm', followMtx+'.inputMatrix[%d]' % ( i-1 ) )

        self._name = followMtx
        
        
    def __rshift__( self, retargetInst ):
        
        if not cmds.isConnected( self._name+'.outputMatrix', retargetInst.sourceParent ):
            cmds.connectAttr( self._name +'.outputMatrix', retargetInst.sourceParent, f=1 )
    

        
class getTargetFollow( TopInfo ):
    
    
    def __init__( self ):
        
        TopInfo.__init__(self)
        
        originalParent = self._targetNS+self._parentList[0]

        followMtx = cmds.createNode( 'followMatrix', n=self._target+'_targetFollow' )
        
        if self._transParent:
            combineNode = fnc.getCombineNode_from( self._targetNS+self._transParent, originalParent )
            cmds.connectAttr( combineNode+'.outputMatrix', followMtx+'.originalMatrix' )
        else:
            cmds.connectAttr( originalParent+'.wm', followMtx+'.originalMatrix' )
            
        for i in range( 1, len( self._parentList ) ):
            parent = self._targetNS+self._parentList[i]
            
            if self._transParent:
                combineNode = fnc.getCombineNode_from( self._targetNS+self._transParent, parent )
                cmds.connectAttr( combineNode+'.outputMatrix', followMtx+'.inputMatrix[%d]' % ( i-1 ) )
            else:
                cmds.connectAttr( parent+'.wm', followMtx+'.inputMatrix[%d]' % ( i-1 ) )
        
        self._name = followMtx 
        
        
    def __rshift__( self, retargetInst ):
        
        if not cmds.isConnected( self._name+'.outputMatrix', retargetInst.targetParent ):
            cmds.connectAttr( self._name +'.outputMatrix', retargetInst.targetParent, f=1 )