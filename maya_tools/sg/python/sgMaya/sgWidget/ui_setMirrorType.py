#coding=utf8

from maya import cmds
from sgModules import sgHumanRigCommands
import os, json



def makeFolder( pathName ):
    if os.path.exists( pathName ):return None
    os.makedirs( pathName )
    return pathName



class InfoAttrs:
    
    origNameAttr = 'rig_origName'
    parentAttr   = 'rig_parents'
    reverseAttrs = 'rig_reverseAttrs'
    sidePrefixAttr = 'rig_sidePrefix'
    outerMatrixAttr= 'rig_outerMatrix'
    innerMatrixAttr= 'rig_innerMatrix'
    
    leftPrefixList = ['left', 'Left', '_L_']
    rightPrefixList = ['right', 'Right', '_R_']



class Win_Global:
    
    winName = 'sgui_setMirrorType_v01'
    title   = 'UI - Set Mirror Type'
    width = 400
    height = 100
    
    infoPath = cmds.about( pd=1 ) + '/sg/sgui_setMirrorType_v01_info.txt'
    makeFolder( os.path.dirname( infoPath ) )
    
    mirrorTypeList = ['none', 'default', 'center', 'matrix', 'local' ]
    

    @staticmethod
    def saveInfo():
        pass


    @staticmethod
    def loadInfo():
        pass




