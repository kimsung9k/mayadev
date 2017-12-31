import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
from __qtImprot import *
import os, json
from pymel.core import nodetypes
import maya.OpenMayaUI



if not cmds.pluginInfo( 'AbcExport', q=1, l=1 ):
    cmds.loadPlugin( 'AbcExport' )


def makeFolder( pathName ):
    if os.path.exists( pathName ):return None
    os.makedirs( pathName )
    return pathName



class Window_global:
    
    name = "sgSceneImport"
    title = "UI - Scene Import"
    wh = [430,20]
    
    folderIconPath = os.path.dirname( __file__ ) + '/icon/folder.png'
    
    import __init__
    recentInfoPath = __init__.recentInfoPath

    form_exportTarget = ''
    scriptJopIndex = None
    
    mayaWin = shiboken.wrapInstance( long( maya.OpenMayaUI.MQtUtil.mainWindow() ), QWidget )
    txf_rootPath = ''
    txf_abcPath = ''
    txf_sceneInfoPath = ''
    
    
    

class Window_cmds:
    
    
    @staticmethod
    def getCamAndGeos():
        
        sels = cmds.ls( sl=1 )
        camAndGeos     = []
        for sel in sels:
            if cmds.listRelatives( sel, c=1, ad=1, type='mesh' ) or cmds.listRelatives( sel, c=1, ad=1, type='camera' ):
                camAndGeos.append( sel )
        return camAndGeos    

    
    @staticmethod
    def getDirectory( evt=0 ):
    
        dialog = QFileDialog(Window_global.mayaWin )
        dialog.setDirectory( Window_global.getDefaultFolder() )
        choosedFolder = dialog.getExistingDirectory()
        if not choosedFolder: choosedFolder = Window_global.getDefaultFolder()
        cmds.textField( Window_global.txf_rootPath, e=1, tx=choosedFolder )
    


    @staticmethod
    def importScene( evt=0 ):
        
        rootPath = cmds.textField( Window_global.txf_rootPath, q=1, tx=1 )
        abcPath  = rootPath + '/' + cmds.textField( Window_global.txf_abcPath, q=1, tx=1 )
        sceneInfoPath = rootPath + '/' + cmds.textField( Window_global.txf_sceneInfoPath, q=1, tx=1 )
        
        cmds.AbcImport( abcPath, mode='import' )
        
        def getBBCenter( targetTransform ):
            bbmin = cmds.getAttr( targetTransform + '.boundingBoxMin' )[0]
            bbmax = cmds.getAttr( targetTransform + '.boundingBoxMax' )[0]
            bbcenter = OpenMaya.MPoint( (bbmin[0] + bbmax[0])/2.0, (bbmin[1] + bbmax[1])/2.0, (bbmin[2] + bbmax[2])/2.0  )
            pmtx = cmds.getAttr( targetTransform + '.parentMatrix' )
            mtx = OpenMaya.MMatrix()
            OpenMaya.MScriptUtil.createMatrixFromList( pmtx, mtx )
            bbcenter *= mtx
            return [bbcenter.x, bbcenter.y,bbcenter.z]
        
        def addNamespaceToChildren( namespace, rootNode ):
            import pymel.core
            children = pymel.core.listRelatives( rootNode, c=1, ad=1, type='transform' )
            if not children: children = []
            for child in children:
                child.rename( namespace + ':' + child.name().split( '|' )[-1] )

        f = open( sceneInfoPath, 'r' )
        data = json.load( f )
        f.close()

        cmds.currentUnit( time=data['timeUnit'] )
        cmds.playbackOptions( min=data['minFrame'], max=data['maxFrame'] )
        cmds.currentTime( data['exportFrame'] )
        cmds.refresh()
        
        namespaceRoots = data['namespaceRoots']
        rootCenters = data['rootCenters']
        for i in range( len( namespaceRoots ) ):
            namespaceRoot = namespaceRoots[i]
            localName = namespaceRoot.split( '|' )[-1]
            namespace = ':'.join( localName.split( ':' )[:-1] )
            try:cmds.namespace( add=namespace )
            except:pass
            
            target = '|'.join( namespaceRoot.split( '|' )[:-1] ) + '|' + localName.replace( namespace+':', '' ) + '*'
            targets = cmds.ls( target, type='transform' )
            
            if len( targets ) == 1:
                target = targets[0]
                addNamespaceToChildren( namespace, target )
                cmds.rename( target, namespaceRoot.split( '|' )[-1] )
            else:
                for target in targets:
                    targetCenter = OpenMaya.MPoint( *getBBCenter( target ) )
                    rootCenter = OpenMaya.MPoint( *rootCenters[i] )
                    
                    if targetCenter.distanceTo( rootCenter ) < 0.0001:
                        addNamespaceToChildren( namespace, target )
                        cmds.rename( target, namespaceRoot.split( '|' )[-1] )


    @staticmethod
    def settingDefault( evt=0 ):

        if not os.path.exists( Window_global.recentInfoPath ): return None
        
        f = open( Window_global.recentInfoPath, 'r' )
        data = json.load( f )
        f.close()
        
        try:
            rootPath = data['rootPath']
            abcPath  = data['abcPath']
            sceneInfoPath = data['sceneInfoPath']
            
            cmds.textField( Window_global.txf_rootPath, e=1, tx=rootPath )
            cmds.textField( Window_global.txf_abcPath, e=1, tx=abcPath )
            cmds.textField( Window_global.txf_sceneInfoPath, e=1, tx=sceneInfoPath )
        except:
            pass




class UI_exportPath:
    
    def __init__(self):
        pass
    
    def create(self):
        
        form = cmds.formLayout()
        tx_rootPath = cmds.text( l='Root Path : ', h=25, w=90, al='right' )
        txf_rootPath = cmds.textField( h=25 )
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
        txf_abcPath = cmds.textField( h=25 )
        tx_sceneInfoPath = cmds.text( l='Scene Info Path : ', h=25, w=90, al='right' )
        txf_sceneInfoPath = cmds.textField( h=25 )
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
        buttonExport = cmds.button( l='Import', h=30, c=Window_cmds.importScene )
        cmds.setParent('..')
        
        cmds.formLayout( form, e=1,
                         af = [( exportPath, 'top', 0 ), ( exportPath, 'left', 0 ), ( exportPath, 'right', 0 ),
                               ( buttonExport, 'left', 0 ), ( buttonExport, 'right', 0 ),
                               ( exportTargets, 'left', 0 ), ( exportTargets, 'right', 0 )],
                         ac = [( buttonExport, 'top', 0, exportTargets ), ( exportTargets, 'top', 0, exportPath )] )
        
        cmds.window( Window_global.name, e=1, wh= Window_global.wh, rtf=1 )
        cmds.showWindow( Window_global.name )
        
        Window_cmds.settingDefault()


def show():
    
    Window().show()



