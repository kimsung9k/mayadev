from maya import cmds, mel, OpenMaya
import pymel.core
import copy


class sgCmds:
    
    @staticmethod
    def getVectorList():
        return [ [1,0,0], [0,1,0], [0,0,1], [-1,0,0], [0,-1,0], [0,0,-1] ]
    
    
    @staticmethod
    def listToMatrix( mtxList ):
        if type( mtxList ) == OpenMaya.MMatrix:
            return mtxList
        matrix = OpenMaya.MMatrix()
        if type( mtxList ) == list:
            resultMtxList = mtxList
        else:
            resultMtxList = []
            for i in range( 4 ):
                for j in range( 4 ):
                    resultMtxList.append( mtxList[i][j] )
        
        OpenMaya.MScriptUtil.createMatrixFromList( resultMtxList, matrix )
        return matrix
    
    
    @staticmethod
    def getMMatrix( inputAttr ):
        if type( inputAttr ) == pymel.core.general.Attribute:
            attr = pymel.core.ls( inputAttr )[0]
            return sgCmds.listToMatrix( cmds.getAttr( attr.name() ) )
        elif type( inputAttr ) == pymel.core.datatypes.Matrix:
            return sgCmds.listToMatrix( inputAttr )
        else:
            return inputAttr


    @staticmethod
    def getDagPath( inputTarget ):
        
        target = pymel.core.ls( inputTarget )[0]
        dagPath = OpenMaya.MDagPath()
        selList = OpenMaya.MSelectionList()
        selList.add( target.name() )
        try:
            selList.getDagPath( 0, dagPath )
            return dagPath
        except:
            return None
    
    
    @staticmethod
    def getNodeFromHistory( target, nodeType ):
    
        pmTarget = pymel.core.ls( target )[0]
        hists = pmTarget.history()
        targetNodes = []
        for hist in hists:
            if hist.type() == nodeType:
                targetNodes.append( hist )
        return targetNodes
    
    
    
    @staticmethod
    def getDecomposeMatrix( matrixAttr ):
    
        matrixAttr = pymel.core.ls( matrixAttr )[0]
        cons = matrixAttr.listConnections( s=0, d=1, type='decomposeMatrix' )
        if cons: 
            pymel.core.select( cons[0] )
            return cons[0]
        decomposeMatrix = pymel.core.createNode( 'decomposeMatrix' )
        matrixAttr >> decomposeMatrix.imat
        return decomposeMatrix
    


    @staticmethod
    def getMultMatrix( *matrixAttrList ):
    
        mm = pymel.core.createNode( 'multMatrix' )
        for i in range( len( matrixAttrList ) ):
            pymel.core.connectAttr( matrixAttrList[i], mm.i[i] )
        return mm
    


    @staticmethod
    def getClosestParamAtPoint( inputTargetObj, inputCurve ):
    
        targetObj = pymel.core.ls( inputTargetObj )[0]
        curve = pymel.core.ls( inputCurve )[0]
        
        if curve.nodeType() == 'transform':
            crvShape = curve.getShape()
        else:
            crvShape = curve
        
        dagPathTarget = sgCmds.getDagPath( targetObj )
        mtxTarget = dagPathTarget.inclusiveMatrix()
        dagPathCurve  = sgCmds.getDagPath( crvShape )
        mtxCurve  = dagPathCurve.inclusiveMatrix()
        
        pointTarget = OpenMaya.MPoint( mtxTarget[3] )
        pointTarget *= mtxCurve.inverse()
        
        fnCurve = OpenMaya.MFnNurbsCurve( sgCmds.getDagPath( crvShape ) )
        
        util = OpenMaya.MScriptUtil()
        util.createFromDouble( 0.0 )
        ptrDouble = util.asDoublePtr()
        fnCurve.closestPoint( pointTarget, 0, ptrDouble )
        
        paramValue = OpenMaya.MScriptUtil().getDouble( ptrDouble )
        return paramValue
    
    
    @staticmethod
    def getLookAtChildMatrixAttr( lookTargetMatrix, baseMatrix, baseVector ):

        baseInverse = pymel.core.createNode( 'inverseMatrix' )
        baseMatrix >> baseInverse.inputMatrix
        dcmp = sgCmds.getDecomposeMatrix( sgCmds.getMultMatrix( lookTargetMatrix, baseInverse.outputMatrix ).matrixSum )
        angleNode = pymel.core.createNode( 'angleBetween' )
    
        lookTargetMVector = OpenMaya.MVector( *dcmp.ot.get() )
        baseMVector       = OpenMaya.MVector( *baseVector )
    
        if lookTargetMVector * baseMVector < 0:
            baseVector = [ -value for value in baseVector ]
    
        angleNode.vector1.set( baseVector )
        dcmp.ot >> angleNode.vector2
    
        compose = pymel.core.createNode( 'composeMatrix' )
        angleNode.euler >> compose.ir
    
        mm = pymel.core.createNode( 'multMatrix' )
        compose.outputMatrix >> mm.i[0]
        baseMatrix >> mm.i[1]
    
        return mm.matrixSum
    
    
    @staticmethod
    def createBlendTwoMatrixNode( inputFirstAttr, inputSecondAttr ):
    
        firstAttr  = pymel.core.ls( inputFirstAttr )[0]
        secondAttr = pymel.core.ls( inputSecondAttr )[0]
        
        wtAddMtx = pymel.core.createNode( 'wtAddMatrix' )
        wtAddMtx.addAttr( 'blend', min=0, max=1, dv=0.5, k=1 )
        
        revNode  = pymel.core.createNode( 'reverse' )
    
        firstAttr >> wtAddMtx.i[0].m
        secondAttr >> wtAddMtx.i[1].m
        
        wtAddMtx.blend >> revNode.inputX
        revNode.outputX >> wtAddMtx.i[0].w
        wtAddMtx.blend >> wtAddMtx.i[1].w
        
        return wtAddMtx
    
    
    
    @staticmethod
    def getDirectionIndex( inputVector ):
    
        import math
        
        if type( inputVector ) in [ list, tuple ]:
            normalInput = OpenMaya.MVector(*inputVector).normal()
        else:
            normalInput = OpenMaya.MVector(inputVector).normal()
        
        xVector = OpenMaya.MVector( 1,0,0 )
        yVector = OpenMaya.MVector( 0,1,0 )
        zVector = OpenMaya.MVector( 0,0,1 )
        
        xdot = xVector * normalInput
        ydot = yVector * normalInput
        zdot = zVector * normalInput
        
        xabs = math.fabs( xdot )
        yabs = math.fabs( ydot )
        zabs = math.fabs( zdot )
        
        dotList = [xdot, ydot, zdot]
        
        dotIndex = 0
        if xabs < yabs:
            dotIndex = 1
            if yabs < zabs:
                dotIndex = 2
        elif xabs < zabs:
            dotIndex = 2
            
        if dotList[ dotIndex ] < 0:
            dotIndex += 3
        
        return dotIndex
    
    
    
    @staticmethod
    def getTangetAtParam( inputCurveObj, paramValue ):
    
        curveObj = pymel.core.ls( inputCurveObj )[0]
        if curveObj.nodeType() == 'nurbsCurve':
            curveShape = curveObj
        else:
            curveShape = curveObj.getShape()
        
        fnCurve = OpenMaya.MFnNurbsCurve( sgCmds.getDagPath( curveShape ) )
        tangent = fnCurve.tangent( paramValue, OpenMaya.MSpace.kWorld )
        return tangent
    
    
    @staticmethod
    def getAimDirection( inputCurve, inputUpObjects ):
        
        curve = pymel.core.ls( inputCurve )[0]
        upObjects = [ pymel.core.ls( inputUpObject )[0] for inputUpObject in inputUpObjects ]
        
        curveMtx = sgCmds.getMMatrix( curve.wm.get() )
        
        vectorList = sgCmds.getVectorList()
        dotValueList = [ 0 for i in range( len( vectorList ) ) ]
        
        for i in range( len( vectorList ) ):
            vector = OpenMaya.MVector( *vectorList[i] )
            for upObject in upObjects:
                upObjectMtx = sgCmds.getMMatrix( upObject.wm.get() )
                param = sgCmds.getClosestParamAtPoint( upObject, curve )
                tangent = sgCmds.getTangetAtParam( curve, param )

                worldUpVector = vector * upObjectMtx
                worldTangent  = tangent * curveMtx
                dotValueList[i] += worldUpVector * worldTangent
        
        maxIndex = dotValueList.index( max(dotValueList) )
        maxIndexVector = vectorList[ maxIndex ]
        
        return maxIndexVector
        

    
    
    @staticmethod
    def tangentConstraintByGroup( inputCurve, inputTargets, inputUpObjects, aimDirection ):
    
        curve = pymel.core.ls( inputCurve )[0]
        targets = [ pymel.core.ls( inputTarget )[0] for inputTarget in inputTargets ]
        upObjects = [ pymel.core.ls( inputUpObject )[0] for inputUpObject in inputUpObjects ]
        
        def getWorldTangentAttr( tangentAttr ):
            srcCons = tangentAttr.node().inputCurve.listConnections( s=1, d=0, p=1 )
            if not srcCons: return None
            
            spaceType = 'world'
            if srcCons[0].longName() == 'local':
                spaceType = 'local'
            elif srcCons[0].longName() == 'world':
                spaceType = 'world'
            
            if spaceType == 'local':
                vectorNode = pymel.core.createNode( 'vectorProduct' )
                vectorNode.op.set( 3 )
                pointOnCurveInfoNode.tangent >> vectorNode.input1
                srcCons[0].node().wm >> vectorNode.matrix
                return vectorNode.output
            else:
                return pointOnCurveInfoNode.tangent
        
        
        def getPointOnCurveInfo( curve, target ):
            
            curveShape = curve.getShape()
            
            pointOnCurveInfos = sgCmds.getNodeFromHistory( target, 'pointOnCurveInfo' )
            
            if pointOnCurveInfos:
                for pointOnCurveInfo in pointOnCurveInfos:
                    cons = pointOnCurveInfo.listConnections( s=1, d=0, shapes=1 )
                    if curve.getShape() in cons:
                        return pointOnCurveInfo 
    
            compose =  pymel.core.createNode( 'composeMatrix' )
            mm = pymel.core.createNode( 'multMatrix' )
            dcmp = pymel.core.createNode( 'decomposeMatrix' )
            mm.o >> dcmp.imat
            target.t >> compose.it
            compose.outputMatrix >> mm.i[0]
            target.pm >> mm.i[1]
            curveShape.pim >> mm.i[2]
            pointOnCurveInfo = pymel.core.createNode( 'pointOnCurveInfo' )
            nearCurve = pymel.core.createNode( 'nearestPointOnCurve' )
            curveShape.local >> pointOnCurveInfo.inputCurve
            curveShape.local >> nearCurve.inputCurve
            dcmp.ot >> nearCurve.inPosition
            nearCurve.parameter >> pointOnCurveInfo.parameter        
            return pointOnCurveInfo

        
        def twoUpObjectAndParam( target, upObjects ):
            
            if len( upObjects ) == 1:
                firstUpObject  = upObjects[0]
                secondUpObject = upObjects[0]
            else:
                firstUpObject  = upObjects[0]
                secondUpObject = upObjects[1]
            
            targetParam = sgCmds.getClosestParamAtPoint( target, curve )
            
            betweenParam = 1
            for i in range( len( upObjects )-1 ):
                firstUpObject = upObjects[i]
                secondUpObject = upObjects[i+1]
                
                firstUpParam = sgCmds.getClosestParamAtPoint( firstUpObject, curve )
                secondUpParam = sgCmds.getClosestParamAtPoint( secondUpObject, curve )
                
                multParamDirection = 1
                if firstUpParam > secondUpParam:
                    multParamDirection = -1
                
                if multParamDirection * ( targetParam - firstUpParam ) < 0:
                    betweenParam = 0
                    break
                elif multParamDirection * ( targetParam - secondUpParam ) < 0:
                    betweenParam = ( targetParam - firstUpParam ) / ( secondUpParam - firstUpParam )
                    break
                else:
                    continue
                    
            return firstUpObject, secondUpObject, betweenParam
        
        
        def getLocalTangentAngleNodeFromBlendMtxNode( curve, blendMtx ):
            
            aimVectorNode = pymel.core.createNode( 'vectorProduct' )
            aimVectorNode.op.set( 3 )
            worldTangentAttr = getWorldTangentAttr( pointOnCurveInfoNode.tangent )
            multDirectionTangentNode = pymel.core.createNode( 'multiplyDivide' )
            
            worldTangentAttr >> multDirectionTangentNode.input1
            multDirectionTangentNode.input2.set( 1, 1, 1 )
            multDirectionTangentNode.output >> aimVectorNode.input1
            invMtxNode.outputMatrix >> aimVectorNode.matrix
            
            angleNode = pymel.core.createNode( 'angleBetween' )
            angleNode.vector1.set( aimDirection )
            aimVectorNode.output >> angleNode.vector2
            return angleNode
            
            
        
        for target in targets:
            pointOnCurveInfoNode = getPointOnCurveInfo( curve, target )
            
            firstUpObject, secondUpObject, betweenParam = twoUpObjectAndParam( target, upObjects )
            
            firstAimVector  = copy.copy( aimDirection )
            secondAimVector = copy.copy( aimDirection )
            
            firstUpMatrixAttr  = sgCmds.getLookAtChildMatrixAttr( secondUpObject.wm, firstUpObject.wm, firstAimVector )
            secondUpMatrixAttr = sgCmds.getLookAtChildMatrixAttr( firstUpObject.wm, secondUpObject.wm, secondAimVector )
            
            blendMtxNode = sgCmds.createBlendTwoMatrixNode( firstUpMatrixAttr, secondUpMatrixAttr )
            blendMtxNode.blend.set( betweenParam )
            
            invMtxNode = pymel.core.createNode( 'inverseMatrix' )
            blendMtxNode.matrixSum >> invMtxNode.inputMatrix
            baseAimVector = blendMtxNode.matrixSum.get()[ sgCmds.getDirectionIndex( aimDirection ) % 3 ]
            
            angleNode = getLocalTangentAngleNodeFromBlendMtxNode( curve, blendMtxNode )
            
            composeRot = pymel.core.createNode( 'composeMatrix' )
            angleNode.euler >> composeRot.ir
            
            mmResult = pymel.core.createNode( 'multMatrix' )
            composeRot.outputMatrix >> mmResult.i[0]
            blendMtxNode.matrixSum >> mmResult.i[1]
            target.pim >> mmResult.i[2]
            
            dcmp = sgCmds.getDecomposeMatrix( mmResult.o )
            dcmp.outputRotate >> target.r




