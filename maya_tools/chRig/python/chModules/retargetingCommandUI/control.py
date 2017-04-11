from model import *
from functools import partial

import maya.cmds as cmds
import function
import os, glob


import chModules.retargetingCommand.control as retargetControl


class SetClearCmd:
    
    def __init__(self):
        
        self.clearFolderUIInfo()
        self.clearFolderSubRenameUiInfo()
        self.clearFolderSubDeleteUiInfo()
        self.clearRadioUIInfo()
        self.clearPartUIInfo()
        self.clearExportUIInfo()
        self.clearImportUIInfo()
        self.clearBakeUIInfo()
        
        
    def clearFolderUIInfo(self):
        
        FolderUIInfo._cmdGetPath = []
        FolderUIInfo._cmdLoadFileList = []
        FolderUIInfo._cmdSelect = []
        FolderUIInfo._cmdOpenRenameSub = []
        FolderUIInfo._cmdOpenDeleteSub = []
        
        
    def clearFolderSubRenameUiInfo(self):
        
        FolderSubRenameUiInfo._cmdRename = []
        
        
    def clearFolderSubDeleteUiInfo(self):
        
        FolderSubDeleteUiInfo._cmdDelete = []
        
        
    def clearRadioUIInfo(self):
        
        RadioUIInfo._cmdEnableOn = []
        RadioUIInfo._cmdWeightOn = []
        
        
    def clearPartUIInfo(self):
        
        PartUIInfo._cmdCheck = []
        PartUIInfo._cmdField = []
        
        
    def clearExportUIInfo(self):
        
        ExportUIInfo._cmdLoadSelected = []
        ExportUIInfo._cmdExportPose = []
        ExportUIInfo._cmdExportAnim = []
        
        
    def clearImportUIInfo(self):
        
        ImportUIInfo._cmdLoadSelected = []
        ImportUIInfo._cmdImport = []
        
    
    def clearBakeUIInfo(self):
        
        BakeUIInfo._cmdBake = []
        BakeUIInfo._cmdDeleteAnim = []




