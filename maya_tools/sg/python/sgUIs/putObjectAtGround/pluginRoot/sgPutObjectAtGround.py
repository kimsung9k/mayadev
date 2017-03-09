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





class ViewportEventFilter( QtCore.QObject ):
    
    def __init__(self):
        QtCore.QObject.__init__(self)
    
    
    def eventFilter(self, obj, event ):
        if event.type() == QtCore.QEvent.MouseMove:
            activeView = OpenMayaUI.M3dView().active3dView()
            PutObjectContext.doMove( event.x(), activeView.portHeight() - event.y() )
        if event.type() in [QtCore.QEvent.Wheel] :
            return 1




class Tool_global:
    mouseX = 0
    mouseY = 0
    offsetMouseX = 0
    offsetMouseY = 0
    currentGlWidget = None
    currentEventFilter = ViewportEventFilter()
    
    groundTextWidget = None
    putObjectWidget  = None
    
    ground = ''
    groundShape = ''
    selItem = ''
    instShape = ''
    duTarget = ''
    
    ctrlPressed  = False
    shiftPressed = False
    
    intersectPoint = OpenMaya.MPoint()
    intersectNormal = OpenMaya.MVector()
    intersectOffset = OpenMaya.MPoint()
    
    outerRotMatrix = OpenMaya.MMatrix()
    
    @staticmethod
    def setDefault():
        Tool_global.intersectPoint = OpenMaya.MPoint()
        Tool_global.intersectNormal = OpenMaya.MVector()
        Tool_global.intersectOffset = OpenMaya.MPoint()
        Tool_global.outerRotMatrix = OpenMaya.MMatrix()




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
        
        selItem = cmds.textScrollList( listWidgetName, q=1, si=1 )
        if not selItem:
            selItem = cmds.textScrollList( listWidgetName, q=1, ai=1 )
        return selItem[0]
    
    
    @staticmethod
    def getGround():    
        return cmds.textField( lineEditName, q=1, tx=1 )
    
    
    
    @staticmethod
    def getInstanceObject():
        
        instObjName = 'sgPutObjectAtGround_instObj'
        selItem = Functions.getSelectedObject()
        selItemShape = cmds.listRelatives( selItem, s=1, f=1 )
        if not selItemShape: return None
        selItemShape = selItemShape[0]
        if cmds.objExists( instObjName ): 
            instObjShape = cmds.listRelatives( instObjName, s=1, f=1 )[0]
            if not cmds.isConnected( selItemShape + '.outMesh', instObjShape + '.inMesh' ):
                cmds.undoInfo( swf=0 )
                cmds.connectAttr( selItemShape + '.outMesh', instObjShape + '.inMesh', f=1 )
                cmds.undoInfo( swf=1 )
            return instObjName
        
        cmds.undoInfo( swf=0 )
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
        shadingEngine = cmds.listConnections( selItemShape, s=0, d=1, type='shadingEngine' )
        if not shadingEngine: 
            cmds.sets( instObjShape, e=1, forceElement='initialShadingGroup' )
        else:
            cmds.sets( instObjShape, e=1, forceElement=shadingEngine[0] )
        cmds.undoInfo( swf=1 )
        
        return instObj
    


    @staticmethod
    def clearInstance():
        cmds.undoInfo( swf=0 )
        cmds.delete( Functions.getInstanceObject() )
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
            return intersectPoints[0] * meshMatrix, (normal * meshMatrix).normal()
        else:
            return OpenMaya.MPoint(), OpenMaya.MVector(0,1,0)
            #t = ( -D - (A,B,C)*P0 ) / ( A,B,C )*( P1-P0 )
    
    
    @staticmethod
    def copyObject( src ):
        
        dst = cmds.createNode( 'transform', n=src + '_du' )
        srcShape = cmds.listRelatives( src, s=1, f=1 )[0]
        OpenMaya.MFnMesh().copy( getMObject( srcShape ), getMObject( dst ) )
        dstShape = cmds.listRelatives( dst, s=1, f=1 )[0]
        
        shadingEngine = cmds.listConnections( srcShape, s=0, d=1, type='shadingEngine' )
        if not shadingEngine: 
            cmds.sets( dstShape, e=1, forceElement='initialShadingGroup' )
        else:
            cmds.sets( dstShape, e=1, forceElement=shadingEngine[0] )
    
    
    @staticmethod
    def getRotationFromNormal( normalVector ):
        import math
        yVector = OpenMaya.MVector( 0,1,0 )
        rotValue = yVector.rotateTo( normalVector ).asEulerRotation().asVector()
        return math.degrees( rotValue.x ), math.degrees( rotValue.y ), math.degrees( rotValue.z )
    
    
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
    
    
    
    @staticmethod
    def viewPointToWorldPoint( inputViewPoint ):
        
        viewPoint = OpenMaya.MPoint( inputViewPoint.x, inputViewPoint.y, inputViewPoint.z )
        activeView = OpenMayaUI.M3dView().active3dView()
        camDagPath = OpenMaya.MDagPath()
        activeView.getCamera( camDagPath )
        
        projectionMatrix = OpenMaya.MMatrix()
        activeView.projectionMatrix(projectionMatrix)
        camMatrix = camDagPath.inclusiveMatrix()
        
        viewPoint.x = viewPoint.x/activeView.portWidth()*2-1
        viewPoint.y = viewPoint.y/activeView.portHeight()*2-1
        worldPoint = viewPoint * projectionMatrix.inverse()
        worldPoint.x = worldPoint.x/worldPoint.w
        worldPoint.y = worldPoint.y/worldPoint.w
        worldPoint.z = worldPoint.z/worldPoint.w
        worldPoint.w = 1
        return worldPoint * camMatrix



    @staticmethod
    def getRotationMatrix( inputVector, rotValue ):
        
        import math
        cos = math.cos
        sin = math.sin
        
        vector = inputVector.normal()
        wx = vector.x
        wy = vector.y
        wz = vector.z
        r = rotValue
        
        rotMatrixList = [ cos( r ) - ( cos(r)-1 )*wx*wx, ( 1 - cos(r) )*wx*wy - sin(r)*wz, sin(r)*wy - ( cos(r) - 1 )*wx*wz, 0,
                         (1-cos(r))*wx*wy + sin(r)*wz, cos(r)-(cos(r)-1)*wy*wy, -sin(r)*wx-(cos(r)-1)*wy*wz, 0,
                         -sin(r)*wy - ( cos(r)-1 )*wx*wz, sin(r)*wx - ( cos(r)-1 )*wy*wz, cos(r) - ( cos(r)-1 )*wz*wz, 0,
                         0,0,0,1]
        
        rotMatrix = OpenMaya.MMatrix()
        OpenMaya.MScriptUtil.createMatrixFromList( rotMatrixList, rotMatrix )
        return rotMatrix
    
    
    @staticmethod
    def getCamVector():
        
        activeView = OpenMayaUI.M3dView().active3dView()
        camDagPath = OpenMaya.MDagPath()
        activeView.getCamera( camDagPath )
        
        return OpenMaya.MVector( camDagPath.inclusiveMatrix()[3] )
    
    
    @staticmethod
    def getRotationMatrixFromNormal( normalVector ):
        yVector = OpenMaya.MVector( 0,1,0 )
        return yVector.rotateTo( normalVector ).asMatrix()
    
    
    
    


