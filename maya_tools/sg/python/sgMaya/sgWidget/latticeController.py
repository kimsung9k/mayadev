#coding=utf8

from maya import cmds, OpenMaya
import maya.OpenMayaUI
import pymel.core, math, copy



if int( cmds.about( v=1 ) ) < 2017:
    from PySide import QtGui, QtCore
    import shiboken
    from PySide.QtGui import QListWidgetItem, QDialog, QListWidget, QMainWindow, QWidget, QColor, QLabel,\
    QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QAbstractItemView, QMenu,QCursor, QMessageBox, QBrush, QSplitter,\
    QScrollArea, QSizePolicy, QTextEdit, QApplication, QFileDialog, QCheckBox, QDoubleValidator, QSlider, QIntValidator,\
    QImage, QPixmap, QTransform, QPaintEvent, QTabWidget, QFrame, QTreeWidgetItem, QTreeWidget, QComboBox, QGroupBox, QAction,\
    QFont, QGridLayout
else:
    from PySide2 import QtGui, QtCore, QtWidgets
    import shiboken2 as shiboken
    from PySide2.QtWidgets import QListWidgetItem, QDialog, QListWidget, QMainWindow, QWidget, QVBoxLayout, QLabel,\
    QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QAbstractItemView, QMenu, QMessageBox, QSplitter,\
    QScrollArea, QSizePolicy, QTextEdit, QApplication, QFileDialog, QCheckBox, QSlider,\
    QTabWidget, QFrame, QTreeWidgetItem, QTreeWidget, QComboBox, QGroupBox, QAction, QGridLayout
    
    from PySide2.QtGui import QColor, QCursor, QBrush, QDoubleValidator, QIntValidator, QImage, QPixmap, QTransform,\
    QPaintEvent, QFont




