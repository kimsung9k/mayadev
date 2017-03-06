import maya.cmds as cmds
import maya.OpenMaya as om
import uiData
import chModules.retargetTool.cmd.timeControl as timeCmd
import chModules.retargetTool.functions as fnc


class addAttributePopup:
    

    def __init__(self, uiFunc, targetUi ):
        
        self._uiFunc = uiFunc
        self._targetUi = targetUi
        
        cmds.popupMenu()
        cmds.menuItem( l='Set key', c=self.setKey )
        cmds.menuItem( l='Break Connection', c=self.breakKey )
        

    def setTargetAttr(self, attrs, *args ):
        
        self._attrs = attrs
        
        
    def setKey(self, *args):
        
        for attr in self._attrs:
            cmds.setKeyframe( attr )
        
        self.updateCondition()
        

    def breakKey(self, *args):
        
        for attr in self._attrs:
            animCurveCons = cmds.listConnections( attr, s=1, d=0, type='animCurve' )
            
            if animCurveCons:
                cmds.delete( animCurveCons[0] )
        
        self.updateCondition()
            
            
    def updateCondition(self, *args):
        
        if not self._attrs: return None
        
        if not cmds.objExists( self._attrs[-1].split( '.' )[0] ): return None
        
        animCurveCons = cmds.listConnections( self._attrs[-1], s=1, d=0, type='animCurve' )
        
        if animCurveCons:
            self._uiFunc( self._targetUi, e=1, bgc=[0.871, 0.447, 0.478] )
        else:
            self._uiFunc( self._targetUi, e=1, bgc=[0.165, 0.165, 0.165] )



class Cmd:
    
    def __init__(self):
        
        self._dragOn = False
        self._keepValues = []
            
        uiData.updateFunctionList.append( self.refreshFloatField )
        
        
    def saveSetting(self, *args ):
        
        pass
        
        #strList = [ worldCtl, filePath, rangeString, rangeSlider ]
        #allStr = '||'.join( strList )
        
        #uiData.saveData( self._fileTextName, allStr )
            
            
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
                
        timeControls = timeCmd.getTimeControl( targetWorldCtl, worldCtls )
        
        cmds.textScrollList( self._timeControl, e=1, ra=1, a=timeControls )
        
          
    def refreshFloatField(self, *args ):
        
        timeControl = cmds.textScrollList( self._timeControl, q=1, si=1 )
        
        if not timeControl: return None
        
        timeControl = timeControl[-1]
        
        weight = cmds.getAttr( timeControl+'.weight' )
        offset = cmds.getAttr( timeControl+'.offset' )
        mult = cmds.getAttr( timeControl+'.mult' )
        limitAble = cmds.getAttr( timeControl+'.limitAble' )
        minTime = cmds.getAttr( timeControl+'.minTime' )
        maxTime = cmds.getAttr( timeControl+'.maxTime' )
        
        cmds.floatField( self._weight, e=1, v=weight )
        cmds.floatField( self._offset, e=1, v=offset )
        cmds.floatField( self._mult, e=1, v=mult )
        cmds.checkBox( self._limitAble, e=1, v=limitAble )
        cmds.floatField( self._minTime, e=1, v=minTime )
        cmds.floatField( self._maxTime, e=1, v=maxTime )
        
        if cmds.checkBox( self._limitAble, q=1, v=1 ):
            cmds.rowColumnLayout( self._limitAbleLay, e=1, en=1 )
        else:
            cmds.rowColumnLayout( self._limitAbleLay, e=1, en=0 )
            
        for popup in self._popupList:
            popup.updateCondition()
        
        
    def leftScrollSelectCmd(self, *args ):
        
        selItems = cmds.textScrollList( self._timeControl, q=1, si=1 )
        
        if selItems:
            cmds.rowColumnLayout( self._attrs, e=1, en=1 )
        else:
            cmds.rowColumnLayout( self._attrs, e=1, en=0 )
        
        for i in range(6):
            popupAttrs = []
            for selItem in selItems:
                popupAttrs.append( selItem+'.'+self._attrList[i] )
            self._popupList[i].setTargetAttr( popupAttrs )
        
        self.refreshFloatField()
        
        cmds.select( selItems )
        
        
    def changeCmd(self, *args ):
        
        weight = cmds.floatField( self._weight, q=1, v=1 )
        offset = cmds.floatField( self._offset, q=1, v=1 )
        mult = cmds.floatField( self._mult, q=1, v=1 )
        limitAble = cmds.checkBox( self._limitAble, q=1, v=1 )
        minTime = cmds.floatField( self._minTime, q=1, v=1 )
        maxTime = cmds.floatField( self._maxTime, q=1, v=1 )
        
        if self._dragOn:
            self.setBeforeValue()
            self._dragOn = False
        
        self.setAttr( weight, offset, mult, minTime, maxTime, limitAble )
        
        if cmds.checkBox( self._limitAble, q=1, v=1 ):
            cmds.rowColumnLayout( self._limitAbleLay, e=1, en=1 )
        else:
            cmds.rowColumnLayout( self._limitAbleLay, e=1, en=0 )
            
            
    def dragCmd(self, *args ):

        weight = cmds.floatField( self._weight, q=1, v=1 )
        offset = cmds.floatField( self._offset, q=1, v=1 )
        mult = cmds.floatField( self._mult, q=1, v=1 )
        minTime = cmds.floatField( self._minTime, q=1, v=1 )
        maxTime = cmds.floatField( self._maxTime, q=1, v=1 )
        limitAble = cmds.checkBox( self._limitAble, q=1, v=1 )
        
        if not self._dragOn:
            self.getBeforeValue()
            self._dragOn = True
            
        self.setAttrApi( weight, offset, mult, minTime, maxTime, limitAble )
            
            
    def setAttr(self, weight, offset, mult, minTime, maxTime, limitAble, *args ):
        
        selItems = cmds.textScrollList( self._timeControl, q=1, si=1 )
        
        for timeControl in selItems:
            cmds.setAttr( timeControl+'.weight', weight )
            cmds.setAttr( timeControl+'.offset', offset )
            cmds.setAttr( timeControl+'.mult', mult )
            cmds.setAttr( timeControl+'.minTime', minTime )
            cmds.setAttr( timeControl+'.maxTime', maxTime )
            cmds.setAttr( timeControl+'.limitAble', limitAble )
            

    def setAttrApi(self, weight, offset, mult, minTime, maxTime, limitAble, *args ):
        
        selItems = cmds.textScrollList( self._timeControl, q=1, si=1 )
        
        for timeControl in selItems:
            fnc.setAttrApi( timeControl+'.weight', weight )
            fnc.setAttrApi( timeControl+'.offset', offset )
            fnc.setAttrApi( timeControl+'.mult', mult )
            fnc.setAttrApi( timeControl+'.minTime', om.MTime( minTime ) )
            fnc.setAttrApi( timeControl+'.maxTime', om.MTime( maxTime ) )
            
            
    def getBeforeValue(self):
        
        selItems = cmds.textScrollList( self._timeControl, q=1, si=1 )
        
        values = []
        for selItem in selItems:
            values.append( cmds.getAttr( selItem+'.weight' ) )
            values.append( cmds.getAttr( selItem+'.offset' ) )
            values.append( cmds.getAttr( selItem+'.mult' ) )
            values.append( cmds.getAttr( selItem+'.minTime' ) )
            values.append( cmds.getAttr( selItem+'.maxTime' ) )
            
        self._keepValues.append( values )
        
        
    def setBeforeValue(self):
        
        selItems = cmds.textScrollList( self._timeControl, q=1, si=1 )
        
        for values in self._keepValues:

            for selItem in selItems:
                fnc.setAttrApi( selItem+'.weight', values[0] )
                fnc.setAttrApi( selItem+'.offset', values[1] )
                fnc.setAttrApi( selItem+'.mult', values[2] )
                fnc.setAttrApi( selItem+'.minTime', om.MTime( values[3] ) )
                fnc.setAttrApi( selItem+'.maxTime', om.MTime( values[4] ) )
                
                
    def setDefault(self, *args ):
        
        pass
        
            

