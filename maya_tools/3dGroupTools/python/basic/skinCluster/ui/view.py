import maya.cmds as cmds
from functools import partial
from uiModel import *
from cmdModel import *
import model


def cmdNone( *args ):
        
    pass




class BindSkinView:
    
    def __init__(self):
        
        self._cmdBindSkin  = cmdNone
        self._cmdSelectInfluence = cmdNone
        self._cmdPaintWeightTool = cmdNone
        self._cmdSetSkinMatrixDefault = cmdNone
        
    
    def create(self):
        
        form = cmds.formLayout()
        
        height = SmoothBindModel._buttonHeight
        
        bindSkin = cmds.button( l='Bind Skin', h=height, c=self._cmdBindSkin )
        selectInfluence = cmds.button( l='Select Influence', h=height, c=self._cmdSelectInfluence )
        paintWeight     = cmds.button( l='Paint Weight', h=height, c=self._cmdPaintWeightTool )
        skinDefault     = cmds.button( l='Set Skin Matrix Default', h=height, c=self._cmdSetSkinMatrixDefault )

        cmds.formLayout( form, e=1,
                         af=[(bindSkin, 'top', 0), (bindSkin, 'left', 0), (bindSkin, 'right', 0),
                             (selectInfluence, 'left', 0), (selectInfluence, 'right', 0),
                             (paintWeight, 'left', 0), (paintWeight, 'right', 0),
                             (skinDefault, 'left', 0), (skinDefault, 'right', 0)],
                         ac=[(selectInfluence,'top',0,bindSkin),
                             (paintWeight,'top',0,selectInfluence),
                             (skinDefault,'top',0,paintWeight)] )
        cmds.setParent( '..' )
        
        return form
        


class LockView:
    
    def __init__(self):
        
        self._cmdLockAll    = cmdNone
        self._cmdUnlockAll  = cmdNone
        self._cmdLockSel    = cmdNone
        self._cmdUnlockSel  = cmdNone
        self._cmdLockOSel   = cmdNone
        self._cmdUnlockOSel = cmdNone
    
    
    def create(self):
        
        form = cmds.formLayout()
        
        height      = LockViewModel._buttonHeight
        leftSpace   = LockViewModel._leftSpace
        rightSpace  = LockViewModel._rightSpace
        buttonSpace = LockViewModel._buttonSpace
        
        lockAll   = cmds.button( l='Lock All', h=height, c=self._cmdLockAll )
        unlockAll = cmds.button( l='Unlock All', h=height, c=self._cmdUnlockAll )
        
        lockSel   = cmds.button( l='Lock Sel', h=height, c=self._cmdLockSel )
        unlockSel = cmds.button( l='Unlock Sel', h=height, c=self._cmdUnlockSel )
        
        lockOnlySel   = cmds.button( l='Lock Only Sel', h=height, c=self._cmdLockOSel )
        unlockOnlySel = cmds.button( l='Unlock Only Sel', h=height, c=self._cmdUnlockOSel )
        
        cmds.formLayout( form, e=1,
                         af=[(lockAll, 'top', 0), (unlockAll, 'top', 0),
                             (lockAll, 'left', leftSpace), (unlockAll, 'right', rightSpace),
                             (lockSel, 'left', leftSpace), (unlockSel, 'right', rightSpace), 
                             (lockOnlySel, 'left', leftSpace), (unlockOnlySel, 'right', rightSpace)],
                        
                         ac=[(lockSel, 'top', buttonSpace, lockAll ), (unlockSel, 'top', buttonSpace, unlockAll ),
                             (lockOnlySel, 'top', buttonSpace, lockSel ), (unlockOnlySel, 'top', buttonSpace, unlockSel )],
                         ap=[(lockAll,'right',0,50), (unlockAll,'left',0,50),
                             (lockSel,'right',0,50), (unlockSel,'left',0,50),
                             (lockOnlySel,'right',0,50), (unlockOnlySel,'left',0,50)] )
        cmds.setParent( '..' )
        
        return form



