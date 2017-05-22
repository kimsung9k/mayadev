from maya import cmds
from sgModules import sgHumanRigCommands
import os, json



def makeFolder( pathName ):
    
    pathName = pathName.replace( '\\', '/' )
    splitPaths = pathName.split( '/' )
    
    cuPath = splitPaths[0]
    
    folderExist = True
    for i in range( 1, len( splitPaths ) ):
        checkPath = cuPath+'/'+splitPaths[i]
        if not os.path.exists( checkPath ):
            os.chdir( cuPath )
            os.mkdir( splitPaths[i] )
            folderExist = False
        cuPath = checkPath
        
    if folderExist: return None
        
    return pathName



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
    
    parentAttr    = 'ctlParent'
    otherSideAttr = 'ctlOtherSide'
    reverseAttrsAttr = 'ctlReverseAttrs'
    mirrorTypeAttr   = 'ctlMirrorType'
    
    @staticmethod
    def loadBaseCtl( *args ):
        sels = cmds.ls( sl=1 )
        if not sels: return None
        cmds.textField( Win_Global.txf_base, e=1, tx=sels[0] )
        
        otherSideCtl = ''
        otherSideCtlStr = ''
        if sels[0].find( '_L_' ) != -1:
            otherSideCtl = sels[0].replace( '_L_', '_R_' )
        if sels[0].find( '_R_' ) != -1:
            otherSideCtl = sels[0].replace( '_R_', '_L_' )
        
        if cmds.objExists( otherSideCtl ):
            otherSideCtlStr = otherSideCtl
        
        parentCtlStr = ''
        mirrorTypeStr = ''
        if cmds.attributeQuery( Win_Cmd.parentAttr, node=sels[0], ex=1 ):
            parentCtlStr = cmds.getAttr( sels[0] + '.' + Win_Cmd.parentAttr )
        if cmds.attributeQuery( Win_Cmd.otherSideAttr, node=sels[0], ex=1 ):
            otherSideCtlStr = cmds.getAttr( sels[0] + '.' + Win_Cmd.otherSideAttr )
        if cmds.attributeQuery( Win_Cmd.mirrorTypeAttr, node=sels[0], ex=1 ):
            mirrorTypeStr = cmds.getAttr( sels[0] + '.' + Win_Cmd.mirrorTypeAttr )
        
        mirrorTypeSplits = mirrorTypeStr.split( ',' )
        
        cmds.textField( Win_Global.txf_parent, e=1, tx=parentCtlStr )
        cmds.textField( Win_Global.txf_otherSide, e=1, tx=otherSideCtlStr )
        if mirrorTypeStr:
            cmds.optionMenu( Win_Global.options, e=1, sl= Win_Global.mirrorTypeList.index( mirrorTypeSplits[0] ) + 1 )
        cmds.textField( Win_Global.txf_mirrorType, e=1, tx= ','.join( mirrorTypeSplits[1:] ) )


    @staticmethod
    def loadParentCtl( *args ):        
        sels = cmds.ls( sl=1 )
        if not sels: return None
        selsStr = ','.join( sels )
        cmds.textField( Win_Global.txf_parent, e=1, tx=selsStr )
    
    
    @staticmethod
    def loadOtherSide( *args ):
        
        sels = cmds.ls( sl=1 )
        if not sels: return None
        cmds.textField( Win_Global.txf_otherSide, e=1, tx=sels[0] )


    @staticmethod
    def setMirrorType( *args ):
        
        targetCtl      = cmds.textField( Win_Global.txf_base, q=1, tx=1 )
        parentCtls     = cmds.textField( Win_Global.txf_parent, q=1, tx=1 )
        otherSideCtl   = cmds.textField( Win_Global.txf_otherSide, q=1, tx=1 )
        mirrorTypeStr  = Win_Global.mirrorTypeList[ cmds.optionMenu( Win_Global.options, q=1, sl=1 )-1]
        mirrorTypeStrOther = cmds.textField( Win_Global.txf_mirrorType, q=1, tx=1 )
        
        if mirrorTypeStrOther:
            mirrorTypeStrs = mirrorTypeStr + ',' + mirrorTypeStrOther
        else:
            mirrorTypeStrs = mirrorTypeStr
        
        if not cmds.attributeQuery( Win_Cmd.parentAttr, node=targetCtl, ex=1 ):
            cmds.addAttr( targetCtl, ln=Win_Cmd.parentAttr, dt='string' )
        cmds.setAttr( targetCtl + '.' + Win_Cmd.parentAttr, parentCtls, type='string' )
        if not cmds.attributeQuery( Win_Cmd.otherSideAttr, node=targetCtl, ex=1 ):
            cmds.addAttr( targetCtl, ln=Win_Cmd.otherSideAttr, dt='string' )
        cmds.setAttr( targetCtl + '.' + Win_Cmd.otherSideAttr, otherSideCtl, type='string' )
        if not cmds.attributeQuery( Win_Cmd.mirrorTypeAttr, node=targetCtl, ex=1 ):
            cmds.addAttr( targetCtl, ln=Win_Cmd.mirrorTypeAttr, dt='string' )
        cmds.setAttr( targetCtl + '.' + Win_Cmd.mirrorTypeAttr, mirrorTypeStrs, type='string' )

        if otherSideCtl:
            if not cmds.attributeQuery( Win_Cmd.parentAttr, node=otherSideCtl, ex=1 ):
                cmds.addAttr( otherSideCtl, ln=Win_Cmd.parentAttr, dt='string' )
            otherParentCtls = []
            for parentCtl in [ i.strip() for i in parentCtls.split( ',' ) ]:
                otherParentCtl = ''
                if parentCtl.find( '_L_' ) != -1:
                    otherParentCtl = parentCtl.replace( '_L_', '_R_' )
                elif parentCtl.find( '_R_' ) != -1:
                    otherParentCtl = parentCtl.replace( '_R_', '_L_' )
                otherParentCtls.append(otherParentCtl)
            otherParentCtlString = ','.join( otherParentCtls )
            cmds.setAttr( otherSideCtl + '.' + Win_Cmd.parentAttr, otherParentCtlString, type='string' )
            if not cmds.attributeQuery( Win_Cmd.otherSideAttr, node=otherSideCtl, ex=1 ):
                cmds.addAttr( otherSideCtl, ln=Win_Cmd.otherSideAttr, dt='string' )
            cmds.setAttr( otherSideCtl + '.' + Win_Cmd.otherSideAttr, targetCtl, type='string' )
            if not cmds.attributeQuery( Win_Cmd.mirrorTypeAttr, node=otherSideCtl, ex=1 ):
                cmds.addAttr( otherSideCtl, ln=Win_Cmd.mirrorTypeAttr, dt='string' )
            cmds.setAttr( otherSideCtl + '.' + Win_Cmd.mirrorTypeAttr, mirrorTypeStrs, type='string' )




