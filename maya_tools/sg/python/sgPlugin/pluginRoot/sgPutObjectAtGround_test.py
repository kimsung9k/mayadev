import sys
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMayaMPx as OpenMayaMPx

import maya.OpenMayaUI
from PySide import QtGui, QtCore
import shiboken


mayaWin = shiboken.wrapInstance( long( maya.OpenMayaUI.MQtUtil.mainWindow() ), QtGui.QWidget )

lineEditName   = "sgui_putObjectAtGround_lineEdit"
listWidgetName = "sgui_putObjectAtGround_listWidget"


def getMObject( nodeName ):
    
    selList = OpenMaya.MSelectionList()
    selList.add( nodeName )
    oNode = OpenMaya.MObject()
    selList.getDependNode( 0, oNode )
    return oNode


def getDagPath( nodeName ):
    if not cmds.objExists( nodeName ): return None
    selList = OpenMaya.MSelectionList()
    selList.add( nodeName )
    dagPath = OpenMaya.MDagPath()
    selList.getDagPath( 0, dagPath )
    return dagPath


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




class ViewportEventFilter( QtCore.QObject ):
    
    def __init__(self):
        QtCore.QObject.__init__(self)
    
    
    def eventFilter(self, obj, event ):
        if event.type() == QtCore.QEvent.MouseMove:
            activeView = OpenMayaUI.M3dView().active3dView()
            PutObjectContext.doMove( event.x(), activeView.portHeight() - event.y() )
        if not event.type() in [QtCore.QEvent.Wheel] : return None
        #print "wheel modified_"
        return 1




class Tool_global:
    mouseX = 0
    mouseY = 0
    currentGlWidget = None
    currentEventFilter = ViewportEventFilter()
    
    groundTextWidget = None
    putObjectWidget  = None
    
    ground = ''
    groundShape = ''
    selItem = ''
    instShape = ''
    duTarget = ''
    
    isDragging = False




class MainWindowEventFilter(QtCore.QObject):
    
    def __init__(self):
        QtCore.QObject.__init__(self)


    def eventFilter(self, obj, event): 
        
        focusWidget = QtGui.QApplication.focusWidget()

        if not focusWidget:
            try:
                Tool_global.currentGlWidget.removeEventFilter( Tool_global.currentEventFilter )
            except:
                pass
            return None

        widgetChildren = focusWidget.children()
        
        if not widgetChildren:
            try:
                Tool_global.currentGlWidget.removeEventFilter( Tool_global.currentEventFilter )
            except:
                pass
            return None

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
                Tool_global.currentGlWidget.removeEventFilter( Tool_global.currentEventFilter )
                Tool_global.currentGlWidget = None
        else:
            if Tool_global.currentGlWidget != glWidget:
                if Tool_global.currentGlWidget:
                    Tool_global.currentGlWidget.removeEventFilter( Tool_global.currentEventFilter )
                Tool_global.currentGlWidget = glWidget
                Tool_global.currentGlWidget.installEventFilter( Tool_global.currentEventFilter )
        return False





