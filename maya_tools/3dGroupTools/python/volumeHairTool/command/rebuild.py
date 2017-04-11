import maya.cmds as cmds
import maya.OpenMaya as om
import volumeHairTool.functions as fnc
import volumeHairTool.progress as progress



class SetDirection:


    def __init__(self, surfaceObject, mesh ):

        currentSurface = fnc.getShapeFromObject( surfaceObject, 'nurbsSurface' )
        
        if fnc.checkComponentIsMoved( currentSurface ):
            jnt = cmds.createNode( 'joint' )
            cmds.skinCluster( [currentSurface, jnt] )
            cmds.select( currentSurface )
            cmds.DeleteHistory()
            cmds.delete( jnt )
        
        origSurface    = fnc.getOrigShape( currentSurface )
        
        self.checkReverseOption( origSurface, mesh )
        self.doIt( currentSurface )


    def checkReverseOption(self, origSurface, mesh ):

        surface = origSurface
        
        self._doSwap = False
        self._doReverse = False
        self._canNotCheck = False

        surfaceMtxList = cmds.getAttr( surface+'.worldMatrix' )
        meshMtxList = cmds.getAttr( mesh+'.worldMatrix' )

        surfaceMatrix = om.MMatrix()
        meshMatrix = om.MMatrix()

        om.MScriptUtil.createMatrixFromList( surfaceMtxList, surfaceMatrix )
        om.MScriptUtil.createMatrixFromList( meshMtxList, meshMatrix )

        fnSurface = om.MFnNurbsSurface( fnc.getMObject( surface ) )
        self._fnMesh    = om.MFnMesh( fnc.getMObject( mesh ) )

        minRangeU, maxRangeU = cmds.getAttr( surface+'.minMaxRangeU' )[0]
        minRangeV, maxRangeV = cmds.getAttr( surface+'.minMaxRangeV' )[0]

        nUnV_point = om.MPoint()
        nUxV_point = om.MPoint()
        xUnV_point = om.MPoint()
        xUxV_point = om.MPoint()

        fnSurface.getPointAtParam( minRangeU,minRangeV, nUnV_point )
        fnSurface.getPointAtParam( minRangeU,maxRangeV, nUxV_point )
        fnSurface.getPointAtParam( maxRangeU,minRangeV, xUnV_point )
        fnSurface.getPointAtParam( maxRangeU,maxRangeV, xUxV_point )

        nUnV_point *= surfaceMatrix*meshMatrix.inverse()
        nUxV_point *= surfaceMatrix*meshMatrix.inverse()
        xUnV_point *= surfaceMatrix*meshMatrix.inverse()
        xUxV_point *= surfaceMatrix*meshMatrix.inverse()

        closePoint = om.MPoint()
        closeNormal = om.MVector()

        self._fnMesh.getClosestPointAndNormal( nUnV_point,  closePoint, closeNormal )
        if( ( nUnV_point-closePoint )*closeNormal < 0 ):
            nUnV = 'in'
        else: nUnV = 'out'
        self._fnMesh.getClosestPointAndNormal( nUxV_point,  closePoint, closeNormal )
        if( ( nUxV_point-closePoint )*closeNormal < 0 ):
            nUxV = 'in'
        else: nUxV = 'out'
        self._fnMesh.getClosestPointAndNormal( xUnV_point,  closePoint, closeNormal )
        if( ( xUnV_point-closePoint )*closeNormal < 0 ):
            xUnV = 'in'
        else: xUnV = 'out'
        self._fnMesh.getClosestPointAndNormal( xUxV_point,  closePoint, closeNormal )
        if( ( xUxV_point-closePoint )*closeNormal < 0 ):
            xUxV = 'in'
        else: xUxV = 'out'


        if( [nUnV,nUxV,xUnV,xUxV] == ['in','in','out','out'] ):
            self._doSwap = False
            self._doReverse = False
        elif( [nUnV,nUxV,xUnV,xUxV] == ['in','out','in','out'] ):
            self._doSwap = True
            self._doReverse = False
        elif( [nUnV,nUxV,xUnV,xUxV] == ['out','out','in','in'] ):
            self._doSwap = False
            self._doReverse = True
        elif( [nUnV,nUxV,xUnV,xUxV] == ['out','in','out','in'] ):
            self._doSwap = True
            self._doReverse = True
        else:
            self._canNotCheck = True
            print nUnV,nUxV,xUnV,xUxV


    def doIt( self, currentSurface ):
        
        if self._canNotCheck: 
            print currentSurface
            return None

        surface = currentSurface

        reverseNum = 0
        reverseNum += self._doSwap
        reverseNum += self._doReverse

        hists = cmds.listHistory( surface )

        reverseNodes = []
        
        for hist in hists:
            if cmds.nodeType( hist ) == 'reverseSurface':
                reverseNum -= 1
                if reverseNum == -1:
                    outputCon = cmds.listConnections( hist, s=1, d=0, c=1, p=1 )[1]
                    inputCon  = cmds.listConnections( hist, s=0, d=1, c=1, p=1 )[1]
                    cmds.connectAttr( outputCon, inputCon, f=1 )
                    cmds.delete( hist )
                    reverseNum += 1
                else:
                    reverseNodes.append( hist )

        if self._doSwap:
            if reverseNodes:
                cmds.setAttr( reverseNodes.pop() + '.direction', 3 )
            else:
                cmds.reverseSurface( surface, d=3, ch=1, rpo=1 )
        if self._doReverse:
            if reverseNodes:
                cmds.setAttr( reverseNodes.pop() + '.direction', 0 )
            else:
                cmds.reverseSurface( surface, d=0, ch=1, rpo=1 )



