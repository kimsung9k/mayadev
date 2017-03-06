import maya.cmds as cmds
import uiInfo
from functools import partial
import volumeHairTool.command.volume as mainCmd
import volumeHairTool.progress as progress


class Cmd:
    
    def __init__(self):
        
        self._dragStart = False
        self._targetCurves = []
        self._keepTargetCurveValues = []
        

    def setCmd(self, winPointer, basePointer, *args ):
        
        sels = cmds.ls( sl=1 )
        
        baseMesh = cmds.textField( basePointer._baseMesh, q=1, tx=1 )
        meshObj = cmds.listRelatives( baseMesh, p=1 )[0]
        surfs = winPointer.getSurfaceShapes( basePointer )
        
        numSpansEn = cmds.checkBox( self._byNumSpans, q=1, v=1 )
        otNumCurve = cmds.intSliderGrp( self._outerNumCurve, q=1, v=1 )
        otORand = cmds.floatSliderGrp( self._outerOffsetRand, q=1, v=1 )
        otPRand = cmds.floatSliderGrp( self._outerParamRand, q=1, v=1 )
        
        inNumCurve = cmds.intSliderGrp( self._numCurve, q=1, v=1 )
        inORand = cmds.floatSliderGrp( self._innerOffsetRand, q=1, v=1 )
        inPRand = cmds.floatSliderGrp( self._innerParamRand, q=1, v=1 )
        
        progress.start()
        progress.append( 'Volume' )
        
        progress.setLength( len( surfs ) )
        
        for surf in surfs:
            progress.addCount()
            surfObj = cmds.listRelatives( surf, p=1 )[0]
            mainInst = mainCmd.CreateVolumeHair( surfObj, meshObj )
            mainInst.createInCurve( inNumCurve, inPRand, inORand )
            
            if numSpansEn:
                surfShape = cmds.listRelatives( surfObj, s=1 )[0]
                minV, maxV = cmds.getAttr( surfShape+'.minMaxRangeV' )[0]
                mainInst.createOutCurve( maxV - minV, otPRand, otORand )
            else:
                mainInst.createOutCurve( otNumCurve, otPRand, otORand )

        progress.end()
            
        if sels:
            try:cmds.select( sels )
            except:pass
            
            
    def selectCurveCmd(self, winPointer, basePointer, curveTypeList, *args ):
        
        surfs = winPointer.getSurfaceShapes( basePointer )
        
        targetCurves = []
        
        for surf in surfs:
            volumeCurvesOnSurfNodes = cmds.listConnections( surf, type='volumeCurvesOnSurface' )
            
            if not volumeCurvesOnSurfNodes: continue
            
            for volumeCurvesOnSurfNode in volumeCurvesOnSurfNodes:
                for curveType in curveTypeList:
                    if cmds.attributeQuery( curveType, node= volumeCurvesOnSurfNode, ex=1 ):
                        outputCurves = cmds.listConnections( volumeCurvesOnSurfNode+'.outputCurve', type='nurbsCurve', s=0, d=1 )
                        
                        if outputCurves:
                            targetCurves += outputCurves
        
        if targetCurves:
            cmds.select( targetCurves )
        
        

    def offsetCurveDragCmd(self, *args ):
        
        if not self._dragStart:
            
            selCurves = cmds.ls( sl=1 )
        
            self._targetCurves = []
            self._keepTargetCurveValues = []
            for curve in selCurves:
                if cmds.attributeQuery( 'centerRate' , node = curve, ex=1 ):
                    self._targetCurves.append( curve )
                    self._keepTargetCurveValues.append( cmds.getAttr( curve+'.centerRate' ) )
            
            if not self._targetCurves:
                cmds.warning( "Select VolumeCurves" )
                return None
            
            self._dragStart = True
            cmds.undoInfo( swf=0 )
            
        multRate = cmds.floatSliderGrp( self._offsetCurve, q=1, v=1 )
            
        for i in range( len( self._targetCurves ) ):
            targetCurve = self._targetCurves[i]
            value       = self._keepTargetCurveValues[i]
            
            cmds.setAttr( targetCurve+'.centerRate', value*multRate )
            
            

    def offsetCurveChangeCmd(self, *args ):
        
        multRate = cmds.floatSliderGrp( self._offsetCurve, q=1, v=1 )
        cmds.floatSliderGrp( self._offsetCurve, e=1, v=1 )
        
        if self._dragStart:
            
            for i in range( len( self._targetCurves ) ):
                targetCurve= self._targetCurves[i]
                value      = self._keepTargetCurveValues[i]
                cmds.setAttr( targetCurve+'.centerRate', value )
            
            cmds.undoInfo( swf=1 )
            self._dragStart = False
            
            for i in range( len( self._targetCurves ) ):
                targetCurve= self._targetCurves[i]
                value      = self._keepTargetCurveValues[i]
                cmds.setAttr( targetCurve+'.centerRate', value*multRate )
        else:
            selCurves = cmds.ls( sl=1 )
        
            self._targetCurves = []
            self._keepTargetCurveValues = []
            for curve in selCurves:
                if cmds.attributeQuery( 'centerRate' , node = curve, ex=1 ):
                    self._targetCurves.append( curve )
                    self._keepTargetCurveValues.append( cmds.getAttr( curve+'.centerRate' ) )
            
            if not self._targetCurves:
                cmds.warning( "Select VolumeCurves" )
                return None
            
            for i in range( len( self._targetCurves ) ):
                targetCurve= self._targetCurves[i]
                value      = self._keepTargetCurveValues[i]
                cmds.setAttr( targetCurve+'.centerRate', value*multRate )
                
                
    def byNumSpansCmd(self, *args ):
        
        value = cmds.checkBox( self._byNumSpans, q=1, v=1 )
        
        if value:
            cmds.intSliderGrp( self._outerNumCurve, e=1, en=0 )
        else:
            cmds.intSliderGrp( self._outerNumCurve, e=1, en=1 )
                


