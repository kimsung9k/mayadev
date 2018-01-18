#coding=utf8

from maya import cmds, mel, OpenMaya
import maya.OpenMayaUI
from functools import partial
import pymel.core, math, copy, os, json
from maya.api._OpenMaya_py2 import MFnDependencyNode



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
    
    pass



class sgCmds:
    
    @staticmethod
    def makeFolder( pathName ):
        if os.path.exists( pathName ):return None
        os.makedirs( pathName )
        return pathName
    
    
    @staticmethod
    def makeFile( filePath ):
        if os.path.exists( filePath ): return None
        filePath = filePath.replace( "\\", "/" )
        splits = filePath.split( '/' )
        folder = '/'.join( splits[:-1] )
        sgCmds.makeFolder( folder )
        f = open( filePath, "w" )
        f.close()
    
    
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
    def getMObject( inputTarget ):
        target = pymel.core.ls( inputTarget )[0]
        mObject = OpenMaya.MObject()
        selList = OpenMaya.MSelectionList()
        selList.add( target.name() )
        selList.getDependNode( 0, mObject )
        return mObject
        
    
    
        


class LocalCmds:    
    
    @staticmethod
    def getMesh():
        pass





class Widget_LoadVertex( QWidget ):

    def __init__(self, *args, **kwargs ):
        
        QWidget.__init__( self, *args )
        
        title = ""
        if kwargs.has_key( 'title' ):
            title = kwargs['title']
            
        self.infoPath = cmds.about(pd=True) + "/sg/fingerWeightCopy/Widget_LoadVertex_%s.txt" % title
        sgCmds.makeFile( self.infoPath )
        
        vLayout = QVBoxLayout( self ); vLayout.setContentsMargins(0,0,0,0)
        
        groupBox = QGroupBox( title )
        groupBox.setAlignment( QtCore.Qt.AlignCenter )
        vLayout.addWidget( groupBox )
        
        hLayout = QHBoxLayout()
        lineEdit = QLineEdit()
        button   = QPushButton("Load"); button.setFixedWidth( 50 )
        hLayout.addWidget( lineEdit )
        hLayout.addWidget( button )
        
        groupBox.setLayout( hLayout )
        
        self.lineEdit = lineEdit
        
        QtCore.QObject.connect( button, QtCore.SIGNAL( "clicked()" ), self.loadVertex )
        self.loadInfo()
    
    
    def loadVertex(self):
        
        selVertices = cmds.ls( sl=1, fl=1 )
        if len( selVertices ) != 1:
            cmds.error( "Select Only One Vertex" )
        
        targetVtx = None
        for vtx in selVertices:
            if vtx.find( 'vtx' ) == -1: continue
            targetVtx = vtx
            break
        if not targetVtx: return None
        self.lineEdit.setText( targetVtx )
        self.saveInfo()
    


    def saveInfo(self):
        
        f = open( self.infoPath, 'w' )
        data = [ self.lineEdit.text() ]
        json.dump( data, f, indent=2 )
        f.close()
    


    def loadInfo(self):
        
        f = open( self.infoPath, 'r' )
        try:data = json.load( f )
        except: f.close();return
        f.close()
        if not data: data = []
        self.lineEdit.setText( data[0] )
        
    
        



