import maya.cmds as cmds
import uiData
import chModules.retargetTool.cmd.bake as mainCmd



class Cmd:
    
    def __init__(self):
        
        self._timeRange = [1,10,0]
        self._fileBrowserStr = ''
        self._rangeBySlider = False
        
        self.readFile()
        self.getSetting()


    def readFile(self ):
        
        getStr = uiData.openText( self._fileTextName )
        
        if getStr:
            strSplit = getStr.split( '||' )
            
            try: self._timeRange = strSplit[0]
            except: self._timeRange = '1,10,1'
            try: self._rangeBySlider = strSplit[1]
            except: self._rangeBySlider = 0
        else:
            self._timeRange = '1,10,1'
            self._rangeBySlider = 0

    
    def getSetting( self ):
        try:
            minValue, maxValue, byFrame = self._timeRange.split( ',' )
            minValue = float( minValue )
            maxValue = float( maxValue )
            byFrame  = float( byFrame )
        except: 
            minValue, maxValue, byFrame = ( 1.0, 10.0, 1.0 )
            
        try:
            self._rangeBySlider = int( self._rangeBySlider )
        except:
            self._rangeBySlider = 0
    
        cmds.floatField( self._minField, e=1, v=minValue, en=(1-self._rangeBySlider) )
        cmds.floatField( self._maxField, e=1, v=maxValue, en=(1-self._rangeBySlider) )
        cmds.floatField( self._byFrameField, e=1, v=byFrame )
        cmds.checkBox( self._rangeBySliderAble, e=1, v=self._rangeBySlider )


    def saveSetting(self, *args ):
        
        minValue = cmds.floatField( self._minField, q=1, v=1 )
        maxValue = cmds.floatField( self._maxField, q=1, v=1 )
        byFrameValue = cmds.floatField( self._byFrameField, q=1, v=1 )
        rangeString = str( minValue )+','+str(maxValue)+','+str(byFrameValue)
        rangeSlider = str( int(cmds.checkBox( self._rangeBySliderAble, q=1, v=1 )) )
        
        strList = [ rangeString, rangeSlider ]
        allStr = '||'.join( strList )
        
        uiData.saveData( self._fileTextName, allStr )

   
    def loadWorldCtl(self, *args ):
        
        sels = cmds.ls( sl=1 )
        
        if not sels: return None
        
        if sels[-1].find( 'World_CTL' ) == -1: return None

        cmds.textField( self._worldCtl, e=1, tx= sels[-1] )
        
          
    def rangeBySliderChange(self, *args ):
        
        if cmds.checkBox( self._rangeBySliderAble, q=1, v=1 ):
            cmds.floatField( self._minField, e=1, en=0 )
            cmds.floatField( self._maxField, e=1, en=0 )
        else:
            cmds.floatField( self._minField, e=1, en=1 )
            cmds.floatField( self._maxField, e=1, en=1 )
            
        self.saveSetting()
        
        
    def bakeAllCmd(self, *args ):
        
        worldCtl = cmds.textField( self._worldCtl, q=1, tx= 1 )
        
        if cmds.checkBox( self._rangeBySliderAble, q=1, v=1 ):
            minValue = cmds.playbackOptions( q=1, min=1 )
            maxValue = cmds.playbackOptions( q=1, max=1 )
        else:
            minValue = cmds.floatField( self._minField, q=1, v=1 )
            maxValue = cmds.floatField( self._maxField, q=1, v=1 )
            
        sampleValue = cmds.floatField( self._byFrameField, q=1, v=1 )
        
        self.saveSetting()
        mainCmd.Bake().lastBake(worldCtl, [minValue, maxValue, sampleValue])
        
        
    def refreshTextScrollList(self, *args ):
        
        pass
        
        
    def setDefault(self, *args ):

        pass

        
        
        