class sgModel:
    
    class Controller:
        
        cubePoints = [[0.50000,0.50000,0.50000],
            [0.50000,-0.50000,0.50000],
            [-0.50000,-0.50000,0.50000],
            [-0.50000,0.50000,0.50000],
            [0.50000,0.50000,0.50000],
            [0.50000,0.50000,-0.50000],
            [-0.50000,0.50000,-0.50000],
            [-0.50000,0.50000,0.50000],
            [-0.50000,-0.50000,0.50000],
            [-0.50000,-0.50000,-0.50000],
            [-0.50000,0.50000,-0.50000],
            [0.50000,0.50000,-0.50000],
            [0.50000,-0.50000,-0.50000],
            [-0.50000,-0.50000,-0.50000],
            [-0.50000,-0.50000,0.50000],
            [0.50000,-0.50000,0.50000],
            [0.50000,-0.50000,-0.50000]]
    
        circlePoints = [[0.00000,0.00000,-1.00000],
                [-0.17365,0.00000,-0.98481],
                [-0.34202,0.00000,-0.93969],
                [-0.50000,0.00000,-0.86603],
                [-0.64279,0.00000,-0.76604],
                [-0.76604,0.00000,-0.64279],
                [-0.86603,0.00000,-0.50000],
                [-0.93969,0.00000,-0.34202],
                [-0.98481,0.00000,-0.17365],
                [-1.00000,0.00000,-0.00000],
                [-0.98481,-0.00000,0.17365],
                [-0.93969,-0.00000,0.34202],
                [-0.86603,-0.00000,0.50000],
                [-0.76604,-0.00000,0.64279],
                [-0.64279,-0.00000,0.76604],
                [-0.50000,-0.00000,0.86603],
                [-0.34202,-0.00000,0.93969],
                [-0.17365,-0.00000,0.98481],
                [-0.00000,-0.00000,1.00000],
                [0.17365,-0.00000,0.98481],
                [0.34202,-0.00000,0.93969],
                [0.50000,-0.00000,0.86603],
                [0.64279,-0.00000,0.76604],
                [0.76604,-0.00000,0.64279],
                [0.86603,-0.00000,0.50000],
                [0.93969,-0.00000,0.34202],
                [0.98481,-0.00000,0.17365],
                [1.00000,-0.00000,0.00000],
                [0.98481,0.00000,-0.17365],
                [0.93969,0.00000,-0.34202],
                [0.86603,0.00000,-0.50000],
                [0.76604,0.00000,-0.64279],
                [0.64279,0.00000,-0.76604],
                [0.50000,0.00000,-0.86603],
                [0.34202,0.00000,-0.93969],
                [0.17365,0.00000,-0.98481],
                [0.00000,0.00000,-1.00000]]
        
        planePoints = [[-1.00000,0.00000,-1.00000],
                [-1.00000,0.00000,1.00000],
                [1.00000,0.00000,1.00000],
                [1.00000,0.00000,-1.00000],
                [-1.00000,0.00000,-1.00000]]
        
        movePoints = [[-0.19902,0.00000,-0.99508],
                [-0.19902,0.00000,-1.19409],
                [-0.39803,0.00000,-1.19409],
                [0.00000,0.00000,-1.59212],
                [0.39803,0.00000,-1.19409],
                [0.19902,0.00000,-1.19409],
                [0.19902,0.00000,-0.99508],
                [0.43175,0.00000,-0.89653],
                [0.62042,0.00000,-0.77798],
                [0.77798,0.00000,-0.62042],
                [0.89653,0.00000,-0.43175],
                [0.99508,0.00000,-0.19902],
                [1.19409,0.00000,-0.19902],
                [1.19409,0.00000,-0.39803],
                [1.59212,0.00000,0.00000],
                [1.19409,0.00000,0.39803],
                [1.19409,0.00000,0.19902],
                [0.99508,0.00000,0.19902],
                [0.89653,0.00000,0.43175],
                [0.77798,0.00000,0.62042],
                [0.62042,0.00000,0.77798],
                [0.43175,0.00000,0.89653],
                [0.19902,0.00000,0.99508],
                [0.19902,0.00000,1.19409],
                [0.39803,0.00000,1.19409],
                [0.00000,0.00000,1.59212],
                [-0.39803,0.00000,1.19409],
                [-0.19902,0.00000,1.19409],
                [-0.19902,0.00000,0.99508],
                [-0.43175,0.00000,0.89653],
                [-0.62042,0.00000,0.77798],
                [-0.77798,0.00000,0.62042],
                [-0.89653,0.00000,0.43175],
                [-0.99508,0.00000,0.19902],
                [-1.19409,0.00000,0.19902],
                [-1.19409,0.00000,0.39803],
                [-1.59212,0.00000,0.00000],
                [-1.19409,0.00000,-0.39803],
                [-1.19409,0.00000,-0.19902],
                [-0.99508,0.00000,-0.19902],
                [-0.89653,0.00000,-0.43175],
                [-0.77798,0.00000,-0.62042],
                [-0.62042,0.00000,-0.77798],
                [-0.43175,0.00000,-0.89653],
                [-0.19902,0.00000,-0.99508]]