class Add( Cmd ):
    
    def __init__(self, winPointer, basePointer ):
        
        Cmd.__init__(self)
        
        self._uiName = "volumeHairTool_volumeHair"
        self._label = "  Volume"
        self._width = winPointer._width-4
        self._densityDefault = 3
        
        self._winPointer = winPointer
        self._basePointer = basePointer
        
        self.core()
        

    def core(self):
        
        uiInfo.addFrameLayout( self._uiName, self._label )
        
        uiInfo.setSpace( 10 )
        
        uiInfo.floatSliderColumn( self._width )
        cmds.text( l="Outer Curve : ", al='right' )
        self._byNumSpans = cmds.checkBox( l='By Num Spans', cc= self.byNumSpansCmd )
        uiInfo.setSpace()
        self._outerNumCurve  = uiInfo.intSlider( 0, 5, 30, self._densityDefault )
        cmds.text( l="Offset Rand Rate : ", al='right' )
        self._outerOffsetRand  = uiInfo.floatSlider( 0, 1, 1, 0.1 )
        cmds.text( l="Param Rand Rate : ", al='right' )
        self._outerParamRand  = uiInfo.floatSlider( 0, 1, 1, 0.1 )
        cmds.setParent( '..' )
        
        uiInfo.floatSliderColumn( self._width )
        cmds.text( l="Inner Curve : ", al='right' )
        self._numCurve  = uiInfo.intSlider( 0, 5, 30, self._densityDefault )
        cmds.text( l="Offset Rand Rate : ", al='right' )
        self._innerOffsetRand  = uiInfo.floatSlider( 0, 1, 1, 0.1 )
        cmds.text( l="Param Rand Rate : ", al='right' )
        self._innerParamRand  = uiInfo.floatSlider( 0, 1, 1, 0.1 )
        cmds.setParent( '..' )
        
        uiInfo.setSpace( 5 )
        
        cmds.rowColumnLayout( nc=3, cw=[(1,10),(2,self._width-20),(3,10)])
        uiInfo.setSpace()
        uiInfo.setButton( partial( self.setCmd, self._winPointer, self._basePointer ) )
        uiInfo.setSpace()
        cmds.setParent( '..' )
        
        uiInfo.separator( self._width, 2 )
        
        halfWidth = ( self._width - 20) /2
        elseWidth = ( self._width - 20) - halfWidth
        
        cmds.rowColumnLayout( nc=4, cw=[(1,10),(2,halfWidth),(3,elseWidth),(4,10)])
        uiInfo.setSpace()
        cmds.button( l='Select In Curve', h=25, c = partial( self.selectCurveCmd, self._winPointer, self._basePointer, ['isInCurveNode'] ) )
        cmds.button( l='Select Out Curve', h=25, c = partial( self.selectCurveCmd, self._winPointer, self._basePointer, ['isOutCurveNode'] ) )
        uiInfo.setSpace()
        cmds.setParent( '..' )
        
        cmds.rowColumnLayout( nc=3, cw=[(1,10),(2,self._width-20),(3,10)])
        uiInfo.setSpace()
        cmds.button( l='Select All Curve', h=30, c = partial( self.selectCurveCmd, self._winPointer, self._basePointer, ['isInCurveNode', 'isOutCurveNode'] ) )
        uiInfo.setSpace()
        cmds.setParent( '..' )
        
        uiInfo.floatSliderColumn( self._width )
        cmds.text( l="Offset Curve : ", al='right' )
        self._offsetCurve  = uiInfo.floatSlider( 0, 2, 2, 1 )
        cmds.floatSliderGrp( self._offsetCurve, e=1, dc= self.offsetCurveDragCmd, cc=self.offsetCurveChangeCmd )
        cmds.setParent( '..' )
        
        uiInfo.setSpace( 5 )
        
        uiInfo.getOutFrameLayout()
        
        
    def clear(self):
        
        cmds.floatSliderGrp( self._density, e=1, v=.5 )
        cmds.floatSliderGrp( self._offset, e=1, v=.1 )
        self.saveData()