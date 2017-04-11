

def showMayaWindow( targetPath ):

    import os
    import maya.cmds as cmds
    import maya.mel as mel
    
    if not os.path.exists( targetPath ): return None
    
    targetPath = targetPath.replace( '\\', '/' )
    _3dGroupMenu = targetPath.split( '/' )[-1]
    
    if cmds.menu( _3dGroupMenu, q=1, ex=1 ):
        cmds.menu( _3dGroupMenu, e=1, to=1 )
        cmds.menu( _3dGroupMenu, e=1, dai=1 )
    else:
        cmds.menu( _3dGroupMenu, l= '_'.join( _3dGroupMenu.split( '_' )[1:] ), parent='MayaWindow', to=1 )
    cmds.refresh()
    
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
    
    
    def renameTargets( folderName ):
        
        for root, dirs, names in os.walk( folderName ):
            
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
            targets_afterNames = []
            
            folderIndices = []
            fileIndices   = []
            
            renameIndex = 1
            for i in range( len( targets ) ):
                target = targets[i]
                if os.path.isdir( root + '/' + target ):
                    folderIndices.append( i )
                else:
                    fileIndices.append( i )
                    
                splits = target.split( '.' )
                indexNameStart = 0
                for j in range( len( splits ) ):
                    if splits[j].isdigit():
                        indexNameStart = j+1
                    else:
                        break
                
                if not os.path.exists( root + '/' + '%02d.' % renameIndex +'.'.join( splits[ indexNameStart: ] ) ):
                    os.rename( root+'/'+target, root+'/%02d.' % renameIndex +'.'.join( splits[ indexNameStart: ] ) )
                targets_afterNames.append( root+'/%02d.' % renameIndex +'.'.join( splits[ indexNameStart: ] ) )
                
                if splits[ indexNameStart ][0] != '#':
                    renameIndex += 1
            
            for i in folderIndices:
                renameTargets( targets_afterNames[i] )
            
            break


    def assignCommand( targetPath ):
        
        import sgBFunction_fileAndPath
        locusPath = sgBFunction_fileAndPath.getLocusCommPackagePrefsPath()
        radioButtonInfoPath = sgBFunction_fileAndPath.getLocusCommPackagePrefsPath()+'/radioButtonInfo'

        for root, dirs, names in os.walk( targetPath ):
            root = root.replace( '\\', '/' )
            targets = []
            
            for dir in dirs:
                targets.append( [dir, 'isDir'] )
            
            for name in names:
                extention = name.split( '.' )[-1]
                f = open( root + '/' + name, 'r' )
                data = f.read()
                f.close() 
                
                if extention in ['mel','melScript']:
                    targets.append( [name, "import maya.mel\nmaya.mel.eval('source \"%s\"')" % (root + '/' + name) ] )
                else:
                    if data.find( '%' ) != -1:
                        targets.append( [name, 'execfile( "%s" )' % (root + '/' + name) ] )
                    else:
                        targets.append( [name, data ] )
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
                if targetOnlyName[0] == '@':
                    if targetOnlyName == '@radioCollection':
                        cmds.radioMenuItemCollection( targetUIName, p = parentUIName )
                    else:
                        firstLine = command.split( '\n' )[0]
                        uiName = firstLine.split( "'" )[-2]
                        cmds.menuItem( uiName, l=label[1:], c=command, radioButton=False, p = parentUIName )
                        
                elif targetOnlyName[0] == '#':
                    dividerLabel = targetOnlyName[1:].replace( '-', '' )
                    if dividerLabel:
                        if i == 0:
                            cmds.menuItem( targetUIName + 'labelSpace', l='', p=parentUIName )
                        cmds.menuItem( targetUIName + targetOnlyName, d=1, dividerLabel=dividerLabel, p=parentUIName )
                    else:
                        cmds.menuItem( targetUIName + targetOnlyName, d=1, p=parentUIName )
                else:
                    if command == 'isDir':
                        cmds.menuItem( targetUIName, l=label, sm=1, p=parentUIName, to=1 )
                    else:
                        cmds.menuItem( targetUIName, l=label, c=command, p=parentUIName )
    
        for root, dirs, names in os.walk( radioButtonInfoPath ):
            for name in names:
                command = cmds.menuItem( name, q=1, c=1 )
                tempFilePath = locusPath + '/~~tempFile'
                f = open( tempFilePath, 'w' )
                f.write( command )
                f.close()
                execfile( tempFilePath )
                os.remove( tempFilePath )
                
                cmds.menuItem( name, e=1, radioButton=True )
                
            break

    renameTargets( targetPath )
    assignCommand( targetPath )



def showMayaWindows_inScriptPath():
    
    import maya.mel as mel
    import os
    
    paths = mel.eval( 'getenv MAYA_SCRIPT_PATH' )
    
    windowMenuFolders = []
    for path in paths.split( ';' ):
        for root, dirs, names in os.walk( path ):
            for directory in dirs:
                if directory[:15] != 'mayaWindowMenu_': continue
                windowMenuFolders.append( root+ '/' + directory )
            break
    
    for windowMenuFolder in windowMenuFolders:
        showMayaWindow( windowMenuFolder )



def show3dGroupTools():

    def get3dGroupPath():
        import sys
        _3dGroupPath = ''

        for path in sys.path:
            path = path.replace( '\\', '/' )
            if path.find( '/packages/3dGroupTools' ) != -1:
                _3dGroupPath = path.split( '/packages/3dGroupTools' )[0]
                _3dGroupPath += '/packages/3dGroupTools'
                break
            if path.find( '/packages/3dGroup' ) != -1:
                _3dGroupPath = path.split( '/packages/3dGroup' )[0]
                _3dGroupPath += '/packages/3dGroup'
                break
    
        return _3dGroupPath

    import os
    _3dGroupPath =  __file__.split( 'python' )[0] + 'datas/menus'
    
    print "3d grounp path : ", _3dGroupPath

    for root, dirs, names in os.walk( _3dGroupPath ):
        for directory in dirs:
            print directory
            if directory[:15] != 'mayaWindowMenu_': continue
            showMayaWindow( root+'/'+directory )
        break

show3dGroupTools()