class MirrorWeightView:
    
    def __init__(self):
        
        self._cmdWToL   = cmdNone
        self._cmdWToR   = cmdNone
    
    
    def create(self):
        
        topSpace = WeightViewModel._topSpace
        bottomSpace = WeightViewModel._bottomSpace
        leftSpace   = WeightViewModel._leftSpace
        rightSpace  = WeightViewModel._rightSpace
        buttonSpace = WeightViewModel._buttonSpace
        
        form = cmds.formLayout()
        
        mirrorToR = cmds.button( l='W to R >>', c=self._cmdWToL )
        mirrorToL = cmds.button( l='<< W to L', c=self._cmdWToR )
        
        cmds.formLayout( form, e=1,
                         af=[(mirrorToR, 'left', leftSpace),  (mirrorToR, 'top', topSpace), (mirrorToR, 'bottom', bottomSpace),
                             (mirrorToL, 'right', rightSpace),(mirrorToL, 'top', topSpace), (mirrorToL, 'bottom', bottomSpace)],
                         ap=[(mirrorToR, 'right', buttonSpace*0.5, 50 ), (mirrorToL, 'left', buttonSpace*0.5, 50)] )
        cmds.setParent( '..' )
        
        return form
    


class WeightView:
    
    def __init__(self):
        
        self._cmdCopyVtxW    = cmdNone
        self._cmdPastVtxW    = cmdNone
        self._cmdHammer      = cmdNone
        self._cmdSmoothBrush = cmdNone
        self._cmdHardBrush   = cmdNone
        
    def create(self):
        
        buttonHeight = WeightViewModel._buttonHeight
        topSpace = WeightViewModel._topSpace
        bottomSpace = WeightViewModel._bottomSpace
        leftSpace   = WeightViewModel._leftSpace
        rightSpace  = WeightViewModel._rightSpace
        buttonSpace = WeightViewModel._buttonSpace
        
        form = cmds.formLayout()
        
        copyVtxW = cmds.button( "COPY VTX W", c=self._cmdCopyVtxW, h=buttonHeight )
        pastVtxW = cmds.button( "PAST VTX W", c=self._cmdPastVtxW, h=buttonHeight )
        hammer   = cmds.button( "Weight Hammer", c=self._cmdHammer, h=buttonHeight )
        smoothBrush = cmds.button( "Weight Smooth Brush", c=self._cmdSmoothBrush )
        hardBrush   = cmds.button( "Weight Hard Brush", c=self._cmdHardBrush )
        
        cmds.formLayout( form, e=1,
                         af=[( pastVtxW, 'top',  topSpace ),  ( copyVtxW, 'top',  topSpace ),
                             ( pastVtxW, 'left', leftSpace ), ( copyVtxW, 'right', rightSpace ),
                             ( hammer, 'left', leftSpace ), ( hammer, 'right', rightSpace ),
                             ( smoothBrush, 'left', leftSpace ), ( smoothBrush, 'right', rightSpace ),
                             ( hardBrush, 'left', leftSpace ), ( hardBrush, 'right', rightSpace ), ( hardBrush, 'bottom', bottomSpace )],
                         ac=[( hammer, 'top', buttonSpace*0.5 , pastVtxW ),
                             ( smoothBrush, 'top', buttonSpace*0.5 , hammer ),
                             ( hardBrush, 'top',  buttonSpace*0.5 , smoothBrush )],
                         ap=[( pastVtxW, 'right', buttonSpace*0.5 , 50 ),
                             ( copyVtxW, 'left',  buttonSpace*0.5 , 50 )] )
        
        cmds.setParent( '..' )
        
        return form
    
    
