import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
from sgModules import sgdata
import pymel.core
import math, copy
import os



def getIntPtr( intValue = 0 ):
    util = OpenMaya.MScriptUtil()
    util.createFromInt(intValue)
    return util.asIntPtr()




def getDoublePtr( doubleValue=0 ):
    util = OpenMaya.MScriptUtil()
    util.createFromDouble( doubleValue )
    return util.asDoublePtr()



def getDoubleFromDoublePtr( ptr ):
    return OpenMaya.MScriptUtil.getDouble( ptr )



def getInt2Ptr():
    util = OpenMaya.MScriptUtil()
    util.createFromList([0,0],2)
    return util.asInt2Ptr()




def getListFromInt2Ptr( ptr ):
    util = OpenMaya.MScriptUtil()
    v1 = util.getInt2ArrayItem( ptr, 0, 0 )
    v2 = util.getInt2ArrayItem( ptr, 0, 1 )
    return [v1, v2]




def getFloat2Ptr():
    util = OpenMaya.MScriptUtil()
    util.createFromList( [0,0], 2 )
    return util.asFloat2Ptr()




def getMObject( target ):
    mObject = OpenMaya.MObject()
    selList = OpenMaya.MSelectionList()
    selList.add( target )
    selList.getDependNode( 0, mObject )
    return mObject



def getDagPath( target ):
    dagPath = OpenMaya.MDagPath()
    selList = OpenMaya.MSelectionList()
    selList.add( target )
    try:
        selList.getDagPath( 0, dagPath )
        return dagPath
    except:
        return None



def getDirectionIndex( inputVector ):
    
    import math
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
    
    
    
def matrixToList( matrix ):
    mtxList = range( 16 )
    for i in range( 4 ):
        for j in range( 4 ):
            mtxList[ i * 4 + j ] = matrix( i, j )
    return mtxList



def listToMatrix( mtxList ):
    matrix = OpenMaya.MMatrix()
    OpenMaya.MScriptUtil.createMatrixFromList( mtxList, matrix  )
    return matrix





def rotateToMatrix( rotation ):
    
    import math
    rotX = math.radians( rotation[0] )
    rotY = math.radians( rotation[1] )
    rotZ = math.radians( rotation[2] )
    
    trMtx = OpenMaya.MTransformationMatrix()
    trMtx.rotateTo( OpenMaya.MEulerRotation( OpenMaya.MVector(rotX, rotY, rotZ) ) )
    return trMtx.asMatrix()





def setAttrDefault( sels, **options ):
    
    attrs = []
    targetIsKeyAttrs = False
    
    if options.has_key( 'attrs' ):
        attrs = options['attrs']
    if options.has_key( 'k' ):
        if options['k']:
            targetIsKeyAttrs = True
    
    for sel in sels:
        if targetIsKeyAttrs:
            keyAttrs = cmds.listAttr( sel, k=1 )
            for attr in keyAttrs:
                defaultValue = cmds.attributeQuery( attr, node=sel, ld=1 )
                try:cmds.setAttr( sel + '.' + attr, defaultValue[0] )
                except:pass
        for attr in attrs:
            defaultValue = cmds.attributeQuery( attr, node=sel, ld=1 )
            try:cmds.setAttr( sel + '.' + attr, defaultValue[0] )
            except:pass





def convertSideString( string ):
    
    import copy
    converted = copy.copy( string )
    if string.find( '_L_' ) != -1:
        converted = string.replace( '_L_', '_R_' )
    elif string.find( '_R_' ) != -1:
        converted = string.replace( '_R_', '_L_' )
    return converted




def getNameReplaceList( firstName, secondName ):
    
    splitsFirst = firstName.split( '_' )
    splitsSecond = secondName.split( '_' )
    
    diffIndices = []
    for i in range( len( splitsFirst ) ):
        if splitsFirst[i] != splitsSecond[i]:
            diffIndices.append(i)
    
    replaceStrsList = []
    for diffIndex in diffIndices:
        firstStr = splitsFirst[diffIndex]
        secondStr = splitsSecond[diffIndex]
        
        if diffIndex == 0:
            firstStr = firstStr + '_'
            secondStr = secondStr + '_'
        elif diffIndex == len( splitsFirst ) - 1:
            firstStr = '_' + firstStr
            secondStr = '_' + secondStr
        else:
            firstStr = '_' + firstStr + '_'
            secondStr = '_' + secondStr + '_'
        
        replaceStrsList.append( [firstStr, secondStr] )
    
    return replaceStrsList




def getOtherSideName( nodeName ):
    
    if nodeName.find( '_L_' ):
        return nodeName.replace( '_L_', '_R_' )
    elif nodeName.find( '_R_' ):
        return nodeName.replace( '_R_', '_L_' )
    return nodeName




def makeFolder( pathName ):
    
    pathName = pathName.replace( '\\', '/' )
    splitPaths = pathName.split( '/' )
    
    cuPath = splitPaths[0]
    
    folderExist = True
    for i in range( 1, len( splitPaths ) ):
        checkPath = cuPath+'/'+splitPaths[i]
        if not os.path.exists( checkPath ):
            os.chdir( cuPath )
            os.mkdir( splitPaths[i] )
            folderExist = False
        cuPath = checkPath
        
    if folderExist: return None
        
    return pathName


def makeFile( filePath ):
    if os.path.exists( filePath ): return None
    filePath = filePath.replace( "\\", "/" )
    splits = filePath.split( '/' )
    folder = '/'.join( splits[:-1] )
    makeFolder( folder )
    f = open( filePath, "w" )
    f.close()



def reloadModules( pythonPath='' ):

    import os, imp, sys
    
    if not pythonPath:
        pythonPath = __file__.split( '\\' )[0]
    
    for root, folders, names in os.walk( pythonPath ):
        root = root.replace( '\\', '/' )
        for name in names:
            try:onlyName, extension = name.split( '.' )
            except:continue
            if extension.lower() != 'py': continue
            
            if name == '__init__.py':
                fileName = root
            else:
                fileName = root + '/' + name
                
            moduleName = fileName.replace( pythonPath, '' ).split( '.' )[0].replace( '/', '.' )[1:]
            moduleEx =False
            try:
                sys.modules[moduleName]
                moduleEx = True
            except:
                pass
            
            if moduleEx:
                try:reload( sys.modules[moduleName] )
                except:pass






class SGPoint:
    
    def __init__(self, *args, **options ):
        
        self.x = 1
        self.y = 0
        self.z = 0
        self.w = 1
        
        if type( args ) in [list, tuple] and type( args[0] ) in [type(1), type(1.0)]:
            args = list(args)
            while len( args ) < 3:
                args.append( 0.0 )
            if len( args ) == 3:
                args.append( 1.0 )
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]
            self.w = args[3]
        elif isinstance( args[0], OpenMaya.MPoint ) or isinstance( args[0], SGPoint ):
            self.x = args[0].x
            self.y = args[0].y
            self.z = args[0].z
            self.w = args[0].w
        elif isinstance( args[0], OpenMaya.MVector ) or isinstance( args[0], SGVector ):
            self.x = args[0].x
            self.y = args[0].y
            self.z = args[0].z
            self.w = 1
        
    
    def getList(self):
        return [ self.x, self.y, self.z ]
    
    
    def __mul__(self, other ):
        other = SGVector( other )
        return self.x * other.x, self.y * other.y, self.z * other.z
            
        



class SGVector:
    
    def __init__(self, *args, **options ):
        
        self.x = 1
        self.y = 0
        self.z = 0
        
        if type( args ) in [list, tuple] and type( args[0] ) in [type(1), type(1.0)]:
            args = list(args)
            while len( args ) < 3:
                args.append( 0.0 )
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]
        elif isinstance( args[0], OpenMaya.MPoint ) or isinstance( args[0], SGPoint ) or isinstance( args[0], OpenMaya.MVector ) or isinstance( args[0], SGVector ):
            self.x = args[0].x
            self.y = args[0].y
            self.z = args[0].z
        
    
    def getList(self):
        return [ self.x, self.y, self.z ]
    
    
    def __mul__(self, other ):
        other = SGVector( other )
        return self.x * other.x, self.y * other.y, self.z * other.z
            




class SGMatrix:
    
    def __init__(self, *args, **options ):
        
        if type( args[0] ) in [type([]), type(())]:
            self.m = OpenMaya.MMatrix()
            OpenMaya.MScriptUtil.createMatrixFromList( args[0], self.m )
        elif type( args[0] ) == type(OpenMaya.MMatrix()):
            self.m = args[0]
        elif isinstance( args[0], SGMatrix ):
            self.m = args[0].m
        
    def getList(self):
        mtxList = range( 16 )
        for i in range( 4 ):
            for j in range( 4 ):
                mtxList[ i * 4 + j ] = self.m( i, j )
        return mtxList
    
    
    def __mul__(self, other ):
        return SGMatrix( self.m * SGMatrix( other ).m )
    
    
    def inverse(self):
        return SGMatrix( self.m.inverse() )
    
    
    def rotateInside(self, *rot ):
        
        trMtx = OpenMaya.MTransformationMatrix()
        trMtx.rotateTo( OpenMaya.MEulerRotation( math.radians( rot[0] ), math.radians( rot[1] ), math.radians( rot[2] ) ) )
        self.m = trMtx.asMatrix() * self.m


    def rotateOutside(self, *rot ):
        
        trMtx = OpenMaya.MTransformationMatrix()
        trMtx.rotateTo( OpenMaya.MEulerRotation( math.radians( rot[0] ), math.radians( rot[1] ), math.radians( rot[2] ) ) )
        self.m = self.m * trMtx.asMatrix()

    
    def translateInside(self, *tr ):
        
        trMtx = OpenMaya.MTransformationMatrix()
        trMtx.setTranslation( OpenMaya.MVector( *tr ) )
        self.m = trMtx.asMatrix() * self.m
    
    
    def translateOutside(self, *trs ):
        trMtx = OpenMaya.MTransformationMatrix()
        trMtx.setTranslation( OpenMaya.MVector( *trs ), OpenMaya.MSpace.kTransform )
        self.m = self.m * trMtx.asMatrix()
    
    
    def getTranslate(self):
        return SGPoint( self.m( 3, 0 ), self.m( 3,1 ), self.m( 3,2 ) )


    def getRotate(self):
        trMtx = OpenMaya.MTransformationMatrix( self.m )
        return SGVector( trMtx.eulerRotation().asVector() )
    
    
    def setRotate(self, *rot ):
        rotVector = SGVector( *rot )
        trMtx = OpenMaya.MTransformationMatrix(self.m)
        self.m = trMtx.rotateTo( OpenMaya.MEulerRotation( *rotVector.getList() ) ).asMatrix()


    def setTranslate(self, *inputTrans ):
        sgpoint = SGPoint( *inputTrans )
        trMtx = OpenMaya.MTransformationMatrix( self.m )
        trMtx.setTranslation( OpenMaya.MVector(*sgpoint.getList()), OpenMaya.MSpace.kTransform )
        self.m = trMtx.asMatrix()
        afTrans = self.getTranslate()
    




class SGObject( object ):
    
    def __eq__(self, other ):
        return self.name() == other.name()
    
    
    def __ne__(self, other ):
        return self.name() != other.name()
    
    
    def __add__(self, addStr ):
        return self.name() + addStr
    
    
    def split(self, splitTarget ):
        return self.name().split( splitTarget )
    
    
    def convertSg(self, nodeName ):
        if not type( nodeName ) in [str, unicode]: 
            return nodeName
        if nodeName.find( '.' ) != -1:
            return SGAttribute( nodeName )
        nodeType = cmds.nodeType( nodeName )
        if nodeType in sgdata.NodeType.shape:
            sgNode = SGDagNode( nodeName )
        elif nodeType in sgdata.NodeType.transform:
            sgNode = SGTransformNode( nodeName )
        else:
            sgNode = SGNode( nodeName )
        return sgNode
    
    
    def convertName(self, nodeName ):
        if isinstance( nodeName, SGNode ):
            return nodeName.name()
        return nodeName
    

    
    def listConnections( self, **options ):
    
        cons = cmds.listConnections( self.name(), **options )
        if not cons: return []
        
        sgcons = []
        for con in cons:
            sgcons.append( self.convertSg( con ) )
            
        return sgcons
    
    
    def duplicate(self, **options ):
        
        duObjs = cmds.duplicate( self.name(), **options )

        converted = []
        for duObj in duObjs:
            converted.append( self.convertSg( duObj ) )
        return converted


    def rename(self, *args, **options ):
        cmds.rename( self.name(), args[0], **options )
        return self
    
    
    def replace(self, src, dst ):
        return self.name().replace( src, dst )






class SGAttribute( SGObject ):
    
    def __init__(self, *args ):
        
        self._index = None
        if isinstance( args[0], SGAttribute ):
            self._sgnode = args[0]._sgnode
            self._attrName = args[0]._attrName
            self._index = args[0]._index
        elif isinstance( args[0], SGNode ):
            self._sgnode = args[0]
            self._attrName = args[1]
        elif type( args[0] ) in [str, unicode]:
            if args[0].find( '.' ) != -1:
                splits = args[0].split( '.' )
                self._sgnode = SGNode( splits[0] )
                self._attrName = '.'.join( splits[1:] )
            else:
                self._sgnode = SGNode( args[0] )
                self._attrName = args[1]

        if self._attrName[-1] == ']':
            splits = self._attrName.split( '[' )
            self._attrName = '['.join( splits[:-1] )
            self._index = int( splits[-1][:-1] )
            
            childAttrs = cmds.attributeQuery( self._attrName, node= self._sgnode.name(), lc=1 )

            if childAttrs:
                childAttrsSn = []
                for childAttr in childAttrs:
                    childAttrsSn.append( cmds.attributeQuery( childAttr, node= self._sgnode.name(), sn=1 ) )
                childAttrs += childAttrsSn
                
                for childAttr in childAttrs:
                    exec( "self.%s = SGAttribute( self.name()+'[%d].'+childAttr )" %( childAttr, self._index ) )
                    

    def set(self, *values, **options ):
        try:cmds.setAttr( self.name(), *values, **options )
        except:pass
        return self
        
    
    def setKeyable(self, keyValue=True):
        cmds.setAttr( self.name(), e=1, k=keyValue )
        return self


    def setChannelBox(self, attrName, channelBoxValue=True):
        cmds.setAttr( self.name(), e=1, cb=channelBoxValue )
        return self


    def get(self):
        return cmds.getAttr( self.name() )
    
    
    def name(self):
        return self._sgnode.name() + "." + self.attrName()


    def node(self):
        return self._sgnode


    def nodeName(self):
        return self._sgnode.name()


    def attrName(self):
        if self._index != None:
            return self._attrName + '[%d]' % self._index
        return self._attrName
    
    
    def listDefault(self):
        defaults = cmds.attributeQuery( self.attrName(), node= self.nodeName(), ld=1 )
        if not defaults: defaults = []
        return defaults
    
    
    def setToDefault(self):
        cmds.setAttr( self.name(), *self.listDefault() )
        return self
    
    
    def __getitem__(self, index ):
        if cmds.attributeQuery( self._attrName, node= self._sgnode.name(), m=1 ):
            attrInst = SGAttribute( self._sgnode, self._attrName + '[%d]' % index )
            childAttrs = cmds.attributeQuery( self._attrName, node= self._sgnode.name(), lc=1 )
            if childAttrs:
                childAttrsSn = []
                for childAttr in childAttrs:
                    childAttrsSn.append( cmds.attributeQuery( childAttr, node= self._sgnode.name(), sn=1 ) )
                childAttrs += childAttrsSn
                
                for childAttr in childAttrs:
                    exec( "attrInst.%s = SGAttribute( self.name()+'[%d].'+childAttr )" %( childAttr, index ) )
            return attrInst
        else:
            childAttrs = cmds.attributeQuery( self._attrName, node= self._sgnode.name(), lc=1 )
            return SGAttribute( self._sgnode, childAttrs[index] )
        

    def __rshift__( self, other ):
        if not cmds.isConnected( self.name(), other.name() ):
            cmds.connectAttr( self.name(), other.name(), f=1 )
    
    
    def __floordiv__(self, other ):
        if cmds.isConnected( self.name(), other.name() ):
            cmds.disconnectAttr( self.name(), other.name() )
    
    
    def getPlug(self):
        
        fnNode = OpenMaya.MFnDependencyNode( self._sgnode.mObject )
        splitAttrNames = self.attrName().split( '.' )
        
        attrNames = []
        indices   = []
        for splitAttrName in splitAttrNames:
            if splitAttrName.find( '[' ) != -1:
                attrName, otherName = splitAttrName.split( '[' )
                attrNames.append( attrName )
                indices.append( int( otherName.split( ']' )[0] ) )
            else:
                attrNames.append( splitAttrName )
                indices.append( None )
        
        firstAttrName = attrNames.pop(0)
        firstIndex   =  indices.pop(0)
        
        if firstIndex == None:
            return fnNode.findPlug( firstAttrName )
        
        firstPlug    = fnNode.findPlug( firstAttrName )
        element = firstPlug.elementByLogicalIndex( firstIndex )
        
        for i in range( len( attrNames ) ):
            attrName = attrNames[i]
            index    = indices[i]
            
            childIndex = 0
            for j in range( element.numChildren() ):
                if attrName == element.child(j).name().split( '.' )[-1]:
                    childIndex = j
            
            element = element.child( childIndex )
            if index != None:
                element = element.elementByLogicalIndex( index )
        
        return element




class SGNode( SGObject ):
    
    def __init__(self, nodeName ):
        
        if isinstance( nodeName, SGNode ):
            self.mObject = nodeName.mObject
            self.mDagPath = nodeName.mDagPath
        if type( nodeName ) in [ str, unicode ]:
            self.mObject  = getMObject( nodeName )
            self.mDagPath = getDagPath( nodeName )
        
        attrNames = []
        if self.nodeType() in sgdata.NodeType.dag:
            attrNames += sgdata.Attrs.dagAttrs
        if not attrNames:
            attrNames += cmds.listAttr( self.name() )
            shortNames = cmds.listAttr( self.name(), sn=1 )
            for shortName in shortNames:
                if not shortName in ['def','tg.try','try','global','ats.as','as','or', 'is', 'in', 'if']:
                    attrNames.append( shortName )

        for attrName in attrNames:
            exec( "self.%s = self.attr( attrName )" % attrName )


    def name(self):
        if self.mDagPath:
            fnDagNode = OpenMaya.MFnDagNode( self.mDagPath )
            return fnDagNode.partialPathName()
        else:
            fnNode = OpenMaya.MFnDependencyNode( self.mObject )
            return fnNode.name()
    
    
    def rename(self, inputName ):
        cmds.rename( self.name(), inputName )
        return self
    
    
    def apiType(self):
        return self.mObject.apiType()


    def apiTypeStr(self):
        return self.mObject.apiTypeStr()
    
    
    def nodeType(self):
        return cmds.nodeType( self.name() )
    
    
    def addAttr(self, *attrNames, **options ):
        
        defaultOptions = {}
        if len( attrNames ) > 2:
            defaultOptions.update( {'ln':attrNames[0]} )
            defaultOptions.update( {'sn':attrNames[1]} )
        elif len( attrNames ) == 1:
            defaultOptions.update( {'ln':attrNames[0]} )        
        options.update( defaultOptions )
        
        keys = options.keys()
        longName = None
        shortName = None
        if 'ln' in keys:
            longName = options['ln']
        elif 'longName' in keys:
            longName = options['longName']
        if 'sn' in keys:
            shortName = options['sn']
        elif 'shortName' in keys:
            shortName = options['shortName']
        
        attrExists = False
        if longName:
            if cmds.attributeQuery( longName, node= self.name(), ex=1 ):
                cmds.warning( "%s has already '%s'" %( self.name(), longName ))
                attrExists = True
        if shortName:
            if cmds.attributeQuery( shortName, node= self.name(), ex=1 ):
                cmds.warning( "%s has already '%s'" %( self.name(), shortName ))
                attrExists = True
        
        attrName = longName
        if shortName: attrName = shortName
        
        channelValue = None
        keyableValue = None
        for key, value in options.items():
            if key in ['cb', 'channelBox']:
                channelValue = value
                options.pop( key )
            elif key in ['k', 'keyable']:
                keyableValue = value 
                options.pop( key )
        
        if not attrExists:cmds.addAttr( self.name(), **options )
        if channelValue != None:
            cmds.setAttr( self.name()+'.'+attrName, e=1, cb=channelValue )
        if keyableValue != None:
            cmds.setAttr( self.name()+'.'+attrName, e=1, k=keyableValue )
        
        sgAttr = SGAttribute( self, attrName )
        if longName:
            exec( 'self.%s = sgAttr' % longName )
        if shortName:
            exec( 'self.%s = sgAttr' % shortName )
        
        return sgAttr
    
    
    def setAttr(self, attrName, *values, **options ):
        cmds.setAttr( self.name() + '.' + attrName, *values, **options )
        return self
        
    
    def setKeyable(self, attrName, keyValue=True):
        cmds.setAttr( self.name()+'.'+attrName, e=1, k=keyValue )
        return self


    def setChannelBox(self, attrName, channelBoxValue=True):
        cmds.setAttr( self.name()+'.'+attrName, e=1, cb=channelBoxValue )
        return self
    
    
    def getAttr(self, attrName ):
        return cmds.getAttr( self.name() + '.' + attrName )
        
        
    def attr(self, attrName ):
        return SGAttribute( self, attrName )
    
    
    def listAttr(self, **options ):
        attrs = cmds.listAttr( self.name(), **options )
        if not attrs: return []
        return attrs
    
    
    def vectorOutput(self):
        
        if self.nodeType() == "decomposeMatrix":
            return self.attr( 'ot' )
        if self.nodeType() == "vectorProduct":
            return self.attr( "output" )
        if self.nodeType() == "closestPointOnMesh":
            return self.attr( "normal" )
        if self.nodeType() == "plusMinusAverage":
            return self.attr( "output3D" )
    
    
    def matrixOutput(self):
        
        if self.nodeType() in ['composeMatrix', 'inverseMatrix']:
            return self.attr( 'outputMatrix' )
        elif self.nodeType() in ['multMatrix', 'wtAddMatrix']:
            return self.attr( 'matrixSum' )
        elif self.nodeType() in ['fourByFourMatrix']:
            return self.attr( 'output' )
    
    
    def scalarOutput(self):
        
        if self.nodeType() == 'distanceBetween':
            return self.attr( 'distance' )
    
    
    def attributeQuery(self, attrName, **options ):
        options.update( {'node':self.name()} )
        return cmds.attributeQuery( attrName, **options )




