import maya.cmds as cmds
import uiInfo
import volumeHairTool.command.guide as mainCmd
import functions as fnc
from functools import partial
import maya.mel as mel
import os
import uiModel

class progress:
    
    def __init__(self, numSurfaces ):
        
        self._winName = 'volumeHairTool_guideProgress'
        
        self._title = 'Guide Progress'
        
        self._numSurfaces = numSurfaces
        
        self._bgc = [ 0.95, 0.95, 0 ]
        
        self._progCw = [(1,150),(2,200)]
        self._cw = [(1,1),(2,199)]
        
        
    def setNum(self,num ):
        
        self._numSurfaces = num
        
    
    def start(self):
        
        if cmds.window( self._winName, ex=1 ):
            cmds.deleteUI( self._winName )
        
        cmds.window( self._winName, title= self._title )
        
        column = cmds.columnLayout()
        
        cmds.rowColumnLayout( nc=2, cw=self._progCw )
        cmds.text( 'Set Value : ', al='right' )
        cmds.frameLayout( labelVisible=0 )
        self._cutting = cmds.rowColumnLayout( nc=2, cw=self._cw )
        cmds.text( l='', bgc=self._bgc )
        cmds.setParent( column )

        
        cmds.window( self._winName, e=1, wh=[ 350,50 ], rtf=1 )
        
        cmds.showWindow( self._winName )
        
        
    def end(self):
        
        cmds.deleteUI( self._winName )
        
        
    def setElement(self, target, num ):
        
        value = int( float( num )/self._numSurfaces * 200 )
        invValue = 201-value
        
        if value == 0: value =1
        
        cmds.rowColumnLayout( target, e=1, cw=[(1,value),(2,invValue)] )


