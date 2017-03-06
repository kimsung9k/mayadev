import maya.cmds as cmds
import sgBFunction_ui
import os
from functools import partial


class Win01_field:
    
    def __init__(self, label='', w=120, h=22 ):
        
        self.label = label
        self.width = w
        self.height = h
    
        self.txf   = None
        self.form  = None
    
    def create(self):
        
        form = cmds.formLayout()
        txt = cmds.text( l=self.label, al='right', w=self.width, h=self.height )
        txf = cmds.textField()
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[( txt, 'top', 0 ),( txt,'left', 0 ),
                             ( txf, 'top', 0 ),( txf, 'right', 0 )],
                         ac=[( txf, 'left', 0, txt )] )
        
        self.txf  = txf
        self.form = form
        
        return form



class Win01_checkBox:
    
    def __init__(self, label ='', h=22 ):
        
        self.label  = label
        self.height = h
    
    
    def create(self):
        
        form = cmds.formLayout()
        check = cmds.checkBox( l= self.label, h=self.height )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[(check, 'top', 0 ), (check, 'left', 30 ), (check, 'right', 0 )])
        
        self.check = check
        
        return form



class Win01_buttons:
    
    def __init__( self, label1='', label2='', label3='', h=25 ):
        
        self.label1 = label1
        self.label2 = label2
        self.height = h
    
    
    def create(self):
        
        form = cmds.formLayout()
        button1 = cmds.button( l= self.label1, h=self.height )
        button2 = cmds.button( l= self.label2, h=self.height )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[( button1, 'top', 0 ), ( button1, 'left', 0 ),
                             ( button2, 'top', 0 ), ( button2, 'right', 0 )], 
                         ap=[( button1, 'right', 0, 50 ),
                             ( button2, 'left', 0, 50 )] )
        
        self.button1 = button1
        self.button2 = button2
        
        return form




class Win01_command:
    
    def __init__(self, ptr_window ):
    
        import sgBExcute_data
        import sgBFunction_fileAndPath
        self.ptr_window = ptr_window
        
        self.ptr_cmdImportMesh = sgBExcute_data.importSgMeshData
        self.ptr_cmdImportUVs  = sgBExcute_data.importSgUVData
        self.ptr_cmdGetDefaultMeshDataPath = sgBFunction_fileAndPath.getPath_defaultSgMeshData
        self.ptr_cmdGetDefaultUVDataPath   = sgBFunction_fileAndPath.getPath_defaultSgUVData
    
    
    def cmdImportMesh(self, *args ):
        
        importMeshPath = cmds.textField( self.ptr_window.field_mesh.txf, q=1, tx=1 )
        skipCheck      = cmds.checkBox( self.ptr_window.check.check, q=1, v=1 )
        
        if not os.path.exists( importMeshPath ):
            cmds.error( '"%s" is not Exists' % importMeshPath )
            return None
        
        self.ptr_cmdImportMesh( importMeshPath, skipCheck )
        #cmds.displayString( 'Mesh Data is imported in "%s".' %( cmds.ls( sl=1 )[0] ) )
        self.ptr_window.getTextInfomation()
        

    def cmdImportUVs(self, *args ):
        
        importUVPath   = cmds.textField( self.ptr_window.field_uv.txf, q=1, tx=1 )
        
        if not os.path.exists( importUVPath ):
            cmds.error( '"%s" is not Exists' % importUVPath )
            return None
        
        self.ptr_cmdImportUVs( cmds.ls( sl=1 ), importUVPath )
        #cmds.displayString( 'UV Data is imported in "%s".' %( cmds.ls( sl=1 )[0] ) )
        
        self.ptr_window.getTextInfomation()




class Win01:
    
    def __init__(self):
        
        self.winName = 'sgWindow_data_mesh_import01'
        self.title   = 'Import Mesh'
        self.width = 400
        self.height = 50
    
        self.field_mesh   = Win01_field( 'Import Mesh Path : ' )
        self.field_uv     = Win01_field( 'Import UV Path : ' )
        self.check        = Win01_checkBox( "Skip Import by Name" )
        self.buttons    = Win01_buttons( 'Import Mesh', 'Import UV' )
        
        self.cmd = Win01_command( self )
        
        import sgBFunction_fileAndPath
        self.infoPath = sgBFunction_fileAndPath.getLocusCommPackagePrefsPath() + '/sgPWindow_data_mesh/info.txt'



    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title= self.title )
        
        form = cmds.formLayout()
        field_meshForm = self.field_mesh.create()
        field_uvForm   = self.field_uv.create()
        checkForm      = self.check.create()
        buttons_form   = self.buttons.create()
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[(field_meshForm, 'top', 0 ), ( field_meshForm, 'left', 0 ), ( field_meshForm, 'right', 0 ),
                             (field_uvForm, 'left', 0 ), ( field_uvForm, 'right', 0 ),
                             (checkForm, 'left', 0 ), (checkForm, 'right', 0 ),
                             (buttons_form, 'left', 0 ), ( buttons_form, 'right', 0 ) ],
                         ac=[(field_uvForm, 'top', 0, field_meshForm ),
                             (checkForm, 'top', 0, field_uvForm),
                             (buttons_form, 'top', 0, checkForm )])
        
        cmds.window( self.winName, e=1, w=self.width, h=self.height )
        cmds.showWindow( self.winName ) 
    
        self.setTextInfomation()
        self.popupSetting()
        self.buttonCommandSetting()



    def popupSetting(self):
        
        popupFieldMesh = cmds.popupMenu( p = self.field_mesh.txf )
        sgBFunction_ui.updatePathPopupMenu( self.field_mesh.txf, popupFieldMesh )
        
        popupFieldUV   = cmds.popupMenu( p = self.field_uv.txf )
        sgBFunction_ui.updatePathPopupMenu( self.field_uv.txf, popupFieldUV )
    


    def buttonCommandSetting(self):
        
        cmds.button( self.buttons.button1, e=1, c=self.cmd.cmdImportMesh )
        cmds.button( self.buttons.button2, e=1, c=self.cmd.cmdImportUVs  )
    


    def getTextInfomation(self):
        
        import sgBFunction_fileAndPath
        import cPickle
        infoPath = sgBFunction_fileAndPath.getPath_sgPWindow_data_mesh_info()
        meshPath = cmds.textField( self.field_mesh.txf, q=1, tx=1 )
        uvPath = cmds.textField( self.field_uv.txf, q=1, tx=1 )
        f = open( infoPath, 'w' )
        cPickle.dump( [meshPath, uvPath], f )
        f.close()
        


    def setTextInfomation(self):
        
        import sgBFunction_fileAndPath
        import cPickle
        infoPath = sgBFunction_fileAndPath.getPath_sgPWindow_data_mesh_info()
        if not os.path.exists( infoPath ): return None
        f = open( infoPath, 'r' )
        try:
            meshPath, uvPath = cPickle.load( f )
            f.close()
        except: 
            f.close()
            return None
        
        cmds.textField( self.field_mesh.txf, e=1, tx=meshPath )
        cmds.textField( self.field_uv.txf,   e=1, tx=uvPath )


mc_showWindow = """import sgPWindow_data_mesh_import
sgPWindow_data_mesh_import.Win01().create()"""