class Win_Cmd:
    
    @staticmethod
    def addAttr( target, **options ):
    
        items = options.items()
        
        attrName = ''
        channelBox = False
        keyable = False
        for key, value in items:
            if key in ['ln', 'longName']:
                attrName = value
            elif key in ['cb', 'channelBox']:
                channelBox = True
                options.pop( key )
            elif key in ['k', 'keyable']:
                keyable = True 
                options.pop( key )
        
        if cmds.attributeQuery( attrName, node=target, ex=1 ): return None
        
        cmds.addAttr( target, **options )
        
        if channelBox:
            cmds.setAttr( target+'.'+attrName, e=1, cb=1 )
        elif keyable:
            cmds.setAttr( target+'.'+attrName, e=1, k=1 )

    
    
    @staticmethod
    def loadTargetCtl( *args ):
        sels = cmds.ls( sl=1 )
        if not sels: return None
        targetCtl = sels[-1]
        cmds.textField( Win_Global.txf_targetCtl, e=1, tx=targetCtl )

        if cmds.attributeQuery( InfoAttrs.parentAttr, node=targetCtl, ex=1 ):
            parentNameStr = cmds.getAttr( targetCtl + '.' + InfoAttrs.parentAttr )
            cmds.textField( Win_Global.txf_parentAttr, e=1, tx=parentNameStr )
        else:
            cmds.textField( Win_Global.txf_parentAttr, e=1, tx='' )

        if cmds.attributeQuery( InfoAttrs.sidePrefixAttr, node=targetCtl, ex=1 ):
            sidePrefixStr = cmds.getAttr( targetCtl + '.' + InfoAttrs.sidePrefixAttr )
            cmds.textField( Win_Global.txf_sidePrefixAttr, e=1, tx=sidePrefixStr )
        else:
            cmds.textField( Win_Global.txf_sidePrefixAttr, e=1, tx='' )

        if cmds.attributeQuery( InfoAttrs.reverseAttrs, node=targetCtl, ex=1 ):
            revereAttrStr = cmds.getAttr( targetCtl + '.' + InfoAttrs.reverseAttrs )
            cmds.textField( Win_Global.txf_reverseAttrs, e=1, tx=revereAttrStr )
        else:
            cmds.textField( Win_Global.txf_reverseAttrs, e=1, tx='' )
            
        if cmds.attributeQuery( InfoAttrs.outerMatrixAttr, node=targetCtl, ex=1 ):
            outerMatrixStr = cmds.getAttr( targetCtl + '.' + InfoAttrs.outerMatrixAttr )
            cmds.textField( Win_Global.txf_outerMatrixAttr, e=1, tx=outerMatrixStr )
        else:
            cmds.textField( Win_Global.txf_outerMatrixAttr, e=1, tx='' )
            
        if cmds.attributeQuery( InfoAttrs.innerMatrixAttr, node=targetCtl, ex=1 ):
            outerMatrixStr = cmds.getAttr( targetCtl + '.' + InfoAttrs.innerMatrixAttr )
            cmds.textField( Win_Global.txf_innerMatrixAttr, e=1, tx=outerMatrixStr )
        else:
            cmds.textField( Win_Global.txf_innerMatrixAttr, e=1, tx='' )

        prefixStr = ''
        for i in range( len( InfoAttrs.leftPrefixList ) ):
            if targetCtl.find( InfoAttrs.leftPrefixList[i] ) != -1:
                prefixStr = InfoAttrs.leftPrefixList[i]
                break
        for i in range( len( InfoAttrs.rightPrefixList ) ):
            if targetCtl.find( InfoAttrs.rightPrefixList[i] ) != -1:
                prefixStr = InfoAttrs.rightPrefixList[i]
                break
        
        cmds.textField( Win_Global.txf_origNameAttr, e=1, tx= targetCtl )
        if prefixStr:
            cmds.textField( Win_Global.txf_sidePrefixAttr, e=1, tx=prefixStr )


    @staticmethod
    def setMirrorType( *args ):
        
        targetCtl = cmds.textField( Win_Global.txf_targetCtl, q=1, tx=1 )
        
        origNameAttrValue = cmds.textField( Win_Global.txf_origNameAttr, q=1, tx=1 )
        parentAttrValue = cmds.textField( Win_Global.txf_parentAttr, q=1, tx=1 )
        sidePrefixAttrValue = cmds.textField( Win_Global.txf_sidePrefixAttr, q=1, tx=1 )
        reverseAttrsValue = cmds.textField( Win_Global.txf_reverseAttrs, q=1, tx=1 )
        outerMatrixAttrValue = cmds.textField( Win_Global.txf_outerMatrixAttr, q=1, tx=1 )
        innerMatrixAttrValue = cmds.textField( Win_Global.txf_innerMatrixAttr, q=1, tx=1 )
        
        Win_Cmd.addAttr( targetCtl, ln=InfoAttrs.origNameAttr, dt='string' )
        Win_Cmd.addAttr( targetCtl, ln=InfoAttrs.parentAttr, dt='string' )
        Win_Cmd.addAttr( targetCtl, ln=InfoAttrs.sidePrefixAttr, dt='string' )
        Win_Cmd.addAttr( targetCtl, ln=InfoAttrs.reverseAttrs, dt='string' )
        Win_Cmd.addAttr( targetCtl, ln=InfoAttrs.outerMatrixAttr, dt='string' )
        Win_Cmd.addAttr( targetCtl, ln=InfoAttrs.innerMatrixAttr, dt='string' )
        
        cmds.setAttr( targetCtl + '.' + InfoAttrs.origNameAttr, origNameAttrValue, type='string' )
        cmds.setAttr( targetCtl + '.' + InfoAttrs.parentAttr, parentAttrValue, type='string' )
        cmds.setAttr( targetCtl + '.' + InfoAttrs.sidePrefixAttr, sidePrefixAttrValue, type='string' )
        cmds.setAttr( targetCtl + '.' + InfoAttrs.reverseAttrs, reverseAttrsValue, type='string' )
        cmds.setAttr( targetCtl + '.' + InfoAttrs.outerMatrixAttr, outerMatrixAttrValue, type='string' )
        cmds.setAttr( targetCtl + '.' + InfoAttrs.innerMatrixAttr, innerMatrixAttrValue, type='string' )
        
        prefixStr = ''
        otherPrefixStr = ''
        otherSideCtl = ''
        for i in range( len( InfoAttrs.leftPrefixList ) ):
            if targetCtl.find( InfoAttrs.leftPrefixList[i] ) != -1:
                prefixStr = InfoAttrs.leftPrefixList[i]
                otherPrefixStr = InfoAttrs.rightPrefixList[i]
                otherSideCtl = targetCtl.replace( InfoAttrs.leftPrefixList[i], InfoAttrs.rightPrefixList[i] )
                break
        for i in range( len( InfoAttrs.rightPrefixList ) ):
            if targetCtl.find( InfoAttrs.rightPrefixList[i] ) != -1:
                prefixStr = InfoAttrs.rightPrefixList[i]
                otherPrefixStr = InfoAttrs.leftPrefixList[i]
                otherSideCtl = targetCtl.replace( InfoAttrs.rightPrefixList[i], InfoAttrs.leftPrefixList[i] )
                break
        
        if otherSideCtl:
            Win_Cmd.addAttr( otherSideCtl, ln=InfoAttrs.origNameAttr, dt='string' )
            Win_Cmd.addAttr( otherSideCtl, ln=InfoAttrs.parentAttr, dt='string' )
            Win_Cmd.addAttr( otherSideCtl, ln=InfoAttrs.sidePrefixAttr, dt='string' )
            Win_Cmd.addAttr( otherSideCtl, ln=InfoAttrs.reverseAttrs, dt='string' )
            Win_Cmd.addAttr( otherSideCtl, ln=InfoAttrs.outerMatrixAttr, dt='string' )
            Win_Cmd.addAttr( otherSideCtl, ln=InfoAttrs.innerMatrixAttr, dt='string' )
            cmds.setAttr( otherSideCtl + '.' + InfoAttrs.origNameAttr, origNameAttrValue.replace( prefixStr,otherPrefixStr), type='string' )
            cmds.setAttr( otherSideCtl + '.' + InfoAttrs.parentAttr, parentAttrValue.replace( prefixStr,otherPrefixStr), type='string' )
            cmds.setAttr( otherSideCtl + '.' + InfoAttrs.sidePrefixAttr, otherPrefixStr, type='string' )
            cmds.setAttr( otherSideCtl + '.' + InfoAttrs.reverseAttrs, reverseAttrsValue, type='string' )
            cmds.setAttr( otherSideCtl + '.' + InfoAttrs.outerMatrixAttr, outerMatrixAttrValue, type='string' )
            cmds.setAttr( otherSideCtl + '.' + InfoAttrs.innerMatrixAttr, innerMatrixAttrValue, type='string' )
    
    
    @staticmethod
    def testFlip( *args ):
        target = cmds.textField( Win_Global.txf_targetCtl, q=1, tx=1 )
        rigControl = sgHumanRigCommands.RigControllerControl( target )
        rigControl.setFlip()
    
    
    @staticmethod
    def loadParentCtls( *args ):
        cmds.textField( Win_Global.txf_parentAttr, e=1, tx= ','.join( cmds.ls( sl=1 ) ) )
    
    
    @staticmethod
    def getReverseMatrixStr( *args ):
        cmds.textField( args[0], e=1, tx = str( [-1,0,0,0, 0,-1,0,0, 0,0,-1,0, 0,0,0,1] ) )
    
    @staticmethod
    def getXRotateMatrixStr( *args ):
        cmds.textField( args[0], e=1, tx = str( [1,0,0,0, 0,-1,0,0, 0,0,-1,0, 0,0,0,1] ) )
    
    @staticmethod
    def getYRotateMatrixStr( *args ):
        cmds.textField( args[0], e=1, tx = str( [-1,0,0,0, 0,1,0,0, 0,0,-1,0, 0,0,0,1] ) )
    
    @staticmethod
    def getZRotateMatrixStr( *args ):
        cmds.textField( args[0], e=1, tx = str( [1,0,0,0, 0,-1,0,0, 0,0,-1,0, 0,0,0,1] ) )
    
    @staticmethod
    def getXMirrorMatrixStr( *args ):
        cmds.textField( args[0], e=1, tx = str( [-1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1] ) )
        
    @staticmethod
    def getYMirrorMatrixStr( *args ):
        cmds.textField( args[0], e=1, tx = str( [1,0,0,0, 0,-1,0,0, 0,0,1,0, 0,0,0,1] ) )
    
    @staticmethod
    def getZMirrorMatrixStr( *args ):
        cmds.textField( args[0], e=1, tx = str( [1,0,0,0, 0,1,0,0, 0,0,-1,0, 0,0,0,1] ) )
        