class sgCmds:
    
    
    @staticmethod
    def getMObject( inputTarget ):
        target = pymel.core.ls( inputTarget )[0]
        mObject = OpenMaya.MObject()
        selList = OpenMaya.MSelectionList()
        selList.add( target.name() )
        selList.getDependNode( 0, mObject )
        return mObject
    
    
    @staticmethod
    def getDefaultMatrix():
        return [1,0,0,0, 0,1,0,0, 0,0,1,0 ,0,0,0,1]

    
    @staticmethod
    def makeParent( inputSel, **options ):
        sel = pymel.core.ls( inputSel )[0]
        if not options.has_key( 'n' ) and not options.has_key( 'name' ):
            options.update( {'n':'P'+ sel.nodeName()} )
        selP = sel.getParent()
        transform = pymel.core.createNode( 'transform', **options )
        if selP: pymel.core.parent( transform, selP )
        pymel.core.xform( transform, ws=1, matrix= sel.wm.get() )
        pymel.core.parent( sel, transform )
        pymel.core.xform( sel, os=1, matrix= sgCmds.getDefaultMatrix() )
        return transform
    
    
    @staticmethod
    def getIndexColor( inputDagNode ):
    
        dagNode = pymel.core.ls( inputDagNode )[0]
        return dagNode.overrideColor.get()
    
    
    @staticmethod
    def setIndexColor( inputDagNode, index ):
        
        dagNode = pymel.core.ls( inputDagNode )[0]
        dagNode.overrideEnabled.set( 1 )
        dagNode.overrideColor.set( index )
    
    
    @staticmethod
    def copyShapeToTransform( inputShape, inputTransform ):
    
        shape = pymel.core.ls( inputShape )[0]
        transform = pymel.core.ls( inputTransform )[0]
        
        tempTr = pymel.core.createNode( 'transform' )
        oTarget = sgCmds.getMObject( tempTr )
        
        if shape.type() == 'mesh':
            oMesh = sgCmds.getMObject( shape )
            fnMesh = OpenMaya.MFnMesh( oMesh )
            fnMesh.copy( oMesh, oTarget )
        elif shape.type() == 'nurbsCurve':
            oCurve = sgCmds.getMObject( shape )
            fnCurve = OpenMaya.MFnNurbsCurve( oCurve )
            fnCurve.copy( oCurve, oTarget )
        elif shape.type() == 'nurbsSurface':
            oSurface = sgCmds.getMObject( shape )
            fnSurface = OpenMaya.MFnNurbsSurface( oSurface )
            fnSurface.copy( oSurface, oTarget )
        
        if tempTr.getShape():
            sgCmds.setIndexColor( tempTr.getShape(), sgCmds.getIndexColor( shape ) )
            pymel.core.parent( tempTr.getShape(), transform, shape=1, add=1 )
        pymel.core.delete( tempTr )
    
    
    
    @staticmethod
    def addIOShape( inputShape ):
    
        shape = pymel.core.ls( inputShape )[0]
        
        if shape.type() == 'transform':
            targetShape = shape.getShape()
        else:
            targetShape = shape
        
        targetTr    = targetShape.getParent()
        newShapeTr = pymel.core.createNode( 'transform' )
        sgCmds.copyShapeToTransform( targetShape, newShapeTr )
        ioShape = newShapeTr.getShape()
        ioShape.attr( 'io' ).set( 1 )
        pymel.core.parent( ioShape, targetTr, add=1, shape=1 )
        pymel.core.delete( newShapeTr )
        ioShape = targetTr.listRelatives( s=1 )[-1]
        return ioShape

    
    @staticmethod
    def makeController( pointList, defaultScaleMult = 1, **options ):
    
        newPointList = copy.deepcopy( pointList )
        
        options.update( {'p':newPointList, 'd':1} )
        
        typ = 'transform'
        if options.has_key( 'typ' ):
            typ = options.pop( 'typ' )
        
        mp = False
        if options.has_key( 'makeParent' ):
            mp = options.pop('makeParent')
        
        colorIndex = -1
        if options.has_key( 'colorIndex' ):
            colorIndex = options.pop('colorIndex')
        
        crv = pymel.core.curve( **options )
        crvShape = crv.getShape()
        
        if options.has_key( 'n' ):
            name = options['n']
        elif options.has_key( 'name' ):
            name = options['name']
        else:
            name = None
        
        jnt = pymel.core.ls( cmds.createNode( typ ) )[0]
        pJnt = None
        
        if mp:
            pJnt = pymel.core.ls( sgCmds.makeParent( jnt ) )[0]
        
        if name:
            jnt.rename( name )
            if pJnt:
                pJnt.rename( 'P' + name )
    
        pymel.core.parent( crvShape, jnt, add=1, shape=1 )
        pymel.core.delete( crv )
        crvShape = jnt.getShape()
        
        ioShape = sgCmds.addIOShape( jnt )
        ioShape = pymel.core.ls( ioShape )[0]
        
        crvShape.addAttr( 'shape_tx', dv=0 ); jnt.shape_tx.set( e=1, cb=1 )
        crvShape.addAttr( 'shape_ty', dv=0); jnt.shape_ty.set( e=1, cb=1 )
        crvShape.addAttr( 'shape_tz', dv=0); jnt.shape_tz.set( e=1, cb=1 )
        crvShape.addAttr( 'shape_rx', dv=0, at='doubleAngle' ); jnt.shape_rx.set( e=1, cb=1 )
        crvShape.addAttr( 'shape_ry', dv=0, at='doubleAngle' ); jnt.shape_ry.set( e=1, cb=1 )
        crvShape.addAttr( 'shape_rz', dv=0, at='doubleAngle' ); jnt.shape_rz.set( e=1, cb=1 )
        crvShape.addAttr( 'shape_sx', dv=1 ); jnt.shape_sx.set( e=1, cb=1 )
        crvShape.addAttr( 'shape_sy', dv=1 ); jnt.shape_sy.set( e=1, cb=1 )
        crvShape.addAttr( 'shape_sz', dv=1 ); jnt.shape_sz.set( e=1, cb=1 )
        crvShape.addAttr( 'scaleMult', dv=defaultScaleMult, min=0 ); jnt.scaleMult.set( e=1, cb=1 )
        composeMatrix = pymel.core.createNode( 'composeMatrix' )
        composeMatrix2 = pymel.core.createNode( 'composeMatrix' )
        multMatrix = pymel.core.createNode( 'multMatrix' )
        composeMatrix.outputMatrix >> multMatrix.i[0]
        composeMatrix2.outputMatrix >> multMatrix.i[1]
        crvShape.shape_tx >> composeMatrix.inputTranslateX
        crvShape.shape_ty >> composeMatrix.inputTranslateY
        crvShape.shape_tz >> composeMatrix.inputTranslateZ
        crvShape.shape_rx >> composeMatrix.inputRotateX
        crvShape.shape_ry >> composeMatrix.inputRotateY
        crvShape.shape_rz >> composeMatrix.inputRotateZ
        crvShape.shape_sx >> composeMatrix.inputScaleX
        crvShape.shape_sy >> composeMatrix.inputScaleY
        crvShape.shape_sz >> composeMatrix.inputScaleZ
        crvShape.scaleMult >> composeMatrix2.inputScaleX
        crvShape.scaleMult >> composeMatrix2.inputScaleY
        crvShape.scaleMult >> composeMatrix2.inputScaleZ
        trGeo = pymel.core.createNode( 'transformGeometry' )
        try:jnt.attr( 'radius' ).set( 0 )
        except:pass
        
        ioShape.local >> trGeo.inputGeometry
        multMatrix.matrixSum >> trGeo.transform
        
        trGeo.outputGeometry >> crvShape.create
        
        if colorIndex != -1:
            shape = jnt.getShape().name()
            cmds.setAttr( shape + '.overrideEnabled', 1 )
            cmds.setAttr( shape + '.overrideColor', colorIndex )
    
        return jnt

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
    def getConstrainMatrix( inputFirst, inputTarget ):
        first = pymel.core.ls( inputFirst )[0]
        target = pymel.core.ls( inputTarget )[0]
        mm = pymel.core.createNode( 'multMatrix' )
        first.wm >> mm.i[0]
        target.pim >> mm.i[1]
        return mm
    
    
    
    @staticmethod
    def constrain_all( first, target ):
    
        mm = sgCmds.getConstrainMatrix( first, target )
        dcmp = sgCmds.getDecomposeMatrix( mm.matrixSum )
        cmds.connectAttr( dcmp + '.ot',  target + '.t', f=1 )
        cmds.connectAttr( dcmp + '.or',  target + '.r', f=1 )
        cmds.connectAttr( dcmp + '.os',  target + '.s', f=1 )
        cmds.connectAttr( dcmp + '.osh',  target + '.sh', f=1 )
    
    
    @staticmethod
    def matrixToList( matrix ):
        if type( matrix ) == list:
            return matrix
        
        mtxList = range( 16 )
        for i in range( 4 ):
            for j in range( 4 ):
                mtxList[ i * 4 + j ] = matrix( i, j )
        return mtxList
    
    
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
    def getTranslateFromMatrix( mtxValue ):
        return sgCmds.matrixToList( sgCmds.getMMatrix( mtxValue ) )[12:-1]
    
    
    @staticmethod
    def setTransformDefault( inputTarget ):
        target = pymel.core.ls( inputTarget )[0]
        attrs = ['tx','ty','tz','rx','ry','rz','sx','sy','sz']
        values = [0,0,0,0,0,0,1,1,1]
        for i in range( len( attrs ) ):
            try:cmds.setAttr( target + '.' + attrs[i], values[i] )
            except:pass

    
    @staticmethod
    def constrain_scale( first, target ):
        mm = sgCmds.getConstrainMatrix( first, target )
        dcmp = sgCmds.getDecomposeMatrix( mm.matrixSum )
        cmds.connectAttr( dcmp + '.os', target + '.s', f=1 )
    
    
    @staticmethod
    def getLocalMatrix( matrixAttr, inverseMatrixAttr ):
    
        matrixAttr = pymel.core.ls( matrixAttr )[0]
        inverseMatrixAttr = pymel.core.ls( inverseMatrixAttr )[0]
        multMatrixNodes = matrixAttr.listConnections( d=1, s=0, type='multMatrix' )
        for multMatrixNode in multMatrixNodes:
            firstAttr = multMatrixNode.i[0].listConnections( s=1, d=0, p=1 )
            secondAttr = multMatrixNode.i[1].listConnections( s=1, d=0, p=1 )
            thirdConnection = multMatrixNode.i[2].listConnections( s=1, d=0 )
            
            if not firstAttr or not secondAttr or thirdConnection: continue
            
            firstEqual = firstAttr[0] == matrixAttr
            secondEqual = secondAttr[0] == inverseMatrixAttr
            
            if firstEqual and secondEqual:
                pymel.core.select( multMatrixNode )
                return multMatrixNode
        return sgCmds.createLocalMatrix( matrixAttr, inverseMatrixAttr )
    
    
    @staticmethod
    def setBindPreMatrix( inputJnt, inputBindPre ):
    
        jnt = pymel.core.ls( inputJnt )[0]
        bindPre = pymel.core.ls( inputBindPre )[0]
        
        targetAttrs = jnt.wm.listConnections( s=0, d=1, type='skinCluster', p=1 )
        if not targetAttrs: return None
        
        for targetAttr in targetAttrs:
            node = targetAttr.node()
            try:index = targetAttr.index()
            except: continue
            bindPre.wim >> node.bindPreMatrix[ index ]
    
    
    @staticmethod
    def createLocalMatrix( matrixAttr, inverseMatrixAttr ):
        matrixAttr = pymel.core.ls( matrixAttr )[0]
        inverseMatrixAttr = pymel.core.ls( inverseMatrixAttr )[0]
        multMatrixNode = pymel.core.createNode( 'multMatrix' )
        matrixAttr >> multMatrixNode.i[0]
        inverseMatrixAttr >> multMatrixNode.i[1]
        return multMatrixNode
    
    
    @staticmethod
    def getLocalDecomposeMatrix( matrixAttr, matrixAttrInv ):
        return sgCmds.getDecomposeMatrix( sgCmds.getLocalMatrix( matrixAttr, matrixAttrInv ).matrixSum )


    @staticmethod
    def constrain_parent( first, target, **options ):
        
        mo = False
        if options.has_key( 'mo' ):
            mo = options['mo']
        
        mm = sgCmds.getConstrainMatrix( first, target )
        dcmp = sgCmds.getDecomposeMatrix( mm.matrixSum )
        
        if mo:
            localMtx = sgCmds.getMMatrix( target.wm ) * sgCmds.getMMatrix( first.wim )
            trValue = sgCmds.getTranslateFromMatrix( localMtx )
            rotValue = sgCmds.getRotateFromMatrix( localMtx )
            scaleValue = sgCmds.getScaleFromMatrix( localMtx )
            shearValue = sgCmds.getShearFromMatrix( localMtx )
            compose = pymel.core.createNode( 'composeMatrix' )
            compose.it.set( trValue )
            compose.ir.set( rotValue )
            compose.inputScale.set( scaleValue )
            compose.ish.set( shearValue )
            sgCmds.insertMatrix( compose.outputMatrix, mm )
        
        cmds.connectAttr( dcmp + '.ot',  target + '.t', f=1 )
        cmds.connectAttr( dcmp + '.or',  target + '.r', f=1 )
        




