toolPath = "A:/@@DEV@@/maya_tools"
startupPath = toolPath + "/startup.py"

f = open( startupPath, 'r' )
data = f.read()
f.close()

data = data.replace( 'TOOL_PATH', toolPath )
exec( data )