class UI_baseCtl:
    
    def __init__(self):
        
        pass
    
    
    def create(self):
        
        form = cmds.formLayout()
        text = cmds.text( l='Base Ctl : ', al='right', h=25, w=80 )
        txf  = cmds.textField( h=25 )
        button = cmds.button( l='Load', h=25, w=80, c= Win_Cmd.loadBaseCtl ) 
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af=[ (text, 'top', 0 ), (text, 'left', 0 ), 
                              (txf, 'top', 0 ),
                              (button, 'top', 0 ), (button, 'right', 0 ) ],
                         ac=[ (txf, 'left', 0, text ), (txf, 'right', 0, button ) ] )
        
        Win_Global.txf_base = txf
        
        return form




class UI_ParentStrs:
    
    def __init__(self):
        
        pass
    
    
    def create(self):
        
        form = cmds.formLayout()
        text = cmds.text( l='Parent Ctls : ', al='right', h=22, w=80 )
        txf  = cmds.textField( h=22 )
        button = cmds.button( l='Load', h=22, w=80, c= Win_Cmd.loadParentCtl )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af=[ (text, 'top', 0 ), (text, 'left', 0 ), 
                              (txf, 'top', 0 ),
                              (button, 'top', 0 ), (button, 'right', 0 ) ],
                         ac=[ (txf, 'left', 0, text ), (txf, 'right', 0, button ) ] )
        
        Win_Global.txf_parent = txf
        
        return form




