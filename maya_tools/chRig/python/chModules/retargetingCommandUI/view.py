import maya.cmds as cmds
import os

from model import *
from functools import partial



class FolderUI:

    def __init__(self):
        
        pass


    def create(self):
        
        #getInfo
        folderImagePath  = ExportImportUIInfo._uiImagePath + '/folder.png'
        offsetScrollList = FolderUIInfo._offsetScrollList
        fieldOffset      = FolderUIInfo._fieldOffset
        textPosition     = FolderUIInfo._textPosition
        
        #define UI
        form       = cmds.formLayout()
        
        text       = cmds.image( image=folderImagePath )
        
        field      = cmds.textField( cc=FolderUIInfo.cmdLoadFileList )
        button     = cmds.button( l='Load', w=50, c=FolderUIInfo.cmdGetPath )
        
        scrollList = cmds.textScrollList( sc=FolderUIInfo.cmdSelect )
        cmds.popupMenu()
        cmds.menuItem( l='Rename', c=FolderUIInfo.cmdOpenRenameSub )
        cmds.menuItem( l='Delete', c=FolderUIInfo.cmdOpenDeleteSub )
        
        cmds.formLayout( form, e=1,
                         attachForm = [(text,  'top', 0 ), (text,  'left', 5 ),
                                       (field, 'top', 0 ),
                                       (button, 'top', 0 ), ( button, 'right', 0 ),
                                       (scrollList, 'left',0), (scrollList, 'right',0),
                                       (scrollList, 'bottom',0)],
                         attachControl = [(scrollList, 'top', offsetScrollList, field ),
                                          ( field, 'left', fieldOffset, text ),
                                          ( field, 'right', fieldOffset, button ) ],
                         attachPosition = [ (text, 'right', 0, textPosition)] )
        cmds.setParent( '..' )
        
        #setInfo
        FolderUIInfo._textUI = form.split( '|' )[-1]
        FolderUIInfo._fieldUI = field.split( '|' )[-1]
        FolderUIInfo._scrollListUI = scrollList.split( '|' )[-1]
        
        return form



class RadioUI:

    def __init__(self):
        
        pass
    
    
    def create(self):
        
        buttonOffset = RadioUIInfo._offset
        
        form = cmds.formLayout()
        
        cmds.radioCollection()
        enable = cmds.radioButton( l='Enable', sl=1, onc=RadioUIInfo.cmdEnableOn )
        weight = cmds.radioButton( l='Weight', sl=0, onc=RadioUIInfo.cmdWeightOn )
        
        cmds.formLayout( form, e=1,
                         attachForm = [(enable, 'top', 0),
                                       (weight, 'top', 0), (weight, 'right', 0)],
                         attachControl = [(enable, 'right', buttonOffset, weight)] )
        cmds.setParent( '..' )
        
        return form



class PartUI:
    
    def __init__(self):
        
        pass
    
    
    def create(self):
        
        imagePath = ExportImportUIInfo._uiImagePath + '/part.png'
        width = PartUIInfo._width
        height = PartUIInfo._height
        bgc    = DetailUIInfo._bgc
        
        form = cmds.formLayout( w=width, h=height )
        image = cmds.image( image = imagePath )
        
        template = "uiTemplate"
        if not cmds.uiTemplate( template, ex=1 ):
            cmds.uiTemplate( template )
        cmds.checkBox( dt=template, v=1, cc=PartUIInfo.cmdCheck )
        cmds.floatField( dt=template, vis=0, v=1.0, pre=2, w=40, cc=PartUIInfo.cmdField )
        
        cmds.setUITemplate( template, pushTemplate=1 )
        
        headCheck  = cmds.checkBox( l='Head' );      headField  = cmds.floatField()
        bodyCheck  = cmds.checkBox( l='Body' );      bodyField  = cmds.floatField()
        armLCheck  = cmds.checkBox( l='ArmL' );      armLField  = cmds.floatField()
        armRCheck  = cmds.checkBox( l='ArmR' );      armRField  = cmds.floatField()
        handLCheck = cmds.checkBox( l='HandL');      handLField = cmds.floatField()
        handRCheck = cmds.checkBox( l='HandR');      handRField = cmds.floatField()
        legLCheck  = cmds.checkBox( l='LegL' );      legLField  = cmds.floatField()
        legRCheck  = cmds.checkBox( l='LegR' );      legRField  = cmds.floatField()
        
        cmds.setUITemplate( popTemplate=1 )
        
        cmds.formLayout( form, e=1, 
                         attachForm = [ ( image, 'left', 0 ), ( image, 'top', 0 ),
                                        ( headCheck,'left', 92 ), ( headCheck,'top', 8 ),
                                        ( bodyCheck,'left', 94 ), ( bodyCheck,'top', 125 ),            
                                        ( armRCheck,'left', 20 ),  ( armRCheck,'top', 105 ),
                                        ( armLCheck,'left', 165 ), ( armLCheck,'top', 105 ),
                                        ( handRCheck,'left', 20 ), ( handRCheck,'top', 174 ),
                                        ( handLCheck,'left', 160 ),( handLCheck,'top', 174 ),
                                        ( legRCheck,'left', 40 ),( legRCheck,'top', 280 ),
                                        ( legLCheck,'left', 155 ),( legLCheck,'top', 280 ),
                                        
                                        ( headField,'left', 95 ), ( headField,'top', 8 ),
                                        ( bodyField,'left', 95 ), ( bodyField,'top', 125 ),
                                        ( armRField,'left', 20 ), ( armRField,'top', 105 ),
                                        ( armLField,'left', 166 ), ( armLField,'top', 105 ),
                                        ( handRField,'left', 27 ), ( handRField,'top', 174 ),
                                        ( handLField,'left', 162 ),( handLField,'top', 174 ),
                                        ( legRField,'left', 40 ),  ( legRField,'top', 280 ),
                                        ( legLField,'left', 148 ), ( legLField,'top', 280 )] )

        cmds.setParent( '..' )
        
        PartUIInfo._checkBoxGroup    = [headCheck,bodyCheck,armLCheck,armRCheck,handLCheck,handRCheck,legLCheck,legRCheck]
        PartUIInfo._floatFieldGroup  = [headField,bodyField,armLField,armRField,handLField,handRField,legLField,legRField]
        PartUIInfo._bodyCheck = bodyCheck.split( '|' )[-1]
        PartUIInfo._boydField = bodyField.split( '|' )[-1]
        
        return form



