import maya.cmds as cmds
import sgBFunction_ui
import sgBFunction_value
import sgBFunction_selection
import os
from functools import partial
from maya.OpenMaya import MGlobal



class WinA_Global:
    
    winName = "sgPWindow_data_keyAndCache_export"
    title   = "Export Data Key And Cache Export"
    width   = 500
    height  = 50
    titleBarMenu = True
    
    exportKeyPath_txf     = ''
    exportCachePath_txf   = ''
    
    fld_startFrame = ''
    fld_endFrame   = ''
    
    chk_exportByMatrix = ''
    
    optionMenu = ''
    
    import sgBFunction_fileAndPath
    cacheExportInfoFolder = sgBFunction_fileAndPath.getLocusCommPackagePrefsPath() + '/sgPWindow_data_cache'
    cacheExportInfoFile   = sgBFunction_fileAndPath.getLocusCommPackagePrefsPath() + '/sgPWindow_data_cache/filePath.txt'
    keyExportInfoFolder = sgBFunction_fileAndPath.getLocusCommPackagePrefsPath() + '/sgPWindow_data_key'
    keyExportInfoFile   = sgBFunction_fileAndPath.getLocusCommPackagePrefsPath() + '/sgPWindow_data_key/filePath.txt'
    
    infoPath = sgBFunction_fileAndPath.getLocusCommPackagePrefsPath() + '/sgPWindow_data_keyAndCache_export/info.txt'
    
    



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
        
        self.txf = txf
        WinA_Global.exportPath_form = form
        
        return form





class WinA_ExportType:
    
    def __init__(self, label, type1Label, type2Label, type3Label, **options ):
        
        self.label = label
        self.type1 = type1Label
        self.type2 = type2Label
        self.type3 = type3Label
        self.options = options

    
    def create(self):
        
        form = cmds.formLayout()
        text = cmds.text( l=self.label, **self.options )
        radio = cmds.radioCollection()
        rb1 = cmds.radioButton( l=self.type1, sl=1 )
        rb2 = cmds.radioButton( l=self.type2 )
        rb3 = cmds.radioButton( l=self.type3 )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af=[( text, 'top', 0 ), ( text, 'left', 0 ),
                             ( rb1, 'top', 0 )],
                         ac=[( rb1, 'left', 0, text ),
                             ( rb2, 'left', 0, text ), ( rb2, 'top', 0, rb1  ),
                             ( rb3, 'left', 0, text ), ( rb3, 'top', 0, rb2 )] )
        
        WinA_Global.exportType_radio = radio
        WinA_Global.exportType_form  = form
        
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



class WinA_CacheType:
    
    def __init__(self, label1, label2, label3 ):
        
        self.label1 = label1
        self.label2 = label2
        self.label3 = label3
    
    
    def create(self):
        
        form = cmds.formLayout()
        optionMenu = cmds.optionMenu( l=self.label1 )
        cmds.menuItem( l= self.label2 )
        cmds.menuItem( l= self.label3 )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af = [( optionMenu, 'left', 80 ), ( optionMenu, 'top', 0 )])
        
        WinA_Global.optionMenu = optionMenu
        
        return form





class WinA_ExportByMatrix:
    
    def __init__(self, label, w=1, h=1 ):
        
        self.label = label
        self.width  = w
        self.height = h
    
    
    def create(self):
        
        form = cmds.formLayout()
        checkbox = cmds.checkBox( l= self.label, h= self.height )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af = [( checkbox, 'left', self.width )])
        
        WinA_Global.chk_exportByMatrix = checkbox
        
        self.form = form
        
        return form





class WinA_Buttons:
    
    def __init__(self, label1, label2, h ):
        
        self.label1 = label1
        self.label2 = label2
        self.height = h
    
    
    def create(self):
        
        form = cmds.formLayout()
        button1 = cmds.button( l= self.label1, h=self.height )
        button2 = cmds.button( l= self.label2, h=self.height )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af =[ ( button1, 'top', 0 ), ( button1, 'left', 0 ),
                               ( button2, 'top', 0 ), ( button2, 'right', 0 ) ],
                         ap = [( button1, 'right', 0, 50 ), ( button2, 'left', 0, 50 )])

        return form
    
    
    
    
