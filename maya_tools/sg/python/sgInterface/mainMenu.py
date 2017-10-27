import os
import maya.cmds as cmds
import maya.mel as mel


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


def showMayaWindow( menuName, targetPath ):
    if not os.path.exists( targetPath ): return None
    
    targetPath = targetPath.replace( '\\', '/' )
    menuUiName = 'sg_maya_mainWindow_' + menuName
    
    if cmds.menu( menuUiName, q=1, ex=1 ):
        cmds.menu( menuUiName, e=1, to=1 )
        cmds.menu( menuUiName, e=1, dai=1 )
    else:
        cmds.menu( menuUiName, l= menuName, parent='MayaWindow', to=1 )
    cmds.refresh()
    
    def getAnableUIName( name ):
        replaceStringList = "~!@#$%^&()-=+[]{},' "
        for char in replaceStringList:
            name = name.replace( char, '_' )
        return name
    
    def getUINameAndLabel( name ):
        splits = name.split( '.' )
        targetName = splits[1]
        return getAnableUIName( menuUiName +'_'+ targetName), targetName
    
    def getUIName( folderName ):
        targetName = folderName.split( '.' )[1]
        return getAnableUIName( menuUiName +'_'+ targetName)
    
    
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
                    print root+'/'+target
                    print root+'/%02d.' % renameIndex +'.'.join( splits[ indexNameStart: ] )
                    os.rename( root+'/'+target, root+'/%02d.' % renameIndex +'.'.join( splits[ indexNameStart: ] ) )
                targets_afterNames.append( root+'/%02d.' % renameIndex +'.'.join( splits[ indexNameStart: ] ) )
                
                renameIndex += 1
            
            for i in folderIndices:
                renameTargets( targets_afterNames[i] )
            
            break


    def assignCommand( targetPath ):
        
        infomationPath = cmds.about(pd=True) + "/sg_menu_mainMenu/infoPath.txt"
        makeFile( infomationPath )

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
                    parentUIName = menuUiName
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

    renameTargets( targetPath )
    assignCommand( targetPath )