class SGDagNode( SGNode ):
    
    def __init__(self, nodeName ):
        SGNode.__init__(self, nodeName)


    def position(self, **options ):
        defaultOptions = {'q':1, 't':1 }
        defaultOptions.update( options )
        return OpenMaya.MPoint( *cmds.xform( self.name(), **defaultOptions ) )
    
    
    def localName(self):
        fnDagNode = OpenMaya.MFnDagNode( self.mDagPath )
        return fnDagNode.name()
    
    
    def fullPathName(self):
        fnDagNode = OpenMaya.MFnDagNode( self.mDagPath )
        return fnDagNode.fullPathName()
    
    
    def parent(self):
        parents = cmds.listRelatives( self.name(), p=1, f=1 )
        if not parents: return None
        return self.convertSg( parents[0] )
    
    
    def transform(self):
        if self.apiTypeStr() in sgdata.ApiType.transform:
            return SGTransformNode( self )
        return SGTransformNode( self.parent() )


    def shape(self):
        if self.apiTypeStr() in sgdata.ApiType.shape:
            return self
        children = cmds.listRelatives( self.name(), c=1, s=1, f=1 )
        if not children: return None
        for child in children:
            if cmds.getAttr( child + '.io' ): continue
            return SGDagNode( child )
        
        for child in children:
            return SGDagNode( child )


    def shapes(self):
        if self.apiTypeStr() in sgdata.ApiType.shape:
            return [self]
        children = cmds.listRelatives( self.name(), c=1, s=1, f=1 )
        if not children: return []
        dagNodes = []
        for child in children:
            dagNodes.append( SGDagNode( child ) )
        return dagNodes
    


    def getNodeFromHistory( self, historyType, **options ):
    
        hists = cmds.listHistory( self.name(), **options )
        
        if not hists: return []
        
        returnTargets = []
        for hist in hists:
            if cmds.nodeType( hist ) == historyType:
                node = None
                if cmds.nodeType( hist ) in sgdata.NodeType.dag:
                    node = SGDagNode( hist )
                else:
                    node = SGNode( hist )
                returnTargets.append( node )
        return returnTargets
        

    def listRelatives(self, **options ):
        
        options.update( {'f':1} )
        results = cmds.listRelatives( self.name(), **options )
        if not results: return []
        sgresults = []
        for result in results:
            if cmds.nodeType( result ) in sgdata.NodeType.shape:
                sgresults.append( SGDagNode( result ) )
            elif cmds.nodeType( result ) in sgdata.NodeType.transform:
                sgresults.append( SGTransformNode( result ) )
            else:
                sgresults.append( SGNode( result ) )
        return sgresults
    
    
    def inputGeometry(self):
        nodeType = self.nodeType()
        if nodeType == 'mesh':
            return self.attr( 'inMesh' )
        elif nodeType in ['nurbsCurve', 'nurbsSurface']:
            return self.attr( 'create' )
    
    
    
    def outputGeometry(self):
        
        nodeType = self.nodeType()
        if nodeType == 'mesh':
            return self.attr( 'outMesh' )
        elif nodeType in ['nurbsCurve', 'nurbsSurface']:
            return self.attr( 'local' )
        
        


class SGTransformNode( SGDagNode ):
    
    def __init__(self, nodeName ):
        SGDagNode.__init__(self, nodeName)
        
        if self.nodeType() == 'joint':
            self.jo = SGAttribute( self, 'jo' )
            self.jointOrient = self.jo
    
    
    def setOrient(self, *args, **options ):
        
        args = list( args )
        args.append( self.name() )
        cmds.rotate( *args, **options )
        return self


    def setPosition(self, *args, **options ):
        
        args = list( args )
        args.append( self.name() )
        cmds.move( *args, **options )
        return self
    
    
    def xform(self, *args, **options ):
        result = cmds.xform( self.name(), **options )
        if not result:
            return self
        return result
    
        
    def makeChild(self, addName='_child', *args, **options ):
        
        childNode = SGTransformNode( cmds.createNode( 'transform', n=self.localName() + addName ) )
        cmds.parent( childNode.name(), self.name() )[0]
        childNode.setTransformDefault()
        return childNode


    def setTransformDefault(self):
        self.t.set( 0,0,0 )
        self.r.set( 0,0,0 )
        self.s.set( 1,1,1 )
        self.sh.set( 0,0,0 )
        if self.nodeType() == 'joint':
            self.jo.set( 0,0,0)
        return self
    
    
    def parentTo(self, target ):
        cmds.parent( self.name(), self.convertName( target ) )[0]
        return self
    

    def getPivotMatrix( self ):
        mtxList = self.wm.get()
        mtx = listToMatrix( mtxList )
        piv = OpenMaya.MPoint( *self.attr( 'rotatePivot' ).get()[0] )
        wp = piv * mtx
        mtxList[ 12 ] = wp.x
        mtxList[ 13 ] = wp.y
        mtxList[ 14 ] = wp.z
        return SGMatrix( mtxList )


    def getWorldMatrix(self):
        return SGMatrix( self.wm.get() )
        


    def getMatrix(self):
        return SGMatrix( self.m.get() )






def convertArgs( args ):
    newArgs = []
    for arg in args:
        if type( arg ) in [str, unicode]:
            newArgs.append( arg )
        else:
            newArgs.append( arg.name() )
    return newArgs



def convertSg( nodeName ):
    if type( nodeName ) in [ list, tuple ]:
        returnList = []
        for nodeNameElement in nodeName:
            returnList.append( convertSg(nodeNameElement) )
        return returnList
    
    if not type( nodeName ) in [str, unicode]: 
        return nodeName
    if nodeName.find( '.' ) != -1:
        return SGAttribute( nodeName )
    nodeType = cmds.nodeType( nodeName )
    if nodeType in sgdata.NodeType.shape:
        sgNode = SGDagNode( nodeName )
    elif nodeType in sgdata.NodeType.transform:
        sgNode = SGTransformNode( nodeName )
    else:
        sgNode = SGNode( nodeName )
    return sgNode



def convertSg_dec(func):
    def wrapper(*args, **kwargs):
        sgs = []
        for arg in args:
            if type( arg ) in [ tuple, list ]:
                for i in arg:
                    sgs.append( convertSg( i ) )
            else:
                sgs.append( convertSg( arg ) )
        return func(*sgs, **kwargs)
    return wrapper



def convertName( node ):
    if not type( node ) in [str, unicode]:
        try:return node.name()
        except:pass
    return node


def convertName_dec(func):
    def wrapper(*args, **kwargs):
        sgs = []
        sgkwargs = {}
        for arg in args:
            if type( arg ) in [ tuple, list ]:
                for i in arg:
                    sgs.append( convertName( i ) )
            else:
                sgs.append( convertName( arg ) )
        for key, value in kwargs.items():
            sgkwargs.update( {'%s'%key: convertName( value ) }  )
            
        return func(*sgs, **sgkwargs)
    return wrapper




def listNodes( *args, **options ):
    
    nodes = cmds.ls( *args, **options )
    
    sgNodes = []
    for node in nodes:
        sgNodes.append( convertSg( node ) )
    
    return sgNodes



def listConnections( *args, **options ):
    
    newArgs = convertArgs( args )
    cons = cmds.listConnections( *newArgs, **options )
    if not cons: return []
    
    sgcons = []
    for con in cons:
        if con.find( '.' ) != -1:
            sgcons.append( SGAttribute( con ) )
        else:
            sgcons.append( SGNode( con ) )
    
    return sgcons



def createNode( *args, **options ):
    
    nodeName = cmds.createNode( *args, **options )
    return convertSg( nodeName )



def shadingNode( *args, **options ):
    
    nodeName = cmds.shadingNode( *args, **options )
    return convertSg( nodeName )



def select( *args, **options ):
    
    allList = []
    for arg in args:
        if type( arg ) in [ list, tuple ]:
            allList += list( arg )
        else:
            allList.append( arg )
    
    for i in range( len( allList ) ):
        allList[i] = convertName( allList[i] )

    cmds.select( *allList, **options )




def getConstrainMatrix( first, target ):
    
    first = convertSg( first )
    target = convertSg( target )
    
    mmFirstAttr = first.wm.listConnections( type='multMatrix', p=1 )
    mmSecondAttr = target.pim.listConnections( type="multMatrix", p=1 )
    
    mm = None
    if mmFirstAttr and mmSecondAttr:
        mmFirstAttr = mmFirstAttr[0]
        mmSecondAttr = mmSecondAttr[0]
        if mmFirstAttr.attrName() in ["matrixIn[0]","i[0]"] and mmSecondAttr.attrName() in ["matrixIn[1]","i[1]"]:
            if mmFirstAttr.nodeName() == mmSecondAttr.nodeName():
                node = mmFirstAttr.node()
                if not node.i[1].listConnections():
                    mm = node
    
    if not mm:
        mm = createNode( 'multMatrix' )
        first.wm >> mm.i[0]
        target.pim >> mm.i[1]
    
    return mm



@convertSg_dec
def constrain_point( first, target ):
    
    mm = getConstrainMatrix( first, target )
    dcmp = getDecomposeMatrix( mm )
    dcmp.ot >> target.t



@convertSg_dec
def constrain_rotate( first, target ):
    
    mm = getConstrainMatrix( first, target )
    dcmp = getDecomposeMatrix( mm )
    dcmp.outputRotate >> target.r




@convertSg_dec
def constrain_scale( first, target ):
    
    mm = getConstrainMatrix( first, target )
    dcmp = getDecomposeMatrix( mm )
    dcmp.os >> target.s




@convertSg_dec
def constrain_parent( first, target ):
    
    mm = getConstrainMatrix( first, target )
    dcmp = getDecomposeMatrix( mm )
    dcmp.ot >> target.t
    dcmp.outputRotate >> target.r



@convertSg_dec
def constrain_tangent( curve, upObject, target, **options ):
    
    curveShape = curve.shape()
    pointOnCurve = createNode( 'pointOnCurveInfo' )
    curveShape.attr( 'worldSpace' ) >> pointOnCurve.inputCurve
    nearNode = getNearPointOnCurve( target, curve )
    paramValue = nearNode.parameter.get()
    delete( nearNode )
    
    pointOnCurve.parameter.set( paramValue )
    
    vectorProduct = createNode( 'vectorProduct' ).setAttr( 'operation', 3 ).setAttr( 'input1', 0,1,0 )
    upObject.wm >> vectorProduct.matrix
    
    fbf = createNode( 'fourByFourMatrix' )
    pointOnCurve.tangentX >> fbf.in00
    pointOnCurve.tangentY >> fbf.in01
    pointOnCurve.tangentZ >> fbf.in02
    vectorProduct.outputX >> fbf.in10
    vectorProduct.outputY >> fbf.in11
    vectorProduct.outputZ >> fbf.in12
    mm = createNode( 'multMatrix' )
    fbf.output >> mm.i[0]
    target.pim >> mm.i[1]
    fbfDcmp = getDecomposeMatrix( mm )
    
    fbfDcmp.outputRotate >> target.r



@convertSg_dec
def constrain_onCurve( curve, upObject, target, **options ):
    
    curveShape = curve.shape()
    pointOnCurve = createNode( 'pointOnCurveInfo' )
    curveShape.attr( 'worldSpace' ) >> pointOnCurve.inputCurve
    nearNode = getNearPointOnCurve( target, curve )
    position = cmds.xform( target.name(), ws=1, q=1, t=1 )[:3]
    nearNode.inPosition.set( position )
    paramValue = nearNode.parameter.get()
    delete( nearNode )
    
    pointOnCurve.parameter.set( paramValue )
    
    vectorProduct = createNode( 'vectorProduct' ).setAttr( 'operation', 3 ).setAttr( 'input1', 0,1,0 )
    upObject.wm >> vectorProduct.matrix
    
    fbf = createNode( 'fourByFourMatrix' )
    pointOnCurve.tangentX >> fbf.in00
    pointOnCurve.tangentY >> fbf.in01
    pointOnCurve.tangentZ >> fbf.in02
    vectorProduct.outputX >> fbf.in10
    vectorProduct.outputY >> fbf.in11
    vectorProduct.outputZ >> fbf.in12
    pointOnCurve.positionX >> fbf.in30
    pointOnCurve.positionY >> fbf.in31
    pointOnCurve.positionZ >> fbf.in32
    mm = createNode( 'multMatrix' )
    fbf.output >> mm.i[0]
    target.pim >> mm.i[1]
    dcmp = createNode( 'decomposeMatrix' )
    mm.o >> dcmp.imat
    dcmp.outputRotate >> target.r
    dcmp.outputTranslate >> target.t
    
    




@convertSg_dec
def constrain_all( first, target ):
    
    mm = getConstrainMatrix( first, target )
    dcmp = getDecomposeMatrix( mm )
    dcmp.ot >> target.t
    dcmp.outputRotate >> target.r
    dcmp.os >> target.s
    dcmp.osh >> target.sh
    
    

@convertName_dec
def parent( *args, **options ):
    parentedTargets = cmds.parent( *args, **options )
    for target in parentedTargets:
        if cmds.nodeType( target ) == 'joint':
            freezeJoint( target )
    return convertSg( parentedTargets )



def xform( *args, **options ):
    sgnodeNames = []
    for arg in args:
        sgnodeNames.append( convertSg( arg ).name() )
    return cmds.xform( *sgnodeNames, **options )



def isConnected( *args, **options ):
    srcAttr = SGAttribute( args[0] )
    dstAttr = SGAttribute( args[1] )
    return cmds.isConnected( srcAttr.name(), dstAttr.name(), **options )


@convertSg_dec
def getOutputMatrixAttribute( node ):
    targetAttr = None
    if node.nodeType() == 'transform':
        targetAttr = node.worldMatrix
    elif node.nodeType() in ['multMatrix', 'wtAddMatrix', 'addMatrix']:
        targetAttr = node.matrixSum
    elif node.nodeType() in ['composeMatrix', 'transposeMatrix', 'inverseMatrix']:
        targetAttr = node.outputMatrix
    
    return targetAttr


@convertSg_dec
def getOutputVectorAttribute( node ):
    targetAttr = None
    if node.nodeType() in ["transform", "joint"]:
        targetAttr = node.translate
    elif node.nodeType() in ["decomposeMatrix"]:
        targetAttr = node.outputTranslate
    return targetAttr



@convertSg_dec
def createLocalMatrix( localTarget, parentTarget ):
    
    multMatrixNode = createNode( 'multMatrix' )
    
    localTarget.wm >> multMatrixNode.i[0]
    parentTarget.wim >> multMatrixNode.i[1]
    
    return multMatrixNode




@convertSg_dec
def getLocalMatrix( localTarget, parentTarget ):
    
    multMatrixNodes = localTarget.wm.listConnections( d=1, s=0, type='multMatrix' )
    for multMatrixNode in multMatrixNodes:
        firstAttr = multMatrixNode.i[0].listConnections( s=1, d=0, p=1 )
        secondAttr = multMatrixNode.i[1].listConnections( s=1, d=0, p=1 )
        thirdConnection = multMatrixNode.i[2].listConnections( s=1, d=0 )
        
        if not firstAttr or not secondAttr or thirdConnection: continue
        
        firstEqual = firstAttr[0].node() == localTarget and firstAttr[0].attrName() in ["wm", "worldMatrix"]
        secondEqual = secondAttr[0].node() == parentTarget and secondAttr[0].attrName() in ["wim", "worldInverseMatrix"]
        
        if firstEqual and secondEqual:
            select( multMatrixNode )
            return multMatrixNode
    
    return createLocalMatrix( localTarget, parentTarget )



@convertSg_dec
def getDecomposeMatrix( node ):
    
    if isinstance( node, SGDagNode ):
        outputMatrixAttr = node.worldMatrix
    else:
        outputMatrixAttr = node.matrixOutput()

    if outputMatrixAttr:
        destNodes = listConnections( outputMatrixAttr, s=0, d=1, type='decomposeMatrix' )
        if destNodes: return destNodes[0]
        decomposeMatrixNode = createNode( 'decomposeMatrix' )
        outputMatrixAttr >> decomposeMatrixNode.imat
        return decomposeMatrixNode



@convertSg_dec
def opptimizeConnection( node ):
    
    srcAttrs = listConnections( node, s=1, d=0, p=1 )
    dstAttrs = listConnections( node, s=0, d=1, p=1 )
    
    if len( srcAttrs ) != 1 or len( dstAttrs ) != 1: return None
    
    if not isConnected( srcAttrs[0], dstAttrs[0] ):
        try:
            srcAttrs[0] >> dstAttrs[0]
        except:
            pass



def getConstrainedObject( node, messageName = '' ):
    
    messageAttr = None
    if messageName:
        messageAttr = node.attr( messageName )
        if not messageAttr:
            messageAttr = node.addAttr( ln=messageName, at='message' )
    
    targetNode = None
    if messageAttr:
        connectedNodes = messageAttr.listConnections( s=0, d=1, type='transform' )
        if connectedNodes:
            targetNode = connectedNodes[0]



@convertSg_dec
def getDistance( node ):
    distNode = createNode( 'distanceBetween' )
    if node.nodeType() == "decomposeMatrix":
        node.outputTranslate >> distNode.point1
    elif node.nodeType() in ['composeMatrix', 'transposeMatrix', 'inverseMatrix','multMatrix', 'wtAddMatrix', 'addMatrix']:
        getOutputMatrixAttribute(node) >> distNode.matrix1
    return distNode




@convertSg_dec
def createLookAtMatrix( lookTarget, rotTarget ):
    
    mm = createNode( 'multMatrix' )
    compose = createNode( 'composeMatrix' )
    mm2 = createNode( 'multMatrix' )
    invMtx = createNode( 'inverseMatrix' )
    
    lookTarget.wm >> mm.i[0]
    rotTarget.t >> compose.it
    compose.outputMatrix >> mm2.i[0]
    rotTarget.pm >> mm2.i[1]
    mm2.matrixSum >> invMtx.inputMatrix
    invMtx.outputMatrix >> mm.i[1]
    return mm



@convertSg_dec
def getLookAtMatrix( lookTarget, rotTarget ):
    
    consLookTarget = lookTarget.wm.listConnections( type="multMatrix", p=1 )
    '''
    mm = None
    if consLookTarget:
        for i in range( len( consLookTarget ) ):
            conLookTarget = consLookTarget[i]
            if not conLookTarget.attrName() in ['i[0]','matrixIn[0]']: continue
            if not conLookTarget.node().i[1].listConnections( type="inverseMatrix" ):continue
            mm = conLookTarget.node()
            mmSrcs = getSourceList( mm )
            srcCons = []
            for mmSrc in mmSrcs:
                srcCons += mmSrc.listConnections( s=1, d=0 )
            for srcCon in srcCons:
                print srcCon.name(), rotTarget.name()'''

    return createLookAtMatrix( lookTarget, rotTarget )


