from maya import cmds, OpenMaya
import pymel.core, copy, math
from functools import partial


class Win_Global:
    
    winName = 'sg_createFkControl_ui'
    title = "UI - Create Fk Control"
    width = 300
    height = 50



class Controller:
    
    pinPoints = [[0.00000,0.00000,0.00000],
            [0.00000,0.99175,0.00000],
            [0.09028,1.01594,0.00000],
            [0.15637,1.08203,0.00000],
            [0.18056,1.17232,0.00000],
            [0.15637,1.26260,0.00000],
            [0.09028,1.32869,0.00000],
            [0.00000,1.35288,0.00000],
            [-0.09028,1.32869,0.00000],
            [-0.15637,1.26260,0.00000],
            [-0.18056,1.17232,0.00000],
            [-0.15637,1.08203,0.00000],
            [-0.09028,1.01594,0.00000],
            [0.00000,0.99175,0.00000]]

    
    circlePoints = [[0.00000,0.00000,-1.00000],
            [-0.17365,0.00000,-0.98481],
            [-0.34202,0.00000,-0.93969],
            [-0.50000,0.00000,-0.86603],
            [-0.64279,0.00000,-0.76604],
            [-0.76604,0.00000,-0.64279],
            [-0.86603,0.00000,-0.50000],
            [-0.93969,0.00000,-0.34202],
            [-0.98481,0.00000,-0.17365],
            [-1.00000,0.00000,-0.00000],
            [-0.98481,-0.00000,0.17365],
            [-0.93969,-0.00000,0.34202],
            [-0.86603,-0.00000,0.50000],
            [-0.76604,-0.00000,0.64279],
            [-0.64279,-0.00000,0.76604],
            [-0.50000,-0.00000,0.86603],
            [-0.34202,-0.00000,0.93969],
            [-0.17365,-0.00000,0.98481],
            [-0.00000,-0.00000,1.00000],
            [0.17365,-0.00000,0.98481],
            [0.34202,-0.00000,0.93969],
            [0.50000,-0.00000,0.86603],
            [0.64279,-0.00000,0.76604],
            [0.76604,-0.00000,0.64279],
            [0.86603,-0.00000,0.50000],
            [0.93969,-0.00000,0.34202],
            [0.98481,-0.00000,0.17365],
            [1.00000,-0.00000,0.00000],
            [0.98481,0.00000,-0.17365],
            [0.93969,0.00000,-0.34202],
            [0.86603,0.00000,-0.50000],
            [0.76604,0.00000,-0.64279],
            [0.64279,0.00000,-0.76604],
            [0.50000,0.00000,-0.86603],
            [0.34202,0.00000,-0.93969],
            [0.17365,0.00000,-0.98481],
            [0.00000,0.00000,-1.00000]]




