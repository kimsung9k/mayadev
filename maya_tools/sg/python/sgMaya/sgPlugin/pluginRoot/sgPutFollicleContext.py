import sys
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMayaMPx as OpenMayaMPx

import maya.OpenMayaUI



def getMObject( nodeName ):
    
    selList = OpenMaya.MSelectionList()
    selList.add( nodeName )
    oNode = OpenMaya.MObject()
    selList.getDependNode( 0, oNode )
    return oNode


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
    currentGlWidget = None
    currentEventFilter = None



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
        return intersectPoints[0] * meshMatrix
 
    
    
    @staticmethod
    def getFollicle( dagPath ):
        
        import math
        
        fnMesh = OpenMaya.MFnMesh( dagPath )
        
        follicleTrs = cmds.listConnections( fnMesh.partialPathName(), type= 'follicle' )
        if not follicleTrs: follicleTrs = []
        
        for follicle in follicleTrs:
            jointPosition = OpenMaya.MPoint( *cmds.xform( follicle, q=1, ws=1, t=1 ) )
            jointViewPoint = worldPointToViewPoint( jointPosition )
            
            if math.fabs( jointViewPoint.x - Tool_global.mouseX ) > 10: continue
            if math.fabs( jointViewPoint.y - Tool_global.mouseY ) > 10: continue
            return cmds.listRelatives( follicle, s=1, f=1 )[0], follicle
        
        follicle = cmds.createNode( 'follicle' )
        
        cmds.undoInfo( swf=0 )
        follicleTr = cmds.listRelatives( follicle, p=1, f=1 )[0]
        
        cmds.connectAttr( follicle + '.outTranslate', follicleTr + '.t' )
        cmds.connectAttr( follicle + '.outRotate', follicleTr + '.r' )
        
        fnMesh = OpenMaya.MFnMesh( dagPath )
        cmds.connectAttr( fnMesh.partialPathName() + '.outMesh', follicle+'.inputMesh' )
        cmds.connectAttr( fnMesh.partialPathName() + '.worldMatrix[0]', follicle+'.inputWorldMatrix' )
        
        cmds.undoInfo( swf=1 )
        
        return follicle, follicleTr
    



class PutObjectContext( OpenMayaMPx.MPxSelectionContext ):

    contextName = 'sgPutFollicleContext'
    
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
    

    
    def doPress( self, event ):
        self.newFollicle = None
        
        argX = OpenMaya.MScriptUtil()
        argX.createFromInt(0)
        argXPtr = argX.asShortPtr()
        argY = OpenMaya.MScriptUtil()
        argY.createFromInt(0)
        argYPtr = argY.asShortPtr()
        event.getPosition(argXPtr, argYPtr)
        mouseX = OpenMaya.MScriptUtil(argXPtr).asShort()
        mouseY = OpenMaya.MScriptUtil(argYPtr).asShort()

        intersectPoint = Functions.getIntersectPoint( self.dagPath, mouseX, mouseY )
        if not intersectPoint: 
            return None
        
        print intersectPoint.x, intersectPoint.y, intersectPoint.z
        
        self.newFollicle, self.newFollicleTr = Functions.getFollicle(self.dagPath)
        
        cmds.select( self.newFollicle )
        
        fnMesh = OpenMaya.MFnMesh( self.dagPath )
        util = OpenMaya.MScriptUtil()
        util.createFromList( [0,0], 2 )
        uvPtr = util.asFloat2Ptr()
        fnMesh.getUVAtPoint( intersectPoint, uvPtr, OpenMaya.MSpace.kWorld )
        uvValues = listFromFloat2Ptr( uvPtr )
        
        cmds.undoInfo( swf=0 )
        
        cmds.setAttr( self.newFollicle + '.parameterU', uvValues[0] )
        cmds.setAttr( self.newFollicle + '.parameterV', uvValues[1] )
        cmds.undoInfo( swf=1 )
        cmds.refresh()
        
        self.origUvValues = uvValues
    

    def doDrag(self, event ):
        if not self.newFollicle: return None
        
        argX = OpenMaya.MScriptUtil()
        argX.createFromInt(0)
        argXPtr = argX.asShortPtr()
        argY = OpenMaya.MScriptUtil()
        argY.createFromInt(0)
        argYPtr = argY.asShortPtr()
        event.getPosition(argXPtr, argYPtr)
        mouseX = OpenMaya.MScriptUtil(argXPtr).asShort()
        mouseY = OpenMaya.MScriptUtil(argYPtr).asShort()

        intersectPoint = Functions.getIntersectPoint( self.dagPath, mouseX, mouseY )
        if not intersectPoint: 
            return None
        
        fnMesh = OpenMaya.MFnMesh( self.dagPath )
        util = OpenMaya.MScriptUtil()
        util.createFromList( [0,0], 2 )
        uvPtr = util.asFloat2Ptr()
        fnMesh.getUVAtPoint( intersectPoint, uvPtr, OpenMaya.MSpace.kWorld )
        uvValues = listFromFloat2Ptr( uvPtr )
        
        fnFollicle = OpenMaya.MFnDependencyNode( getMObject( self.newFollicle ) )
        fnFollicleTr = OpenMaya.MFnDependencyNode( getMObject( self.newFollicleTr ) )
        
        uPlug = fnFollicle.findPlug( 'parameterU' )
        vPlug = fnFollicle.findPlug( 'parameterV' )
        dlaPlug = fnFollicleTr.findPlug( 'dla' )
        
        uPlug.setFloat( uvValues[0] )
        vPlug.setFloat( uvValues[1] )
        dlaPlug.setBool( 1 )
        
        cmds.refresh()
        
        self.currentUvValues = uvValues


    def doRelease(self, event ):
        fnFollicleTr = OpenMaya.MFnDependencyNode( getMObject( self.newFollicleTr ) )
        
        dlaPlug = fnFollicleTr.findPlug( 'dla' )
        dlaPlug.setBool( 0 )




class PutObjectContextCommand( OpenMayaMPx.MPxContextCommand ):
    
    commandName = "sgPutFollicleContextCommand"
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