import maya.OpenMayaUI
from __qtImprot import *
import os, sys
import json
from functools import partial



class Widget_curvePart( QWidget ):

    def __init__(self, *args, **kwargs ):
        QWidget.__init__( self, *args, **kwargs )
        
        mainLayout = QHBoxLayout( self )
        mainLayout.setContentsMargins(0,0,0,0)
        label = QLabel( "Target Curve : " )
        lineEdit = QLineEdit()
        loadButton = QPushButton( "Load Curve" )
        
        mainLayout.addWidget( label )
        mainLayout.addWidget( lineEdit )
        mainLayout.addWidget( loadButton )
        
        self.label = label
        self.lineEdit = lineEdit
        self.button = loadButton
        QtCore.QObject.connect( loadButton, QtCore.SIGNAL( 'clicked()' ), self.loadCurve )


    def loadCurve(self):
        
        sels = pymel.core.ls( sl=1 )
        targetCurve = None
        for sel in sels:
            if not sel.getShape(): continue
            if sel.getShape().nodeType() != 'nurbsCurve': continue
            targetCurve = sel
            break
        self.lineEdit.setText( targetCurve.name() )




class Widget_upObjectsPart( QWidget ):

    def __init__(self, *args, **kwargs ):

        QWidget.__init__( self, *args, **kwargs )
        
        mainLayout = QVBoxLayout( self )
        mainLayout.setContentsMargins(0,0,0,0)
        listWidget = QListWidget()
        loadButton = QPushButton( "Load Up Objects" )
        mainLayout.addWidget( listWidget )
        mainLayout.addWidget( loadButton )
        
        self.listWidget = listWidget
        self.loadButton = loadButton
        QtCore.QObject.connect( self.loadButton, QtCore.SIGNAL( 'clicked()' ), self.loadUpObjects )


    def loadUpObjects(self):
        
        sels = pymel.core.ls( sl=1 )
        targetUpObjects = []
        for sel in sels:
            if not pymel.core.attributeQuery( 'wm', node=sel, ex=1 ): continue
            targetUpObjects.append( sel )
        
        self.listWidget.clear()
        self.listWidget.upObjects = targetUpObjects
        for targetUpObject in targetUpObjects:
            self.listWidget.addItem( targetUpObject.name() )