class PutObjectContext( OpenMayaMPx.MPxSelectionContext ):

    contextName = 'sgPutObjectAtGroundContext'
    
    def __init__(self):
        OpenMayaMPx.MPxSelectionContext.__init__( self )


    def toolOnSetup(self, *args, **kwargs ):
        
        meshShape = getSelection()
        
        if meshShape:
            self.meshName = meshShape
            self.dagPath = getDagPath( meshShape )
        else:
            self.dagPath = None
        
        OpenMayaMPx.MPxSelectionContext.toolOnSetup( self, *args, **kwargs )
        Tool_global.eventFilter   = MainWindowEventFilter()
        Tool_global.mainWindowPtr = mayaWin
        Tool_global.mainWindowPtr.installEventFilter( Tool_global.eventFilter )
        
        cmds.undoInfo( swf=0 )
        Tool_global.locator = cmds.spaceLocator()[0]
        cmds.undoInfo( swf=1 )
        
        Tool_global.setDefault()
        


    def toolOffCleanup( self, *args, **kwargs ):
        try:
            Tool_global.currentGlWidget.removeEventFilter( Tool_global.currentEventFilter )
        except:
            pass
        Tool_global.mainWindowPtr.removeEventFilter( Tool_global.eventFilter )
        OpenMayaMPx.MPxSelectionContext.toolOffCleanup(self, *args, **kwargs )
        Functions.clearInstance()
        
        cmds.undoInfo( swf=0 )
        #cmds.delete( Tool_global.locator )
        cmds.undoInfo( swf=1 )


    def className( self, *args, **kwargs):
        OpenMayaMPx.MPxSelectionContext.className(self, *args, **kwargs)
    
    
    @staticmethod
    def doMove( mouseX, mouseY ):
        
        import math
        cmds.undoInfo( swf=0 )
        
        instObj = Functions.getInstanceObject()
        ground = Functions.getGround()
        groundShape = cmds.listRelatives( ground, s=1, f=1 )[0]
        
        intersectPoint, intersectNormal = Functions.getIntersectPointAndNormal( mouseX, 
                                                                                mouseY, 
                                                                                getDagPath( groundShape ) )
        
        modifiers = QtGui.QApplication.keyboardModifiers()
        
        if modifiers == QtCore.Qt.ControlModifier and modifiers != QtCore.Qt.ShiftModifier:
            srcPoint = Tool_global.intersectPoint
            dstPoint = srcPoint + Tool_global.intersectNormal
            srcViewPoint = Functions.worldPointToViewPoint( srcPoint )
            dstViewPoint = Functions.worldPointToViewPoint( dstPoint )
            mousePoint = OpenMaya.MPoint( mouseX, mouseY, 0 )
            lineVector = dstViewPoint - srcViewPoint
            mouseVector = mousePoint - srcViewPoint
            projVector = lineVector * (lineVector * mouseVector)/( lineVector.length()**2 )
            paramValue = projVector.length()/lineVector.length()
            if projVector * lineVector < 0:
                paramValue *= -1
            Tool_global.intersectOffset = Tool_global.intersectNormal * paramValue
            cmds.move( Tool_global.intersectOffset.x + Tool_global.intersectPoint.x, 
                       Tool_global.intersectOffset.y + Tool_global.intersectPoint.y, 
                       Tool_global.intersectOffset.z + Tool_global.intersectPoint.z, instObj )
            
        elif modifiers != QtCore.Qt.ControlModifier and modifiers == QtCore.Qt.ShiftModifier:
            srcPoint = Tool_global.intersectPoint
            srcViewPoint = Functions.worldPointToViewPoint( srcPoint )
            mousePoint = OpenMaya.MPoint( mouseX, mouseY, 0 )
            
            mouseWorldPoint     = Functions.viewPointToWorldPoint( mousePoint )
            srcViewPointToWorld = Functions.viewPointToWorldPoint( srcViewPoint )
            
            directionVector = mouseWorldPoint - srcViewPointToWorld
            camVector = Functions.getCamVector()
            crossVector = directionVector ^ camVector
            
            viewPointVector = OpenMaya.MVector(mousePoint) - OpenMaya.MVector(srcViewPoint)
            rotValue = viewPointVector.length()

            rotMatrix = Functions.getRotationMatrixFromNormal( Tool_global.intersectNormal )
            outerRotMatrix = Functions.getRotationMatrix( crossVector, math.radians(rotValue) )
            trRotMatrix = OpenMaya.MTransformationMatrix( rotMatrix*outerRotMatrix )
            rotVector = trRotMatrix.eulerRotation().asVector()
            cmds.rotate( math.degrees(rotVector.x), math.degrees(rotVector.y), math.degrees(rotVector.z), instObj )
            Tool_global.outerRotMatrix = outerRotMatrix
            
        elif modifiers == QtCore.Qt.ControlModifier and modifiers == QtCore.Qt.ShiftModifier:
            pass
        
        else:
            Tool_global.intersectPoint = intersectPoint
            Tool_global.intersectNormal = intersectNormal
            
            rotValue = Functions.getRotationFromNormal( intersectNormal )     
            cmds.move( Tool_global.intersectOffset.x + Tool_global.intersectPoint.x, 
                       Tool_global.intersectOffset.y + Tool_global.intersectPoint.y, 
                       Tool_global.intersectOffset.z + Tool_global.intersectPoint.z, instObj )
            
            rotMatrix = Functions.getRotationMatrixFromNormal( Tool_global.intersectNormal )
            trRotMatrix = OpenMaya.MTransformationMatrix( rotMatrix*Tool_global.outerRotMatrix )
            rotVector = trRotMatrix.eulerRotation().asVector()
            cmds.rotate( math.degrees(rotVector.x), math.degrees(rotVector.y), math.degrees(rotVector.z), instObj )
        
        cmds.undoInfo( swf=1 )


    
    def doPress( self, event ):
        
        import math
        
        targetObject = Functions.getSelectedObject()
        
        cmds.undoInfo( ock=1 )
        copyObject = Functions.copyObject( targetObject )     
        cmds.move( Tool_global.intersectOffset.x + Tool_global.intersectPoint.x, 
                       Tool_global.intersectOffset.y + Tool_global.intersectPoint.y, 
                       Tool_global.intersectOffset.z + Tool_global.intersectPoint.z, copyObject ) 
        rotMatrix = Functions.getRotationMatrixFromNormal( Tool_global.intersectNormal )
        trRotMatrix = OpenMaya.MTransformationMatrix( rotMatrix*Tool_global.outerRotMatrix )
        rotVector = trRotMatrix.eulerRotation().asVector()
        cmds.rotate( math.degrees(rotVector.x), math.degrees(rotVector.y), math.degrees(rotVector.z), copyObject )
        cmds.undoInfo( cck=1 )
        
        self.copyObject = copyObject
        

    def doDrag(self, event ):
        
        pass


    def doRelease(self, event ):
        
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
    
    try:
        Tool_global.currentGlWidget.releaseKeyboard();
        Tool_global.currentGlWidget.removeEventFilter( Tool_global.currentEventFilter )
    except:
        pass
    
    try:
        Tool_global.mainWindowPtr.removeEventFilter( Tool_global.eventFilter )
    except:
        pass
    
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    mplugin.deregisterContextCommand( PutObjectContextCommand.commandName )