class Widget_SelectionGrow( QWidget ):
    
    def __init__(self, *args, **kwargs ):
        
        QWidget.__init__( self, *args )
        
        self.infoPath = cmds.about(pd=True) + "/sg/fingerWeightCopy/Widget_SelectionGrow.txt"
        sgCmds.makeFile( self.infoPath )
        
        validator = QIntValidator()
        
        layout = QHBoxLayout( self ); layout.setContentsMargins(0,0,0,0)
        groupBox = QGroupBox()
        layout.addWidget( groupBox )
        
        hLayout = QHBoxLayout()
        labelTitle = QLabel( "Grow Selection : " )
        buttonGrow = QPushButton( "Grow" ); buttonGrow.setFixedWidth( 50 )
        buttonShrink = QPushButton( "Shrink" ); buttonShrink.setFixedWidth( 50 )        
        lineEdit = QLineEdit(); lineEdit.setValidator( validator );lineEdit.setText( '0' )
        
        hLayout.addWidget( labelTitle )
        hLayout.addWidget( buttonGrow )
        hLayout.addWidget( buttonShrink )
        hLayout.addWidget( lineEdit )
        
        groupBox.setLayout( hLayout )
        
        self.lineEdit = lineEdit
        
        QtCore.QObject.connect( buttonGrow, QtCore.SIGNAL("clicked()"), self.growNum )
        QtCore.QObject.connect( buttonShrink, QtCore.SIGNAL("clicked()"), self.shrinkNum )
        
        self.vtxLineEditList = []
        self.loadInfo()


    def growNum(self):
        
        try:beforeIndex = int( self.lineEdit.text() )
        except:beforeIndex = 0
        self.lineEdit.setText( str(beforeIndex+1) )
        self.saveInfo()
    
    
    def shrinkNum(self):
        
        try:beforeIndex = int( self.lineEdit.text() )
        except:beforeIndex = 0
        self.lineEdit.setText( str( max(beforeIndex-1, 0)) )
        self.saveInfo()
    
    
    def saveInfo(self):
        
        f = open( self.infoPath, 'w' )
        data = [ self.lineEdit.text() ]
        json.dump( data, f, indent=2 )
        f.close()
    
    
    
    def loadInfo(self):
        
        f = open( self.infoPath, 'r' )
        try:data = json.load( f )
        except: f.close();return
        f.close()
        if not data: data = []
        self.lineEdit.setText( data[0] )
    



class Widget_loadJoints( QWidget ):


    def __init__(self, title, *args, **kwargs ):
        
        QWidget.__init__( self, *args )
        
        self.infoPath = cmds.about(pd=True) + "/sg/fingerWeightCopy/Widget_loadJoints_%s.txt" % title
        sgCmds.makeFile( self.infoPath )
        
        layout = QVBoxLayout( self ); layout.setContentsMargins(0,0,0,0)
        
        groupBox = QGroupBox( title )
        layout.addWidget( groupBox )
        
        baseLayout = QVBoxLayout()
        groupBox.setLayout( baseLayout )
        
        listWidget = QListWidget()
        
        hl_buttons = QHBoxLayout(); hl_buttons.setSpacing( 5 )
        b_addSelected = QPushButton( "Add Selected" )
        b_clear = QPushButton( "Clear" )
        
        hl_buttons.addWidget( b_addSelected )
        hl_buttons.addWidget( b_clear )
        
        baseLayout.addWidget( listWidget )
        baseLayout.addLayout( hl_buttons )
        
        self.listWidget = listWidget
        
        QtCore.QObject.connect( listWidget, QtCore.SIGNAL( "itemClicked(QListWidgetItem*)" ), self.selectJointFromItem )
        QtCore.QObject.connect( b_addSelected, QtCore.SIGNAL("clicked()"), self.addSelected )
        QtCore.QObject.connect( b_clear, QtCore.SIGNAL( "clicked()" ), self.clearSelected )
        
        self.otherWidget = None        
        self.loadInfo()
    


    def addSelected(self):
        
        selJoints = []
        for i in range( self.listWidget.count() ):
            selJoints += cmds.ls( self.listWidget.item( i ).text() )
        
        for selJnt in cmds.ls( os=1, type='joint' ):
            if selJnt in selJoints: continue
            selJoints.append( selJnt )
        
        self.listWidget.clear()
        self.listWidget.addItems( selJoints )
        self.saveInfo()
    
    
    
    def clearSelected(self):
        
        self.listWidget.clear()
        self.saveInfo()
    
    
    
    def selectJointFromItem(self, item ):
        
        cmds.select( item.text() )
        
        if not self.otherWidget: return 
        itemIndex = self.listWidget.row( item )
        if self.otherWidget.listWidget.count() <= itemIndex: return
        
        otherItem = self.otherWidget.listWidget.item( itemIndex )
        self.otherWidget.listWidget.setCurrentItem( otherItem )
        
        otherJoint = otherItem.text()
        if not cmds.objExists( otherJoint ): return
        cmds.select( otherJoint, add=1 )

    
    
    def saveInfo(self):
        
        f = open( self.infoPath, 'w' )
        data = [ self.listWidget.item(i).text() for i in range( self.listWidget.count() ) ]
        json.dump( data, f, indent=2 )
        f.close()
    
    
    
    def loadInfo(self):
        
        f = open( self.infoPath, 'r' )
        try:data = json.load( f )
        except: f.close();return
        f.close()
        if not data: data = []
        self.listWidget.clear()
        self.listWidget.addItems( data )