class Widget_targetsPart( QWidget ):

    def __init__(self, *args, **kwargs ):
        QWidget.__init__( self, *args, **kwargs )

        mainLayout = QVBoxLayout( self )
        mainLayout.setContentsMargins(0,0,0,0)
        listWidget = QListWidget()
        loadButton = QPushButton( "Load Constrain Targets" )
        mainLayout.addWidget( listWidget )
        mainLayout.addWidget( loadButton )
        
        self.listWidget = listWidget
        self.loadButton = loadButton
        QtCore.QObject.connect( self.loadButton, QtCore.SIGNAL( 'clicked()' ), self.loadConstrainTargets )
    
    
    def loadConstrainTargets(self):
        
        sels = pymel.core.ls( sl=1 )
        constrainTargets = []
        for sel in sels:
            if not pymel.core.attributeQuery( 'wm', node=sel, ex=1 ): continue
            constrainTargets.append( sel )
        
        self.listWidget.clear()
        self.listWidget.constrainTargets = constrainTargets
        for target in constrainTargets:
            self.listWidget.addItem( target.name() )




class Widget_horizontalSeparator( QFrame ):
    
    def __init__(self, *args, **kwargs ):
        
        QFrame.__init__( self, *args, **kwargs )
        self.setFrameShape( QFrame.HLine );
        self.setFrameShadow( QFrame.Sunken );




