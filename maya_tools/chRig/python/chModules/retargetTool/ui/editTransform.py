import maya.cmds as cmds
import uiData
import chModules.retargetTool.cmd.retargeting as retargetCmd
import chModules.retargetTool.cmd.editTransform as editCmd
import curvePathEditor


class Cmd:


    def __init__(self):
         
        pass
            
            
    def getSetting( self, *args ):
    
        pass
        
        
    def saveSetting(self, *args ):
        
        pass
        
        #strList = [ worldCtl, filePath, rangeString, rangeSlider ]
        #allStr = '||'.join( strList )
        
        #uiData.saveData( self._fileTextName, allStr )


    def type1(self,*args ):
        
        targetWorldCtl = cmds.textField( self._worldCtl, q=1, tx=1 )
        
        selItems = cmds.textScrollList( self._retargetList, q=1, si=1 )
        if not selItems: return None

        sels = cmds.ls( sl=1 )
        
        if not sels: return None
        
        for sel in sels:
            editCmd.ControlType1( sel, selItems[0], targetWorldCtl )
            
        self.leftScrollSelectCmd()
        
        
    def type2(self,*args ):
        
        targetWorldCtl = cmds.textField( self._worldCtl, q=1, tx=1 )
        
        selItems = cmds.textScrollList( self._retargetList, q=1, si=1 )
        if not selItems: return None

        sels = cmds.ls( sl=1 )
        
        if not sels: return None
        
        for sel in sels:
            editCmd.ControlType2( sel, selItems[0], targetWorldCtl )
        
        self.leftScrollSelectCmd()
        
            
    def type3(self,*args ):
        
        targetWorldCtl = cmds.textField( self._worldCtl, q=1, tx=1 )
        
        selItems = cmds.textScrollList( self._retargetList, q=1, si=1 )
        if not selItems: return None

        sels = cmds.ls( sl=1 )
        
        if not sels: return None
        
        editCmd.ControlType3( sels[0], sels[1], selItems[0], targetWorldCtl )
        
        self.leftScrollSelectCmd()

                   
    def loadWorldCtl(self, *args ):
        
        sels = cmds.ls( sl=1 )
        
        if not sels: return None
        
        if sels[-1].find( 'World_CTL' ) == -1: return None

        cmds.textField( self._worldCtl, e=1, tx= sels[-1] )
        
        self.refreshTextScrollList()
        

    def refreshTextScrollList(self, *args ):
        
        targetWorldCtl = cmds.textField( self._worldCtl, q=1, tx=1 )
        
        refs = cmds.ls( type='reference' )

        worldCtls = []
        for ref in refs:
            try :ctls = cmds.reference( rfn=ref, n=1 )
            except: continue
            for ctl in ctls:
                if ctl == targetWorldCtl: continue
                if ctl[-9:] == 'World_CTL':
                    worldCtls.append( ctl )
                    break
                elif ctl.find( 'DGTR' ) != -1 and ctl[-4:] == '_CTL':
                    namespace = ctl.split( 'DGTR' )[0]
                    worldCtls.append( namespace+'DGTR_World_CTL' )
                    break
           
        connectedCtls = retargetCmd.getConnectedRetargetWorldCtl( targetWorldCtl )
        
        for connectedCtl in connectedCtls:
            worldCtls.remove( connectedCtl )
        
        cmds.textScrollList( self._retargetList, e=1, ra=1, a=connectedCtls )
        cmds.textScrollList( self._transformList, e=1, ra=1 )

        
    def leftScrollSelectCmd(self, *args ):
        
        targetWorldCtl = cmds.textField( self._worldCtl, q=1, tx=1 )
        
        selItems = cmds.textScrollList( self._retargetList, q=1, si=1 )
        
        localCtls = []
        for selItem in selItems:
            inst = editCmd.localControler( selItem, targetWorldCtl )
            
            localCtls += inst.getLocalControler()
        
        cmds.textScrollList( self._transformList, e=1, ra=1, a=localCtls )
        
        
    def rightScrollSelectCmd(self, *args ):
        
        selItems = cmds.textScrollList( self._transformList, q=1, si=1 )
        
        cmds.select( selItems )
        
        enAble = False
        
        for selItem in selItems:
            if cmds.nodeType( selItem ) == "editMatrixByCurve":
                enAble = True
                

    def removeCmd(self, *args ):
        
        targetWorldCtl = cmds.textField( self._worldCtl, q=1, tx=1 )
        
        selRetargets = cmds.textScrollList( self._retargetList, q=1, si=1 )
        selItems = cmds.textScrollList( self._transformList, q=1, si=1 )
        
        for selItem in selItems:
            inst = editCmd.localControler( targetWorldCtl, '' )
            inst.deleteLocalControler( selItem )
            
        self.refreshTextScrollList()
        
        for selRetarget in selRetargets:
            cmds.textScrollList( self._retargetList, e=1, si=selRetarget )
        
        self.leftScrollSelectCmd()
        
        
    def loadCurvePathEditor(self, *args ):
        
        curvePathEditor.Load( self )
        
        
    def setDefault(self, *args ):

        pass



class Add( Cmd ):
    
    def __init__(self):
        
        self._uiName = 'retarget_EditTransform_ui'
        self._label = 'Edit Transform'
        self._fileTextName = 'EditTransform'
        
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
        self._retargetList  = cmds.textScrollList( h=100, ams=True, sc= self.leftScrollSelectCmd  )
        self._transformList = cmds.textScrollList( h=100, ams=True, sc= self.rightScrollSelectCmd )
        uiData.setSpace()
        cmds.setParent( '..' )
        
        halfByHalfWidth = halfWidth/3
        otherHalfWidth = halfWidth - halfByHalfWidth*2
        
        cmds.rowColumnLayout( nc=6, cw=[(1,self._sideSpace),(2,halfByHalfWidth ),(3,halfByHalfWidth ),(4,otherHalfWidth ),(5,lastWidth ),(6,self._sideSpace)] )
        uiData.setSpace()
        cmds.button( l='Type1',  c = self.type1, h=30 )
        cmds.button( l='Type2',  c = self.type2, h=30 )
        cmds.button( l='Type3',  c = self.type3, h=30 )
        cmds.button( l='Remove',c = self.removeCmd, h=30 )
        uiData.setSpace()
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=3, cw=[(1,self._sideSpace),(2,self._width),(3,self._sideSpace)] )
        uiData.setSpace()
        cmds.button( l='Open Curve Path Editor', h=30, c= self.loadCurvePathEditor )
        uiData.setSpace()
        cmds.setParent( '..' )
        
        uiData.setSpace( 5 )
        
        cmds.setParent( '..' )
        cmds.setParent( '..' )