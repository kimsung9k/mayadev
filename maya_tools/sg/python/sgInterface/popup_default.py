import maya.cmds as cmds
import sgUIs.imageLoader
import sgUIs.loadImagePlane
import sgUIs.pluginReload
import sgUIs.connectAttr


def reloadModules( evt=0 ):

    import os, imp, sys
    
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
                reload( sys.modules[moduleName] )


def create( parent ):
    
    if cmds.ls( sl=1 ): return None
    
    cmds.menuItem( l = "Modeling Menu", rp = "W", sm=1, p=parent )
    cmds.menuItem( l = "UI Image Loader", rp="N", c = command.ui.imageLoader.show )
    cmds.menuItem( l = "UI Load Image Plane", rp="NW", c = command.ui.loadImagePlane.Window().show )
    
    cmds.menuItem( l='Rigging Menu', rp='N', sm=1, p=parent )
    cmds.menuItem( l="UI Connect Attr", rp="N", c= command.ui.connectAttr.show )
    
    cmds.menuItem( l="UI Plugin Debug", c= command.ui.pluginReload.UI().show, p=parent )
    cmds.menuItem( l="Reload Modules", c= reloadModules, p=parent )