class Widget_verticalSeparator( QFrame ):
    
    def __init__(self, *args, **kwargs ):
        
        QFrame.__init__( self, *args, **kwargs )
        self.setFrameShape( QFrame.VLine );
        self.setFrameShadow( QFrame.Sunken );





class Widget_aimDirectionPart( QWidget ):

    def __init__(self, *args, **kwargs ):
        QWidget.__init__( self, *args, **kwargs )
        
        mainLayout = QHBoxLayout( self )
        mainLayout.setContentsMargins(0,0,0,0)
        label = QLabel( "Aim Direction  : " )
        lineEdit1 = QLineEdit()
        lineEdit2 = QLineEdit()
        lineEdit3 = QLineEdit()
        verticalSeparator = Widget_verticalSeparator()
        checkBox = QCheckBox( "Set Auto" )
        mainLayout.addWidget( label )
        mainLayout.addWidget( lineEdit1 )
        mainLayout.addWidget( lineEdit2 )
        mainLayout.addWidget( lineEdit3 )
        mainLayout.addWidget( verticalSeparator )
        mainLayout.addWidget( checkBox )
        
        validator = QDoubleValidator( -10000.0, 10000.0, 2 )
        lineEdit1.setValidator( validator )
        lineEdit2.setValidator( validator )
        lineEdit3.setValidator( validator )
        lineEdit1.setText( "0.0" )
        lineEdit2.setText( "1.0" )
        lineEdit3.setText( "0.0" )
        checkBox.setChecked( True )
        self.label = label; self.lineEdit1 = lineEdit1; 
        self.lineEdit2 = lineEdit2; self.lineEdit3 = lineEdit3; self.checkBox = checkBox
        self.setVectorEnabled()
        
        
        QtCore.QObject.connect( checkBox, QtCore.SIGNAL( 'clicked()' ), self.setVectorEnabled )


    def setVectorEnabled(self):

        checkBoxValue = not self.checkBox.isChecked()
        self.label.setEnabled( checkBoxValue )
        self.lineEdit1.setEnabled( checkBoxValue )
        self.lineEdit2.setEnabled( checkBoxValue )
        self.lineEdit3.setEnabled( checkBoxValue )