class sgCmds:
    
    @staticmethod
    def getMObject( inputTarget ):
        target = pymel.core.ls( inputTarget )[0]
        mObject = OpenMaya.MObject()
        selList = OpenMaya.MSelectionList()
        selList.add( target.name() )
        selList.getDependNode( 0, mObject )
        return mObject
    
    
    @staticmethod
    def getDefaultMatrix():
        return [1,0,0,0, 0,1,0,0, 0,0,1,0 ,0,0,0,1]


    @staticmethod
    def makeParent( inputSel, **options ):
    
        sel = pymel.core.ls( inputSel )[0]
        if not options.has_key( 'n' ) and not options.has_key( 'name' ):
            options.update( {'n':'P'+ sel.shortName()} )
        selP = sel.getParent()
        transform = pymel.core.createNode( 'transform', **options )
        if selP: pymel.core.parent( transform, selP )
        pymel.core.xform( transform, ws=1, matrix= sel.wm.get() )
        pymel.core.parent( sel, transform )
        pymel.core.xform( sel, os=1, matrix= sgCmds.getDefaultMatrix() )
        return transform
    
    
    
    @staticmethod
    def copyShapeToTransform( inputShape, inputTransform ):
    
        shape = pymel.core.ls( inputShape )[0]
        transform = pymel.core.ls( inputTransform )[0]
        
        oTarget = sgCmds.getMObject( transform )
        if shape.type() == 'mesh':
            oMesh = sgCmds.getMObject( shape )
            fnMesh = OpenMaya.MFnMesh( oMesh )
            fnMesh.copy( oMesh, oTarget )
        elif shape.type() == 'nurbsCurve':
            oCurve = sgCmds.getMObject( shape )
            fnCurve = OpenMaya.MFnNurbsCurve( oCurve )
            fnCurve.copy( oCurve, oTarget )
        elif shape.type() == 'nurbsSurface':
            oSurface = sgCmds.getMObject( shape )
            fnSurface = OpenMaya.MFnNurbsSurface( oSurface )
            fnSurface.copy( oSurface, oTarget )
    
    
    
    @staticmethod
    def addIOShape( inputShape ):
    
        shape = pymel.core.ls( inputShape )[0]
        
        if shape.type() == 'transform':
            targetShape = shape.getShape()
        else:
            targetShape = shape
        
        targetTr    = targetShape.getParent()
        newShapeTr = pymel.core.createNode( 'transform' )
        sgCmds.copyShapeToTransform( targetShape, newShapeTr )
        ioShape = newShapeTr.getShape()
        ioShape.attr( 'io' ).set( 1 )
        pymel.core.parent( ioShape, targetTr, add=1, shape=1 )
        pymel.core.delete( newShapeTr )
        return targetTr.listRelatives( s=1 )[-1]


    @staticmethod
    def makeController( pointList, defaultScaleMult = 1, **options ):
    
        newPointList = copy.deepcopy( pointList )
        
        options.update( {'p':newPointList, 'd':1} )
        
        typ = 'transform'
        if options.has_key( 'typ' ):
            typ = options.pop( 'typ' )
        
        mp = False
        if options.has_key( 'makeParent' ):
            mp = options.pop('makeParent')
        
        colorIndex = -1
        if options.has_key( 'colorIndex' ):
            colorIndex = options.pop('colorIndex')
        
        crv = pymel.core.curve( **options )
        crvShape = crv.getShape()
        
        if options.has_key( 'n' ):
            name = options['n']
        elif options.has_key( 'name' ):
            name = options['name']
        else:
            name = None
        
        jnt = pymel.core.ls( cmds.createNode( typ ) )[0]
        pJnt = None
        
        if mp:
            pJnt = pymel.core.ls( sgCmds.makeParent( jnt ) )[0]
        
        if name:
            jnt.rename( name )
            if pJnt:
                pJnt.rename( 'P' + name )
    
        pymel.core.parent( crvShape, jnt, add=1, shape=1 )
        pymel.core.delete( crv )
        crvShape = jnt.getShape()
        
        ioShape = sgCmds.addIOShape( jnt )
        ioShape = pymel.core.ls( ioShape )[0]
        
        jnt.addAttr( 'shape_tx', dv=0 ); jnt.shape_tx.set( e=1, cb=1 )
        jnt.addAttr( 'shape_ty', dv=0); jnt.shape_ty.set( e=1, cb=1 )
        jnt.addAttr( 'shape_tz', dv=0); jnt.shape_tz.set( e=1, cb=1 )
        jnt.addAttr( 'shape_rx', dv=0, at='doubleAngle' ); jnt.shape_rx.set( e=1, cb=1 )
        jnt.addAttr( 'shape_ry', dv=0, at='doubleAngle' ); jnt.shape_ry.set( e=1, cb=1 )
        jnt.addAttr( 'shape_rz', dv=0, at='doubleAngle' ); jnt.shape_rz.set( e=1, cb=1 )
        jnt.addAttr( 'shape_sx', dv=1 ); jnt.shape_sx.set( e=1, cb=1 )
        jnt.addAttr( 'shape_sy', dv=1 ); jnt.shape_sy.set( e=1, cb=1 )
        jnt.addAttr( 'shape_sz', dv=1 ); jnt.shape_sz.set( e=1, cb=1 )
        jnt.addAttr( 'scaleMult', dv=defaultScaleMult, min=0 ); jnt.scaleMult.set( e=1, cb=1 )
        composeMatrix = pymel.core.createNode( 'composeMatrix' )
        composeMatrix2 = pymel.core.createNode( 'composeMatrix' )
        multMatrix = pymel.core.createNode( 'multMatrix' )
        composeMatrix.outputMatrix >> multMatrix.i[0]
        composeMatrix2.outputMatrix >> multMatrix.i[1]
        jnt.shape_tx >> composeMatrix.inputTranslateX
        jnt.shape_ty >> composeMatrix.inputTranslateY
        jnt.shape_tz >> composeMatrix.inputTranslateZ
        jnt.shape_rx >> composeMatrix.inputRotateX
        jnt.shape_ry >> composeMatrix.inputRotateY
        jnt.shape_rz >> composeMatrix.inputRotateZ
        jnt.shape_sx >> composeMatrix.inputScaleX
        jnt.shape_sy >> composeMatrix.inputScaleY
        jnt.shape_sz >> composeMatrix.inputScaleZ
        jnt.scaleMult >> composeMatrix2.inputScaleX
        jnt.scaleMult >> composeMatrix2.inputScaleY
        jnt.scaleMult >> composeMatrix2.inputScaleZ
        trGeo = pymel.core.createNode( 'transformGeometry' )
        try:jnt.attr( 'radius' ).set( 0 )
        except:pass
        
        ioShape.local >> trGeo.inputGeometry
        multMatrix.matrixSum >> trGeo.transform
        
        trGeo.outputGeometry >> crvShape.create
        
        if colorIndex != -1:
            shape = jnt.getShape().name()
            cmds.setAttr( shape + '.overrideEnabled', 1 )
            cmds.setAttr( shape + '.overrideColor', colorIndex )
    
        return jnt
    
    
    @staticmethod
    def setTransformDefault( inputTarget ):
        target = pymel.core.ls( inputTarget )[0]
        attrs = ['tx','ty','tz','rx','ry','rz','sx','sy','sz']
        values = [0,0,0,0,0,0,1,1,1]
        for i in range( len( attrs ) ):
            try:cmds.setAttr( target + '.' + attrs[i], values[i] )
            except:pass
        
    
    
    @staticmethod
    def getDirectionIndex( inputVector ):
    
        import math
        
        if type( inputVector ) in [ list, tuple ]:
            normalInput = OpenMaya.MVector(*inputVector).normal()
        else:
            normalInput = OpenMaya.MVector(inputVector).normal()
        
        xVector = OpenMaya.MVector( 1,0,0 )
        yVector = OpenMaya.MVector( 0,1,0 )
        zVector = OpenMaya.MVector( 0,0,1 )
        
        xdot = xVector * normalInput
        ydot = yVector * normalInput
        zdot = zVector * normalInput
        
        xabs = math.fabs( xdot )
        yabs = math.fabs( ydot )
        zabs = math.fabs( zdot )
        
        dotList = [xdot, ydot, zdot]
        
        dotIndex = 0
        if xabs < yabs:
            dotIndex = 1
            if yabs < zabs:
                dotIndex = 2
        elif xabs < zabs:
            dotIndex = 2
            
        if dotList[ dotIndex ] < 0:
            dotIndex += 3
        
        return dotIndex
    
    
    @staticmethod
    def getOptionValue( keyName, returnValue, **options ):
    
        if options.has_key( keyName ):
            returnValue = options[ keyName ]
        return returnValue
    
    
    @staticmethod
    def createLocalMatrix( matrixAttr, inverseMatrixAttr ):
        matrixAttr = pymel.core.ls( matrixAttr )[0]
        inverseMatrixAttr = pymel.core.ls( inverseMatrixAttr )[0]
        multMatrixNode = pymel.core.createNode( 'multMatrix' )
        matrixAttr >> multMatrixNode.i[0]
        inverseMatrixAttr >> multMatrixNode.i[1]
        return multMatrixNode
    
    
    @staticmethod
    def getLocalMatrix( matrixAttr, inverseMatrixAttr ):
    
        matrixAttr = pymel.core.ls( matrixAttr )[0]
        inverseMatrixAttr = pymel.core.ls( inverseMatrixAttr )[0]
        multMatrixNodes = matrixAttr.listConnections( d=1, s=0, type='multMatrix' )
        for multMatrixNode in multMatrixNodes:
            firstAttr = multMatrixNode.i[0].listConnections( s=1, d=0, p=1 )
            secondAttr = multMatrixNode.i[1].listConnections( s=1, d=0, p=1 )
            thirdConnection = multMatrixNode.i[2].listConnections( s=1, d=0 )
            
            if not firstAttr or not secondAttr or thirdConnection: continue
            
            firstEqual = firstAttr[0] == matrixAttr
            secondEqual = secondAttr[0] == inverseMatrixAttr
            
            if firstEqual and secondEqual:
                pymel.core.select( multMatrixNode )
                return multMatrixNode
        return sgCmds.createLocalMatrix( matrixAttr, inverseMatrixAttr )
    
    
    
    @staticmethod
    def listToMatrix( mtxList ):
        if type( mtxList ) == OpenMaya.MMatrix:
            return mtxList
        matrix = OpenMaya.MMatrix()
        if type( mtxList ) == list:
            resultMtxList = mtxList
        else:
            resultMtxList = []
            for i in range( 4 ):
                for j in range( 4 ):
                    resultMtxList.append( mtxList[i][j] )
        
        OpenMaya.MScriptUtil.createMatrixFromList( resultMtxList, matrix )
        return matrix
    
    
    
    @staticmethod
    def getMMatrix( inputAttr ):
    
        attr = pymel.core.ls( inputAttr )[0]
        return sgCmds.listToMatrix( cmds.getAttr( attr.name() ) )


    @staticmethod
    def matrixToList( matrix ):
        if type( matrix ) == list:
            return matrix
        mtxList = range( 16 )
        for i in range( 4 ):
            for j in range( 4 ):
                mtxList[ i * 4 + j ] = matrix( i, j )
        return mtxList

    
    
    @staticmethod
    def getTranslateFromMatrix( mtxValue ):
    
        if type( mtxValue ) != list:
            mtxList = sgCmds.matrixToList( mtxValue )
        else:
            mtxList = mtxValue
        
        return mtxList[12:-1]
    
    
    
    @staticmethod
    def getRotateFromMatrix( mtxValue ):
    
        if type( mtxValue ) == list:
            mtxValue = sgCmds.listToMatrix( mtxValue )
        
        trMtx = OpenMaya.MTransformationMatrix( mtxValue )
        rotVector = trMtx.eulerRotation().asVector()
        
        return [math.degrees(rotVector.x), math.degrees(rotVector.y), math.degrees(rotVector.z)]


    
    @staticmethod
    def getShearFromMatrix( mtxValue ):
    
        if type( mtxValue ) == list:
            mtxValue = sgCmds.listToMatrix( mtxValue )
        
        trMtx = OpenMaya.MTransformationMatrix( mtxValue )
        
        util = OpenMaya.MScriptUtil()
        util.createFromDouble(0.0, 0.0, 0.0)
        ptr = util.asDoublePtr()
        trMtx.getShear(ptr, OpenMaya.MSpace.kObject)
        
        shearXY = util.getDoubleArrayItem(ptr, 0)
        shearXZ = util.getDoubleArrayItem(ptr, 1)
        shearYZ = util.getDoubleArrayItem(ptr, 2)
        
        return [shearXY, shearXZ, shearYZ]
    
    
    
    @staticmethod
    def getScaleFromMatrix( mtxValue ):
    
        if type( mtxValue ) == list:
            mtxValue = sgCmds.listToMatrix( mtxValue )
        
        trMtx = OpenMaya.MTransformationMatrix( mtxValue )
        
        util = OpenMaya.MScriptUtil()
        util.createFromDouble(0.0, 0.0, 0.0)
        ptr = util.asDoublePtr()
        trMtx.getScale(ptr, OpenMaya.MSpace.kObject)
        
        scaleX = util.getDoubleArrayItem(ptr, 0)
        scaleY = util.getDoubleArrayItem(ptr, 1)
        scaleZ = util.getDoubleArrayItem(ptr, 2)
        
        return [scaleX, scaleY, scaleZ]
    
    
    @staticmethod
    def getOffsetNode( target, base ):
    
        offsetNode = pymel.core.createNode( 'composeMatrix' )
        matValue = sgCmds.getMMatrix( target.wm ) * sgCmds.getMMatrix( base.wim )
        offsetNode.it.set( sgCmds.getTranslateFromMatrix( matValue ) )
        offsetNode.ir.set( sgCmds.getRotateFromMatrix( matValue ) )
        offsetNode.inputScale.set( sgCmds.getScaleFromMatrix( matValue ) )
        offsetNode.ish.set( sgCmds.getShearFromMatrix( matValue ) )
        return offsetNode
    
    
    @staticmethod
    def insertMatrix( inputTargetAttr, inputMM ):

        targetAttr = pymel.core.ls( inputTargetAttr )[0]
        mm = pymel.core.ls( inputMM )[0]
        
        cons = mm.i.listConnections( s=1, d=0, p=1, c=1 )    
        srcAttrs = []
        dstIndices = []
        for i in range( len( cons ) ):
            origCon, srcCon = cons[i]
            srcAttrs.append( srcCon )
            dstIndices.append( origCon.index()+1 )
            srcCon // origCon
        
        targetAttr >> mm.i[0]
        for i in range( len( srcAttrs ) ):
            srcAttrs[i] >> mm.i[dstIndices[i]]
    


    @staticmethod
    def addAttr( target, **options ):
        
        items = options.items()
        
        attrName = ''
        channelBox = False
        keyable = False
        for key, value in items:
            if key in ['ln', 'longName']:
                attrName = value
            elif key in ['cb', 'channelBox']:
                channelBox = True
                options.pop( key )
            elif key in ['k', 'keyable']:
                keyable = True 
                options.pop( key )
        
        if pymel.core.attributeQuery( attrName, node=target, ex=1 ): return None
        
        pymel.core.addAttr( target, **options )
        
        if channelBox:
            pymel.core.setAttr( target+'.'+attrName, e=1, cb=1 )
        elif keyable:
            pymel.core.setAttr( target+'.'+attrName, e=1, k=1 )



    @staticmethod
    def getDecomposeMatrix( matrixAttr ):
    
        matrixAttr = pymel.core.ls( matrixAttr )[0]
        cons = matrixAttr.listConnections( s=0, d=1, type='decomposeMatrix' )
        if cons: 
            pymel.core.select( cons[0] )
            return cons[0]
        decomposeMatrix = pymel.core.createNode( 'decomposeMatrix' )
        matrixAttr >> decomposeMatrix.imat
        return decomposeMatrix
    
    
    @staticmethod
    def constrain( *inputs, **options ):
    
        srcs   = inputs[:-1]
        target = inputs[-1]
        
        atToChild = False
        mo = False
        ct = True
        cr = True
        cs = False
        csh = False
        
        atToChild = sgCmds.getOptionValue( 'atToChild', atToChild, **options )
        mo = sgCmds.getOptionValue( 'mo', mo, **options )
        ct = sgCmds.getOptionValue( 'ct', ct, **options )
        cr = sgCmds.getOptionValue( 'cr', cr, **options )
        cs = sgCmds.getOptionValue( 'cs', cs, **options )
        csh = sgCmds.getOptionValue( 'csh', csh, **options )
        
        if len( srcs ) == 1:
            mm = sgCmds.getLocalMatrix( srcs[0].wm, target.pim )
            if mo: 
                offsetNode = sgCmds.getOffsetNode( target, srcs[0] )
                sgCmds.insertMatrix( offsetNode.outputMatrix, mm )
        else:
            addNode = pymel.core.createNode( 'plusMinusAverage' )
            conditionNode = pymel.core.createNode( 'condition' )
            addNode.output1D >> conditionNode.firstTerm
            addNode.output1D >> conditionNode.colorIfFalseR
            conditionNode.colorIfTrueR.set( 1 )
            
            wtAddMtx = pymel.core.createNode( 'wtAddMatrix' )
            mm = sgCmds.getLocalMatrix( wtAddMtx.matrixSum, target.pim )
            
            for i in range( len( srcs ) ):
                eachMM = pymel.core.createNode( 'multMatrix' )
                srcs[i].wm >> eachMM.i[0]
                if mo: 
                    offsetNode = sgCmds.getOffsetNode( target, srcs[i] )
                    sgCmds.insertMatrix( offsetNode.outputMatrix, eachMM )
                    
                if atToChild:
                    targetChild = target.listRelatives( c=1, type='transform' )
                    if targetChild:
                        sgCmds.addAttr( targetChild[0], ln='blend_%d' % i, k=1, min=0, dv=1 )
                        blendAttr = targetChild[0].attr( 'blend_%d' % i )
                    else:
                        sgCmds.addAttr( target, ln='blend_%d' % i, k=1, min=0, dv=1 )
                        blendAttr = target.attr( 'blend_%d' % i )
                else:
                    sgCmds.addAttr( target, ln='blend_%d' % i, k=1, min=0, dv=1 )
                    blendAttr = target.attr( 'blend_%d' % i )
                blendAttr >> addNode.input1D[i]
                divNode = pymel.core.createNode( 'multiplyDivide' ); divNode.op.set( 2 )
                blendAttr >> divNode.input1X
                conditionNode.outColorR >> divNode.input2X
                
                eachMM.o >> wtAddMtx.i[i].m
                divNode.outputX >> wtAddMtx.i[i].w
        resultDcmp = sgCmds.getDecomposeMatrix( mm.o )
        
        if ct  : resultDcmp.ot >> target.t
        if cr  : resultDcmp.outputRotate >> target.r
        if cs  : resultDcmp.os >> target.s
        if csh : resultDcmp.osh >> target.sh
    

    @staticmethod
    def createFkControl( topJoint, controllerSize = 1,  pinExists = False ):

        selChildren = topJoint.listRelatives( c=1, ad=1 )
        selH = selChildren + [topJoint]
        selH.reverse()
        
        beforeCtl = None
        ctls = []
        pinCtls = []
        for i in range( len( selH ) ):    
            target = selH[i]
            ctlTarget = sgCmds.makeController( Controller.circlePoints, controllerSize, makeParent=1 )
            ctlP = ctlTarget.getParent()
            pymel.core.xform( ctlP, ws=1, matrix=target.wm.get() )
            if beforeCtl:
                ctlTarget.getParent().setParent( beforeCtl )
            beforeCtl = ctlTarget
            
            if pinExists and ( i != 0 and i != len( selH )-1 ):
                ctlPin = sgCmds.makeController( Controller.pinPoints, controllerSize * 1.2, makeParent=1 )
                ctlPin.shape_ry.set( 90 )
                ctlPinP = ctlPin.getParent()
                ctlPinP.setParent( ctlTarget )
                sgCmds.setTransformDefault( ctlPinP )
                pinCtls.append( ctlPin )
            else:
                pinCtls.append( None )
            ctls.append( ctlTarget )
        
        for i in range( len( selH )-1 ):
            directionIndex = sgCmds.getDirectionIndex( selH[i+1].t.get() )
            
            if directionIndex % 3 == 0:
                ctls[i].shape_rz.set( 90 )
                ctls[i+1].shape_rz.set( 90 )
            elif directionIndex % 3 == 2:
                ctls[i].shape_rx.set( 90 )
                ctls[i+1].shape_rx.set( 90 )
            
            vectorList = [[1,0,0], [0,1,0], [0,0,1], [-1,0,0], [0,-1,0], [0,0,-1]]
            aim = vectorList[ directionIndex ]
            up  = vectorList[ (directionIndex + 1)%6 ]
            aimObj = ctls[i+1]
            upObj = ctls[i]
            if pinCtls[i]:
                upObj = pinCtls[i]
            if pinCtls[i+1]:
                aimObj = pinCtls[i+1]
            pymel.core.aimConstraint( aimObj, selH[i], aim=aim, u=up, wu=up, wut='objectrotation', wuo=upObj )
            sgCmds.constrain( upObj, selH[i], cr=0 )
        sgCmds.constrain( ctls[-1], selH[-1], cr=0 ) 
        
        for i in range( len( selH ) ):
            dcmp = selH[i].listConnections( s=1, d=0, type='decomposeMatrix' )[0]
            dcmp.os >> selH[i].s
            selH[i].attr( 'segmentScaleCompensate' ).set( 1 )
        
        return ctls, pinCtls




