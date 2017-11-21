import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import os, json
from pymel.core import nodetypes
from __qtImprot import * 
import maya.OpenMayaUI
import ntpath



def makeFolder( pathName ):
    if os.path.exists( pathName ):return None
    os.makedirs( pathName )
    return pathName



def exportAlembic( exportPath, minFrame, maxFrame ):
    
    def getCurrentModelPanels():
        pannels = cmds.getPanel( vis=1 )
        modelPanels = []
        for pannel in pannels:
            if cmds.modelPanel( pannel, ex=1 ):
                modelPanels.append( pannel )
        return modelPanels


    def getTopTransformNodes():
        topNodes = cmds.ls( sl=1 )
        if not topNodes:
            sels = cmds.ls( l=1, type='transform' )
            topNodes = []
            for sel in sels:
                if len( sel.split( '|' ) ) == 2:
                    topNodes.append( sel )
        return topNodes
    
    makeFolder( os.path.dirname( exportPath ) )
    
    exportRoots = getTopTransformNodes()
    
    rootStr = ''
    for exportRoot in exportRoots:
        rootStr += ' -root %s ' % exportRoot
    
    cmds.AbcExport( j="-frameRange %d %d -noNormals -ro -uvWrite -wholeFrameGeo -writeVisibility -eulerFilter"\
                " -dataFormat ogawa %s -file %s" %( minFrame, maxFrame, rootStr, exportPath ) )



def exportSceneInfo( infoPath, minFrame, maxFrame ):
    
    def getTopTransformNodes():
        sels = cmds.ls( l=1, type='transform' )
        topNodes = []
        for sel in sels:
            if len( sel.split( '|' ) ) == 2:
                topNodes.append( sel )
        return topNodes
    
    def getNamespaceRootTransformNodes( targetTransform ):
        
        targetNodes = []
        if targetTransform.find( ':' ) != -1:
            targetNodes.append( targetTransform )
        else:
            children = cmds.listRelatives( targetTransform, c=1, f=1 )
            if children:
                for child in children:
                    targetNodes += getNamespaceRootTransformNodes( child )
        return targetNodes
    
    def getBBCenter( targetTransform ):
        bbmin = cmds.getAttr( targetTransform + '.boundingBoxMin' )[0]
        bbmax = cmds.getAttr( targetTransform + '.boundingBoxMax' )[0]
        bbcenter = OpenMaya.MPoint( (bbmin[0] + bbmax[0])/2.0, (bbmin[1] + bbmax[1])/2.0, (bbmin[2] + bbmax[2])/2.0  )
        pmtx = cmds.getAttr( targetTransform + '.parentMatrix' )
        mtx = OpenMaya.MMatrix()
        OpenMaya.MScriptUtil.createMatrixFromList( pmtx, mtx )
        bbcenter *= mtx
        return [bbcenter.x, bbcenter.y,bbcenter.z]
        
                
    topNodes = getTopTransformNodes()
    namespaceRootNodes = []
    for topNode in topNodes:
        namespaceRootNodes += getNamespaceRootTransformNodes( topNode )
    
    namespaceList = []
    rootCenters = []
    for namespaceRootNode in namespaceRootNodes:
        localName = namespaceRootNode.split( '|' )[-1]
        nodeNs = ':'.join( localName.split( ':' )[:-1] )
        namespaceList.append( nodeNs )
        rootCenters.append( getBBCenter( namespaceRootNode ) )
    
    print "export scene info"
    
    makeFolder( os.path.dirname( infoPath ) )
    sceneInfomation = {"timeUnit":cmds.currentUnit( q=1, time=1 ),"minFrame":minFrame,"maxFrame":maxFrame,"exportFrame":cmds.currentTime(q=1), 'namespaceRoots':namespaceRootNodes,
                       'rootCenters':rootCenters }

    f = open( infoPath, 'w' )
    json.dump( sceneInfomation, f, indent=2 )
    f.close()




class Window_global:
    
    name = "sgSceneExport"
    title = "UI - Scene Export"
    wh = [430,20]
    
    folderIconPath = os.path.dirname( __file__ ) + '/icon/folder.png'
    form_exportTarget = ''
    scriptJopIndex = None
    
    import __init__
    recentInfoPath = __init__.recentInfoPath
    
    mayaWin = shiboken.wrapInstance( long( maya.OpenMayaUI.MQtUtil.mainWindow() ), QWidget )
    txf_rootPath = ''
    txf_abcPath = ''
    txf_sceneInfoPath = ''

    @staticmethod
    def getDefaultFolder():
        dirPath = os.path.dirname( cmds.file( q=1, sceneName=1 ) )
        dirname = ntpath.split( dirPath )[-1]
        return os.path.dirname( cmds.file( q=1, sceneName=1 ) ) + '/' + dirname + '_cache'# + '/' + sceneLocalName
    
    
    @staticmethod
    def getDefaultAlembicName():
        dirPath = os.path.dirname( cmds.file( q=1, sceneName=1 ) )
        dirname = ntpath.split( dirPath )[-1]
        return dirname + '.abc'
    
    
    @staticmethod
    def getDefaultSceneInfoName():
        dirPath = os.path.dirname( cmds.file( q=1, sceneName=1 ) )
        dirname = ntpath.split( dirPath )[-1]
        return dirname + '.sceneInfo'
    
    
    


