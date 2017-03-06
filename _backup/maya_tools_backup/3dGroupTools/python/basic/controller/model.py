import sys, os

class MelFileInfo:

    _colorOverridePath = ''
        
    for j in sys.path:
        if not os.path.isdir( j ):
            continue
        dirList = os.listdir( j )
        if 'basic' in dirList:
            _colorOverridePath = j+'/basic/controller/melFile/colorOverride.mel'