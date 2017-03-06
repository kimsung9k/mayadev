import maya.cmds as cmds
import sgBFunction_ui
import sgBFunction_value
import sgBFunction_selection
import os
from functools import partial
from maya.OpenMaya import MGlobal




class WinA_Global:
    
    winName = "sgPWindow_object_cam_export"
    title   = "Export Camera"
    width   = 500
    height  = 50
    titleBarMenu = True
    
    txf_export   = ''
    
    fld_startFrame = ''
    fld_endFrame   = ''
    
    import sgBFunction_fileAndPath
    infoFolderPath = sgBFunction_fileAndPath.getLocusCommPackagePrefsPath() + '/sgPWindow_object_export'
    infoFilePath   = sgBFunction_fileAndPath.getLocusCommPackagePrefsPath() + '/sgPWindow_object_export/filePath.txt'
    
    




class WinA_Title:
    
    def __init__(self, label, bgc, h=30 ):
        
        self.label = label
        self.height = h
        self.bgc = bgc


    def create(self):
        
        form = cmds.formLayout( bgc=self.bgc )
        
        text = cmds.text( l= self.label, h=self.height, al='center' )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[( text, 'top', 0 ), ( text, 'left', 0 ), ( text, 'right', 0 )])
        
        self.form = form
        return form





class WinA_ExportPath:
    
    def __init__(self, label, w, h, al ):
        
        self.label  = label
        self.width  = w
        self.height = h
        self.aline  = al


    def create(self):
        
        form = cmds.formLayout()
        
        text = cmds.text( l=self.label, w=self.width, h=self.height, al= self.aline )
        txf  = cmds.textField( h = self.height )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af = [( text, 'top', 0 ), ( text, 'left', 0 ),
                               ( txf,  'top', 0 ), ( txf,  'right', 0 )],
                         ac = [( txf, 'left', 0, text )] )

        WinA_Global.txf_export = txf
        self.form = form
        
        return form





class WinA_TimeRanges:
    
    def __init__(self, label1, label2, w1, w2, h ):
        
        self.label1 = label1
        self.label2 = label2
        self.width1 = w1
        self.width2 = w2
        self.height = h
    
    
    def create(self):
        
        form = cmds.formLayout()
        text1 = cmds.text( l= self.label1, w=self.width1, h=self.height, al='right' )
        text2 = cmds.text( l= self.label2, w=self.width1, h=self.height, al='right' )
        field1 = cmds.intField( w=self.width2, h=self.height )
        field2 = cmds.intField( w=self.width2, h=self.height )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af=[( text1, 'top', 0 ), ( text1, 'left', 0 ),
                             ( text2, 'top', 0 )],
                         ac=[( text1, 'right', 0, field1 ), ( field2, 'left', 0, text2 )],
                         ap=[( field1, 'right', 0, 50 ),( text2, 'left', 0, 50 )] )
        
        WinA_Global.fld_startFrame = field1
        WinA_Global.fld_endFrame   = field2
        
        self.form = form
        return form

    
    
    
    
class WinA_Cmd:
    
    @staticmethod
    def export( *args ):
        
        import sgBFunction_fileAndPath
        import sgBFunction_dag
        
        exportPath = cmds.textField( WinA_Global.txf_export, q=1, tx=1 )
        minFrame = cmds.intField( WinA_Global.fld_startFrame, q=1, v=1 )
        maxFrame = cmds.intField( WinA_Global.fld_endFrame,  q=1, v=1 )

        exportPath = exportPath.replace( '\\', '/' )
        folderPath = '/'.join( exportPath.split( '/' )[-1:] )
        sgBFunction_fileAndPath.makeFolder( folderPath )
        
        sels = cmds.ls( sl=1 )
        cams = []
        for sel in sels:
            selShape = sgBFunction_dag.getShape( sel )
            if cmds.nodeType( selShape ) == 'camera':
                cams.append( sel )
        
        import sgBFunction_scene
        
        sgBFunction_scene.doBake( exportPath, minFrame, maxFrame )
        
        WinA_Cmd.write_windowInfo()
        
        
    
    
    @staticmethod
    def setWindowCondition():
        
        minValue = cmds.playbackOptions( q=1, min=1 )
        maxValue = cmds.playbackOptions( q=1, max=1 )
        cmds.intField( WinA_Global.fld_startFrame, e=1, v=minValue )
        cmds.intField( WinA_Global.fld_endFrame, e=1, v=maxValue )
    
    
    
    @staticmethod
    def read_windowInfo():
        
        import cPickle
        
        try:
            f = open( WinA_Global.infoFilePath, 'r' )
            data = cPickle.load( f )
            f.close()
        except: return None
        
        exportPath = data
        if not exportPath: exportPath = ''
        
        print "export path", exportPath
        cmds.textField( WinA_Global.txf_export, e=1, tx=exportPath )
        
        
        
        
    @staticmethod
    def write_windowInfo():
        
        exportPath = cmds.textField( WinA_Global.txf_export, q=1, tx=1 )
        
        data = exportPath
        
        import cPickle
        import sgBFunction_fileAndPath
        sgBFunction_fileAndPath.makeFolder( WinA_Global.infoFolderPath )
        
        f = open( WinA_Global.infoFilePath, 'w' )
        cPickle.dump( data, f )
        f.close()






class WinA:

    def __init__(self):

        self.uiExportPath = WinA_ExportPath( "Export Path :  ", w=120, h=22, al='right' )
        self.uiTimeRanges = WinA_TimeRanges( "Start Frame : ", "End Frame : ", 120, 50, 22 )


    def create(self):
        
        if cmds.window( WinA_Global.winName, ex=1 ):
            cmds.deleteUI( WinA_Global.winName, wnd=1 )
        cmds.window( WinA_Global.winName, title = WinA_Global.title, titleBarMenu = WinA_Global.titleBarMenu )
        
        form = cmds.formLayout()
        exportPathForm    = self.uiExportPath.create()
        timeRanges        = self.uiTimeRanges.create()
        buttonsForm = cmds.button( l='<<   EXPORT   C A M E R A   >>', bgc=[0.35,0.45,0.8], h=30 )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af = [( exportPathForm, 'top', 8 ), ( exportPathForm, 'left', 0 ), ( exportPathForm, 'right', 5 ),
                               ( timeRanges, 'left', 0 ), ( timeRanges, 'right', 0 ),
                               ( buttonsForm, 'left', 0 ), ( buttonsForm, 'right', 0 ) ],
                         ac = [( timeRanges, 'top', 8, exportPathForm ),
                               ( buttonsForm, 'top', 8, timeRanges )] )

        cmds.window( WinA_Global.winName, e=1,
                     w = WinA_Global.width, h = WinA_Global.height )
        cmds.showWindow( WinA_Global.winName )

        self.button = buttonsForm
        self.setUiCommand()

        WinA_Cmd.read_windowInfo()
        WinA_Cmd.setWindowCondition()


    def setUiCommand(self):
        
        cmds.button( self.button, e=1, c= WinA_Cmd.export )
        
        exportPathPopup = cmds.popupMenu( p=WinA_Global.txf_export )
        sgBFunction_ui.updatePathPopupMenu( WinA_Global.txf_export, exportPathPopup )



mc_showWindow = """import sgPWindow_object_cam_export
sgPWindow_object_cam_export.WinA().create()"""