class sgRig:    
    
    @staticmethod
    def createMatrixObjectFromGeo( target, directionBasedGeo=False ):
    
        targetShapes = pymel.core.listRelatives( target, c=1, ad=1, type='mesh' )
        
        if directionBasedGeo:
            vectorDicts = {}
            xBaseVector = OpenMaya.MVector( 1,0,0 )
            yBaseVector = OpenMaya.MVector( 0,1,0 )
            zBaseVector = OpenMaya.MVector( 0,0,1 )
            
            for targetShape in targetShapes:
                dagPathMesh = sgCmds.getDagPath(targetShape)
                fnMesh = OpenMaya.MFnMesh( dagPathMesh )
                
                points = OpenMaya.MPointArray()
                fnMesh.getPoints( points, OpenMaya.MSpace.kWorld )
                
                for i in range( fnMesh.numEdges() ):
                    util = OpenMaya.MScriptUtil()
                    util.createFromList([0,0],2)
                    int2Ptr = util.asInt2Ptr()
                    fnMesh.getEdgeVertices( i, int2Ptr )
                    index1 = util.getInt2ArrayItem( int2Ptr, 0, 0 )
                    index2 = util.getInt2ArrayItem( int2Ptr, 0, 1 )
                    
                    point1 = points[ index1 ]
                    point2 = points[ index2 ]
                    
                    vector = point2 - point1
                    
                    dotX = math.fabs( xBaseVector * vector )
                    dotY = math.fabs( yBaseVector * vector )
                    dotZ = math.fabs( zBaseVector * vector )
                    
                    if dotY == max( [ dotX, dotY, dotZ ] ):
                        continue
                    
                    if dotX > dotZ:
                        convertedVector = vector if xBaseVector * vector > 0 else -vector
                    elif dotZ >= dotX:
                        convertedVector = vector if zBaseVector * vector > 0 else -vector
                    
                    key = "%.2f,%.2f,%.2f" %( convertedVector.x, convertedVector.y, convertedVector.z )
                    if not vectorDicts.has_key( key ):
                        vectorDicts[ key ] = { "value":[convertedVector.x, 0, convertedVector.z], "length":convertedVector.length()}
                    else:
                        vectorDicts[ key ]['length'] += convertedVector.length()
                        vectorDicts[ key ]['value'][0] +=  convertedVector.x
                        vectorDicts[ key ]['value'][1] +=  0
                        vectorDicts[ key ]['value'][2] +=  convertedVector.z
                
            maxLength = 0.0
            maxLengthKey = None
            for key in vectorDicts.keys():
                if maxLength < vectorDicts[ key ]['length']:
                    maxLength = vectorDicts[ key ]['length']
                    maxLengthKey = key
            
            horizonVector = OpenMaya.MVector( *vectorDicts[ maxLengthKey ][ 'value' ] ).normal()
            upVector      = OpenMaya.MVector( 0,1,0 )
            
            dotX = math.fabs( xBaseVector * horizonVector )
            dotZ = math.fabs( zBaseVector * horizonVector )
            
            if dotX > dotZ:
                xVector = horizonVector
                yVector = upVector
                zVector = horizonVector ^ upVector
            else:
                xVector = horizonVector
                yVector = upVector
                zVector = upVector ^ horizonVector
        else:
            xVector = OpenMaya.MVector( 1,0,0 )
            yVector = OpenMaya.MVector( 0,1,0 )
            zVector = OpenMaya.MVector( 0,0,1 )
        
        worldPivot = pymel.core.xform( target, q=1, ws=1, rotatePivot=1 )
        mtxList = [xVector.x, xVector.y, xVector.z,0, yVector.x, yVector.y, yVector.z,0, zVector.x, zVector.y, zVector.z,0, worldPivot[0],worldPivot[1],worldPivot[2],1]
        mtx = sgCmds.listToMatrix( mtxList )
        invMtx = mtx.inverse()
        
        bb = OpenMaya.MBoundingBox()
        
        pointsList = []
        for targetShape in targetShapes:
            dagPathMesh = sgCmds.getDagPath(targetShape)
            fnMesh = OpenMaya.MFnMesh( dagPathMesh )
            
            points = OpenMaya.MPointArray()
            fnMesh.getPoints( points, OpenMaya.MSpace.kWorld )
            pointsList.append( points )
        
        for points in pointsList:
            for i in range( points.length() ):
                bb.expand( points[i] * invMtx )
            
        bbCenter = bb.center() * mtx
        mtxList[12] = bbCenter.x;mtxList[13] = bbCenter.y;mtxList[14] = bbCenter.z
        
        tr = pymel.core.createNode( 'transform' )
        tr.dh.set( 1 )
        pymel.core.xform( tr, ws=1, matrix= mtxList )
        xSize = bb.max().x-bb.min().x
        ySize = bb.max().y-bb.min().y
        zSize = bb.max().z-bb.min().z
        tr.s.set( xSize, ySize, zSize )
        return tr
    
    
    
    @staticmethod
    def createLatticeController( targets, numController=0 ):

        numController = max([numController,2])
        deformer, lattice, latticeBase = pymel.core.lattice(  divisions=[2,numController,2], objectCentered=False,  ldv=[2,numController+1,2] )
        mtxObject = sgRig.createMatrixObjectFromGeo( targets )
        pymel.core.parent( lattice, latticeBase, mtxObject )
        lattice.t.set( 0,0,0 ), lattice.r.set( 0,0,0 ), lattice.s.set( 1,1,1 )
        latticeBase.t.set( 0,0,0 ), latticeBase.r.set( 0,0,0 ), latticeBase.s.set( 1,1,1 )
        
        mtxObjectSize = mtxObject.sx.get() + mtxObject.sy.get() + mtxObject.sz.get()
        minSize = mtxObjectSize / 20.0
        mtxObject.sx.set( max( [minSize,mtxObject.sx.get()] ) )
        mtxObject.sy.set( max( [minSize,mtxObject.sy.get()] ) )
        mtxObject.sz.set( max( [minSize,mtxObject.sz.get()] ) )
        mtxObject.v.set( 0 )
    
        mainCtl = sgCmds.makeController( sgModel.Controller.cubePoints, 1, makeParent=1 );sgCmds.setIndexColor( mainCtl, 22 )
        pymel.core.xform( mainCtl, ws=1, matrix=mtxObject.wm.get() )
    
        sgCmds.constrain_all( mainCtl, mtxObject )
    
        dtCtlBase = pymel.core.createNode( 'transform' )
        sgCmds.constrain_parent( mainCtl, dtCtlBase )
    
        pointers = []
        for i in range( numController ):
            position = float(i)/(numController-1) - 0.5
            pointer = pymel.core.createNode( 'transform' )
            pointer.setParent( mainCtl )
            sgCmds.setTransformDefault( pointer )
            pointer.ty.set( position )
            pointers.append( pointer )
            sgCmds.constrain_scale( dtCtlBase, pointer )
        
        conditionNode = pymel.core.createNode( 'condition' )
        conditionNode.op.set( 4 )
        mtxObject.sx >> conditionNode.firstTerm
        mtxObject.sz >> conditionNode.secondTerm
        mtxObject.sx >> conditionNode.colorIfTrueR
        mtxObject.sz >> conditionNode.colorIfFalseR
        
        joints = []
        bindPres = []
        planeCtls = []
        
        beforeParent = dtCtlBase
        for pointer in pointers:
            moveCtl = sgCmds.makeController( sgModel.Controller.movePoints, 1, makeParent=1 );sgCmds.setIndexColor( moveCtl, 20 )
            conditionNode.outColorR >> moveCtl.scaleMult
            
            dcmp = sgCmds.getLocalDecomposeMatrix( pointer.wm, beforeParent.wim )
            planeCtl = sgCmds.makeController( sgModel.Controller.circlePoints, 0.5, makeParent=1 );sgCmds.setIndexColor( planeCtl, 18 )
            moveCtl.getParent().setParent( planeCtl )
            ctlShape = planeCtl.getShape()
            pPlaneCtl = planeCtl.getParent()
            pPlaneCtl.setParent( beforeParent )
            dcmp.ot >> pPlaneCtl.t
            dcmp.outputRotate >> pPlaneCtl.r
            mainCtl.sx >> ctlShape.shape_sx
            mainCtl.sy >> ctlShape.shape_sy
            mainCtl.sz >> ctlShape.shape_sz
            
            multSxMinus = pymel.core.createNode( 'multDoubleLinear' )
            multSxPlus = pymel.core.createNode( 'multDoubleLinear' )
            multSzMinus = pymel.core.createNode( 'multDoubleLinear' )
            multSzPlus = pymel.core.createNode( 'multDoubleLinear' )
            
            mainCtl.sx >> multSxMinus.input1; multSxMinus.input2.set( -0.5 )
            mainCtl.sx >> multSxPlus.input1; multSxPlus.input2.set( 0.5 )
            mainCtl.sz >> multSzMinus.input1; multSzMinus.input2.set( -0.5 )
            mainCtl.sz >> multSzMinus.input1; multSzMinus.input2.set( 0.5 )
            
            for i, position in [ (0,[multSxMinus,multSzMinus]), (1,[multSxMinus,multSzPlus]), 
                                 (2,[multSxPlus,multSzMinus]), (3,[multSxPlus,multSzPlus]) ]:
                pymel.core.select( moveCtl )
                joint   = pymel.core.joint(); joint.drawStyle.set( 2 )
                bindPre = pymel.core.createNode( 'transform' )
                bindPre.setParent( pointer )
                sgCmds.setTransformDefault( bindPre )
                joints.append( joint )
                bindPres.append( bindPre )
                position[0].output >> joint.tx; position[1].output >> joint.tz
                position[0].output >> bindPre.tx; position[1].output >> bindPre.tz
            planeCtls.append( planeCtl )
            beforeParent = pointer
        
        for i in range( len( planeCtls )-1 ):
            planeCtls[i+1].getParent().setParent( planeCtls[i] )
    
        skinCluster = pymel.core.skinCluster( joints, lattice, dr=1000 )
        for i in range( len( joints ) ):
            sgCmds.setBindPreMatrix( joints[i], bindPres[i] )
        lattice.wm >> skinCluster.geomMatrix
    
        allGrp = pymel.core.createNode( 'transform' )
        pymel.core.parent( mainCtl.getParent(), mtxObject, dtCtlBase, allGrp )
    
        return mainCtl




