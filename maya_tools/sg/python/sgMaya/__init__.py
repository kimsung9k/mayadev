
def reloadModules( pythonPath='' ):

    import os, imp, sys
    
    if not pythonPath:
        pythonPath = __file__.split( '\\' )[0]


    for root, folders, names in os.walk( pythonPath ):
        root = root.replace( '\\', '/' )
        for name in names:
            try:onlyName, extension = name.split( '.' )
            except:continue
            if extension.lower() != 'py': continue
            
            if name == '__init__.py':
                fileName = root
            else:
                fileName = root + '/' + name
            
            moduleName = fileName.replace( pythonPath, '' ).split( '.' )[0].replace( '/', '.' )[1:]
            moduleEx =False
            
            try:
                sys.modules[moduleName]
                moduleEx = True
            except:
                pass
            
            if moduleEx:
                try:
                    reload( sys.modules[moduleName] )
                except:pass



import os, shutil



def removeDirectory( targetdir ):
    
    if not os.path.exists( targetdir ): return None
    for root, dirs, names in os.walk( targetdir ):
        for name in names:
            try:os.remove( root + '/' + name )
            except:pass
    targetDirs = []
    for root, dirs, names in os.walk( targetdir ):
        for dir in dirs:
            if os.path.exists( root + '/' + dir ):
                targetDirs.append( root + '/' + dir )
    targetDirs.reverse()
    for dir in targetDirs:
        try:os.rmdir( dir )
        except:pass
    try:os.rmdir( targetdir )
    except:pass


def copyPythonModules( srcdir, targetdir ):
    
    removeDirectory( targetdir )
    packages = []
    for root, dirs, names in os.walk( srcdir ):
        for dir in dirs:
            packages.append( root.replace( '\\', '/' ) + '/' + dir )
        break
    
    for package in packages:
        pythonFolder = package + '/python'
        for root, dirs, names in os.walk( pythonFolder ):
            replacedName = root.replace( pythonFolder, '' )
            if replacedName and replacedName[1] == '.': continue
            baseFolder = targetdir + replacedName
            if not os.path.exists( baseFolder ):os.makedirs( baseFolder )
            for dir in dirs:
                if dir[0] == '.': continue
                newFolder = baseFolder + '/' + dir
                if not os.path.exists( newFolder ):os.makedirs( newFolder )
            for name in names:
                if os.path.splitext( name )[-1].lower() in ['.pyc'] or name[0] == '.': continue
                try:shutil.copy2( root + '/' + name, baseFolder + '/' + name )
                except:
                    print "failed to copy : %s --> %s" % ( root + '/' + name, baseFolder + '/' + name )