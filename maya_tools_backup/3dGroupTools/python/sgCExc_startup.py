


def showMayaWindow( targetPath ):

    import os
    import maya.cmds as cmds
    
    print "auto maya window menu path : ", targetPath
    
    if not os.path.exists( targetPath ): return None
    
    targetPath = targetPath.replace( '\\', '/' )
    _3dGroupMenu = targetPath.split( '/' )[-1]
    
    if cmds.menu( _3dGroupMenu, q=1, ex=1 ):
        cmds.menu( _3dGroupMenu, e=1, to=1 )
        cmds.menu( _3dGroupMenu, e=1,dai=1 )
    else:
        cmds.menu( _3dGroupMenu, l=_3dGroupMenu.split( '_' )[-1], parent='MayaWindow', to=1 )
    
    
    def getAnableUIName( name ):
        replaceStringList = "~!@#$%^&()-=+[]{},' "
        for char in replaceStringList:
            name = name.replace( char, '_' )
        return name
    
    def getUINameAndLabel( name ):
        splits = name.split( '.' )
        targetName = splits[1]
        return getAnableUIName(_3dGroupMenu +'_'+ targetName), targetName
    
    def getUIName( folderName ):
        targetName = folderName.split( '.' )[1]
        return getAnableUIName(_3dGroupMenu +'_'+ targetName)
    
    
    for root, dirs, names in os.walk( targetPath ):
        
        root = root.replace( '\\', '/' )
        
        targets = []
        
        for dir in dirs:
            targets.append( dir )
        
        for name in names:
            f = open( root + '/' + name, 'r' )
            data = f.read()
            f.close() 
            targets.append( name )
        
        targets.sort()
        
        renameIndex = 1
        for target in targets:
            splits = target.split( '.' )
            indexNameStart = 0
            for j in range( len( splits ) ):
                if splits[j].isdigit():
                    indexNameStart = j+1
                else:
                    break
            
            if not os.path.exists( root + '/' + '%02d.' % renameIndex +'.'.join( splits[ indexNameStart: ] ) ):
                print "rename file : ", root + '/' + target
                os.rename( root + '/' + target, root + '/' + '%02d.' % renameIndex +'.'.join( splits[ indexNameStart: ] ) )
            if splits[ indexNameStart ][0] != '#':
                renameIndex += 1
                
                
    
    for root, dirs, names in os.walk( targetPath ):
        
        root = root.replace( '\\', '/' )
        
        targets = []
        
        for dir in dirs:
            targets.append( [dir, ''] )
        
        for name in names:
            f = open( root + '/' + name, 'r' )
            data = f.read()
            f.close() 
            targets.append( [name, data] )
        
        targets.sort()
        
        for i in range( len( targets ) ):
            target, command = targets[i]
            splits = root.replace( targetPath, '' )[1:].split( '.' )
            if len( splits ) == 1:
                parentUIName = _3dGroupMenu
            else:
                parentUIName = getUIName( root.split( '/' )[-1] )
            
            targetUIName, label = getUINameAndLabel( target )
            
            targetOnlyName = target.split( '.' )[1]
            if targetOnlyName[0] == '#':
                dividerLabel = targetOnlyName[1:].replace( '-', '' )
                if dividerLabel:
                    if i == 0:
                        cmds.menuItem( targetUIName + 'labelSpace', l='', p=parentUIName )
                    cmds.menuItem( targetUIName + targetOnlyName, d=1, dividerLabel=dividerLabel, p=parentUIName )
                else:
                    cmds.menuItem( targetUIName + targetOnlyName, d=1, p=parentUIName )
            else:
                if command:
                    cmds.menuItem( targetUIName, l=label, c=command, p=parentUIName )
                else:
                    cmds.menuItem( targetUIName, l=label, sm=1, p=parentUIName, to=1 )



def showMayaWindows_inScriptPath():
    
    import maya.mel as mel
    import os
    
    paths = mel.eval( 'getenv MAYA_SCRIPT_PATH' )
    
    windowMenuFolders = []
    for path in paths.split( ';' ):
        for root, dirs, names in os.walk( path ):
            for dir in dirs:
                if dir[:15] != 'mayaWindowMenu_': continue
                windowMenuFolders.append( root+ '/' + dir )
            break
        break
    
    for windowMenuFolder in windowMenuFolders:
        showMayaWindow( windowMenuFolder )