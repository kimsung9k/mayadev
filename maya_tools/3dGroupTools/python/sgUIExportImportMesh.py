import maya.cmds as cmds
import sgFunctionSceneBake3
import sgModelUI


class CmdExportImportMesh:
    
    def __init__(self, ptr_window ):
        
        self.windowName = ptr_window.uiName
        self.fld_filePath = ptr_window.fld_filePath
    
    
    def exportMesh(self, *args ):
        
        filePath = cmds.textField( self.fld_filePath, q=1, tx=1 )
        sgFunctionSceneBake3.exportMesh( filePath )
    
    
    def importMesh(self, *args ):
        
        filePath = cmds.textField( self.fld_filePath, q=1, tx=1 )
        sgFunctionSceneBake3.importMesh( filePath )
    
    
    def close(self, *args ):
        
        cmds.deleteUI( self.windowName, wnd=1 )
        
        
        
        
class UiTextField:
    
    def __init__(self, firstString, w=120, h=22 ):
        
        self.firstString = firstString
        self.width = w
        self.height = h
    
    
    def create(self):
        
        form = cmds.formLayout()
        
        txt_first  = cmds.text( l=self.firstString, al='right', w= self.width, h=self.height )
        fld_first  = cmds.textField( h=self.height )
        
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af = [ ( txt_first, 'top', 0 ),      ( txt_first, 'left', 0 ),
                                ( fld_first, 'top', 0 ),( fld_first, 'right', 0 )],
                         ac = [ ( fld_first,   'left', 0, txt_first ) ] )
        
        
        self.txt_first  = txt_first
        self.fld_first  = fld_first
        self.form = form
        
        return form
        



class UiThreeButtons:
    
    def __init__(self, firstLabel, secondLabel, thirdLabel, h=25 ):
        
        self.firstLabel  = firstLabel
        self.secondLabel = secondLabel
        self.thirdLabel  = thirdLabel
        self.height = h
    
    
    def create(self):
        
        form = cmds.formLayout()
        
        bt_first  = cmds.button( l= self.firstLabel, h=self.height )
        bt_second = cmds.button( l= self.secondLabel, h=self.height )
        bt_third  = cmds.button( l= self.thirdLabel, h=self.height )
        
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af = [( bt_first, 'top', 0 ), ( bt_first, 'left', 0 ),
                               ( bt_second,'top', 0), ( bt_second,'right', 0 ),
                               ( bt_third,'left', 0), ( bt_third,'bottom', 0 ), ( bt_third,'right', 0 ) ],
                         ap = [( bt_first, 'right', 0, 50 ),( bt_first, 'bottom', 0, 50 ),
                               ( bt_second, 'left', 0, 50 ), ( bt_second, 'bottom', 0, 50 ),
                               ( bt_third, 'top', 0, 50 )] )
        
        self.bt_first  = bt_first
        self.bt_second = bt_second
        self.bt_third  = bt_third
        self.form = form
        
        return form



class WindowExportImportMesh:
    
    def __init__(self):
        
        self.uiName = "sgUIExportImportMesh"
        self.title  = "Export Import Mesh UI"
        self.width  = 450
        self.height = 80
    
        self.uiTextField    = UiTextField( "Target Path :" )
        self.uiThreeButtons = UiThreeButtons( "Export Mesh", "Import Mesh", "Close" )
    
    
    def create(self):
        
        if cmds.window( self.uiName, ex=1 ):
            cmds.deleteUI( self.uiName, wnd=1 )
        cmds.window( self.uiName, title=self.title )

        form = cmds.formLayout()
        uiTextFieldForm = self.uiTextField.create()
        uiButtonsForm   = self.uiThreeButtons.create()
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af= [ (uiTextFieldForm, 'top', 5 ), (uiTextFieldForm, 'left', 0 ), (uiTextFieldForm, 'right', 5 ),
                               (uiButtonsForm, 'bottom', 0 ), (uiButtonsForm, 'left', 0 ), (uiButtonsForm, 'right', 0 ) ],
                         ac= [ (uiButtonsForm, 'top', 5, uiTextFieldForm ) ] )
        
        cmds.window( self.uiName, e=1, width=self.width, height=self.height )
        cmds.showWindow( self.uiName )
        
        
        self.fld_filePath = self.uiTextField.fld_first

        self.cmd = CmdExportImportMesh( self )
        
        self.afterCreate_popupSetting()
        self.afterCreate_buttonCommandSetting()



    def afterCreate_popupSetting( self, addCommand = None ):
        
        popup = cmds.popupMenu( p=self.fld_filePath )
        sgModelUI.updatePathPopupMenu( self.fld_filePath,  popup, addCommand )



    def afterCreate_buttonCommandSetting( self ):
        
        cmds.button( self.uiThreeButtons.bt_first,  e=1, c = self.cmd.exportMesh )
        cmds.button( self.uiThreeButtons.bt_second, e=1, c = self.cmd.importMesh )
        cmds.button( self.uiThreeButtons.bt_third,  e=1, c = self.cmd.close )