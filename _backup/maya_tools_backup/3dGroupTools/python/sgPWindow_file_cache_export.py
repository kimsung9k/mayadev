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
    
    winName = sgBModel_sgPWindow.sgPWindow_file_cache_export_winName
    title   = "Export Cache"
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
    
    om_cacheType = ''
    om_pointsSpace = ''
    
    import sgBFunction_fileAndPath
    pathInfo = sgBFunction_fileAndPath.getPathInfo_sgPWindow_file_cache()
    uiInfo = sgBFunction_fileAndPath.getUiInfo_sgPWindow_file_cache()
    
    sgBModel_editUi.targetWindowsClose_whenSceneUpdate.append( winName )
    
    



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





class WinA_searchFor:
    
    def __init__(self, label, w1, w2, h, al ):
        
        self.label  = label
        self.width1 = w1
        self.width2 = w2
        self.height = h
        self.aline  = al
        

    def create(self):
        
        form = cmds.formLayout()
        text = cmds.text( l=self.label, w=self.width1, h=self.height, al = self.aline )
        txf  = cmds.textField( w= self.width2, h = self.height )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af = [( text, 'top', 0 ), ( text, 'left', 0 ),
                               ( txf,  'top', 0 )],
                         ac = [( txf, 'left', 0, text )] )
        
        WinA_Global.searchFor_txf  = txf
        WinA_Global.searchFor_form = form
        
        return form


class WinA_searchForType:
    
    def __init__(self, label, rbLabel1, rbLabel2, rbLabel3, rbLabel4, 
                       w1, w2, w3, w4, h, al ):
        
        self.label = label
        self.rbLabel1 = rbLabel1
        self.rbLabel2 = rbLabel2
        self.rbLabel3 = rbLabel3
        self.rbLabel4 = rbLabel4
        self.width1 = w1
        self.width2 = w2
        self.width3 = w3
        self.width4 = w4
        self.height = h
        self.aline  = al
        
    
    def create(self):
        
        form = cmds.formLayout()
        text = cmds.text( l= self.label, w=self.width1, h=self.height, al= self.aline )
        radio = cmds.radioCollection()
        rb1  = cmds.radioButton( l=self.rbLabel1, w=self.width2, sl=1 )
        rb2  = cmds.radioButton( l=self.rbLabel2, w=self.width3 )
        rb3  = cmds.radioButton( l=self.rbLabel3, w=self.width4 )
        check = cmds.checkBox( l=self.rbLabel4 )
        txf  = cmds.textField( en=0 )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af = [( text, 'top', 0 ),( text, 'left', 0 ),
                               ( rb1, 'top', 0 ), ( rb2, 'top', 0 ), ( rb3, 'top', 0 )],
                         ac = [( rb1, 'left', 0, text ), ( rb2, 'left', 0, rb1 ), ( rb3, 'left', 0, rb2 ),
                               ( check, 'top', 0, text ), ( check, 'left', 0, text ),
                               ( txf, 'top', 0, text ), ( txf, 'left', 0, check )] )
        
        WinA_Global.searchForType_radio = radio
        WinA_Global.searchForType_check = check
        WinA_Global.searchForType_txf   = txf
        WinA_Global.searchForType_form  = form
        
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



