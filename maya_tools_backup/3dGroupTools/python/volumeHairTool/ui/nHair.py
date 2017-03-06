import maya.cmds as cmds
import uiInfo
import volumeHairTool.command.nHair as mainCmd
import volumeHairTool.progress as progress
from functools import partial



class Cmd:
    
    def __init__(self):
        
        pass

    """
    def getUpObjectCmd(self, winPointer, basePointer, *args ):
        
        baseMesh = cmds.textField( basePointer._baseMesh, q=1, tx=1 )
        surfs = winPointer.getSurfaceShapes( basePointer )
        
        for surf in surfs:
            surfP = cmds.listRelatives( surf, p=1 )[0]
            cCurve = cmds.listConnections( surfP+'.centerCurve' )[0]
            
            cCurveShape = cmds.listRelatives( cCurve, s=1 )[0]
            
            mainCmd.getSurfaceUpObject(cCurveShape, baseMesh)"""
            
            
    
    def addControlerToCurveCmd(self, winPointer, basePointer, *args ):
        
        sels = cmds.ls( sl=1 )
        
        baseMesh = cmds.textField( basePointer._baseMesh, q=1, tx=1 )
        surfs = winPointer.getSurfaceShapes( basePointer )
        
        controlerNum = cmds.intSliderGrp( self._controlerNum, q=1, v=1 )
        
        progress.start()
        progress.append( 'N Hair' )
        
        progress.setLength( len( surfs ) )
        
        if cmds.checkBox( self._addControler, q=1, v=1 ):
            for surf in surfs:
                progress.addCount()
                mainCmd.allSet( surf, baseMesh, True, controlerNum )
        else:
            for surf in surfs:
                progress.addCount()
                mainCmd.allSet( surf, baseMesh, False )
        
        progress.end()
            
        if sels:
            cmds.select( sels )
    


    def checkAddControler(self, *args ):
        
        if cmds.checkBox( self._addControler, q=1, v=1 ):
            cmds.intSliderGrp( self._controlerNum, e=1, en=1 )
        else:
            cmds.intSliderGrp( self._controlerNum, e=1, en=0 )
            
            
    
    def selectUpCtlCmd(self, winPointer, basePointer, *args ):
        
        surfs = winPointer.getSurfaceShapes( basePointer )
        
        upObjList = []
        for surf in surfs:
            surfObj = cmds.listRelatives( surf, p=1 )[0]
            
            if cmds.attributeQuery( 'upObject', node=surfObj, ex=1 ):
                upObjGrpCons = cmds.listConnections( surfObj+'.upObject' )
                if upObjGrpCons:
                    upObjGrp = upObjGrpCons[0]
            
            upObj = cmds.listRelatives( upObjGrp, c=1 )[0]
            upObjList.append( upObj )
            
        cmds.select( upObjList )
        
        
    def showDCtl(self, winPointer, basePointer, *args ):
        
        surfs = winPointer.getSurfaceShapes( basePointer )
        
        upObjList = []
        for surf in surfs:
            surfObj = cmds.listRelatives( surf, p=1 )[0]
            
            if cmds.attributeQuery( 'upObject', node=surfObj, ex=1 ):
                upObjGrpCons = cmds.listConnections( surfObj+'.upObject' )
                if upObjGrpCons:
                    upObjGrp = upObjGrpCons[0]
            
            upObj = cmds.listRelatives( upObjGrp, c=1 )[0]
            upObjList.append( upObj )
        
        if not upObjList: return None    
        children = cmds.listRelatives( upObjList, c=1, ad=1 )
        
        if not children: return None
        
        dCtls = []
        for child in children:
            nodeCons = cmds.listConnections( child, d=1, s=0, type='clusterControledCurve' )
            if nodeCons:
                dCtls.append( child )
        
        for dCtl in dCtls:
            dhValue = cmds.getAttr( dCtl+'.dh' )
            if dhValue:
                cmds.setAttr( dCtl+'.dh', 0 )
            else:
                cmds.setAttr( dCtl+'.dh', 1 )



class Add( Cmd ):
    
    def __init__(self, winPointer, basePointer ):
        
        Cmd.__init__( self )
        
        self._uiName = "volumeHairTool_nHairSet"
        self._label = "  nHair"
        self._width = winPointer._width-4
        self._winPointer  = winPointer
        self._basePointer = basePointer
        self._defaultValue = 5
        
        self.core()
        

    def core(self):
        
        uiInfo.addFrameLayout( self._uiName, self._label )
        
        uiInfo.setSpace( 10 )
        
        firstWidth = (self._width - 40)*.33
        secondWdith = (self._width - 40)*.33
        thirdWidth = (self._width - 40) - firstWidth - secondWdith
        
        cmds.rowColumnLayout( nc=5, cw=[(1,20), (2,firstWidth), (3,secondWdith), (4,thirdWidth), (5,20)] )
        uiInfo.setSpace()
        self._addControler = cmds.checkBox( l='Add Controler', v=0, cc=self.checkAddControler )
        cmds.button( l='Select Up Object', c=partial( self.selectUpCtlCmd, self._winPointer, self._basePointer ) )
        cmds.button( l='Show DCTL', c=partial( self.showDCtl, self._winPointer, self._basePointer ) )
        uiInfo.setSpace()
        cmds.setParent( '..' )
        
        uiInfo.setSpace( 5 )
        
        uiInfo.floatSliderColumn( self._width )
        cmds.text( l='Num Of Controler :  ', al='right' )
        self._controlerNum = uiInfo.intSlider( 2, 10, 20, self._defaultValue )
        cmds.intSliderGrp( self._controlerNum, e=1, en=0 )
        cmds.setParent( '..' )
        
        uiInfo.setSpace( 10 )
        
        cmds.rowColumnLayout( nc=3, cw=[(1,10),(2,self._width-20),(3,10)])
        uiInfo.setSpace()
        uiInfo.setButton( partial( self.addControlerToCurveCmd, self._winPointer, self._basePointer ) )
        uiInfo.setSpace()
        cmds.setParent( '..' )
        
        uiInfo.setSpace( 10 )
        
        uiInfo.getOutFrameLayout()
        
        
    def clear(self):
        
        cmds.floatSliderGrp( self._offset, e=1, v=0 )
        self.saveData()