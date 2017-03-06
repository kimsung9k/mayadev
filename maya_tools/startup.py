import maya.cmds as cmds
import maya.mel as mel

import os
import sys

TOOLS_ADMIN_ROOT = 'TOOL_PATH'
PLUGIN_FOLDER_NAME = 'plugins'
PYTHON_FOLDER_NAME = 'python'
MEL_FOLDER_NAME = 'mel'
LOAD_FILE = 'loadPackage.py'


def getPackages():

    for root, folders, names in os.walk( TOOLS_ADMIN_ROOT ):
        return folders



def appendPythonPath( packages ):

    print "MAYA_PYTHON_PATH : "
    for package in packages:
        pythonPath = TOOLS_ADMIN_ROOT + '/' + package + '/' + PYTHON_FOLDER_NAME
        if not os.path.exists( pythonPath ): continue
        if pythonPath in sys.path: continue
        sys.path.append( pythonPath )
        print "    ", pythonPath



def appendPluginPath( packages ):

    addPluginPaths = []

    version = cmds.about(version=True)[:4]

    for package in packages:
        pluginPath = TOOLS_ADMIN_ROOT + "/" + package + "/" + PLUGIN_FOLDER_NAME
        if not os.path.exists( pluginPath + '/' + version ): continue
        addPluginPaths.append( pluginPath + '/' + version )

    putenvStr = mel.eval( 'getenv "MAYA_PLUG_IN_PATH"' ) +';'
    for addPluginPath in addPluginPaths:
        putenvStr += addPluginPath + ";"
    mel.eval( 'putenv "MAYA_PLUG_IN_PATH" "%s"' % putenvStr )
    putenvStr = mel.eval( 'getenv "MAYA_PLUG_IN_PATH"' ) 
    print "MAYA_PLUG_IN_PATH : "
    for path in putenvStr.split( ';' ):
        print "    ", path



def sourceMelScripts( packages ):

    for package in packages:
        melPath = TOOLS_ADMIN_ROOT + "/" + package + "/" + MEL_FOLDER_NAME
        for root, dirs, names in os.walk( melPath ):
            root = root.replace( '\\', '/' )
            for name in names:
                if name.endswith( '.mel' ):
                    print "sourcing mel file : ", root + "/" + name
                    mel.eval( 'source "%s"' % ( root + '/' + name ) )



def loadPackage( packages ):

    print "Load Package : "
    for package in packages:
        packagePath = TOOLS_ADMIN_ROOT + "/" + package
        for root, dirs, names in os.walk( packagePath ):
            root = root.replace( '\\', '/' )
            for name in names:
                if name.startswith( LOAD_FILE+'.' ) and name.endswith( '.py' ):
                    execfile (u'%s' % ( packagePath + '/' + name ) )
                elif name.startswith( LOAD_FILE+'.' ) and name.endswith( '.mel' ):
                    mel.eval( 'source "%s"' % ( root + '/' + name ) )
        print "    ", packagePath + '/' + 'loadPackage.py'
        if os.path.exists( packagePath + '/' + 'loadPackage.py'):
            execfile( packagePath + '/' + 'loadPackage.py' )



def doUserSetup():

    packages = getPackages()

    appendPythonPath( packages )
    appendPluginPath( packages )
    sourceMelScripts( packages )
    loadPackage( packages )

# ############################################################################################################################################
#  main     
if __name__ == "__main__":
    doUserSetup()