class SetUICmd:
    
    def __init__(self):
        
        self.setRadioUI()
        self.setFolderUI()
        self.enableWeightConnect()
        self.setExportUI()
        self.setImportUI()
    
    
    def setFolderUI(self):
        
        def cmdLoadFileList( *args ):
        
            path = cmds.textField( FolderUIInfo._fieldUI, q=1, tx=1 )
            
            fileNames = []
            folderNames = []
            for root, dirs, names in os.walk( path ):
                for name in names:
                    if name[-6:] == '.cpose':
                        fileNames.append( name )
                for dir in dirs:
                    if dir[-6:] == '.canim':
                        folderNames.append( dir )
                break
            cmds.textScrollList( FolderUIInfo._scrollListUI, e=1, ra=1 )
            if not fileNames and not folderNames: return None
            cmds.textScrollList( FolderUIInfo._scrollListUI, e=1, append=fileNames )
            cmds.textScrollList( FolderUIInfo._scrollListUI, e=1, append=folderNames )
            
            retargetControl.ImportData().importPose( ExportImportUIInfo._poseData )


        def cmdSelect( *args ):
            
            path = cmds.textField( FolderUIInfo._fieldUI, q=1, tx=1 )
            item = cmds.textScrollList( FolderUIInfo._scrollListUI, q=1, si=1 )
            
            if not os.path.exists( path + '/' + item[0] ):
                cmds.textScrollList( FolderUIInfo._scrollListUI, e=1, ri=item[0] )
                return None
            
            if item[0][-6:] == ".canim":
                cmds.floatFieldGrp( ImportUIInfo._speedField, e=1, en=1 )
                cmds.floatFieldGrp( ImportUIInfo._frameField, e=1, en=1 )
            else:
                cmds.floatFieldGrp( ImportUIInfo._speedField, e=1, en=0 )
                cmds.floatFieldGrp( ImportUIInfo._frameField, e=1, en=0 )


        def cmdGetPath( *args ):

            getPath = cmds.fileDialog2( fm=2, ff='Folder', dialogStyle=2)
            if not getPath: return None
            cmds.textField( FolderUIInfo._fieldUI, e=1, tx=getPath[0] )
            
            cmdLoadFileList()


        FolderUIInfo._cmdGetPath.append( cmdGetPath )
        FolderUIInfo._cmdLoadFileList.append( cmdLoadFileList )
        FolderUIInfo._cmdSelect.append( cmdSelect )
        ExportUIInfo._cmdExportPose.append( cmdLoadFileList )
        ExportUIInfo._cmdExportAnim.append( cmdLoadFileList )
        FolderSubRenameUiInfo._cmdRename.append( cmdLoadFileList )


    def setRadioUI(self):

        def cmdEnableOn( *args ):
            
            checkBoxGroup   = PartUIInfo._checkBoxGroup   + DetailUIInfo._checkBoxGroup
            floatFieldGroup = PartUIInfo._floatFieldGroup + DetailUIInfo._floatFieldGroup
            
            for checkBox in checkBoxGroup:
                cmds.checkBox( checkBox, e=1, vis=1 )
            
            for floatField in floatFieldGroup:
                cmds.floatField( floatField, e=1, vis= 0 )

                
        def cmdWeightOn( *args ):
            
            checkBoxGroup   = PartUIInfo._checkBoxGroup   + DetailUIInfo._checkBoxGroup
            floatFieldGroup = PartUIInfo._floatFieldGroup + DetailUIInfo._floatFieldGroup
            
            for checkBox in checkBoxGroup:
                cmds.checkBox( checkBox, e=1, vis=0 )
            
            for floatField in floatFieldGroup:
                cmds.floatField( floatField, e=1, vis= 1 )
                
        RadioUIInfo._cmdEnableOn.append( cmdEnableOn )
        RadioUIInfo._cmdWeightOn.append( cmdWeightOn )


    def enableWeightConnect(self):
        
        def floatFieldEnable( floatField, enable, *args ):
            cmds.floatField( floatField, e=1, en=enable )
        def formEnable( form, enable, *args ):
            cmds.formLayout( form, e=1, en=enable )
            cmds.floatField( PartUIInfo._boydField, e=1, en=enable )
        
        checkBoxGroup   = PartUIInfo._checkBoxGroup   + DetailUIInfo._checkBoxGroup
        floatFieldGroup = PartUIInfo._floatFieldGroup + DetailUIInfo._floatFieldGroup
        
        for i in range( len( checkBoxGroup ) ):
            checkBox = checkBoxGroup[i]
            floatField = floatFieldGroup[i]
            
            cmds.checkBox( checkBox, e=1,
                           onc=partial( floatFieldEnable, floatField, 1 ),
                           ofc=partial( floatFieldEnable, floatField, 0 ) )
            
        cmds.checkBox( PartUIInfo._bodyCheck, e=1,
                       onc=partial( formEnable, DetailUIInfo._form, 1 ),
                       ofc=partial( formEnable, DetailUIInfo._form, 0 ) )
        

    def setExportUI(self):
        
        def loadSelected( *args ):
            sels = cmds.ls( sl=1 )
            if not sels: return None
            if len( sels[-1] ) < 9: return None
            if sels[-1][-9:] != 'World_CTL': return None
            cmds.textField( ExportUIInfo._textField, e=1, tx=sels[-1] )
        
        ExportUIInfo._cmdLoadSelected.append( loadSelected )
    
    
    def setImportUI(self):
        
        def loadSelected( *args ):
            sels = cmds.ls( sl=1 )
            if not sels: return None
            if len( sels[-1] ) < 9: return None
            if sels[-1][-9:] != 'World_CTL': return None
            cmds.textField( ImportUIInfo._textField, e=1, tx=sels[-1] )
        
        ImportUIInfo._cmdLoadSelected.append( loadSelected )




