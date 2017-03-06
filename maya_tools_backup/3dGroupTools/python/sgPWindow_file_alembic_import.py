import maya.cmds as cmds
import sgBFunction_ui
import sgBModel_sgPWindow



class WinA_Global:
    
    winName = 'sgPWindow_file_Alembic_import'
    title   = "Alembic Import"
    width   = 450
    height  = 50
    
    alembicListBase = ''
    importPath_txf  = ''
    chk_all = ''
    button  = ''
    checkList    = []
    prefixList   = []
    fileNameList = []
    
    import sgBFunction_fileAndPath
    pathInfo = sgBFunction_fileAndPath.getPathInfo_sgPWindow_file_alembic()
    
    titleBarMenu = True
    




class WinA_ImportPath:
    
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
        
        WinA_Global.importPath_txf  = txf
        WinA_Global.importPath_form = form
        
        return form





class WinA_AlembicListLabel:
    

    def __init__( self ):
        
        pass


    def create(self):

        form = cmds.formLayout()
        frame_check  = cmds.checkBox( label = ' ', w=22, v=1, h=21 )
        frame_prefix = cmds.frameLayout( label = 'Add Prefix', w=120, borderStyle='etchedIn' ); cmds.setParent( '..' )
        frame_path   = cmds.frameLayout( label = 'File Name', borderStyle='etchedIn' ); cmds.setParent( '..' )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[ ( frame_check, 'left', 8 ), ( frame_path, 'right', 0 ) ],
                         ac=[ ( frame_prefix, 'left', 0, frame_check ) ],
                         ap=[ ( frame_prefix, 'right', 0, 35 ), ( frame_path, 'left', 0, 35 ) ] )
        
        WinA_Global.chk_all = frame_check
        
        return form





class WinA_AlembicListBase:
    
    def __init__(self):
        
        pass

    
    def create(self):
        
        form = cmds.formLayout()
        cmds.setParent( '..' )
        
        WinA_Global.alembicListBase = form
        
        return form





class WinA_AlembicList:
    
    def __init__(self ):
        
        pass
    
    
    def create(self):
        
        form = cmds.formLayout()
        check = cmds.checkBox( l='', v=1, w=22, h=21 )
        field_prefix = cmds.textField( h=21 )
        field_path   = cmds.textField( h=21 )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[ ( check, 'left', 8 ), ( field_path, 'right', 0 ) ],
                         ac=[ ( field_prefix, 'left', 0, check ) ],
                         ap=[ ( field_prefix, 'right', 0, 35 ), ( field_path, 'left', 0, 35 ) ] )
        
        self.chk  = check
        self.fld_prefix = field_prefix
        self.fld_path   = field_path

        return form





class WinA_Button:
    
    def __init__( self, label, bgc, height ):
        
        self.label = label
        self.bgc = bgc
        self.height = height

    
    def create(self):
        
        button = cmds.button( l=self.label, h= self.height, bgc=self.bgc )
        WinA_Global.button = button
        
        return button
        