@convertSg_dec
def getLookAtAngleNode( lookTarget, rotTarget, **options ):
    
    if options.has_key( 'direction' ) and options['direction']:
        direction = options['direction']
    else:
        direction = [1,0,0]
    
    lookTarget = convertSg( lookTarget )
    rotTarget = convertSg( rotTarget )
    
    dcmpLookAt = getDecomposeMatrix( getLookAtMatrix( lookTarget, rotTarget ) )
    
    abnodes = dcmpLookAt.ot.listConnections( type='angleBetween' )
    if not abnodes:
        node = createNode( 'angleBetween' ).setAttr( "v1", *direction )
        dcmpLookAt.ot >> node.v2
    else:
        node = abnodes[0]
    return node


@convertSg_dec
def lookAtConnect( lookTarget, rotTarget, **options ):
    
    if options.has_key( 'direction' ) and options['direction']:
        direction = options['direction']
    else:
        direction = None
    
    if not direction:
        pRotTarget = rotTarget.parent()
        wim = listToMatrix( pRotTarget.wim.get() )
        pos = OpenMaya.MPoint( *lookTarget.xform( q=1, ws=1, t=1 ) )
        directionIndex = getDirectionIndex( pos*wim )
        direction = [[1,0,0], [0,1,0], [0,0,1],[-1,0,0], [0,-1,0], [0,0,-1]][directionIndex]
    
    node = getLookAtAngleNode( lookTarget, rotTarget, direction=direction )
    node.euler >> rotTarget.r




@convertSg_dec
def makeChild( target ):
    trNode = createNode( 'transform' )
    parent( trNode, target )
    trNode.setTransformDefault()
    return trNode



@convertSg_dec
def makeLookAtChild( lookTarget, pRotTarget, **options ):
    rotTarget = makeChild( pRotTarget )
    if options.has_key( 'n' ):
        rotTarget.rename( options['n'] )
    elif options.has_key( 'name' ):
        rotTarget.rename( options['name'] )
    lookAtConnect( lookTarget, rotTarget, **options )
    return rotTarget




@convertSg_dec
def createBlendTwoMatrixNode( first, second, **options ):
    
    wtAddMtx = createNode( 'wtAddMatrix' )
    wtAddMtx.addAttr( ln='blend', min=0, max=1, dv=0.5, k=1 )
    
    revNode  = createNode( 'reverse' )
    
    local = False
    if options.has_key('local') and options['local']:
        local = True
    
    if first.nodeType() == 'multMatrix':
        firstAttr = first.matrixSum
    else:
        if local:
            firstAttr = first.m
        else:
            firstAttr = first.wm
        
    if second.nodeType() == 'multMatrix':
        secondAttr = second.matrixSum
    else:
        if local:
            secondAttr = second.m
        else:
            secondAttr = second.wm

    firstAttr >> wtAddMtx.i[0].m
    secondAttr >> wtAddMtx.i[1].m
    
    wtAddMtx.blend >> revNode.inputX
    revNode.outputX >> wtAddMtx.i[0].w
    wtAddMtx.blend >> wtAddMtx.i[1].w
    
    return wtAddMtx


@convertSg_dec
def getBlendTwoMatrixNode( first, second, **options ):

    local = False
    if options.has_key('local') and options['local']:
        local = True
    
    if first.nodeType() == 'multMatrix':
        firstAttr = first.matrixSum
    else:
        if local:
            firstAttr = first.m
        else:
            firstAttr = first.wm
    
    firstConnected = firstAttr.listConnections( type='wtAddMatrix', p=1 )
    
    if firstConnected:
        cons = firstConnected[0].node().i[1].m.listConnections( s=1, d=0 )
        if cons and cons[0] == second:
            select( firstConnected[0].node() )
            return firstConnected[0].node()

    wtAddMtx = createBlendTwoMatrixNode( first, second, **options )
    select( wtAddMtx )
    return wtAddMtx




@convertSg_dec
def blendTwoMatrix( first, second, target, **options ):
    
    connectBlendTwoMatrix(first, second, target, **options)




@convertSg_dec
def connectBlendTwoMatrix( first, second, target, **options ):

    blendNode = createBlendTwoMatrixNode( first, second )
    mm = createNode( 'multMatrix' )
    blendNode.matrixOutput() >> mm.i[0]
    target.pim >> mm.i[1]
    dcmp = getDecomposeMatrix( mm )
    
    trConnect = False
    roConnect = False
    scaleConnect = False
    
    if options.has_key( 'ct' ):
        trConnect = options['ct']
    if options.has_key( 'cr' ):
        roConnect = options['cr']
    if options.has_key( 'cs' ):
        scaleConnect = options['cs']
    
    if trConnect: dcmp.ot >> target.t
    if roConnect: dcmp.outputRotate >> target.r
    if scaleConnect: dcmp.outputScale >> target.s
    
    target.addAttr( ln='blend', min=0, max=1, k=1, dv=0.5 )
    target.blend >> blendNode.blend



@convertSg_dec
def createBlendMatrix( *args, **options ):
    
    constObjs = args[:-1]
    target = args[-1]
    
    isLocal = False
    if options.has_key( 'local' ):
        isLocal = options['local']
    
    wtAddMtx = createNode( 'wtAddMatrix' )
    plusNode = createNode( 'plusMinusAverage' )
    if isLocal :
        outDcmp = getDecomposeMatrix( wtAddMtx )
    else:
        outMM    = createNode( 'multMatrix' )
        wtAddMtx.o >> outMM.i[0]
        target.pim >> outMM.i[1]
        outDcmp = getDecomposeMatrix( outMM )
    
    for i in range( len(constObjs) ):
        constObj = constObjs[i]
        if options.has_key('mo') and options['mo']:
            constChild = constObj.makeChild('_Offset')
            constChild.xform( ws=1, matrix= target.wm.get() )
            constMatrixAttr = constChild.wm
        elif isLocal:
            constMatrixAttr = constObj.m
        else:
            constMatrixAttr = constObj.wm
        
        divNode = createNode( 'multiplyDivide' )
        divNode.op.set( 2 )
        
        target.addAttr( ln='constWeight_%d' % i, k=1, dv=1 )
        target.attr( 'constWeight_%d' % i ) >> plusNode.attr( 'input1D[%d]' % i )
        target.attr( 'constWeight_%d' % i ) >> divNode.attr( 'input1X' )
        plusNode.attr( 'output1D' ) >> divNode.input2X
        
        constMatrixAttr >> wtAddMtx.attr( 'i[%d].m' % i )
        divNode.outputX >> wtAddMtx.attr( 'i[%d].w' % i )
    
    outDcmp.ot >> target.t
    outDcmp.outputRotate >> target.r



@convertSg_dec
def addBlendMatrix( *args, **options ):
    
    constObjs = args[:-1]
    target = args[-1]
    
    wtAddMtx = target.getNodeFromHistory( 'wtAddMatrix' )
    averages = target.getNodeFromHistory( 'plusMinusAverage' )
    
    if not wtAddMtx:
        createBlendMatrix( *args, **options )
        return 0
    
    multNodes = wtAddMtx[0].listConnections( s=1, type='multiplyDivide' )
    length = len( multNodes )
    
    for i in range( len( constObjs ) ):
        cuNumber = length + i
        target.addAttr( ln='constWeight_%d' % cuNumber, k=1 )
        
        divNode = createNode( 'multiplyDivide' ).setAttr( 'op', 2 )
        
        target.attr( 'constWeight_%d' % cuNumber ) >> averages[0].input1D[cuNumber]
        target.attr( 'constWeight_%d' % cuNumber ) >> divNode.input1X
        averages[0].output1D >> divNode.input2X
        
        if options.has_key( 'mo' ) and options['mo']:
            constChild = constObjs[i].makeChild('_Offset')
            constChild.xform( ws=1, matrix= target.wm.get() )
            constAttr = constChild.wm
        else:
            constAttr = constObjs[i].wm
            
        constAttr >> wtAddMtx[0].i[cuNumber].m
        divNode.outputX >> wtAddMtx[0].i[cuNumber].w
    
    return length


def getAngle( node, axis=[1,0,0] ):
    
    node = convertSg( node )
    
    outputAttr = node.vectorOutput()
    connectedAttrs = outputAttr.listConnections( s=0, d=1, p=1, type='angleBetween' )
    
    conectedindex = None
    for i in range( len( connectedAttrs ) ):
        value = connectedAttrs[i].node().attr( 'vector1' ).get()[0]
        if OpenMaya.MVector(*axis) * OpenMaya.MVector( *value ) > 0.999:
            conectedindex = i
            break
    
    if conectedindex == None:
        angleNode = createNode("angleBetween")
        angleNode.vector1.set( *axis )
        outputAttr >> angleNode.vector2
        return angleNode
    else:
        targetNode = connectedAttrs[conectedindex].node()
        select( targetNode )
        return targetNode



@convertSg_dec
def getFbfMatrix( *args ):
    
    xNode = args[0]
    yNode = args[1]
    zNode = args[2]
    
    if isinstance( xNode, SGAttribute ):
        xAttr = xNode
    else:
        xAttr = xNode.vectorOutput()
    
    if isinstance( yNode, SGAttribute ):
        yAttr = yNode
    else:
        yAttr = yNode.vectorOutput()
    
    if isinstance( zNode, SGAttribute ):
        zAttr = zNode
    else:
        zAttr = zNode.vectorOutput()
    
    fbfMtx = createNode( 'fourByFourMatrix' )
    xAttr[0] >> fbfMtx.attr('in00')
    xAttr[1] >> fbfMtx.attr('in01')
    xAttr[2] >> fbfMtx.attr('in02')
    yAttr[0] >> fbfMtx.attr('in10')
    yAttr[1] >> fbfMtx.attr('in11')
    yAttr[2] >> fbfMtx.attr('in12')
    zAttr[0] >> fbfMtx.attr('in20')
    zAttr[1] >> fbfMtx.attr('in21')
    zAttr[2] >> fbfMtx.attr('in22')
    
    return fbfMtx



@convertSg_dec
def getCrossVectorNode( *args ):
    
    first = args[0]
    second = args[1]
    
    if isinstance( first, SGAttribute ):
        firstAttr = first
    else:
        firstAttr = first.vectorOutput()
    
    if isinstance( second, SGAttribute ):
        secondAttr = second
    else:
        secondAttr = second.vectorOutput()
    
    crossVector = createNode( 'vectorProduct' )
    crossVector.attr( 'op' ).set( 2 )
    
    firstAttr  >> crossVector.attr( 'input1' )
    secondAttr >> crossVector.attr( 'input2' )
    
    return crossVector



@convertSg_dec
def replaceConnection( *args ):
    
    first = args[0] 
    second = args[1] 
    target = args[2]
    
    cons = target.listConnections( s=1, d=0, p=1, c=1 )
    for i in range( 0, len(cons), 2 ):
        con = cons[i+1]
        dest = cons[i]
        
        splits = con.split( '.' )
        node = splits[0]
        attr = '.'.join( splits[1:] )
        
        if con.node() != first: continue 
        cmds.connectAttr( second + '.' + attr, dest.name(), f=1 )



@convertSg_dec
def freezeJoint( joint ):
    
    import math
    mat = listToMatrix( cmds.getAttr( joint + '.m' ) )
    rot = OpenMaya.MTransformationMatrix( mat ).eulerRotation().asVector()
    joint.attr( 'jo' ).set( math.degrees( rot.x ), math.degrees( rot.y ), math.degrees( rot.z ) )
    joint.attr( 'r' ).set( 0,0,0 )
    


@convertSg_dec
def freezeByParent( target ):

    pTarget = target.listRelatives( p=1 )[0]
    xform( pTarget, ws=1, matrix = cmds.getAttr( target + '.wm' ) )
    target.setTransformDefault()
    



@convertSg_dec
def setCenter( sel ):
    
    import math
    import copy
    
    matList = sel.wm.get()
    mat = listToMatrix(matList)
    
    maxXIndex = 0
    maxXValue = 0
    
    minXIndex = 1
    minXValue = 100000000.0
    
    for i in range( 3 ):
        v = OpenMaya.MVector( mat[i] )
        if math.fabs( v.x ) > maxXValue:
            maxXValue = math.fabs( v.x )
            maxXIndex = i
        if math.fabs( v.x ) < minXValue:
            minXValue = math.fabs( v.x )
            minXIndex = i
    
    minVector = OpenMaya.MVector( mat[minXIndex] )
    maxVector = OpenMaya.MVector( mat[maxXIndex] )
    
    maxVector.y = 0
    maxVector.z = 0
    minVector.x = 0
    
    maxVector.normalize()
    minVector.normalize()
    otherVector = maxVector ^ minVector
    
    if (maxXIndex + 1) % 3 != minXIndex:
        otherVector *= -1
    
    allIndices = [0,1,2]
    allIndices.remove( minXIndex )
    allIndices.remove( maxXIndex )
    
    otherIndex = allIndices[0]
    
    newMatList = copy.copy( matList )
    
    newMatList[ minXIndex * 4 + 0 ] = minVector.x
    newMatList[ minXIndex * 4 + 1 ] = minVector.y
    newMatList[ minXIndex * 4 + 2 ] = minVector.z
    
    newMatList[ maxXIndex * 4 + 0 ] = maxVector.x
    newMatList[ maxXIndex * 4 + 1 ] = maxVector.y
    newMatList[ maxXIndex * 4 + 2 ] = maxVector.z
    
    newMatList[ otherIndex * 4 + 0 ] = otherVector.x
    newMatList[ otherIndex * 4 + 1 ] = otherVector.y
    newMatList[ otherIndex * 4 + 2 ] = otherVector.z
    
    newMatList[3*4] = 0
    
    newMat = listToMatrix( newMatList )
    
    trMat = OpenMaya.MTransformationMatrix( newMat )
    trans = trMat.getTranslation( OpenMaya.MSpace.kWorld )
    rot   = trMat.eulerRotation().asVector()
    
    sel.setPosition( trans.x, trans.y, trans.z, ws=1 )
    sel.setOrient( math.degrees(rot.x), math.degrees(rot.y), math.degrees(rot.z), ws=1 )



@convertSg_dec
def setMirror( sel ):

    matList = sel.wm.get()
    matList[1]  *= -1
    matList[2]  *= -1
    matList[4]  *= -1
    matList[8]  *= -1
    matList[12] *= -1
    sel.xform( ws=1, matrix= matList )
    



@convertSg_dec
def setMirrorLocal( sel ):

    matList = sel.m.get()
    matList[1]  *= -1
    matList[2]  *= -1
    matList[4]  *= -1
    matList[8]  *= -1
    matList[12] *= -1
    mtx = listToMatrix( matList )
    trMtx = OpenMaya.MTransformationMatrix( mtx )
    rotValue = trMtx.eulerRotation().asVector()
    rotList = [math.degrees(rotValue.x), math.degrees(rotValue.y), math.degrees(rotValue.z)]
    sel.xform( os=1, ro=rotList )
    sel.tx.set( -sel.tx.get() )





@convertSg_dec
def setCenterMirrorLocal( sel ):

    matList = sel.m.get()
    matList[1]  *= 0
    matList[2]  *= 0
    matList[4]  *= 0
    matList[8]  *= 0
    matList[12] *= 0
    
    xVector = OpenMaya.MVector( matList[0], matList[1], matList[2] )
    yVector = OpenMaya.MVector( matList[4], matList[5], matList[6] )
    xVector.normalize()
    yVector.normalize()
    zVector = xVector ^ yVector
    
    matList[0] = xVector.x; matList[1] = xVector.y; matList[2] = xVector.z
    matList[4] = yVector.x; matList[5] = yVector.y; matList[6] = yVector.z
    matList[8] = zVector.x; matList[9] = zVector.y; matList[10] = zVector.z
    
    mtx = listToMatrix( matList )
    trMtx = OpenMaya.MTransformationMatrix( mtx )
    rotValue = trMtx.eulerRotation().asVector()
    rotList = [math.degrees(rotValue.x), math.degrees(rotValue.y), math.degrees(rotValue.z)]
    
    sel.tx.set( 0 )
    sel.xform( os=1, ro=rotList )





@convertSg_dec
def lookAt( aimTarget, rotTarget, baseDir=None, **options ):
    
    rotWorldMatrix = listToMatrix( rotTarget.wm.get() )
    aimWorldMatrix = listToMatrix( aimTarget.wm.get() )
    localAimTarget = aimWorldMatrix * rotWorldMatrix.inverse()
    localAimPos    = OpenMaya.MPoint( localAimTarget[3] )
    direction = OpenMaya.MVector( localAimPos ).normal()
    
    directionIndex = getDirectionIndex( direction )
    
    if not baseDir:
        baseDir = [[1,0,0], [0,1,0], [0,0,1], [-1,0,0], [0,-1,0], [0,0,-1]][directionIndex]
    
    baseDir = OpenMaya.MVector( *baseDir )
    direction = OpenMaya.MVector( *direction )
    localAngle = baseDir.rotateTo( direction ).asMatrix()
    
    rotResultMatrix = localAngle * rotWorldMatrix
    trRotMatrix = OpenMaya.MTransformationMatrix( rotResultMatrix )
    rotVector = trRotMatrix.eulerRotation().asVector()
    
    options.update( {'ws':1} )
    rotTarget.setOrient( math.degrees( rotVector.x ), math.degrees( rotVector.y ), math.degrees( rotVector.z ), **options )
    

@convertSg_dec
def insertMatrix( target, multMatrixNode ):

    cons = multMatrixNode.listConnections( s=1, d=0, p=1, c=1 )    
    srcAttrs = []
    dstLists = []
    for i in range( 0, len( cons ), 2 ):
        nodeName = cons[i].node().name()
        attrName = cons[i]._attrName
        index    = cons[i]._index
        
        srcAttrs.append( cons[i+1] )
        dstLists.append( [nodeName, attrName, index] )
        
        cons[i+1] // cons[i]
    
    target.matrixOutput() >> multMatrixNode.i[0]
    for i in range( len( srcAttrs ) ):
        srcAttrs[i] >> SGAttribute( dstLists[i][0], dstLists[i][1] + '[%d]' % (dstLists[i][2]+1) )
        

@convertSg_dec
def getSourceConnection( *args ):
    
    targets = args[:-1]
    src = args[-1]
    
    cons = src.listConnections( s=1, d=0, c=1, p=1 )

    srcAttrs = []
    connectedAttrs = []
    
    for i in range( 0, len( cons ), 2 ):
        srcAttrs.append( cons[i+1] )
        connectedAttrs.append( cons[i].attrName() )
    
    for target in targets:
        for i in range( len( connectedAttrs ) ):
            try:
                srcAttrs[i] >> target.attr( connectedAttrs[i] )
            except:
                pass
            


def getAnimCurveValueAtFloatInput( animCurveNode, inputFloat ):
    
    animCurveNode = convertName( animCurveNode )
    
    import maya.OpenMayaAnim as OpenMayaAnim
    
    oAnimCurve = getMObject( animCurveNode )
    fnAnim = OpenMayaAnim.MFnAnimCurve( oAnimCurve )
    doublePtr2 = getDoublePtr()
    fnAnim.evaluate( inputFloat, doublePtr2 )
    
    return getDoubleFromDoublePtr( doublePtr2 )




def getSourceList( node, nodeList = [] ):
    
    node = convertSg( node )
    if node in nodeList: return []
    
    nodeList.append( node )
    if node.nodeType() in sgdata.NodeType.transform:
        cons = []
        attrs = ['t', 'r', 's']
        attrs += cmds.listAttr( node.name(), k=1 )
        for attr in attrs:
            cons += node.attr( attr ).listConnections( s=1, d=0, p=1, c=1 )
    else:
        cons = node.listConnections( s=1, d=0, p=1, c=1 )

    srcs = cons[1::2]
    
    returnList = [node]
    for i in range( len( srcs ) ):
        results = getSourceList( srcs[i].node(), nodeList )
        if not results: continue
        returnList += results
    return returnList



