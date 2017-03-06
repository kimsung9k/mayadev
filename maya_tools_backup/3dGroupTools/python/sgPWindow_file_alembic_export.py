import maya.cmds as cmds
import sgBFunction_ui
import sgBFunction_value
import sgBFunction_selection
import os
from functools import partial
from maya.OpenMaya import MGlobal
import sgBModel_sgPWindow
import sgBModel_editUi



class WinA_Global:
    
    winName = 'sgPWindow_file_cache_export'
    title   = "Alembic Export"
    width   = 500
    height  = 50
    titleBarMenu = True
    
    exportPath_txf   = ''
    exportType_radio = ''
    searchFor_txf    = ''
    
    searchFor_txf  = ''
    
    searchForType_radio = ''
    searchForType_check = ''
    searchForType_txf   = ''
    
    fld_startFrame = ''
    fld_endFrame   = ''
    fld_step = ''
    
    optionMenu = ''
    
    import sgBFunction_fileAndPath
    pathInfo = sgBFunction_fileAndPath.getPathInfo_sgPWindow_file_alembic()



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
        
        WinA_Global.exportPath_txf  = txf
        WinA_Global.exportPath_form = form
        
        return form





class WinA_ExportType:
    
    def __init__(self, label, type1Label, type2Label, **options ):
        
        self.label = label
        self.type1 = type1Label
        self.type2 = type2Label
        self.options = options

    
    def create(self):
        
        form = cmds.formLayout()
        text = cmds.text( l=self.label, **self.options )
        radio = cmds.radioCollection()
        rb1 = cmds.radioButton( l=self.type1, sl=1 )
        rb2 = cmds.radioButton( l=self.type2 )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af=[( text, 'top', 0 ), ( text, 'left', 0 ),
                             ( rb1, 'top', 0 )],
                         ac=[( rb1, 'left', 0, text ),
                             ( rb2, 'left', 0, text ), ( rb2, 'top', 0, rb1  )] )
        
        WinA_Global.exportType_radio = radio
        WinA_Global.exportType_form  = form
        
        return form




class WinA_TimeRanges:
    
    def __init__(self, label1, label2, label3, w1, w2, h ):
        
        self.label1 = label1
        self.label2 = label2
        self.label3 = label3
        self.width1 = w1
        self.width2 = w2
        self.height = h
    
    
    def create(self):
        
        form = cmds.formLayout()
        text1 = cmds.text( l= self.label1, w=self.width1, h=self.height, al='right' )
        text2 = cmds.text( l= self.label2, w=self.width1, h=self.height, al='right' )
        text3 = cmds.text( l= self.label3, w=self.width1-10, h=self.height, al='right' )
        field1 = cmds.floatField( w=self.width2, h=self.height, step=0.25, pre=2 )
        field2 = cmds.floatField( w=self.width2, h=self.height, step=0.25, pre=2 )
        field3 = cmds.floatField( w=self.width2, h=self.height, step=0.25, pre=2, v=1 )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af=[( text1, 'top', 0 ), ( text1, 'left', 0 ),
                             ( text2, 'top', 0 ), 
                             ( text3, 'top', 0 )],
                         ac=[( field1, 'left', 0, text1 ), ( text2, 'left', 0, field1 ),
                             ( field2, 'left', 0, text2 ), ( text3, 'left', 0, field2 ),
                             ( field3, 'left', 0, text3 )])
        
        WinA_Global.fld_startFrame = field1
        WinA_Global.fld_endFrame   = field2
        WinA_Global.fld_step       = field3
        
        self.form = form
        return form

    
    
    
