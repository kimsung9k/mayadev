import maya.OpenMaya as om
import maya.cmds as cmds
import baseFunctions
import createFixEditShape
        


class BlendShapeAssign:
    
    def __init__(self, targets, base ):
        
        targets.append( base )
        
        self._mainBlendShape = cmds.blendShape( *targets, n= base+'_mainBlendShape' )[0]
        
        cmds.addAttr( self._mainBlendShape, ln='isMainBlendShape', at='bool' )


        
class BlendShapeAppend:
    
    def __init__(self, targets, base ):
        
        hists = cmds.listHistory( base, pdo=1 )
         
        for hist in hists:
            
            if cmds.attributeQuery( 'isMainBlendShape', node=hist, ex=1 ):
                
                mainBlendShape = hist
        
        for target in targets:
            
            #baseFunctions.removeUnConnectedIndies( mainBlendShape+'.w' )
            currentIndex = baseFunctions.getLastIndex( mainBlendShape+'.w' )+1
            
            cmds.blendShape( base, e=1, t=[ base, currentIndex, target, 1 ] )

    
        
class FixShapeAssign:
    
    def __init__(self, target, base ):
       
        self._target = target
        
        self._baseObj = base
        
        mainBlendShape = self.getMainBlendShape()
        
        self.check_weight( mainBlendShape )
        
        self.doIt()
        
        
    def getMainBlendShape(self):

        hists = cmds.listHistory( self._baseObj, pdo=1 )
        
        if hists:
            for hist in hists:
                if cmds.attributeQuery( 'isMainBlendShape', node=hist, ex=1 ):
                    return hist
        else:
            return None
        
    
    
    def check_weight(self, mainBlendShape ):
        
        mainBlendShapeObj = baseFunctions.getMObject( mainBlendShape )
        
        fnPsdNode = om.MFnDependencyNode( mainBlendShapeObj )
        weightPlug = fnPsdNode.findPlug( 'weight' )
        
        self.weightValues = []
        self.weightedIndies = []
        
        for i in range( weightPlug.numElements() ):
            
            weightValue = weightPlug[i].asFloat()
            
            if weightValue > 0.01:
                
                self.weightedIndies.append( i )
                self.weightValues.append( weightValue )
                
    
    
    def doIt(self):

        mainBlendShape = self.getMainBlendShape()
        self.check_weight( mainBlendShape )

        createFixEditShape.Create( self._target, self._baseObj, mainBlendShape, self.weightedIndies, self.weightValues )




class Assign:
    
    
    def __init__(self, targets, base ):
        
        mainBlendShape = self.checkIsMainBlendShape( base )
        
        if mainBlendShape:
            
            if self.checkIsWeighted( mainBlendShape ):
                FixShapeAssign( targets[-1], base )
            else:
                BlendShapeAppend( targets, base )
        else:
            BlendShapeAssign( targets, base )
                
        
        
    def checkIsMainBlendShape(self, base ):
        
        hists = cmds.listHistory( base, pdo=1 )
    
        if not hists: return False
    
        for hist in hists:
            
            if cmds.attributeQuery( 'isMainBlendShape', node=hist, ex=1 ):
                return hist
            
        return False
    
    
    def checkIsWeighted(self, mainBlendShape ):
        
        lastIndex = baseFunctions.getLastIndex( mainBlendShape+'.w' )
        
        for i in range( lastIndex+1 ):
            
            value = cmds.getAttr( mainBlendShape+'.w[%d]' % i )
            
            if value: return True
            
        return False