import sys, os
import maya.cmds as cmds
import maya.mel as mel
from functools import partial


class OpenAutoLoad_MayaMenu:
    
    def __init__( self, path, title ):
        
        self.uiName = 'autoLoadMayaMenu_' + title
        self.title = title
        self.parentUIName = 'MayaWindow'
        self.path = path
        
    
    def pyCommand( self, importString, *args ):
        
        try:reload( sys.modules['%s' % importString] )
        except:exec( 'import %s' % importString )
        
        
    def melCommand(self, execPath, *args ):
        mel.eval( 'source "%s";' % execPath )
    
        
    def create( self ):
        
        if cmds.menu( self.uiName, ex=1 ):
            cmds.deleteUI( self.uiName )
        cmds.menu( self.uiName, l= self.title, p=self.parentUIName, to=1 )
        
        beforeSplits = []
        checkPath = self.path+'/'+self.title
        checkPath = checkPath.replace( '\\', '/' )
        
        if not checkPath in sys.path:
            sys.path.append( checkPath )

        for root, dirs, names in os.walk( checkPath ):
            
            root = root.replace( '\\', '/' )
            
            if checkPath == root: continue
            
            splits = root.replace( checkPath, '' )[1:].split( '/' )
            folderName = splits[-1]
            
            mainCommand = None
            
            for name in names:
                if name == 'MainCommand.py':
                    isCommandFolder = True
                    importString = root.replace( checkPath+'/', '' ).replace( '/', '.' )+'.'+name.split( '.' )[0]
                    mainCommand = name
                    break
                elif name == 'MainCommand.mel':
                    isCommandFolder = True
                    commandPath = root +'/'+ name
                    mainCommand = name
                    break
                    
            reloadTargets = []
            sourceTargets = []
            for name in names:
                if name.find( 'MainCommand' ) != -1:
                    continue
                if name.find( '.py' ) != -1:
                    reloadTargets.append( root.replace( checkPath+'/', '' ).replace( '/', '.' )+'.'+name.split( '.' )[0] )
                elif name.find( '.mel' ) != -1:
                    mel.eval( 'source "%s";' % ( root + '/' + name ) )
                    sourceTargets.append( root+'.'+name )
            
            if mainCommand:
                if mainCommand == 'MainCommand.py':
                    cmds.menuItem( l= folderName, c=partial( self.pyCommand, importString ) )
                elif mainCommand == 'MainCommand.mel':
                    cmds.menuItem( l= folderName, c=partial( self.melCommand, commandPath ) )
            else:
                setParentNum = 0
                for i in range( len( beforeSplits ) ):
                    if i >= len( splits ): 
                        setParentNum += 1
                        continue
                    if beforeSplits[i] != splits[i]:
                        setParentNum += 1
                for num in range( setParentNum ):
                    cmds.setParent( '..', menu=1 )
                cmds.menuItem( l= folderName, sm=1, to=1 )
                beforeSplits = splits



def showAutoLoadMenu( menuNames = [] ):
    for path in sys.path:
        for root, dirs, names in os.walk( path ):
            if 'isAutoLoadMenuArea.txt' in names:
                if not menuNames:
                    rootChildren = os.listdir( root )
                else:
                    rootChildren = menuNames
                for rootChild in rootChildren:
                    if os.path.isfile( root+'/'+rootChild ): continue
                    OpenAutoLoad_MayaMenu( root, rootChild ).create()
            break



