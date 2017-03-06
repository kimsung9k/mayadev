import sys
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMayaMPx as OpenMayaMPx

import maya.OpenMayaUI
from PySide import QtGui, QtCore
import shiboken



class Tool_global:
    mouseX = 0
    mouseY = 0
    currentGlWidget = None
    currentEventFilter = None



def getMayaWindowPtr():
    return shiboken.wrapInstance( long( maya.OpenMayaUI.MQtUtil.mainWindow() ), QtGui.QWidget )



class MainWindowEventFilter(QtCore.QObject):
    
    def __init__(self):
        QtCore.QObject.__init__(self)

    def eventFilter(self, obj, event):
        
        focusWidget = QtGui.QApplication.focusWidget()
        try:widgetChildren = focusWidget.children()
        except: return False
        
        glWidget = None
        
        for widgetObj in widgetChildren:
            widgetChildren2 = widgetObj.children()
            if not len( widgetChildren2 ): continue
            for widgetObj2 in widgetChildren2:
                if widgetObj2.metaObject().className() != "QmayaGLWidget": continue
                glWidget = widgetObj2
                break
            if glWidget: break
        
        if not glWidget:
            if Tool_global.currentGlWidget:
                #print "remove event filter"
                Tool_global.currentGlWidget.removeEventFilter( Tool_global.currentEventFilter )
                Tool_global.currentGlWidget = None
        else:
            if Tool_global.currentGlWidget != glWidget:
                if Tool_global.currentGlWidget:
                    #print "remove event filter"
                    Tool_global.currentGlWidget.removeEventFilter( Tool_global.currentEventFilter )
                #print "create event filter"
                Tool_global.currentGlWidget = glWidget
                Tool_global.currentGlWidget.installEventFilter( Tool_global.currentEventFilter )
        return False



class glWidgetEventFilter( QtCore.QObject ):
    def __init__(self):
        QtCore.QObject.__init__( self )
    
    def eventFilter(self, obj, event ):
        if event.type() == QtCore.QEvent.MouseButtonPress or event.type() == QtCore.QEvent.MouseMove or event.type() == QtCore.QEvent.MouseButtonRelease:
            Tool_global.mouseX = event.x()
            Tool_global.mouseY = Tool_global.currentGlWidget.height() - event.y()



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
    



class PutObjectContext( OpenMayaMPx.MPxSelectionContext ):
    
    contextName = "PutObjectContext"
    
    def __init__(self):
        OpenMayaMPx.MPxSelectionContext.__init__( self )
    
    def toolOnSetup(self, *args, **kwargs ):
        
        Tool_global.currentGlWidget = None
        Tool_global.currentEventFilter = glWidgetEventFilter()
        
        meshShape = getSelection()
        if not meshShape:
            cmds.error( "Select mesh first" )
        
        self.main_window = getMayaWindowPtr()
        self.eventFilter = MainWindowEventFilter()
        self.main_window.installEventFilter(self.eventFilter)
        
        self.dagPath = getDagPath( meshShape )
        self.meshMatrix = self.dagPath.inclusiveMatrix()
        self.meshMatrixInv = self.dagPath.inclusiveMatrixInverse()
        
        OpenMayaMPx.MPxSelectionContext.toolOnSetup( self, *args, **kwargs )
    
    def toolOffCleanup( self, *args, **kwargs ):
        
        self.main_window.removeEventFilter(self.eventFilter)
        
        if Tool_global.currentGlWidget:
            Tool_global.currentGlWidget.removeEventFilter( Tool_global.currentEventFilter )
        
        OpenMayaMPx.MPxSelectionContext.toolOffCleanup(self, *args, **kwargs )
        
    def className( self, *args, **kwargs):
        OpenMayaMPx.MPxSelectionContext.className(self, *args, **kwargs)
        
    
    def getIntersectPointAndNormal(self):
        
        activeView = OpenMayaUI.M3dView().active3dView()
        nearPoint = OpenMaya.MPoint()
        farPoint  = OpenMaya.MPoint()
        activeView.viewToWorld( Tool_global.mouseX, Tool_global.mouseY, nearPoint, farPoint )
        
        nearPoint *= self.meshMatrixInv
        farPoint  *= self.meshMatrixInv
        
        fnMesh = OpenMaya.MFnMesh( self.dagPath )
        intersectPoints = OpenMaya.MPointArray()
        
        fnMesh.intersect( nearPoint, farPoint - nearPoint, intersectPoints )
        closeNormal = OpenMaya.MVector()
        fnMesh.getClosestNormal( intersectPoints[0], closeNormal )
        
        if not intersectPoints: return None, None
        return intersectPoints[0] * self.meshMatrix, closeNormal * self.meshMatrix  
    
    
    
    def getJoint(self ):
        
        import math
        joints = cmds.ls( type='joint' )
        
        for joint in joints:
            cons = cmds.listConnections( joint, s=1, d=0 )
            if cons: continue
            jointPosition = OpenMaya.MPoint( *cmds.xform( joint, q=1, ws=1, t=1 ) )
            jointViewPoint = worldPointToViewPoint( jointPosition )
            
            if math.fabs( jointViewPoint.x - Tool_global.mouseX ) > 10: continue
            if math.fabs( jointViewPoint.y - Tool_global.mouseY ) > 10: continue
            return joint
        
        return cmds.createNode( 'joint' )
            
    
    
    def doPress( self, *args, **kwargs ):
        self.newJoint = None
        
        intersectPoint, intersectNormal = self.getIntersectPointAndNormal()
        if not intersectPoint: 
            return None
        
        self.newJoint = self.getJoint()
        
        cmds.undoInfo( swf=0 )
        cmds.select( self.newJoint )
        cmds.setAttr( self.newJoint+'.dla', 1 )
        
        self.origPosition = OpenMaya.MPoint( *cmds.xform( self.newJoint, q=1, ws=1, t=1 ) )
        
        cmds.move( intersectPoint.x, intersectPoint.y, intersectPoint.z, self.newJoint, ws=1 )
        angle = cmds.angleBetween( v1=[0,0,1], v2=[intersectNormal.x,intersectNormal.y,intersectNormal.z], er=1 )
        cmds.rotate( angle[0], angle[1], angle[2], self.newJoint, ws=1 )
        cmds.refresh()
    

    def doDrag(self, *args, **kwargs):
        if not self.newJoint: return None
        
        intersectPoint, intersectNormal = self.getIntersectPointAndNormal()
        if not intersectPoint: 
            return None
        
        cmds.move( intersectPoint.x, intersectPoint.y, intersectPoint.z, self.newJoint, ws=1 )
        angle = cmds.angleBetween( v1=[0,0,1], v2=[intersectNormal.x,intersectNormal.y,intersectNormal.z], er=1 )
        cmds.rotate( angle[0], angle[1], angle[2], self.newJoint, ws=1 )
        cmds.refresh()
        self.movedPosition = intersectPoint


    def doRelease(self, *args, **kwargs):
        cmds.setAttr( self.newJoint+'.dla', 0 )
        print self.origPosition
        print self.origPosition.x, self.origPosition.y, self.origPosition.z
        cmds.move( self.origPosition.x, self.origPosition.y, self.origPosition.z, self.newJoint, ws=1 )
        cmds.undoInfo( swf=1 )
        cmds.move( self.movedPosition.x, self.movedPosition.y, self.movedPosition.z, self.newJoint, ws=1 )




class PutObjectContextCommand( OpenMayaMPx.MPxContextCommand ):
    
    commandName = "PutObjectContextCommand"
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
