import sys
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMayaMPx as OpenMayaMPx

import maya.OpenMayaUI
if int( cmds.about( v=1 ) ) < 2017:
    from PySide import QtGui, QtCore
    import shiboken
    from PySide.QtGui import QListWidgetItem, QDialog, QListWidget, QMainWindow, QWidget, QColor, QLabel,\
    QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QAbstractItemView, QMenu,QCursor, QMessageBox, QBrush, QSplitter,\
    QScrollArea, QSizePolicy, QTextEdit, QApplication, QFileDialog, QCheckBox, QDoubleValidator, QSlider, QIntValidator,\
    QImage, QPixmap, QTransform, QPaintEvent, QTabWidget, QFrame, QTreeWidgetItem, QTreeWidget, QComboBox, QGroupBox
else:
    from PySide2 import QtGui, QtCore, QtWidgets
    import shiboken2 as shiboken
    from PySide2.QtWidgets import QListWidgetItem, QDialog, QListWidget, QMainWindow, QWidget, QVBoxLayout, QLabel,\
    QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QAbstractItemView, QMenu, QMessageBox, QSplitter,\
    QScrollArea, QSizePolicy, QTextEdit, QApplication, QFileDialog, QCheckBox, QSlider,\
    QTabWidget, QFrame, QTreeWidgetItem, QTreeWidget, QComboBox, QGroupBox
    
    from PySide2.QtGui import QColor, QCursor, QBrush, QDoubleValidator, QIntValidator, QImage, QPixmap, QTransform,\
    QPaintEvent


class Window_global:
    
    mayaWin = shiboken.wrapInstance( long( maya.OpenMayaUI.MQtUtil.mainWindow() ), QWidget )

    objectName = 'sgui_putObjectOnGround'
    listWidgetPutName      =  objectName + "_listPut"
    listWidgetGroundName   =  objectName + "_listGround"
    randomOptionRotName    =  objectName + "_randomRot"
    randomOptionRotAName   =  objectName + "_randomRotAll"
    randomOptionScaleName  =  objectName + "_randomScale"
    randomOptionScaleAName =  objectName + "_randomScaleAll"
    offsetByObjectName     = objectName + '_offsetObject'
    offsetByGroundName     = objectName + '_offsetGround'
    checkNormalOrientName  = objectName + '_checkNormalOrient'
    orientEditModeName     = objectName + '_orientEditMode'
    duGroupListName        = objectName + '_duGroupList'
    componentCheckName         = objectName + '_componentCheck'
    
    windowObject = None
    ui_listWidgetPut = None
    ui_listWidgetGround = None
    ui_randomOptionRot = None
    ui_randomOptionScale = None
    ui_randomOptionRotA = None
    ui_randomOptionScaleA = None
    ui_offsetByObject = None
    ui_offsetByGround = None
    ui_checkNormalOrient = None
    ui_orientEditMode    = None
    ui_duGroupList = None
    ui_componentCheck = None
    
    @staticmethod
    def getUIObjects():        
        windowObject          = Window_global.mayaWin.findChild( QMainWindow, Window_global.objectName )
        ui_listWidgetPut      = windowObject.findChild( QWidget, Window_global.listWidgetPutName )
        ui_listWidgetGround   = windowObject.findChild( QWidget, Window_global.listWidgetGroundName )
        ui_randomOptionRot    = windowObject.findChild( QWidget, Window_global.randomOptionRotName )
        ui_randomOptionScale  = windowObject.findChild( QWidget, Window_global.randomOptionScaleName )
        ui_randomOptionRotA   = windowObject.findChild( QWidget, Window_global.randomOptionRotAName )
        ui_randomOptionScaleA = windowObject.findChild( QWidget, Window_global.randomOptionScaleAName )
        ui_offsetByObject     = windowObject.findChild( QWidget, Window_global.offsetByObjectName )
        ui_offsetByGround     = windowObject.findChild( QWidget, Window_global.offsetByGroundName )
        ui_checkNormalOrient  = windowObject.findChild( QWidget, Window_global.checkNormalOrientName )
        ui_orientEditMode     = windowObject.findChild( QWidget, Window_global.orientEditModeName )
        ui_duGroupList        = windowObject.findChild( QWidget, Window_global.duGroupListName )
        ui_componentCheck         = windowObject.findChild( QWidget, Window_global.componentCheckName)

        Window_global.windowObject = windowObject
        Window_global.ui_listWidgetPut       = ui_listWidgetPut
        Window_global.ui_listWidgetGround    = ui_listWidgetGround
        Window_global.ui_randomOptionRot     = ui_randomOptionRot
        Window_global.ui_randomOptionScale   = ui_randomOptionScale
        Window_global.ui_randomOptionRotA    = ui_randomOptionRotA
        Window_global.ui_randomOptionScaleA  = ui_randomOptionScaleA
        Window_global.ui_offsetByObject      = ui_offsetByObject
        Window_global.ui_offsetByGround      = ui_offsetByGround
        Window_global.ui_checkNormalOrient   = ui_checkNormalOrient
        Window_global.ui_orientEditMode      = ui_orientEditMode
        Window_global.ui_duGroupList         = ui_duGroupList
        Window_global.ui_componentCheck          = ui_componentCheck
        


