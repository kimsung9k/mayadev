import os, sys

iconPath = ''
for path in sys.path:
    path = path.replace( '\\', '/' )
    if path[-1] == '/':
        path = path[:-1]
    if path.find( '3dGroupTools' ) == -1:
        continue
    
    for root, dirs, names in os.walk( path ):
        for dir in dirs:
            if dir == 'volumeHairTool':
                iconPath = root+'/volumeHairTool/Icon'