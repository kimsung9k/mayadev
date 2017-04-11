import maya.cmds as cmds

class CreateVolumeHair:

    def __init__(self, surface, mesh ):
        
        self._surfShape = self.getSurfaceShape( surface )
        self._meshShape = self.getMeshShape( mesh )
        
        self._sepNum = 6
        self.getSurfaceInfo( self._sepNum )
        
        self.create()
        #self.startEPSet()
        

    def getSurfaceShape(self, surface ):
        
        if cmds.nodeType( surface ) == 'nurbsSurface':
            return surface
        elif cmds.nodeType( surface ) == 'transform':
            return cmds.listRelatives( surface, s=1 )[0]



    def getMeshShape(self, mesh ):
        
        if cmds.nodeType( mesh ) == 'mesh':
            return mesh
        elif cmds.nodeType( mesh ) == 'transform':
            return cmds.listRelatives( mesh, s=1 )[0]
        

        
    def getSurfaceInfo(self, paramSep ):
        
        minValue, maxValue = cmds.getAttr( self._surfShape+'.minMaxRangeV' )[0]
        self._paramRate = ( maxValue-minValue )/paramSep
        self._numSpans = cmds.getAttr( self._surfShape+'.spansU' )
        


    def create(self):
        
        node = cmds.createNode( 'volumeCurvesOnSurface' )
        
        cmds.connectAttr( self._surfShape+'.local', node+'.inputSurface' )
        cmds.connectAttr( self._surfShape+'.wm', node+'.inputMatrix' )
        
        cmds.connectAttr( self._meshShape+'.outMesh', node+'.inputMesh' )
        cmds.connectAttr( self._meshShape+'.wm', node+'.meshMatrix' )
        
        for i in range( self._sepNum ):
            crvNode = cmds.createNode( 'nurbsCurve' )
            cmds.setAttr( node+'.curveInfo[%d].paramRate' % i, self._paramRate*i )
            cmds.setAttr( node+'.numOfSample', self._numSpans )
            cmds.connectAttr( node+'.outputCurve[%d]' % i, crvNode+'.create' )
            
        self._node = node
            


    def startEPSet(self):
        
        for i in range( self._sepNum ):
            for j in range( 100 ):
                cmds.setAttr( self._node+'.curveInfo[%d].startEP[%d]' %( i, j ), .1,.1,.1 )