class DetailUI:
    
    def __init__(self):
        
        pass
    
    
    def create(self):
        
        imagePath = ExportImportUIInfo._uiImagePath + '/detail.png'
        width = DetailUIInfo._width
        height = DetailUIInfo._height
        bgc    = DetailUIInfo._bgc
        
        form = cmds.formLayout( w=width, h=height )
        image = cmds.image( image = imagePath )
        
        template = "uiTemplate"
        if not cmds.uiTemplate( template, ex=1 ):
            cmds.uiTemplate( template )
        cmds.checkBox( dt=template, v=1, cc=PartUIInfo.cmdCheck )
        cmds.floatField( dt=template, vis=0, v=1.0, pre=2, w=40, cc=PartUIInfo.cmdField )
        
        cmds.setUITemplate( template, pushTemplate = 1 )
        
        shoulderLCheck   = cmds.checkBox( l='ShoulderL');   shoulderLWeight   = cmds.floatField()
        shoulderRCheck   = cmds.checkBox( l='ShoulderR');   shoulderRWeight   = cmds.floatField()
        collarLCheck     = cmds.checkBox( l='CollarL'  );   collarLWeight     = cmds.floatField()
        collarRCheck     = cmds.checkBox( l='CollarR'  );   collarRWeight     = cmds.floatField()
        chestMoveCheck   = cmds.checkBox( l='ChestMove');   chestMoveWeight   = cmds.floatField()
        chestCheck       = cmds.checkBox( l='Chest');       chestWeight       = cmds.floatField()
        waistCheck       = cmds.checkBox( l='Waist');       waistWeight       = cmds.floatField()
        torsoRotateCheck = cmds.checkBox( l='TorsoRotate'); torsoRotateWeight = cmds.floatField()
        rootCheck        = cmds.checkBox( l='Root' );       rootWeight        = cmds.floatField()
        hipCheck         = cmds.checkBox( l='Hip'  );       hipWeight         = cmds.floatField()
        
        cmds.setUITemplate( popTemplate=1 )
        
        cmds.formLayout( form, e=1,
                         attachForm = [ ( image, 'left', 0 ), ( image, 'top', 0 ),
                                        ( shoulderRCheck, 'left', 20  ), ( shoulderRCheck, 'top', 65 ),
                                        ( shoulderLCheck, 'left', 160 ), ( shoulderLCheck, 'top', 65 ),
                                        ( collarRCheck, 'left', 67 ), ( collarRCheck, 'top', 110 ),                                        
                                        ( collarLCheck, 'left', 127 ), ( collarLCheck, 'top', 110 ),                                        
                                        ( chestMoveCheck, 'left', 97 ), ( chestMoveCheck, 'top', 135 ),
                                        ( chestCheck, 'left', 97 ), ( chestCheck, 'top', 152 ),
                                        ( waistCheck, 'left', 97 ), ( waistCheck, 'top', 205 ),
                                        ( torsoRotateCheck, 'left', 97 ), ( torsoRotateCheck, 'top', 255 ),
                                        ( rootCheck, 'left', 97 ), ( rootCheck, 'top', 273 ),
                                        ( hipCheck, 'left', 97 ), ( hipCheck, 'top', 291 ),
                                        
                                        ( shoulderRWeight, 'left', 20  ), ( shoulderRWeight, 'top', 72 ),
                                        ( shoulderLWeight, 'left', 170 ), ( shoulderLWeight, 'top', 72 ),
                                        ( collarRWeight, 'left', 72 ), ( collarRWeight, 'top', 110 ),                                        
                                        ( collarLWeight, 'left', 122 ), ( collarLWeight, 'top', 110 ),                                        
                                        ( chestMoveWeight, 'left', 98 ), ( chestMoveWeight, 'top', 133 ),
                                        ( chestWeight, 'left', 98 ), ( chestWeight, 'top', 155 ),
                                        ( waistWeight, 'left', 98 ), ( waistWeight, 'top', 205 ),
                                        ( torsoRotateWeight, 'left', 98 ), ( torsoRotateWeight, 'top', 255 ),
                                        ( rootWeight, 'left', 98 ), ( rootWeight, 'top', 273 ),
                                        ( hipWeight, 'left', 98 ), ( hipWeight, 'top', 291 ) ] )

        cmds.setParent( '..' )
        
        DetailUIInfo._checkBoxGroup   = [shoulderLCheck,shoulderRCheck,collarLCheck,collarRCheck,chestMoveCheck,chestCheck,waistCheck,torsoRotateCheck,rootCheck,hipCheck]
        DetailUIInfo._floatFieldGroup = [shoulderLWeight,shoulderRWeight,collarLWeight,collarRWeight,chestMoveWeight,chestWeight,waistWeight,torsoRotateWeight,rootWeight,hipWeight]
        DetailUIInfo._form = form.split( '|' )[-1]
        
        return form