class WinA_Cmd:
    
    @staticmethod
    def setWindowCondition( *args ):
        
        pass
    
    
    @staticmethod
    def getSplitName():
        
        check = cmds.checkBox( WinA_Global.searchForType_check, q=1, v=1 )
        searchForTypeText = cmds.textField( WinA_Global.searchForType_txf, q=1, tx=1 )
        
        if not check: return ''
        return searchForTypeText
    
    
    @staticmethod
    def read_windowInfo():
        
        import cPickle
        import sgBFunction_fileAndPath
        
        sgBFunction_fileAndPath.makeFile( WinA_Global.keyExportInfoFile, False )
        sgBFunction_fileAndPath.makeFile( WinA_Global.cacheExportInfoFile, False )
        sgBFunction_fileAndPath.makeFile( WinA_Global.infoPath, False )
        
        try:
            f = open( WinA_Global.keyExportInfoFile, 'r' )
            keyExportInfoPath = cPickle.load( f )
            f.close()
            
            cmds.textField( WinA_Global.exportKeyPath_txf, e=1, tx=keyExportInfoPath )
        except:pass
        
        try:
            f = open( WinA_Global.cacheExportInfoFile, 'r' )
            cacheExportInfoPath = cPickle.load( f )
            f.close()
            
            cmds.textField( WinA_Global.exportCachePath_txf, e=1, tx=cacheExportInfoPath )
        except:pass
        
        try:
            f = open( WinA_Global.infoPath, 'r' )
            data = cPickle.load( f )
            f.close()
            
            cacheTypeIndex = data[0]
            exportByMatrix = data[1]
            
            cmds.optionMenu( WinA_Global.optionMenu, e=1, sl=cacheTypeIndex )
            cmds.checkBox( WinA_Global.chk_exportByMatrix , e=1, v=exportByMatrix )
        except: return None
        
        
        
    @staticmethod
    def write_windowInfo():
        
        import cPickle
        
        exportCachePath = cmds.textField( WinA_Global.exportCachePath_txf, q=1, tx=1 )
        exportKeyPath   = cmds.textField( WinA_Global.exportKeyPath_txf, q=1, tx=1 )
        cacheType       = cmds.optionMenu( WinA_Global.optionMenu, q=1, sl=1 )
        exportByMatrix  = cmds.checkBox( WinA_Global.chk_exportByMatrix, q=1, v=1 )
        
        
        f = open( WinA_Global.cacheExportInfoFile, 'w' )
        cPickle.dump( exportCachePath, f )
        f.close()
        
        f = open( WinA_Global.keyExportInfoFile, 'w' )
        cPickle.dump( exportKeyPath, f )
        f.close()
        
        data = [ cacheType, exportByMatrix ]
        
        f = open( WinA_Global.infoPath, 'w' )
        cPickle.dump( data, f )
        f.close()
        
        
    @staticmethod
    def splitStringEnable( *args ):
        
        check = cmds.checkBox( WinA_Global.searchForType_check, q=1, v=1 )
        if check:
            cmds.textField( WinA_Global.searchForType_txf, e=1, en=1 )
        else:
            cmds.textField( WinA_Global.searchForType_txf, e=1, en=0 )
    
    
    @staticmethod
    def export( *args ):

        import sgBExcute_data
        
        WinA_Cmd.write_windowInfo()
        
        keyTargets   = WinA_Global.exportKeyTarget.getFieldTexts()
        cacheTargets = WinA_Global.exportCacheTarget.getFieldTexts() 
        
        keyPath      = cmds.textField( WinA_Global.exportKeyPath_txf, q=1, tx=1 )
        cachePath    = cmds.textField( WinA_Global.exportCachePath_txf, q=1, tx=1 )
        
        startFrame = cmds.intField( WinA_Global.fld_startFrame, q=1, v=1 )
        endFrame   = cmds.intField( WinA_Global.fld_endFrame, q=1, v=1 )
        
        exportByMatrix = cmds.checkBox( WinA_Global.chk_exportByMatrix, q=1, v=1 )
        cacheTypeIndex = cmds.optionMenu( WinA_Global.optionMenu, q=1, sl=1 )-1
        cacheType = ['mcc', 'mcx']
        
        sgBExcute_data.exportKeyAndCacheData(keyTargets, cacheTargets, keyPath, cachePath, startFrame, endFrame, exportByMatrix, cacheType[cacheTypeIndex] )



    @staticmethod
    def setDefaultUICondition( *args ):

        minValue = cmds.playbackOptions( q=1, min=1 )
        maxValue = cmds.playbackOptions( q=1, max=1 )
        cmds.intField( WinA_Global.fld_startFrame, e=1, v=minValue )
        cmds.intField( WinA_Global.fld_endFrame, e=1, v=maxValue )





