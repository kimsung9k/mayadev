import maya.cmds as cmds
import sgModelRule
import sgModelUI
import sgRigCurve
import sgRigAttribute



def getMenuItem():
    
    sgHairSystemLabelAttrName = sgModelRule.sgHairSystemLabelAttrName
    targetAttrs = cmds.ls( '*.'+sgHairSystemLabelAttrName )
    for targetAttr in targetAttrs:
        getStr = cmds.getAttr( targetAttr )
        cmds.menuItem( label = getStr )
    


class Window:
    
    def __init__(self):
        
        self.uiname = 'sgUIMakeCurveDynamic'
        self.title   = 'SG Make Curve Dynamic'
        self.width   = 400
        self.height  = 50
        
        self.popupController = sgModelUI.PopupFieldUI( 'Hair System Controller : ', 'load Selected', 'single', position = 40 )
        self.popupCurves = sgModelUI.PopupFieldUI( 'Target Curves : ', 'load Selected', 'multi', position = 40 )


    def cmdOn(self, *args ):

        cmds.rowColumnLayout( self.columnNewSystem, e=1, vis=1 )
        cmds.rowColumnLayout( self.columnAssignSystem, e=1, vis=0 )
        cmds.window( self.uiname, e=1, h=121 )


    def cmdOff(self, *args ):

        cmds.rowColumnLayout( self.columnNewSystem, e=1, vis=0 )
        cmds.rowColumnLayout( self.columnAssignSystem, e=1, vis=1 )
        cmds.window( self.uiname, e=1, h=100 )


    def cmdCreate(self, *args ):

        newSystemType    = cmds.rowColumnLayout( self.columnNewSystem, q=1, vis=1 )
        assignSystemType = cmds.rowColumnLayout( self.columnAssignSystem, q=1, vis=1 )
        newCurve         = cmds.checkBox( self.check, q=1, v=1 )

        sels = self.popupCurves.getFieldTexts()

        if newSystemType:
            ctlName = self.popupController.getFieldText()
            addName = cmds.textFieldGrp( self.addName, q=1, tx=1 )
            if not newCurve:
                hairSystem = sgRigCurve.makeDynamicCurveKeepSrc( sels, addName )
            else:
                hairSystem = sgRigCurve.makeDynamicCurve( sels, addName )
            sgRigAttribute.connectHairAttribute( ctlName, hairSystem )
        elif assignSystemType:
            addName = cmds.textFieldGrp( self.addName, q=1, tx=1 )
            menuItems = cmds.optionMenuGrp( self.option, q=1, itemListLong=1 )
            selectIndex = cmds.optionMenuGrp( self.option, q=1, sl=1 )-1
            menuItemLabel = cmds.menuItem( menuItems[selectIndex], q=1, label=1 )
            if not newCurve:
                hairSystem = sgRigCurve.makeDynamicCurveKeepSrc( sels, addName )
            else:
                hairSystem = sgRigCurve.makeDynamicCurve( sels, addName )


    def show(self):

        columnWidth = self.width -2
        halfWidth = ( columnWidth -2 )/2
        elseHalfWidth = ( columnWidth -2 ) - halfWidth
        textWidth = ( columnWidth -2 )*0.4
        fieldWidth = ( columnWidth - 2 ) - textWidth

        if cmds.window( self.uiname, ex=1 ):
            cmds.deleteUI( self.uiname, wnd=1 )
        cmds.window( self.uiname, title= self.title )

        cmds.columnLayout()
        '''
        cmds.rowColumnLayout( nc=2, co=[(1,'left', 30), (2,'left',30)], cw=[(1,halfWidth),(2,elseHalfWidth)])
        cmds.radioCollection()
        cmds.radioButton( l='Create New Hair System', sl=1, onc= self.cmdOn, ofc= self.cmdOff  )
        cmds.radioButton( l='Assign Hair System')
        cmds.setParent( '..' )
        '''
        
        #cmds.separator( w=self.width )

        self.columnNewSystem = cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)])
        self.popupController.create()
        self.addName = cmds.textFieldGrp( l='Hair System Label : ', cw=[( 1, textWidth ), ( 2, fieldWidth )], tx='Dynamic_' )
        cmds.setParent( '..' )

        self.columnAssignSystem = cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)], vis=0 )
        self.option = cmds.optionMenuGrp( l='Assign System Target : ', cw=[( 1, textWidth ), ( 2, fieldWidth )] )
        getMenuItem()
        cmds.setParent( '..' )

        cmds.separator( w=self.width )
        cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth)] )
        self.popupCurves.create()
        cmds.setParent( '..' )

        cmds.rowColumnLayout( nc=2, cw=[(1,30)] )
        cmds.text( l='' )
        self.check = cmds.checkBox( l='Create New Curve', v=0 )
        cmds.setParent( '..' )

        cmds.rowColumnLayout( nc=1, cw=[(1,columnWidth )])
        cmds.button( l='Create', en=1, c= self.cmdCreate )
        cmds.setParent( '..' )

        cmds.window( self.uiname, e=1,
                     w = self.width, h = self.height )
        cmds.showWindow( self.uiname )


mc_showWindow = """import sgUIMakeCurveDynamic
sgUIMakeCurveDynamic.Window().show()"""