class Win_Cmd:
    
    @staticmethod
    def create( *args ):
        
        controllerName = cmds.textField( Win_Global.textField, q=1, tx=1 )
        checked = cmds.checkBox( Win_Global.checkBox, q=1, v=1 )
        colorIndex1 = cmds.intField( Win_Global.intField1, q=1, v=1 )
        colorIndex2 = cmds.intField( Win_Global.intField2, q=1, v=1 )
        controllerSize = cmds.floatField( Win_Global.floatField, q=1, v=1 )
        
        topJoints = pymel.core.ls( sl=1 )
        for i in range( len( topJoints ) ):
            topJoint = topJoints[i]
            ctls, pinCtls = sgCmds.createFkControl( topJoint, controllerSize, checked )
            for j in range( len( ctls ) ):
                ctl = ctls[j]
                pinCtl = pinCtls[j]
                ctl.getShape().overrideEnabled.set( 1 )
                ctl.getShape().overrideColor.set( colorIndex1 )
                
                if pinCtl:
                    pinCtl.getShape().overrideEnabled.set( 1 )
                    pinCtl.getShape().overrideColor.set( colorIndex2 )
                
                if controllerName:
                    if len( topJoints ) == 1:
                        cuName = controllerName + '_%d' %( j )
                    else:
                        cuName = controllerName + '_%d_%d' %( i, j )
                    ctl.rename( cuName )
                    ctl.getParent().rename( 'P' + cuName )
                    if pinCtl:
                        pinCtl.rename( cuName + '_Move' )
                        pinCtl.getParent().rename( 'P' + pinCtl.name() )

    @staticmethod
    def close( *args ):
        cmds.deleteUI( Win_Global.winName )
    