class WinA_type:
    
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
        
        self.optionMenu = optionMenu
        
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
        
        i = WinA_Cmd.getExportType()
        
        if i == 0: enable = False 
        else: enable = True
        cmds.formLayout( WinA_Global.searchFor_form, e=1, en=enable )
        cmds.formLayout( WinA_Global.searchFor_form, e=1, en=enable )
        cmds.formLayout( WinA_Global.searchForType_form, e=1, en=enable )
        
        check = cmds.checkBox( WinA_Global.searchForType_check, q=1, v=1 )
        if check: enbale = True
        else: enable = False
        cmds.textField( WinA_Global.searchForType_txf, e=1, en= enable )

    
    @staticmethod
    def getExportType():

        items = cmds.radioCollection( WinA_Global.exportType_radio, q=1, cia=1 )
        
        for i in range( len( items ) ):
            if cmds.radioButton( items[i], q=1, sl=1 ):
                break
        return i
    
    
    @staticmethod
    def getSearchForType():
        
        items = cmds.radioCollection( WinA_Global.searchForType_radio, q=1, cia=1 )
        for i in range( len( items ) ):
            if cmds.radioButton( items[i], q=1, sl=1 ):
                break
        return i
    
    
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
        
        if not os.path.exists( WinA_Global.uiInfo ):
            sgBFunction_fileAndPath.makeFile( WinA_Global.uiInfo, False )
        try:
            f = open( WinA_Global.uiInfo, 'r' )
            data = cPickle.load( f )
            f.close()
            
            exportPath, exportType, searchFor, searchForType, splitStringAndSerchCheck, splitStringAndSearchString, cacheType, pointsSpace = data
        except:
            sgBFunction_fileAndPath.makeFile( WinA_Global.uiInfo, False )
        
            exportPath = ''
            exportType = 'Export By Selection'
            searchFor  = ''
            searchForType = 'Ani position'
            splitStringAndSerchCheck = False
            splitStringAndSearchString = ''
            cacheType = 1
            pointsSpace = 1
        
        import sgBModel_aniScene
        
        upFolderNum, addPath = sgBModel_aniScene.exportCachePathFromAni
        sceneName = cmds.file( q=1, sceneName=1 )
        sceneFolder = '/'.join( sceneName.split( '/' )[:-1+upFolderNum] )
        exportPath = sceneFolder + addPath
        
        cmds.textField( WinA_Global.exportPath_txf, e=1, tx= exportPath )
        cmds.textField( WinA_Global.searchFor_txf, e=1, tx=searchFor )
        cmds.checkBox( WinA_Global.searchForType_check, e=1, v=splitStringAndSerchCheck )
        cmds.textField( WinA_Global.searchForType_txf, e=1, tx=splitStringAndSearchString )
        cmds.optionMenu( WinA_Global.om_cacheType, e=1, sl=cacheType )
        cmds.optionMenu( WinA_Global.om_pointsSpace, e=1, sl=pointsSpace )

    @staticmethod
    def write_windowInfo():
        
        exportPath = cmds.textField( WinA_Global.exportPath_txf, q=1, tx=1 )
        exportType = WinA_Cmd.getExportType()
        searchFor = cmds.textField( WinA_Global.searchFor_txf, q=1, tx=1 )
        searchForType = WinA_Cmd.getSearchForType()
        splitStringAndSearchCheck = cmds.checkBox( WinA_Global.searchForType_check, q=1, v=1 )
        splitStringAndSearchString = cmds.textField( WinA_Global.searchForType_txf, q=1, tx=1 )
        cacheType = cmds.optionMenu( WinA_Global.om_cacheType, q=1, sl=1 )
        pointsSpace = cmds.optionMenu( WinA_Global.om_pointsSpace, q=1, sl=1 )
        
        data = [ exportPath, exportType, searchFor, searchForType, splitStringAndSearchCheck, splitStringAndSearchString, cacheType, pointsSpace ]
        
        import cPickle
        import sgBFunction_fileAndPath
        sgBFunction_fileAndPath.makeFile( WinA_Global.pathInfo, False )
        f = open( WinA_Global.uiInfo, 'w' )
        cPickle.dump( data, f )
        f.close()
        
        f = open( WinA_Global.pathInfo, 'w' )
        cPickle.dump( exportPath, f )
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
        import sgBFunction_fileAndPath
        
        WinA_Cmd.write_windowInfo()
        path = cmds.textField( WinA_Global.exportPath_txf, q=1, tx=1 )
        
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
        exportTargets = sgBFunction_selection.getDeformedObjectsFromGroup( WinA_Cmd.getExportTargets() )
        cacheTypeIndex = cmds.optionMenu( WinA_Global.om_cacheType, q=1, sl=1 )-1
        pointsSpaceIndex = cmds.optionMenu( WinA_Global.om_pointsSpace, q=1, sl=1 )-1
        
        cacheType = ['mcc', 'mcx']
        pointsSpace = ['world', 'local']
        
        if not exportTargets:
            cmds.error( 'Target is not exists' )
        else:
            sgBExcute_data.exportCacheData( exportTargets, startFrame, endFrame, step, path, cacheType[cacheTypeIndex], pointsSpace[pointsSpaceIndex] )


    @staticmethod
    def getExportTargets( *args ):
        
        exportTargets = []
        
        def searchIsRight( tr, searchForType, searchFor, splitName ):
            if splitName: compairTr = tr.split( splitName )[-1]
            else: compairTr = tr
            if searchForType == 0 and compairTr.find( searchFor ) != -1:
                return True
            elif searchForType == 1 and compairTr[ :len(searchFor) ] == searchFor:
                return True
            elif searchForType == 2 and compairTr[ -len( searchFor ): ] == searchFor:
                return True
                
        exportType = WinA_Cmd.getExportType()
        if exportType == 0:
            meshObjs = sgBFunction_selection.getTransformNodesFromGroup( cmds.ls( sl=1 ) )
            for meshObj in meshObjs:
                meshObj = cmds.ls( meshObj )[0]
                exportTargets.append( meshObj )
                
        elif exportType == 1:
            searchFor = cmds.textField( WinA_Global.searchFor_txf, q=1, tx=1 )
            searchForType = WinA_Cmd.getSearchForType()
            splitName = WinA_Cmd.getSplitName()
            if not searchFor: cmds.error( "Check Search For String" )
            
            targets = []
            for tr in cmds.ls( tr=1 ):
                if searchIsRight( tr, searchForType, searchFor, splitName ):
                    targets.append( tr )
            meshObjs = sgBFunction_selection.getTransformNodesFromGroup( targets )
            for meshObj in meshObjs:
                meshObj = cmds.ls( meshObj )[0]
                exportTargets.append( meshObj )
                
        elif exportType == 2:
            searchFor = cmds.textField( WinA_Global.searchFor_txf, q=1, tx=1 )
            searchForType = WinA_Cmd.getSearchForType()
            splitName = WinA_Cmd.getSplitName()
            if not searchFor: cmds.error( "Check Search For String" )
            
            targets = []
            trChildren = cmds.listRelatives( cmds.ls( sl=1 ), c=1, ad=1, f=1, type='transform' )
            trChildren += cmds.ls( sl=1 )
            for tr in trChildren:
                if searchIsRight( tr, searchForType, searchFor, splitName ):
                    targets.append( tr )
                
            meshObjs = sgBFunction_selection.getMeshObjectFromGroup( targets )
            for meshObj in meshObjs:
                meshObj = cmds.ls( meshObj )[0]
                exportTargets.append( meshObj )
            
        return exportTargets

    @staticmethod
    def setDefaultUICondition( *args ):

        minValue = cmds.playbackOptions( q=1, min=1 )
        maxValue = cmds.playbackOptions( q=1, max=1 )
        cmds.floatField( WinA_Global.fld_startFrame, e=1, v=minValue )
        cmds.floatField( WinA_Global.fld_endFrame, e=1, v=maxValue )