class Function_growSelectionInfo:
    
    def __init__(self, meshName ):
                
        self.dagPath = sgCmds.getDagPath( meshName )
        self.itMeshVertex = OpenMaya.MItMeshVertex( self.dagPath )
        self.itMeshPolygon = OpenMaya.MItMeshPolygon( self.dagPath )
        self.checkedIndices = []


    def setCheckedIndices(self, indices ):
    
        self.checkedIndices = indices
    
    
    def getGrowIndices(self):
        
        util = OpenMaya.MScriptUtil()
        util.createFromInt( 1 )
        prevIndex = util.asIntPtr()
        
        if not self.checkedIndices:
            cmds.error( "checked indices is not exists" ); return []
    
        targetVtxIndices = []
        for i in range( len( self.checkedIndices ) ):
            checkedIndex = self.checkedIndices[i]
            intArrFaces = OpenMaya.MIntArray()
            self.itMeshVertex.setIndex( checkedIndex, prevIndex )
            self.itMeshVertex.getConnectedFaces( intArrFaces )
            for j in range( intArrFaces.length() ):
                faceIndex = intArrFaces[j]
                intArrVertices = OpenMaya.MIntArray()
                self.itMeshPolygon.setIndex( faceIndex, prevIndex )
                self.itMeshPolygon.getVertices( intArrVertices )
                for k in range( intArrVertices.length() ):
                    vtxIndex = intArrVertices[k]
                    if vtxIndex in self.checkedIndices: continue
                    targetVtxIndices.append( vtxIndex )
                    self.checkedIndices.append( vtxIndex )
        return targetVtxIndices



