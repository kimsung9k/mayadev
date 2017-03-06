import maya.cmds as cmds
import uiInfo
import menu
import mainButton
import baseSetting
import rebuild
import nHair
import volume
import cutting
import convert
import grooming
import guide
import bake
import functions

import volumeHairTool

from functools import partial
import maya.OpenMaya as om

mEvent = om.MEventMessage()


import volumeHairTool.basecode as basecode


class Cmd:
    
    def __init__(self):
        
        pass
    
    
    
    def getBaseMesh(self, pointer ):
        
        return cmds.textField( pointer._baseMesh, q=1, tx=1 )

    
    
    def getSurfaceShapes(self, pointer ):
        
        sels= cmds.ls( sl=1 )
        
        if not sels:
            surfGrp = cmds.textField( pointer._surfaceGroup, q=1, tx=1 )
            return functions.getAllSurfaceFromGroup( surfGrp )
        
        selSurfaces = functions.getSurface( sels )
        
        volumeCurves = []
        for sel in sels:
            if cmds.listConnections( sel, type='volumeCurvesOnSurface' ):
                volumeCurves.append( sel )
        
        if not selSurfaces and not volumeCurves:
            surfGrp = cmds.textField( pointer._surfaceGroup, q=1, tx=1 )
            return functions.getAllSurfaceFromGroup( surfGrp )
        
        return selSurfaces
    


class Show( Cmd ):

    
    def __init__(self, *args ):
        
        autoLoadPlugin = basecode.AutoLoadPlugin()

        autoLoadPlugin.load( 'HSBVC' )
        autoLoadPlugin.load( 'pgYetiMaya' )
        
        self._winName = "hsbvcTool_ui"
        self._title   = "HSBVC Tool"
        self._width = 400
        self._height = 330
        
        self._baseSetting = None
        self._rebuild = None
        self._simulation = None
        self._volumeHair = None
        self._cutting = None
        self._convert = None
        self._grooming = None
        self._guide = None
        self._bake = None
        
        self.core()
     
    def core(self):
        
        if cmds.window( self._winName , ex=1 ):
            cmds.deleteUI( self._winName, wnd=1 )
            
        cmds.window( self._winName, title = self._title, menuBar=True )
        
        menu.File( self )
        menu.About( self )
        
        cmds.columnLayout()
        
        uiInfo.separator( self._width, 10 )
        self._baseSetting = baseSetting.Add( self )
        uiInfo.setSpace(14)
        uiInfo.separator( self._width, 1 )
        uiInfo.setSpace(5)
        
        self._mainButton = mainButton.Add( self )
        uiInfo.setSpace(8)
        
        self._rebuild = rebuild.Add( self, self._baseSetting )
        self._simulation = nHair.Add( self, self._baseSetting )
        self._volumeHair = volume.Add( self, self._baseSetting )
        self._cutting = cutting.Add( self, self._baseSetting )
        self._convert = convert.Add( self, self._baseSetting )
        self._grooming = grooming.Add( self, self._baseSetting )
        self._guide = guide.Add( self, self._baseSetting )
        self._bake = bake.Add( self, self._baseSetting )
        
        cmds.window( self._winName, e=1, w= self._width, h=self._height )
        cmds.showWindow( self._winName )
        
        self._height = cmds.window( self._winName, q=1, h=1 )

mc_showHSBVCTool = """import volumeHairTool.ui
volumeHairTool.ui.Show()"""