class Functions:
    
    @staticmethod
    def getSelectedObject():
        
        ground = Tool_global.groundTextWidget.text()
        selItem = ''
        for SelectedItem in Tool_global.putObjectWidget.selectedItems():
            selItem = SelectedItem.text()
        
        Tool_global.ground = ground
        Tool_global.groundShape = cmds.listRelatives( ground, s=1, f=1 )[0]
        Tool_global.selItem = selItem
    
        return ground, selItem
    
    
    @staticmethod
    def getInstanceObject():
        
        instObjName = 'sgPutObjectAtGround_instObj'
        if cmds.objExists( instObjName ): return instObjName
        
        cmds.undoInfo( swf=0 )
        ground, selItem = Functions.getSelectedObject()
        
        selItemShape = cmds.listRelatives( selItem, s=1, f=1 )
        if not selItemShape: return None
        selItemShape = selItemShape[0]
        shapeType = cmds.nodeType( selItemShape )
        
        instObjShape = cmds.createNode( shapeType )
        instObj = cmds.listRelatives( instObjShape, p=1, f=1 )[0]
        instObj = cmds.rename( instObj, instObjName )
        instObjShape = cmds.listRelatives( instObj, s=1, f=1 )[0]
        Tool_global.instShape = instObjShape
        
        if shapeType in ['nurbsSurface', 'nurbsCurve']:
            inputAttr = 'create'
            outputAttr = 'local'
        elif shapeType == 'mesh':
            inputAttr = 'inMesh'
            outputAttr = 'outMesh'
        
        if not cmds.isConnected( selItemShape + '.' + outputAttr, Tool_global.instShape + '.' + inputAttr ):
            cmds.connectAttr( selItemShape + '.' + outputAttr, Tool_global.instShape + '.' + inputAttr, f=1 )
        cmds.undoInfo( swf=1 )
        
        return instObj
    
    
    @staticmethod
    def clearInstance():
        cmds.undoInfo( swf=0 )
        if cmds.objExists( Tool_global.instShape ):
            instObj = cmds.listRelatives( Tool_global.instShape, p=1, f=1 )[0]
            cmds.delete( instObj )
        cmds.undoInfo( swf=1 )
        


    @staticmethod
    def getIntersectPointAndNormal( mouseX, mouseY, meshDagPath=None ):
        
        activeView = OpenMayaUI.M3dView().active3dView()
        nearPoint = OpenMaya.MPoint()
        farPoint  = OpenMaya.MPoint()
        activeView.viewToWorld( mouseX, mouseY, nearPoint, farPoint )
        
        if meshDagPath:
            meshMatrix = meshDagPath.inclusiveMatrix()
            invMtx = meshDagPath.inclusiveMatrixInverse()
            
            nearPoint *= invMtx
            farPoint  *= invMtx
            
            fnMesh = OpenMaya.MFnMesh( meshDagPath )
            intersectPoints = OpenMaya.MPointArray()
            
            fnMesh.intersect( nearPoint, farPoint - nearPoint, intersectPoints )
            
            if not intersectPoints.length(): return OpenMaya.MPoint(), OpenMaya.MVector()
            normal = OpenMaya.MVector()
            fnMesh.getClosestNormal( intersectPoints[0], normal, OpenMaya.MSpace.kTransform )
            return intersectPoints[0] * meshMatrix, normal * meshMatrix
        else:
            return OpenMaya.MPoint(), OpenMaya.MVector()
            #t = ( -D - (A,B,C)*P0 ) / ( A,B,C )*( P1-P0 )
    
    
    @staticmethod
    def copyShader( src, dst ):
        
        shadingEngine = cmds.listConnections( src, s=0, d=1, type='shadingEngine' )
        if not shadingEngine: 
            cmds.sets( dst, e=1, forceElement='initialShadingGroup' )
        else:
            cmds.sets( dst, e=1, forceElement=shadingEngine[0] )
    
    


class PutObjectContext( OpenMayaMPx.MPxSelectionContext ):

    contextName = 'sgPutObjectAtGroundContext'
    
    def __init__(self):
        OpenMayaMPx.MPxSelectionContext.__init__( self )


    def toolOnSetup(self, *args, **kwargs ):
        
        Tool_global.groundTextWidget = mayaWin.findChild( QtGui.QLineEdit, lineEditName )
        Tool_global.putObjectWidget  = mayaWin.findChild( QtGui.QListWidget, listWidgetName )
        
        meshShape = getSelection()
        
        if meshShape:
            self.meshName = meshShape
            self.dagPath = getDagPath( meshShape )
        else:
            self.dagPath = None
        
        OpenMayaMPx.MPxSelectionContext.toolOnSetup( self, *args, **kwargs )
        self.eventFilter   = MainWindowEventFilter()
        self.mainWindowPtr = mayaWin
        self.mainWindowPtr.installEventFilter( self.eventFilter )


    def toolOffCleanup( self, *args, **kwargs ):
        try:
            Tool_global.currentGlWidget.removeEventFilter( Tool_global.currentEventFilter )
        except:
            pass
        self.mainWindowPtr.removeEventFilter( self.eventFilter )
        OpenMayaMPx.MPxSelectionContext.toolOffCleanup(self, *args, **kwargs )
        Functions.clearInstance()


    def className( self, *args, **kwargs):
        OpenMayaMPx.MPxSelectionContext.className(self, *args, **kwargs)
    
    
    @staticmethod
    def doMove( mouseX, mouseY ):
        
        if Tool_global.isDragging: return None
        instObj = Functions.getInstanceObject()
        intersectPoint, intersectNormal = Functions.getIntersectPointAndNormal( mouseX, mouseY, getDagPath( Tool_global.groundShape ) )        
        cmds.undoInfo( swf=0 )
        cmds.move( intersectPoint.x, intersectPoint.y, intersectPoint.z, instObj )
        cmds.undoInfo( swf=1 )


    
    def doPress( self, event ):
        
        import maya.mel as mel
        
        argX = OpenMaya.MScriptUtil()
        argX.createFromInt(0)
        argXPtr = argX.asShortPtr()
        argY = OpenMaya.MScriptUtil()
        argY.createFromInt(0)
        argYPtr = argY.asShortPtr()
        event.getPosition(argXPtr, argYPtr)
        mouseX = OpenMaya.MScriptUtil(argXPtr).asShort()
        mouseY = OpenMaya.MScriptUtil(argYPtr).asShort()
        
        mel.eval( '%s -s %s -n %s' %( PutObjectCommand.commandName, Functions.getSelectedObject()[1], Functions.getSelectedObject()[1] + '_du' ) )
        
        intersectPoint, intersectNormal = Functions.getIntersectPointAndNormal( mouseX, mouseY, getDagPath( Tool_global.groundShape ) )        
        cmds.undoInfo( swf=0 )
        cmds.move( intersectPoint.x, intersectPoint.y, intersectPoint.z, Tool_global.duTarget )
        Functions.clearInstance()
        cmds.refresh()
        
        cmds.undoInfo( swf=1 )
        
        Tool_global.isDragging = True
        
    

    def doDrag(self, event ):
        
        argX = OpenMaya.MScriptUtil()
        argX.createFromInt(0)
        argXPtr = argX.asShortPtr()
        argY = OpenMaya.MScriptUtil()
        argY.createFromInt(0)
        argYPtr = argY.asShortPtr()
        event.getPosition(argXPtr, argYPtr)
        mouseX = OpenMaya.MScriptUtil(argXPtr).asShort()
        mouseY = OpenMaya.MScriptUtil(argYPtr).asShort()
        
        intersectPoint, intersectNormal = Functions.getIntersectPointAndNormal( mouseX, mouseY, getDagPath( Tool_global.groundShape ) )        
        cmds.undoInfo( swf=0 )
        cmds.move( intersectPoint.x, intersectPoint.y, intersectPoint.z, Tool_global.duTarget )
        cmds.undoInfo( swf=1 )
        cmds.refresh()


    def doRelease(self, event ):
        
        Tool_global.isDragging = False
        pass