class UI_OtherSideStr:
    
    def __init__(self):
        
        pass
    
    
    def create(self):
        
        form = cmds.formLayout()
        text = cmds.text( l='Other Side Ctl : ', al='right', h=22, w=80 )
        txf  = cmds.textField( h=22 )
        button = cmds.button( l='Load', h=22, w=80, c= Win_Cmd.loadOtherSide )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af=[ (text, 'top', 0 ), (text, 'left', 0 ), 
                              (txf, 'top', 0 ),
                              (button, 'top', 0 ), (button, 'right', 0 ) ],
                         ac=[ (txf, 'left', 0, text ), (txf, 'right', 0, button ) ] )
        
        Win_Global.txf_otherSide = txf
        
        return form



class UI_MirrorType:
    
    def __init__(self):
        
        pass


    def create(self):
        
        form = cmds.formLayout()
        text = cmds.text( l='Mirror Type : ', al='right', h=22, w=80 )
        optionMenu = cmds.optionMenu()
        txf  = cmds.textField( h=22 )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af=[ (text, 'top', 0 ), (text, 'left', 0 ), 
                              (optionMenu, 'top', 0 ),
                              (txf, 'top', 0 ), (txf, 'right', 0 ) ],
                         ac=[ (optionMenu, 'left', 0, text), 
                              (txf, 'left', 0, optionMenu) ] )
        
        Win_Global.txf_mirrorType = txf
        Win_Global.options = optionMenu
        
        for mirrorType in Win_Global.mirrorTypeList:
            cmds.menuItem( mirrorType, p = optionMenu )
        
        return form




class UI_infomation:
    
    def __init__(self):
        
        self.ui_parentStrs = UI_ParentStrs()
        self.ui_otherSideStr = UI_OtherSideStr()
        self.ui_mirrorType = UI_MirrorType()
    
    
    def create(self):
        
        frame = cmds.frameLayout( bv=1, lv=0 )
        form = cmds.formLayout()
        parentStrsForm = self.ui_parentStrs.create()
        otherSideForm  = self.ui_otherSideStr.create()
        mirrorTypeForm = self.ui_mirrorType.create()
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[(parentStrsForm, 'top', 5), (parentStrsForm, 'left', 5), (parentStrsForm, 'right', 5),
                             (otherSideForm, 'left', 5), (otherSideForm, 'right', 5), 
                             (mirrorTypeForm, 'left', 5), (mirrorTypeForm, 'right', 5), (mirrorTypeForm, 'bottom', 5)],
                         ac=[(otherSideForm, 'top', 5, parentStrsForm ),
                             (mirrorTypeForm, 'top', 5, otherSideForm )],
                         ap=[] )
        
        return frame
        



class UI_Buttons:
    
    def __init__(self):
        
        pass
    
    
    def create(self):
        
        form = cmds.formLayout()
        btSet = cmds.button( l='Set', c=Win_Cmd.setMirrorType )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af = [( btSet, 'top', 0 ), ( btSet, 'left', 0 ), ( btSet, 'right', 0 )] )
        
        return form


    
        

class Win:
    
    def __init__(self ):
        
        self.ui_baseCtl    = UI_baseCtl()
        self.ui_infomation = UI_infomation()
        self.ui_buttons    = UI_Buttons()

    
    def create(self):
        
        if cmds.window( Win_Global.winName, q=1, ex=1 ):
            cmds.deleteUI( Win_Global.winName )
        
        cmds.window( Win_Global.winName, title= Win_Global.title )
        
        formOuter = cmds.formLayout()
        baseCtlForm = self.ui_baseCtl.create()
        infomationForm = self.ui_infomation.create()
        buttonsForm = self.ui_buttons.create()
        cmds.setParent( '..' )

        cmds.formLayout( formOuter, e=1, 
                         af=[( baseCtlForm, 'top', 5 ), ( baseCtlForm, 'left', 5 ), ( baseCtlForm, 'right', 5 ),
                             ( infomationForm, 'left', 5 ), ( infomationForm, 'right', 5 ),
                             ( buttonsForm, 'left', 5 ), ( buttonsForm, 'right', 5 ), ( buttonsForm, 'bottom', 5 ) ],
                         ac=[( infomationForm, 'top', 5, baseCtlForm ),
                             ( buttonsForm, 'top', 5, infomationForm )] )
        
        cmds.window( Win_Global.winName, e=1, width = Win_Global.width, height= Win_Global.height )
        cmds.showWindow( Win_Global.winName )
        
        Win_Global.loadInfo()
        
        
    