class SetCmd:

    def __init__(self):
        
        self._exportData = retargetControl.ExportData()
        self._importData = retargetControl.ImportData()
        
        self.setSelectScrollList()
        self.setExport()
        self.setImport()
        self.setBake()
        self.setPopupScrollList()
        
    
    def setExportEnable(self):
        self._exportData.setEnableDefault(1)
                
        for i in range( len( PartUIInfo._checkBoxGroup ) ):
            value = cmds.checkBox( PartUIInfo._checkBoxGroup[i], q=1, v=1 )
            if not value:
                self._exportData.setPartEnable( PartUIInfo._partList[i], value )
        
        for i in range( len( DetailUIInfo._checkBoxGroup ) ):
            value = cmds.checkBox( DetailUIInfo._checkBoxGroup[i], q=1, v=1 )
            if not value:
                self._exportData.setCtlEnable( DetailUIInfo._detailList[i], value )
                
        self._exportData.setEnable()
    

    def setImportEnable(self):
        self._importData.setEnableDefault( 1 )
        
        targetWorld = cmds.textField( ImportUIInfo._textField, q=1, tx=1 )
        
        for i in range( len( PartUIInfo._checkBoxGroup ) ):
            value = cmds.checkBox( PartUIInfo._checkBoxGroup[i], q=1, v=1 )
            if not value:
                self._importData.setPartEnable( PartUIInfo._partList[i], value )
        
        for i in range( len( DetailUIInfo._checkBoxGroup ) ):
            value = cmds.checkBox( DetailUIInfo._checkBoxGroup[i], q=1, v=1 )
            if not value:
                self._importData.setCtlEnable( DetailUIInfo._detailList[i], value )
                
        self._importData.setEnable(targetWorld)
        
        
    def setImportWeight(self):
        self._importData.setWeightDefault( 1.0 )
        
        targetWorld = cmds.textField( ImportUIInfo._textField, q=1, tx=1 )
        
        for i in range( len( PartUIInfo._floatFieldGroup ) ):
            value = cmds.floatField( PartUIInfo._floatFieldGroup[i], q=1, v=1 )
            if value != 1.0:
                self._importData.setPartWeight( PartUIInfo._partList[i], value )
        for i in range( len( DetailUIInfo._floatFieldGroup ) ):
            value = cmds.floatField( DetailUIInfo._floatFieldGroup[i], q=1, v=1 )
            if value != 1.0:
                self._importData.setCtlWeight( DetailUIInfo._detailList[i], value )
        self._importData.setWeight( targetWorld )
        
                
    def setSelectScrollList(self):
        
        def importData( *args ):
            
            folderPath = cmds.textField( FolderUIInfo._fieldUI, q=1, tx=1 )
            fileName   = cmds.textScrollList( FolderUIInfo._scrollListUI, q=1, si=1 )
            
            worldCtl = cmds.textField( ImportUIInfo._textField, q=1, tx=1 )
            if not worldCtl: return None
            if not cmds.objExists( worldCtl ): return None
            if worldCtl == 'World_CTL':
                cmds.warning( "%s do not have namespace" % worldCtl )
                return None
            
            if not fileName: return None
            fileName = fileName[0]
            
            if fileName[-6:] == '.cpose':
                self._importData.importPose( folderPath + '/' + fileName )
            elif fileName[-6:] == '.canim':
                self._importData.importAnim( folderPath + '/' + fileName )
        
        FolderUIInfo._cmdSelect.append( importData )
    

    def setPopupScrollList(self):
        
        def cmdOpenRenameSub( *args ):
            selItem = cmds.textScrollList( FolderUIInfo._scrollListUI, q=1, si=1 )
            if selItem:
                FolderSubRenameUiInfo._renameTarget = selItem[0]
            else:
                FolderSubRenameUiInfo._renameTarget = ''
        
        def cmdOpenDeleteSub( *args ):
            selItem = cmds.textScrollList( FolderUIInfo._scrollListUI, q=1, si=1 )
            if selItem:
                FolderSubDeleteUiInfo._deleteTarget = selItem[0]
            else:
                FolderSubDeleteUiInfo._deleteTarget = ''
        
        def cmdRename( *args ):

            renameTarget = FolderSubRenameUiInfo._renameTarget
            path = cmds.textField( FolderUIInfo._fieldUI, q=1, tx=1 )

            srcPath = path + '/' + renameTarget
            if not os.path.exists( path + '/' + renameTarget ): cmds.error( '%s is not Exists' % srcPath )
            
            extension = renameTarget.split( '.' )[1]
            
            fieldName = cmds.textField( FolderSubRenameUiInfo._renameTextField, q=1, tx=1 )
            if not fieldName: return None

            destPath = path + '/'
            if os.path.exists( path + '/' + fieldName+'.'+extension):
                addNum = 0
                while os.path.exists( path + '/' + fieldName+str(addNum)+'.'+extension ):
                    addNum += 1
                destPath += fieldName+str(addNum)+'.'+extension
            else:
                destPath += fieldName+'.'+extension
            os.rename( srcPath, destPath )
            
            cmds.deleteUI( FolderSubRenameUiInfo._winName, wnd=1 )
            
            cmds.textScrollList( FolderUIInfo._scrollListUI, e=1, ri=renameTarget )
            cmds.textScrollList( FolderUIInfo._scrollListUI, e=1, a=fieldName+'.'+extension )

        def cmdDelete( *args ):
            
            deleteTarget = FolderSubDeleteUiInfo._deleteTarget
            path = cmds.textField( FolderUIInfo._fieldUI, q=1, tx=1 )

            deleteTargetPath = path + '/' + deleteTarget
            if not os.path.exists( deleteTargetPath ): cmds.error( '%s is not Exists' % deleteTargetPath )
            
            if os.path.isdir( deleteTargetPath ):
                for i in glob.glob( deleteTargetPath+'/*' ):
                    os.remove( i )
                os.rmdir( deleteTargetPath )
            else:
                os.remove( deleteTargetPath )
            
            cmds.deleteUI( FolderSubDeleteUiInfo._winName, wnd=1 )
            
            cmds.textScrollList( FolderUIInfo._scrollListUI, e=1, ri=deleteTarget )

        FolderUIInfo._cmdOpenRenameSub.append( cmdOpenRenameSub )
        FolderUIInfo._cmdOpenDeleteSub.append( cmdOpenDeleteSub )
        FolderSubRenameUiInfo._cmdRename.append( cmdRename )
        FolderSubDeleteUiInfo._cmdDelete.append( cmdDelete )


    def setExport(self):
        
        def setCharacter( *args ):
            targetName = cmds.textField( ExportUIInfo._textField, q=1, tx=1 )
            self._exportData.setCharacter( targetName )
            
        def exportPose( *args ):
            self.setExportEnable()
            folderPath = cmds.textField( FolderUIInfo._fieldUI, q=1, tx=1 )
            fileName = function.getNewCPoseName( folderPath )
            self._exportData.exportPose( folderPath + '/' + fileName )
            cmds.textScrollList( FolderUIInfo._scrollListUI, e=1, a=fileName )
            
        def exportAnim( *args ):
            self.setExportEnable()
            folderPath = cmds.textField( FolderUIInfo._fieldUI, q=1, tx=1 )
            value1 = cmds.floatFieldGrp( ExportUIInfo._floatField, q=1, value1=1 )
            value2 = cmds.floatFieldGrp( ExportUIInfo._floatField, q=1, value2=1 )
            fileName = function.getNewCAnimName( folderPath )
            exportAnimPath = folderPath + '/' + fileName
            self._exportData.exportAnim( exportAnimPath, value1, value2 )
            cmds.textScrollList( FolderUIInfo._scrollListUI, e=1, a=fileName )
                
        
        ExportUIInfo._cmdLoadSelected.append( setCharacter )
        ExportUIInfo._cmdExportPose.append( exportPose )
        ExportUIInfo._cmdExportAnim.append( exportAnim )


    def setImport(self):
        
        def setCharacter( *args ):
            targetName = cmds.textField( ImportUIInfo._textField, q=1, tx=1 )
            self._importData.setCharacter( targetName )
            
        def importCharacter( *args ):
            
            selItems = cmds.textScrollList( FolderUIInfo._scrollListUI, q=1, si=1 )
            if not selItems:
                cmds.formLayout( BakeUIInfo._form, e=1, en=0 )
            
            self.setImportEnable()
            self.setImportWeight()
            
            if selItems[0][-6:] == '.cpose':
                flip   = cmds.checkBox( ImportUIInfo._flipCheck, q=1, v=1 )
                self._importData.retargetPose(flip)
                cmds.formLayout( BakeUIInfo._form, e=1, en=0 )
            elif selItems[0][-6:] == '.canim':
                flip   = cmds.checkBox( ImportUIInfo._flipCheck, q=1, v=1 )
                value1 = cmds.floatFieldGrp( ImportUIInfo._frameField, q=1, value1=1 )
                value2 = cmds.floatFieldGrp( ImportUIInfo._frameField, q=1, value2=1 )
                speed   = cmds.floatFieldGrp( ImportUIInfo._speedField, q=1, value1=1 )
                offset  = cmds.floatFieldGrp( ImportUIInfo._speedField, q=1, value2=1 )
                self._importData.setFrameRange( value1, value2 )
                self._importData.setSpeed( speed )
                self._importData.setOffset( offset )
                self._importData.retargetAnim(flip)
                cmds.formLayout( BakeUIInfo._form, e=1, en=1 )
                
        
        ImportUIInfo._cmdLoadSelected.append( setCharacter )
        ImportUIInfo._cmdImport.append( importCharacter )


    def setBake(self):
        
        def bake( *args ):
            value = cmds.radioButton( BakeUIInfo._radio, q=1, sl=1 )
            self._importData.bake( value )
            cmds.formLayout( BakeUIInfo._form, e=1, en=0 )
            
        def deleteAnim( *args ):
            cmds.delete( 'ImportRetargetingEachCommand' )
            cmds.formLayout( BakeUIInfo._form, e=1, en=0 )
            
        BakeUIInfo._cmdDeleteAnim.append( deleteAnim )
        BakeUIInfo._cmdBake.append( bake )