@convertSg_dec
def copyChildren( source, target ):
    first = source
    firstName = source.localName()
    secondName = target.localName()
    
    replaceStrsList = getNameReplaceList(firstName, secondName)
    
    firstChildren = first.listRelatives( c=1, ad=1, type='transform' )
    firstChildren.reverse()
    
    for firstChild in firstChildren:
        childName = firstChild.localName()
        for replaceSrc, replaceDst in replaceStrsList:
            childName = childName.replace( replaceSrc, replaceDst )
        parentName = firstChild.parent().localName()
        for replaceSrc, replaceDst in replaceStrsList:
            parentName = parentName.replace( replaceSrc, replaceDst )
        if not cmds.objExists( parentName ): continue
        exists = False
        if not cmds.objExists( childName ):
            secondChild = createNode( firstChild.nodeType() ).rename( childName )
        else:
            secondChild = SGTransformNode( childName )
            exists = True
        try:
            parent( secondChild, parentName )
        except: pass
        if not exists: 
            secondChild.xform( os=1, matrix= firstChild.m.get() )
            secondChild.attr( 'dh' ).set( firstChild.attr( 'dh' ).get() )
            if secondChild.nodeType() == 'joint':
                secondChild.attr( 'radius' ).set( firstChild.attr( 'radius' ).get() )


@convertSg_dec
def copyRig( source, target ):
    
    sourceName = source.localName()
    targetName = target.localName()
    
    replaceStrList = getNameReplaceList(sourceName, targetName)
    
    copyChildren( source, target )

    sourceChildren = source.listRelatives( c=1, ad=1, type='transform' )
    sourceChildren.append( source )
    
    def getReplacedNode( source, replaceStrList ):
        sourceName = source.name()
        for srcStr, dstStr in replaceStrList:
            sourceName = sourceName.replace( srcStr, dstStr )
        if sourceName == source.name():
            sourceName = source.name() + '_rigCopyed'
        else:
            if cmds.objExists( sourceName ):
                return convertSg( sourceName )
        if cmds.objExists( sourceName ): 
            return convertSg( sourceName )
        
        if source.nodeType() in sgdata.NodeType.transform:
            return None
        try:
            srcCons = source.listConnections( s=1, d=0, p=1, c=1 )
            dstCons = source.listConnections( s=0, d=1, p=1, c=1 )
            for i in range( 0, len( srcCons ), 2 ):
                srcCons[i+1] // srcCons[i]
            for i in range( 0, len( dstCons ), 2 ):
                dstCons[i] // dstCons[i+1]
            duObjs = source.duplicate( n=sourceName )
            for i in range( 0, len( srcCons ), 2 ):
                srcCons[i+1] >> srcCons[i]
            for i in range( 0, len( dstCons ), 2 ):
                dstCons[i] >> dstCons[i+1]
            return duObjs[0]
        except:
            return None
    
    for i in range( len( sourceChildren ) ):
        sourceNodes = getSourceList( sourceChildren[i], [] )
        if not sourceNodes: continue
        for sourceNode in sourceNodes:
            replacedSourceNode = getReplacedNode( sourceNode, replaceStrList )
            if not replacedSourceNode: continue
            
            srcCons = sourceNode.listConnections( s=1, d=0, p=1, c=1 )
            dstCons = sourceNode.listConnections( s=0, d=1, p=1, c=1 )
            dstCons.reverse()
            
            for cons in [ srcCons, dstCons ]:
                for i in range( 0, len( cons ), 2 ):
                    dest  = cons[i]
                    start = cons[i+1]
                    
                    destNode = dest.node()
                    startNode = start.node()
                    destAttrName = dest.attrName()
                    startAttrName = start.attrName()
                    
                    replacedDestNode = getReplacedNode( destNode, replaceStrList )
                    replacedStartNode = getReplacedNode( startNode, replaceStrList )
                    
                    if not replacedDestNode or not replacedStartNode: continue
                    
                    replacedStartNode.attr( startAttrName ) >> replacedDestNode.attr( destAttrName )
    
    duNodes = cmds.ls( '*_rigCopyed' )
    for duNode in duNodes:
        cmds.rename( duNode, duNode.replace( '_rigCopyed', '' ) )

    
    
def setAngleReverse( rigedNode ):
    srcList = getSourceList( rigedNode, [] )
    for src in srcList:
        if src.nodeType() == 'angleBetween':
            vector1Value = src.vector1.get()[0]
            src.vector1.set( -vector1Value[0],-vector1Value[1],-vector1Value[2])


def getSelectedVertices( targetObj=None ):
    
    cmds.select( targetObj )
    selList = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList(selList)
    
    returnTargets = []
    for i in range( selList.length() ):
        dagPath    = OpenMaya.MDagPath()
        oComponent = OpenMaya.MObject()
        
        selList.getDagPath( i, dagPath, oComponent )
        
        if dagPath.node().apiTypeStr() != 'kMesh': continue 
        
        fnMesh = OpenMaya.MFnMesh( dagPath )
        targetVertices = OpenMaya.MIntArray()
        if oComponent.isNull(): continue
        
        singleComp = OpenMaya.MFnSingleIndexedComponent( oComponent )
        elements = OpenMaya.MIntArray()
        singleComp.getElements( elements )
            
        
        if singleComp.componentType() == OpenMaya.MFn.kMeshVertComponent :
            for j in range( elements.length() ):
                targetVertices.append( elements[j] )
        elif singleComp.componentType() == OpenMaya.MFn.kMeshEdgeComponent:
            for j in range( elements.length() ):
                vtxList = getInt2Ptr()
                fnMesh.getEdgeVertices( elements[j], vtxList )
                values = getListFromInt2Ptr(vtxList)
                targetVertices.append( values[0] )
                targetVertices.append( values[1] )
        elif singleComp.componentType() == OpenMaya.MFn.kMeshPolygonComponent:
            for j in range( elements.length() ):
                intArr = OpenMaya.MIntArray()
                fnMesh.getPolygonVertices( elements[j], intArr )
                for k in range( intArr.length() ):
                    targetVertices.append( intArr[k] )
        
        if targetVertices.length():
            returnTargets.append( [dagPath, targetVertices] )
    
    return returnTargets



def getCenter( sels ):
    if not sels: return None
    
    bb = OpenMaya.MBoundingBox()
    
    selVerticesList = getSelectedVertices(sels)
    
    if selVerticesList:
        for selVertices in selVerticesList:
            dagPath, vtxIds = selVertices
            fnMesh = OpenMaya.MFnMesh( dagPath )
            points = OpenMaya.MPointArray()
            fnMesh.getPoints( points, OpenMaya.MSpace.kWorld )
            for i in range( vtxIds.length() ):
                bb.expand( points[vtxIds[i]] )
    else:
        for sel in sels:
            pos = OpenMaya.MPoint( *cmds.xform( sel, q=1, ws=1, t=1 ) )
            bb.expand( pos )
    
    return bb.center()




def putObject( putTargets, typ='joint', putType='boundingBoxCenter' ):
    
    for i in range( len( putTargets )):
        putTargets[i] = convertName( putTargets[i] )
    
    if putType == 'boundingBoxCenter':
        center = getCenter( putTargets )

        if typ == 'locator':
            putTarget = cmds.spaceLocator()[0]
        elif typ == 'null':
            putTarget = cmds.createNode( 'transform' )
            cmds.setAttr( putTarget + '.dh', 1 )
        else:
            putTarget = cmds.createNode( typ )
    
        cmds.move( center.x, center.y, center.z, putTarget, ws=1 )    
        
        if len( putTargets ) == 1:
            rot = cmds.xform( putTargets[0], q=1, ws=1, ro=1 )
            cmds.rotate( rot[0], rot[1], rot[2], putTarget, ws=1 )
        
        return convertSg( putTarget )
    
    else:
        newObjects = []
        for putTarget in putTargets:
            mtx = cmds.getAttr( putTarget + '.wm' )
            if typ == 'locator':
                newObject = cmds.spaceLocator()[0]
            elif typ == 'null':
                newObject = cmds.createNode( 'transform' )
                cmds.setAttr( putTarget + '.dh', 1 )
            else:
                newObject = cmds.createNode( typ )
            cmds.xform( newObject, ws=1, matrix=mtx )
            newObjects.append( convertSg(newObject) )
        return newObjects



@convertName_dec
def copyShapeToTransform( shape, target ):
    
    oTarget = getMObject( target )
    if cmds.nodeType( shape ) == 'mesh':
        oMesh = getMObject( shape )
        fnMesh = OpenMaya.MFnMesh( oMesh )
        fnMesh.copy( oMesh, oTarget )
    elif cmds.nodeType( shape ) == 'nurbsCurve':
        oCurve = getMObject( shape )
        fnCurve = OpenMaya.MFnNurbsCurve( oCurve )
        fnCurve.copy( oCurve, oTarget )
    elif cmds.nodeType( shape ) == 'nurbsSurface':
        oSurface = getMObject( shape )
        fnSurface = OpenMaya.MFnNurbsSurface( oSurface )
        fnSurface.copy( oSurface, oTarget )



@convertSg_dec
def addIOShape( target ):
    
    targetTr    = target.transform()
    targetShape = target.shape()
    newShapeTr = createNode( 'transform' )
    copyShapeToTransform( targetShape, newShapeTr )
    newShapeTr.shape().attr( 'io' ).set( 1 )
    newShapeName = newShapeTr.shape().name()
    cmds.parent( newShapeName, targetTr.name(), add=1, shape=1 )
    cmds.delete( newShapeTr.name() )
    return convertSg( newShapeName )
        


def curve( **options ):
    return convertSg( cmds.curve( **options ) )



@convertName_dec
def delete( *args, **options ):
    cmds.delete( *args, **options )



def makeController( pointList, defaultScaleMult = 1, **options ):
    
    import copy
    newPointList = copy.deepcopy( pointList )
    for point in newPointList:
        point[0] *= defaultScaleMult
        point[1] *= defaultScaleMult
        point[2] *= defaultScaleMult
    
    options.update( {'p':newPointList, 'd':1} )
    
    typ = 'transform'
    if options.has_key( 'typ' ):
        typ = options.pop( 'typ' )
    
    print typ
    
    crv = curve( **options )
    crvShape = crv.shape()
    
    if options.has_key( 'n' ):
        name = options['n']
    elif options.has_key( 'name' ):
        name = options['name']
    else:
        name = None
    
    jnt = createNode( typ )
    if name: jnt.rename( name )
    parent( crvShape, jnt, add=1, shape=1 )
    delete( crv )
    crvShape = jnt.shape()
    
    ioShape = addIOShape( jnt )
    
    jnt.addAttr( ln='shape_tx', dv=0, cb=1 )
    jnt.addAttr( ln='shape_ty', dv=0, cb=1 )
    jnt.addAttr( ln='shape_tz', dv=0, cb=1 )
    jnt.addAttr( ln='shape_rx', dv=0, cb=1, at='doubleAngle' )
    jnt.addAttr( ln='shape_ry', dv=0, cb=1, at='doubleAngle' )
    jnt.addAttr( ln='shape_rz', dv=0, cb=1, at='doubleAngle' )
    jnt.addAttr( ln='shape_sx', dv=1, cb=1 )
    jnt.addAttr( ln='shape_sy', dv=1, cb=1 )
    jnt.addAttr( ln='shape_sz', dv=1, cb=1 )
    composeMatrix = createNode( 'composeMatrix' )
    jnt.shape_tx >> composeMatrix.inputTranslateX
    jnt.shape_ty >> composeMatrix.inputTranslateY
    jnt.shape_tz >> composeMatrix.inputTranslateZ
    jnt.shape_rx >> composeMatrix.inputRotateX
    jnt.shape_ry >> composeMatrix.inputRotateY
    jnt.shape_rz >> composeMatrix.inputRotateZ
    jnt.shape_sx >> composeMatrix.inputScaleX
    jnt.shape_sy >> composeMatrix.inputScaleY
    jnt.shape_sz >> composeMatrix.inputScaleZ
    trGeo = createNode( 'transformGeometry' )
    jnt.attr( 'radius' ).set( 0 )
    
    ioShape.outputGeometry() >> trGeo.inputGeometry
    composeMatrix.outputMatrix >> trGeo.transform
    
    trGeo.outputGeometry >> crvShape.create

    return jnt





@convertSg_dec
def transformGeometryControl( controller, mesh ):
    
    meshShape = mesh.shape()
    mm = createNode( 'multMatrix' )
    trGeo = createNode( 'transformGeometry' )
    origMesh = addIOShape( mesh )
    srcCon = meshShape.inputGeometry().listConnections( s=1, d=0, p=1 )
    srcAttr = origMesh.attr( 'inMesh' )
    if srcCon:
        srcAttr = srcCon[0]
    print srcAttr.name()

    mesh.wm >> mm.i[0]
    controller.pim >> mm.i[1]
    controller.wm >> mm.i[2]
    mesh.wim >> mm.i[3]
    
    srcAttr >> trGeo.inputGeometry
    mm.o >> trGeo.transform
    
    trGeo.outputGeometry >> meshShape.inputGeometry()
    
    fnMesh = OpenMaya.MFnMesh( getMObject( meshShape.name() ) )
    numVertices = fnMesh.numVertices()
    
    meshName = meshShape.name()
    for i in range( numVertices ):
        cmds.setAttr( meshName + '.pnts[%d]' % i, 0,0,0 )
    



def setPntsZero( targetMesh ):
    shapes = convertSg( targetMesh ).listRelatives( s=1 )
    for shape in shapes:
        if shape.attr( 'io' ).get(): continue
        if shape.nodeType() == 'mesh':
            fnMesh = OpenMaya.MFnMesh( getMObject( shape.name() ) )
            numVertices = fnMesh.numVertices()
            
            meshName = shape.name()
            for i in range( numVertices ):
                cmds.setAttr( meshName + '.pnts[%d]' % i, 0,0,0 )
        elif shape.nodeType() == 'nurbsCurve':
            fnNurbsCurve = OpenMaya.MFnNurbsCurve( getMObject(shape.name()) )
            numCVs = fnNurbsCurve.numCVs()
            
            curveName = shape.name()
            for i in range( numCVs ):
                cmds.setAttr( curveName + '.controlPoints[%d]' % i, 0,0,0 )




@convertSg_dec
def updateFollicleConnection( follicleTr ):
    
    transAttr = follicleTr.t.listConnections( s=1, d=0, p=1 )[0]
    rotateAttr = follicleTr.r.listConnections( s=1, d=0, p=1 )[0]
    
    compose = createNode( 'composeMatrix' )
    mm = createNode( 'multMatrix' )
    dcmp = getDecomposeMatrix( mm )
    
    transAttr >> compose.inputTranslate
    rotateAttr >> compose.inputRotate
    
    compose.outputMatrix >> mm.i[0]
    follicleTr.pim >> mm.i[1]
    
    dcmp.ot >> follicleTr.t
    dcmp.outputRotate >> follicleTr.r


@convertSg_dec
def sliderVisibilityConnection( sliderAttr, *meshs, **options ):
    
    offset = 0
    if options.has_key( 'offset' ):
        offset = options[ 'offset' ]
    
    for i in range( len( meshs ) ):
        setRange = createNode( 'setRange' )
        multNode = createNode( 'multDoubleLinear' )
        setRange.oldMinX.set( offset + i-0.5 )
        setRange.oldMaxX.set( offset + i+0.5 )
        setRange.oldMinY.set( offset + i+0.5 )
        setRange.oldMaxY.set( offset + i+1.4999 )
        setRange.maxX.set( 1 )
        setRange.minY.set( 1 )
        sliderAttr >> setRange.valueX
        sliderAttr >> setRange.valueY
        setRange.outValueX >> multNode.input1
        setRange.outValueY >> multNode.input2
        multNode.output >> meshs[i].v
    
    
    
@convertSg_dec
def makeCurveFromSelection( *sels, **options ):
    
    poses = []
    for sel in sels:
        pose = sel.xform( q=1, ws=1, t=1 )[:3]
        poses.append( pose )
    curve = convertSg( cmds.curve( p=poses, **options ) )
    curveShape = curve.shape()
    
    for i in range( len( sels ) ):
        dcmp = createNode( 'decomposeMatrix' )
        vp   = createNode( 'vectorProduct' ).setAttr( 'op', 4 )
        sels[i].wm >> dcmp.imat
        dcmp.ot >> vp.input1
        curve.wim >> vp.matrix
        vp.output >> curveShape.attr( 'controlPoints' )[i]




class CreateJointOnCurveSet:
    
    def __init__( self ):
        
        self._curveShape = ''
        self._minParam   = 0.0
        self._maxParam   = 1.0
        self._infoNum    = 5
        self._numSpans   = 5
        
        
    def setJointNum( self, num ):
        
        self._infoNum = num
        
        
    def setCurve( self, curveShape ):
        
        self._curveShape = curveShape
        self._minParam = cmds.getAttr( self._curveShape+'.minValue' )
        self._maxParam = cmds.getAttr( self._curveShape+'.maxValue' )
        self._numSpans = cmds.getAttr( self._curveShape+'.spans' )
    
    
    def create(self, distanceNode ):
        
        eachParam = ( self._maxParam - self._minParam )/( self._infoNum - 1 )
        
        eachInfos = []
        
        for i in range( self._infoNum ):
            
            info = cmds.createNode( 'pointOnCurveInfo', n= self._curveShape+'_info%d' % i )
            cmds.connectAttr( self._curveShape+'.local', info+'.inputCurve' )
            cmds.setAttr( info+'.parameter', eachParam*i + self._minParam )
            eachInfos.append( info )
            
        cmds.select( d=1 )
        
        joints = []
        for i in range( self._infoNum ):
            joints.append( cmds.joint(p=[i,0,0]) )
            
        handle, effector = cmds.ikHandle( sj=joints[0], ee=joints[-1], sol='ikSplineSolver', ccv=False, pcv=False, curve=self._curveShape )
        
        distNodes = []
        for i in range( self._infoNum -1 ):
            
            firstInfo = eachInfos[i]
            secondInfo = eachInfos[i+1]
            targetJoint = joints[i+1]
            
            distNode = cmds.createNode( 'distanceBetween' )
            distNodes.append( distNode )
            
            cmds.connectAttr( firstInfo+'.position', distNode+'.point1' )
            cmds.connectAttr( secondInfo+'.position', distNode+'.point2')
            
            if distanceNode:
                cmds.connectAttr( distNode+'.distance', targetJoint+'.tx' )
            else:
                cmds.setAttr( targetJoint+'.tx', cmds.getAttr( distNode+'.distance' ) )
        
        if not distanceNode:
            cmds.delete( distNodes )
        
        return handle, joints
    





def createJointOnCurve( curve, numJoint, distanceNode = True ):
    
    curve = convertSg( curve )
    curveShape = curve.shape()
    
    curveSetInst = CreateJointOnCurveSet()
    curveSetInst.setJointNum( numJoint )
    
    curveSetInst.setCurve( curveShape.name() )
    
    return curveSetInst.create( distanceNode )
    




class SliderBase:
    
    def __init__(self):

        pass
    

    def create(self, axis=None, *args ):
    
        axisX = True
        axisY = True
        
        if axis:
            axisX = False
            axisY = False
            if axis == 'x': axisX = True
            elif axis == 'y': axisY = True
            elif axis == 'xy': axisX = True; axisY = True
    
        baseData = [[-.5,-.5,0],[.5,-.5,0],[.5,.5,0],[-.5,.5,0],[-.5,-.5,0]]
        baseCurve = curve( p=baseData, d=1 )
        baseCurveOrigShape=  addIOShape( baseCurve )
        baseCurveShape = baseCurve.shape()
        
        trGeo = createNode( 'transformGeometry' )
        composeMatrix = createNode( 'composeMatrix' )
        
        if axisX:
            multNodeX = createNode( 'multDoubleLinear' ).setAttr( 'input2', 0.5 )
            addNodeX = createNode( 'addDoubleLinear' ).setAttr( 'input2', 1 )
            baseCurve.addAttr( ln='slideSizeX', min=0, cb=1 )
            baseCurve.slideSizeX >> multNodeX.input1
            baseCurve.slideSizeX >> addNodeX.input1
            addNodeX.output >> composeMatrix.inputScaleX
            multNodeX.output >> composeMatrix.inputTranslateX
        
        if axisY:
            multNodeY = createNode( 'multDoubleLinear' ).setAttr( 'input2', 0.5 )
            addNodeY = createNode( 'addDoubleLinear' ).setAttr( 'input2', 1 )
            baseCurve.addAttr( ln='slideSizeY', min=0, cb=1 )
            baseCurve.slideSizeY >> multNodeY.input1
            baseCurve.slideSizeY >> addNodeY.input1
            addNodeY.output >> composeMatrix.inputScaleY
            multNodeY.output >> composeMatrix.inputTranslateY
        
        composeMatrix.outputMatrix >> trGeo.transform
        baseCurveOrigShape.outputGeometry() >> trGeo.inputGeometry
        trGeo.outputGeometry >> baseCurveShape.inputGeometry()
        
        return baseCurve



