import maya.cmds as cmds
import sgBFunction_ui
import sgBFunction_value
import sgBFunction_selection
import os
from functools import partial
from maya.OpenMaya import MGlobal



class WinA_Global:
    
    winName = "sgExportMeshGroup"
    title   = "Export Mesh Group"
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
    
    import sgBFunction_fileAndPath
    infoFolderPath = sgBFunction_fileAndPath.getLocusCommPackagePrefsPath() + '/sgPWindow_data_mesh_exportGroup'
    infoPathPath= sgBFunction_fileAndPath.getLocusCommPackagePrefsPath() + '/sgPWindow_data_mesh_group/filePath.txt'
    infoPath = sgBFunction_fileAndPath.getLocusCommPackagePrefsPath() + '/sgPWindow_data_mesh_exportGroup/info.txt'
    



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
        
        if not os.path.exists( WinA_Global.infoPath ):
            sgBFunction_fileAndPath.makeFile( WinA_Global.infoPath )
            sgBFunction_fileAndPath.makeFile( WinA_Global.infoPathPath )
        try:
            f = open( WinA_Global.infoPath, 'r' )
            data = cPickle.load( f )
            f.close()
        except: return None
        
        if not data: return None
        
        try:exportPath, exportType, searchFor, searchForType, splitStringAndSerchCheck, splitStringAndSearchString = data
        except: return None
        
        cmds.textField( WinA_Global.exportPath_txf, e=1, tx= exportPath )
        items = cmds.radioCollection( WinA_Global.exportType_radio, q=1, cia=1 )
        cmds.radioButton( items[ exportType ], e=1, sl=1 )
        cmds.textField( WinA_Global.searchFor_txf, e=1, tx=searchFor )
        items = cmds.radioCollection( WinA_Global.searchForType_radio, q=1, cia=1 )
        cmds.radioButton( items[ searchForType ], e=1, sl=1 )
        cmds.checkBox( WinA_Global.searchForType_check, e=1, v=splitStringAndSerchCheck )
        cmds.textField( WinA_Global.searchForType_txf, e=1, tx=splitStringAndSearchString )
        
    @staticmethod
    def write_windowInfo():
        
        exportPath = cmds.textField( WinA_Global.exportPath_txf, q=1, tx=1 )
        exportType = WinA_Cmd.getExportType()
        searchFor = cmds.textField( WinA_Global.searchFor_txf, q=1, tx=1 )
        searchForType = WinA_Cmd.getSearchForType()
        splitStringAndSearchCheck = cmds.checkBox( WinA_Global.searchForType_check, q=1, v=1 )
        splitStringAndSearchString = cmds.textField( WinA_Global.searchForType_txf, q=1, tx=1 )
        
        data = [ exportPath, exportType, searchFor, searchForType, splitStringAndSearchCheck, splitStringAndSearchString ]
        
        import cPickle
        import sgBFunction_fileAndPath
        sgBFunction_fileAndPath.makeFolder( WinA_Global.infoFolderPath )
        sgBFunction_fileAndPath.makeFile( WinA_Global.infoPathPath, False )
        
        f = open( WinA_Global.infoPath, 'w' )
        cPickle.dump( data, f )
        f.close()
        
        f = open( WinA_Global.infoPathPath, 'w' )
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
                print "try make folder : ", path
                sgBFunction_fileAndPath.makeFolder( path ) 
            except:
                cmds.error( '"%s" is not exist path' % path )
                return None
        
        if not os.path.isdir( path ):
            cmds.error( '"%s" is not Directory' % path )
            return None

        path = cmds.textField( WinA_Global.exportPath_txf, q=1, tx=1 )
        sgBExcute_data.exportSgMeshDatas( WinA_Cmd.getExportTargets(), path )
        


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
            meshObjs = sgBFunction_selection.getMeshObjectFromGroup( cmds.ls( sl=1 ) )
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
            meshObjs = sgBFunction_selection.getMeshObjectFromGroup( targets )
            for meshObj in meshObjs:
                meshObj = cmds.ls( meshObj )[0]
                exportTargets.append( meshObj )
                
        elif exportType == 2:
            searchFor = cmds.textField( WinA_Global.searchFor_txf, q=1, tx=1 )
            searchForType = WinA_Cmd.getSearchForType()
            splitName = WinA_Cmd.getSplitName()
            if not searchFor: cmds.error( "Check Search For String" )
            
            targets = []
            if splitName:
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
        self.uiButtons    = WinA_Buttons( "Export", "Close", 30 )


    def create(self):
        
        if cmds.window( WinA_Global.winName, ex=1 ):
            cmds.deleteUI( WinA_Global.winName, wnd=1 )
        cmds.window( WinA_Global.winName, title = WinA_Global.title, titleBarMenu = WinA_Global.titleBarMenu )
        
        form = cmds.formLayout()
        exportPathForm = self.uiExportPath.create()
        exportTypeForm = self.uiExportType.create()
        searchForForm  = self.uisearchFor.create()
        searchForTypeForm = self.uisearchForType.create()
        buttonsForm = cmds.button( l='<<   EXPORT   M E S H   >>', bgc=[0.5,0.5,0.6], h=30 )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af = [( exportPathForm, 'top', 8 ), ( exportPathForm, 'left', 0 ), ( exportPathForm, 'right', 5 ),
                               ( exportTypeForm, 'left',0 ), ( exportTypeForm, 'right', 0 ),
                               ( searchForForm, 'left', 0 ),
                               ( searchForTypeForm, 'left', 0 ),
                               ( buttonsForm, 'left', 0 ), ( buttonsForm, 'right', 0 ) ],
                         ac = [( exportTypeForm, 'top', 8, exportPathForm ),
                               ( searchForForm, 'top', 8, exportTypeForm ),
                               ( searchForTypeForm, 'top', 8, searchForForm ),
                               ( buttonsForm, 'top', 12, searchForTypeForm )] )

        cmds.window( WinA_Global.winName, e=1,
                     w = WinA_Global.width, h = WinA_Global.height )
        cmds.showWindow( WinA_Global.winName )

        self.button = buttonsForm
        self.setUiCommand()

        WinA_Cmd.read_windowInfo()
        WinA_Cmd.setWindowCondition()



    def setUiCommand(self):
        
        cmds.button( self.button, e=1, c= WinA_Cmd.export )
        
        items = cmds.radioCollection( WinA_Global.exportType_radio, q=1, cia=1 )
        for item in items:
            cmds.radioButton( item, e=1, cc= WinA_Cmd.setWindowCondition )
        
        cmds.checkBox( WinA_Global.searchForType_check, e=1, cc= WinA_Cmd.splitStringEnable )
        
        exportPathPopup = cmds.popupMenu( p=WinA_Global.exportPath_txf )
        sgBFunction_ui.updatePathPopupMenu( WinA_Global.exportPath_txf, exportPathPopup )


mc_showWindow = """import sgPWindow_data_mesh_exportGroup
sgPWindow_data_mesh_exportGroup.WinA().create()"""