class UI_targetCtl:
    
    def __init__(self):
        
        pass


    
    def create(self):
        
        form = cmds.formLayout()
        text = cmds.text( l='Target Ctl : ', al='right', h=25, w=80 )
        txf  = cmds.textField( h=25 )
        button = cmds.button( l='Load', h=25, w=80, c= Win_Cmd.loadTargetCtl ) 
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af=[ (text, 'top', 0 ), (text, 'left', 0 ), 
                              (txf, 'top', 0 ),
                              (button, 'top', 0 ), (button, 'right', 0 ) ],
                         ac=[ (txf, 'left', 0, text ), (txf, 'right', 0, button ) ] )
        
        Win_Global.txf_targetCtl = txf
        
        return form



class UI_infomation:
    
    def __init__(self, infoAttrName ):
        
        self.infoAttrName = infoAttrName
    
    
    def create(self):
        
        form = cmds.formLayout()
        text = cmds.text( l= self.infoAttrName, w=100, al='right' )
        txf  = cmds.textField()
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af = [( text, 'top', 0 ), ( text, 'left', 0 ), ( text, 'bottom', 0 ),
                               ( txf, 'top', 0 ), ( txf, 'right', 0 ), ( txf, 'bottom', 0 )],
                         ac = [( txf, 'left', 5, text )] )
        
        self.txf = txf
        
        return form