class AverageRebuild:


    def __init__(self ):
        
        self._length = 0
        self._numSpansList = []
        self._surfaceList = []
        self._lengthList = []
        
    
    def appendSurfaceInfo(self, surface ):
        
        if fnc.checkComponentIsMoved( surface ):
            jnt = cmds.createNode( 'joint' )
            cmds.skinCluster( [surface, jnt] )
            cmds.select( surface )
            cmds.DeleteHistory()
            cmds.delete( jnt )
        
        fnSurface = om.MFnNurbsSurface( fnc.getMObject( fnc.getOrigShape( surface ) ) )
        surfaceMatrix = fnc.getMMatrixFromMtxList( cmds.getAttr( surface+'.wm' ) )
        
        reverseRate = 0
        for hist in cmds.listHistory( surface ):
            if cmds.nodeType( hist ) == 'reverseSurface':
                if cmds.getAttr( hist+'.direction' ) == 3:
                    reverseRate = 1-reverseRate
        
        if reverseRate:
            numSpans = fnSurface.numSpansInV()
            degree = fnSurface.degreeV()
            numFirst = fnSurface.numCVsInV()
            numSecond = fnSurface.numCVsInU()
        else:
            numSpans = fnSurface.numSpansInU()
            degree = fnSurface.degreeU()
            numFirst = fnSurface.numCVsInU()
            numSecond = fnSurface.numCVsInV()
        
        cvPoints = om.MPointArray()
        cvPoints.setLength( numFirst )
        knots    = om.MDoubleArray()
        knots.setLength( numFirst+degree-1 )
        
        for i in range( numFirst ):
            bbox = om.MBoundingBox()
            point = om.MPoint()
            for j in range( numSecond ):
                if reverseRate:
                    fnSurface.getCV( j, i, point )
                else:
                    fnSurface.getCV( i, j, point )
                bbox.expand( point )
            minPoint = om.MVector( bbox.min() )
            maxPoint = om.MVector( bbox.max() )
            cPoint = om.MPoint(( minPoint + maxPoint )/2)*surfaceMatrix
            cvPoints.set( cPoint, i )
            
        for i in range( numFirst+degree-1 ):
            if i < degree-1:
                knots[i] = 0
            elif i-degree+1 > numSpans:
                knots[i] = numSpans
            else:
                knots[i] = i-degree+1
        
        curveData = om.MFnNurbsCurveData()
        createCurveObj = curveData.create()
        fnCreateCurve = om.MFnNurbsCurve()
        fnCreateCurve.create( cvPoints, knots, degree, om.MFnNurbsCurve.kOpen, 0,0, createCurveObj )
        
        fnCurve = om.MFnNurbsCurve( createCurveObj )
        
        self._numSpansList.append( numSpans )
        self._surfaceList.append( surface )
        self._lengthList.append( fnCurve.length() )
        self._length += 1


    def doIt(self, rebuildRate=1, keepOriginal = 0 ):
        
        allSpans = 0.0
        allLength = 0.0
        
        for i in range( self._length ):
            allSpans += self._numSpansList[i]
            allLength += self._lengthList[i]
        
        spanRate = allSpans / allLength
        
        progress.setLength( self._length )
        
        for i in range( self._length ):
            progress.addCount()
            
            hists = cmds.listHistory( self._surfaceList[i] )
            deleteNode = False
            for hist in hists:
                if cmds.nodeType( hist ) == 'rebuildSurface':
                    if deleteNode:
                        hists.remove( hist )
                        cmds.delete( hist )
                elif cmds.nodeType( hist ) == 'reverseSurface':
                    deleteNode = True
            
            if keepOriginal:
                currentSpan = self._numSpansList[i]
            else:
                currentSpan = round( spanRate*self._lengthList[i]*rebuildRate )
                
            rebuildNode = None
            for hist in hists:
                if cmds.nodeType( hist ) == 'rebuildSurface':
                    rebuildNode = hist
            
            if rebuildNode:
                cmds.setAttr( rebuildNode+'.rebuildType', 0 )
                cmds.setAttr( rebuildNode+'.rebuildType', 0 )
                cmds.setAttr( rebuildNode+'.spansU', currentSpan )
                cmds.setAttr( rebuildNode+'.degreeU', 0 )
                cmds.setAttr( rebuildNode+'.degreeV', 0 )
                cmds.setAttr( rebuildNode+'.tolerance', 0.01 )
                cmds.setAttr( rebuildNode+'.endKnots', 0 )
                cmds.setAttr( rebuildNode+'.keepCorners', 0 )
                cmds.setAttr( rebuildNode+'.keepRange', 0 )
                cmds.setAttr( rebuildNode+'.keepControlPoints', 0 )
            else:
                cmds.rebuildSurface( self._surfaceList[i], ch=1, rpo=1, rt=0, end=1, kr=1, kcp=0, kc=0, su=currentSpan, du=0, dv=0, tol=0.01, fr=0, dir=0 )