class Function_skinWeight:
    
    def __init__(self, srcMesh, influences ):
        
        srcMeshSkinCluters = sgCmds.getNodeFromHistory( srcMesh, 'skinCluster' )
    
        if not srcMeshSkinCluters:
            cmds.error( "%s has no skincluster" % srcMesh ); return
    
        fnSkinCluster = OpenMaya.MFnDependencyNode( sgCmds.getMObject( srcMeshSkinCluters[0] ) )
    
        self.influenceIndices = []
        for origPlug, influencePlug in pymel.core.listConnections( fnSkinCluster.name() + '.matrix', s=1, d=0, p=1, c=1 ):
            influenceName = influencePlug.node().name()
            if not influenceName in influences: continue
            self.influenceIndices.append( origPlug.index() ) 

        self.weightListPlug = fnSkinCluster.findPlug( 'weightList' )
        self.vtxIndex = 0
    
        self.weightsPlug = self.weightListPlug.elementByLogicalIndex( self.vtxIndex ).child(0)
        
        self.influenceWeights = {}
        for i in range( self.weightsPlug.numElements() ):
            weightPlug = self.weightsPlug.elementByPhysicalIndex( i )
            logicalIndex = weightPlug.logicalIndex()
            self.influenceWeights[ logicalIndex ] = weightPlug.asFloat()
        
    
    def setVtxIndex(self, index ):
        self.vtxIndex = index
    
        self.weightsPlug = self.weightListPlug.elementByLogicalIndex( self.vtxIndex ).child(0)
        
        self.influenceWeights = {}
        for i in range( self.weightsPlug.numElements() ):
            weightPlug = self.weightsPlug.elementByPhysicalIndex( i )
            logicalIndex = weightPlug.logicalIndex()
            self.influenceWeights[ logicalIndex ] = weightPlug.asFloat()
    
    
    @staticmethod
    def copyWeight( src, trg ):
        
        srcInfluences = src.influenceIndices
        trgInfluences = trg.influenceIndices
        
        srcKeys = src.influenceWeights.keys()
        
        trgInfluenceWeights = copy.deepcopy( trg.influenceWeights )
        
        copyWeightValues = {}
        sumWeights = 0
        
        for srcKey in srcKeys:
            if not srcKey in srcInfluences: continue
            trgKey = trgInfluences[ srcInfluences.index( srcKey ) ]
            srcWeightValue = src.influenceWeights[ srcKey ]
            if not trgInfluenceWeights.has_key( trgKey ): continue
            copyWeightValues[ trgKey ] = srcWeightValue
            trgInfluenceWeights.pop( trgKey )
            sumWeights += srcWeightValue
        
        otherSumWeights = 0
        for trgKey in trgInfluenceWeights.keys():
            otherSumWeights += trgInfluenceWeights[ trgKey ]
        
        multOtherWeight = 1.0 if otherSumWeights == 0 else (1-sumWeights)/otherSumWeights
        
        for trgKey in trgInfluenceWeights.keys():
            copyWeightValues[ trgKey ] = trgInfluenceWeights[ trgKey ] * multOtherWeight
        
        for key in copyWeightValues.keys():
            cmds.setAttr( trg.weightsPlug.elementByLogicalIndex( key ).name(), copyWeightValues[key] )





