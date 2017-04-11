import maya.cmds as cmds
import sgModelUI
import cPickle, shutil

import sgBFunction_fileAndPath
        
settingInfoPath = sgBFunction_fileAndPath.getLocusCommPackagePrefsPath() + "/reloadPluginInfo.txt"
tempPluginTestPath = sgBFunction_fileAndPath.getDefaultScenePath()
sgBFunction_fileAndPath.makeFile( settingInfoPath, False )
sgBFunction_fileAndPath.makeFile( tempPluginTestPath, False )


class TwoTextFiels:
    
    def __init__(self, firstString, secondString, w=120, h=22 ):
        
        self.firstString = firstString
        self.secondString = secondString
        self.width = w
        self.height = h
    
    
    def create(self):
        
        form = cmds.formLayout()
        
        txt_first  = cmds.text( l=self.firstString, al='right', w= self.width, h=self.height )
        txt_second = cmds.text( l=self.secondString, al='right', w= self.width, h=self.height )
        fld_first  = cmds.textField( h=self.height )
        fld_second = cmds.textField( h=self.height )
        
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af = [ ( txt_first, 'top', 0 ),      ( txt_first, 'left', 0 ),
                                ( txt_second, 'left', 0 ),
                                ( fld_first, 'top', 0 ),( fld_first, 'right', 0 ),
                                ( fld_second, 'right', 0 ) ],
                         ac = [ ( txt_second, 'top', 0, txt_first ),
                                ( fld_first,   'left', 0, txt_first ),
                                ( fld_second, 'left', 0, txt_second ), ( fld_second, 'top', 0, txt_first ) ] )
        
        
        self.txt_first  = txt_first
        self.txt_second = txt_second
        self.fld_first  = fld_first
        self.fld_second = fld_second
        self.form = form
        
        return form




class ThreeButtons:
    
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
                         af = [( bt_first, 'top', 0 ), ( bt_first, 'left', 0 ), ( bt_first, 'bottom', 0 ),
                               ( bt_second,'top', 0), ( bt_second,'bottom', 0 ),
                               ( bt_third,'top', 0), ( bt_third,'bottom', 0 ), ( bt_third,'right', 0 ) ],
                         ap = [( bt_first, 'right', 0, 33 ),
                               ( bt_second, 'left', 0, 33 ), ( bt_second, 'right', 0, 66 ),
                               ( bt_third, 'left', 0, 66 )] )
        
        self.bt_first  = bt_first
        self.bt_second = bt_second
        self.bt_third  = bt_third
        self.form = form
        
        return form
        
        


class CmdReloadPlugin:
    
    def __init__(self, ptr_window ):
        
        self.windowName = ptr_window.uiName
        self.fld_codePath = ptr_window.fld_codePath
        self.fld_plugPath = ptr_window.fld_plugPath
        self.fld_srcName  = ptr_window.fld_srcName
        self.fld_dstName  = ptr_window.fld_dstName

    
    def reloadAndReopen( self, *args ):
        
        codePath = cmds.textField( self.fld_codePath, q=1, tx=1 )
        plugPath = cmds.textField( self.fld_plugPath, q=1, tx=1 )
        srcName  = cmds.textField( self.fld_srcName,  q=1, tx=1 )
        dstName  = cmds.textField( self.fld_dstName,  q=1, tx=1 )
        
        srcPath = ( codePath + '/' + srcName ).replace( '\\', '/' )
        dstPath = ( plugPath + '/' + dstName ).replace( '\\', '/' )
        
        currentSceneName = cmds.file( q=1, sceneName=1 )
        cmds.file( new=1, f=1 )
        cmds.unloadPlugin( dstName )
        
        shutil.copy2( srcPath, dstPath )
        
        print "Copy From : ", srcPath
        print "Past To   : ", dstPath
        
        if not currentSceneName: currentSceneName = tempPluginTestPath
        try:cmds.file( currentSceneName, f=1, options="v=0;", o=1 )
        except:cmds.file( rename = currentSceneName )
        
        cmds.loadPlugin( dstName )
        
        self.textFieldSaveCommand()
        
    
    def reloadOnly( self, *args ):
        
        codePath = cmds.textField( self.fld_codePath, q=1, tx=1 )
        plugPath = cmds.textField( self.fld_plugPath, q=1, tx=1 )
        srcName  = cmds.textField( self.fld_srcName,  q=1, tx=1 )
        dstName  = cmds.textField( self.fld_dstName,  q=1, tx=1 )
        
        srcPath = ( codePath + '/' + srcName ).replace( '\\', '/' )
        dstPath = ( plugPath + '/' + dstName ).replace( '\\', '/' )
        
        cmds.unloadPlugin( dstName )
        
        shutil.copy2( srcPath, dstPath )
        
        print "Copy From : ", srcPath
        print "Past To   : ", dstPath
        
        cmds.loadPlugin( dstName )
        
        self.textFieldSaveCommand()
        
    
    def close( self, *args ):
        
        self.textFieldSaveCommand()
        cmds.deleteUI( self.windowName, wnd=1 )
    
    
    
    def textFieldSaveCommand( self, *args ):
        
        codePath = cmds.textField( self.fld_codePath, q=1, tx=1 )
        plugPath = cmds.textField( self.fld_plugPath, q=1, tx=1 )
        srcName  = cmds.textField( self.fld_srcName,  q=1, tx=1 )
        dstName  = cmds.textField( self.fld_dstName,  q=1, tx=1 )
        widthHeight = cmds.window( self.windowName, q=1, wh=1 )
    
        f = open( settingInfoPath, 'w' )
        cPickle.dump( [codePath, plugPath, srcName, dstName, widthHeight[0], widthHeight[1] ], f )
        f.close()


    def textFieldLoadCommand( self ):
        
        f = open( settingInfoPath, 'r' )
        data = cPickle.load( f )
        f.close()
        
        if not data: return None 
        
        try: codePath, plugPath, srcName, dstName, width, height = data
        except: return None
        
        cmds.textField( self.fld_codePath, e=1, tx=codePath )
        cmds.textField( self.fld_plugPath, e=1, tx=plugPath )
        cmds.textField( self.fld_srcName,  e=1, tx=srcName  )
        cmds.textField( self.fld_dstName,  e=1, tx=dstName  )
        
        cmds.window( self.windowName, e=1, w=width )
        cmds.window( self.windowName, e=1, h=height )