class UI_ControllerName:
    
    def __init__(self):
        
        pass
    
    
    def create(self):
        
        form = cmds.formLayout()
        text = cmds.text( l='Controller Name : ', w=100, al='left', h=25 )
        textField = cmds.textField( h=25, w=150 )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af = [(text, 'top', 0 ), ( text, 'left', 20),
                               ( textField, 'top', 0 )],
                         ac = [(textField, 'left', 0, text )])
        Win_Global.textField = textField
        return form





class UI_ColorIndex:
    
    def __init__(self):
        
        pass
    
    
    def create(self):
        
        form = cmds.formLayout()
        text = cmds.text( l='ColorIndex : ', w=100, al='left', h=25 )
        intField1 = cmds.intField(h=25, w=100, v=0 )
        intField2 = cmds.intField(h=25, w=100, v=0 )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af = [(text,'top',0), (text,'left',20),
                               (intField1,'top',0),(intField2,'top',0)],
                         ac = [(intField1, 'left', 0, text), (intField2, 'left', 0, intField1)] )
        
        Win_Global.intField1 = intField1
        Win_Global.intField2 = intField2
        
        return form





class UI_ControllerSize:
    
    def __init__(self):
        
        pass
    
    
    def create(self):
        
        form = cmds.formLayout()
        text = cmds.text( l='Controller Size : ', w=100, al='left', h=25 )
        floatField = cmds.floatField(h=25, w=100, v=1.0, pre=2 )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af = [(text,'top',0), (text,'left',20),
                               (floatField,'top',0)],
                         ac = [(floatField, 'left', 0, text)] )
        
        Win_Global.floatField = floatField
        
        return form
    