class Cmd:
    
    def __init__(self):
        
        self._selCommandOn = True
        self._attrAndValues = []
        self._sliders = []
        
        self._values = []
        strValues = self.openText().split( '|' )
        
        print strValues
        
        for strValue in strValues:
            self._values.append( float( strValue ) )
        
        self._sliderDefineList = []
        self._sliderDefineList.append( ['weight', 0, 1, self._values[0]] )
        self._sliderDefineList.append( ['lengthWeight', 0, 1, self._values[1]] )
        self._sliderDefineList.append( ['innerRadius', 0, 10, self._values[2]] )
        self._sliderDefineList.append( ['outerRadius', 0, 10, self._values[3]] )
        self._sliderDefineList.append( ['density', 0, 1, self._values[4]] )
        self._sliderDefineList.append( ['baseAttraction', 0, 1, self._values[5]] )
        self._sliderDefineList.append( ['tipAttraction', 0, 1, self._values[6]] )
        self._sliderDefineList.append( ['attractionBias', -1, 1, self._values[7]] )
        self._sliderDefineList.append( ['randomAttraction', 0, 1, self._values[8]] )
        self._sliderDefineList.append( ['twist', 0, 1, self._values[9]] )
        self._sliderDefineList.append( ['surfaceDirectionLimit', 0, 1, self._values[10]] )
        self._sliderDefineList.append( ['surfaceDirectionLimitFalloff', 0, 3, self._values[11]] )
        
    
    def saveData(self, *args ):
        
        app_dir = mel.eval( 'getenv( "MAYA_APP_DIR" )' )+"/LocusCommPackagePrefs"

        path = app_dir+"/HSBVC_prefs/GUIDE.txt"
        
        values = []
        for slider in self._sliders:
            value = cmds.floatSliderGrp( slider[1], q=1, v=1 )
            values.append( str( value ) )
        
        fileTextSpace = open( path, 'w' )
        fileTextSpace.write( '|'.join( values ) )
        fileTextSpace.close()
        
    
    def openText(self):
        
        app_dir = mel.eval( 'getenv( "MAYA_APP_DIR" )' )+"/LocusCommPackagePrefs"

        path = app_dir+"/HSBVC_prefs/GUIDE.txt"
        
        if not os.path.exists( path ):
            return "1.0|1.0|0.0|2.0|1.0|0.0|0.0|0.1|0.0|0.0|0.0|1.0"
        
        fileTextSpace = open( path, 'r' )
        text = fileTextSpace.read()
        fileTextSpace.close()
        
        return text
    

    def selectOnSetCmd( self, *args ):
        
        cmds.textScrollList( self._guideSet, e=1, da=1 )
        if self._selCommandOn:
            items = cmds.textScrollList( self._set, q=1, si=1 )
            cmds.select( items, ne=1 )
        
    def selectOnGuideSetCmd( self, *args ):
        
        cmds.textScrollList( self._set, e=1, da=1 )
        if self._selCommandOn:
            items = cmds.textScrollList( self._guideSet, q=1, si=1 )
            cmds.select( items, ne=1 )
    
    def sliderSet( self, name, minValue, maxValue, dv, cw ):
        
        cmds.text( l = mainCmd.attrNameToDisplayName( name )+'  ', al='right' )  
        cmds.columnLayout(h=20)
        check = cmds.checkBox( l='', v=1 )
        cmds.setParent('..')
        slider = cmds.floatSliderGrp( f=1, min=minValue, max=maxValue, cw=cw, v=dv )
        
        return check, slider
        
    
    
    def setCmd( self, *args ):
        
        sels = cmds.ls( sl=1 )
        
        if not sels: return None
        
        allChildren = mainCmd.getAllChildren( sels )
        
        if not allChildren: return None
        
        attrsAndValues = []
        for i in range( len( self._sliders ) ):
            attr   = self._sliderDefineList[i][0]
            value = cmds.floatSliderGrp( self._sliders[i][1], q=1, v=1 )
            attrsAndValues.append( [attr, value] )
        
        progressInst = progress( len( allChildren ) )
        
        progressInst.start()
        i=0
        cmds.refresh( suspend=1 )
        for i in range( len( allChildren ) ):
            for j in range( len( attrsAndValues ) ):
                attr, value = attrsAndValues[j]
                if cmds.checkBox( self._sliders[j][0], q=1, v=1 ):
                    if cmds.attributeQuery( attr, node=allChildren[i], ex=1 ):
                        cmds.setAttr( allChildren[i]+'.'+attr, value )
            i+=1
            try:progressInst.setElement( progressInst._cutting, i )
            except:break
            cmds.refresh()
        cmds.refresh( suspend=0 )
        progressInst.end()
                    
    
    def getCmd(self, *args ):
        
        sels = cmds.ls( sl=1 )
        
        if not sels: return None
        
        allChildren = mainCmd.getAllChildren( sels )
        
        if not allChildren: return None
        
        for i in range( len( self._sliders ) ):
            if cmds.checkBox( self._sliders[i][0], q=1, v=1 ):
                attr = self._sliderDefineList[i][0]
                value = cmds.getAttr( allChildren[0]+'.%s' % attr )
                cmds.floatSliderGrp( self._sliders[i][1], e=1, v=value )
            
            
    def allCheckBoxOnCmd(self, *args):
        
        for slider in self._sliders:
            check1, em = slider
            cmds.checkBox( check1, e=1, v=1 )
            
    def allCheckBoxOffCmd(self, *args ):
        
        for slider in self._sliders:
            check1, em = slider
            cmds.checkBox( check1, e=1, v=0 )
            
    def reverseCheckBoxCmd(self, *args ):
        
        for slider in self._sliders:
            check1, em = slider
            value = cmds.checkBox( check1, q=1, v=1 )
            cmds.checkBox( check1, e=1, v=( 1-value ) )
            