@convertSg_dec
def makeParent( sel, **options ):
    
    if not options.has_key( 'n' ) and not options.has_key( 'name' ):
        options.update( {'n':'P'+ sel.localName()} )
    
    selP = sel.parent()
    transform = createNode( 'transform', **options )
    if selP: parent( transform, selP )
    transform.xform( ws=1, matrix= sel.wm.get() )
    parent( sel, transform )
    sel.setTransformDefault()
    return transform



@convertName_dec
def getMatrixFromSelection( *sels ):
    
    isTransform = False
    if len( sels ) == 1:
        if sels[0].find( '.' ) == -1:
            if cmds.objExists( sels[0] ) and cmds.nodeType( sels[0] ) in ['mesh', 'transform']:
                isTransform = True
            
    if sels:
        if isTransform:
            return convertSg( sels[0] ).wm.get()
        else:
            try:
                centerPos = getCenter( sels )
                mtx = [1,0,0,0, 0,1,0,0, 0,0,1,0, centerPos.x, centerPos.y, centerPos.z,1 ]
                return mtx
            except:
                return [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]
    else:
        return [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]



@convertName_dec
def joint( *args, **options ):
    return SGTransformNode( cmds.joint( *args, **options ) )



@convertName_dec
def ikHandle( *args, **options ):
    return convertSg( cmds.ikHandle( *args, **options ) )






        
    


@convertName_dec
def autoCopyWeight( *args ):
    
    first = args[0]
    second = args[1]
    
    hists = cmds.listHistory( first, pdo=1 )
    
    skinNode = None
    for hist in hists:
        if cmds.nodeType( hist ) == 'skinCluster':
            skinNode = hist
    
    if not skinNode: return None
    
    targetSkinNode = None
    targetHists = cmds.listHistory( second, pdo=1 )
    if targetHists:
        for hist in targetHists:
            if cmds.nodeType( hist ) == 'skinCluster':
                targetSkinNode = hist

    if not targetSkinNode:
        bindObjs = cmds.listConnections( skinNode+'.matrix', s=1, d=0, type='joint' )
        bindObjs.append( second )
        cmds.skinCluster( bindObjs, tsb=1 )
    
    cmds.copySkinWeights( first, second, noMirror=True, surfaceAssociation='closestPoint', influenceAssociation ='oneToOne' )
    
    

    
@convertName_dec
def setSkinClusterDefault( *args ):
    
    import sgPlugin
    if not cmds.pluginInfo( 'sgCmdSkinCluster', q=1, l=1 ):
        cmds.loadPlugin( 'sgCmdSkinCluster' )
    cmds.sgCmdSkinClustser( cmds.ls( sl=1 ), d=1 )
    



def separateParentConnection( node, attr ):
    
    parentAttr = cmds.attributeQuery( attr, node=node, listParent=1 )
    
    if parentAttr:
        cons = cmds.listConnections( node+'.'+parentAttr[0], s=1, d=0, p=1, c=1 )
        if cons:
            cmds.disconnectAttr( cons[1], cons[0] )
            srcAttr = cons[1]
            srcNode, srcParentAttr = srcAttr.split( '.' )
            srcAttrs = cmds.attributeQuery( srcParentAttr, node=srcNode, listChildren=1 )
            dstAttrs = cmds.attributeQuery( parentAttr[0], node=node,    listChildren=1 )
            for i in range( len( srcAttrs ) ):
                if cmds.connectAttr( srcNode+'.'+srcAttrs[i], node+'.'+dstAttrs[i] ): continue
                cmds.connectAttr( srcNode+'.'+srcAttrs[i], node+'.'+dstAttrs[i], f=1 )




@convertName_dec
def addMultDoubleLinearConnection( node, attr ):

    newAttrName = 'mult_' + attr
    SGNode( node ).addAttr( ln=newAttrName, cb=1, dv=1 )
    multDouble = cmds.createNode( 'multDoubleLinear' )
    
    separateParentConnection( node, attr )
    
    cons = cmds.listConnections( node + '.' + attr, s=1, d=0, p=1, c=1 )
    cmds.connectAttr( cons[1], multDouble+'.input1' )
    cmds.connectAttr( node+'.'+newAttrName, multDouble + '.input2' )
    cmds.connectAttr( multDouble + '.output', node+'.'+attr, f=1 )
    return convertSg( multDouble )



@convertName_dec
def addAnimCurveConnection( node, attr ):
    
    separateParentConnection( node, attr )
          
    cons = cmds.listConnections( node+'.'+attr, s=1, d=0, p=1, c=1 )
    if not cons: return None
    
    attrType = cmds.attributeQuery( attr, node= node, attributeType=1 )
    
    if attrType == 'doubleLinear':
        animCurveType= 'animCurveUL'
    elif attrType == 'doubleAngle':
        animCurveType = 'animCurveUA'
    else:
        animCurveType = 'animCurveUU'
    
    animCurve = cmds.createNode( animCurveType )
    cmds.connectAttr( cons[1], animCurve+'.input' )
    cmds.connectAttr( animCurve+'.output', cons[0], f=1 )
    
    cmds.setKeyframe( animCurve, f= -1, v= -1 )
    cmds.setKeyframe( animCurve, f=-.5, v=-.5 )
    cmds.setKeyframe( animCurve, f=  0, v=  0 )
    cmds.setKeyframe( animCurve, f= .5, v= .5 )
    cmds.setKeyframe( animCurve, f=  1, v=  1 )
    
    cmds.setAttr( animCurve + ".postInfinity", 1 )
    cmds.setAttr( animCurve + ".preInfinity", 1 )
    
    cmds.selectKey( animCurve )
    cmds.keyTangent( itt='spline', ott='spline' )
    return convertSg( animCurve )




@convertName_dec
def getOrigShape( shape ):
    for hist in cmds.listHistory( shape ):
        if cmds.nodeType( hist ) != 'mesh': continue
        if not cmds.getAttr( hist + '.io' ): continue
        return convertSg( hist )




@convertSg_dec
def createPointOnCurve( curve ):
    
    selShape = curve.shape()
    pointInfoNode = createNode( 'pointOnCurveInfo' )
    trNode = createNode( 'transform' ).setAttr( 'dh', 1 )
    selShape.attr( 'worldSpace' ) >> pointInfoNode.inputCurve
    
    composeNode = createNode( 'composeMatrix' )
    mm = createNode( 'multMatrix' )
    dcmp = createNode( 'decomposeMatrix' )
    
    pointInfoNode.position >> composeNode.inputTranslate
    composeNode.outputMatrix >> mm.i[0]
    trNode.pim >> mm.i[1]
    mm.matrixSum >> dcmp.imat
    
    dcmp.ot >> trNode.t
    trNode.addAttr( ln='parameter', k=1, 
                    min=selShape.attr( 'minValue' ).get(), max=selShape.attr( 'maxValue' ).get() )
    trNode.parameter >> pointInfoNode.parameter
    return trNode.name()



@convertSg_dec
def getParents( target, **options ):
    
    firstTarget=None 
    parents = []
    
    if options.has_key( 'firstTarget' ):
        firstTarget = options['firstTarget']
    if options.has_key('parents' ):
        parents = options['parents']
    
    if not firstTarget:
        firstTarget = target
        parents = []

    ps = target.listRelatives( p=1 )
    if not ps: return parents
    parents.insert( 0, ps[0] )
    
    return getParents( ps[0], firstTarget=firstTarget, parents=parents )



class DataPtr:
    
    def __init__(self):
        
        self.defaultIgnore = []
        self.reverseAttrs = []
        
        self.leftPrefix  = []
        self.rightPrefix = []
        self.data = []



class MirrorInfo:
    
    prefix = 'mi_'
    mirrorTypeAttr = 'mirrorType'
    
    def __init__(self, nodeName ):
        
        nodeName = convertName( nodeName )
        if nodeName[ :len( MirrorInfo.prefix ) ] == MirrorInfo.prefix:    
            mirrorInfo = nodeName
        else:
            mirrorInfo = MirrorInfo.prefix + nodeName
        
        if not cmds.objExists( mirrorInfo ):
            mirrorInfo = cmds.createNode( 'transform', n=mirrorInfo )
            cmds.setAttr( mirrorInfo + '.dh', 1 )
            
        self.mirrorInfo = convertSg( mirrorInfo )
        pivMatrix = convertSg( nodeName ).getPivotMatrix()
        self.mirrorInfo.xform( ws=1, matrix=pivMatrix.getList() )

    
    def origName(self):
        return self.mirrorInfo.localName()[ len( MirrorInfo.prefix ): ]


    def name(self):
        return self.mirrorInfo.name()


    def parent(self):
        mirrorInfoParent = self.mirrorInfo.parent()
        if not mirrorInfoParent:
            return None
        return MirrorInfo( mirrorInfoParent )


    def setParent( self, nodeName ):
        
        parentInst = MirrorInfo( nodeName )
        origParents = self.mirrorInfo.parent()
        if not origParents or origParents.name() != parentInst.mirrorInfo.name():
            parent( self.mirrorInfo, parentInst.mirrorInfo )
    

    def getOtherSide(self, leftPrefixList, rightPrefixList ):
        
        orig = self.mirrorInfo.name()[len( MirrorInfo.prefix ):]
        otherSideOrig = copy.copy( orig )
        for i in range( len( leftPrefixList ) ):
            leftPrefix  = leftPrefixList[i]
            rightPrefix = rightPrefixList[i]
            if orig.find( leftPrefix ) != -1:
                otherSideOrig = orig.replace( leftPrefix, rightPrefix )
            elif orig.find( rightPrefix ) != -1:
                otherSideOrig = orig.replace( rightPrefix, leftPrefix )
            if otherSideOrig:
                break
        
        if not otherSideOrig or not cmds.objExists( otherSideOrig ): return None
        return MirrorInfo( otherSideOrig )
    
    
    def setMirrorType(self, mirrorTypeName ):
        
        self.mirrorInfo.addAttr( ln= MirrorInfo.mirrorTypeAttr, cb=1, at='enum', en=mirrorTypeName + ':' )
    
    
    def getMirrorType(self):
        
        if cmds.attributeQuery( MirrorInfo.mirrorTypeAttr, node = self.mirrorInfo.name(), ex=1 ):
            return cmds.attributeQuery( MirrorInfo.mirrorTypeAttr, node=self.mirrorInfo.name(),le=1 )[0]
        else:
            return 'center'
    
    
        


def getDataPtrFromMirrorInfo( rootMirrorInfo, leftPrefixList, rightPrefixList ):
    
    origRoot = rootMirrorInfo[len(MirrorInfo.prefix):]
    parents = getParents( origRoot )
    rootMirrorInfo = convertSg( rootMirrorInfo )
    children = rootMirrorInfo.listRelatives( c=1, ad=1, type='transform' )
    dataPtrInst = DataPtr()
    dataPtrInst.leftPrefix = leftPrefixList
    dataPtrInst.rightPrefix = rightPrefixList
    for child in children:
        info = MirrorInfo( child )
        otherSide = info.getOtherSide( leftPrefixList, rightPrefixList )
        parent = info.parent()
        dataPtrInst.data.append( [info.origName(), parent.origName(), otherSide.origName(), info.getMirrorType()] )
    return dataPtrInst





class SymmetryControl:

    def __init__(self, name, dataPtr ):
        self.__name = name
        self.__origName = self.__name.split( ':' )[-1]
        self.__namespace = ':'.join( self.__name.split( ':' )[:-1] )
        self.sgtransform = convertSg( self.__name )
        self.dataPtr = dataPtr
    
    
    def fullName(self, origName ):
        return self.__namespace + ':' + origName


    def parent(self):
        for origName, pOrigName, otherSide, mirrorType in self.dataPtr.data:
            if origName != self.__origName: continue
            if not pOrigName: return self
            return [ SymmetryControl( self.fullName( i ), self.dataPtr ) for i in pOrigName.split( ',' ) ]
    
    
    def side(self):
        for leftPrefix in self.dataPtr.leftPrefix:
            if leftPrefix == self.__origName[:len( leftPrefix ) ]:
                return 'left'
        for rightPrefix in self.dataPtr.rightPrefix:
            if rightPrefix == self.__origName[:len( rightPrefix ) ]:
                return 'right'
        return 'center'
    
    
    def otherSide(self):
        for origName, pOrigName, otherSide, mirrorType in self.dataPtr.data:
            if origName != self.__origName:continue
            if not otherSide: return self
            return SymmetryControl( self.fullName( otherSide ), self.dataPtr )


    def mirrorType(self):
        for origName, pOrigName, otherSide, mirrorType in self.dataPtr.data:
            if origName != self.__origName:continue
            return mirrorType.split( ',' )


    def name(self):
        return self.sgtransform.name()


    def setMatrixByMirrorType( self, mirrorTypes, srcLocalMtx ):
        attrs  = ['tx', 'ty', 'tz','rx', 'ry', 'rz']
        revs = [1,1,1,1,1,1]
        values = [0,0,0,0,0,0]
        for mirrorType in mirrorTypes[1:]:
            for attr in attrs:
                mirrorAttr, rev, value= mirrorType.split( '_' )
                if mirrorAttr != attr: continue
                if rev == 'r': revs[ attrs.index( attr ) ] *= -1
                values[ attrs.index( attr ) ] = float( value )

        trans = srcLocalMtx.getTranslate()
        rots  = srcLocalMtx.getRotate()
        trans.x *= revs[0]
        trans.y *= revs[1]
        trans.z *= revs[2]
        rots.x *= revs[3]
        rots.y *= revs[4]
        rots.z *= revs[5]
        srcLocalMtx.setTranslate( trans )
        srcLocalMtx.setRotate( rots )
        transAddValues = values[:3]
        rotAddValues = values[3:]
        srcLocalMtx.translateOutside( *transAddValues )
        srcLocalMtx.rotateInside( *rotAddValues )
        return srcLocalMtx


    def getCtlData(self, source ):
        
        sourceParent = source.parent()
        if not source.parent(): return None
        
        sgtrans = source.sgtransform
        udAttrs = sgtrans.listAttr( k=1, ud=1 )
        udAttrValues = []
        for attr in udAttrs:
            if attr in self.dataPtr.reverseAttrs:
                udAttrValues.append( -sgtrans.attr( attr ).get() )
            else:
                udAttrValues.append( sgtrans.attr( attr ).get() )
        transformAttrs = ['tx','ty','tz','rx','ry','rz','sx','sy','sz']
        transformAttrValues = []
        for attr in transformAttrs:
            transformAttrValues.append( sgtrans.attr( attr ).get() )
        worldMatrix = sgtrans.getWorldMatrix()
        pivMatrix   = sourceParent[0].sgtransform.getPivotMatrix()
        return udAttrs, udAttrValues, transformAttrs, transformAttrValues, worldMatrix * pivMatrix.inverse()
    
    
    def setCtlData(self, source, target, ctlData, typ='mirror' ):

        if not ctlData: return None

        mirrorTypes = source.mirrorType()
        udAttrs, udAttrValues, transformAttrs, transformValues, localMatrix = ctlData
        
        trg = target.sgtransform
        for i in range( len( udAttrs ) ):
            try:
                trg.attr( udAttrs[i] ).set( udAttrValues[i] )
            except:pass
        for i in range( len( transformAttrs ) ):
            try:trg.attr( transformAttrs[i] ).set( transformValues[i] )
            except:pass
        
        if 'none' in mirrorTypes: return None

        if 'local' in mirrorTypes:
            trg.tx.set( -trg.tx.get() )
            trg.ty.set( -trg.ty.get() )
            trg.tz.set( -trg.tz.get() )
        
        if 'txm' in mirrorTypes:
            trg.tx.set( -trg.tx.get() )
        if 'tym' in mirrorTypes:
            trg.ty.set( -trg.ty.get() )
        if 'tzm' in mirrorTypes:
            trg.tz.set( -trg.tz.get() )
        if 'rxm' in mirrorTypes:
            trg.rx.set( -trg.rx.get() )
        if 'rym' in mirrorTypes:
            trg.ry.set( -trg.ry.get() )
        if 'rzm' in mirrorTypes:
            trg.rz.set( -trg.rz.get() )

        if 'matrix' in mirrorTypes:
            srcLocalMtx = self.setMatrixByMirrorType( mirrorTypes, localMatrix )
            dstMatrix = srcLocalMtx * target.parent()[0].sgtransform.getPivotMatrix()

            rotList = dstMatrix.getRotate().getList()
            for i in range( len( rotList ) ):
                rotList[i] = math.degrees(rotList[i])
            target.sgtransform.xform( ws=1, t= dstMatrix.getTranslate().getList() )
            target.sgtransform.xform( ws=1, ro= rotList )
        
        if 'center' in mirrorTypes:
            if typ == 'flip':
                setMirrorLocal( target.sgtransform )
            elif typ == 'mirror':
                setCenterMirrorLocal( target.sgtransform )
        
    
    def isMirrorAble(self):
        
        for origName, pOrigName, otherSide, mirrorType in self.dataPtr.data:
            if origName != self.__origName: continue
            return True
        return False
    
    

    def setMirror(self, side ):
        
        if not self.isMirrorAble(): return None
        
        if side == 'LtoR':
            if self.side() == 'left':
                source = self
                target = self.otherSide()
            else:
                source = self.otherSide()
                target = self
                
        if side == 'RtoL':
            if self.side() == 'right':
                source = self
                target = self.otherSide()
            else:
                source = self.otherSide()
                target = self
        
        self.setCtlData( source, target, self.getCtlData( source ), 'mirror' )
    
    
    def setFlip(self):

        if not self.isMirrorAble(): return None

        source = self
        target = self.otherSide()
        dataSource = self.getCtlData( source )
        dataTarget = self.getCtlData( target )
        
        self.setCtlData( source, target, dataSource, 'flip' )
        self.setCtlData( target, source, dataTarget, 'flip' )
    


    def flipH(self):
        
        if not self.isMirrorAble(): return None
        
        H = self.allChildren()
    
        flipedList = []
        sourceList = []
        targetList = []
        sourceDataList = []
        targetDataList = []
        
        for h in H:
            
            name = h.otherSide().name()
            if name in flipedList: continue
            flipedList.append( h.name() )
            
            otherSide = h.otherSide()
            sourceList.append( h )
            targetList.append( otherSide )
            sourceDataList.append( self.getCtlData( h ) )
            targetDataList.append( self.getCtlData( otherSide ) )
        
        for i in range( len( sourceList ) ):
            self.setCtlData( sourceList[i], targetList[i], sourceDataList[i], 'flip' )
            self.setCtlData( targetList[i], sourceList[i], targetDataList[i], 'flip' )


    def mirrorH(self, side ):
        
        if not self.isMirrorAble(): return None
        
        if side == 'LtoR':
            if self.side() == 'left':
                source = self
            else:
                source = self.otherSide()
                
        if side == 'RtoL':
            if self.side() == 'right':
                source = self
            else:
                source = self.otherSide()
        
        H = source.allChildren()
    
        sourceList = []
        targetList = []
        sourceDatas = []

        for h in H:
            if side == 'LtoR' and h.side() == 'right': continue
            if side == 'RtoL' and h.side() == 'left' : continue
            
            otherSide = h.otherSide()
            sourceList.append( h )
            targetList.append( otherSide )
            sourceDatas.append( self.getCtlData( h ) )
        
        for i in range( len( sourceList ) ):
            self.setCtlData( sourceList[i], targetList[i], sourceDatas[i], 'mirror' )
        


    def children(self):
        
        targetChildren = []
        for origName, pOrigName, otherSide, mirrorType in self.dataPtr.data:
            if not self.__origName in pOrigName.split( ',' ): continue
            print "origName : ", origName
            targetChildren.append( SymmetryControl( self.fullName( origName ), self.dataPtr ) )
        return targetChildren


    def allChildren(self):
        
        localChildren = self.children()
        childrenH = []
        for localChild in localChildren:
            childrenH += localChild.allChildren()
        localChildren += childrenH
        childrenNames = []

        localChildrenSet = []
        for localChild in localChildren:
            name = localChild.name()
            if name in childrenNames: continue
            childrenNames.append( name )
            localChildrenSet.append( localChild )
        
        return localChildrenSet
    
    
    def hierarchy(self):
        
        localChildren = [self]
        localChildren += self.allChildren()
        return localChildren
    

    def setDefault(self):

        attrs = self.sgtransform.listAttr( k=1 )
        for attr in attrs:
            if attr in self.dataPtr.defaultIgnore: continue
            try:self.sgtransform.attr(attr).setToDefault()
            except:pass