class UI_infomations:
    
    def __init__(self):
        
        self.ui_origName     = UI_infomation( InfoAttrs.origNameAttr )
        self.ui_parents      = UI_infomation( InfoAttrs.parentAttr )
        self.ui_reverseAttrs = UI_infomation( InfoAttrs.reverseAttrs )
        self.ui_sidePrefix   = UI_infomation( InfoAttrs.sidePrefixAttr )
        self.ui_outerMatrix = UI_infomation( InfoAttrs.outerMatrixAttr )
        self.ui_innerMatrix = UI_infomation( InfoAttrs.innerMatrixAttr )
    
    
    def create(self):
        
        frame = cmds.frameLayout( bv=1, lv=0 )
        form = cmds.formLayout()
        
        form_origName   = self.ui_origName.create()
        form_parents    = self.ui_parents.create()
        form_sidePrefix = self.ui_sidePrefix.create()
        form_reverseAttrs   = self.ui_reverseAttrs.create()
        form_outerMatrix   = self.ui_outerMatrix.create()
        form_innerMatrix   = self.ui_innerMatrix.create()
        
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[(form_origName, 'top', 5), (form_origName, 'left', 5), (form_origName, 'right', 5),
                             (form_parents, 'left', 5), (form_parents, 'right', 5), 
                             (form_sidePrefix, 'left', 5), (form_sidePrefix, 'right', 5), 
                             (form_reverseAttrs, 'left', 5), (form_reverseAttrs, 'right', 5), 
                             (form_outerMatrix, 'left', 5), (form_outerMatrix, 'right', 5),
                             (form_innerMatrix, 'left', 5), (form_innerMatrix, 'right', 5), (form_innerMatrix, 'bottom', 5)],
                         ac=[(form_parents, 'top', 5, form_origName ),
                             (form_sidePrefix, 'top', 5, form_parents ),
                             (form_reverseAttrs, 'top', 5, form_sidePrefix ),
                             (form_outerMatrix, 'top', 5, form_reverseAttrs ),
                             (form_innerMatrix, 'top', 5, form_outerMatrix )],
                         ap=[] )
        
        Win_Global.txf_origNameAttr = self.ui_origName.txf
        Win_Global.txf_parentAttr = self.ui_parents.txf
        Win_Global.txf_sidePrefixAttr = self.ui_sidePrefix.txf
        Win_Global.txf_reverseAttrs = self.ui_reverseAttrs.txf
        Win_Global.txf_outerMatrixAttr = self.ui_outerMatrix.txf
        Win_Global.txf_innerMatrixAttr = self.ui_innerMatrix.txf
        
        return frame
        



