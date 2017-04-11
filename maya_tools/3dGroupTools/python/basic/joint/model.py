import sys, os


class MelFileInfo:

    _propertiesPath = ''
        
    for j in sys.path:
        if not os.path.isdir( j ):
            continue
        dirList = os.listdir( j )
        if 'basic' in dirList:
            _propertiesPath = j+'/basic/joint/melFile/properties.mel'