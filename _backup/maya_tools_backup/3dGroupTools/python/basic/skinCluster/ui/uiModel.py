import sys, os


class SmoothBindModel:
    
    _buttonHeight = 22


class LockViewModel:
    
    _buttonHeight = 25
    
    _topSpace= 10
    _buttomSpace = 5
    _leftSpace = 0
    _rightSpace = 0
    
    _buttonSpace = 0
    
    _uiImagePath = ''
    
    for j in sys.path:
        if not os.path.isdir( j ):
            continue
        dirList = os.listdir( j )
        if 'simpleSkinWeightEditTool' in dirList:
            _uiImagePath = j+'/simpleSkinWeightEditTool/uiimage'



class WeightViewModel:

    _buttonHeight = 25
    
    _topSpace = 0
    _bottomSpace = 0
    _leftSpace = 0
    _rightSpace = 0
    
    _buttonSpace = 0



class ExportImportModel:
    
    _buttonHeight = 25
    
    
    
class InfluenceModel:
    
    _buttonHeight = 25



class UIModel:
    
    _winName = "simpleWeightEditUI"
    _title   = "Simple Weight Edit UI"
    
    _width = 160
    _height = 410
    _buttonHeight = 25
    
    _separateSpace = 10