class WinA:

    def __init__(self):

        self.uiExportPath = WinA_ExportPath( "Export Path :  ", w=120, h=22, al='right' )
        self.uiExportType = WinA_ExportType( "Export Type :  ", 
                                             "Export By Selection", "Export By Name ", "Export By Name And Selection",
                                             w=120, h=22, al='right' )
        self.uisearchFor  = WinA_searchFor( "Search For : ", w1= 120, w2=150, h=21, al='right' )
        self.uisearchForType = WinA_searchForType( "Search For Type : ", "Any position", "Start position", "End Position", 
                                                   "Split String and Search :",
                                                    w1= 120, w2=110, w3=110, w4=110, h=22, al='right' )
        self.uiTimeRanges = WinA_TimeRanges( "Start Frame : ", "End Frame : ", "step : ", 100, 50, 22 )
        self.uiCacheType    = WinA_type( "  Cache Type : ", "mcc", "mcx" )
        self.uiPointsSpace  = WinA_type( "Points Space : ", "World", "Local" )
        self.uiButtons    = WinA_Buttons( "Export", "Close", 30 )


    def create(self):
        
        if cmds.window( WinA_Global.winName, ex=1 ):
            cmds.deleteUI( WinA_Global.winName, wnd=1 )
        cmds.window( WinA_Global.winName, title = WinA_Global.title, titleBarMenu = WinA_Global.titleBarMenu )
        
        form = cmds.formLayout()
        exportPathForm    = self.uiExportPath.create()
        exportTypeForm    = self.uiExportType.create()
        searchForForm     = self.uisearchFor.create()
        searchForTypeForm = self.uisearchForType.create()
        timeRanges        = self.uiTimeRanges.create()
        cacheTypes        = self.uiCacheType.create()
        pointsSpace       = self.uiPointsSpace.create()
        buttonsForm = cmds.button( l='<<   EXPORT   C A C H E   >>', bgc=[0.5,0.6,0.5], h=30 )
        cmds.setParent( '..' )
        
        WinA_Global.om_cacheType = self.uiCacheType.optionMenu
        WinA_Global.om_pointsSpace = self.uiPointsSpace.optionMenu
        
        cmds.formLayout( form, e=1,
                         af = [( exportPathForm, 'top', 8 ), ( exportPathForm, 'left', 0 ), ( exportPathForm, 'right', 5 ),
                               ( exportTypeForm, 'left',0 ), ( exportTypeForm, 'right', 0 ),
                               ( searchForForm, 'left', 0 ),
                               ( searchForTypeForm, 'left', 0 ),
                               ( timeRanges, 'left', 0 ), ( timeRanges, 'right', 0 ),
                               ( cacheTypes, 'left', 0 ), ( cacheTypes, 'right', 0 ),
                               ( pointsSpace, 'left', 0 ), ( pointsSpace, 'right', 0 ),
                               ( buttonsForm, 'left', 0 ), ( buttonsForm, 'right', 0 ) ],
                         ac = [( exportTypeForm, 'top', 8, exportPathForm ),
                               ( searchForForm, 'top', 8, exportTypeForm ),
                               ( searchForTypeForm, 'top', 8, searchForForm ),
                               ( timeRanges, 'top', 8, searchForTypeForm ),
                               ( cacheTypes, 'top', 8, timeRanges ),
                               ( pointsSpace, 'top', 8, cacheTypes ),
                               ( buttonsForm, 'top', 12, pointsSpace )] )

        cmds.window( WinA_Global.winName, e=1,
                     w = WinA_Global.width, h = WinA_Global.height )
        cmds.showWindow( WinA_Global.winName )

        self.button = buttonsForm
        self.setUiCommand()

        WinA_Cmd.read_windowInfo()
        WinA_Cmd.setDefaultUICondition()
        WinA_Cmd.setWindowCondition()


    def setUiCommand(self):
        
        cmds.button( self.button, e=1, c= WinA_Cmd.export )
        
        items = cmds.radioCollection( WinA_Global.exportType_radio, q=1, cia=1 )
        for item in items:
            cmds.radioButton( item, e=1, cc= WinA_Cmd.setWindowCondition )
        
        cmds.checkBox( WinA_Global.searchForType_check, e=1, cc= WinA_Cmd.splitStringEnable )
        
        exportPathPopup = cmds.popupMenu( p=WinA_Global.exportPath_txf )
        sgBFunction_ui.updatePathPopupMenu( WinA_Global.exportPath_txf, exportPathPopup )



mc_showWindow = """import sgPWindow_file_cache_export
sgPWindow_file_cache_export.WinA().create()"""