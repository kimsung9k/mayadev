import maya.cmds as cmds
import volumeHairTool.uiInfo as uiInfo
import volumeHairTool.command.cutting as mainCmd
import volumeHairTool.progress as progress
from functools import partial
import maya.mel as mel
import os


class Cmd:
    
    def __init__(self):
        
        pass
    
    
    def setCmd( self, winPointer, basePointer, *args ):
        
        sels = cmds.ls( sl=1 )
        
        surfs = winPointer.getSurfaceShapes( basePointer )
        
        constStart = cmds.floatSliderGrp( self._constStart , q=1, v=1 )
        consEnd    = cmds.floatSliderGrp( self._constEnd   , q=1, v=1 )
        applyUV    = cmds.checkBox( self._applyUV, q=1, v=1 )
        
        progress.start()
        progress.append( 'Cutting' )
        
        progress.setLength( len( surfs ) )
        
        for surf in surfs:
            progress.addCount()
            mainCmd.cutCurve( surf, constStart, consEnd, applyUV )
        
        progress.end()
            
        if sels:
            cmds.select( sels )



class Add( Cmd ):


    def __init__(self, winPointer, basePointer ):
        
        Cmd.__init__(self)
        
        self._uiName = "volumeHairTool_cutting"
        self._label = "  Cutting"
        self._width = winPointer._width-4
        
        self._winPointer = winPointer
        self._basePointer = basePointer
        
        self._attachDefault = 0.0
        self._blendDefault = 0.1
        
        self.core()


    def core(self):
        
        uiInfo.addFrameLayout( self._uiName, self._label )
        
        uiInfo.setSpace( 10 )
        
        uiInfo.floatSliderColumn( self._width )
        cmds.text( l="Const Start : ", al='right' )
        self._constStart = uiInfo.floatSlider( 0.0, 1.0, 1.0, self._attachDefault )
        cmds.text( l="Const End : ", al='right' )
        self._constEnd = uiInfo.floatSlider( 0.01, 1.0, 1.0, self._blendDefault )
        uiInfo.setSpace();uiInfo.setSpace()
        uiInfo.setSpace()
        self._applyUV = cmds.checkBox( l='Apply UV' )
        cmds.setParent( '..' )
        
        uiInfo.setSpace( 5 )
        
        cmds.rowColumnLayout( nc=3, cw=[(1,10),(2,self._width-20),(3,10)])
        uiInfo.setSpace()
        uiInfo.setButton( partial( self.setCmd, self._winPointer, self._basePointer ) )
        uiInfo.setSpace()
        cmds.setParent( '..' )
        
        uiInfo.setSpace( 10 )
        
        uiInfo.getOutFrameLayout()
        
        
    def clear(self):
        
        cmds.floatSliderGrp( self._attachPose, e=1, v=1 )
        cmds.floatSliderGrp( self._blendArea, e=1, v=4 )
        self.saveData()