class UI_Buttons:
    
    def __init__(self):
        
        pass
    
    
    def create(self):
        
        form = cmds.formLayout()
        btSet  = cmds.button( l='Set', c=Win_Cmd.setMirrorType )
        btTest = cmds.button( l='Test Flip', c=Win_Cmd.testFlip )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af = [( btSet, 'top', 0 ), ( btSet, 'left', 0 ),
                               ( btTest, 'top', 0 ), ( btTest, 'right', 0 )],
                         ap = [( btSet, 'right', 2, 50 ), ( btTest, 'left', 2, 50 )] )
        
        return form


    
        

class Win:
    
    def __init__(self ):
        
        self.ui_targetCtl    = UI_targetCtl()
        self.ui_infomation = UI_infomations()
        self.ui_buttons    = UI_Buttons()

    
    def create(self):
        
        if cmds.window( Win_Global.winName, q=1, ex=1 ):
            cmds.deleteUI( Win_Global.winName )
        
        cmds.window( Win_Global.winName, title= Win_Global.title )
        
        formOuter = cmds.formLayout()
        targetCtlForm = self.ui_targetCtl.create()
        infomationForm = self.ui_infomation.create()
        buttonsForm = self.ui_buttons.create()
        cmds.setParent( '..' )

        cmds.formLayout( formOuter, e=1, 
                         af=[( targetCtlForm, 'top', 5 ), ( targetCtlForm, 'left', 5 ), ( targetCtlForm, 'right', 5 ),
                             ( infomationForm, 'left', 5 ), ( infomationForm, 'right', 5 ),
                             ( buttonsForm, 'left', 5 ), ( buttonsForm, 'right', 5 ), ( buttonsForm, 'bottom', 5 ) ],
                         ac=[( infomationForm, 'top', 5, targetCtlForm ),
                             ( buttonsForm, 'top', 5, infomationForm )] )
        
        cmds.window( Win_Global.winName, e=1, width = Win_Global.width, height= Win_Global.height )
        cmds.showWindow( Win_Global.winName )
        
        Win_Global.loadInfo()
        
        cmds.popupMenu( p=Win_Global.txf_parentAttr )
        cmds.menuItem( l='Load Parent Controller', c= Win_Cmd.loadParentCtls )
        
        from functools import partial
        
        for txf in [Win_Global.txf_outerMatrixAttr,Win_Global.txf_innerMatrixAttr]:
            cmds.popupMenu( p=txf )
            cmds.menuItem( l='Reverse Matrix', c= partial( Win_Cmd.getReverseMatrixStr, txf ) )
            cmds.menuItem( l='XRot Matrix', c= partial( Win_Cmd.getXRotateMatrixStr, txf ) )
            cmds.menuItem( l='YRot Matrix', c= partial( Win_Cmd.getYRotateMatrixStr, txf ) )
            cmds.menuItem( l='ZRot Matrix', c= partial( Win_Cmd.getZRotateMatrixStr, txf ) )
            cmds.menuItem( l='XMirror Matrix', c= partial( Win_Cmd.getXMirrorMatrixStr, txf ) )
            cmds.menuItem( l='YMirror Matrix', c= partial( Win_Cmd.getYMirrorMatrixStr, txf ) )
            cmds.menuItem( l='ZMirror Matrix', c= partial( Win_Cmd.getZMirrorMatrixStr, txf ) )
        
        
        
        
        
        
        
    