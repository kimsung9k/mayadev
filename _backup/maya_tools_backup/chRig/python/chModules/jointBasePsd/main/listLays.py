import maya.cmds as cmds
import jointBasePsd.uifunctions as uifnc
import math


class MovedDriverList:
    
    def __init__(self, width, minValue ):
        
        self._width = width
        self._minValue = minValue
    
    
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
        cmds.floatField( precision=2, v=angleValues[1], bgc= bgcList[1] )
        cmds.floatField( precision=2, v=angleValues[2], bgc= bgcList[2] )
        
        '''
        uifnc.setSpace()
        cmds.button( l='%5.2f' % angleValues[0], en= enList[0] )
        cmds.button( l='%5.2f' % angleValues[1], en= enList[1] )
        cmds.button( l='%5.2f' % angleValues[2], en= enList[2] )
        '''
        cmds.setParent( '..' )