class ExportUI:

    def __init__(self):

        self._exportAnimInfo = [':World_CTL',1.0, 24.0]


    def create(self):
        
        buttonLeftSpace = ExportUIInfo._buttonLeft
        
        form = cmds.formLayout()
        
        text   = cmds.text( l='EXPORT TARGET : ', h=22 )
        
        textField = cmds.textField( h=22 )
        cmds.popupMenu()
        cmds.menuItem( l='Load Selected', c=ExportUIInfo.cmdLoadSelected )
        
        exPose = cmds.button( l='Export Pose', c= ExportUIInfo.cmdExportPose )
        exAnim = cmds.button( l='Export Anim', c= ExportUIInfo.cmdExportAnim,  w=100 )
        fField = cmds.floatFieldGrp( l='Min/Max', nf=2, value1=1.0, value2=24.0, cw3=(50,50,50) )
        
        fieldLength = 38
        
        cmds.formLayout( form, e=1,
                         attachForm= [(text, 'top', 0), (text, 'left', 0),
                                      (textField, 'top', 0),
                                      (exPose, 'top', 0),
                                      (exAnim, 'top', 0),
                                      (fField, 'top', 0), (fField, 'right', 0)],
                         attachControl =  [(textField, 'left', 0, text),
                                           (exPose, 'left', buttonLeftSpace, textField),
                                           (exAnim, 'right', 0, fField)],
                         attachPosition = [(textField, 'right', 0, fieldLength),
                                           (exPose, 'right', 0, 50 )] )
        cmds.setParent( '..' )
        
        ExportUIInfo._textField = textField.split( '|' )[-1]
        ExportUIInfo._floatField = fField.split( '|' )[-1]
        
        return form



class ImportUI:
    
    def __init__(self):
        
        pass
    
    
    def create(self):
        
        buttonLeftSpace = ImportUIInfo._buttonLeft
        
        form = cmds.formLayout()
        
        text   = cmds.text( l='IMPORT TARGET : ', h=22 )
        
        textField = cmds.textField( h=22 )
        cmds.popupMenu()
        cmds.menuItem( l='Load Selected', c=ImportUIInfo.cmdLoadSelected )
        
        imButton = cmds.button( l='Import', c=ImportUIInfo.cmdImport )
        flipCheck = cmds.checkBox( l='Flip', h=25 )
        frameField = cmds.floatFieldGrp( l='Min/Max', nf=2, value1=1.0, value2=24.0, cw3=(47,50,50), en=0  )
        speedField = cmds.floatFieldGrp( l='Speed/offset', nf=2, value1=1.0, value2=0.0, cw3=(80,50,50), en=0 )
        
        fieldLength = 38
        
        cmds.formLayout( form, e=1, 
                         attachForm= [(text, 'top', 0), (text, 'left', 0),
                                      (textField, 'top', 0),
                                      (imButton, 'top', 0),
                                      (flipCheck, 'top', 0 ),
                                      (speedField, 'top', 0),
                                      (frameField, 'top', 0), (frameField, 'right', 0)],
                         attachControl =  [(textField, 'left', 0, text),
                                           (imButton, 'left', buttonLeftSpace, textField),
                                           (flipCheck, 'left', buttonLeftSpace, imButton),
                                           (speedField, 'right', 0, frameField)],
                         attachPosition = [(textField, 'right', 0, fieldLength),
                                           (imButton, 'right', 0, 50) ] )
        cmds.setParent( '..' )
        
        ImportUIInfo._textField = textField.split( '|' )[-1]
        ImportUIInfo._flipCheck = flipCheck.split( '|' )[-1]
        ImportUIInfo._speedField = speedField.split( '|' )[-1]
        ImportUIInfo._frameField = frameField.split( '|' )[-1]
        
        return form



