import sys
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMayaMPx as OpenMayaMPx



def getMObject( nodeName ):
    
    selList = OpenMaya.MSelectionList()
    selList.add( nodeName )
    oNode = OpenMaya.MObject()
    selList.getDependNode( 0, oNode )
    return oNode
    


def float2Ptr():
    util = OpenMaya.MScriptUtil()
    util.createFromList( [0,0], 2 )
    return util.asFloat2Ptr()


def listFromFloat2Ptr( ptr ):
    util = OpenMaya.MScriptUtil()
    v1 = util.getFloat2ArrayItem( ptr, 0, 0 )
    v2 = util.getFloat2ArrayItem( ptr, 0, 1 )
    return [v1, v2]



def shortPtr( intValue = 0 ):
    util = OpenMaya.MScriptUtil()
    util.createFromInt(intValue)
    return util.asShortPtr()

def shortFromShortPtr( ptr ):
    return OpenMaya.MScriptUtil.getShort( ptr )



class Tool_global:
    mouseX = 0
    mouseY = 0



def getSelection():
    sels = cmds.ls( sl=1 )
    for sel in sels:
        if cmds.nodeType( sel ) == 'mesh':
            return sel
        if cmds.nodeType( sel ) != 'transform': continue
        selShapes = cmds.listRelatives( sel, s=1, f=1 )
        for selShape in selShapes:
            if cmds.nodeType( selShape ) == 'mesh': return selShape
    return None



def getDagPath( nodeName ):
    selList = OpenMaya.MSelectionList()
    selList.add( nodeName )
    dagPath = OpenMaya.MDagPath()
    selList.getDagPath( 0, dagPath )
    return dagPath



def getShortPtr( intValue = 0 ):
    util = OpenMaya.MScriptUtil()
    util.createFromInt(intValue)
    return util.asShortPtr()



def getValueFromShortPtr( ptr ):
    return OpenMaya.MScriptUtil().getShort( ptr )



def worldPointToViewPoint( worldPoint ):
    
    activeView = OpenMayaUI.M3dView().active3dView()
    camDagPath = OpenMaya.MDagPath()
    activeView.getCamera( camDagPath )
    
    projectionMatrix = OpenMaya.MMatrix()
    activeView.projectionMatrix(projectionMatrix)
    camInvMatrix = camDagPath.inclusiveMatrixInverse()
    
    viewPoint = worldPoint * camInvMatrix * projectionMatrix
    viewPoint.x = (viewPoint.x/viewPoint.w + 1.0 )/2.0 * activeView.portWidth()
    viewPoint.y = (viewPoint.y/viewPoint.w + 1.0 )/2.0 * activeView.portHeight()
    viewPoint.z = 0
    viewPoint.w = 1
    
    return viewPoint



class Functions:
    
    @staticmethod
    def getIntersectPoint( meshDagPath, mouseX, mouseY ):
        
        meshMatrix = meshDagPath.inclusiveMatrix()
        invMtx = meshDagPath.inclusiveMatrixInverse()
        
        activeView = OpenMayaUI.M3dView().active3dView()
        nearPoint = OpenMaya.MPoint()
        farPoint  = OpenMaya.MPoint()
        activeView.viewToWorld( mouseX, mouseY, nearPoint, farPoint )
        
        nearPoint *= invMtx
        farPoint  *= invMtx
        
        fnMesh = OpenMaya.MFnMesh( meshDagPath )
        intersectPoints = OpenMaya.MPointArray()
        
        fnMesh.intersect( nearPoint, farPoint - nearPoint, intersectPoints )
        
        if not intersectPoints.length(): return None
        
        if intersectPoints.length() == 1:
            return intersectPoints[0] * meshMatrix
        elif intersectPoints.length() > 1:
            pointCenter = (OpenMaya.MVector(intersectPoints[0]) + OpenMaya.MVector(intersectPoints[1]))/2.0
            return pointCenter * meshMatrix
    
    
    @staticmethod
    def getTransform( mouseX, mouseY ):
        
        import math
        for transform in cmds.ls( type='transform' ):
            if not cmds.getAttr( transform + '.dh' ): continue
            
            point = OpenMaya.MPoint( *cmds.xform( transform, q=1, ws=1, t=1 ) )
            viewPoint = worldPointToViewPoint( point )
            
            if math.fabs( viewPoint.x - mouseX ) > 10 or math.fabs( viewPoint.y - mouseY ) > 10: continue
            return transform
        
        transform = cmds.createNode( 'transform' )
        cmds.setAttr( transform + '.dh', 1 )
        return transform
        
    