@convertSg_dec
def getTransformWorldVector( trNode, **options ):
    
    vectorName = 'v'
    vectorValue = [1,0,0]
    if options.has_key( 'vectorName' ):
        vectorName = options['vectorName']
    if options.has_key( 'vector' ):
        vectorValue = options['vector']
    
    dcmp = getDecomposeMatrix( trNode ).rename( 'dcmp_' + trNode.name() )
    compose = createNode( 'composeMatrix' ).rename( 'composeTrans_' + trNode.name() )
    dcmp.ot >> compose.inputTranslate
    inverse = createNode( 'inverseMatrix' ).rename( 'invm_' + trNode.name() )
    compose.matrixOutput() >> inverse.inputMatrix
    composeVector = createNode( 'composeMatrix', n='compose_%sVector' % vectorName )
    composeVector.it.set( *vectorValue )
    mmTrans = createNode( 'multMatrix', n='mmTrans_' + trNode.name() )
    
    composeVector.outputMatrix >> mmTrans.i[0]
    trNode.wm >> mmTrans.i[1]
    inverse.matrixOutput() >> mmTrans.i[2]
    
    return getDecomposeMatrix( mmTrans ).rename( 'dcmp%sVector_' % vectorName + trNode.name() )





@convertSg_dec
def getCloseMatrixOnMesh( matrixObj, mesh  ):

    matrixObjDcmp = getDecomposeMatrix( getLocalMatrix( matrixObj, mesh) )
    meshShape = mesh.shape()
    closePointOnMesh = createNode( 'closestPointOnMesh', n='close_%s_%s' %( matrixObj.name(), mesh.name() ) )
    meshShape.outMesh     >> closePointOnMesh.inMesh
    matrixObjDcmp.outputTranslate >> closePointOnMesh.inPosition
    
    normalVector = createNode( 'vectorProduct' ).setAttr( 'op', 3 )
    positionVector     = createNode( 'vectorProduct' ).setAttr( 'op', 4 )
    closePointOnMesh.normal >> normalVector.input1
    meshShape.worldMatrix >> normalVector.matrix
    closePointOnMesh.position >> positionVector.input1
    meshShape.worldMatrix >> positionVector.matrix
    
    dcmpYVector = getTransformWorldVector( matrixObj, vectorName = 'y', vector=[0,1,0] )
    
    xVectorNode = getCrossVectorNode( dcmpYVector, normalVector )
    yVectorNode = getCrossVectorNode( normalVector, xVectorNode )
    
    fbfNode = getFbfMatrix( xVectorNode, yVectorNode, normalVector )
    positionVector.outputX >> fbfNode.in30
    positionVector.outputY >> fbfNode.in31
    positionVector.outputZ >> fbfNode.in32
    
    mm = createNode( 'multMatrix' )
    trNode = createNode( 'transform' ).setAttr( 'dh', 1 )
    
    fbfNode.matrixOutput() >> mm.i[0]
    trNode.parentInverseMatrix >> mm.i[1]
    
    dcmp = getDecomposeMatrix( mm )
    dcmp.outputTranslate >> trNode.t
    dcmp.outputRotate >> trNode.r
    
    select( trNode )



def createTextureFileNode( filePath ):
    
    fileNode = convertSg( cmds.shadingNode( "file", asTexture=1, isColorManaged=1 ) )
    place2d  = convertSg( cmds.shadingNode( "place2dTexture", asUtility=1 ) )
    
    fileNode.attr( 'fileTextureName' ).set( filePath, type='string' )
    
    place2d.coverage >> fileNode.coverage
    place2d.translateFrame  >> fileNode.translateFrame 
    place2d.rotateFrame  >> fileNode.rotateFrame 
    place2d.mirrorU  >> fileNode.mirrorU 
    place2d.mirrorV  >> fileNode.mirrorV
    place2d.stagger >> fileNode.stagger
    place2d.wrapU >> fileNode.wrapU
    place2d.wrapV >> fileNode.wrapV
    place2d.repeatUV >> fileNode.repeatUV
    place2d.offset >> fileNode.offset
    place2d.rotateUV >> fileNode.rotateUV
    place2d.noiseUV >> fileNode.noiseUV
    place2d.vertexUvOne >> fileNode.vertexUvOne
    place2d.vertexUvTwo >> fileNode.vertexUvTwo
    place2d.vertexUvThree >> fileNode.vertexUvThree
    place2d.vertexCameraOne >> fileNode.vertexCameraOne
    place2d.outUV >> fileNode.uv
    place2d.outUvFilterSize >> fileNode.uvFilterSize
    
    return fileNode, place2d



@convertSg_dec
def assignToLayeredTexture( textureNode, layeredTexture, **options ):
    
    index = None
    blendMode = None
    if options.has_key( 'index' ):
        index = options['index']
    if options.has_key( 'blendMode' ):
        blendMode = options['blendMode']

    if index == None:
        inputsPlug = layeredTexture.attr( 'inputs' ).getPlug()
        if inputsPlug.numElements():
            logicalIndex = inputsPlug[ inputsPlug.numElements()-1 ].logicalIndex()
        else:
            logicalIndex = -1
        index = logicalIndex + 1

    textureNode.outColor >> layeredTexture.inputs[ index ].color
    textureNode.outAlpha >> layeredTexture.inputs[ index ].alpha
    
    if blendMode != None:
        layeredTexture.inputs[ index ].blendMode.set( blendMode )



@convertSg_dec
def clearArrayAttribute( attr ):

    connectedAttrs = attr.node().listConnections( s=1, d=0, p=1, c=1 )
    
    for i in range( 0, len( connectedAttrs ), 2 ):
        srcAttr = connectedAttrs[i+1]
        dstAttr = connectedAttrs[ i ]
        
        srcAttr // dstAttr
    
    plugAttr = attr.getPlug()
    for i in range( plugAttr.numElements() ):
        try:cmds.removeMultiInstance( plugAttr[i].name() )
        except:pass
    
    

@convertName_dec
def group( *args, **kwangs ):
    grp = cmds.group( *args, **kwangs )
    return convertSg( grp )





def getCurrentModelPanels():
    
    pannels = cmds.getPanel( vis=1 )

    modelPanels = []
    for pannel in pannels:
        if cmds.modelPanel( pannel, ex=1 ):
            modelPanels.append( pannel )
    return modelPanels




@convertName_dec
def combineMultiShapes( *shapeObjs ):
    
    shapes = []
    
    trNodes = cmds.listRelatives( shapeObjs, c=1, ad=1, type='transform' )
    if not trNodes: trNodes = []
    trNodes += shapeObjs
    
    for trNode in trNodes:
        childShapes = cmds.listRelatives( trNode, s=1, f=1 )
        if not childShapes: continue
        for childShape in childShapes:
            if cmds.nodeType( childShape ) != 'nurbsCurve': continue
            shapes.append( childShape )
    
    mtxGroup = cmds.getAttr( shapeObjs[0]+'.wm' )
    mmtxInvGroup = listToMatrix( mtxGroup ).inverse()
    
    for shape in shapes:
        shapeType = cmds.nodeType( shape )
        
        shapeTransform = cmds.listRelatives( shape, p=1 )[0]
        
        mtxShapeTransform = cmds.getAttr( shapeTransform+'.wm' )
        
        mmtxShapeTransform = listToMatrix( mtxShapeTransform )
        mmtxLocal = mmtxShapeTransform * mmtxInvGroup
        
        mtxLocal = matrixToList( mmtxLocal )
        trGeoNode = cmds.createNode( 'transformGeometry' )
        
        outputShapeNode = cmds.createNode( shapeType )
        outputShapeObject = cmds.listRelatives( outputShapeNode, p=1 )[0]
        if shapeType == 'mesh':
            outputAttr = 'outMesh'
            inputAttr = 'inMesh'
        elif shapeType == 'nurbsCurve':
            outputAttr = 'local'
            inputAttr  = 'create'
        elif shapeType == 'nurbsSurface':
            outputAttr = 'local'
            inputAttr = 'create'
        else:
            continue
            
        cmds.connectAttr( shape+'.'+outputAttr, trGeoNode+'.inputGeometry' )
        cmds.setAttr( trGeoNode+'.transform', mtxLocal, type='matrix' )
        cmds.connectAttr( trGeoNode+'.outputGeometry', outputShapeNode+'.'+inputAttr )
        
        outputShapeNode = cmds.parent( outputShapeNode, shapeObjs[0], add=1, shape=1 )
        cmds.delete( outputShapeObject )
        cmds.rename( outputShapeNode, shapeObjs[0]+'Shape' )
        cmds.refresh()
    
    cmds.delete( shapeObjs[1:])
    cmds.delete( cmds.listRelatives( shapeObjs[0], c=1, ad=1, f=1, type='transform' ) )
    
    return shapeObjs[0]



def duplicateShadingNetwork( shadingEngine ):
    
    import pymel.core
    shadingEngine = pymel.core.ls( shadingEngine )[0]
    shaderConnectedNodes = shadingEngine.listConnections( s=1, d=0 )
    
    hists = []
    for node in shaderConnectedNodes:
        if hasattr( node, 'worldMatrix' ):continue
        hists += node.history()
    
    shadingNodes = [shadingEngine.name()]
    duShadingNodes = [cmds.duplicate( shadingEngine.name() )[0]]
    for hist in hists:
        if hasattr( hist, 'worldMatrix' ): continue
        if hist.name() in shadingNodes: continue
        shadingNodes.append( hist.name() )
        duShadingNodes.append( cmds.duplicate( hist.name() )[0] )
    
    for i in range( len( shadingNodes ) ):
        shadingNode = shadingNodes[i]
        duOrig = duShadingNodes[i]
    
        srcCons = cmds.listConnections( shadingNode, s=1, d=0, p=1, c=1 )
        dstCons = cmds.listConnections( shadingNode, s=0, d=1, p=1, c=1 )
        if not srcCons: srcCons = []
        if not dstCons: dstCons = []

        for j in range( 0, len( srcCons ), 2 ):
            origCon = srcCons[j]
            srcCon  = srcCons[j+1]
            
            origAttr = '.'.join( origCon.split( '.' )[1:] )
            srcNode  = srcCon.split( '.' )[0]
            srcAttr  = '.'.join( srcCon.split( '.' )[1:] )
            
            if not srcNode in shadingNodes: continue
            targetIndex = shadingNodes.index(srcNode)
            duSrcNode = duShadingNodes[ targetIndex ]
            if cmds.isConnected( duSrcNode + '.' + srcAttr, duOrig + '.' + origAttr ): continue
            cmds.connectAttr( duSrcNode + '.' + srcAttr, duOrig + '.' + origAttr )
        
        for j in range( 0, len( dstCons ), 2 ):
            origCon = dstCons[j]
            dstCon  = dstCons[j+1]
            
            origAttr = '.'.join( origCon.split( '.' )[1:] )
            dstNode  = dstCon.split( '.' )[0]
            dstAttr  = '.'.join( dstCon.split( '.' )[1:] )

            if not dstNode in shadingNodes: continue
            targetIndex = shadingNodes.index(dstNode)
            duDstNode = duShadingNodes[ targetIndex ]
            if cmds.isConnected( duOrig + '.' + origAttr, duDstNode + '.' + dstAttr ): continue
            print duOrig + '.' + origAttr, duDstNode + '.' + dstAttr
            cmds.connectAttr( duOrig + '.' + origAttr, duDstNode + '.' + dstAttr )



def reverseOutput( target ):
    
    target = pymel.core.ls( target )[0]
    destCons = target.listConnections( s=0, d=1, p=1, c=1 )
    
    outputAttrs = []
    for origAttr, destAttr in destCons:
        if origAttr.parent():
            outputAttrs.append( origAttr.parent() )
        else:
            outputAttrs.append( origAttr )
    outputAttrs = list( set( outputAttrs ) )
    
    def connectReverseVectorOutput( outputAttr ):
        multNode = outputAttr.listConnections( type='multiplyDivide', s=0, d=1 )
        if multNode: multNode = multNode[0]
        else: multNode = None
        cons = outputAttr.listConnections( s=0, d=1, p=1, c=1 )
        if not cons: cons = []
        dstAttrs = []
        for origAttr, dstAttr in cons:
            dstAttrs.append( dstAttr )
        if not multNode:
            multNode = pymel.core.createNode( 'multiplyDivide' )
            outputAttr >> multNode.input1
            multNode.input2.set( 1,1,1 )
        if multNode.input2.listConnections( s=1, d=0 ):
            multNode = pymel.core.createNode( 'multiplyDivide' )
            outputAttr >> multNode.input1
            multNode.input2.set( 1,1,1 )
        origValue = multNode.input2.get()
        multNode.input2.set( -origValue[0], -origValue[1], -origValue[2] )
        for dstAttr in dstAttrs:
            if dstAttr.node() == multNode: continue
            multNode.output >> dstAttr
        
        childrenAttrs = outputAttr.children()
        for i in range( len( childrenAttrs ) ):
            childrenAttr = childrenAttrs[i]
            childrenCons = childrenAttr.listConnections( s=0, d=1, p=1, c=1 )
            if not childrenCons: childrenCons = []
            for origAttr, dstAttr in childrenCons:
                multNode.output.children()[i] >> dstAttr

    def connectReverseScalarOutput( outputAttr ):
        multNode = outputAttr.listConnections( type='multDoubleLinear', s=0, d=1 )
        if multNode: multNode = multNode[0]
        else: multNode = None
        if not multNode:
            multNode = pymel.core.createNode( 'multDoubleLinear' )
            outputAttr >> multNode.input1
            multNode.input2.set( 1 )
        if multNode.input2.listConnections( s=1, d=0 ):
            multNode = pymel.core.createNode( 'multDoubleLinear' )
            outputAttr >> multNode.input1
            multNode.input2.set( 1 )
        origValue = multNode.input2.get()
        multNode.input2.set( -origValue )
        cons = outputAttr.listConnections( s=0, d=1, p=1, c=1 )
        for origAttr, dstAttr in cons:
            if dstAttr.node() == multNode: continue
            multNode.output >> dstAttr

    for outputAttr in outputAttrs:
        try:
            childrenAttr = outputAttr.children()
            connectReverseVectorOutput( outputAttr )
        except:
            connectReverseScalarOutput( outputAttr )
            


@convertName_dec
def bezierCurve( *sels ):

    selPoses = []
    
    for sel in sels:
        selPos = cmds.xform( sel, q=1, ws=1, t=1 )[:3]
        selPoses.append( selPos )
    
    bezier = cmds.curve( bezier=1, p=selPoses, d=3 )
    bezier = cmds.listRelatives( bezier, s=1, f=1 )[0]
    
    for i in range( len( sels ) ):
        sel = sels[i]
        dcmp = cmds.createNode( 'decomposeMatrix' )
        cmds.connectAttr( sel + '.wm', dcmp + '.imat' )
        cmds.connectAttr( dcmp + '.ot', bezier + '.controlPoints[%d]' % i )



@convertSg_dec
def getCurveInfo( curve, **options ):
    
    space = 'world'
    if options.has_key( space ):
        space = options[ space ]
    
    curveShape = curve.shape()
    
    outputAttr = 'worldSpace'
    if space == 'local':
        outputAttr = 'local'
    
    cons = curveShape.attr( outputAttr ).listConnections( d=1, s=0, type='curveInfo' )
    if cons:
        return cons[0].name()
    
    curveInfo = createNode( 'curveInfo' )
    curveShape.attr( outputAttr ) >> curveInfo.inputCurve
    return curveInfo.name()



def makeCurveInfoTransforms( curve ):
    
    curve = pymel.core.ls( curve )[0]
    if curve.type() == 'transform':
        curveShape = curve.getShape()
    else:
        curveShape = curve
    numCVs = curveShape.numCVs()
    
    curveInfo = getCurveInfo( curve ) 
    curveInfo = pymel.core.ls( curveInfo )[0]
    
    targets = []
    for i in range( numCVs ):
        target = pymel.core.createNode( 'transform' )
        target.dh.set( 1 )
        vectorNode = pymel.core.createNode( 'vectorProduct' )
        vectorNode.op.set( 4 )
        curveInfo.controlPoints[i] >> vectorNode.input1
        target.pim >> vectorNode.matrix
        vectorNode.output >> target.t
        targets.append( target.name() )
    return targets



def makeFloorResult( tr, floorTr ):

    resultTr = createNode( 'transform' )
    condition = createNode( 'condition' ).setAttr( 'operation', 2 ).setAttr( 'colorIfFalseR', 0 )
    composeMtx = createNode( 'composeMatrix' )
    localDcmp = getDecomposeMatrix( getLocalMatrix( tr, floorTr ) )
    
    localDcmp.oty >> condition.firstTerm
    localDcmp.oty >> condition.colorIfTrueR
    
    localDcmp.otx >> composeMtx.itx
    condition.outColorR >> composeMtx.ity
    localDcmp.otz >> composeMtx.itz
    
    mm = createNode( 'multMatrix' )
    composeMtx.outputMatrix >> mm.i[0]
    convertSg( floorTr ).wm >> mm.i[1]
    resultTr.pim >> mm.i[2]
    dcmp = getDecomposeMatrix( mm )
    
    dcmp.ot >> resultTr.t



def setGeometryMatrixToTarget( geo, matrixTarget ):
    
    geo = convertSg( geo )
    matrixTarget = convertSg( matrixTarget )
    geoShapes = geo.listRelatives( s=1 )
    
    geoMatrix    = listToMatrix( geo.wm.get() )
    targetMatrix = listToMatrix( matrixTarget.wm.get() )
    
    outputAttr = ''
    inputAttr = ''
    
    for geoShape in geoShapes:
        ioShape = addIOShape( geoShape )
        if geoShape.nodeType() == 'mesh':
            outputAttr = 'outMesh'
            inputAttr = 'inMesh'
        elif geoShape.nodeType() in ['nurbsCurve', 'nurbsSurface']:
            outputAttr = 'local'
            inputAttr = 'create'
        
        trGeo = createNode( 'transformGeometry' )
        ioShape.attr( outputAttr ) >> trGeo.inputGeometry
        trGeo.outputGeometry >> geoShape.attr( inputAttr )
        trGeo.transform.set( matrixToList(geoMatrix * targetMatrix.inverse()), type='matrix' )
    
    geo.xform( ws=1, matrix= matrixTarget.wm.get() )
    setPntsZero( geo )


@convertSg_dec
def getNearPointOnCurve( tr, curve ):

    node = createNode( 'nearestPointOnCurve' )
    dcmp = getDecomposeMatrix( tr )
    curveShape = curve.shape()
    
    dcmp.ot >> node.inPosition
    curveShape.attr( 'worldSpace' ) >> node.inputCurve
    
    return node
    
    


@convertSg_dec
def replaceShape( src, dst ):
    
    dstShapes = dst.listRelatives( s=1 )
    srcShape = src.shape()
    
    delete( dstShapes )
    parent( srcShape, dst, add=1, shape=1 )
    
    
    
def todayNodeId():
    
    import datetime
    cuTime = datetime.datetime.now()
    sg = str( hex( 0x73 + 0x67 ) )
    today = str( hex( int( '%04d' % cuTime.year + '%02d' % cuTime.month + '%02d' % cuTime.day ) ) )
    return sg + " + " + today
    



@convertName_dec
def getSortedListByClosestPosition( srcGrp, targetGrp ):
    
    srcChildren = cmds.listRelatives( srcGrp, c=1, type='transform' )
    targetChildren = cmds.listRelatives( targetGrp, c=1, type='transform' )
    
    srcPoses = []
    for srcChild in srcChildren:
        srcPos = OpenMaya.MPoint( *cmds.xform( srcChild, q=1, ws=1, t=1 ) )
        srcPoses.append( srcPos )
    
    targetPoses = []
    for targetChild in targetChildren:
        targetPos = OpenMaya.MPoint( *cmds.xform( targetChild, q=1, ws=1, t=1 ) )
        targetPoses.append( targetPos )
    
    sortedChildren = []
    for i in range( len( srcPoses ) ):
        srcPose = srcPoses[i]
        minDist = 10000000.0
        minDistIndex = 0
        for j in range( len( targetPoses ) ):
            targetPose = targetPoses[j]
            dist = srcPose.distanceTo( targetPose )    
            if minDist > dist:
                minDist = dist
                minDistIndex = j
        
        sortedChildren.append( targetChildren[minDistIndex] )
    return sortedChildren
                


    

def getInfluencesFromSelVertices():
    
    sels = pymel.core.ls( sl=1, fl=1 )
    
    targetJnts = []
    for sel in sels:
        mesh = sel.node()
        hists = mesh.history()
        skinNode = None
        for hist in hists:
            if hist.type() == 'skinCluster':
                skinNode = hist
                break
        
        elements = skinNode.weightList[ sel.index() ].weights.elements()
        for element in elements:
            index = int( element.split( '[' )[-1].replace( ']', '' ) )
            jnts = skinNode.matrix[ index ].listConnections( s=1, d=0, type='joint' )
            for jnt in jnts:
                targetJnts.append( jnt.name() )
    
    return list( set( targetJnts ) )
    
    