class WindowReloadPlugin:
    
    def __init__(self):
        
        self.uiName = 'sgReloadPluginUi'
        self.title  = 'Reload Plug-in UI'
        self.width  = 400
        self.height = 100
        
        self.pathsFiels = TwoTextFiels( 'Code Path : ', 'Plug-in Path : ')
        self.namesFiels = TwoTextFiels( 'Source Plug-in Name : ', 'Dest Plug-in Name : ' )
        self.buttons    = ThreeButtons( 'Reload and Reopen', 'Reload Only', 'Close', 30 )



    def create( self ):
        
        if cmds.window( self.uiName, ex=1 ):
            cmds.deleteUI( self.uiName )
        cmds.window( self.uiName, title= self.title, tbm=0 )
        
        form = cmds.formLayout()
        
        uiPathsForm = self.pathsFiels.create()
        uiNamesForm = self.namesFiels.create()
        uiButtons   = self.buttons.create()
        
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[ ( uiPathsForm, 'top', 5 ), ( uiPathsForm, 'left', 0 ),
                              ( uiPathsForm, 'right', 0 ),
                              ( uiNamesForm, 'left', 0 ),( uiNamesForm, 'right', 0 ),
                              ( uiButtons, 'left', 0 ), ( uiButtons, 'right', 0 ), ( uiButtons, 'bottom', 0 ) ],
                         ac =[ ( uiNamesForm, 'top', 10, uiPathsForm ),
                               ( uiButtons, 'top', 10, uiNamesForm)] )

        cmds.window( self.uiName, e=1, width=self.width, height=self.height )
        cmds.showWindow( self.uiName )

        self.fld_codePath = self.pathsFiels.fld_first
        self.fld_plugPath = self.pathsFiels.fld_second
        self.fld_srcName  = self.namesFiels.fld_first
        self.fld_dstName  = self.namesFiels.fld_second

        self.cmd = CmdReloadPlugin( self )
        
        self.afterCreate_popupSetting()
        self.afterCreate_buttonCommandSetting()
        
        self.cmd.textFieldLoadCommand()



    def afterCreate_popupSetting( self, addCommand = None ):
        
        codePathPopup = cmds.popupMenu( p=self.fld_codePath )
        plugPathPopup = cmds.popupMenu( p=self.fld_plugPath )
        sgModelUI.updatePathPopupMenu( self.fld_codePath,  codePathPopup, addCommand )
        sgModelUI.updatePathPopupMenu( self.fld_plugPath,  plugPathPopup, addCommand )



    def afterCreate_buttonCommandSetting( self ):
        
        cmds.button( self.buttons.bt_first,  e=1, c = self.cmd.reloadAndReopen )
        cmds.button( self.buttons.bt_second, e=1, c = self.cmd.reloadOnly )
        cmds.button( self.buttons.bt_third,  e=1, c = self.cmd.close )