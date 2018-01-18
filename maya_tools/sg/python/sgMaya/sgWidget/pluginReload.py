import maya.cmds as cmds
import maya.mel as mel
import os
import shutil
import cPickle




def makeFolder( pathName ):
    if os.path.exists( pathName ):return None
    os.makedirs( pathName )
    return pathName


def makeFile( filePath ):
    if os.path.exists( filePath ): return None
    filePath = filePath.replace( "\\", "/" )
    splits = filePath.split( '/' )
    folder = '/'.join( splits[:-1] )
    makeFolder( folder )
    f = open( filePath, "w" )
    f.close()
    


class WindowInfo:
    
    _winName = 'maya_plug_in_reload_ui'
    _title   = 'Maya Plug-in Reload UI'
    
    _width = 300
    _height = 10
    
    
class CodePathUIInfo:
    
    _label = 'Code Path  :   '
    _sepPercent = 40
    
    

class PluginPathUIInfo:
    
    _label = 'Plug-in Path  :   '
    _sepPercent = 40
    
    
class SourceNameUIInfo:
    
    _label = 'Source Name  :   '
    _sepPercent = 40
    

class DestNameUIInfo:
    
    _label = 'Dest Name  :   '
    _sepPercent = 40
    
    
class ButtonUIInfo:
    
    _label1 = 'Reload'
    _label2 = 'close'




class TextAndTextField:
    
    def __init__(self):
        
        self._cmdChange = []
        self._cmdPopup  = []


    def append_cmdChange(self, cmd ):
        self._cmdChange.append( cmd )


    def cmdChange(self, *args):
        for cmd in self._cmdChange: cmd()
        
        
    def append_cmdPopup(self, cmd ):
        self._cmdPopup.append( cmd )


    def cmdPopup(self, *args ):
        for cmd in self._cmdPopup: cmd()
    

    def create( self, label, sepPercent=30, text='' ):
        
        ui_form = cmds.formLayout()
        ui_txt = cmds.text( l=label, al='right' )
        ui_tf  = cmds.textField( tx=text, cc=self.cmdChange )
        
        cmds.formLayout( ui_form, e=1,
                         attachForm = [ ( ui_txt, 'top', 0 ),( ui_txt, 'bottom', 0 ),( ui_txt, 'left', 0 ),
                                        ( ui_tf,  'top', 0 ),( ui_tf,  'bottom', 0 ),( ui_tf, 'right', 0 ) ],
                         attachPosition = [ ( ui_txt, 'right', 0, sepPercent ),
                                            ( ui_tf , 'left' , 0, sepPercent ) ] )
        cmds.setParent( '..' )
        
        self._ui_txt  = ui_txt
        self._ui_tf   = ui_tf
        self._ui_form = ui_form



class TwoButton:
    
    def __init__(self ):
        
        self._cmdButton1 = []
        self._cmdButton2 = []
    
    
    def append_cmdButton1(self, cmd ):
        self._cmdButton1.append( cmd )

    def append_cmdButton2(self, cmd ):    
        self._cmdButton2.append( cmd )
        
    def cmdButton1(self, *args ):
        for cmd in self._cmdButton1: cmd()
    
    def cmdButton2(self, *args ):
        for cmd in self._cmdButton2: cmd()
    

    def create( self, label1, label2, sepPercent = 50 ):
        
        ui_form = cmds.formLayout()
        ui_button1 = cmds.button( l=label1, c=self.cmdButton1 )
        ui_button2 = cmds.button( l=label2, c=self.cmdButton2 )
        
        cmds.formLayout( ui_form, e=1, 
                         attachForm = [ ( ui_button1, 'top', 0 ), ( ui_button1, 'bottom', 0 ), ( ui_button1, 'left' , 0 ),
                                        ( ui_button2, 'top', 0 ), ( ui_button2, 'bottom', 0 ), ( ui_button2, 'right', 0 ) ],
                         attachPosition = [ ( ui_button1, 'right', 0, sepPercent ),
                                            ( ui_button2, 'left',  0, sepPercent )] )
        cmds.setParent( '..' )
        
        self._ui_button1 = ui_button1
        self._ui_button2 = ui_button2
        self._ui_form    = ui_form        



uiInfoPath = cmds.about(pd=True) + "/sg/sg_toolInfo/pluginReload.txt"
makeFile( uiInfoPath )



class UI_Global:

    txf_codePath = ""
    txf_pluginPath = ""
    txf_sourceName = ""
    txf_destName = ""