def matrixToList( matrix ):
    mtxList = range( 16 )
    for i in range( 4 ):
        for j in range( 4 ):
            mtxList[ i * 4 + j ] = matrix( i, j )
    return mtxList


def listToMatrix( mtxList ):
    matrix = OpenMaya.MMatrix()
    OpenMaya.MScriptUtil.createMatrixFromList( mtxList, matrix  )
    return matrix



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
    mousePressed = False
    currentSize = 1
    
    stilPressed_shift   = False
    stilPressed_control = False
    
    randomIndex = 0
    
    currentGlWidget = None
    currentEventFilter = ViewportEventFilter()
    
    groundTextWidget = None
    putObjectWidget  = None
    
    ground = ''
    groundShape = ''
    selItem = ''
    instShape = ''
    duTarget = ''
    
    intersectPoint  = OpenMaya.MPoint()
    intersectNormal = OpenMaya.MVector()
    defaultMatrix = OpenMaya.MMatrix()
    scaledMatrix  = OpenMaya.MMatrix()
    rotatedMatrix = OpenMaya.MMatrix()
    normalRotMatrix  = OpenMaya.MMatrix()
    randomMatrix  = OpenMaya.MMatrix()
    transMatrix = OpenMaya.MMatrix()
    scaleEditMatrix = OpenMaya.MMatrix()
    rotationEditMatrix = OpenMaya.MMatrix()
    rotationYEditMatrix = OpenMaya.MMatrix()
    
    randomMatrixExists = False
    
    targetViewSize = None
    instancePoints = OpenMaya.MPointArray()
    
    beforeInstObj = None
    
    @staticmethod
    def setDefault():
        Tool_global.intersectPoint = OpenMaya.MPoint()
        Tool_global.intersectNormal = OpenMaya.MVector()
        Tool_global.intersectOffset = OpenMaya.MPoint()
        Tool_global.defaultMatrix = OpenMaya.MMatrix()
        Tool_global.rotatedMatrix = OpenMaya.MMatrix()
        Tool_global.beforeInstObj = None
        Tool_global.randomMatrixExists = False
        Tool_global.targetViewSize = None
        Tool_global.instancePoints = OpenMaya.MPointArray()




class MainWindowEventFilter(QtCore.QObject):
    
    def __init__(self):
        QtCore.QObject.__init__(self)


    def eventFilter(self, obj, event): 
        
        focusWidget = QApplication.focusWidget()

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
                try:Tool_global.currentGlWidget.removeEventFilter( Tool_global.currentEventFilter )
                except:pass
                Tool_global.currentGlWidget = None
        else:
            if Tool_global.currentGlWidget != glWidget:
                if Tool_global.currentGlWidget:
                    try:Tool_global.currentGlWidget.removeEventFilter( Tool_global.currentEventFilter )
                    except:pass
                Tool_global.currentGlWidget = glWidget
                Tool_global.currentGlWidget.installEventFilter( Tool_global.currentEventFilter )
        return False