class UI_Buttons:
    
    def __init__(self):
        
        pass


    def create(self):
        
        form = cmds.formLayout()
        createButton = cmds.button( l='Create', h=25, c=Win_Cmd.create )
        closeButton  = cmds.button( l='Close', h=25,  c=Win_Cmd.close )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af = [( createButton, 'top', 0 ), ( createButton, 'left', 0 ), ( createButton, 'bottom', 0 ),
                               ( closeButton, 'top', 0 ), ( closeButton, 'right', 0 ), ( closeButton, 'bottom', 0 )],
                         ap = [ ( createButton, 'right', 0, 50 ), ( closeButton, 'left', 0, 50 ) ])
    
        return form




class Win:
    
    def __init__(self):
        
        self.ui_controllerName = UI_ControllerName()
        self.ui_colorIndex = UI_ColorIndex()
        self.ui_controllerSize = UI_ControllerSize()
        self.ui_buttons  = UI_Buttons()


    def create(self):
        
        if cmds.window( Win_Global.winName, q=1, ex=1 ):
            cmds.deleteUI( Win_Global.winName )
        cmds.window( Win_Global.winName, title=Win_Global.title )
        
        form  = cmds.formLayout()
        text   = cmds.text( l= "Select joint tops", al='center', h=30, bgc=[.5,.5,.5] )
        check = cmds.checkBox( l='Add Pin Control' )
        controllerName = self.ui_controllerName.create()
        colorIndex = self.ui_colorIndex.create()
        controllerSize = self.ui_controllerSize.create()
        button = self.ui_buttons.create()
        cmds.setParent( '..' )

        cmds.formLayout( form, e=1, af=[ (text, 'top', 0 ), (text, 'left', 0 ), (text, 'right', 0 ),
                                         (check, 'top', 5 ), (check, 'left', 10 ), (check, 'right', 0 ),
                                         (controllerName, 'left', 10 ), (controllerName, 'right', 5 ),
                                         (colorIndex, 'left', 10 ), (colorIndex, 'right', 5 ),
                                         (controllerSize, 'left', 10 ), (controllerSize, 'right', 5 ),
                                         (button, 'left', 0 ), (button, 'right', 0 ), (button, 'bottom', 0 )],
                                    ac=[ (check, 'top', 5, text),
                                         (controllerName, 'top', 5, check),
                                         (colorIndex, 'top', 5, controllerName), 
                                         (controllerSize, 'top', 5, colorIndex), 
                                         (button, 'top', 5, controllerSize) ] )
        
        cmds.window( Win_Global.winName, e=1,
                     width = Win_Global.width, height = Win_Global.height,
                     rtf=1 )
        cmds.showWindow( Win_Global.winName )
        
        Win_Global.checkBox = check

