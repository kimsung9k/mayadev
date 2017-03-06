import uifunctions as uifnc

import maya.cmds as cmds
import math

import bjtDriverSet
import makePSDSkin


class Cmd:
    
    def __init__(self):
        
        pass
    
    
    def loadCmd(self, *args ):
        
        selObjs = cmds.ls( sl=1 )
        
        if not selObjs: return None
        
        selObj = selObjs[0]
        
        cmds.textField( self._rootField, e=1, tx=selObj )
        
        self.updateCondition()
        
        
    def updateCondition(self, *args ):
        
        rootName = cmds.textField( self._rootField, q=1, tx=1 )
        
        children = cmds.listRelatives( rootName, c=1, ad=1 )
        
        angleDriverList = []
        for child in children:
            hists = cmds.listHistory( child )
            
            for hist in hists:
                if cmds.nodeType( hist ) == 'angleDriver':
                    if not hist in angleDriverList:
                        angleDriverList.append( hist )
                        
        onlyMoved = cmds.checkBox( self._showOnlyMovedCheck, q=1, v=1 )
        
        showDrivers = []
        
        minValue = cmds.floatField( self._smallerValueField, q=1, v=1 )
        
        if onlyMoved:
            for driver in angleDriverList:
                angle1, angle2, angle3 = cmds.getAttr( driver+'.outDriver' )[0]
                
                if math.fabs( angle1 ) > minValue or math.fabs( angle2 ) > minValue or math.fabs( angle3 ) > minValue:
                    showDrivers.append( driver )
        else:
            for driver in angleDriverList:
                showDrivers.append( driver )
                
        cmds.textScrollList( self._driverList, e=1, ra=1, a=showDrivers )
        
        
    def selectDriverCmd(self, *args ):
        
        minValue = cmds.floatField( self._smallerValueField, q=1, v=1 )
        
        drivers = cmds.textScrollList( self._driverList, q=1, si=1 )
        
        if not drivers:
            cmds.rowColumnLayout( self._angleFrame, e=1, en=1 )
            return None
            
        cmds.rowColumnLayout( self._angleFrame, e=1, en=1 )
        cmds.select( drivers )
        
        angles = cmds.getAttr( drivers[-1]+'.outDriver' )[0]
        
        cmds.floatField( self._angle1, e=1, v=angles[0] )
        cmds.floatField( self._angle2, e=1, v=angles[1] )
        cmds.floatField( self._angle3, e=1, v=angles[2] )
        
        onBGC = [ .9, .9, .2 ]
        offBGC = [ .2, .2, .2 ]
        
        angle1BGC = offBGC
        angle2BGC = offBGC
        angle3BGC = offBGC
        
        if math.fabs( angles[0] ) > minValue:
            angle1BGC = onBGC
        if math.fabs( angles[1] ) > minValue:
            angle2BGC = onBGC
        if math.fabs( angles[2] ) > minValue:
            angle3BGC = onBGC
        
        cmds.floatField( self._angle1, e=1, bgc=angle1BGC )
        cmds.floatField( self._angle2, e=1, bgc=angle2BGC )
        cmds.floatField( self._angle3, e=1, bgc=angle3BGC )
        
    
    def setDriverCmd(self, *args ):
        
        sels = cmds.ls( sl=1 )
        
        for sel in sels:
            bjtDriverSet.DirectSet( sel )
    
    
    def checkCmd(self, *args ):
        
        self.updateCondition()
        
        
    def makePSDSkinCmd(self, *args ):
        
        selMeshObjs = cmds.ls( sl=1 )
        
        for selObj in selMeshObjs:
            makePSDSkin.blendAndFix_toSkin( selObj )
        
        cmds.select( selMeshObjs )
        
    
    