class Functions:
    
    @staticmethod
    def getSelectedObject():
        
        selWidgets = Window_global.ui_listWidgetPut.selectedItems()
        if not selWidgets:
            selWidgets = []
            for i in range( Window_global.ui_listWidgetPut.count() ):
                selWidgets.append( Window_global.ui_listWidgetPut.item(i) )
        selItems = []
        for selWidget in selWidgets:
            selItems.append( selWidget.text() )
        return selItems[ Tool_global.randomIndex % len( selItems ) ]



    @staticmethod
    def getGround():
        
        groundItems = []
        for i in range( Window_global.ui_listWidgetGround.count() ):
            groundItems.append( Window_global.ui_listWidgetGround.item(i).text() )
        return groundItems
        


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
                cmds.connectAttr( selItemShape + '.outMesh', instObjShape + '.inMesh', f=1 )
                dagPath = getDagPath( instObjShape )
                fnMesh = OpenMaya.MFnMesh( dagPath )
                fnMesh.getPoints( Tool_global.instancePoints )
            return instObjName
        
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
            dagPath = getDagPath( instObjShape )
            fnMesh = OpenMaya.MFnMesh( dagPath )
            fnMesh.getPoints( Tool_global.instancePoints )

        shadingEngine = cmds.listConnections( selItemShape, s=0, d=1, type='shadingEngine' )
        if not shadingEngine: 
            cmds.sets( instObjShape, e=1, forceElement='initialShadingGroup' )
        else:
            cmds.sets( instObjShape, e=1, forceElement=shadingEngine[0] )
        
        dagPath = getDagPath( instObjShape )
        fnMesh = OpenMaya.MFnMesh( dagPath )
        fnMesh.getPoints( Tool_global.instancePoints )
        
        return instObj
    


    @staticmethod
    def clearInstance():
        cmds.undoInfo( swf=0 )
        cmds.delete( Functions.getInstanceObject() )
        cmds.undoInfo( swf=1 )
        


    @staticmethod
    def getIntersectPointAndNormal( mouseX, mouseY, meshGrps = [] ):
        
        activeView = OpenMayaUI.M3dView().active3dView()
        nearPoint = OpenMaya.MPoint()
        farPoint  = OpenMaya.MPoint()
        activeView.viewToWorld( mouseX, mouseY, nearPoint, farPoint )
        
        meshShapes = []
        for meshGrp in meshGrps:
            if cmds.nodeType( meshGrp ) == 'mesh':
                meshShapes.append( meshGrp )
            elif cmds.nodeType( meshGrp ) == 'transform':
                shapes = cmds.listRelatives( meshGrp, s=1, f=1 )
                for shape in shapes:
                    if cmds.getAttr( shape + '.io' ): continue
                    if cmds.nodeType( shape ) == 'mesh':
                        meshShapes.append( shape )
        
        allIntersectPointAndNormal = []
        for meshShape in meshShapes:
            meshDagPath = getDagPath( meshShape )
            meshMatrix = meshDagPath.inclusiveMatrix()
            invMtx = meshDagPath.inclusiveMatrixInverse()
            
            localNearPoint = nearPoint * invMtx
            localFarPoint  = farPoint * invMtx
            
            fnMesh = OpenMaya.MFnMesh( meshDagPath )
            intersectPoints = OpenMaya.MPointArray()
            fnMesh.intersect( localNearPoint, localFarPoint - localNearPoint, intersectPoints )
            if intersectPoints.length():
                normal = OpenMaya.MVector()
                fnMesh.getClosestNormal( intersectPoints[0], normal, OpenMaya.MSpace.kTransform )
                allIntersectPointAndNormal.append( [intersectPoints[0]*meshMatrix, normal.normal()*meshMatrix] )
        
        if allIntersectPointAndNormal:
            minDist = 100000000.0
            minDistIndex = 0
            for i in range( len(allIntersectPointAndNormal) ):
                point, normal = allIntersectPointAndNormal[i]
                dist = nearPoint.distanceTo( point )
                if dist < minDist:
                    minDist = dist
                    minDistIndex = i
            return allIntersectPointAndNormal[minDistIndex]
        else:
            return OpenMaya.MPoint(), OpenMaya.MVector(0,1,0)
            #t = ( -D - (A,B,C)*P0 ) / ( A,B,C )*( P1-P0 )
    
    
    @staticmethod
    def copyObject( src ):
        
        numGroups = Window_global.ui_duGroupList.count()
        
        if numGroups:
            for i in range( numGroups ):
                targetItem = Window_global.ui_duGroupList.item(i)
                if not cmds.objExists( targetItem.text() ):
                    Window_global.ui_duGroupList.takeItem( Window_global.ui_duGroupList.row(targetItem) )
            numGroups = Window_global.ui_duGroupList.count()
        
        if not numGroups:
            newGroup = cmds.group( em=1, n='CopyedObjectList' )
            Window_global.ui_duGroupList.addItem( newGroup )
        
        cuItem = Window_global.ui_duGroupList.currentItem()
        if not cuItem:
            Window_global.ui_duGroupList.setCurrentRow( 0 )
        cuItem = Window_global.ui_duGroupList.currentItem()
        
        duObject = cmds.duplicate( src, n= src+'_du' )[0]
        return cmds.parent( duObject, cuItem.text() )[0]
    
    
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
        r = math.radians( rotValue )
        
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
        
        if Window_global.ui_checkNormalOrient.isChecked():
            yVector = OpenMaya.MVector( 0,1,0 )
            return yVector.rotateTo( normalVector ).asMatrix()
        return OpenMaya.MMatrix()
    
    
    @staticmethod
    def getTargetViewSize( srcObject, intersectPoint ):
        
        bbMin = OpenMaya.MVector( *cmds.getAttr( srcObject + '.boundingBoxMin' )[0] )
        bbMax = OpenMaya.MVector( *cmds.getAttr( srcObject + '.boundingBoxMax' )[0] )
        
        bbMin += OpenMaya.MVector( intersectPoint )
        bbMax += OpenMaya.MVector( intersectPoint )
        
        pointSrc = ( bbMin + bbMax )/2
        
        activeView = OpenMayaUI.M3dView().active3dView()
        camDagPath = OpenMaya.MDagPath()
        activeView.getCamera( camDagPath )
        
        camXVector = OpenMaya.MVector( camDagPath.inclusiveMatrix()[0] )
        camXVector.normalize()
        
        pointDst = pointSrc + camXVector
        
        viewPointSrc = Functions.worldPointToViewPoint( OpenMaya.MPoint( pointSrc ) )
        viewPointDst = Functions.worldPointToViewPoint( OpenMaya.MPoint( pointDst ) )
        
        return viewPointSrc.distanceTo( viewPointDst )
    
    
    @staticmethod
    def getRandomMatrix():
        
        import random, math
        
        layoutRot,   checkRot,    rMinX, rMaxX, rMinY, rMaxY, rMinZ, rMaxZ = Window_global.ui_randomOptionRot.children()
        layoutScale, checkScale,  sMinX, sMaxX, sMinY, sMaxY, sMinZ, sMaxZ = Window_global.ui_randomOptionScale.children()
        layoutRotA,  checkRotA,   rMin, rMax    = Window_global.ui_randomOptionRotA.children()
        layoutScaleA,checkScaleA, sMin, sMax    = Window_global.ui_randomOptionScaleA.children()
        
        rotChecked   = checkRot.isChecked()
        scaleChecked = checkScale.isChecked()
        rotAChecked   = checkRotA.isChecked()
        scaleAChecked = checkScaleA.isChecked()
        
        rx = 0; ry = 0; rz = 0;
        sx = 1; sy = 1; sz = 1;
        rax = 0; ray = 0; raz = 0;
        sa = 1
        
        if rotChecked:
            rx = math.radians( random.uniform( float(rMinX.text()), float(rMaxX.text()) ) )
            ry = math.radians( random.uniform( float(rMinY.text()), float(rMaxY.text()) ) )
            rz = math.radians( random.uniform( float(rMinZ.text()), float(rMaxZ.text()) ) )
        if scaleChecked:
            sx = random.uniform( float(sMinX.text()), float(sMaxX.text()) )
            sy = random.uniform( float(sMinY.text()), float(sMaxY.text()) )
            sz = random.uniform( float(sMinZ.text()), float(sMaxZ.text()) )
        
        rUtil = OpenMaya.MScriptUtil()
        rUtil.createFromList([rx, ry, rz], 3)
        rotPtr = rUtil.asDoublePtr()
        sUtil = OpenMaya.MScriptUtil()
        sUtil.createFromList([sx, sy, sz], 3)
        scalePtr = sUtil.asDoublePtr()
        
        trMtx = OpenMaya.MTransformationMatrix()
        trMtx.setRotation( rotPtr, trMtx.kXYZ )
        trMtx.setScale( scalePtr, OpenMaya.MSpace.kTransform )
        
        if rotAChecked:
            rax = math.radians( random.uniform( float(rMin.text()), float(rMax.text()) ) )
            ray = math.radians( random.uniform( float(rMin.text()), float(rMax.text()) ) )
            raz = math.radians( random.uniform( float(rMin.text()), float(rMax.text()) ) )
        if scaleAChecked:
            sa = random.uniform( float(sMin.text()), float(sMax.text()) )
        
        rUtil = OpenMaya.MScriptUtil()
        rUtil.createFromList([rax, ray, raz], 3)
        rotPtr = rUtil.asDoublePtr()
        sUtil = OpenMaya.MScriptUtil()
        sUtil.createFromList([sa,sa,sa], 3)
        scalePtr = sUtil.asDoublePtr()
        
        trMtxA = OpenMaya.MTransformationMatrix()
        trMtxA.setRotation( rotPtr, trMtxA.kXYZ )
        trMtxA.setScale( scalePtr, OpenMaya.MSpace.kTransform )
        
        return trMtxA.asMatrix() * trMtx.asMatrix()


    @staticmethod
    def getOffsetMatrix( editMatrix, normalMatrix ):
        
        def getBoundingBoxMinMaxY( selObject ):
            bb = OpenMaya.MBoundingBox()
            bbmin = cmds.getAttr( selObject + '.boundingBoxMin' )[0]
            bbmax = cmds.getAttr( selObject + '.boundingBoxMax' )[0]
            multMatrix = Tool_global.randomMatrix * Tool_global.scaleEditMatrix
            point1 = OpenMaya.MPoint( bbmin[0], bbmin[1], bbmin[2] ) * multMatrix
            point2 = OpenMaya.MPoint( bbmax[0], bbmin[1], bbmin[2] ) * multMatrix
            point3 = OpenMaya.MPoint( bbmax[0], bbmax[1], bbmin[2] ) * multMatrix
            point4 = OpenMaya.MPoint( bbmax[0], bbmax[1], bbmax[2] ) * multMatrix
            point5 = OpenMaya.MPoint( bbmin[0], bbmax[1], bbmax[2] ) * multMatrix
            point6 = OpenMaya.MPoint( bbmin[0], bbmin[1], bbmax[2] ) * multMatrix
            bb.expand( point1 ); bb.expand( point2 ); bb.expand( point3 )
            bb.expand( point4 ); bb.expand( point5 ); bb.expand( point6 )
            return bb.min().y, bb.max().y
            
        
        srcMatrix = editMatrix * normalMatrix.inverse()
        
        oValidator, oMainLayout, oCheck, oLineEdit, oSlider = Window_global.ui_offsetByObject.children()
        gValidator, oMainLayout, gCheck, gLineEdit, gSlider = Window_global.ui_offsetByGround.children()
        
        objectOffsetCheck = oCheck.isChecked()
        groundOffsetCheck = gCheck.isChecked()
        objectOffset = float( oLineEdit.text() )
        groundOffset = float( gLineEdit.text() )
        
        if Window_global.ui_componentCheck.isChecked():
            maxY = -1000000000.0
            minY =  1000000000.0
            for i in range( Tool_global.instancePoints.length() ):
                pointEdited = Tool_global.instancePoints[i] * srcMatrix
                if pointEdited.y < minY:
                    minY = pointEdited.y
                if pointEdited.y > maxY:
                    maxY = pointEdited.y
            offsetObjectY = ( maxY - minY ) * objectOffset
        else:
            minY, maxY = getBoundingBoxMinMaxY( Functions.getSelectedObject() )
            offsetObjectY = ( maxY - minY ) * objectOffset
            
        if not objectOffsetCheck:
            offsetObjectY = 0
        if not groundOffsetCheck:
            groundOffset = 0
        
        offsetVector = OpenMaya.MVector( 0,-minY+groundOffset+offsetObjectY,0 ) * normalMatrix
        
        mtxList = [1,0,0,0, 0,1,0,0, 0,0,1,0, offsetVector.x,offsetVector.y,offsetVector.z,1]
        mtx = OpenMaya.MMatrix()
        OpenMaya.MScriptUtil.createMatrixFromList( mtxList, mtx )
        return mtx
    
    
    @staticmethod
    def getRotationEditMatrix( mouseX, mouseY ):
        
        import math
        
        if Window_global.ui_orientEditMode.currentText() == 'All':
            srcPoint = Tool_global.intersectPoint
            srcViewPoint = Functions.worldPointToViewPoint( srcPoint )
            mousePoint = OpenMaya.MPoint( mouseX, mouseY, 0 )
            
            mouseWorldPoint     = Functions.viewPointToWorldPoint( mousePoint )
            srcViewPointToWorld = Functions.viewPointToWorldPoint( srcViewPoint )
            
            directionVector = mouseWorldPoint - srcViewPointToWorld
            camVector = Functions.getCamVector()
            crossVector = directionVector ^ camVector
            
            viewPointVector = OpenMaya.MVector(mousePoint) - OpenMaya.MVector(srcViewPoint)
            rotValue = viewPointVector.length() / Tool_global.targetViewSize * 90
        
            return Functions.getRotationMatrix( crossVector, rotValue )
            
        return OpenMaya.MMatrix()
    
    
    @staticmethod
    def getRotationYEditMatrix( mouseX, mouseY ):
        
        import math
        
        if Window_global.ui_orientEditMode.currentText() == 'Only Y':
            srcPoint = Tool_global.intersectPoint
            srcViewPoint = Functions.worldPointToViewPoint( srcPoint )
            mousePoint = OpenMaya.MPoint( mouseX, mouseY, 0 )
            
            mouseWorldPoint     = Functions.viewPointToWorldPoint( mousePoint )
            srcViewPointToWorld = Functions.viewPointToWorldPoint( srcViewPoint )
            
            directionVector = mouseWorldPoint - srcViewPointToWorld
            camVector = Functions.getCamVector()
            crossVector = directionVector ^ camVector
            
            viewPointVector = OpenMaya.MVector(mousePoint) - OpenMaya.MVector(srcViewPoint)
            rotValue = viewPointVector.x / Tool_global.targetViewSize * 45
        
            trMtx = OpenMaya.MTransformationMatrix()
            euler = OpenMaya.MEulerRotation( 0.0,math.radians(rotValue),0.0 )
            quat = euler.asQuaternion()
            trMtx.setRotationQuaternion( quat.x, quat.y, quat.z, quat.w )
            return trMtx.asMatrix()
        else:
            return OpenMaya.MMatrix()
    
    
    @staticmethod
    def getScaleEditMatrix( mouseX, mouseY ):
        
        srcPoint     = Tool_global.intersectPoint
        srcViewPoint = Functions.worldPointToViewPoint( srcPoint )
        mousePoint   = OpenMaya.MPoint( mouseX, mouseY, 0 )
        
        viewPointVector     = OpenMaya.MVector(mousePoint) - OpenMaya.MVector(srcViewPoint)
        addSize = viewPointVector.y / Tool_global.targetViewSize * Tool_global.currentSize
        
        return  listToMatrix( [ addSize + 1, 0, 0, 0,
                                0, addSize + 1, 0, 0,
                                0, 0, addSize + 1, 0,
                                0, 0, 0, 1 ])
    
    
    
    
    


