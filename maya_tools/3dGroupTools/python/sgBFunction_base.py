import maya.mel as mel
import maya.cmds as cmds
import os




def reloadModule( targetModule ):

    import sgBModel_base
    
    if sgBModel_base.moduleReloadAble:
        print "module reload : ", targetModule
        reload( targetModule )




def openFileBrowser( path='', *args ):
    
    path = path.replace( '\\', '/' )
    
    if not os.path.isfile( path ) and not os.path.isdir( path ):
        return None
    
    if os.path.isfile( path ):
        path = '/'.join( path.split( '/' )[:-1] )
        
    os.startfile( path )



def autoLoadPlugin( pluginName ):
    import glob
    
    def displayMessage( message, messageOn = False ):
        if messageOn:
            print message
        
    pluginPaths = []
    for path in mel.eval( 'getenv MAYA_PLUG_IN_PATH' ).split( ';' ):
        if not path: continue
        pluginPaths.append( path )
    pluginList = cmds.pluginInfo( q=1, listPlugins=1 )
    
    loadPluginPaths = []
    for path in pluginPaths:
        loadPluginPaths += glob.glob( "%s/%s*.mll" %( path, pluginName ) )
    
    targetPlugList = []
    paths = []
    for pluginPath in loadPluginPaths:
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
        displayMessage( '"%s" is not existing in plug-in path' % pluginName )
        return None
         
    if len( paths ) > 1:
        displayMessage( "\nTarget Plug-in exist in multiple paths" )
        displayMessage( "------------------------------------------------------" )
        for path in paths:
            displayMessage( path )
        displayMessage( "------------------------------------------------------\n" )
        displayMessage( "Target Plug-in exist in multiple paths" )
        return None
    
    if pluginList:
        if targetPlugList[-1] in pluginList:
            displayMessage( "%s is already loaded" % targetPlugList[-1] )
            return None
        for targetPlug in targetPlugList:
            if targetPlug in pluginList:
                try:
                    cmds.unloadPlugin( targetPlug )
                    displayMessage( '"%s" is unloaded' % targetPlug )
                except: 
                    displayMessage( "UnloadPlugin Failed : %s" % targetPlug )
                    return None
    else:
        for targetPlug in targetPlugList:
            try: 
                cmds.unloadPlugin( targetPlug )
                displayMessage( '"%s" is unloaded' % targetPlug )
            except: 
                displayMessage( "UnloadPlugin Failed : %s" % targetPlug )
                return None

    cmds.loadPlugin( targetPlugList[-1] )
    displayMessage( '"%s" is loaded' % targetPlugList[-1] )