def connectBindPre( targetGeo ):
    
    targetGeo = pymel.core.ls( sl=1, fl=1 )[0]
    
    hists = targetGeo.history( pdo=1 )
    
    skinNode = None
    for hist in hists:
        if hist.type() == 'skinCluster':
            skinNode = hist
            break
    
    cons = skinNode.matrix.listConnections( s=1, d=0, c=1 )
    for attr, targetJnt in cons:
        targetJnt.pim >> attr.replace( 'matrix', 'bindPreMatrix' )




@convertSg_dec
def addOptionAttribute( target ):
    
    barString = '____'
    while target.attributeQuery( barString, ex=1 ):
        barString += '_'
    
    target.addAttr( ln=barString,  at="enum", en="Options:", cb=1 )


    
    
class BodyRig:
    
    def __init__(self, stdBase, stdRoot, stdBackFirst, stdBackSecond, stdChest ):
        
        self.stdPrefix = 'StdJnt_'
        self.stdBase = convertSg( stdBase )
        self.stdRoot = convertSg( stdRoot )
        self.stdBackFirst = convertSg( stdBackFirst )
        self.stdBackSecond = convertSg( stdBackSecond )
        self.stdChest = convertSg( stdChest )
        
        self.controllerSize = 1
        
        
    
    def createAll(self, numJoint, controllerSize = 1 ):
        
        self.controllerSize = controllerSize
        
        self.createRigBase()
        self.createController()
        self.connectAndParentController()
        self.createOrigCurve()
        self.createCurve()
        self.createResultJoints( numJoint )
    
        
    
    def createRigBase(self):
        
        self.rigBase = createNode( 'transform', n= 'RigBase_body' )
        self.rigBase.xform( ws=1, matrix= self.stdRoot.wm.get() )
    


    def createController(self):
        
        self.ctlRoot = makeController( sgdata.Controllers.movePoints, self.controllerSize, n= 'Ctl_Root' ).xform( ws=1, matrix= self.stdRoot.wm.get() )
        self.ctlPervis = makeController( sgdata.Controllers.cubePoints, self.controllerSize, n='Ctl_PervisRotator' ).xform( ws=1, matrix= self.stdRoot.wm.get() )
        self.ctlBodyRotator1 = makeController( sgdata.Controllers.cubePoints, self.controllerSize, n='Ctl_BodyRotator1' ).xform( ws=1, matrix= self.stdBackFirst.wm.get() )
        self.ctlBodyRotator2 = makeController( sgdata.Controllers.cubePoints, self.controllerSize, n='Ctl_BodyRotator2' ).xform( ws=1, matrix= self.stdBackSecond.wm.get() )
        self.ctlChest = makeController( sgdata.Controllers.circlePoints, self.controllerSize, n='Ctl_Chest' ).xform( ws=1, matrix= self.stdChest.wm.get() )
        self.ctlWaist = makeController( sgdata.Controllers.circlePoints, self.controllerSize, n='Ctl_Waist' ).xform( ws=1, matrix= self.stdBackFirst.wm.get() )
        self.ctlHip   = makeController( sgdata.Controllers.circlePoints, self.controllerSize, n='Ctl_Hip' ).xform( ws=1, matrix= self.stdRoot.wm.get() )
        
        makeParent( self.ctlRoot )
        makeParent( self.ctlPervis )
        makeParent( self.ctlBodyRotator1 )
        makeParent( self.ctlBodyRotator2 )
        makeParent( self.ctlChest )
        makeParent( self.ctlWaist )
        makeParent( self.ctlHip )
    


    def connectAndParentController(self):
        
        pCtlHip = self.ctlHip.parent()
        pCtlWaist = self.ctlWaist.parent()
        pCtlChest = self.ctlChest.parent()
        pCtlRoot = self.ctlRoot.parent()
        pCtlPervis = self.ctlPervis.parent()
        pCtlBodyRotator1 = self.ctlBodyRotator1.parent()
        pCtlBodyRotator2 = self.ctlBodyRotator2.parent()
        
        parent( pCtlRoot, self.rigBase )
        parent( pCtlHip, self.ctlRoot )
        parent( pCtlPervis, self.ctlRoot )
        parent( pCtlBodyRotator1, self.ctlRoot )
        
        parent( pCtlBodyRotator2, self.ctlBodyRotator1 )
        parent( pCtlWaist, self.ctlBodyRotator1 )
        
        self.stdBackSecond.t >> pCtlBodyRotator2.t
        self.stdBackSecond.r >> pCtlBodyRotator2.r
        self.stdChest.t >> pCtlChest.t
        self.stdChest.r >> pCtlChest.r
        
        parent( pCtlChest, self.ctlBodyRotator2 )

        hipPivInWaist = createNode( 'transform', n='Pointer_hipInWaist' )
        parent( hipPivInWaist, self.ctlWaist )
        dcmp_hipPivInWaist = getDecomposeMatrix( getLocalMatrix( self.ctlPervis, pCtlWaist ) )
        dcmp_hipPivInWaist.ot >> hipPivInWaist.t
        dcmp_hipPivInWaist.outputRotate >> hipPivInWaist.r
        
        constrain_parent( hipPivInWaist, pCtlHip )
        
        waistPivInPervis = createNode( 'transform', n='Pointer_waistiInPervis' )
        parent( waistPivInPervis, self.ctlPervis )
        self.stdBackFirst.t >> waistPivInPervis.t
        
        constrain_point( waistPivInPervis, pCtlBodyRotator1 )
        
        self.stdBackFirst.r >> pCtlBodyRotator1.r
    
    
    
    def createOrigCurve(self):
        
        dcmp0 = getDecomposeMatrix( getLocalMatrix ( self.stdRoot, self.stdRoot ) )
        dcmp1 = getDecomposeMatrix( getLocalMatrix ( self.stdBackFirst, self.stdRoot ) )
        dcmp2 = getDecomposeMatrix( getLocalMatrix ( self.stdBackSecond, self.stdRoot ) )
        dcmp3 = getDecomposeMatrix( getLocalMatrix ( self.stdChest, self.stdRoot ) )
    
        points = [ [0.0,0.0,0.0] for i in range( 4 ) ]
        origCurve = curve( p=points, d=3 ).parentTo( self.ctlRoot ).setTransformDefault()
        origCurveShape = origCurve.shape()
        dcmp0.ot >> origCurveShape.attr( "controlPoints" )[0]
        dcmp1.ot >> origCurveShape.attr( "controlPoints" )[1]
        dcmp2.ot >> origCurveShape.attr( "controlPoints" )[2]
        dcmp3.ot >> origCurveShape.attr( "controlPoints" )[3]
        self.origCurve = origCurve
    
    
    
    def createCurve(self):
        
        pointerGrp_inChest = createNode( 'transform' ).parentTo( self.ctlChest.parent() )
        pointerGrp_inChest.setTransformDefault()
        pointerBody1_inChest = createNode( 'transform' ).parentTo( pointerGrp_inChest )
        pointerBody2_inChest = createNode( 'transform' ).parentTo( pointerGrp_inChest )
        pointerGrp_inHip = createNode( 'transform' ).parentTo( self.ctlHip.parent() ).setTransformDefault()
        pointerBody1_inHip   = createNode( 'transform' ).parentTo( pointerGrp_inHip )
        pointerBody2_inHip   = createNode( 'transform' ).parentTo( pointerGrp_inHip )
        pointerBody1 = createNode( 'transform' ).parentTo( self.rigBase )
        pointerBody2 = createNode( 'transform' ).parentTo( self.rigBase )
        
        self.ctlChest.t >> pointerGrp_inChest.t
        self.ctlHip.t >> pointerGrp_inHip.t
        
        dcmpPointerBody1_inChest = getDecomposeMatrix( getLocalMatrix( self.ctlBodyRotator1, self.ctlChest.parent() ) )
        dcmpPointerBody2_inChest = getDecomposeMatrix( getLocalMatrix( self.ctlBodyRotator2, self.ctlChest.parent() ) )
        dcmpPointerBody1_inHip   = getDecomposeMatrix( getLocalMatrix( self.ctlBodyRotator1, self.ctlHip.parent() ) )
        dcmpPointerBody2_inHip   = getDecomposeMatrix( getLocalMatrix( self.ctlBodyRotator2, self.ctlHip.parent() ) )

        dcmpPointerBody1_inChest.ot >> pointerBody1_inChest.t
        dcmpPointerBody2_inChest.ot >> pointerBody2_inChest.t
        dcmpPointerBody1_inHip.ot >> pointerBody1_inHip.t
        dcmpPointerBody2_inHip.ot >> pointerBody2_inHip.t
        
        blendMtxPointer1 = getBlendTwoMatrixNode( pointerBody1_inChest, pointerBody1_inHip ).setAttr( 'blend', 0.6666 )
        blendMtxPointer2 = getBlendTwoMatrixNode( pointerBody2_inChest, pointerBody2_inHip ).setAttr( 'blend', 0.3333 )
        mmPointer1 = createNode( 'multMatrix' )
        mmPointer2 = createNode( 'multMatrix' )
        blendMtxPointer1.matrixOutput() >> mmPointer1.i[0]
        blendMtxPointer2.matrixOutput() >> mmPointer2.i[0]
        
        pointerBody1.pim >> mmPointer1.i[1]
        pointerBody2.pim >> mmPointer2.i[1]
        
        dcmpPointer1 = getDecomposeMatrix( mmPointer1 )
        dcmpPointer2 = getDecomposeMatrix( mmPointer2 )
        
        dcmpPointer1.ot >> pointerBody1.t
        dcmpPointer2.ot >> pointerBody2.t
        
        dcmpCurvePointer0 = getDecomposeMatrix( getLocalMatrix( self.ctlHip, self.ctlRoot ) )
        dcmpCurvePointer1 = getDecomposeMatrix( getLocalMatrix( pointerBody1, self.ctlRoot ) )
        dcmpCurvePointer2 = getDecomposeMatrix( getLocalMatrix( pointerBody2, self.ctlRoot ) )
        dcmpCurvePointer3 = getDecomposeMatrix( getLocalMatrix( self.ctlChest, self.ctlRoot ) )

        bodyCurve = curve( p=[[0,0,0] for i in range( 4 )] )
        curveShape = bodyCurve.shape()
        dcmpCurvePointer0.ot >> curveShape.attr( 'controlPoints[0]' )
        dcmpCurvePointer1.ot >> curveShape.attr( 'controlPoints[1]' )
        dcmpCurvePointer2.ot >> curveShape.attr( 'controlPoints[2]' )
        dcmpCurvePointer3.ot >> curveShape.attr( 'controlPoints[3]' )
        
        bodyCurve.parentTo( self.ctlRoot ).setTransformDefault()
        self.currentCurve = bodyCurve
    

    def createResultJoints(self, numJoints = 5 ):
        
        jnts = []
        select( self.ctlRoot )
        self.rootJnt = joint().setAttr( 'dla', 1 )
        for i in range( numJoints + 1 ):
            jnt = joint()
            jnt.ty.set( 1.0 );
            jnts.append( jnt )
            jnt.attr( 'displayLocalAxis' ).set( 1 )
        
        self.handle, self.effector = ikHandle( sj=jnts[0], ee=jnts[-1], curve= self.currentCurve, sol='ikSplineSolver',  ccv=False, pcv=False )
        self.handle.parentTo( self.rigBase )
        self.ctlChest.addAttr( ln="stretch", min=0, max=1, dv=0, k=1 )
        
        currentShape = self.currentCurve.shape()
        origShape = self.origCurve.shape()
        
        currentInfos = []
        origInfos = []
        for i in range( numJoints + 1 ):
            currentParam = i / float( numJoints )
            currentInfo = createNode( 'pointOnCurveInfo' ).setAttr( 'top', 1 ).setAttr( 'parameter', currentParam )
            origInfo    = createNode( 'pointOnCurveInfo' ).setAttr( 'top', 1 ).setAttr( 'parameter', currentParam )
            currentShape.attr( 'local' ) >> currentInfo.inputCurve
            origShape.attr( 'local' ) >> origInfo.inputCurve
            currentInfos.append( currentInfo )
            origInfos.append( origInfo )
        
        for i in range( numJoints ):
            distCurrent = createNode( 'distanceBetween' )
            distOrig    = createNode( 'distanceBetween' )
            currentInfos[i].position >> distCurrent.point1
            currentInfos[i+1].position >> distCurrent.point2
            origInfos[i].position >> distOrig.point1
            origInfos[i+1].position >> distOrig.point2
            
            blendNode = createNode( 'blendTwoAttr' )
            distOrig.distance >> blendNode.input[0]
            distCurrent.distance >> blendNode.input[1]
            self.ctlChest.stretch >> blendNode.attributesBlender
            blendNode.output >> jnts[i+1].ty
        
        self.handle.attr( 'dTwistControlEnable' ).set( 1 )
        self.handle.attr( 'dWorldUpType' ).set( 4 )
        self.handle.attr( 'dForwardAxis' ).set( 2 )
        self.handle.attr( 'dWorldUpAxis' ).set( 6 )
        self.handle.attr( 'dWorldUpVector' ).set( 1,0,0 )
        self.handle.attr( 'dWorldUpVectorEnd' ).set( 1,0,0 )
        self.ctlHip.wm   >> self.handle.attr( 'dWorldUpMatrix' )
        self.ctlChest.wm >> self.handle.attr( 'dWorldUpMatrixEnd' )
        
        constrain_rotate( self.ctlChest, jnts[-1] )
        constrain_parent( self.ctlHip, self.rootJnt )
        




