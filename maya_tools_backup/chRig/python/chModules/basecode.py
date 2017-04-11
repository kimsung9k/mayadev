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


class ItemBase:
    def getItemList( self ):
        itemList = []
        
        for i in dir( self ):
            classItem = None
            exec('classItem = self.%s' % i )
            if type( classItem ) == type(0):
                itemList.append( i )
        return itemList
    
    def getItemIndex( self, itemName ):
        itemIndex = None
        exec('itemIndex = self.%s' % itemName )
        return itemIndex
    
    def numOfItem(self):
        return len( self.getItemList() )
    
    def getSortItemList( self ):
        itemList = self.getItemList()
        
        sortList = []
        for i in range( len( itemList ) ):
            sortList.append( '' )
        
        for item in self.getItemList():
            index = self.getItemIndex( item )
            sortList[ index ] = item
        return sortList
    
    def getItemName( self, index ):
        return self.getSortItemList()[ index ]
    
class CtlItemBase:
    def getItemList( self ):
        itemList = []
        
        for i in dir( self ):
            classItem = None
            exec('classItem = self.%s' % i )
            if type( classItem ) == type([]):
                itemList.append( i )
        return itemList
    
    def getItemIndex( self, itemName ):
        itemIndex = None
        exec('itemIndex = self.%s' % itemName )
        return itemIndex
    
    def numOfItem(self):
        return len( self.getItemList() )
    
    def getSortItemList( self ):
        itemList = self.getItemList()
        
        sortList = []
        for i in range( len( itemList ) ):
            sortList.append( '' )
        
        for item in self.getItemList():
            index = self.getItemIndex( item )
            sortList[ index ] = item
        return sortList
    
    def getItemName( self, index ):
        return self.getSortItemList()[ index ]
    
def oneToList( one ):
    if not type( one ) in [ type([]), type(()) ]:
        return [one]
    else:
        return one
    
def listToOne( list ):
    if len( list ) == 1:
        return list[0]
    else:
        return list
    
def sepNameSpaceAndOriginal( node ):
    splitData = node.split( ':' )
    if len( splitData ) == 1:
        return '', splitData[-1]
    else:
        return ':'.join( splitData[:-1] ), splitData[-1]
    
def getRealNamespace( node, originName ):
    nameSpace, otherName = sepNameSpaceAndOriginal( node )
    if nameSpace: nameSpace+=':'
    return nameSpace + otherName.replace( originName, '' )

def removeNumber_str( name ):
    replaceTargets = []
    for char in name:
        if char.isdigit():
            replaceTargets.append( char )
    
    for target in replaceTargets:
        name = name.replace( target, '' )
    
    return name