class Show( Cmd ):
    
    def __init__(self):
        
        self._winName = 'psdDriverSet_ui'
        self._title   = 'PSD Driver Set UI'
        
        self._width = 400
        self._height = 385
        
        self.core()
        
        
    def setScriptJob(self):
        
        cmds.scriptJob( e=['linearUnitChanged', "print 'script job doing'"], p=self._winName )
    

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
        self._rootField = cmds.textField( w=widthList[2] )
        cmds.button( l='Load', w=widthList[3], c= self.loadCmd )
        uifnc.setSpace()
        cmds.setParent( '..' )
        
        uifnc.setSpace( 10 )
        cmds.separator( width = self._width+2 )
        uifnc.setSpace( 10 )
        
        widthList = uifnc.setWidthByPerList( [ 5, 45, 3, 45, 5 ], self._width )

        cmds.rowColumnLayout( nc=5, cw=[(1,widthList[0]), (2,widthList[1]), (3,widthList[2]), (4,widthList[3]), (5,widthList[4]) ]  )
        
        uifnc.setSpace()
        
        cmds.rowColumnLayout( nc=1, cw=(1,widthList[1]) )
        cmds.text( l='Driver List', al='center' )
        uifnc.setSpace(10)
        cmds.scrollLayout()
        self._driverList = cmds.textScrollList( w=widthList[1]-8, sc= self.selectDriverCmd, ams=1 )
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        
        uifnc.setSpace()
        
        cmds.rowColumnLayout( nc=1, cw=(1,widthList[3]-1) )
        cmds.text( l='Driver Value' )
        uifnc.setSpace( 30 )
        cmds.frameLayout( cll=0, lv=0 )
        uifnc.setSpace()
        driverWidthList = uifnc.setWidthByPerList( [ 50,50, 5 ], widthList[3]-2 )
        self._angleFrame = cmds.rowColumnLayout( nc=3, cw=[(1,driverWidthList[0]), (2,driverWidthList[1]), (3,driverWidthList[2])], en=1 )
        cmds.text( l='Angle1' ); self._angle1 = cmds.floatField( editable=False );uifnc.setSpace()
        cmds.text( l='Angle2' ); self._angle2 = cmds.floatField( editable=False );uifnc.setSpace()
        cmds.text( l='Angle3' ); self._angle3 = cmds.floatField( editable=False );uifnc.setSpace()
        cmds.setParent( '..' )
        uifnc.setSpace()
        cmds.setParent( '..' )
        
        driverWidthList = uifnc.setWidthByPerList( [ 5, 60,40, 5 ], widthList[3]-2 )
        cmds.rowColumnLayout( nc=4, cw=[(1,driverWidthList[0]), (2,driverWidthList[1]), (3,driverWidthList[2]), (4,driverWidthList[3])])
        uifnc.setSpace()
        cmds.text( l='Smaller Value : ' )
        self._smallerValueField = cmds.floatField( v=0.01 )
        uifnc.setSpace()
        cmds.setParent( '..' )
        
        uifnc.setSpace( 20 )
        self._showOnlyMovedCheck = cmds.checkBox( l='Show Only Moved Driver', cc= self.checkCmd )
        uifnc.setSpace( 10 )
        cmds.button( l='Update Condition', h=30, c=self.updateCondition )
        
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout()
        uifnc.setSpace( 10 )
        cmds.separator( width = self._width+2 )
        uifnc.setSpace( 10 )
        
        cmds.setParent( '..' )
        uifnc.setSpace()
        cmds.setParent( '..' )
        
        driverWidthList = uifnc.setWidthByPerList( [ 5,90,5 ], self._width )
        cmds.rowColumnLayout( nc=3, cw=[(1,driverWidthList[0]), (2,driverWidthList[1]), (3,driverWidthList[2])] )
        uifnc.setSpace()
        cmds.button( l='Set Driver', h=30, c= self.setDriverCmd )
        uifnc.setSpace()
        
        uifnc.setSpace()
        cmds.button( l='Make PSD Skin', h=30, c= self.makePSDSkinCmd )
        uifnc.setSpace()
        
        cmds.setParent( '..' )
        
        cmds.window( self._winName, e=1, width = self._width+2, height = self._height )
        cmds.showWindow( self._winName )
        
        self.setScriptJob()