class Add( Cmd ):
    
    def __init__(self):
        
        self._uiName = 'retarget_TimeControl_ui'
        self._label = 'Time Control'
        self._fileTextName = 'TimeControl'
        
        self._height = 45
        self._sideSpace = 5
        self._width = uiData.winWidth-4-self._sideSpace*2
        
        self.core()
        
        self._attrList = [ 'weight', 'offset', 'mult', 'limitAble', 'minTime', 'maxTime' ]
        self._popupList = [ self._weightPopup, self._offsetPopup, self._multPopup, self._limitAblePopup, self._minTimePopup, self._maxTimePopup ]
        
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
        
        halfWidth = self._width*0.5
        lastWidth = self._width - halfWidth
        
        cmds.rowColumnLayout( nc=4, cw=[(1,self._sideSpace),(2,halfWidth ),(3,lastWidth ),(4,self._sideSpace)] )
        uiData.setSpace()
        self._timeControl  = cmds.textScrollList( h=140, ams=True, sc= self.leftScrollSelectCmd  )
        
        self._attrs = cmds.rowColumnLayout( nc=1, cw=[1,lastWidth], en=0 )
        cmds.rowColumnLayout( nc=2, cw=[(1,lastWidth*0.5),(2,lastWidth*0.5)] )
        cmds.text( l='Weight : ', align='right', h=22 ); 
        self._weight = cmds.floatField( v=10.0, cc= self.changeCmd, dc=self.dragCmd, step=0.01, min=0.0, max=10.0 )
        self._weightPopup = addAttributePopup( cmds.floatField, self._weight )
        cmds.text( l='Offset : ', align='right', h=22 ); 
        self._offset = cmds.floatField( cc= self.changeCmd, dc=self.dragCmd, step=0.01 )
        self._offsetPopup = addAttributePopup( cmds.floatField, self._offset )
        cmds.text( l='Mult  : ', align='right', h=22); 
        self._mult = cmds.floatField( v=1.0, cc= self.changeCmd, dc=self.dragCmd, step=0.01 )
        self._multPopup = addAttributePopup( cmds.floatField, self._mult )
        cmds.text( l='' );  
        self._limitAble = cmds.checkBox( l='Limit Able', h=25, cc= self.changeCmd, bgc=[0.165, 0.165, 0.165] )
        self._limitAblePopup = addAttributePopup( cmds.checkBox, self._limitAble )
        cmds.setParent( '..' )
        self._limitAbleLay = cmds.rowColumnLayout( nc=2, cw=[(1,lastWidth*0.5),(2,lastWidth*0.5)], en=0 )
        cmds.text( l='Min Time  : ', align='right', h=22 ); 
        self._minTime = cmds.floatField( cc= self.changeCmd, dc=self.dragCmd, step=0.01 )
        self._minTimePopup = addAttributePopup( cmds.floatField, self._minTime )
        cmds.text( l='Max Time  : ', align='right', h=22 ); 
        self._maxTime = cmds.floatField( v=1.0, cc= self.changeCmd, dc=self.dragCmd, step=0.01 )
        self._maxTimePopup = addAttributePopup( cmds.floatField, self._maxTime )
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        uiData.setSpace()
        cmds.setParent( '..' )
        
        uiData.setSpace( 5 )
        
        cmds.setParent( '..' )
        cmds.setParent( '..' )