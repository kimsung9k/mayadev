
#setup script jobs
try:
    cmds.evalDeferred( 'import loadPackage' )
    cmds.evalDeferred( 'loadPackage.mayaTools()' )
except:
    pass