class PutObjectContext( OpenMayaMPx.MPxSelectionContext ):

    contextName = 'sgPutObjectOnGroundContext'
    
    def __init__( self ):
        OpenMayaMPx.MPxSelectionContext.__init__( self )


    def toolOnSetup( self, *args, **kwargs ):
        
        Window_global.getUIObjects()
        if not Window_global.windowObject:
            cmds.warning( "ui is not exists" )
            return None
        
        OpenMayaMPx.MPxSelectionContext.toolOnSetup( self, *args, **kwargs )
        Tool_global.eventFilter   = MainWindowEventFilter()
        Tool_global.mainWindowPtr = Window_global.mayaWin
        Tool_global.mainWindowPtr.installEventFilter( Tool_global.eventFilter )
        Tool_global.setDefault()


    def toolOffCleanup( self, *args, **kwargs ):
        try:
            Tool_global.currentGlWidget.removeEventFilter( Tool_global.currentEventFilter )
        except:
            pass
        Tool_global.mainWindowPtr.removeEventFilter( Tool_global.eventFilter )
        OpenMayaMPx.MPxSelectionContext.toolOffCleanup(self, *args, **kwargs )
        Functions.clearInstance()


    def className( self, *args, **kwargs):
        OpenMayaMPx.MPxSelectionContext.className(self, *args, **kwargs)
    
    
    @staticmethod
    def doMove( mouseX, mouseY ):
    
        cmds.undoInfo( swf=0 )
        
        if Tool_global.mousePressed: return None
        modifiers = QApplication.keyboardModifiers()
        
        if modifiers != QtCore.Qt.ShiftModifier:
            Tool_global.stilPressed_shift   = False
        if modifiers != QtCore.Qt.ControlModifier:
            Tool_global.stilPressed_control = False
        
        selObj  = Functions.getSelectedObject()
        instObj = Functions.getInstanceObject()
        ground = Functions.getGround()
        intersectPoint, intersectNormal = Functions.getIntersectPointAndNormal( mouseX, 
                                                                                mouseY, 
                                                                                ground )
        Tool_global.mouseX = mouseX
        Tool_global.mouseY = mouseY
        Tool_global.targetViewSize = Functions.getTargetViewSize( selObj, intersectPoint ) * Tool_global.currentSize

        transMatrixList = [1,0,0,0,
                           0,1,0,0,
                           0,0,1,0,
                           Tool_global.intersectPoint.x, Tool_global.intersectPoint.y, Tool_global.intersectPoint.z, 1]
        
        
        if not Tool_global.stilPressed_control and modifiers == QtCore.Qt.ControlModifier and modifiers != QtCore.Qt.ShiftModifier:
            Tool_global.scaleEditMatrix = Functions.getScaleEditMatrix( mouseX, mouseY )

        elif not Tool_global.stilPressed_shift and  modifiers != QtCore.Qt.ControlModifier and modifiers == QtCore.Qt.ShiftModifier:
            Tool_global.rotationYEditMatrix = Functions.getRotationYEditMatrix(mouseX, mouseY)
            Tool_global.rotationEditMatrix = Functions.getRotationEditMatrix( mouseX, mouseY )
        else:
            Tool_global.intersectPoint = intersectPoint
            Tool_global.intersectNormal = intersectNormal
        
        if not Tool_global.randomMatrixExists:
            Tool_global.randomMatrix       = Functions.getRandomMatrix()
            Tool_global.randomMatrixExists = True
        
        transMatrix = listToMatrix( transMatrixList )
        normalRotMatrix    = Functions.getRotationMatrixFromNormal( Tool_global.intersectNormal )
        editMatrix = Tool_global.rotationYEditMatrix * Tool_global.randomMatrix * normalRotMatrix*Tool_global.scaleEditMatrix*Tool_global.rotationEditMatrix
        offsetMatrix = Functions.getOffsetMatrix(editMatrix,normalRotMatrix)    
        Tool_global.cuMatrix = editMatrix * offsetMatrix * transMatrix
        mtxList = matrixToList( Tool_global.cuMatrix )
        cmds.xform( instObj, ws=1, matrix=mtxList )
        cmds.undoInfo( swf=1 )


    
    def doPress( self, event ):

        cmds.undoInfo( ock=1 )
        targetObject = Functions.getSelectedObject()
        copyObject = Functions.copyObject( targetObject )
        mtxList = matrixToList( Tool_global.cuMatrix )
        cmds.xform( copyObject, ws=1, matrix=mtxList )
        Tool_global.mousePressed = True
        cmds.undoInfo( cck=1 )
        
        Tool_global.scaleEditMatrix = OpenMaya.MMatrix()
        Tool_global.rotationEditMatrix = OpenMaya.MMatrix()
        Tool_global.rotationYEditMatrix = OpenMaya.MMatrix()
        
        Tool_global.randomMatrixExists= False



    def doDrag(self, event ):
        
        pass



    def doRelease(self, event ):
        
        import random
        
        count = Window_global.ui_listWidgetPut.count()
        Tool_global.randomIndex = int( random.uniform( 0, count ) )
        Tool_global.targetViewSize = None
        
        Tool_global.mousePressed = False
        
        modifiers = QApplication.keyboardModifiers()
        Tool_global.stilPressed_shift   = modifiers == QtCore.Qt.ShiftModifier
        Tool_global.stilPressed_control = modifiers == QtCore.Qt.ControlModifier
        
        Functions.getRandomMatrix()





class PutObjectContextCommand( OpenMayaMPx.MPxContextCommand ):
    
    commandName = "sgPutObjectOnGroundContextCommand"
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