class reloadPlug_cmd:
    
    @staticmethod
    def reloadPlug( *args ):
        
        codePath = cmds.textField( UI_Global.txf_codePath, q=1, tx=1 )
        plugPath = cmds.textField( UI_Global.txf_pluginPath, q=1, tx=1 )
        srcName  = cmds.textField( UI_Global.txf_sourceName, q=1, tx=1 )
        dstName  = cmds.textField( UI_Global.txf_destName, q=1, tx=1 )
        
        reloadPlug_cmd.setPath( codePath, plugPath, srcName, dstName )
        
        currentScene = cmds.file( q=1, sn=1 )
        cmds.file( f=1, new=1 )
        cmds.unloadPlugin( dstName )
        
        codePath += '\\'+srcName
        plugPath += '\\'+dstName

        print codePath
        print plugPath
        
        shutil.copy2( codePath, plugPath )
        
        cmds.loadPlugin( '%s' % plugPath )
        
        extension = currentScene.split( '.' )[-1]
        
        if extension == 'mb':
            cmds.file( currentScene, f=1, options = "v=0;",  typ = "mayaBinary", o=1 )
            mel.eval( 'addRecentFile("%s", "mayaBinary");' % currentScene )
        elif extension == "ma":
            cmds.file( currentScene, f=1, options = "v=0;",  typ = "mayaAscii", o=1 )
            mel.eval( 'addRecentFile("%s", "mayaBinary");' % currentScene )

    @staticmethod
    def getPath( *args ):
        
        codePath = ''
        plugPath = ''
        srcName = ''
        dsgName = ''
        f = open( uiInfoPath, 'r' )
        try:
            codePath, plugPath, srcName, dsgName = cPickle.load(f)
        except:
            print "failed to load"
        f.close()
            
        cmds.textField( UI_Global.txf_codePath, e=1, tx=codePath )
        cmds.textField( UI_Global.txf_pluginPath, e=1, tx=plugPath )
        cmds.textField( UI_Global.txf_sourceName, e=1, tx=srcName )
        cmds.textField( UI_Global.txf_destName, e=1, tx=dsgName )
        
    @staticmethod
    def setPath( codePath, plugPath, plugSrc, plugDst, *args ):

        f = open( uiInfoPath, 'w' )
        data = [codePath, plugPath, plugSrc, plugDst]
        try:
            cPickle.dump( data, f )
            f.close()
        except:
            f.close()
            if data != None:
                f = open( uiInfoPath, 'w' )
                f.write(data)
                f.close()

    @staticmethod
    def deleteUI( *args ):
        cmds.deleteUI( WindowInfo._winName, wnd=1 )
        


class UI:
    
    def __init__(self):
        
        self._codePathUI = TextAndTextField()
        self._pluginPathUI = TextAndTextField()
        self._sourceNameUI = TextAndTextField()
        self._destNameUI = TextAndTextField()
        self._buttonUI = TwoButton()
    
    
    def show(self, evt=0 ):
        
        if cmds.window( WindowInfo._winName, ex=1 ):
            cmds.deleteUI( WindowInfo._winName, wnd=1 )
        cmds.window( WindowInfo._winName, title=WindowInfo._title )
        
        cmds.columnLayout()
        
        cmds.rowColumnLayout( nc=1, cw=[(1,WindowInfo._width-2)] )
        self._codePathUI.create( CodePathUIInfo._label, CodePathUIInfo._sepPercent )
        self._pluginPathUI.create( PluginPathUIInfo._label, PluginPathUIInfo._sepPercent )
        self._sourceNameUI.create( SourceNameUIInfo._label, SourceNameUIInfo._sepPercent )
        self._destNameUI.create( DestNameUIInfo._label, DestNameUIInfo._sepPercent )
        self._buttonUI.create( ButtonUIInfo._label1, ButtonUIInfo._label2 )
        cmds.setParent( '..' )

        UI_Global.txf_codePath = self._codePathUI._ui_tf
        UI_Global.txf_pluginPath = self._pluginPathUI._ui_tf
        UI_Global.txf_sourceName = self._sourceNameUI._ui_tf
        UI_Global.txf_destName = self._destNameUI._ui_tf
        self._buttonUI.append_cmdButton1( reloadPlug_cmd.reloadPlug ) 
        self._buttonUI.append_cmdButton2( reloadPlug_cmd.deleteUI ) 

        cmds.window( WindowInfo._winName, e=1, w=WindowInfo._width, h=WindowInfo._height )
        cmds.showWindow( WindowInfo._winName )

        reloadPlug_cmd.getPath()



def show():
    UI().show()



if __name__ == '__main__':
    show()



