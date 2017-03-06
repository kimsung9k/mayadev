import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
from PySide import QtGui
import os
from pymel.core import nodetypes
import shiboken
import maya.OpenMayaUI


def exportAlembic( exportRoot, minFrame, maxFrame, targetFilePath ):
    
    def getCurrentModelPanels():
        pannels = cmds.getPanel( vis=1 )
        modelPanels = []
        for pannel in pannels:
            if cmds.modelPanel( pannel, ex=1 ):
                modelPanels.append( pannel )
        return modelPanels
    
    pannels = getCurrentModelPanels()
    
    cmds.select( exportRoot )
    for pannel in pannels:
        cmds.isolateSelect( pannel, state=1 )
    
    cmds.AbcExport( j="-frameRange %d %d -noNormals -ro -uvWrite -wholeFrameGeo -writeVisibility -eulerFilter"\
                " -dataFormat ogawa -root %s -file %s" %( minFrame, maxFrame, exportRoot, targetFilePath ) )
    
    for pannel in pannels:
        cmds.isolateSelect( pannel, state=0 )



class Window_global:
    
    name = "sgSceneExport"
    title = "UI - Scene Export"
    wh = [430,20]
    
    folderIconPath = os.path.dirname( __file__ ) + '/icon/folder.png'
    form_exportTarget = ''
    scriptJopIndex = None
    
    mayaWin = shiboken.wrapInstance( long( maya.OpenMayaUI.MQtUtil.mainWindow() ), QtGui.QWidget )
    txf_rootPath = ''

    @staticmethod
    def getDefaultFolder():
        sceneLocalName = cmds.file( q=1, sceneName=1 ).split( '/' )[-1].split( '.' )[0]
        return os.path.dirname( cmds.file( q=1, sceneName=1 ) ) + '/' + sceneLocalName
    
    
    

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
    def updateBySelection( evt=0 ):

        camAndGeos = Window_cmds.getCamAndGeos()
        if not camAndGeos: return None
        
        afs = []
        acs = []
        
        children = cmds.formLayout( Window_global.form_exportTarget, q=1, childArray=1 )
        if children:
            for child in children:
                cmds.deleteUI( child )
        
        isFirst = True
        tx_before = None
        
        for i in range( len( camAndGeos ) ):
            camAndGeo = camAndGeos[i].split( '|' )[-1]
            extension = 'abc'
            
            tx_target  = cmds.text( l="Target geometry : ", h=25, w=100, al='right', p=Window_global.form_exportTarget )
            txf_target = cmds.textField( p=Window_global.form_exportTarget, h=25, tx='/%s.%s' % ( camAndGeo.replace( ':', '_' ), extension ) )
            if isFirst:
                afs += [ (tx_target, 'top', 5), (txf_target, 'top', 5 ) ]
                isFirst = False
            else:
                acs += [ (tx_target, 'top', 5, tx_before), (txf_target, 'top', 5, tx_before) ]
            tx_before = tx_target
            afs += [ (tx_target, 'left', 5), (txf_target, 'right', 15 ) ]
            acs += [ (txf_target, 'left', 5, tx_target ) ]

        try:
            afs += [(tx_target, 'bottom', 5), (txf_target, 'bottom', 5)]
            cmds.formLayout( Window_global.form_exportTarget, e=1, af = afs, ac = acs )
        except:pass
    

    
    @staticmethod
    def getDirectory( evt=0 ):
    
        dialog = QtGui.QFileDialog(Window_global.mayaWin )
        dialog.setDirectory( Window_global.getDefaultFolder() )
        choosedFolder = dialog.getExistingDirectory()
        if not choosedFolder: choosedFolder = Window_global.getDefaultFolder()
        cmds.textField( Window_global.txf_rootPath, e=1, tx=choosedFolder )
    


    @staticmethod
    def export( evt=0 ):
        
        rootPath = cmds.textField( Window_global.txf_rootPath, q=1, tx=1 )
        children = cmds.formLayout( Window_global.form_exportTarget, q=1, childArray=1 )
        
        camAndGeos = Window_cmds.getCamAndGeos()
        
        for i in range( 0, len( children ), 2 ):
            otherPath = cmds.textField( children[i+1], q=1, tx=1 )
            targetFilePath = rootPath + otherPath
            minFrame = cmds.playbackOptions( q=1, min=1 )
            maxFrame = cmds.playbackOptions( q=1, max=1 )
            exportAlembic(camAndGeos[(i+1)/2], minFrame, maxFrame, targetFilePath)



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
        cmds.setParent( '..' )
        
        Window_global.form_exportTarget = form
        
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
        cmds.scriptJob( e=['SelectionChanged', Window_cmds.updateBySelection ], parent = Window_global.name )
        
        form = cmds.formLayout()
        exportPath = self._ui_exportPath.create()
        exportTargets = self._ui_exportTargets.create()
        buttonExport = cmds.button( l='Export', h=30, c=Window_cmds.export )
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