class Add( Cmd ):
    
    def __init__(self, winPointer, basePointer ):
        
        Cmd.__init__( self )
        
        self._uiName = "volumeHairTool_guide"
        self._label = "  Guide"
        self._width = winPointer._width-4
        
        self._winPointer = winPointer
        self._basePointer = basePointer
        
        self.core()


    def core(self):
        
        uiInfo.addFrameLayout( self._uiName, self._label )
        
        uiInfo.setSpace( 10 )
        
        textScrollArea = (self._width-20) / 2
        textScrollArea2 =  self._width-20-textScrollArea
        
        cmds.rowColumnLayout( nc=4, cw=[(1,10), (2,textScrollArea),(3,textScrollArea2),(4,10)] )
        uiInfo.setSpace()
        self._set = cmds.textScrollList(  h=100, ams=1,  sc = partial( self.selectOnSetCmd ) )
        self._guideSet = cmds.textScrollList(  h=100, ams=1,  sc = partial( self.selectOnGuideSetCmd ) )
        uiInfo.setSpace()
        cmds.setParent( '..' )
        
        uiInfo.setSpace( 5 )
        
        checkWidth = 25
        textWidth = (self._width-checkWidth-20)*.45 - 5
        sliderWidth = (self._width-checkWidth-20) - textWidth - checkWidth*2 + 5
        
        cmds.rowColumnLayout( nc=7, cw=[(1,10),(2,textWidth),(3,checkWidth),(4,checkWidth),(5,checkWidth),(6,sliderWidth),(7,10)])
        uiInfo.setSpace()
        cmds.frameLayout( lv=0, bs='out', h=20 )
        cmds.text( l='ATTRIBUTE' )
        cmds.setParent( '..' )
        cmds.button( 'A', c=self.allCheckBoxOnCmd, bgc=[.8,.39,.41] )
        cmds.button( 'C', c=self.allCheckBoxOffCmd, bgc=[.47,.72,.21] )
        cmds.button( 'R', c=self.reverseCheckBoxCmd, bgc=[.09,.41,.51] )
        cmds.frameLayout( lv=0, bs='out' )
        cmds.text( l='VALUE' )
        cmds.setParent( '..' )
        uiInfo.setSpace()
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=5, cw=[(1,10),(2,textWidth),(3,20),(4,sliderWidth+checkWidth+20),(5,10)])
        for i in self._sliderDefineList:
            uiInfo.setSpace()
            cuSlider = self.sliderSet( i[0], i[1], i[2], i[3], [(1,50),(2,150)] )
            cmds.floatSliderGrp( cuSlider[1], e=1, step=0.01, fmx=100, cc=self.saveData )
            uiInfo.setSpace()
            
            self._sliders.append( cuSlider )
        cmds.setParent( '..' )
        
        uiInfo.setSpace( 10 )

        cmds.rowColumnLayout( nc=4, cw=[(1,10),(2,30),(3,self._width-20-30),(4,10)])
        uiInfo.setSpace()
        cmds.iconTextButton( image= uiModel.iconPath +'/spoid.png', c= partial( self.getCmd ) )
        uiInfo.setButton( partial( self.setCmd ) )
        uiInfo.setSpace()
        cmds.setParent( '..' )
        
        uiInfo.setSpace( 10 )
        
        uiInfo.getOutFrameLayout()
        
        
    def updateSet(self ):
        
        surfGrp = cmds.textField( self._basePointer._surfaceGroup, q=1, tx=1 )
        
        if not surfGrp: return None

        if cmds.attributeQuery( 'sets', node=surfGrp, ex=1 ):
            sets = cmds.listConnections( surfGrp+'.sets' )
        else:
            return None
        
        cmds.textScrollList( self._set, e=1, removeAll=1 )
        cmds.textScrollList( self._guideSet, e=1, removeAll=1 )
        
        if sets:
            for setElement in sets:
                if cmds.listConnections( setElement, type='pgYetiMaya' ):
                    cmds.textScrollList( self._guideSet, e=1, append = setElement )
                else:
                    cmds.textScrollList( self._set, e=1, append = setElement )
            
    def clear(self):
        
        valueStr = "1.0|1.0|0.0|2.0|1.0|0.0|0.0|0.1|0.0|0.0|0.0|1.0"
        
        values = []
        for i in valueStr.split( '|' ):
            values.append( float( i ) )
                
        for slider in self._sliders:
            index = self._sliders.index( slider )
            cmds.floatSliderGrp( slider[1], e=1, v=values[index] )
            
        self.saveData()