class Window( QDialog ):
    
    mayaWin = shiboken.wrapInstance( long( maya.OpenMayaUI.MQtUtil.mainWindow() ), QWidget )
    objectName = "sgWidget_fingerWeightCopy"
    title = "Widget - Finger Weight Copy"
    defaultWidth = 450
    defaultHeight = 50
    
    shapeInfoPath = cmds.about(pd=True) + "/sg/fingerWeightCopy/shapeInfo.txt"
    sgCmds.makeFile( shapeInfoPath )


    def __init__(self, *args, **kwargs ):
        
        QDialog.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setWindowTitle( Window.title )
    
        mainLayout = QVBoxLayout( self )
        
        sep1 = QFrame();sep1.setFrameShape(QFrame.HLine)
        sep2 = QFrame();sep2.setFrameShape(QFrame.HLine)
        sep3 = QFrame();sep3.setFrameShape(QFrame.HLine)
        
        hl_loadVtx = QHBoxLayout(); hl_loadVtx.setSpacing(5)
        w_loadVtx_src  = Widget_LoadVertex( title="Source Root Vertex" )
        w_loadVtx_trg  = Widget_LoadVertex( title="Target Root Vertex" )
        hl_loadVtx.addWidget( w_loadVtx_src )
        hl_loadVtx.addWidget( w_loadVtx_trg )
        
        hl_loadJoints = QHBoxLayout(); hl_loadJoints.setSpacing(5)
        w_loadJoints_src = Widget_loadJoints("Source Joints")
        w_loadJoints_trg = Widget_loadJoints("Target Joints")
        w_loadJoints_src.otherWidget = w_loadJoints_trg;w_loadJoints_trg.otherWidget = w_loadJoints_src;
        hl_loadJoints.addWidget( w_loadJoints_src )
        hl_loadJoints.addWidget( w_loadJoints_trg )
        
        w_selectionGrow = Widget_SelectionGrow()
        
        hl_select = QHBoxLayout(); hl_select.setSpacing(5)
        b_selectSrc = QPushButton( "Select Source Vertices" )
        b_selectTrg = QPushButton( "Select Target Vertices" )
        hl_select.addWidget( b_selectSrc )
        hl_select.addWidget( b_selectTrg )
        
        b_copyWeight = QPushButton( "Copy Weight" )
        
        mainLayout.addLayout( hl_loadVtx )
        mainLayout.addWidget( sep1 )
        mainLayout.addLayout( hl_loadJoints )
        mainLayout.addWidget( sep2 )
        mainLayout.addWidget( w_selectionGrow )
        mainLayout.addLayout( hl_select )
        mainLayout.addWidget( sep3 )
        mainLayout.addWidget( b_copyWeight )
        
        self.resize( Window.defaultWidth, Window.defaultHeight )
        
        self.li_sourceVertex = w_loadVtx_src.lineEdit
        self.li_targetVertex = w_loadVtx_trg.lineEdit
        self.li_numGrow      = w_selectionGrow.lineEdit
        self.lw_srcJoints    = w_loadJoints_src.listWidget
        self.lw_trgJoints    = w_loadJoints_trg.listWidget
        
        QtCore.QObject.connect( b_selectSrc,  QtCore.SIGNAL( "clicked()" ), self.selectSourceVertices )
        QtCore.QObject.connect( b_selectTrg,  QtCore.SIGNAL( "clicked()" ), self.selectTargetVertices )
        QtCore.QObject.connect( b_copyWeight, QtCore.SIGNAL( 'clicked()' ), self.copyWeight )
        
        
    
    def selectSourceVertices(self):
        
        vertexname = self.li_sourceVertex.text()
        numGrow = int( self.li_numGrow.text() )
        
        if not vertexname or not cmds.objExists( vertexname ): return None
        
        cmds.undoInfo( ock=1 )
        cmds.select( vertexname )
        for i in range( numGrow ):
            mel.eval( "GrowPolygonSelectionRegion" )
        cmds.undoInfo( cck=1 )
        
        self.saveInfo()
    
    
    def selectTargetVertices(self):
        
        vertexname = self.li_targetVertex.text()
        numGrow = int( self.li_numGrow.text() )
        
        if not vertexname or not cmds.objExists( vertexname ): return None
        
        cmds.undoInfo( ock=1 )
        cmds.select( vertexname )
        for i in range( numGrow ):
            mel.eval( "GrowPolygonSelectionRegion" )
        cmds.undoInfo( cck=1 )
        
        self.saveInfo()
    
    
    def copyWeight(self):

        cmds.undoInfo( ock=1 )

        try:
            beforeSels = cmds.ls( sl=1 )
            
            srcVtx = self.li_sourceVertex.text()
            trgVtx = self.li_targetVertex.text()
            numGrow = int( self.li_numGrow.text() )
            srcJoints = [ self.lw_srcJoints.item(i).text() for i in range( self.lw_srcJoints.count() ) ]
            trgJoints = [ self.lw_trgJoints.item(i).text() for i in range( self.lw_trgJoints.count() ) ]
            
            if not cmds.objExists( srcVtx ):
                cmds.error( "%s is not exists" % srcVtx );return
            if not cmds.objExists( trgVtx ):
                cmds.error( "%s is not exists" % trgVtx );return
            
            allJoints = []
            allJoints += srcJoints
            allJoints += trgJoints
            
            for joint in allJoints:
                if not cmds.objExists( joint ):
                    cmds.error( "%s is not exists" % joint );return
                if len( cmds.ls( joint ) ) > 1:
                    cmds.error( "%s is not unique" % joint );return
            
            srcVtx = pymel.core.ls( srcVtx )[0]
            trgVtx = pymel.core.ls( trgVtx )[0]
            
            skinSrcs = sgCmds.getNodeFromHistory( srcVtx.node(), 'skinCluster' )
            skinTrgs = sgCmds.getNodeFromHistory( trgVtx.node(), 'skinCluster' )
            
            if not skinSrcs:
                cmds.error( "%s has no skinCluster" % srcVtx.node().name() ); return
            if not skinTrgs:
                cmds.error( "%s has no skinCluster" % trgVtx.node().name() ); return
            
            
            fSkinWeightSrc = Function_skinWeight( srcVtx.node().name(), srcJoints )
            fSkinWeightTrg = Function_skinWeight( trgVtx.node().name(), trgJoints )
            fSkinWeightSrc.setVtxIndex( srcVtx.index() )
            fSkinWeightTrg.setVtxIndex( trgVtx.index() )
            
            Function_skinWeight.copyWeight( fSkinWeightSrc, fSkinWeightTrg )
            
            checkedSrcIndices = [srcVtx.index()]
            checkedTrgIndices = [trgVtx.index()]
            srcMeshGrowSelectionInfo = Function_growSelectionInfo( srcVtx.node().name() ); srcMeshGrowSelectionInfo.setCheckedIndices( checkedSrcIndices )
            trgMeshGrowSelectionInfo = Function_growSelectionInfo( trgVtx.node().name() ); trgMeshGrowSelectionInfo.setCheckedIndices( checkedTrgIndices )
            
            for i in range( numGrow ):
                srcVtxIndices = srcMeshGrowSelectionInfo.getGrowIndices()
                trgVtxIndices = trgMeshGrowSelectionInfo.getGrowIndices()
                if len( srcVtxIndices ) != len( trgVtxIndices ): break
                
                for j in range( len( srcVtxIndices ) ):
                    srcVtxIndex = srcVtxIndices[j]
                    trgVtxIndex = trgVtxIndices[j]
                    fSkinWeightSrc.setVtxIndex( srcVtxIndex )
                    fSkinWeightTrg.setVtxIndex( trgVtxIndex )
                    Function_skinWeight.copyWeight( fSkinWeightSrc, fSkinWeightTrg )
            
            cmds.select( trgVtx.node().name() )
            mel.eval( 'doNormalizeWeightsArgList 1 {"4"}' )
            cmds.select( beforeSels )
        except:
            pass
            
        cmds.undoInfo( cck=1 )


    def saveInfo( self ):
        
        filePath = Window.shapeInfoPath
        posX = self.pos().x()
        posY = self.pos().y()
        width  = self.width()
        height = self.height()
        f = open( filePath, "w" )
        json.dump( [posX, posY, width, height ], f, True, False, False )
        f.close()



    def loadInfo( self ):
        
        filePath = Window.shapeInfoPath
        
        f = open( filePath, 'r')
        try:data = json.load( f )
        except: f.close(); return None
        f.close()
        if not data: return None
        try:
            posX = data[0]
            posY = data[1]
            width = data[2]
            height = data[3]
            
            desktop = QApplication.desktop()
            desktopWidth = desktop.width()
            desktopHeight = desktop.height()
            if posX + width > desktopWidth: posX = desktopWidth - width
            if posY + height > desktopWidth: posY = desktopHeight - height
            if posX < 0 : posX = 0
            if posY < 0 : posY = 0
            
            self.move( posX, posY )
            self.resize( width, height )
        except:
            self.resize( Window.defaultWidth, Window.defaultHeight )
    


    def eventFilter( self, *args, **kwargs):
        
        event = args[1]
        if event.type() in [QtCore.QEvent.LayoutRequest,QtCore.QEvent.Move,QtCore.QEvent.Resize] :
            self.saveInfo()
        





def show( evt=0 ):
    
    if cmds.window( Window.objectName, ex=1 ):
        cmds.deleteUI( Window.objectName )
    
    mainUI = Window(Window.mayaWin)
    mainUI.setObjectName( Window.objectName )
    mainUI.loadInfo()
    mainUI.show()



if __name__ == '__main__':
    show()