class ExportImportView:
    
    def __init__(self):
        
        self._cmdExportWeight = cmdNone
        self._cmdImportWeight = cmdNone
        self._cmdCopyWeight   = cmdNone
        
    def create(self):
        
        buttonHeight = ExportImportModel._buttonHeight
        
        form = cmds.formLayout()
        
        buttonExport     = cmds.button( l='Export Weight', c=self._cmdExportWeight, h=buttonHeight )
        buttonImport     = cmds.button( l='Import Weight', c=self._cmdImportWeight, h=buttonHeight )
        buttonCopyWeight = cmds.button( l='Copy Weight'  , c=self._cmdCopyWeight, h=buttonHeight   )
        
        cmds.formLayout( form, e=1, 
                         af=[( buttonExport, 'top', 0 ), ( buttonExport, 'left', 0 ), ( buttonExport, 'right', 0 ),
                             ( buttonImport, 'left', 0 ), ( buttonImport, 'right', 0 ),
                             ( buttonCopyWeight, 'bottom', 0 ), ( buttonCopyWeight, 'left', 0 ), ( buttonCopyWeight, 'right', 0 )],
                         ac=[( buttonExport, 'top', 0, buttonImport ), 
                             ( buttonCopyWeight, 'top', 0, buttonExport )] )
        cmds.setParent( '..' )
        
        return form
    
    


class InfluenceView:
    
    def __init__(self):
        
        self._cmdRemoveUnuseed = cmdNone
        self._cmdRemoveInfluence = cmdNone
        self._cmdAddInfluence   = cmdNone
        self._cmdRemoveCrossWeights = cmdNone
    
    
    def create(self):
        
        #buttonHeight = InfluenceModel._buttonHeight
        
        form = cmds.formLayout()
        buttonRemoveUnused = cmds.button( l='Remove Unused Influence', c=self._cmdRemoveUnuseed )
        buttonRemoveSelected = cmds.button( l='Remove Influence', c=self._cmdRemoveInfluence )
        buttonAddInfluence   = cmds.button( l='Add Influence', c=self._cmdAddInfluence )
        
        cmds.formLayout( form, e=1,
                         af=[(buttonRemoveUnused, 'left', 0), (buttonRemoveUnused, 'right', 0),
                             (buttonRemoveSelected, 'left', 0), (buttonRemoveSelected, 'right', 0),
                             (buttonAddInfluence, 'left', 0), (buttonAddInfluence, 'right', 0), (buttonAddInfluence, 'top', 0)],
                         ac=[(buttonRemoveSelected,'top',0,buttonAddInfluence),
                             (buttonRemoveUnused,'top',0,buttonRemoveSelected)])
        cmds.setParent( '..' )
        
        return form




