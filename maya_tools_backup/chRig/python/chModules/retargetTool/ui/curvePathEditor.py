import maya.cmds as cmds
import uiData
import chModules.retargetTool.cmd.retargeting as retargetCmd
import chModules.retargetTool.cmd.editTransform as editCmd


class Cmd_surport:
    
    def __init__(self):
        
        pass
    

    def refreshTextScrollList(self):
        
        targetWorldCtl = cmds.textField( self._worldCtl, q=1, tx=1 )
        
        if not targetWorldCtl: return None
        
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
        
              
    def addPopup( self, field ):
        
        def loadSelectedCurve( *args ):
            
            sels = cmds.ls( sl=1 )
            
            if not sels: return None
            
            selShapes = cmds.listRelatives( sels, s=1, f=1 )
            
            if not selShapes: return None
            
            if cmds.nodeType( selShapes[0] ) == 'nurbsCurve':
                if len( cmds.ls( '*|'+selShapes[0].split( '|' )[-1] ) ) > 1:
                    cmds.textField( field, e=1, tx=selShapes[0] )
                else:
                    cmds.textField( field, e=1, tx=selShapes[0].split( '|' )[-1] )
                return None
                
        cmds.popupMenu()
        cmds.menuItem( l='Load Selected Curve', c=loadSelectedCurve )
        
        
    def getNodeByTextField( self, field ):
        
        nodeName = cmds.textField( field, q=1, tx=1 )
        
        if cmds.objExists( nodeName ):
            return nodeName
        
        return None



class Cmd( Cmd_surport ):

  
    def __init___(self):
        
        Cmd_surport.__init__(self)
        
        
    def getCurve(self, typ ):
        
        typDict = { 'source': self._sourceCurveField, 'dest': self._destCurveField }
        
        sourceNode = self.getNodeByTextField( typDict[ typ ] )
        
        if not sourceNode: return None
        
        if cmds.nodeType( sourceNode ) == 'nurbsCurve':
            return cmds.listRelatives( sourceNode, p=1 )[0]
        
        return None
    

    def loadWorldCtl(self, *args ):
        
        sels = cmds.ls( sl=1 )
        
        if not sels: return None
        
        if sels[-1].find( 'World_CTL' ) == -1: return None

        cmds.textField( self._worldCtl, e=1, tx= sels[-1] )
        
        self.refreshTextScrollList()
        
        
    def firstScrollSelectCmd(self, *args ):
        
        targetWorldCtl = cmds.textField( self._worldCtl, q=1, tx=1 )
        
        selItems = cmds.textScrollList( self._retargetList, q=1, si=1 )
        
        for selItem in selItems:
            inst = editCmd.localControler( selItem, targetWorldCtl )
            
            ctlList = []
            for localCtl in inst.getLocalControler():
                if cmds.nodeType( localCtl ) == 'editMatrixByCurve':
                    retargetNode = cmds.listConnections( localCtl+'.outSourceMatrix', d=1, s=0 )[0]
                    blender = cmds.listConnections( retargetNode, s=0, d=1, type='retargetBlender' )[0]
                    ctl = cmds.listConnections( blender, s=0, d=1 )[0]
                    ctlList.append( ctl )
            cmds.textScrollList( self._controlList, e=1, ra=1, a=ctlList )
        
        
    def secondScrollSelectCmd(self, *args ):

        localCtlList = cmds.textScrollList( self._controlList, q=1, si=1 )
        
        if not localCtlList:
            cmds.button( self._selItemButton, e=1, en=0 )
            return None
        
        for localCtl in localCtlList:
            
            blender = cmds.listConnections( localCtl, s=1, d=0, type='retargetBlender' )[0]
            retargetNode = cmds.listConnections( blender, s=1, d=0, type='retargetTransNode' )[0]
            
            editMatrixNodes = cmds.listConnections( retargetNode, s=1, d=0, type='editMatrixByCurve' )
            
            if not editMatrixNodes:
                continue
            editMatrixNode = editMatrixNodes[0]
            
            sourceTrGeo = cmds.listConnections( editMatrixNode+'.sourceCurve' )[0]
            destTrGeo = cmds.listConnections( editMatrixNode+'.destCurve' )[0]
            
            sourceCrv = cmds.listConnections( sourceTrGeo+'.inputGeometry', sh=1 )[0]
            destCrv   = cmds.listConnections( destTrGeo+'.inputGeometry', sh=1 )[0]
            
            cmds.textField( self._sourceCurveField, e=1, tx=sourceCrv )
            cmds.textField( self._destCurveField, e=1, tx=destCrv )
            
        cmds.button( self._selItemButton, e=1, en=1 )
            
                           
    def connectByNode(self, *args ):
        
        sels = cmds.ls( sl=1 )
        
        if not sels: return None
        
        selItems = cmds.textScrollList( self._retargetList, q=1, si=1 )
        
        if not selItems: return None
        
        selNamespace = selItems[-1].replace( 'World_CTL', '' )
        
        editCmd.CurveType( sels[-1], self.getCurve( 'source'), self.getCurve( 'dest' ), selNamespace ).connect()
        
        self.refreshTextScrollList()
        

    def connectByItem(self, *args ):
        
        selItems = cmds.textScrollList( self._retargetList, q=1, si=1 )
        
        if not selItems: return None
        
        selCtls = cmds.textScrollList( self._controlList, q=1, si=1 )
        
        if not selCtls: return None
        
        selNamespace = selItems[-1].replace( 'World_CTL', '' )
        
        editCmd.CurveType( selCtls[-1], self.getCurve( 'source'), self.getCurve( 'dest' ), selNamespace ).connect()



