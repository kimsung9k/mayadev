import maya.cmds as cmds
import uiData
import chModules.retargetTool.cmd.retargeting as mainCmd


class Cmd:
    
    def __init__(self):
            
        self.getSetting()
        
        #uiData.updateFunctionList.append( self.refreshTextScrollList )
            
            
    def getSetting( self, *args ):
    
        pass
        
        
    def saveSetting(self, *args ):
        
        pass
        
        #strList = [ worldCtl, filePath, rangeString, rangeSlider ]
        #allStr = '||'.join( strList )
        
        #uiData.saveData( self._fileTextName, allStr )


    def connect(self,*args ):
        
        targetWorldCtl = cmds.textField( self._worldCtl, q=1, tx=1 )
        
        selItems = cmds.textScrollList( self._beforeConnectList, q=1, si=1 )
        if not selItems: return None
        
        for selItem in selItems:
            mainCmd.connect( selItem, targetWorldCtl )
        
        self.refreshTextScrollList()
        
         
    def disconnect(self, *args):
        
        targetWorldCtl = cmds.textField( self._worldCtl, q=1, tx=1 )
        connectedCtls =  cmds.textScrollList( self._afterConnectList, q=1, si=1 )
        
        for connectedCtl in connectedCtls:
            mainCmd.disconnect( connectedCtl, targetWorldCtl )
        
        self.refreshTextScrollList()

                       
    def loadWorldCtl(self, *args ):
        
        sels = cmds.ls( sl=1 )
        
        if not sels: return None
        
        if sels[-1].find( 'World_CTL' ) == -1: return None

        cmds.textField( self._worldCtl, e=1, tx= sels[-1] )
        
        uiData.targetWorldCtl = sels[-1]
        
        self.refreshTextScrollList()
        
        
    def refreshTextScrollList(self, *args ):
        
        targetWorldCtl = cmds.textField( self._worldCtl, q=1, tx=1 )

        connectedCtls = mainCmd.getConnectedRetargetWorldCtl( targetWorldCtl )
        
        worldCtls = mainCmd.getWorldCtlList()
        if targetWorldCtl in worldCtls:
            worldCtls.remove( targetWorldCtl )
        
        if connectedCtls:
            for connectedCtl in connectedCtls:
                if connectedCtl in worldCtls:
                    worldCtls.remove( connectedCtl )
        
        cmds.textScrollList( self._beforeConnectList, e=1, ra=1, a=worldCtls )
        cmds.textScrollList( self._afterConnectList, e=1, ra=1, a=connectedCtls )
        
        
    def leftScrollSelectCmd(self, *args ):
        
        cmds.textScrollList( self._afterConnectList, e=1, da=1 )
        
        
    def rightScrollSelectCmd(self, *args ):
        
        cmds.textScrollList( self._beforeConnectList, e=1, da=1 )
        
        
    def setDefault(self, *args ):
        
        pass
        
            
            
class Add( Cmd ):
    
    def __init__(self):
        
        self._uiName = 'retarget_Retargeting_ui'
        self._label = 'Retargeting'
        self._fileTextName = 'Retargeting'
        
        self._height = 45
        self._sideSpace = 5
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
        
        halfWidth = self._width/2
        lastWidth = self._width - halfWidth
        
        cmds.rowColumnLayout( nc=4, cw=[(1,self._sideSpace),(2,halfWidth ),(3,lastWidth ),(4,self._sideSpace)] )
        uiData.setSpace()
        self._beforeConnectList = cmds.textScrollList( h=100, ams=True, sc= self.leftScrollSelectCmd )
        self._afterConnectList = cmds.textScrollList( h=100, ams=True, sc= self.rightScrollSelectCmd )
        uiData.setSpace()
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=4, cw=[(1,self._sideSpace),(2,halfWidth ),(3,lastWidth ),(4,self._sideSpace)] )
        uiData.setSpace()
        cmds.button( l='Connect', c = self.connect, h=30 )
        cmds.button( l='Disconnect',c = self.disconnect, h=30 )
        uiData.setSpace()
        cmds.setParent( '..' )
        uiData.setSpace( 5 )
        
        
        cmds.setParent( '..' )
        cmds.setParent( '..' )