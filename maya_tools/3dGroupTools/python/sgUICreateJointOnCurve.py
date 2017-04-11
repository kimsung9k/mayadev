import maya.cmds as cmds
import sgRigs.sgRigCurve as sgRigCurve


class Window:
    
    def __init__(self):
        
        self._winName = 'createJointOnCurve_ui'
        self._title   = 'Create Joint On Curve'
        self._width   = 350
        self._height  = 50
        
        
        
    def cmdCreate( self, *args ):
        
        checkValue = cmds.checkBox( self._check, q=1, v=1 )
        
        if cmds.radioButton( self._radio1, q=1, sl=1 ):
            numJoint = cmds.intSliderGrp( self._slider1, q=1, v=1 )
            sgRigCurve.createJointOnCurve( numJoint, checkValue )
        else:
            multRate = cmds.floatSliderGrp( self._slider2, q=1, v=1 )
            sgRigCurve.createJointOnCurveByLength( multRate, checkValue )
    
    
    
    def cmdOn(self , *args ):
        
        cmds.intSliderGrp( self._slider1, e=1, en=1 )
        cmds.floatSliderGrp( self._slider2, e=1, en=0 )


    def cmdOff(self, *args ):
        
        cmds.intSliderGrp( self._slider1, e=1, en=0 )
        cmds.floatSliderGrp( self._slider2, e=1, en=1 )
    
        
    
    def show(self):
        
        if cmds.window( self._winName, ex=1 ):
            cmds.deleteUI( self._winName, wnd=1 )
        cmds.window( self._winName, title= self._title )
        
        columnWidth = self._width - 2
        sliderFirstWidth = columnWidth * 0.4
        sliderSecondWidth = 50
        sliderThirdWidth = columnWidth - sliderFirstWidth - sliderSecondWidth
        
        firstWidth = ( columnWidth -2 )/ 2
        secondWidth = ( columnWidth - 2 ) - firstWidth
        
        cmds.columnLayout()
        cmds.rowColumnLayout( nc=2, co=[(1, 'left',30)], cw=[(1,firstWidth),(2,secondWidth)])
        cmds.radioCollection()
        radio1 = cmds.radioButton( l='By Number', sl=1, onc = self.cmdOn, ofc = self.cmdOff )
        radio2 = cmds.radioButton( l='By Length' )
        cmds.setParent( '..' )
        cmds.rowColumnLayout( nc=1, cw=(1,columnWidth) )
        cmds.separator()
        slider1 = cmds.intSliderGrp( l='Num of Joint : ', f=1, 
                                    cw=[(1,sliderFirstWidth),(2,sliderSecondWidth),(3,sliderThirdWidth)],
                                    min=1, max=20, fmn=1, fmx=100, v=5 )
        slider2 = cmds.floatSliderGrp( l='Mult Rate : ', f=1, 
                                    cw=[(1,sliderFirstWidth),(2,sliderSecondWidth),(3,sliderThirdWidth)],
                                    min=0.01, max=10, fmn=0.01, fmx=100, v=1.0, pre=2, en=0 )
        cmds.separator()
        cmds.rowColumnLayout( nc=2, cw=[( 1, 50 ), (2,columnWidth-52)])
        cmds.text( l='' )
        check = cmds.checkBox( l='Connect Distance Node', value =1 )
        cmds.setParent( '..' )
        cmds.text( l='', h=5 )
        cmds.button( l='Create', c=self.cmdCreate )
        cmds.setParent( '..' )
        
        cmds.window( self._winName, e=1,
                     w = self._width, h= self._height )
        cmds.showWindow( self._winName )
        
        self._slider1 = slider1
        self._slider2 = slider2
        self._radio1 = radio1
        self._radio2 = radio2
        self._check = check


def showWindow( *args ):
    Window().show()