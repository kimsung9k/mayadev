from cmdModel import *
from uiModel import *
import dataModel

from functools import partial


class CreateControllerUI:
    
    def __init__(self):
        
        self._targetInstList = []
        
        for i in dir( dataModel ):
            if i.find( '__' ) != 0:
                exec( "self._targetInstList.append( dataModel.%s() )" % i )
                
        self._dragStart = False
                
                
    def cmdPutController(self, targetClass, *args ):
        
        shapeSelectList = cmds.radioCollection( self._shapeCollection, q=1, cia=1 )
        poseSelectList  = cmds.radioCollection( self._poseCollection, q=1, cia=1 )
        shapeSelect = cmds.radioCollection( self._shapeCollection, q=1, sl=1 )
        poseSelect = cmds.radioCollection( self._poseCollection, q=1, sl=1 )
        
        shapeSelIndex = 0
        for i in range( len( shapeSelectList ) ):
            if shapeSelectList[i].find( shapeSelect ) != -1:
                shapeSelIndex = i
               
        poseSelIndex = 0
        for i in range( len( poseSelectList ) ):
            if poseSelectList[i].find( poseSelect ) != -1:
                poseSelIndex = i
        
        shapeOptions = ['Curve', 'All', 'Polygon']
        poseOptions  = ['Translate', 'All', 'Rotate' ]
        
        ucCreateControler( targetClass, shapeOptions[ shapeSelIndex ],
                                        poseOptions[ poseSelIndex ], *args )
        
        
    def cmdRotXController(self, *args ):
        
        degree = cmds.intSliderGrp( self._degreeSlider, q=1, v=1 )
        ucEditShapeByRot( [degree,0,0] )
        
    
    def cmdRotYController(self, *args ):
        
        degree = cmds.intSliderGrp( self._degreeSlider, q=1, v=1 )
        ucEditShapeByRot( [0,degree,0] )
        
        
    def cmdRotZController(self, *args ):
        
        degree = cmds.intSliderGrp( self._degreeSlider, q=1, v=1 )
        ucEditShapeByRot( [0,0,degree] )
    
        
        
    def cmdChangeScaleController(self, *args ):
        
        scale = cmds.floatSliderGrp( self._scaleSlider, q=1, v=1 )
        if self._dragStart:
            ucSetBasePoints()
            ucSetPoints( [scale,scale,scale] )
            self._dragStart = False
        else:
            ucGetBasePoints()
            ucSetPoints( [scale,scale,scale] )
            self._dragStart = False
            
        cmds.floatSliderGrp( self._scaleSlider, e=1, v=1 )
        

    def cmdDragScaleController(self, *args ):
        
        if not self._dragStart:
            ucGetBasePoints()
            self._dragStart = True
        scale = cmds.floatSliderGrp( self._scaleSlider, q=1, v=1 )
        ucSetPointsDrag( [scale,scale,scale] )
        
    
    
    def show(self):
        
        iconPath   = CreateControllerUIInfo._iconImagePath
        iconWidth  = CreateControllerUIInfo._iconWidth
        iconHeight = CreateControllerUIInfo._iconHeight
        windowWidth = CreateControllerUIInfo._width
        windowHeight = CreateControllerUIInfo._height
        
        if cmds.window( CreateControllerUIInfo._winName, ex=1 ):
            cmds.deleteUI( CreateControllerUIInfo._winName, wnd=1 )
        cmds.window( CreateControllerUIInfo._winName,
                     title= CreateControllerUIInfo._title )
        
        cmds.columnLayout()
        
        cmds.frameLayout( label='Add Shape', borderStyle='etchedIn', w=windowWidth )
        firstWidth = int( windowWidth * 0.33 )
        secondWidth = int( windowWidth * 0.33 )
        thirdWidth  = windowWidth - firstWidth - secondWidth
        cmds.rowColumnLayout( nc=3, co=[(1,'left',10),(2,'left',10),(3,'left',10)],
                              cw=[(1,firstWidth),(2,secondWidth),(3,thirdWidth)])
        shapeCollection = cmds.radioCollection()
        cmds.radioButton( l='Curve', sl=1 )
        cmds.radioButton( l='All' )
        cmds.radioButton( l='Polygon' )
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        
        cmds.frameLayout( label='Set Position', borderStyle='etchedIn', w=windowWidth )
        firstWidth = int( windowWidth * 0.33 )
        secondWidth = int( windowWidth * 0.33 )
        thirdWidth  = windowWidth - firstWidth - secondWidth
        cmds.rowColumnLayout( nc=3, co=[(1,'left',10),(2,'left',10),(3,'left',10)],
                              cw=[(1,firstWidth),(2,secondWidth),(3,thirdWidth)] )
        poseCollection = cmds.radioCollection()
        cmds.radioButton( l='Translate', sl=1 )
        cmds.radioButton( l='All' )
        cmds.radioButton( l='Rotate' )
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        
        cmds.frameLayout( borderStyle='out', w=windowWidth, lv=0 )
        cmds.rowColumnLayout( nc=5,cw=[(1,64),(2,64),(2,64),(2,64),(2,64)])
        for inst in self._targetInstList:
            cmds.iconTextButton( i=iconPath+'/%s.png' % inst.name, w=iconWidth, h=iconHeight,
                                 c=partial( self.cmdPutController, inst ) )
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        
        cmds.frameLayout( label='Shape Control', borderStyle='etchedIn', w=windowWidth )
        cmds.text( l='', h=5 )
        firstWidth = int( (windowWidth-4) * 0.33 )
        secondWidth = int( (windowWidth-4) * 0.20 )
        thirdWidth  = windowWidth -4 - firstWidth - secondWidth
        degreeSlider = cmds.intSliderGrp( l='Degree : ', f=1, min=0, max=90, v=45, step=5, cw=[(1,firstWidth),(2,secondWidth),(3,thirdWidth)] )
        firstWidth = int( (windowWidth-4) * 0.33 )
        secondWidth = int( (windowWidth-4) * 0.33 )
        thirdWidth  = windowWidth -4 - firstWidth - secondWidth
        cmds.rowColumnLayout( nc=4, cw=[(1,firstWidth),(2,secondWidth),(3,thirdWidth)])
        cmds.button( l='RotateX', c= self.cmdRotXController )
        cmds.button( l='RotateY', c= self.cmdRotYController )
        cmds.button( l='RotateZ', c= self.cmdRotZController )
        cmds.setParent( '..' )
        
        firstWidth = int( (windowWidth-4) * 0.33 )
        secondWidth = int( (windowWidth-4) * 0.20 )
        thirdWidth  = windowWidth -4 - firstWidth - secondWidth
        scaleSlider =cmds.floatSliderGrp( l='Set Scale', f=1, min=0, max=2, v=1, pre=2, cw=[(1,firstWidth),(2,secondWidth),(3,thirdWidth)],
                                          dc=self.cmdDragScaleController, cc= self.cmdChangeScaleController )
        cmds.text( l='', h=5 )
        cmds.setParent( '..' )
        
        cmds.window( CreateControllerUIInfo._winName, e=1,
                     w=windowWidth, h=windowHeight )
        cmds.showWindow( CreateControllerUIInfo._winName )
        
        self._shapeCollection = shapeCollection
        self._poseCollection  = poseCollection
        self._degreeSlider  = degreeSlider
        self._scaleSlider = scaleSlider