class WinA_Cmd:
    
    @staticmethod
    def cmdImport( *args ):
        
        import sgBExcute_data
        folderPath = cmds.textField( WinA_Global.importPath_txf, q=1, tx=1 )
        
        for i in range( len( WinA_Global.checkList ) ):
            checkValue = cmds.checkBox( WinA_Global.checkList[i], q=1, v=1 )
            if not checkValue: continue
            prefix   = cmds.textField( WinA_Global.prefixList[i], q=1, tx=1 )
            fileName = cmds.textField( WinA_Global.fileNameList[i], q=1, tx=1 )
            filePath = folderPath + '/' + fileName
            sgBExcute_data.importAlembicData( prefix, filePath )

    
    @staticmethod
    def checkAllEdit( *args ):
        
        checkAllValue = cmds.checkBox( WinA_Global.chk_all, q=1, v=1 )
        
        for check in WinA_Global.checkList:
            cmds.checkBox( check, e=1, v=checkAllValue )
    


    @staticmethod
    def checkEachEdit( *args ):
        
        for chk in WinA_Global.checkList:
            if not cmds.checkBox( chk, q=1, v=1 ):
                cmds.checkBox( WinA_Global.chk_all, e=1, v=0 )
                return None
        cmds.checkBox( WinA_Global.chk_all, e=1, v=1 )
    


    @staticmethod
    def updateAlembic( *args ):
        
        import os
        
        childrenUis = cmds.formLayout( WinA_Global.alembicListBase, q=1, ca=1 )
        if childrenUis:
            for ui in childrenUis: cmds.deleteUI( ui )
        
        WinA_Global.checkList    = []
        WinA_Global.prefixList   = []
        WinA_Global.fileNameList = []
        
        path = cmds.textField( WinA_Global.importPath_txf, q=1, tx=1 )
        if not os.path.exists(path): return None
        
        alembicList = []
        for root, dirs, names in os.walk( path ):
            for name in names:
                if not name.split( '.' )[-1].lower() == 'abc': continue
                alembicList.append( name )
            break
        
        cmds.setParent( WinA_Global.alembicListBase )
        forms = []
        for alembicName in alembicList:
            inst = WinA_AlembicList()
            form = inst.create()
            forms.append( form )
            WinA_Global.checkList.append( inst.chk )
            WinA_Global.prefixList.append( inst.fld_prefix )
            WinA_Global.fileNameList.append( inst.fld_path )
        
        import copy
        prefixList = []
        for i in range( len( alembicList ) ):
            prefixOrigName = 'abc_' + alembicList[i].split( '_' )[1].split( '.' )[0].lower()
            prefixName = copy.copy( prefixOrigName )
            index = 1
            while prefixName in prefixList:
                prefixName = prefixOrigName + '%d' % index
                index += 1
            prefixList.append( prefixName )
            prefixName += '_'
            cmds.textField( WinA_Global.prefixList[i], e=1, tx=prefixName )
            cmds.textField( WinA_Global.fileNameList[i], e=1, tx=alembicList[i] )
        
        af = []
        for form in forms:
            af.append( ( form, 'left', 0 ) )
            af.append( ( form, 'right', 0 ) ) 
        
        ac = []
        for i in range( 1, len( forms ) ):
            ac.append( ( forms[i], 'top', 5, forms[i-1] ) )
        
        cmds.formLayout( WinA_Global.alembicListBase, e=1, 
                         af=af, ac=ac )
        
        cmds.window( WinA_Global.winName, e=1, h=114, rtf=1 )



class WinA:
    
    def __init__(self):
        
        self.uiImportPath = WinA_ImportPath( 'Alembic Path : ', 120, 22, 'right' )
        self.uiButton     = WinA_Button( '>>   IMPORT   A L E M B I C   <<', [0.85,0.85,0.45], 30 )
        self.uiAlembicListlabel = WinA_AlembicListLabel()
        self.uiAlembicListBase  = WinA_AlembicListBase()


    def create(self):
        
        if cmds.window( WinA_Global.winName, ex=1 ):
            cmds.deleteUI( WinA_Global.winName, wnd=1 )
        cmds.window( WinA_Global.winName, title= WinA_Global.title, titleBarMenu = WinA_Global.titleBarMenu )

        form = cmds.formLayout()
        importPathForm = self.uiImportPath.create()
        listLabelForm  = self.uiAlembicListlabel.create()
        listBaseForm   = self.uiAlembicListBase.create()
        buttonForm     = self.uiButton.create()
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[(importPathForm, 'top', 8), (importPathForm, 'left', 0), (importPathForm, 'right', 0),
                             (buttonForm,     'left', 0 ), (buttonForm,    'right', 0 ), 
                             (listLabelForm, 'left', 0 ), (listLabelForm, 'right', 0 ),
                             (listBaseForm, 'left', 0 ), (listBaseForm, 'right', 0 )],
                         ac=[(listLabelForm, 'top', 8, importPathForm), 
                             (listBaseForm, 'top', 8, listLabelForm), 
                             (buttonForm, 'top', 16, listBaseForm)] )
        
        cmds.window( WinA_Global.winName, e=1, w= WinA_Global.width, h= WinA_Global.height, rtf=1 )
        cmds.showWindow( WinA_Global.winName )
        
        import cPickle
        f = open( WinA_Global.pathInfo, 'r' )
        path = cPickle.load( f )
        f.close()
        cmds.textField( WinA_Global.importPath_txf, e=1, tx= path )
        WinA_Cmd.updateAlembic()
        
        popup = cmds.popupMenu( p=WinA_Global.importPath_txf )
        sgBFunction_ui.updatePathPopupMenu( WinA_Global.importPath_txf, popup, WinA_Cmd.updateAlembic )
        
        cmds.checkBox( WinA_Global.chk_all, e=1, cc= WinA_Cmd.checkAllEdit )
        for chk in WinA_Global.checkList:
            cmds.checkBox( chk, e=1, cc= WinA_Cmd.checkEachEdit )
        
        cmds.button( WinA_Global.button, e=1, c= WinA_Cmd.cmdImport )