class Window_cmds:
    
    @staticmethod
    def getDirectory( evt=0 ):
    
        dialog = QFileDialog(Window_global.mayaWin )
        dialog.setDirectory( Window_global.getDefaultFolder() )
        choosedFolder = dialog.getExistingDirectory()
        if not choosedFolder: choosedFolder = Window_global.getDefaultFolder()
        cmds.textField( Window_global.txf_rootPath, e=1, tx=choosedFolder )
    


    @staticmethod
    def exportScene( evt=0 ):
        
        rootPath = cmds.textField( Window_global.txf_rootPath, q=1, tx=1 )
        abcPath  = cmds.textField( Window_global.txf_abcPath, q=1, tx=1 )
        sceneInfoPath = cmds.textField( Window_global.txf_sceneInfoPath, q=1, tx=1 )
        
        minFrame = cmds.playbackOptions( q=1, min=1 )
        maxFrame = cmds.playbackOptions( q=1, max=1 )
        exportAlembic( rootPath + '/' + abcPath, minFrame, maxFrame )
        exportSceneInfo( rootPath + '/' + sceneInfoPath, minFrame, maxFrame )
        
        data = { 'rootPath':rootPath, 'abcPath':abcPath, 'sceneInfoPath':sceneInfoPath }
        f = open( Window_global.recentInfoPath, 'w' )
        json.dump( data ,f )
        f.close()





class UI_exportPath:
    
    def __init__(self):
        pass
    
    def create(self):
        
        form = cmds.formLayout()
        tx_rootPath = cmds.text( l='Root Path : ', h=25, w=90, al='right' )
        txf_rootPath = cmds.textField( tx = Window_global.getDefaultFolder(), h=25 )
        itb_rootPath = cmds.iconTextButton( image= Window_global.folderIconPath, w=25, h=25, c=Window_cmds.getDirectory )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af = [ (tx_rootPath, 'top', 5), (tx_rootPath, 'left', 5),
                                (itb_rootPath, 'top', 5), (itb_rootPath, 'right', 15 ),
                                (txf_rootPath, 'top', 5), (txf_rootPath, 'bottom', 5) ],
                         ac = [ (txf_rootPath, 'left', 5, tx_rootPath ), (txf_rootPath, 'right', 5, itb_rootPath ) ] )
        
        Window_global.txf_rootPath = txf_rootPath
        
        return form




class UI_exportTargets:
    
    def __init__(self):
        pass


    def create(self):
        
        form = cmds.formLayout()
        tx_abcPath = cmds.text( l='Alembic Path : ', h=25, w=90, al='right' )
        txf_abcPath = cmds.textField( tx = Window_global.getDefaultAlembicName(), h=25 )
        tx_sceneInfoPath = cmds.text( l='Scene Info Path : ', h=25, w=90, al='right' )
        txf_sceneInfoPath = cmds.textField( tx = Window_global.getDefaultSceneInfoName(), h=25 )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af=[( tx_abcPath, 'top', 5 ), ( tx_abcPath, 'left', 5 ),
                             ( txf_abcPath, 'top', 5 ), ( txf_abcPath, 'right', 5 ),
                             ( tx_sceneInfoPath, 'bottom', 5 ), ( tx_sceneInfoPath, 'left', 5 ),
                             ( txf_sceneInfoPath, 'bottom', 5 ), ( txf_sceneInfoPath, 'right', 5 )],
                         ac = [ (txf_abcPath, 'left', 5, tx_abcPath ), (txf_sceneInfoPath, 'left', 5, tx_sceneInfoPath ),
                                (tx_sceneInfoPath, 'top', 5, tx_abcPath ), (txf_sceneInfoPath, 'top', 5, tx_abcPath ) ] )
        
        Window_global.form_exportTarget = form
        
        Window_global.txf_abcPath = txf_abcPath
        Window_global.txf_sceneInfoPath = txf_sceneInfoPath
        
        
        return form
    





class Window:
    
    def __init__(self):
        
        self._ui_exportPath = UI_exportPath()
        self._ui_exportTargets = UI_exportTargets()
    
    
    def show(self, evt=0 ):
        
        Window_global.selectIndex = 0
        
        if cmds.window( Window_global.name, ex=1 ):
            cmds.deleteUI( Window_global.name, wnd=1 )
        cmds.window( Window_global.name, title=Window_global.title )
        
        form = cmds.formLayout()
        exportPath = self._ui_exportPath.create()
        exportTargets = self._ui_exportTargets.create()
        buttonExport = cmds.button( l='Export', h=30, c=Window_cmds.exportScene )
        cmds.setParent('..')
        
        cmds.formLayout( form, e=1, 
                         af = [( exportPath, 'top', 0 ), ( exportPath, 'left', 0 ), ( exportPath, 'right', 0 ),
                               ( buttonExport, 'left', 0 ), ( buttonExport, 'right', 0 ),
                               ( exportTargets, 'left', 0 ), ( exportTargets, 'right', 0 )],
                         ac = [( buttonExport, 'top', 0, exportTargets ), ( exportTargets, 'top', 0, exportPath )] )
        
        cmds.window( Window_global.name, e=1, wh= Window_global.wh, rtf=1 )
        cmds.showWindow( Window_global.name )


def show():
    
    Window().show()



