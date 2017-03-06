import maya.cmds as cmds
import maya.OpenMaya as openMaya
import sgCFnc_dag



class Dag:
    
    def __init__( self, arg1 ):
        
        self.mDagPath   = sgCFnc_dag.getMDagPath( arg1 )
        self.mFnDagNode = openMaya.MFnDagNode( self.mDagPath )
    
    
    def name(self):
        
        return self.mFnDagNode.name()
    
    
    def fullPathName(self):
        
        return self.mFnDagNode.fullPathName()
    
    
    def getMatrix(self):
        
        return cmds.getAttr( self.mFnDagNode.fullPathName() + '.matrix' )
    
    
    def getWorldMatrix(self):
        
        return cmds.getAttr( self.mFnDagNode.fullPathName() + '.worldMatrix' )
    
    
    def getParentMatrix(self):
        
        return cmds.getAttr( self.mFnDagNode.fullPathName() + '.parentMatrix' )
    
    
    def getMMatrix(self):
        
        return self.mDagPath.inclusiveMatrix() * self.mDagPath.exclusiveMatrixInverse()
    
    
    def getMMatrixWorld(self):
        
        return self.mDagPath.inclusiveMatrix()
    
    
    def getMMatrixParent(self):
        
        return self.mDagPath.exclusiveMatrix()
    
    
    def getMBoundingBox(self):
        
        return self.mFnDagNode.boundingBox()
    
    
    def getChild(self, index ):
        
        if index > self.mFnDagNode.childCount()-1:
            cmds.error( "%d Child not Exists" % index )
            return None
        
        return Dag( self.mFnDagNode.child( index ) )
    

    def getChildren( self ):
        
        children = []
        for i in range( self.mFnDagNode.childCount() ):
            children.append( Dag( self.mFnDagNode.child( i ) ) )
        return children




class Transform( Dag ):
    
    def __init__( self, arg1 ):
        
        Dag.__init__( arg1 )
        self.mTransform = openMaya.MFnTransform( self.mDagPath )





class Mesh( Dag ):
    
    def __init__( self, arg1 ):
        
        Dag.__init__( arg1 )
        self.mFnMesh  = openMaya.MFnMesh( self.mDagPath )





class NurbsCurve( Dag ):
    
    def __init__( self, arg1 ):
        
        Dag.__init__( arg1 )
        self.mFnNurbsCurve = openMaya.MFnMesh( self.mDagPath )




class NurbsSurface( Dag ):
    
    def __init__( self, arg1 ):
        
        Dag.__init__( arg1 )
        self.mFnNurbsSurface = openMaya.MFnMesh( self.mDagPath )