class Window( QDialog ):
    
    mayaWin = shiboken.wrapInstance( long( maya.OpenMayaUI.MQtUtil.mainWindow() ), QWidget )
    objectName = "sgWidget_latticeController"
    title = "Widget - Lattice Controller"
    defaultWidth = 300
    defaultHeight = 50


    def __init__(self, *args, **kwargs ):
        
        QDialog.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setWindowTitle( Window.title )
    
        mainLayout = QVBoxLayout( self )
        
        wLabelDescription = QLabel( "Select Object or Group" )
        
        validator = QIntValidator()
        
        hLayout = QHBoxLayout()
        wLabel = QLabel( "Num Controller : " )
        wLineEdit= QLineEdit();wLineEdit.setValidator(validator); wLineEdit.setText( '5' )
        hLayout.addWidget( wLabel )
        hLayout.addWidget( wLineEdit )
        
        button = QPushButton( "Create" )
        
        mainLayout.addWidget( wLabelDescription )
        mainLayout.addLayout( hLayout )
        mainLayout.addWidget( button )

        self.resize(Window.defaultWidth,Window.defaultHeight)
        
        self.wlineEdit = wLineEdit
        
        QtCore.QObject.connect( button, QtCore.SIGNAL( "clicked()" ), self.cmd_create )
    

    def cmd_create(self):
        
        cmds.undoInfo( ock=1 )
        mainCtl = sgRig.createLatticeController( pymel.core.ls( sl=1 ), int(self.wlineEdit.text()) )
        pymel.core.select( mainCtl )
        cmds.undoInfo( cck=1 )




def show( evt=0 ):
    
    if cmds.window( Window.objectName, ex=1 ):
        cmds.deleteUI( Window.objectName )
    
    mainUI = Window(Window.mayaWin)
    mainUI.setObjectName( Window.objectName )
    mainUI.resize( Window.defaultWidth, Window.defaultHeight )
    mainUI.show()



if __name__ == '__main__':
    show()