class WinA_Cmd:
    
    @staticmethod
    def setExportPath( *args ):
        
        import sgBModel_aniScene
        
        projectName, cutNumberFolderIndex, addPath = sgBModel_aniScene.exportAlembicPathFromAni
        sceneName = cmds.file( q=1, sceneName=1 )
        
        sceneNameSplits = sceneName.split( '/' )
        if not projectName in sceneNameSplits: return None
        
        projectIndex = sceneNameSplits.index( projectName )
        cutName      = sceneNameSplits[ projectIndex + cutNumberFolderIndex ]
        
        exportPath = '/'.join( sceneNameSplits[:projectIndex+1] ) + addPath + '/' + cutName + '/cache/master'
        
        localExportPath = 'D:' + exportPath[2:]
        
        cmds.textField( WinA_Global.exportPath_txf, e=1, tx=localExportPath )


    @staticmethod
    def setFrameRange( *args ):
        
        minValue = cmds.playbackOptions( q=1, min=1 )
        maxValue = cmds.playbackOptions( q=1, max=1 )
        cmds.floatField( WinA_Global.fld_startFrame, e=1, v=minValue )
        cmds.floatField( WinA_Global.fld_endFrame, e=1, v=maxValue )
    
    
    @staticmethod
    def getExportType():

        items = cmds.radioCollection( WinA_Global.exportType_radio, q=1, cia=1 )
        
        for i in range( len( items ) ):
            if cmds.radioButton( items[i], q=1, sl=1 ):
                break
        return i
        
    
    @staticmethod
    def export( *args ):

        import sgBExcute_data
        import sgBFunction_fileAndPath
        import sgBFunction_scene
        import sgBFunction_base
        import cPickle
        
        sgBFunction_base.autoLoadPlugin( 'AbcExport' )
        sgBFunction_base.autoLoadPlugin( 'AbcImport' )
        
        path = cmds.textField( WinA_Global.exportPath_txf, q=1, tx=1 )
        
        sgBFunction_fileAndPath.makeFile( WinA_Global.pathInfo, False )
        f = open( WinA_Global.pathInfo, 'w' )
        cPickle.dump( path, f )
        f.close()
        
        if not os.path.exists( path ):
            try:
                sgBFunction_fileAndPath.makeFolder( path ) 
            except:
                cmds.error( '"%s" is not exist path' % path )
                return None
        
        if not os.path.isdir( path ):
            cmds.error( '"%s" is not Directory' % path )
            return None

        path = cmds.textField( WinA_Global.exportPath_txf, q=1, tx=1 )
        startFrame = cmds.floatField( WinA_Global.fld_startFrame, q=1, v=1 )
        endFrame   = cmds.floatField( WinA_Global.fld_endFrame, q=1, v=1 )
        step       = cmds.floatField( WinA_Global.fld_step, q=1, v=1 )
        exportType = WinA_Cmd.getExportType()
        if exportType == 0: exportTargets = cmds.ls( sl=1 )
        elif exportType == 1:
            exportTargets = []
            for tr in cmds.ls( tr=1 ):
                if cmds.listRelatives( tr, p=1 ): continue
                exportTargets.append( tr )
        
        if not exportTargets:
            cmds.error( 'Target is not exists' )
        else:
            sgBExcute_data.exportAlembicData( sgBFunction_scene.getCutNumber(), exportTargets, startFrame, endFrame, step, path )





class WinA:

    def __init__(self):

        self.uiExportPath = WinA_ExportPath( "Export Path :  ", w=120, h=22, al='right' )
        self.uiExportType = WinA_ExportType( "Export Type :  ", 
                                             "Export Selection", "Export All ", w=120, h=22, al='right' )
        self.uiTimeRanges = WinA_TimeRanges( "Start Frame : ", "End Frame : ", "step : ", 100, 50, 22 )


    def create(self):
        
        if cmds.window( WinA_Global.winName, ex=1 ):
            cmds.deleteUI( WinA_Global.winName, wnd=1 )
        cmds.window( WinA_Global.winName, title = WinA_Global.title, titleBarMenu = WinA_Global.titleBarMenu )
        
        form = cmds.formLayout()
        exportPathForm    = self.uiExportPath.create()
        exportTypeForm    = self.uiExportType.create()
        timeRanges        = self.uiTimeRanges.create()
        buttonsForm = cmds.button( l='<<   EXPORT   A L E M B I C   >>', bgc=[0.85,0.85,0.45], h=30,
                     c = WinA_Cmd.export )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af = [( exportPathForm, 'top', 8 ), ( exportPathForm, 'left', 0 ), ( exportPathForm, 'right', 5 ),
                               ( exportTypeForm, 'left',0 ), ( exportTypeForm, 'right', 0 ),
                               ( timeRanges, 'left', 0 ), ( timeRanges, 'right', 0 ),
                               ( buttonsForm, 'left', 0 ), ( buttonsForm, 'right', 0 ) ],
                         ac = [( exportTypeForm, 'top', 8, exportPathForm ),
                               ( timeRanges, 'top', 8, exportTypeForm ),
                               ( buttonsForm, 'top', 8, timeRanges )] )

        cmds.window( WinA_Global.winName, e=1,
                     w = WinA_Global.width, h = WinA_Global.height )
        cmds.showWindow( WinA_Global.winName )

        self.button = buttonsForm
        
        WinA_Cmd.setFrameRange()
        WinA_Cmd.setExportPath()
        popupMenu = cmds.popupMenu( p= WinA_Global.exportPath_txf )
        sgBFunction_ui.updatePathPopupMenu( WinA_Global.exportPath_txf, popupMenu )
