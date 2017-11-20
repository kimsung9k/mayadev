import sys, math
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMayaRender as OpenMayaRender


class Functions:
    
    @staticmethod
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
    
    
    
    @staticmethod
    def getDagPath( nodeName ):
        selList = OpenMaya.MSelectionList()
        selList.add( nodeName )
        dagPath = OpenMaya.MDagPath()
        selList.getDagPath( 0, dagPath )
        return dagPath

    
    @staticmethod
    def getIntersectPoint( mouseX, mouseY, meshDagPath=None ):
        
        activeView = OpenMayaUI.M3dView().active3dView()
        nearPoint  = OpenMaya.MPoint()
        farPoint   = OpenMaya.MPoint()
        activeView.viewToWorld( mouseX, mouseY, nearPoint, farPoint )
        
        if meshDagPath:
            meshMatrix = meshDagPath.inclusiveMatrix()
            invMtx = meshDagPath.inclusiveMatrixInverse()
            
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
        else:
            activeView = OpenMayaUI.M3dView().active3dView()
            camDagPath = OpenMaya.MDagPath()
            activeView.getCamera( camDagPath )
            
            fnCam   = OpenMaya.MFnCamera( camDagPath )
            focalLength = fnCam.focalLength()
            
            camVector = OpenMaya.MVector( farPoint ) - OpenMaya.MVector( nearPoint )
            camVector.normalize()
            return camVector * focalLength + nearPoint
            


    @staticmethod
    def getMouseXY( event ):
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
        
    
    @staticmethod
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
        



class SGDrawCurveManip( OpenMayaMPx.MPxManipContainer ):
    
    manipName = "sgDrawCurveManip"
    manipId = OpenMaya.MTypeId( 0x20170215 )
    glRenderer = OpenMayaRender.MHardwareRenderer.theRenderer()
    glft = glRenderer.glFunctionTable()
    
    def __init__(self):
        OpenMayaMPx.MPxManipContainer.__init__( self )
        self.fCuveManip = OpenMaya.MDagPath()
    
    def createChildren(self):
        pass
    
    def connectToDependNode(self, node ):
        pass
    
    def draw(self, view, path, style, status ):
        OpenMayaMPx.MPxManipContainer.draw( self, view, path, style, status )
        
        view.beginGL()
        view.drawText( 'Stretch Me!', OpenMaya.MPoint(0,0,0), OpenMayaUI.M3dView.kLeft )
        view.endGL()
    





class SGDrawCurveContext( OpenMayaMPx.MPxSelectionContext ):

    contextName = 'sgDrawCurveContext'
    
    def __init__(self):
        OpenMayaMPx.MPxSelectionContext.__init__( self )
        self.__meshExists = False
        self.__dagPath = None


    def toolOnSetup(self, *args, **kwargs ):
        
        meshShape = Functions.getSelection()
        if meshShape:
            self.__meshName = meshShape
            self.__dagPath = Functions.getDagPath( meshShape )
            self.__meshMatrix = self.__dagPath.inclusiveMatrix()
            self.__meshMatrixInv = self.__dagPath.inclusiveMatrixInverse()
            self.__meshExists = True
        else:
            self.__meshExists = False
        
        OpenMayaMPx.MPxSelectionContext.toolOnSetup( self, *args, **kwargs )
    

    def toolOffCleanup( self, *args, **kwargs ):
        OpenMayaMPx.MPxSelectionContext.toolOffCleanup(self, *args, **kwargs )


    def className( self, *args, **kwargs):
        OpenMayaMPx.MPxSelectionContext.className(self, *args, **kwargs)
    
    
    def doPress( self, event ):
        
        mouseX, mouseY = Functions.getMouseXY( event )
        Functions.getIntersectPoint( mouseX, mouseY )
        print "mouse position : %d, %d" %( mouseX, mouseY )

    

    def doDrag(self, event ):
        
        mouseX, mouseY = Functions.getMouseXY( event )
        Functions.getIntersectPoint( mouseX, mouseY )
        print "mouse position : %d, %d" %( mouseX, mouseY )


    def doRelease(self, event ):
        pass




class SGDrawCurveContextCommand( OpenMayaMPx.MPxContextCommand ):
    
    commandName = "sgDrawCurveContextCommand"
    def __init__(self):
        OpenMayaMPx.MPxContextCommand.__init__( self )
        self.m_pContext = 0
        
    @staticmethod
    def creator():
        return OpenMayaMPx.asMPxPtr( SGDrawCurveContextCommand() )
    
    def doEditFlags( self ):
        return OpenMayaMPx.MPxContextCommand.doEditFlags( self )
    
    def doQueryFlags( self ):
        return OpenMayaMPx.MPxContextCommand.doQueryFlags( self )
    
    def appendSyntax( self ):
        return OpenMayaMPx.MPxContextCommand.appendSyntax( self )
    
    def makeObj(self):
        return OpenMayaMPx.asMPxPtr( SGDrawCurveContext() )



# initialize the script plug-in
def initializePlugin(mobject):
    import maya.mel as mel
    
    mplugin = OpenMayaMPx.MFnPlugin(mobject, "Autodesk", "1.0", "Any")
    mplugin.registerContextCommand( SGDrawCurveContextCommand.commandName,
                                    SGDrawCurveContextCommand.creator )
    
    mel.eval( "%s %s1" %( SGDrawCurveContextCommand.commandName, SGDrawCurveContext.contextName ))



# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    import maya.mel as mel
    
    mel.eval( "deleteUI %s1" %( SGDrawCurveContext.contextName ) )
    
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    mplugin.deregisterContextCommand( SGDrawCurveContextCommand.commandName )
