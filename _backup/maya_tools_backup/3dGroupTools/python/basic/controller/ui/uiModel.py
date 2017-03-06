import sys, os

class CreateControllerUIInfo:
    
    _winName = 'createControler_ui'
    _title   = 'Create Controller UI'
    
    _width = 65*5
    _height = 100
    
    _iconWidth = 64
    _iconHeight = 64
    
    _iconImagePath = ''
    
    for j in sys.path:
        if not os.path.isdir( j ):
            continue
        dirList = os.listdir( j )
        if 'basic' in dirList:
            _iconImagePath = j+'/basic/controller/ui/icons'