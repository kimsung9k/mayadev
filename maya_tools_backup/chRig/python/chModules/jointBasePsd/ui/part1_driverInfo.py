import maya.cmds as cmds
import uifunctions as uifnc
import globalInfo

import math

from functools import partial


class MovedDriverList:
    
    def __init__(self, width, targetUI, minValue=0.1 ):
        
        self._width = width-25
        self._minValue = minValue
        self._updateTargetUi = targetUI


    def driverScrollAddPopupCmd(self, *args ):
        
        try: cmds.deleteUI( self.popupUi, menu=1 )
        except: pass
        
        self.popupUi = cmds.popupMenu( p=self._updateTargetUi )
        
        def removeSelCmd( *args ):
            si = cmds.textScrollList( self._updateTargetUi, q=1, si=1 )
            cmds.textScrollList( self._updateTargetUi, e=1, ri=si )
            
        def removeAllCmd( *args ):
            cmds.textScrollList( self._updateTargetUi, e=1, ra=1 )
            #cmds.deleteUI( self.popupUi, menu=1 )
        
        cmds.menuItem( l='Remove All', c=removeAllCmd )


    def addConnectDriver(self, str1, *args ):

        driverName = str1.split( ':' )[0]

        strList = cmds.textScrollList( self._updateTargetUi, q=1, ai=1 )
        
        if not strList: strList = []
        
        for strTarget in strList:
            targetDriverName = strTarget.split( ':' )[0]
            if driverName == targetDriverName:
                cmds.textScrollList( self._updateTargetUi, e=1, ri=strTarget )

        cmds.textScrollList( self._updateTargetUi, e=1, a=str1 )

    
    def add(self, driverName, angleValues=[] ):
        
        if not angleValues:
            angleValues = [0,0,0]
        
        defaultBgc = [ .1, .1, .1 ]
        onBgc      = [ .9,  .9,  .2  ]
        
        enList = [0,0,0]
        
        bgcList = [None,None,None]
        
        for i in range( 3 ):
            if math.fabs( angleValues[i] ) >= self._minValue:
                bgcList[i] = onBgc
                enList[i] = 1
            else:
                bgcList[i] = defaultBgc
                enList[i] = 0
        
        widthList = uifnc.setWidthByPerList( [70,15,15,15] , self._width )

        cmds.rowColumnLayout( nc=4, cw=[(1,widthList[0]),(2,widthList[1]),(3,widthList[2]),(4,widthList[3])] )
        cmds.text( l= driverName+' : ', al='right' )
        
        cmds.floatField( precision=2, v=angleValues[0], bgc= bgcList[0] )
        cmds.popupMenu(); cmds.menuItem( l='Add Driver', c= partial( self.addConnectDriver, driverName+' | angle0 : %3.2f' %angleValues[0] ) )
        cmds.floatField( precision=2, v=angleValues[1], bgc= bgcList[1] )
        cmds.popupMenu(); cmds.menuItem( l='Add Driver', c= partial( self.addConnectDriver, driverName+' | angle1 : %3.2f' %angleValues[1] ) )
        cmds.floatField( precision=2, v=angleValues[2], bgc= bgcList[2] )
        cmds.popupMenu(); cmds.menuItem( l='Add Driver', c= partial( self.addConnectDriver, driverName+' | angle2 : %3.2f' %angleValues[2] ) )
        
        self.driverScrollAddPopupCmd()
        
        cmds.setParent( '..' )