class WarningUI:
    
    def __init__(self, pointer ):
        
        self._pointer = pointer
        
        self._winName = 'retarget_BakeWarning_ui'
        self._title = 'Bake Warning'
        self._fileTextName = 'Bake'
        self._width = 304
        self._height = 75
        
        if cmds.window( self._winName, ex=1 ):
            cmds.deleteUI( self._winName, wnd=1 )
        cmds.window( self._winName, title=self._title )
        
        cmds.columnLayout()
        
        uiData.setSpace(10)
        
        cmds.rowColumnLayout( nc=1, cw=[(1,300)] )
        cmds.text( l='Bake command is not undo able\nContinue?' )
        cmds.setParent( '..' )
        
        uiData.setSpace(10)
        
        cmds.rowColumnLayout( nc=2, cw=[(1,150),(2,150)] )
        cmds.button( l='Bake', c=self.bake, h=25 )
        cmds.button( l='Cancel', c=self.cancel, h=25 )
        cmds.setParent( '..' )
        
        cmds.window( self._winName, e=1, w=self._width, h=self._height )
        cmds.showWindow( self._winName )
        
        
    def bake(self, *args ):
        
        self._pointer.bakeAllCmd()
        cmds.deleteUI( self._winName, wnd=1 )
    
        
    def cancel(self, *args ):
        
        cmds.deleteUI( self._winName, wnd=1 )
        
            
            

class Add( Cmd ):

    
    def __init__(self):
        
        self._uiName = 'retarget_Bake_ui'
        self._label = 'Bake'
        self._fileTextName = 'Bake'
        
        self._sideSpace = 5
        self._height = 45
        self._width = uiData.winWidth-4-self._sideSpace*2
        
        self.core()
        
        Cmd.__init__( self )
        
    
    def core(self):
        
        uiData.addFrameLayout( self._uiName, self._label, 0, False, False )
        
        uiData.setSpace( 10 )
        
        buttonWidth = 40
        textWidth = self._width * 0.33
        fieldWidth = self._width - textWidth - buttonWidth
        
        cmds.rowColumnLayout( nc=5, cw=[(1,self._sideSpace),(2,textWidth),(3,fieldWidth),(4,buttonWidth),(5,self._sideSpace)] )
        uiData.setSpace()
        cmds.text( l='Target World CTL   :  ', al='right' )
        self._worldCtl = cmds.textField()
        cmds.button( l='Load', c=self.loadWorldCtl )
        uiData.setSpace()
        cmds.setParent( '..' )
        
        uiData.setSpace( 5 )
        cmds.separator()
        uiData.setSpace( 5 )
        
        textWidth = self._width * 0.33
        fieldWidth = ( self._width - textWidth )/3
        
        cmds.rowColumnLayout( nc=6, cw=[(1,self._sideSpace),(2,textWidth),(3,fieldWidth),(4,fieldWidth),(5,fieldWidth),(6,self._sideSpace) ] )
        uiData.setSpace()
        cmds.text( l='Time Range   :  ' , al='right' )
        self._minField = cmds.floatField( v=1.0, step=0.1 )
        self._maxField = cmds.floatField( v=10.0, step=0.1 )
        self._byFrameField = cmds.floatField( v=1.0, min=0.1 )
        uiData.setSpace()
        cmds.setParent( '..' )
        
        textWidth = self._width * 0.33
        otherWidth = self._width - textWidth
        
        cmds.rowColumnLayout( nc=4, cw=[(1,self._sideSpace),(2,textWidth),(3,otherWidth),(4,self._sideSpace)] )
        uiData.setSpace()
        uiData.setSpace()
        self._rangeBySliderAble = cmds.checkBox( l='Range by slider', cc=self.rangeBySliderChange )
        uiData.setSpace()
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=3, cw=[(1,self._sideSpace),(2,self._width),(3,self._sideSpace)] )
        uiData.setSpace()
        cmds.button( l='Bake All', c=self.openWarning, h=30 )
        uiData.setSpace()
        cmds.setParent( '..' )
        uiData.setSpace( 5 )
        
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        
        
    def openWarning(self, *args):
        
        WarningUI( self )