class ArmRig:
    
    def __init__(self, stdBase, stdFirst, stdSecond, stdEnd, stdSecondoffset, stdPoleV, stdLookAt ):
        
        self.stdPrefix = 'StdJnt_'
        self.stdBase = convertSg( stdBase )
        self.stdFirst = convertSg( stdFirst )
        self.stdSecond = convertSg( stdSecond )
        self.stdEnd  = convertSg( stdEnd )
        self.stdSecondoffset = convertSg( stdSecondoffset )
        self.stdPoleV = convertSg( stdPoleV )
        self.stdLookAt = convertSg( stdLookAt )
    
    
    
    def createAll(self, controllerSize, numJnt=3 ):
        
        self.controllerSize = controllerSize
        self.createRigBase()
        self.createIkController()
        self.createPoleVController()
        self.createIkJoints()
        self.connectAndParentIk()
        self.createFKController()
        self.createFkJoints()
        self.connectAndParentFk()
        self.createBlController()
        self.connectBlVisibility()
        self.createBlJoints()
        self.connectAndParentBl()
        self.makeCurve()
        self.makeSpJointsUpper(numJnt)
        self.makeSpJointsLower(numJnt)


    def createRigBase(self ):
        
        self.rigBase = createNode( 'transform', n= self.stdFirst.localName().replace( self.stdPrefix, 'RigBase_' ) )
        self.rigBase.xform( ws=1, matrix= self.stdFirst.wm.get() )
        constrain_parent( self.stdFirst, self.rigBase )
    

    
    def createIkController(self ):
        
        self.ctlIkEnd = makeController( sgdata.Controllers.cubePoints, self.controllerSize, typ='joint', n= self.stdEnd.localName().replace( self.stdPrefix, 'Ctl_Ik' ) )
        self.ctlIkEnd.setAttr( 'shape_sx', 0.1 )
        self.ctlIkEnd.setAttr( 'shape_sy', 1.5 )
        self.ctlIkEnd.setAttr( 'shape_sz', 1.5 )
        self.ctlIkEnd.xform( ws=1, matrix= self.stdEnd.wm.get() )
        pCtlIkEnd = makeParent( self.ctlIkEnd )
    
        dcmpStdEnd = getDecomposeMatrix( self.stdEnd )
        composeMatrix = createNode( 'composeMatrix' )
        
        dcmpStdEnd.ot >> composeMatrix.it
        mmLocalEndPos = createNode( 'multMatrix' )
        composeMatrix.outputMatrix >> mmLocalEndPos.i[0]
        self.stdFirst.wim >> mmLocalEndPos.i[1]
        dcmpPCtlIkEnd = getDecomposeMatrix( mmLocalEndPos )
        
        dcmpPCtlIkEnd.ot >> pCtlIkEnd.t
        dcmpPCtlIkEnd.outputRotate >> pCtlIkEnd.r
        
        invCompose = createNode( 'inverseMatrix' )
        composeMatrix.outputMatrix >> invCompose.inputMatrix
        
        mmIkJo = createNode( 'multMatrix' )
        self.stdEnd.wm >> mmIkJo.i[0]
        invCompose.outputMatrix >> mmIkJo.i[1]
        dcmpJo = getDecomposeMatrix( mmIkJo )
        dcmpJo.outputRotate >> self.ctlIkEnd.jo
        
        
        
    def createPoleVController(self ):
        
        self.ctlIkPoleV = makeController( sgdata.Controllers.diamondPoints, self.controllerSize, n= self.stdPoleV.localName().replace( self.stdPrefix, 'Ctl_PoleV' ) )
        self.ctlIkPoleV.setAttr( 'shape_sx', 0.23 )
        self.ctlIkPoleV.setAttr( 'shape_sy', 0.23 )
        self.ctlIkPoleV.setAttr( 'shape_sz', 0.23 )
        makeParent( self.ctlIkPoleV )
        pIkCtlPoleV = self.ctlIkPoleV.parent()
        pIkCtlPoleV.xform( ws=1, matrix = self.stdLookAt.wm.get() )
        self.poleVTwist = makeParent( pIkCtlPoleV, n='Twist_PoleV' + self.stdPoleV.localName().replace( self.stdPrefix, '' ) )
        
        dcmpPoleVStd = getDecomposeMatrix( getLocalMatrix( self.stdPoleV, self.stdLookAt ))
        dcmpPoleVStd.ot >> pIkCtlPoleV.t
        dcmpPoleVStd.outputRotate >> pIkCtlPoleV.r
        
    
    
    
    def createIkJoints(self ):
        
        firstPos = self.stdFirst.xform( q=1, ws=1, matrix=1 )
        secondPos = self.stdSecond.xform( q=1, ws=1, matrix=1 )
        thirdPos  = self.stdEnd.xform( q=1, ws=1, matrix=1 )
        
        cmds.select( d=1 )
        self.ikJntFirst  = joint( n=self.stdFirst.replace( self.stdPrefix, 'IkJnt_' ) ).xform( ws=1, matrix=firstPos )
        self.ikJntSecond = joint( n=self.stdSecond.replace( self.stdPrefix, 'IkJnt_' ) ).xform( ws=1, matrix=secondPos )
        self.ikJntEnd  = joint( n=self.stdEnd.replace( self.stdPrefix, 'IkJnt_' ) ).xform( ws=1, matrix=thirdPos )
        
        self.stdSecond.tx >> self.ikJntSecond.tx
        self.stdEnd.tx >> self.ikJntEnd.tx
        
        secondRotMtx = listToMatrix( self.stdSecond.xform( q=1, os=1, matrix=1 ) )
        rot = OpenMaya.MTransformationMatrix( secondRotMtx ).eulerRotation().asVector()
        self.ikJntSecond.attr( 'preferredAngleY' ).set( math.degrees( rot.y ) )
        self.ikHandle = ikHandle( sj=self.ikJntFirst, ee=self.ikJntEnd, sol='ikRPsolver' )[0]
        self.ikJntFirst.v.set( 0 )
        self.ikHandle.v.set( 0 )
        constrain_rotate( self.ctlIkEnd, self.ikJntEnd )



    def connectAndParentIk(self):
        
        self.ikGroup = createNode( 'transform', n= self.stdFirst.localName().replace( self.stdPrefix, 'IkGrp_' ) )
        
        lookAtChild = makeLookAtChild( self.ctlIkEnd, self.ikGroup, n='LookAt_' + self.ctlIkPoleV.localName().replace( 'Ctl_', '' ) )
        constrain_point( self.ctlIkEnd, self.ikHandle )
        parent( self.poleVTwist, lookAtChild )
        self.poleVTwist.setTransformDefault()
        
        parent( self.ikGroup, self.rigBase )
        self.ikGroup.setTransformDefault()
        
        parent( self.ctlIkEnd.parent(), self.ikGroup )
        parent( self.ikHandle, self.ikGroup )
        parent( self.ikJntFirst, self.ikGroup )
        
        poleVDcmp = getDecomposeMatrix( getLocalMatrix( self.ctlIkPoleV, self.rigBase ) )
        poleVDcmp.ot >> self.ikHandle.attr( 'poleVector' )
    
    
    
    def createFKController( self ):
        
        self.fkCtlFirst = makeController( sgdata.Controllers.rhombusPoints, self.controllerSize, n= self.stdFirst.localName().replace( self.stdPrefix, 'Ctl_Fk' ) )
        self.fkCtlSecond = makeController( sgdata.Controllers.rhombusPoints, self.controllerSize, n= self.stdSecond.localName().replace( self.stdPrefix, 'Ctl_Fk' ) )
        self.fkCtlEnd = makeController( sgdata.Controllers.rhombusPoints, self.controllerSize, n= self.stdEnd.localName().replace( self.stdPrefix, 'Ctl_Fk' ) )
        
        self.fkCtlFirst.xform( ws=1, matrix = self.stdFirst.wm.get() ).setAttr( 'shape_rz', 90 ).setAttr( 'shape_sx', .7 ).setAttr( 'shape_sy', .7 ).setAttr( 'shape_sz', .7 )
        self.fkCtlSecond.xform( ws=1, matrix = self.stdSecond.wm.get() ).setAttr( 'shape_rz', 90 ).setAttr( 'shape_sx', .7 ).setAttr( 'shape_sy', .7 ).setAttr( 'shape_sz', .7 )
        self.fkCtlEnd.xform( ws=1, matrix = self.stdEnd.wm.get() ).setAttr( 'shape_rz', 90 ).setAttr( 'shape_sx', .7 ).setAttr( 'shape_sy', .7 ).setAttr( 'shape_sz', .7 )
        
        makeParent( self.fkCtlFirst )
        makeParent( self.fkCtlSecond )
        makeParent( self.fkCtlEnd )
        parent( self.fkCtlEnd.parent(), self.fkCtlSecond )
        parent( self.fkCtlSecond.parent(), self.fkCtlFirst )
        
        self.stdSecond.tx >> self.fkCtlSecond.parent().tx
        self.stdEnd.tx >> self.fkCtlEnd.parent().tx
        self.stdSecond.r >> self.fkCtlSecond.parent().r
        self.stdEnd.r >> self.fkCtlEnd.parent().r
        
    
    
    def createFkJoints(self ):
        
        firstPos = self.stdFirst.xform( q=1, ws=1, matrix=1 )
        secondPos = self.stdSecond.xform( q=1, ws=1, matrix=1 )
        thirdPos  = self.stdEnd.xform( q=1, ws=1, matrix=1 )
        
        cmds.select( d=1 )
        self.fkJntFirst  = joint( n=self.stdFirst.localName().replace( self.stdPrefix, 'FkJnt_' ) ).xform( ws=1, matrix=firstPos )
        self.fkJntSecond = joint( n=self.stdSecond.localName().replace( self.stdPrefix, 'FkJnt_' ) ).xform( ws=1, matrix=secondPos )
        self.fkJntEnd  = joint( n=self.stdEnd.localName().replace( self.stdPrefix, 'FkJnt_' ) ).xform( ws=1, matrix=thirdPos )
        self.fkJntFirst.v.set( 0 )
        
        
    
    def connectAndParentFk(self):
        
        self.fkGroup = createNode( 'transform', n= self.stdFirst.localName().replace( self.stdPrefix, 'FkGrp_' ) )
        parent( self.fkGroup, self.rigBase )
        self.fkGroup.setTransformDefault()
        
        parent( self.fkCtlFirst.parent(), self.fkGroup )
        
        parent( self.fkJntFirst, self.fkGroup )
        constrain_parent( self.fkCtlFirst, self.fkJntFirst )
        constrain_parent( self.fkCtlSecond, self.fkJntSecond )
        constrain_parent( self.fkCtlEnd, self.fkJntEnd )
    


    def createBlController(self ):
        
        self.ctlBl = makeController( sgdata.Controllers.switchPoints, self.controllerSize, n= self.stdEnd.localName().replace( self.stdPrefix, 'Ctl_Bl' ) )
        pCtlBl = makeParent( self.ctlBl )
        pCtlBl.xform( ws=1, matrix= self.stdEnd.wm.get() )
        
        tyValue = 0.8
        if self.stdEnd.tx.get() < 0:
            tyValue *= -1
        
        self.ctlBl.setAttr( 'shape_sx', 0.3 ).setAttr( 'shape_sy', 0.3 ).setAttr( 'shape_sz', 0.3 ).setAttr( 'shape_ty', tyValue * self.controllerSize )
        self.ctlBl.setTransformDefault()
        keyAttrs = self.ctlBl.listAttr( k=1 )
        for attr in keyAttrs:
            self.ctlBl.attr( attr ).set( e=1, lock=1, k=0 )
    
    
    def connectBlVisibility(self):
        
        addOptionAttribute( self.ctlBl )
        self.ctlBl.addAttr( ln='blend', min=0, max=1, k=1 )
        self.ctlBl.addAttr( ln='ikVis', at='long', min=0, max=1, cb=1 )
        self.ctlBl.addAttr( ln='fkVis', at='long', min=0, max=1, cb=1 )
        
        visIk  = createNode( 'condition' ).setAttr( 'op', 1 ).setAttr( 'colorIfTrueR', 1 ).setAttr( 'colorIfFalseR', 0 ).setAttr( 'secondTerm', 1 )
        visFk  = createNode( 'condition' ).setAttr( 'op', 1 ).setAttr( 'colorIfTrueR', 1 ).setAttr( 'colorIfFalseR', 0 ).setAttr( 'secondTerm', 0 )
        addVisIk = createNode( 'addDoubleLinear' )
        addVisFk = createNode( 'addDoubleLinear' )
        
        self.ctlBl.blend >> visIk.firstTerm
        self.ctlBl.blend >> visFk.firstTerm
        self.ctlBl.ikVis >> addVisIk.input1
        self.ctlBl.fkVis >> addVisFk.input1
        visIk.outColorR >> addVisIk.input2
        visFk.outColorR >> addVisFk.input2
        
        addVisIk.output >> self.ikGroup.attr( 'v' )
        addVisFk.output >> self.fkGroup.attr( 'v' )
    
    
    
    def createBlJoints(self ):
        
        firstPos = self.stdFirst.xform( q=1, ws=1, matrix=1 )
        secondPos = self.stdSecond.xform( q=1, ws=1, matrix=1 )
        thirdPos  = self.stdEnd.xform( q=1, ws=1, matrix=1 )
        
        self.blJntFirst  = joint( n=self.stdFirst.replace( self.stdPrefix, 'BlJnt_' ) ).xform( ws=1, matrix=firstPos )
        self.blJntSecond = joint( n=self.stdSecond.replace( self.stdPrefix, 'BlJnt_' ) ).xform( ws=1, matrix=secondPos )
        self.blJntEnd    = joint( n=self.stdEnd.replace( self.stdPrefix, 'BlJnt_' ) ).xform( ws=1, matrix=thirdPos )
    


    def connectAndParentBl(self):
        
        self.blGroup = createNode( 'transform', n= self.stdFirst.localName().replace( self.stdPrefix, 'BlGrp_' ) )
        
        parent( self.blGroup, self.rigBase )
        self.blGroup.setTransformDefault()
        
        parent( self.blJntFirst, self.blGroup )
        parent( self.ctlBl.parent(), self.blGroup )
        
        constrain_parent( self.blJntEnd, self.ctlBl.parent() )
        
        blendNodeFirst = getBlendTwoMatrixNode( self.ikJntFirst, self.fkJntFirst, local=1 )
        blendNodeSecond = getBlendTwoMatrixNode( self.ikJntSecond, self.fkJntSecond, local=1 )
        blendNodeEnd = getBlendTwoMatrixNode( self.ikJntEnd, self.fkJntEnd, local=1 )
        
        blendNodeFirstDcmp = getDecomposeMatrix( blendNodeFirst )
        blendNodeSecondDcmp = getDecomposeMatrix( blendNodeSecond )
        blendNodeEndDcmp = getDecomposeMatrix( blendNodeEnd )
        
        blendNodeFirstDcmp.ot >> self.blJntFirst.t
        blendNodeFirstDcmp.outputRotate >> self.blJntFirst.r
        blendNodeSecondDcmp.ot >> self.blJntSecond.t
        blendNodeSecondDcmp.outputRotate >> self.blJntSecond.r
        blendNodeEndDcmp.ot >> self.blJntEnd.t
        blendNodeEndDcmp.outputRotate >> self.blJntEnd.r
        
        self.ctlBl.blend >> blendNodeFirst.blend
        self.ctlBl.blend >> blendNodeSecond.blend
        self.ctlBl.blend >> blendNodeEnd.blend
        


    def makeCurve(self):
        
        self.curveUpper = curve( p=[[0,0,0],[0,0,0]], d=1 )
        self.curveLower = curve( p=[[0,0,0],[0,0,0]], d=1 )
        
        upperShape = self.curveUpper.shape()
        lowerShape = self.curveLower.shape()
        
        self.blJntSecond.t >> upperShape.attr( 'controlPoints[1]' )
        self.blJntEnd.t    >> lowerShape.attr( 'controlPoints[1]' )
        
        parent( self.curveUpper, self.blJntFirst )
        parent( self.curveLower, self.blJntSecond )
        self.curveUpper.setTransformDefault()
        self.curveLower.setTransformDefault()


    
    def makeSpJointsUpper(self, numJnt=3 ):
        
        select( d=1 )
        self.upperJnts = [ joint() ]
        for i in range( numJnt ):
            self.upperJnts.append( joint() )
        
        self.handleUpper, effector = ikHandle( sj=self.upperJnts[0], ee=self.upperJnts[-1], sol='ikSplineSolver', ccv=False, pcv=False, curve=self.curveUpper.shape() )
        curveInfo = createNode( 'curveInfo' )
        
        self.curveUpper.shape().attr( 'local' ) >> curveInfo.inputCurve
        multNode = createNode( 'multDoubleLinear' )
        curveInfo.arcLength >> multNode.input1
        
        multValue = 1.0/numJnt
        if self.blJntSecond.tx.get() < 0:
            multValue *= -1
        
        multNode.input2.set( multValue )
        for upperJnt in self.upperJnts[1:]:
            multNode.output >> upperJnt.tx
        pass
    
        self.handleUpper.attr( 'dTwistControlEnable' ).set( 1 )
        self.handleUpper.attr( 'dWorldUpType' ).set( 4 )
        if self.blJntSecond.tx.get() < 0:
            self.handleUpper.attr( 'dForwardAxis' ).set( 1 )
            upObjectStart = makeLookAtChild( self.blJntSecond, self.blGroup, direction=[-1,0,0] )
        else:
            upObjectStart = makeLookAtChild( self.blJntSecond, self.blGroup, direction=[1,0,0] )
        upObjectEnd   = makeChild( upObjectStart )
        blMtx = getBlendTwoMatrixNode( self.blJntSecond, upObjectStart ).setAttr( 'blend', math.fabs( multValue ) )
        mmBl = createNode( 'multMatrix' )
        blMtx.matrixSum >> mmBl.i[0]
        upObjectEnd.pim >> mmBl.i[1]
        dcmpBl = getDecomposeMatrix( mmBl )
        dcmpBl.outputTranslate >> upObjectEnd.t
        dcmpBl.outputRotate >> upObjectEnd.r
        
        upObjectStart.wm >> self.handleUpper.attr( 'dWorldUpMatrix' )
        upObjectEnd.wm   >> self.handleUpper.attr( 'dWorldUpMatrixEnd' )
        
        for jnt in self.upperJnts:
            jnt.attr( 'dla' ).set(1)
        parent( self.handleUpper, self.rigBase )
    


    def makeSpJointsLower(self, numJnt=3 ):
        
        self.upperJnts[-1].v.set( 0 )
        select( self.upperJnts[-2] )
        self.lowerJnts = [ joint() ]
        for i in range( numJnt ):
            self.lowerJnts.append( joint() )
        
        self.handleLower, effector = ikHandle( sj=self.lowerJnts[0], ee=self.lowerJnts[-1], sol='ikSplineSolver', ccv=False, pcv=False, curve=self.curveLower.shape() )
        curveInfo = createNode( 'curveInfo' )
        
        self.curveLower.shape().attr( 'local' ) >> curveInfo.inputCurve
        multNode = createNode( 'multDoubleLinear' )
        curveInfo.arcLength >> multNode.input1
        
        multValue = 1.0/numJnt
        if self.blJntSecond.tx.get() < 0:
            multValue *= -1
        
        multNode.input2.set( multValue )
        for lowerJnt in self.lowerJnts[1:]:
            multNode.output >> lowerJnt.tx
        
        self.handleLower.attr( 'dTwistControlEnable' ).set( 1 )
        self.handleLower.attr( 'dWorldUpType' ).set( 4 )
        upObjectStart = self.blJntSecond
        if self.blJntSecond.tx.get() < 0:
            self.handleLower.attr( 'dForwardAxis' ).set( 1 )
            pUpObjectEnd  = makeLookAtChild( self.blJntSecond, self.blJntEnd, direction=[1,0,0] )
        else:
            pUpObjectEnd  = makeLookAtChild( self.blJntSecond, self.blJntEnd, direction=[-1,0,0] )
        upObjectEnd = makeChild( pUpObjectEnd )
        connectBlendTwoMatrix( pUpObjectEnd, upObjectStart, upObjectEnd, ct=1, cr=1 )
        upObjectEnd.blend.set( multValue )
        
        upObjectStart.wm >> self.handleLower.attr( 'dWorldUpMatrix' )
        upObjectEnd.wm   >> self.handleLower.attr( 'dWorldUpMatrixEnd' )
        
        for jnt in self.lowerJnts:
            jnt.attr( 'dla' ).set(1)
        
        constrain_rotate( self.blJntEnd, self.lowerJnts[-1] )
        parent( self.handleLower, self.rigBase )
    
        




class LegRig( ArmRig ):
    
    def __init__( self, stdBase, stdFirst, stdSecond, stdEnd, stdSecondoffset, stdPoleV, stdLookAt ):
        ArmRig.__init__( self,stdBase, stdFirst, stdSecond, stdEnd, stdSecondoffset, stdPoleV, stdLookAt )
        
    
    def createAll(self, controllerSize, numJnt=3 ):
        
        self.controllerSize = controllerSize
        self.createRigBase()
        self.createIkController()
        self.createPoleVController()
        self.createIkJoints()
        self.connectAndParentIk()
        self.createFKController()
        self.createFkJoints()
        self.connectAndParentFk()
        self.createBlController()
        self.connectBlVisibility()
        self.createBlJoints()
        self.connectAndParentBl()
        self.makeCurve()
        self.makeSpJointsUpper(numJnt)
        self.makeSpJointsLower(numJnt)
    
    
    
    @convertSg_dec
    def createIkFootRig(self, stdToe, stdToeEnd, stdFootPiv, stdToePiv, stdFootInside, stdFootOutside, stdFootEnd ):
        
        self.footIkGrp = createNode( 'transform', n = self.stdEnd.localName().replace( self.stdPrefix, 'RigFootBase_' ) )
        constrain_parent( self.ctlIkEnd, self.footIkGrp )
        
        ctlFoot = makeController( sgdata.Controllers.circlePoints, self.controllerSize, n= self.stdEnd.localName().replace( self.stdPrefix, 'Ctl_FootIk' ) )
        ctlFoot.shape_rz.set( 90 )
        pCtlFoot = makeParent( ctlFoot )
        parent( pCtlFoot, self.footIkGrp )
        
        select( ctlFoot )
        footPivJnt = joint( n= stdFootPiv.localName().replace( self.stdPrefix, 'FootIkJnt_' ) )
        toePivJnt = joint( n= stdToePiv.localName().replace( self.stdPrefix, 'FootIkJnt_' ) )
        footInsideJnt = joint( n= stdFootInside.localName().replace( self.stdPrefix, 'FootIkJnt_' ) )
        footOusideJnt = joint( n= stdFootOutside.localName().replace( self.stdPrefix, 'FootIkJnt_' ) )
        footEndJnt = joint( n= stdFootEnd.localName().replace( self.stdPrefix, 'FootIkJnt_' ) )
        
        stdFootPiv.t >> pCtlFoot.t
        stdFootPiv.r >> pCtlFoot.r
        
        stdToePiv.t >> toePivJnt.t
        stdFootInside.t >> footInsideJnt.t
        stdFootOutside.t >> footOusideJnt.t
        stdFootEnd.t >> footEndJnt.t
        
        addOptionAttribute( ctlFoot )
        ctlFoot.addAttr( 'liftToe', k=1 )
        ctlFoot.addAttr( 'liftHill', k=1 )
        ctlFoot.addAttr( 'ballRot', k=1 )
        ctlFoot.addAttr( 'bank', k=1 )
        
        multMinusLiftToe = createNode( 'multDoubleLinear' ).setAttr( 'input2', -1 )
        ctlFoot.liftToe >> multMinusLiftToe.input1
        
        multMinusLiftToe.output >> footPivJnt.ry
        ctlFoot.liftHill >> footEndJnt.ry
        ctlFoot.ballRot >> toePivJnt.rx
        
        bankIn  = createNode( 'condition' ).setAttr( 'op', 2 ).setAttr( 'colorIfFalseR', 0 )
        bankOut = createNode( 'condition' ).setAttr( 'op', 4 ).setAttr( 'colorIfFalseR', 0 )
        
        multMinuseBank = createNode( 'multDoubleLinear' ).setAttr( 'input2', -1 )
        ctlFoot.bank >> multMinuseBank.input1
        
        multMinuseBank.output >> bankIn.firstTerm
        multMinuseBank.output >> bankOut.firstTerm
        multMinuseBank.output >> bankIn.colorIfTrueR
        multMinuseBank.output >> bankOut.colorIfTrueR
        
        bankIn.outColorR >> footInsideJnt.rz
        bankOut.outColorR >> footOusideJnt.rz

        select( footEndJnt )
        pivToeJnt = joint( n= 'Piv' + stdToe.localName().replace( self.stdPrefix, 'FootIkJnt_' ) )
        toeJnt = joint( n=stdToe.localName().replace( self.stdPrefix, 'FootIkJnt_' ) )
        footToAnkleJnt = joint( n= toeJnt.localName() + '_end' )
        
        localDcmpToeJnt = getDecomposeMatrix( getLocalMatrix( stdToe, stdFootEnd ) )
        localDcmpToeJnt.ot >> toeJnt.t

        worldDcmpToeJnt = getDecomposeMatrix( stdToe )
        worldDcmpToePiv  = getDecomposeMatrix( self.stdEnd )
        composeWorldToe = createNode( 'composeMatrix' )
        worldDcmpToeJnt.ot >> composeWorldToe.it
        worldDcmpToePiv.outputRotate >> composeWorldToe.ir
        invWorldToe = createNode( 'inverseMatrix' )
        composeWorldToe.outputMatrix >> invWorldToe.inputMatrix
        mmLocalStdEnd = createNode( 'multMatrix' )
        self.stdEnd.wm >> mmLocalStdEnd.i[0]
        invWorldToe.outputMatrix >> mmLocalStdEnd.i[1]
        dcmpToeEnd = getDecomposeMatrix( mmLocalStdEnd )
        dcmpToeEnd.ot >> footToAnkleJnt.t
        
        
        ctlToeEnd = makeController( sgdata.Controllers.spherePoints, self.controllerSize, n= self.stdEnd.localName().replace( stdToeEnd.name(), 'Ctl_FootIk' ) )
        ctlToeEnd.setAttr( 'shape_sx', 0.2 ).setAttr( 'shape_sy', 0.2 ).setAttr( 'shape_sz', 0.2 )
        pCtlToeEnd = makeParent( ctlToeEnd )
        parent( pCtlToeEnd, ctlFoot )
        constrain_parent( footEndJnt, pCtlToeEnd )
        ctlToeEnd.r >> pivToeJnt.r
        
        ctlToe = makeController( sgdata.Controllers.circlePoints, self.controllerSize, n= self.stdEnd.localName().replace( stdToeEnd.name(), 'Ctl_FootIk' ) )
        ctlToe.setAttr( 'shape_sx', 0.5 ).setAttr( 'shape_sy', 0.2 ).setAttr( 'shape_sz', 0.15 ).setAttr( 'shape_ry', 15 ).setAttr( 'shape_tx', 0.3 * self.controllerSize )
        ctlToe.setAttr( 'shape_rz', 90 )
        pCtlToe = makeParent( ctlToe )
        parent( pCtlToe, ctlToeEnd )
        pCtlToe.setTransformDefault()
        localDcmpToeJnt.ot >> pCtlToe.t
        ctlToe.r >> toeJnt.r
    
    



