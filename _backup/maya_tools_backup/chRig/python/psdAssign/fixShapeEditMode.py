import maya.cmds as cmds
import baseFunctions
import assign

import copy


class GetTargetObj:
 
    
    def __init__(self, controler ):

        self._targetObj = self.getTargetObj( controler )
        
        
    def getMainBlendShape( self, controler ):
    
        blendShapeNodes = cmds.listConnections( controler, d=1, s=0, type='blendShape' )
    
        for blendShape in blendShapeNodes:
            if cmds.attributeQuery( 'isMainBlendShape', node=blendShape, ex=1 ):
                return blendShape
            

    def getTargetObj( self, controler ):

        blendShapeMain = self.getMainBlendShape( controler )
        
        targetGeo = cmds.listConnections( blendShapeMain+'.outputGeometry' )[0]
        
        return targetGeo
        



class FixShapeCreate:
    
    
    def __init__(self, targetShape, name='' ):
        
        self._targetShape = targetShape
        
        self.createShape( name )
        self.shaderChange( self._fixShape )
        
    
    def createShape(self, name ):
        
        if name:
            assignName = name
        else:
            assignName = self._targetShape + '_FixTarget'
        
        self._fixShape = cmds.duplicate( self._targetShape, n= assignName )[0]
        
        baseFunctions.cleanMesh( self._fixShape )
        
        if not cmds.attributeQuery( 'editingFixShape', node=self._targetShape, ex=1 ):
            cmds.addAttr( self._targetShape, ln='editingFixShape', at='message' )
            
        cmds.connectAttr( self._fixShape+'.message', self._targetShape+'.editingFixShape', f=1 )
        
        
    def shaderChange( self, changeTarget ):
        
        shaderList = cmds.ls( 'fixShapeEditModeShader', type='blinn' )
        if not shaderList:
            shader = baseFunctions.createShader( n='fixShapeEditModeShader' )
            
            cmds.setAttr( shader+'.colorR', 0.579 )
            cmds.setAttr( shader+'.colorG', 1.000 )
            cmds.setAttr( shader+'.colorB', 0.579 )
            cmds.setAttr( shader+'.specularColorR', 0.4 )
            cmds.setAttr( shader+'.specularColorG', 0.122 )
            cmds.setAttr( shader+'.specularColorB', 0.122 )
        else:
            shader = shaderList[0]
        
        
        cmds.select( changeTarget )
        cmds.hyperShade( assign = shader )




class EditMode:
    
    def __init__(self, targetObj, fixObj ):
        
        cmds.setAttr( targetObj+'.v', 0 )
        cmds.setAttr( fixObj+'.v', 1 )
        
    
    
class NormalMode:
    
    def __init__(self, targetObj, fixObj ):
        
        cmds.setAttr( targetObj+'.v', 1 )
        cmds.setAttr( fixObj+'.v', 0 )
    
    

class Control:
    
    def __init__(self, controler, name='' ):
        
        self._controler = controler
        
        self._name = name
        
        
    
    def fixShapeExistCheck(self):
        
        targetObj = GetTargetObj( self._controler )._targetObj
        
        hists = cmds.listHistory( targetObj, pdo=1 )
        
        for hist in hists:
            
            if cmds.attributeQuery( 'isMainBlendShape', node=hist, ex=1 ):
                
                mainBlendShape = hist
                
        allAffectedIndies = baseFunctions.getAffectedIndies( mainBlendShape+'.w' )
        affectedIndies = []
        
        for i in allAffectedIndies:
            tempItpNodes = cmds.listConnections( mainBlendShape+'.w[%d]' % i, type='vectorInterpolation', d=1, s=0 )
            
            if tempItpNodes:
                affectedIndies.append( i )
        
        if not affectedIndies:
            return None
        
        firstItpNodes = cmds.listConnections( mainBlendShape+'.w[%d]' % affectedIndies[0], type='vectorInterpolation', d=1, s=0 )
        secondItpNodes = []
        if len( affectedIndies ) > 1:
            
            for i in affectedIndies[1:]:
                tempItpNodes = cmds.listConnections( mainBlendShape+'.w[%d]' % i, type='vectorInterpolation' )
                
                for tempItp in tempItpNodes:
                    if tempItp in firstItpNodes:
                        secondItpNodes.append( tempItp )
        
                firstItpNodes = copy.copy( secondItpNodes )
                secondItpNodes = []
        
        affectedLen = len( affectedIndies )
        
        '''
        for itpNode in firstItpNodes:
            baseFunctions.'''
        
    
    def edit(self):
        
        self._targetObj = GetTargetObj( self._controler )._targetObj
        
        self._fixObj = FixShapeCreate( self._targetObj, self._name )._fixShape
        
        EditMode( self._targetObj, self._fixObj )
        
        
        
    def assign( self, controler ):
        
        cons = cmds.listConnections( controler, type='blendShape' )
        
        for con in cons:
            
            if cmds.attributeQuery( 'isMainBlendShape', node=con, ex=1 ):
                
                mainBlendShape = con
                
                
        baseMesh = cmds.listConnections( mainBlendShape+'.outputGeometry[0]' )[0]
        
        fixMesh = cmds.listConnections( baseMesh+'.editingFixShape' )[0]

        
        assign.FixShapeAssign( fixMesh, baseMesh )
        
        NormalMode( baseMesh, fixMesh )