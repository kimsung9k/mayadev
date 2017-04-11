import maya.cmds as cmds
import maya.mel as mel
import glob

class DisplayMessage:
    
    _messageOn = False
    
    def __init__(self, message ):
        if self._messageOn: print message


class AutoLoadPlugin:
    def __init__( self ):
        
        self._pluginPaths = []
        self._pluginList  = []
        
        for path in mel.eval( 'getenv MAYA_PLUG_IN_PATH' ).split( ';' ):
            if not path: continue
            self._pluginPaths.append( path )
        self._pluginList = cmds.pluginInfo( q=1, listPlugins=1 )
            
    def updatePluginList(self):
        self._pluginList = cmds.pluginInfo( q=1, listPlugins=1 )
            
    def load( self, pluginName ):
       
        pluginPaths = []
        for path in self._pluginPaths:
            pluginPaths += glob.glob( "%s/%s*.mll" %( path, pluginName ) )
        
        targetPlugList = []
        paths = []
        for pluginPath in pluginPaths:
            path, plugin = pluginPath.split( '\\' )
           
            digit = plugin[ len( pluginName ): -4].replace( '_', '' )
            if not digit:
                targetPlugList.append( plugin[:-4] )
                if not len( paths ) : paths.append( path )
                if not path in paths: paths.append( path )
            elif digit.isdigit():
                targetPlugList.append( plugin[:-4] )
                if not len( paths ) : paths.append( path )
                if not path in paths: paths.append( path )

        targetPlugList.sort()
        if not targetPlugList: 
            DisplayMessage( '"%s" is not existing in plug-in path' % pluginName )
            return None
             
        if len( paths ) > 1:
            DisplayMessage( "\nTarget Plug-in exist in multiple paths" )
            DisplayMessage( "------------------------------------------------------" )
            for path in paths:
                DisplayMessage( path )
            DisplayMessage( "------------------------------------------------------\n" )
            DisplayMessage( "Target Plug-in exist in multiple paths" )
            return None
        
        if self._pluginList:
            if targetPlugList[-1] in self._pluginList:
                DisplayMessage( "%s is already loaded" % targetPlugList[-1] )
                return None
            for targetPlug in targetPlugList:
                if targetPlug in self._pluginList:
                    try:
                        cmds.unloadPlugin( targetPlug )
                        DisplayMessage( '"%s" is unloaded' % targetPlug )
                    except: 
                        DisplayMessage( "UnloadPlugin Failed : %s" % targetPlug )
                        return None
        else:
            for targetPlug in targetPlugList:
                try: 
                    cmds.unloadPlugin( targetPlug )
                    DisplayMessage( '"%s" is unloaded' % targetPlug )
                except: 
                    DisplayMessage( "UnloadPlugin Failed : %s" % targetPlug )
                    return None

        cmds.loadPlugin( targetPlugList[-1] )
        DisplayMessage( '"%s" is loaded' % targetPlugList[-1] )
        
        self.updatePluginList()