class WinA:

    def __init__(self):

        self.uiExportKeyTarget   = sgBFunction_ui.PopupFieldUI( "Export Key Targets : ",   'Load Selected', 'multi', position=30 )
        self.uiExportCacheTarget = sgBFunction_ui.PopupFieldUI( "Export Cache Targets : ", 'Load Selected', 'multi', position=30 )

        self.uiExportKeyPath     = WinA_ExportPath( "Export Key Path :  ",   w=120, h=22, al='right' )
        self.uiExportCachePath   = WinA_ExportPath( "Export Cache Path :  ", w=120, h=22, al='right' )
        
        self.uiTimeRanges = WinA_TimeRanges( "Start Frame : ", "End Frame : ", 120, 50, 22 )
        self.uiCacheType  = WinA_CacheType( "Cache Type : ", "mcc", "mcx" )
        self.uiCheckbox   = WinA_ExportByMatrix( "Export by Matrix", 100, 22 )


    def create(self):
        
        if cmds.window( WinA_Global.winName, ex=1 ):
            cmds.deleteUI( WinA_Global.winName, wnd=1 )
        cmds.window( WinA_Global.winName, title = WinA_Global.title, titleBarMenu = WinA_Global.titleBarMenu )
        
        form = cmds.formLayout()
        exportKeyTargetForm = self.uiExportKeyTarget.create()
        exportCacheTargetForm = self.uiExportCacheTarget.create()
        separator1           = cmds.separator()
        exportKeyPathForm   = self.uiExportKeyPath.create()
        exportCachePathForm = self.uiExportCachePath.create()
        timeRanges        = self.uiTimeRanges.create()
        cacheTypes        = self.uiCacheType.create()
        separator2        = cmds.separator()
        checkbox          = self.uiCheckbox.create()
        buttonsForm = cmds.button( l='<<   EXPORT   K E Y    A N D    C A C H E   >>', bgc=[0.55,0.55,0.5], h=30 )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af = [( exportKeyTargetForm, 'top', 8 ), ( exportKeyTargetForm, 'left', 0 ), ( exportKeyTargetForm, 'right', 10 ),
                               ( exportCacheTargetForm, 'left', 0 ), ( exportCacheTargetForm, 'right', 10 ),
                               ( separator1, 'left', 0 ), ( separator1, 'right', 0 ),
                               ( exportKeyPathForm, 'left', 0 ), ( exportKeyPathForm, 'right', 5 ),
                               ( exportCachePathForm, 'left', 0 ), ( exportCachePathForm, 'right', 5 ),
                               ( timeRanges, 'left', 0 ), ( timeRanges, 'right', 0 ),
                               ( cacheTypes, 'left', 0 ), ( cacheTypes, 'right', 0 ),
                               ( separator2, 'left', 0 ), ( separator2, 'right', 0 ),
                               ( checkbox,   'left', 0 ), ( checkbox,   'right', 0 ),
                               ( buttonsForm, 'left', 0 ), ( buttonsForm, 'right', 0 ) ],
                         ac = [( exportCacheTargetForm, 'top', 1, exportKeyTargetForm ),
                               ( separator1, 'top', 8, exportCacheTargetForm ),
                               ( exportKeyPathForm, 'top', 8, separator1 ),
                               ( exportCachePathForm, 'top', 1, exportKeyPathForm ),
                               ( timeRanges, 'top', 8, exportCachePathForm ),
                               ( cacheTypes, 'top', 8, timeRanges ),
                               ( separator2, 'top', 12, cacheTypes ),
                               ( checkbox, 'top', 5, separator2 ),
                               ( buttonsForm, 'top', 8, checkbox )] )

        cmds.window( WinA_Global.winName, e=1,
                     w = WinA_Global.width, h = WinA_Global.height )
        cmds.showWindow( WinA_Global.winName )
        
        WinA_Global.exportKeyPath_txf   = self.uiExportKeyPath.txf
        WinA_Global.exportCachePath_txf = self.uiExportCachePath.txf
        
        WinA_Global.exportKeyTarget     = self.uiExportKeyTarget
        WinA_Global.exportCacheTarget   = self.uiExportCacheTarget
        
        self.button = buttonsForm
        self.setUiCommand()

        WinA_Cmd.read_windowInfo()
        WinA_Cmd.setDefaultUICondition()
        WinA_Cmd.setWindowCondition()


    def setUiCommand(self):
        
        cmds.button( self.button, e=1, c= WinA_Cmd.export )
        
        exportKeyPathPopup = cmds.popupMenu( p=WinA_Global.exportKeyPath_txf )
        sgBFunction_ui.updatePathPopupMenu( WinA_Global.exportKeyPath_txf, exportKeyPathPopup )
        
        exportCachePathPopup = cmds.popupMenu( p=WinA_Global.exportCachePath_txf )
        sgBFunction_ui.updatePathPopupMenu( WinA_Global.exportCachePath_txf, exportCachePathPopup )



mc_showWindow = """import sgPWindow_data_keyAndCache_export
sgPWindow_data_keyAndCache_export.WinA().create()"""