class Load( Cmd ):

    
    def __init__(self, pointer ):
        
        self._pointer = pointer
        
        self._winName = 'retarget_editCurve_ui'
        self._title   = 'Curve Path Editor UI'
        
        self._width = 404
        self._height = 135
        self._sideSpace = 10
        
        self.core()
    
        Cmd.__init___(self)
        

    def core(self):
        
        if cmds.window( self._winName, ex=1 ):
            cmds.deleteUI( self._winName )
        cmds.window( self._winName )
        
        cmds.columnLayout()
        
        uiData.setSpace( 10 )
        
        buttonWidth = 40
        textWidth = self._width * 0.33
        fieldWidth = self._width - textWidth - buttonWidth
        
        cmds.rowColumnLayout( nc=5, cw=[(1,self._sideSpace),(2,textWidth),(3,fieldWidth),(4,buttonWidth),(5,self._sideSpace)] )
        uiData.setSpace()
        cmds.text( l='Target World CTL   :  ', al='right' )
        
        pointerText = cmds.textField( self._pointer._worldCtl, q=1, tx=1 )
        self._worldCtl = cmds.textField( tx=pointerText )
        cmds.button( l='Load', c=self.loadWorldCtl )
        uiData.setSpace()
        cmds.setParent( '..' )
        
        uiData.setSpace( 13 )
        
        divWidth = self._width/3
        lastWidth = self._width - divWidth*2
        
        cmds.rowColumnLayout( nc=5, cw=[(1,self._sideSpace),(2,divWidth ),(3,divWidth ),(4,lastWidth ),(5,self._sideSpace)] )
        uiData.setSpace()
        self._retargetList   = cmds.textScrollList( h=100, ams=True, sc= self.firstScrollSelectCmd  )
        self._controlList    = cmds.textScrollList( h=100, ams=True, sc= self.secondScrollSelectCmd  )
        
        cmds.rowColumnLayout( nc=2, cw=[(1,10),(2,lastWidth-12)] )
        uiData.setSpace()
        cmds.rowColumnLayout( nc=1, cw=(1,lastWidth-14) )
        cmds.text( l='Source Curve', al='left' )
        uiData.setSpace()
        self._sourceCurveField = cmds.textField()
        self.addPopup( self._sourceCurveField )
        uiData.setSpace()
        cmds.text( l='Dest Curve', al='left' )
        uiData.setSpace()
        self._destCurveField = cmds.textField()
        self.addPopup( self._destCurveField )
        uiData.setSpace()
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        
        uiData.setSpace( 12 )
        
        
        cmds.rowColumnLayout( nc=3, cw=[(1,self._sideSpace),(2,self._width ),(3,self._sideSpace)] )
        uiData.setSpace()
        self._selItemButton = cmds.button( l='Replace Curve to Selected Item',
                     h=30, c=self.connectByItem, en=0 )
        uiData.setSpace()
        uiData.setSpace()
        cmds.button( l='Connect Curve With Selected Controler',
                     h=30, c=self.connectByNode )
        uiData.setSpace()
        cmds.setParent( '..' )
        
        uiData.setSpace( 10 )
        
        cmds.window( self._winName, e=1, w=self._width, h=self._height )
        cmds.showWindow( self._winName )
        
        self.refreshTextScrollList()