class PutObjectContext( OpenMayaMPx.MPxSelectionContext ):

    contextName = 'sgPutInsideContext'
    
    def __init__(self):
        OpenMayaMPx.MPxSelectionContext.__init__( self )


    def toolOnSetup(self, *args, **kwargs ):
        
        meshShape = getSelection()
        if not meshShape:
            cmds.error( "Select mesh first" )
        
        self.meshName = meshShape
        self.dagPath = getDagPath( meshShape )
        self.meshMatrix = self.dagPath.inclusiveMatrix()
        self.meshMatrixInv = self.dagPath.inclusiveMatrixInverse()
        
        OpenMayaMPx.MPxSelectionContext.toolOnSetup( self, *args, **kwargs )
    

    def toolOffCleanup( self, *args, **kwargs ):
        OpenMayaMPx.MPxSelectionContext.toolOffCleanup(self, *args, **kwargs )


    def className( self, *args, **kwargs):
        OpenMayaMPx.MPxSelectionContext.className(self, *args, **kwargs)
        
    
    
    def getMouseXY(self, event ):
        argX = OpenMaya.MScriptUtil()
        argX.createFromInt(0)
        argXPtr = argX.asShortPtr()
        argY = OpenMaya.MScriptUtil()
        argY.createFromInt(0)
        argYPtr = argY.asShortPtr()
        event.getPosition(argXPtr, argYPtr)
        mouseX = OpenMaya.MScriptUtil(argXPtr).asShort()
        mouseY = OpenMaya.MScriptUtil(argYPtr).asShort()
        return mouseX, mouseY
    
    
    def doPress( self, event ):
        
        self.transform = None
        mouseX, mouseY = self.getMouseXY( event )

        intersectPoint = Functions.getIntersectPoint( self.dagPath, mouseX, mouseY )
        if not intersectPoint: 
            return None
        
        self.transform = Functions.getTransform( mouseX, mouseY )
        cmds.setAttr( self.transform + '.dh', 1 )
        cmds.select( self.transform )
        self.beforePosition = cmds.xform( self.transform, q=1, ws=1, t=1 )[:3]
        cmds.undoInfo( swf=0 )
        cmds.move( intersectPoint.x, intersectPoint.y, intersectPoint.z, self.transform, ws=1 )
        self.currentPosition = [intersectPoint.x, intersectPoint.y, intersectPoint.z]
        cmds.refresh()
    

    def doDrag(self, event ):
        if not self.transform: return None
        mouseX, mouseY = self.getMouseXY( event )

        intersectPoint = Functions.getIntersectPoint( self.dagPath, mouseX, mouseY )
        if not intersectPoint: 
            return None
        
        cmds.move( intersectPoint.x, intersectPoint.y, intersectPoint.z, self.transform, ws=1 )
        self.currentPosition = [intersectPoint.x, intersectPoint.y, intersectPoint.z]
        cmds.refresh()


    def doRelease(self, event ):
        cmds.move( self.beforePosition[0], self.beforePosition[1], self.beforePosition[2], self.transform, ws=1 )
        cmds.undoInfo( swf=1 )
        cmds.move( self.currentPosition[0], self.currentPosition[1], self.currentPosition[2], self.transform, ws=1 )
        pass




class PutObjectContextCommand( OpenMayaMPx.MPxContextCommand ):
    
    commandName = "sgPutInsideContextCommand"
    def __init__(self):
        OpenMayaMPx.MPxContextCommand.__init__( self )
        self.m_pContext = 0
        
    @staticmethod
    def creator():
        return OpenMayaMPx.asMPxPtr( PutObjectContextCommand() )
    
    def doEditFlags( self ):
        return OpenMayaMPx.MPxContextCommand.doEditFlags( self )
    
    def doQueryFlags( self ):
        return OpenMayaMPx.MPxContextCommand.doQueryFlags( self )
    
    def appendSyntax( self ):
        return OpenMayaMPx.MPxContextCommand.appendSyntax( self )
    
    def makeObj(self):
        return OpenMayaMPx.asMPxPtr( PutObjectContext() )



# initialize the script plug-in
def initializePlugin(mobject):
    import maya.mel as mel
    
    mplugin = OpenMayaMPx.MFnPlugin(mobject, "Autodesk", "1.0", "Any")
    mplugin.registerContextCommand( PutObjectContextCommand.commandName,
                                    PutObjectContextCommand.creator )
    
    mel.eval( "%s %s1" %( PutObjectContextCommand.commandName, PutObjectContext.contextName ))



# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    import maya.mel as mel
    
    mel.eval( "deleteUI %s1" %( PutObjectContext.contextName ) )
    
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    mplugin.deregisterContextCommand( PutObjectContextCommand.commandName )