class UIView:
    
    _cmdClose = cmdNone
    _bindSkinView = BindSkinView()
    _lockView = LockView()
    _mirrorWeightView = MirrorWeightView()
    _weightView = WeightView()
    _exportImportView = ExportImportView()
    _influenceView = InfluenceView()
    
    def __init__(self):
        
        pass
    
    @staticmethod
    def deleteUI( *args ):
        
        cmds.deleteUI( UIModel._winName, wnd=1 )

    
    def show(self):
        
        separateSpace = UIModel._separateSpace
        buttonHeight  = UIModel._buttonHeight
        
        if cmds.window( UIModel._winName, ex=1 ):
            cmds.deleteUI( UIModel._winName, wnd=1 )
        cmds.window( UIModel._winName, title=UIModel._title, titleBarMenu= False )
        
        form = cmds.formLayout()
        
        topSpaceView = cmds.text( l='', h=5 )
        bindSkinView = self._bindSkinView.create()
        lockView   = self._lockView.create()
        mirrorWeightView = self._mirrorWeightView.create()
        weightView = self._weightView.create()
        influenceView = self._influenceView.create()
        exportImportView = self._exportImportView.create()
        buttomSpaceView = cmds.text( l='', h=5 )
        
        closeButton = cmds.button( l='CLOSE', c=self._cmdClose, h=buttonHeight )
        
        cmds.formLayout( form, e=1,
                         af=[(topSpaceView,'top',0),
                             (bindSkinView,'left',5), (bindSkinView,'right',5),
                             (lockView, 'left', 5), (lockView, 'right', 5),
                             (mirrorWeightView, 'left', 5), (mirrorWeightView, 'right', 5),
                             (weightView, 'left', 5), (weightView, 'right', 5),
                             (influenceView, 'left', 5), (influenceView, 'right', 5),
                             (exportImportView,'left',5),(exportImportView,'right',5),
                             (closeButton, 'left', 5), (closeButton, 'right', 5)],
                        
                         ac=[(bindSkinView, 'top', 0, topSpaceView),
                             (lockView, 'top', separateSpace, bindSkinView),
                             (weightView, 'top', separateSpace, lockView),
                             (mirrorWeightView, 'top', separateSpace, weightView),
                             (influenceView, 'top', separateSpace, mirrorWeightView),
                             (exportImportView, 'top', separateSpace, influenceView),
                             (closeButton, 'top', 10, exportImportView),
                             (buttomSpaceView,'top',0,closeButton)] )
        
        cmds.setParent( '..' )
        
        width = UIModel._width
        height = UIModel._height
        
        cmds.window( UIModel._winName, e=1, w= width, h= height )
        cmds.showWindow( UIModel._winName )




class ShowSkinWeightEditUIControl:
    
    def __init__(self):

        for melFile in model.melFiles:
            mel.eval( 'source "%s"' % melFile )
    
    
    def showUI(self):
        
        UIView().show()
        
        
    def setCmd(self):
        
        UIView._bindSkinView._cmdBindSkin = cmdSmoothBind.smoothBind
        UIView._bindSkinView._cmdSelectInfluence = cmdSmoothBind.setJointSelectInfluence
        UIView._bindSkinView._cmdPaintWeightTool = cmdSmoothBind.ArtPaintSkinWeightsTool
        UIView._bindSkinView._cmdSetSkinMatrixDefault = cmdSmoothBind.setSkinMatrixDefault
        
        UIView._lockView._cmdLockAll = CmdLock.lockAll
        UIView._lockView._cmdUnlockAll = CmdLock.unlockAll
        UIView._lockView._cmdLockSel= CmdLock.lockSel
        UIView._lockView._cmdUnlockSel = CmdLock.unlockSel
        UIView._lockView._cmdLockOSel = CmdLock.lockOSel
        UIView._lockView._cmdUnlockOSel = CmdLock.unlockOSel
        
        UIView._mirrorWeightView._cmdWToL = CmdMirrorWeight.weightToL
        UIView._mirrorWeightView._cmdWToR = CmdMirrorWeight.weightToR
        UIView._weightView._cmdCopyVtxW = CmdWeight.copyVtxW
        UIView._weightView._cmdPastVtxW = CmdWeight.pastVtxW
        UIView._weightView._cmdHammer = CmdWeight.weightHammer
        UIView._weightView._cmdSmoothBrush = CmdHammerBrush.doCmd
        UIView._weightView._cmdHardBrush = CmdHardBrush.doCmd
        UIView._influenceView._cmdAddInfluence = CmdInfluence.addInfluence
        UIView._influenceView._cmdRemoveInfluence = CmdInfluence.removeInfluence
        UIView._influenceView._cmdRemoveUnuseed = CmdInfluence.removeUnused
        UIView._influenceView._cmdRemoveCrossWeights = CmdInfluence.removeCrossWeightInfluence
        UIView._exportImportView._cmdExportWeight = CmdExportImport.export
        UIView._exportImportView._cmdImportWeight = CmdExportImport.cmdImport
        UIView._exportImportView._cmdCopyWeight   = CmdExportImport.cmdCopyWeight
        
        UIView._cmdClose = UIView.deleteUI