class Cmd:
    
    def __init__(self, width ):
        
        globalInfo.driverInfoInst = self
        

    def updateCmd( self, *args ):

        rootName = globalInfo.rootDriver
        minValue = 0.1
        movedDriverCheck = cmds.checkBox( self._movedDriverCheck, q=1, v=1 )
        
        children = cmds.listRelatives( rootName, c=1, ad=1, f=1 )
        
        angleDriverList = []
        for child in children:
            hists = cmds.listHistory( child )
            
            for hist in hists:
                if cmds.nodeType( hist ) == 'angleDriver':
                    if not hist in angleDriverList:
                        angleDriverList.append( hist )
        
        showDrivers = []
        
        for driver in angleDriverList:
            
            if movedDriverCheck:
                angle1, angle2, angle3 = cmds.getAttr( driver+'.outDriver' )[0]
                
                if math.fabs( angle1 ) > minValue or math.fabs( angle2 ) > minValue or math.fabs( angle3 ) > minValue:
                    showDrivers.append( driver )
            else:
                showDrivers.append( driver )
        
        childUis = cmds.scrollLayout( self._driverListLay, q=1, ca=1 )
        
        if childUis:
            for childUi in childUis:
                cmds.deleteUI( childUi )
        
        cmds.setParent( self._driverListLay )
        
        for driver in showDrivers:
            values = cmds.getAttr( driver+'.outDriver' )[0]
            self._movedDriverInst.add( driver, values )
            
        self._movedDrivers = showDrivers
        
        self.reWriteValueCmd()

    
    def reWriteValueCmd( self ):
        
        items = cmds.textScrollList( self._driverScrollList, q=1, ai=1 )
        
        if not items: items = []
        
        for item in items:
            
            driverName, other = item.split( ' | angle' )
            angleIndex, angleValue = other.split( ' : ' )
            
            angleValue = cmds.getAttr( driverName+'.outDriver%s' % angleIndex )
            
            reItem = driverName+' | angle'+angleIndex+' : %3.2f' % angleValue
            
            cmds.textScrollList( self._driverScrollList, e=1, ri=item )
            if angleValue > 0.1:
                cmds.textScrollList( self._driverScrollList, e=1, a=reItem )
        


class Add( Cmd ):
    
    def __init__(self, width ):
        
        self._emptyWidth = 10
        self._width = width - self._emptyWidth*2 - 4
        self._height = 140
        
        sepList = [ 65, 50 ]
        self._mainWidthList = uifnc.setWidthByPerList( sepList, self._width )
        
        sepList = [ 70, 30 ]
        self._optionWidthList = uifnc.setWidthByPerList( sepList, self._mainWidthList[0]-20 )
        
        Cmd.__init__( self, self._mainWidthList[0] )
        self._rowColumns = []
        self.core()
        
    
    def core(self):
        
        column1 = cmds.rowColumnLayout( nc= 3, cw=[(1,self._emptyWidth),
                                         (2,self._width),
                                         (3,self._emptyWidth)])
        
        uifnc.setSpace()
        cmds.text( l='Driver LIST' )
        uifnc.setSpace()
        cmds.setParent( '..' )
        
        uifnc.setSpace( 5 )
        
        column2 = cmds.rowColumnLayout( nc=4, cw=[(1,self._emptyWidth),
                                        (2,self._mainWidthList[0]),
                                        (3,self._mainWidthList[1]),
                                        (4,self._emptyWidth) ] )
        uifnc.setSpace()
        
        column3 = cmds.rowColumnLayout( nc=1, cw=[(1,self._mainWidthList[0])])
        
        self._driverListLay = cmds.scrollLayout( h=self._height-30 )
        cmds.setParent( '..' )
        
        uifnc.setSpace( 5 )
        
        column4 = cmds.rowColumnLayout( nc= 4, cw=[(1,self._emptyWidth),
                                         (2,self._optionWidthList[0]),
                                         (3,self._optionWidthList[1]),
                                         (4,self._emptyWidth)] )
        uifnc.setSpace()
        self._movedDriverCheck = cmds.checkBox( l='Show Only Moved Drivers', cc= self.updateCmd )
        cmds.button( l='Refresh', c= self.updateCmd )
        uifnc.setSpace()
        cmds.setParent( '..' )
        
        cmds.setParent( '..' )
        
        self._driverScrollList = cmds.textScrollList( h= self._height )
        self._movedDriverInst = MovedDriverList( self._mainWidthList[0], self._driverScrollList )
        uifnc.setSpace()
        cmds.setParent( '..' )
        
        self._rowColumns = [ column1, column2, column3, column4 ]