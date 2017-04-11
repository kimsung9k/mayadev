import maya.cmds as cmds
import uiData
import chModules.retargetTool as main
import chModules.retargetTool.cmd.exportData as mainCmd
import os

class Cmd:
    
    def __init__(self):
        
        getStr = uiData.openText( self._fileTextName )
        
        if getStr:
            strSplit = getStr.split( '||' )
            
            if strSplit[0].find( 'World_CTL' ) != -1:
                self._worldCtlName = strSplit[0]
            else: self._worldCtlName = ''
            try: self._fileBrowserPath = strSplit[1]
            except: self._fileBrowserPath = ''
            try: self._timeRange = strSplit[2]
            except: self._timeRange = '1,10,1'
            try: self._rangeBySlider = strSplit[3]
            except: self._rangeBySlider = 0
            
            if not os.path.exists( self._fileBrowserPath ):
                self._fileBrowserStr = ''
                self._fileBrowserPath = main.app_dir+'/projects/default'
            else:
                self._fileBrowserStr = self._fileBrowserPath
        else:
            self._worldCtlName = ''
            self._fileBrowserStr = ''
            self._fileBrowserPath = main.app_dir+'/projects/default'
            self._timeRange = '1,10,1'
            self._rangeBySlider = 0
            
        self.getSetting()
        self.checkCondition()
        
        
    def checkCondition(self, *args ):
        
        if cmds.checkBox( self._rangeBySliderAble, q=1, v=1 ):
            cmds.floatField( self._minField, e=1, en=0 )
            cmds.floatField( self._maxField, e=1, en=0 )
        else:
            cmds.floatField( self._minField, e=1, en=1 )
            cmds.floatField( self._maxField, e=1, en=1 )
            
        self.saveSetting()
            
            
    def getSetting( self, *args ):
    
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
    
        cmds.textField( self._worldCtl, e=1, tx= self._worldCtlName )
        cmds.textField( self._filePath, e=1, tx= self._fileBrowserStr )
        cmds.floatField( self._minField, e=1, v=minValue )
        cmds.floatField( self._maxField, e=1, v=maxValue )
        cmds.floatField( self._byFrameField, e=1, v=byFrame )
        cmds.checkBox( self._rangeBySliderAble, e=1, v=self._rangeBySlider )
        
        
    def saveSetting(self, *args ):
        
        worldCtl = cmds.textField( self._worldCtl, q=1, tx=1 )
        filePath = cmds.textField( self._filePath, q=1, tx=1 )
        minValue = cmds.floatField( self._minField, q=1, v=1 )
        maxValue = cmds.floatField( self._maxField, q=1, v=1 )
        byFrameValue = cmds.floatField( self._byFrameField, q=1, v=1 )
        rangeString = str( minValue )+','+str(maxValue)+','+str(byFrameValue)
        rangeSlider = str( int(cmds.checkBox( self._rangeBySliderAble, q=1, v=1 )) )
        
        strList = [ worldCtl, filePath, rangeString, rangeSlider ]
        allStr = '||'.join( strList )
        
        uiData.saveData( self._fileTextName, allStr )
        
    
    def loadSelected(self, *args ):
        
        sels = cmds.ls( sl=1 )
        cmds.textField( self._worldCtl, e=1, tx= sels[-1] )
        
        self.saveSetting()
        
        
    def loadFilePath(self, *args ):
        
        loadedText = cmds.fileDialog2( fm= 0, dir=self._fileBrowserPath )
    
        if loadedText:
            cmds.textField( self._filePath, e=1, tx= loadedText[0] )
            self._fileBrowserPath = '/'.join( loadedText[0].split( '/' )[:-1] )
            
        self.saveSetting()


    def export(self,*args ):
        
        worldCtl = cmds.textField( self._worldCtl, q=1, tx=1 )
        filePath = cmds.textField( self._filePath, q=1, tx=1 )
        
        minValue = cmds.floatField( self._minField, q=1, v=1 )
        maxValue = cmds.floatField( self._maxField, q=1, v=1 )
        byFrameValue = cmds.floatField( self._byFrameField, q=1, v=1 )
        
        if cmds.checkBox( self._rangeBySliderAble, q=1, v=1 ):
            minValue = cmds.playbackOptions( q=1, min=1 )
            maxValue = cmds.playbackOptions( q=1, max=1 )
        frameRate = [ minValue, maxValue, byFrameValue ]
        
        mainCmd.ExportSelected( worldCtl, filePath, frameRate )
        
        
    def setDefault(self, *args ):
        
        cmds.textField( self._worldCtl, e=1, tx='' )
        cmds.textField( self._filePath, e=1, tx='' )
        
        cmds.floatField( self._minField, e=1, v=1 )
        cmds.floatField( self._maxField, e=1, v=10 )
        cmds.floatField( self._byFrameField, e=1, v=1 )
        
        cmds.checkBox( self._rangeBySliderAble, e=1, v=1 )
        
        self.checkCondition()
        
        
    def refreshTextScrollList( self, *args ):
        
        pass
        
    

class Add( Cmd ):
    
    def __init__(self):
        
        self._uiName = 'retarget_ExportData_ui'
        self._label = 'Export Data'
        self._fileTextName = 'ExportData'
        
        self._height = 45
        self._sideSpace = 5
        self._width = uiData.winWidth-4-self._sideSpace*2
        
        self.core()
        
        Cmd.__init__( self )
        
    def core(self):
        
        uiData.addFrameLayout( self._uiName, self._label, 0, False, False )
        
        buttonWidth = 40
        textWidth = self._width * 0.33
        fieldWidth = self._width - textWidth - buttonWidth
        
        uiData.setSpace( 5 )
        
        cmds.rowColumnLayout( nc=5, cw=[(1,self._sideSpace),(2,textWidth),(3,fieldWidth),(4,buttonWidth),(5,self._sideSpace)] )
        uiData.setSpace()
        cmds.text( l='World CTL   :  ', al='right' )
        self._worldCtl = cmds.textField()
        cmds.button( l='Load', c=self.loadSelected )
        uiData.setSpace()
        cmds.setParent( '..' )
        
        uiData.setSpace( 5 )
        cmds.separator()
        uiData.setSpace( 5 )
        
        cmds.rowColumnLayout( nc=5, cw=[(1,self._sideSpace),(2,textWidth),(3,fieldWidth),(4,buttonWidth),(5,self._sideSpace)] )
        uiData.setSpace()
        cmds.text( l='Export File Path   :  ', al='right' )
        self._filePath = cmds.textField()
        cmds.iconTextButton( l="", h=23, image=uiData.exportDataFolderImagePath,
                             c= self.loadFilePath )
        uiData.setSpace()
        cmds.setParent( '..' )
        
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
        self._rangeBySliderAble = cmds.checkBox( l='Range by slider', cc=self.checkCondition )
        uiData.setSpace()
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=3, cw=[(1,self._sideSpace),(2,self._width),(3,self._sideSpace)] )
        uiData.setSpace()
        cmds.button( l='Export', c=self.export, h=30 )
        uiData.setSpace()
        cmds.setParent( '..' )
        uiData.setSpace( 5 )
        
        
        cmds.setParent( '..' )
        cmds.setParent( '..' )