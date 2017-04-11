import jointBasePsd.uifunctions as uifnc

import maya.cmds as cmds


class Cmd:
    
    def __init__(self):
        
        pass
    
    
class Show( Cmd ):
    
    def __init__(self):
        
        self._winName = 'psdDriverSet_ui'
        self._title   = 'PSD Driver Set UI'
        
        self._width = 400
        self._height = 400
        
        self.core()
    

    def core(self):
        
        if cmds.window( self._winName, ex=1 ):
            cmds.deleteUI( self._winName )
        
        cmds.window( self._winName, title= self._title )
        
        cmds.columnLayout()
        
        uifnc.setSpace( 5 )
        
        widthList = uifnc.setWidthByPerList( [5 ,25, 45, 20, 5], self._width )
        
        cmds.rowColumnLayout( nc=5, cw=[(1,widthList[0]), (2,widthList[1]), (3,widthList[2]), (4,widthList[3]), (5,widthList[4])])
        uifnc.setSpace()
        cmds.text( l='Target Root :  ', al='right', w=widthList[1] )
        cmds.textField( w=widthList[2] )
        cmds.button( l='Load', w=widthList[3] )
        uifnc.setSpace()
        cmds.setParent( '..' )
        
        uifnc.setSpace( 10 )
        cmds.separator( width = self._width+2 )
        uifnc.setSpace( 10 )
        
        widthList = uifnc.setWidthByPerList( [ 5, 45, 3, 45, 5 ], self._width )

        cmds.rowColumnLayout( nc=5, cw=[(1,widthList[0]), (2,widthList[1]), (3,widthList[2]), (4,widthList[3]), (5,widthList[4]) ]  )
        
        uifnc.setSpace()
        
        cmds.rowColumnLayout( nc=1, cw=(1,widthList[1]))
        cmds.text( l='Driver List', al='center' )
        uifnc.setSpace(10)
        cmds.scrollLayout()
        cmds.textScrollList( w=widthList[1]-8)
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        
        uifnc.setSpace()
        
        cmds.rowColumnLayout( nc=1, cw=(1,widthList[3]-1))
        cmds.text( l='Driver Value' )
        uifnc.setSpace( 30 )
        cmds.frameLayout( cll=0, lv=0 )
        uifnc.setSpace()
        driverWidthList = uifnc.setWidthByPerList( [ 50,50, 5 ], widthList[3]-2 )
        cmds.rowColumnLayout( nc=3, cw=[(1,driverWidthList[0]), (2,driverWidthList[1]), (3,driverWidthList[2])] )
        cmds.text( l='Angle1' ); cmds.floatField( editable=False, bgc=[0.9,0.9,0.3] );uifnc.setSpace()
        cmds.text( l='Angle2' ); cmds.floatField( editable=False, bgc=[0.9,0.9,0.3] );uifnc.setSpace()
        cmds.text( l='Angle3' ); cmds.floatField( editable=False, bgc=[0.9,0.9,0.3] );uifnc.setSpace()
        cmds.setParent( '..' )
        uifnc.setSpace()
        cmds.setParent( '..' )
        
        uifnc.setSpace( 30 )
        cmds.checkBox( l='Show Only Moved Driver')
        uifnc.setSpace( 10 )
        cmds.button( l='Update Condition', h=30 )
        
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout()
        uifnc.setSpace( 10 )
        cmds.separator( width = self._width+2 )
        uifnc.setSpace( 10 )
        
        cmds.setParent( '..' )
        
        uifnc.setSpace()
        cmds.setParent( '..' )
        
        cmds.window( self._winName, e=1, width = self._width+2, height = self._height )
        cmds.showWindow( self._winName )