class PutObjectContextCommand( OpenMayaMPx.MPxContextCommand ):
    
    commandName = "sgPutObjectAtGroundContextCommand"
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




import maya.api.OpenMaya as om


class PutObjectCommand( OpenMayaMPx.MPxCommand ): 
    
    commandName = 'sgPutObjectAtGroundCommand'

    kNameFlags  = ['-n', '-name' ]
    kSourceFlags  = ['-s', '-source']
    
    @staticmethod
    def creator():
        return OpenMayaMPx.asMPxPtr(PutObjectCommand())
    
    
    @staticmethod
    def newSyntax():
        syntax = OpenMaya.MSyntax()
        syntax.addFlag(PutObjectCommand.kNameFlags[0],  PutObjectCommand.kNameFlags[1], OpenMaya.MSyntax.kString )
        syntax.addFlag(PutObjectCommand.kSourceFlags[0],  PutObjectCommand.kSourceFlags[1], OpenMaya.MSyntax.kString )
        return syntax


    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)        
        self.__source = ''
        self.__name   = ''
        self.__newObject = ''
    
    
    def doIt(self, *args):
        
        argData = OpenMaya.MArgDatabase(self.syntax(), *args )
    
        if argData.isFlagSet( PutObjectCommand.kNameFlags[0] ):
            self.__name  = argData.flagArgumentString(PutObjectCommand.kNameFlags[0], 0 )
        if argData.isFlagSet( PutObjectCommand.kSourceFlags[0] ):
            self.__source  = argData.flagArgumentString(PutObjectCommand.kSourceFlags[0], 0 )
        
        self.redoIt()


    def redoIt(self):

        if not cmds.objExists( self.__source ): return None
        if cmds.nodeType( self.__source ) == 'transform':
            sourceShape = cmds.listRelatives( self.__source, s=1, f=1 )[0]
        else:
            sourceShape = self.__source
            
        self.modifier = OpenMaya.MDagModifier()
        sourceDagPath = getDagPath( sourceShape )
        self.newMeshTransform = self.modifier.createNode('transform')
        self.modifier.renameNode( self.newMeshTransform, self.__name )
        self.modifier.doIt()
        
        fnMesh = OpenMaya.MFnMesh( sourceDagPath )
        fnMesh.copy( sourceDagPath.node(), self.newMeshTransform )
        self.__newObject = OpenMaya.MFnTransform(self.newMeshTransform).partialPathName()
        OpenMayaMPx.MPxCommand.setResult( self.__newObject )


    def undoIt(self):

        if cmds.objExists( self.__newObject ):
            OpenMaya.MGlobal.executeCommand( 'delete %s' % self.__newObject )
        
    
    def isUndoable(self):
        return True





# initialize the script plug-in
def initializePlugin(mobject):
    import maya.mel as mel
    
    mplugin = OpenMayaMPx.MFnPlugin(mobject, "Autodesk", "1.0", "Any")
    mplugin.registerContextCommand( PutObjectContextCommand.commandName,
                                    PutObjectContextCommand.creator )
    mplugin.registerCommand( PutObjectCommand.commandName, PutObjectCommand.creator, PutObjectCommand.newSyntax )
    
    mel.eval( "%s %s1" %( PutObjectContextCommand.commandName, PutObjectContext.contextName ))



# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    import maya.mel as mel
    
    mel.eval( "deleteUI %s1" %( PutObjectContext.contextName ) )
    
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    mplugin.deregisterContextCommand( PutObjectContextCommand.commandName )
    mplugin.deregisterCommand( PutObjectCommand.commandName )

