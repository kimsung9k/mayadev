import sys, os



def cmdNone( *args ):
    
    print "cmdNone"
    pass




class ExportImportUIInfo:
    
    _uiImagePath = ''
    _poseData    = ''
    
    for j in sys.path:
        if not os.path.isdir( j ):
            continue
        dirList = os.listdir( j )
        if 'chModules' in dirList:
            _uiImagePath = j+'/chModules/retargetingCommandUI/images'
            _poseData    = j+'/chModules/retargetingCommandUI/file/pose1.cpose'

 


class FolderUIInfo:
    
    _textPosition = 7
    _fieldOffset = 5
    _textHeight = 23
    _offsetScrollList = 7
    
    _textUI = ''
    _fieldUI = ''
    _scrollListUI = ''
    
    _cmdGetPath       = []
    _cmdLoadFileList  = []
    _cmdSelect        = []
    _cmdOpenRenameSub = []
    _cmdOpenDeleteSub = []
    
    
    def cmdGetPath( cls, *args ):
        for cmd in FolderUIInfo._cmdGetPath: cmd()
    def cmdLoadFileList( cls, *args ):
        for cmd in FolderUIInfo._cmdLoadFileList : cmd()
    def cmdSelect( cls, *args ):
        for cmd in FolderUIInfo._cmdSelect : cmd()
    def cmdOpenRenameSub( cls, *args ):
        for cmd in FolderUIInfo._cmdOpenRenameSub : cmd()
    def cmdOpenDeleteSub( cls, *args ):
        for cmd in FolderUIInfo._cmdOpenDeleteSub : cmd()
    
    
    cmdGetPath       = classmethod( cmdGetPath )
    cmdLoadFileList  = classmethod( cmdLoadFileList )
    cmdSelect        = classmethod( cmdSelect )
    cmdOpenRenameSub = classmethod( cmdOpenRenameSub )
    cmdOpenDeleteSub = classmethod( cmdOpenDeleteSub )
    



class FolderSubRenameUiInfo:
    
    _renameTarget = ''
    _width = 200
    _height = 25
    _winName = 'retargetingFolderSubRenameUi'
    
    _renameTextField = ''
    
    _cmdRename = []
    def cmdRename( cls, *args ):
        for cmd in FolderSubRenameUiInfo._cmdRename : cmd()
    cmdRename = classmethod( cmdRename )
    



class FolderSubDeleteUiInfo:
    
    _deleteTarget = ''
    _width = 200
    _height = 44
    _winName = 'retargetingFolderSubDeleteUi'
    
    _cmdDelete = []
    def cmdDelete( cls, *args ):
        for cmd in FolderSubDeleteUiInfo._cmdDelete : cmd()
    cmdDelete = classmethod( cmdDelete )




class RadioUIInfo:
    
    _offset = 5
    
    _cmdEnableOn = []
    _cmdWeightOn = []
    
    def cmdEnableOn( cls, *args ):
        for cmd in RadioUIInfo._cmdEnableOn : cmd()
    def cmdWeightOn( cls, *args ):
        for cmd in RadioUIInfo._cmdWeightOn : cmd()
    
    cmdEnableOn = classmethod( cmdEnableOn )
    cmdWeightOn = classmethod( cmdWeightOn )




class PartUIInfo:
    
    _bodyCheck = ''
    _boydField = ''
    
    _width = 230
    _height = 351
    _bgc    = [0.23,0.23,0.23]
    
    _partList = ['Head', 'Body', 'ArmL', 'ArmR', 'HandL', 'HandR', 'LegL', 'LegR' ]
    
    _checkBoxGroup = []
    _floatFieldGroup = []
    
    _cmdCheck = []
    _cmdField = []
    
    def cmdCheck( cls, *args ):
        for cmd in PartUIInfo._cmdCheck : cmd()
    def cmdField( cls, *args ):
        for cmd in PartUIInfo._cmdField : cmd()
    
    cmdCheck = classmethod( cmdCheck )
    cmdField = classmethod( cmdField )
    

    

class DetailUIInfo:
    
    _form = ''
    _bodyEnable = ''
    
    _width = 228
    _height = 351
    _bgc    = [0.23,0.23,0.23]
    
    _detailList = [ 'Shoulder_L_CTL', 'Shoulder_R_CTL', 'Collar_L_CTL', 'Collar_R_CTL',
                    'ChestMove_CTL', 'Chest_CTL', 'Waist_CTL', 'TorsoRotate_CTL',
                    'Root_CTL', 'Hip_CTL' ]
    
    _checkBoxGroup = []
    _floatFieldGroup = []
                               
    


class ExportUIInfo:
    
    _buttonLeft = 5
    
    _textField = ''
    _floatField = ''

    _cmdLoadSelected = []
    
    def cmdLoadSelected( cls, *args ):
        for cmd in ExportUIInfo._cmdLoadSelected : cmd()
    cmdLoadSelected = classmethod( cmdLoadSelected )

    _cmdExportPose = []
    _cmdExportAnim = []

    def cmdExportPose( cls, *args ):
        for cmd in ExportUIInfo._cmdExportPose : cmd()
    cmdExportPose = classmethod( cmdExportPose )
    def cmdExportAnim( cls, *args ):
        for cmd in ExportUIInfo._cmdExportAnim : cmd()
    cmdExportAnim = classmethod( cmdExportAnim )
        



class ImportUIInfo:
    
    _buttonLeft = 5
    
    _textField = ''
    _flipCheck = ''
    _speedField = ''
    _frameField = ''

    _cmdLoadSelected = []
    _cmdImport       = []
    
    def cmdLoadSelected( cls, *args ):
        for cmd in ImportUIInfo._cmdLoadSelected : cmd()
    cmdLoadSelected = classmethod( cmdLoadSelected )
    
    def cmdImport( cls, *args ):
        for cmd in ImportUIInfo._cmdImport : cmd()
    cmdImport = classmethod( cmdImport )



class BakeUIInfo:
    
    _radio = ''
    _form = ''
    
    _cmdDeleteAnim = []
    _cmdBake      = []
    
    def cmdDeleteAnim( cls, *args ):
        for cmd in BakeUIInfo._cmdDeleteAnim : cmd()
    cmdDeleteAnim = classmethod( cmdDeleteAnim )
    def cmdBake( cls, *args ):
        for cmd in BakeUIInfo._cmdBake : cmd()
    cmdBake = classmethod( cmdBake )



class WindowInfo:
    
    _window = 'retargeting_ui'
    _title = 'Retargeting UI'
    
    _width = 850
    _height = 505
    
    _topSpace = 10
    _leftSpace = 10
    _rightSpace = 10
    _bottomSpace = 10
    
    _holizonOffset = 20
    
    _imageOffset = 5