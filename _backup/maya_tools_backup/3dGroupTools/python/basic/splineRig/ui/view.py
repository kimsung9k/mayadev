import maya.cmds as cmds
from uiModel import *
import cmdModel


class CurveInfoSetUI:
    
    def __init__(self):
        
        self._cmdSet   = []
        self._cmdClose = []
        
        
    def cmdSet(self, *args ):
        for cmd in self._cmdSet: cmd()
        
    
    def cmdClose(self, *args ):
        for cmd in self._cmdClose: cmd()
    
    
    
    def setCmd(self):
        
        def cmdSetModel():
            value = cmds.intSliderGrp( self._slider, q=1, v=1 )
            check = cmds.checkBox( self._check, q=1, v=1 )
            if check:
                cmdModel.ucCreateSplineNode( value )
            else:
                cmdModel.ucCreatePointOnCurveNodes( value )
            
        def cmdCloseModel():
            cmds.deleteUI( CurveInfoSetUIInfo._winName, wnd=1 )
            
        self._cmdSet.append( cmdSetModel )
        self._cmdClose.append( cmdCloseModel )
    
    
    
    def show( self ):
        
        self.setCmd()
        
        if cmds.window( CurveInfoSetUIInfo._winName, ex=1 ):
            cmds.deleteUI( CurveInfoSetUIInfo._winName, wnd=1 )
        
        cmds.window( CurveInfoSetUIInfo._winName, title= CurveInfoSetUIInfo._title )
        
        cmds.columnLayout()
        cmds.rowColumnLayout( nc=3, cw=[(1,95),(2,135),(3,70)] )
        cmds.text( 'Number of Info : ', al='right' )
        slider = cmds.intSliderGrp( f=1, min=1, max=10, fmx=100, cw=[(1,50),(2,150)], v=1 )
        check = cmds.checkBox( l='epCurve' )
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=2, cw=[(1,150),(2,150)] )
        cmds.button( 'SET', c= self.cmdSet )
        cmds.button( 'CLOSE', c= self.cmdClose )
        cmds.setParent( '..' )
        
        cmds.window( CurveInfoSetUIInfo._winName, e=1, 
                     w=CurveInfoSetUIInfo._width,
                     h=CurveInfoSetUIInfo._height )
        cmds.showWindow( CurveInfoSetUIInfo._winName )
        
        self._slider = slider
        self._check  = check