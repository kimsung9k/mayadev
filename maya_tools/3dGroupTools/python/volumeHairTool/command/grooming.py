import maya.cmds as cmds
import maya.OpenMaya as om
import maya.mel as mel
import functions as fnc

class SetCurve:
    
    def __init__(self, surfaces, surfGrp, setName, mode, eachSurface = False ):
        
        self._setNames = []
        
        if eachSurface:
            crvGrps = []
            crvs = []
            for surface in surfaces:
                if cmds.nodeType( surface ) == 'nurbsCurve':
                    crv = cmds.listRelatives( surface, p=1 )[0]
                    if not crv in crvs:
                        crvs.append( crv )
                    continue
                elif cmds.nodeType( surface ) == 'nurbsSurface':
                    surfaceObj = cmds.listRelatives( surface, p=1 )[0]
                    cons = cmds.listConnections( surfaceObj+'.volumeCurveGrp', s=1, d=0 )
                    if not cons: continue
                    crvGrps.append( self.findChildCurves( cons[0] ) )
            if crvs:
                crvGrps.append( crvs )
            
            j = 0
            for crvGrp in crvGrps:
                self.setGroup( crvGrp, surfGrp, setName+'_%d' % j )
                if crvGrp: j+=1
                    
        else:
            crvs = []
            
            for surface in surfaces:
                
                if cmds.nodeType( surface ) == 'nurbsCurve':
                    crv = cmds.listRelatives( surface, p=1 )[0]
                    if not crv in crvs:
                        crvs.append( crv )
                    continue
                    
                surfaceObj = cmds.listRelatives( surface, p=1 )[0]
                
                if not cmds.attributeQuery( 'volumeCurveGrp', node=surfaceObj, ex=1):
                    continue
                
                cons = cmds.listConnections( surfaceObj+'.volumeCurveGrp', s=1, d=0 )
                if not cons: continue
                crvs += self.findChildCurves( cons[0] )
    
            if mode == 'set':
                self.setGroup( crvs, surfGrp, setName )
            elif mode == 'reset':
                self.resetGroup( crvs, surfGrp, setName )
    
    
    def findChildCurves(self, topGrp ):
        
        children = cmds.listRelatives( topGrp, c=1, ad=1, type='transform' )
        
        if not children: return []
        
        crvObjs = []
        
        for child in children:
            
            if cmds.listRelatives( child, s=1 ):
                crvObjs.append( child )
                
        return crvObjs
    
    def setGroup(self, targetObjs, surfGrp, setName ):
  
        if not targetObjs:
            cmds.warning( "Target surface has no curve" ) 
            return None
        setObj = cmds.sets( targetObjs )
        setObj = cmds.rename( setObj, setName )
        
        self._setNames.append( setObj )
        
        fnc.clearArrayElement( surfGrp+'.sets' )
        cuIndex = fnc.getLastIndex( surfGrp+'.sets' )+1
        
        cmds.connectAttr( setObj+'.message', surfGrp+'.sets[%d]' % cuIndex )
        
        
    def resetGroup(self, targetObjs, surfGrp, setName ):
  
        if not targetObjs:
            cmds.warning( "Target surface has no curve" ) 
            return None
        
        setElements = cmds.sets( setName, q=1 )
        
        for element in setElements:
            cmds.sets( element, remove=setName )
        
        for targetObj in targetObjs:
            if not cmds.sets( targetObj, im=setName ):
                cmds.sets( targetObj, addElement=setName )
        

        
class SetYeti:
    
    def __init__(self, mesh, surfGrp, setsList ):
        
        yeti = self.getYetiNode( surfGrp, mesh )
        self.getMeshNode( mesh )
        
        cons =cmds.listConnections( yeti+'.guideSets', s=1, d=0, p=1, c=1 )
        
        if cons:
            outputs = cons[1::2]
            inputs  = cons[0::2]
            
            for i in range( len(outputs) ):
                cmds.disconnectAttr( outputs[i], inputs[i] )
        
        for i in range( len( setsList ) ):
            print setsList[i]
            cmds.connectAttr( setsList[i]+'.usedBy[0]', yeti+'.guideSets[%d]' % i )
            
        
    def getYetiNode( self, surfGrp, mesh ):
            
        cons = cmds.listConnections( mesh+'.worldMesh', type='pgYetiMaya' )
        
        if cons:
            return cons[0]
        
        yetiNode = cmds.createNode( 'pgYetiMaya', n=surfGrp+"_yetiShape" )
        yetiObject = cmds.listRelatives( yetiNode, p=1 )[0]
        cmds.rename( yetiObject, yetiNode.replace( 'yetiShape', 'yeti' ) )
        
        cmds.connectAttr( mesh+'.worldMesh[0]', yetiNode+'.inputGeometry[0]' )
        
        return yetiNode
    
    
    def getMeshNode(self, mesh ):
        
        cons = cmds.listConnections( mesh+'.referenceObject', s=1, d=0 )
        if not cons:
            meshP = cmds.listRelatives( mesh, p=1 )[0]
            refMeshObj = cmds.duplicate( meshP, n=meshP+'_refObj' )[0]
            refMeshShape = cmds.listRelatives( refMeshObj, s=1 )[0]
            cmds.connectAttr( refMeshShape+'.message', mesh+'.referenceObject' )
            
            cons = cmds.listConnections( refMeshShape+'.worldMesh', type='pgYetiMaya', p=1, c=1 )
            cmds.disconnectAttr( cons[0], cons[1] )
            
            cmds.connectAttr( meshP+'.t', refMeshObj+'.t' )
            cmds.connectAttr( meshP+'.r', refMeshObj+'.r' )
            cmds.connectAttr( meshP+'.s', refMeshObj+'.s' )
            cmds.connectAttr( meshP+'.sh', refMeshObj+'.sh' )
            
            cmds.setAttr( refMeshObj+'.template', 1 )
    

class ImportGroom:
    
    def __init__(self, yetiNode, path ):
        
        self._yetiNode = yetiNode
        self._path = path
        
        self.doIt()
        
    def doIt(self):
        
        cmds.setAttr( self._yetiNode+".fileMode", 1 )
        cmds.setAttr( self._yetiNode+".groomFileName", self._path , type='string' )
        mel.eval( 'pgYetiImportGroomFileFromNode %s;' % self._yetiNode )
        cmds.setAttr( self._yetiNode+".fileMode", 0 )
        cmds.setAttr( self._yetiNode+".groomFileName", '', type='string' )
        
        
        

class OpenEditor:
    
    def __init__(self, mesh ):
        
        yetiNode = cmds.listConnections( mesh+'.worldMesh', type='pgYetiMaya' )
        cmds.select( yetiNode )
        mel.eval( 'pgYetiOpenGraphEditor()' )