class Window( QDialog ):
    
    mayaWin = shiboken.wrapInstance( long( maya.OpenMayaUI.MQtUtil.mainWindow() ), QWidget )
    objectName = "sgWidget_tangentConstraintByGroup"
    title = "Tangent Constraint by Group"
    defaultWidth = 400
    defaultHeight = 400


    def __init__(self, *args, **kwargs ):
        
        QDialog.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setWindowTitle( Window.title )
        
        w_curvePart = Widget_curvePart()
        separator1 = Widget_horizontalSeparator()
        w_upObjectsPart = Widget_upObjectsPart()
        w_targetsPart = Widget_targetsPart()
        separator2 = Widget_horizontalSeparator()
        w_aimDirectionPart = Widget_aimDirectionPart()
        separator3 = Widget_horizontalSeparator()
        w_button = QPushButton( "Constraint" )
        
        listLayoutWidget = QWidget()
        listLayout = QHBoxLayout( listLayoutWidget )
        listLayout.setContentsMargins(0,0,0,0)
        listLayout.addWidget( w_upObjectsPart )
        listLayout.addWidget( w_targetsPart )
        
        mainLayout = QVBoxLayout( self )
        mainLayout.addWidget( w_curvePart )
        mainLayout.addWidget( separator1 )
        mainLayout.addWidget( w_aimDirectionPart )
        mainLayout.addWidget( separator2 )
        mainLayout.addWidget( listLayoutWidget )
        mainLayout.addWidget( separator3 )
        mainLayout.addWidget( w_button )
        
        self.lineEdit_curve = w_curvePart.lineEdit
        self.listWidget_upObjects = w_upObjectsPart.listWidget
        self.listWidget_constrainTargets = w_targetsPart.listWidget
        self.x_lineEdit = w_aimDirectionPart.lineEdit1
        self.y_lineEdit = w_aimDirectionPart.lineEdit2
        self.z_lineEdit = w_aimDirectionPart.lineEdit3
        self.checkBox_autoUpVector = w_aimDirectionPart.checkBox
        
        QtCore.QObject.connect( w_button, QtCore.SIGNAL( 'clicked()' ), self.constraint )
    
    
    def constraint(self):
        
        curveName = self.lineEdit_curve.text()
        upObjects = self.listWidget_upObjects.upObjects
        targets   = self.listWidget_constrainTargets.constrainTargets
        
        aimDirection = []
        if self.checkBox_autoUpVector.isChecked():
            aimDirection = sgCmds.getAimDirection( curveName, targets )
        else:
            aimDirection = [ float(self.x_lineEdit.text()), float( self.y_lineEdit.text()), float( self.z_lineEdit.text() ) ]
        
        sgCmds.tangentConstraintByGroup( curveName, targets, upObjects, aimDirection )
        
        
        



def show( evt=0 ):
    
    if cmds.window( Window.objectName, ex=1 ):
        cmds.deleteUI( Window.objectName )
    
    mainUI = Window(Window.mayaWin)
    mainUI.setObjectName( Window.objectName )
    mainUI.resize( Window.defaultWidth, Window.defaultHeight )
    mainUI.show()