class BakeUI:
    
    def __init__(self):
        
        pass
    
    
    def create(self):
        
        form = cmds.formLayout( en=0 )
        
        delAniButton = cmds.button( l='Delete Animation', w=255, c=BakeUIInfo.cmdDeleteAnim )
        bakeButton   = cmds.button( l='Bake', w=125, c=BakeUIInfo.cmdBake )
        
        cmds.radioCollection()
        byKeyframe = cmds.radioButton( l='By Keyframe', sl=1, w=100 )
        byFrame    = cmds.radioButton( l='By Frame', w=100 )
        
        cmds.formLayout( form, e=1,
                         attachForm = [ (delAniButton, 'right', 5),
                                        (byKeyframe,'left',0)],
                         attachControl = [ (byFrame, 'left', 0, byKeyframe),
                                           (bakeButton, 'left', 20, byFrame)],
                         attachPosition = [(bakeButton, 'right', 0, 50)] )
        cmds.setParent( '..' )
        
        BakeUIInfo._radio = byKeyframe.split( '|' )[-1]
        BakeUIInfo._form  = form.split( '|' )[-1]

        return form



class UI:
    
    def __init__(self):
        
        self.create()

        
    def create(self):
        
        window = WindowInfo._window
        title  = WindowInfo._title
        width  = WindowInfo._width
        height = WindowInfo._height
        topSpace = WindowInfo._topSpace
        leftSpace = WindowInfo._leftSpace
        rightSpace = WindowInfo._rightSpace
        bottomSpace = WindowInfo._bottomSpace
        hOffset     = WindowInfo._holizonOffset
        imageOffset = WindowInfo._imageOffset
        
        if cmds.window( window, ex=1 ):
            cmds.deleteUI( window )
        cmds.window( window, title=title )
        
        form = cmds.formLayout()
        folderUIInst = FolderUI().create()
        radioUIInst  = RadioUI().create()
        partUIInst   = PartUI().create()
        DetailUIInfo = DetailUI().create()
        bar          = cmds.separator()
        exportUIInst = ExportUI().create()
        importUIInst = ImportUI().create()
        bakeUIInst   = BakeUI().create()
        
        cmds.formLayout( form, e=1, attachForm=[( folderUIInst, 'top', topSpace ),( folderUIInst, 'left', leftSpace ),
                                                ( radioUIInst, 'top', topSpace ) ,( radioUIInst, 'right', rightSpace ),
                                                ( DetailUIInfo, 'right', rightSpace ),
                                                ( exportUIInst, 'left', leftSpace ), ( exportUIInst, 'right', rightSpace ),
                                                ( importUIInst, 'left', leftSpace ), ( importUIInst, 'right', rightSpace ),
                                                ( bar, 'left', leftSpace ), ( bar, 'right', rightSpace ),
                                                ( bakeUIInst, 'left',  leftSpace ), ( bakeUIInst, 'right', rightSpace )],
                                    attachControl = [( partUIInst, 'top', imageOffset, radioUIInst ),
                                                     ( DetailUIInfo, 'top', imageOffset, radioUIInst ), ( DetailUIInfo, 'left', imageOffset, partUIInst ),
                                                     ( bar, 'top', imageOffset, partUIInst ),
                                                     ( exportUIInst, 'top', topSpace, bar ),
                                                     ( importUIInst, 'top', topSpace, exportUIInst ),
                                                     ( folderUIInst, 'bottom', imageOffset, bar ),
                                                     ( bakeUIInst, 'top', topSpace, importUIInst) ],
                                    attachPosition = [ ( folderUIInst, 'right', hOffset/2, 43 ), 
                                                       ( radioUIInst, 'left', hOffset/2, 43 ),
                                                       ( partUIInst, 'left', hOffset/2, 43 ),
                                                       ( bakeUIInst, 'left', hOffset/2, 0 ) ] )
        cmds.setParent( '..' )
        
        cmds.window( window, e=1, w=width, h=height )
        