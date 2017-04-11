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




def getDirection( inputVector ):
    
    return [ [1,0,0], [0,1,0], [0,0,1], [-1,0,0], [0,-1,0], [0,0,-1] ][getDirectionIndex( inputVector )]


    
    
    
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
        getValue = cmds.getAttr( self.name() )
        if type( getValue ) == list and len( getValue ) == 1:
            return getValue[0]
        return getValue
    
    
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
        origName = self.name()
        resultName = cmds.rename( self.name(), inputName )
        #print "rename : ", origName, "-->", resultName
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
        try:cmds.setAttr( self.name() + '.' + attrName, *values, **options )
        except:pass
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
        elif self.nodeType() in ['multMatrix', 'wtAddMatrix', 'addMatrix']:
            return self.attr( 'matrixSum' )
        elif self.nodeType() in ['fourByFourMatrix']:
            return self.attr( 'output' )
        elif self.nodeType() in ['transform', 'joint']:
            return self.attr( 'wm' )
    
    
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
    
    
    def getMMatrix(self, attrName = 'wm' ):
        return listToMatrix( self.attr( attrName ).get() )
    
    
        
        


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
        
        name = self.localName() + addName
        if options.has_key( 'replaceName' ):
            name = self.localName().replace( *options['replaceName'] )
            
        childNode = SGTransformNode( cmds.createNode( 'transform', n=name ) )
        cmds.parent( childNode.name(), self.name() )[0]
        childNode.setTransformDefault()
        return childNode



    def setTransformDefault(self):
        self.setAttr( 'tx', 0 ).setAttr( 'ty', 0 ).setAttr( 'tz', 0 )
        self.setAttr( 'rx', 0 ).setAttr( 'ry', 0 ).setAttr( 'rz', 0 )
        self.setAttr( 'sx', 1 ).setAttr( 'sy', 1 ).setAttr( 'sz', 1 )
        self.setAttr( 'shxy', 0 ).setAttr( 'shxz', 0 ).setAttr( 'shyz', 0 )
        if self.nodeType() == 'joint':
            self.jo.set( 0,0,0 )
        return self
    


    def parentTo(self, target ):
        cmds.parent( self.name(), self.convertName( target ) )[0]
        return self
    


    def getPivotMatrix( self ):
        piv = OpenMaya.MPoint( *self.attr( 'rotatePivot' ).get() )
        mtxList = matrixToList( OpenMaya.MMatrix() )
        mtxList[ 12 ] = piv.x
        mtxList[ 13 ] = piv.y
        mtxList[ 14 ] = piv.z
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
    
    localTarget.matrixOutput() >> multMatrixNode.i[0]
    parentTarget.wim >> multMatrixNode.i[1]
    
    return multMatrixNode




@convertSg_dec
def getLocalMatrix( localTarget, parentTarget ):
    
    multMatrixNodes = localTarget.matrixOutput().listConnections( d=1, s=0, type='multMatrix' )
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
    if node.nodeType() in ['transform', 'joint' ]:
        node.t >> distNode.point1
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
def getLookAtAngleNode( lookTarget, rotTarget, **options ):

    def getLookAtMatrixNode( lookTarget, rotTarget ):
    
        consLookTarget = lookTarget.wm.listConnections( type="multMatrix", p=1 )
        return createLookAtMatrix( lookTarget, rotTarget )
    
    if options.has_key( 'direction' ) and options['direction']:
        direction = options['direction']
    else:
        direction = [1,0,0]
    
    lookTarget = convertSg( lookTarget )
    rotTarget = convertSg( rotTarget )
    
    dcmpLookAt = getDecomposeMatrix( getLookAtMatrixNode( lookTarget, rotTarget ) )
    
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
        if pRotTarget:
            wim = listToMatrix( pRotTarget.wim.get() )
        else:
            wim = OpenMaya.MMatrix()
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

    if options.has_key( 'local' ):
        blendNode = createBlendTwoMatrixNode( first, second, local='local' )
        dcmp = getDecomposeMatrix( blendNode )
    else:
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
        value = connectedAttrs[i].node().attr( 'vector1' ).get()
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
def setSymmetryToOther( src, trg ):
    
    matList = src.wm.get()
    matList[1]  *= -1
    matList[2]  *= -1
    matList[4]  *= -1
    matList[8]  *= -1
    matList[12] *= -1
    
    if trg.nodeType() == 'joint':
        trg.xform( ws=1, matrix = matList )
        worldMatrix = listToMatrix( matList )
        joValue = trg.attr( 'jo' ).get()
        joRadValue = [ math.radians( joValue[0]), math.radians( joValue[1]), math.radians( joValue[2]) ]
        joMtx = OpenMaya.MEulerRotation( OpenMaya.MVector( *joRadValue ) ).asMatrix()
        pMtx = listToMatrix( trg.attr( 'pm' ).get() )
        localRotMtx = worldMatrix * pMtx.inverse() * joMtx.inverse()
        trMtx = OpenMaya.MTransformationMatrix( localRotMtx )
        rotValue = trMtx.eulerRotation().asVector()
        rotDegValue = [ math.degrees( rotValue[0] ), math.degrees( rotValue[1] ), math.degrees( rotValue[2] ) ]
        #print 'rot deg value : ', rotDegValue
        trg.r.set( *rotDegValue )
    else:
        trg.xform( ws=1, matrix= matList )

    



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
def getLookAtMatrixValue( aimTarget, rotTarget, **options ):
    
    rotWorldMatrix = listToMatrix( rotTarget.wm.get() )
    aimWorldMatrix = listToMatrix( aimTarget.wm.get() )
    localAimTarget = aimWorldMatrix * rotWorldMatrix.inverse()
    localAimPos    = OpenMaya.MPoint( localAimTarget[3] )
    direction = OpenMaya.MVector( localAimPos ).normal()
    
    directionIndex = getDirectionIndex( direction )
    
    baseDir = None
    if options.has_key( 'direction' ):
        baseDir = OpenMaya.MVector( *options[ 'direction' ] ).normal()
    
    if not baseDir:
        baseDir = [[1,0,0], [0,1,0], [0,0,1], [-1,0,0], [0,-1,0], [0,0,-1]][directionIndex]
    
    baseDir = OpenMaya.MVector( *baseDir )
    direction = OpenMaya.MVector( *direction )
    localAngle = baseDir.rotateTo( direction ).asMatrix()
    
    rotResultMatrix = localAngle * rotWorldMatrix
    return rotResultMatrix



def getRotateFromMatrix( mtxValue ):
    
    if type( mtxValue ) == list:
        mtxValue = listToMatrix( mtxValue )
    
    trMtx = OpenMaya.MTransformationMatrix( mtxValue )
    rotVector = trMtx.eulerRotation().asVector()
    
    return math.degrees(rotVector.x), math.degrees(rotVector.y), math.degrees(rotVector.z)





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
            vector1Value = src.vector1.get()
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



def getBBC( target ):
    
    bbmin = cmds.getAttr( target + '.boundingBoxMin' )[0]
    bbmax = cmds.getAttr( target + '.boundingBoxMax' )[0]
    
    bbcenter = []
    for i in range( 3 ):
        bbcenter.append( (bbmin[i] + bbmax[i])/2.0 )
    return bbcenter





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



def putObject( putTarget, typ='joint', putType='' ):
    
    if typ == 'locator':
        newObj = cmds.spaceLocator()[0]
    elif typ == 'null':
        newObj = cmds.createNode( 'transform' )
        cmds.setAttr( newObj + '.dh', 1 )
    else:
        newObj = cmds.createNode( typ )
    
    if type( putTarget ) in [list, tuple]:
        center = getCenter( putTarget )
        cmds.move( center.x, center.y, center.z, newObj, ws=1 )
    else:
        mtx = cmds.getAttr( putTarget + '.wm' )
        cmds.xform( newObj, ws=1, matrix= mtx )
    
    return newObj



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
        
    
    crv = curve( **options )
    crvShape = crv.shape()
    
    if options.has_key( 'n' ):
        name = options['n']
    elif options.has_key( 'name' ):
        name = options['name']
    else:
        name = None
    
    jnt = createNode( typ )
    if name:
        if mp:
            makeParent( jnt ).rename( 'P' + name )
        jnt.rename( name )

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
    jnt.addAttr( ln='scaleMult', dv=defaultScaleMult, cb=1, min=0 )
    composeMatrix = createNode( 'composeMatrix' )
    composeMatrix2 = createNode( 'composeMatrix' )
    multMatrix = createNode( 'multMatrix' )
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
    trGeo = createNode( 'transformGeometry' )
    jnt.attr( 'radius' ).set( 0 )
    
    ioShape.outputGeometry() >> trGeo.inputGeometry
    multMatrix.matrixSum >> trGeo.transform
    
    trGeo.outputGeometry >> crvShape.create
    
    if colorIndex != -1:
        shape = jnt.shape().name()
        cmds.setAttr( shape + '.overrideEnabled', 1 )
        cmds.setAttr( shape + '.overrideColor', colorIndex )

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
    
    return curve




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
        pivMatrix = convertSg( nodeName ).getPivotMatrix() * convertSg( nodeName ).getWorldMatrix()
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
        pivMatrix   = sourceParent[0].sgtransform.getPivotMatrix() * sourceParent[0].sgtransform.getWorldMatrix()
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
            dstMatrix = srcLocalMtx * target.parent()[0].sgtransform.getPivotMatrix() * target.parent()[0].sgtransform.getWorldMatrix()

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




def addOptionAttribute( target, enumName = "Options" ):
    
    target = convertSg( target )
    
    barString = '____'
    while target.attributeQuery( barString, ex=1 ):
        barString += '_'
    
    target.addAttr( ln=barString,  at="enum", en="%s:" % enumName, cb=1 )





def getUVAtPoint( point, mesh ):
    
    if type( point ) in [ type([]), type(()) ]:
        point = OpenMaya.MPoint( *point )
    
    meshShape = convertSg( mesh ).shape().name()
    fnMesh = OpenMaya.MFnMesh( getDagPath( meshShape ) )
    
    util = OpenMaya.MScriptUtil()
    util.createFromList( [0.0,0.0], 2 )
    uvPoint = util.asFloat2Ptr()
    fnMesh.getUVAtPoint( point, uvPoint, OpenMaya.MSpace.kWorld )
    u = OpenMaya.MScriptUtil.getFloat2ArrayItem( uvPoint, 0, 0 )
    v = OpenMaya.MScriptUtil.getFloat2ArrayItem( uvPoint, 0, 1 )
    
    return u, v
    
    
    

def createFollicleOnVertex( vertexName, ct= True, cr= True ):
    
    vtxPos = cmds.xform( vertexName, q=1, ws=1, t=1 )
    mesh = vertexName.split( '.' )[0]
    meshShape = pymel.core.ls( mesh )[0].getShape().name()
    u, v = getUVAtPoint( vtxPos, mesh )
    
    follicleNode = cmds.createNode( 'follicle' )
    follicle = cmds.listRelatives( follicleNode, p=1, f=1 )[0]
    
    cmds.connectAttr( meshShape+'.outMesh', follicleNode+'.inputMesh' )
    cmds.connectAttr( meshShape+'.wm', follicleNode+'.inputWorldMatrix' )
    
    cmds.setAttr( follicleNode+'.parameterU', u )
    cmds.setAttr( follicleNode+'.parameterV', v )
    
    if ct: cmds.connectAttr( follicleNode+'.outTranslate', follicle+'.t' )
    if cr: cmds.connectAttr( follicleNode+'.outRotate', follicle+'.r' )
    
    return follicle





def createFollicleOnClosestPoint( targetObj, mesh ):
        
    vtxPos = cmds.xform( targetObj, q=1, ws=1, t=1 )
    meshShape = convertSg( mesh ).shape().name()
    u, v = getUVAtPoint( vtxPos, mesh )
    
    follicleNode = cmds.createNode( 'follicle' )
    follicle = cmds.listRelatives( follicleNode, p=1, f=1 )[0]
    
    cmds.connectAttr( meshShape+'.outMesh', follicleNode+'.inputMesh' )
    cmds.connectAttr( meshShape+'.wm', follicleNode+'.inputWorldMatrix' )
    
    cmds.setAttr( follicleNode+'.parameterU', u )
    cmds.setAttr( follicleNode+'.parameterV', v )
    
    cmds.connectAttr( follicleNode+'.outTranslate', follicle+'.t' )
    cmds.connectAttr( follicleNode+'.outRotate', follicle+'.r' )






def getMeshAndIndicesPoints( selObjects ):
    
    selObjects = cmds.ls( cmds.polyListComponentConversion( selObjects, tv=1 ), fl=1 )
    
    mesh = ''
    vtxIndices = []
    for obj in selObjects:
        splits = obj.split( '.' )
        if len( splits ) == 1:
            mesh = obj
        else:
            mesh = splits[0]
            index = int( splits[1].split( '[' )[-1].replace( ']', '' ) )
            vtxIndices.append( index )
    
    if vtxIndices:
        vtxIndices = list( set( vtxIndices ) )
    else:
        vtxIndices = [ i for i in range( OpenMaya.MFnMesh( getDagPath( mesh ) ).numVertices() ) ]
    
    return mesh, vtxIndices



def getNodeFromHistory( target, nodeType ):
    
    pmTarget = pymel.core.ls( target )[0]
    hists = pmTarget.history( pdo=1 )
    targetNodes = []
    for hist in hists:
        if hist.type() == nodeType:
            targetNodes.append( hist.name() )
    return targetNodes



def getInfluenceAndWeightList( mesh, vertices = [] ):

    skinClusters = getNodeFromHistory( mesh, 'skinCluster' )
    if not skinClusters: return None
    
    skinCluster = skinClusters[0]
    print "skincluster : ", skinCluster
    
    fnSkinCluster = OpenMaya.MFnDependencyNode( getMObject( skinCluster ) )
    plugWeightList = fnSkinCluster.findPlug( 'weightList' )
    
    if not vertices: vertices = [ i for i in range( plugWeightList.numElements() ) ]
    influenceAndWeightList = [ [] for i in range( len( vertices ) ) ]
    phygicalMap = [ 0 for i in range( plugWeightList.numElements() ) ]
    
    for i in range( len( vertices ) ):
        logicalIndex = vertices[i]
        plugWeights = plugWeightList[ logicalIndex ].child( 0 )
        influenceNums = []
        values = []
        for j in range( plugWeights.numElements() ):
            influenceNum = plugWeights[j].logicalIndex()
            value = plugWeights[j].asFloat()
            influenceNums.append( influenceNum )
            values.append( value )
        
        influenceAndWeightList[i] = [ influenceNums, values ]
        phygicalMap[ logicalIndex ] = i
        
    return influenceAndWeightList, phygicalMap




def getMeshLocalPoints( mesh ):
    
    fnMesh = OpenMaya.MFnMesh( getDagPath( mesh ) )
    points = OpenMaya.MPointArray()
    fnMesh.getPoints( points )
    return points




def createRivetBasedOnSkinWeights( selectedObjs ):
    
    def getPlugMatrix( mesh ):
        skinCluster = getNodeFromHistory( mesh, 'skinCluster' )
        if not skinCluster: return None
        skinCluster = skinCluster[0]
        fnSkinCluster = OpenMaya.MFnDependencyNode( getMObject( skinCluster ) )
        
        return fnSkinCluster.findPlug( 'matrix' )
    
    def getPlugBindPre( mesh ):
    
        skinCluster = getNodeFromHistory( mesh, 'skinCluster' )
        if not skinCluster: return None
        skinCluster = skinCluster[0]
        fnSkinCluster = OpenMaya.MFnDependencyNode( getMObject( skinCluster ) )
        
        return fnSkinCluster.findPlug( 'bindPreMatrix' )
    
    
    def getJointMultMatrix( jnt, mtxBindPre ):
        cons = cmds.listConnections( jnt+'.wm', type='multMatrix' )

        if cons:
            for con in cons:
                if cmds.attributeQuery( 'skinWeightInfluenceMatrix', node=con, ex=1 ):
                    if mtxBindPre == cmds.getAttr( con+'.i[0]' ):
                        return con
        
        mmtxNode = cmds.createNode( 'multMatrix' )
        cmds.setAttr( mmtxNode+'.i[0]', mtxBindPre, type='matrix' )
        cmds.connectAttr( jnt+'.wm', mmtxNode+'.i[1]' )
        
        cmds.addAttr( mmtxNode, ln='skinWeightInfluenceMatrix', at='message' )
        
        return mmtxNode


    mesh, vtxIndices = getMeshAndIndicesPoints( selectedObjs )
    
    skinClusterNode = getNodeFromHistory( mesh, 'skinCluster' )
    if not skinClusterNode: return None
    skinClusterNode = skinClusterNode[0]
    
    influenceAndWeightList, phygicalMap = getInfluenceAndWeightList( mesh, vtxIndices )
    
    meshMatrix = getDagPath( mesh ).inclusiveMatrix()
    meshPoints = getMeshLocalPoints( mesh )
    plugMatrix = getPlugMatrix( mesh )
    plugBindPre = getPlugBindPre( mesh )
    
    BB = OpenMaya.MBoundingBox()
    
    wtAddMtx = cmds.createNode( 'wtAddMatrix' )
    mtxPlugIndidcesAndWeights = {}
    allWeights = 0.0
    for i in vtxIndices:
        influenceList, weights = influenceAndWeightList[ phygicalMap[i] ]
        
        for j in range( len( influenceList ) ):
            mtxPlugIndex = influenceList[j]
            if mtxPlugIndex in mtxPlugIndidcesAndWeights.keys():
                mtxPlugIndidcesAndWeights[mtxPlugIndex] += weights[j]
            else:
                mtxPlugIndidcesAndWeights.update( {mtxPlugIndex:weights[j]} )
            allWeights += weights[j]
        BB.expand( meshPoints[i] )
    worldPoint = BB.center()*meshMatrix
    
    items = mtxPlugIndidcesAndWeights.items()
    for i in range( len( items ) ):
        influence, weight = items[i]
        
        plugMatrixElement = plugMatrix.elementByLogicalIndex( influence )
        plugBindPreElement = plugBindPre.elementByLogicalIndex( influence )
        
        jnt = cmds.listConnections( plugMatrixElement.name(), s=1, d=0, type='joint' )[0]
        mtxBindPre = cmds.getAttr( plugBindPreElement.name() )
        mmtxNode = getJointMultMatrix( jnt, mtxBindPre )
        cmds.connectAttr( mmtxNode+'.o', wtAddMtx+'.i[%d].m' % i )
        cmds.setAttr( wtAddMtx+'.i[%d].w' % i, weight/allWeights )
    
    origObj = cmds.createNode( 'transform', n='OrigObject' )
    destObj = cmds.createNode( 'transform', n='destObject' )
    cmds.setAttr( destObj+'.dh' , 1 )
    cmds.setAttr( destObj+'.dla', 1 )
    mmNode = cmds.createNode( 'multMatrix' )
    dcmp = cmds.createNode( 'decomposeMatrix' )
    mtxWtAdd = cmds.getAttr( wtAddMtx+'.o' )
    
    cmds.connectAttr( origObj+'.wm', mmNode+'.i[0]' )
    cmds.connectAttr( wtAddMtx+'.o', mmNode+'.i[1]' )
    cmds.connectAttr( destObj+'.pim', mmNode+'.i[2]' )
    
    cmds.connectAttr( mmNode+'.o', dcmp+'.imat' )
    
    cmds.connectAttr( dcmp+'.ot', destObj+'.t' )
    cmds.connectAttr( dcmp+'.or', destObj+'.r' )
    
    mmtxWtAdd = listToMatrix( mtxWtAdd )
    worldPoint *= mmtxWtAdd.inverse()
    cmds.setAttr( origObj+'.t', worldPoint.x, worldPoint.y, worldPoint.z )



def getCloseSurfaceNode( target, surface ):
    
    surfShape = cmds.listRelatives( surface, s=1 )[0]
    
    closeNode = cmds.createNode( 'closestPointOnSurface' )
    dcmp = cmds.createNode( 'decomposeMatrix' )
    
    cmds.connectAttr( target+'.wm', dcmp+'.imat' )
    cmds.connectAttr( dcmp+'.ot', closeNode+'.inPosition' )
    cmds.connectAttr( surfShape+'.worldSpace', closeNode+'.inputSurface' )
    
    print closeNode
    return closeNode



def getPointOnSurfaceNode( target, surface, keepClose=False ):
    
    surfShape = cmds.listRelatives( surface, s=1 )[0]
    
    node = cmds.createNode( 'pointOnSurfaceInfo' )
    cmds.connectAttr( surfShape+'.local', node+'.inputSurface' )
    
    closeNode = getCloseSurfaceNode( target, surface )
    
    if not keepClose:
        cmds.setAttr( node+'.u', cmds.getAttr( closeNode+'.u' ) )
        cmds.setAttr( node+'.v', cmds.getAttr( closeNode+'.v' ) )
        cmds.delete( closeNode )
    else:
        cmds.connectAttr( closeNode+'.u', node+'.u' )
        cmds.connectAttr( closeNode+'.v', node+'.v' )
    
    return node


def createTransformOnSurface( target, surface, keepClose=False ):
    
    pointOnSurfNode = getPointOnSurfaceNode( target, surface, keepClose )
    
    tr = cmds.createNode( 'transform', n='P'+target )
    fbfMtx = cmds.createNode( 'fourByFourMatrix' )
    dcmp   = cmds.createNode( 'decomposeMatrix' )
    vectorNode = cmds.createNode( 'vectorProduct' )
    cmds.setAttr( vectorNode+'.op', 2 )
    cmds.connectAttr( pointOnSurfNode+'.tu', vectorNode+'.input1' )
    cmds.connectAttr( pointOnSurfNode+'.n', vectorNode+'.input2' )
    cmds.connectAttr( vectorNode+'.outputX', fbfMtx+'.i00' )
    cmds.connectAttr( vectorNode+'.outputY', fbfMtx+'.i01' )
    cmds.connectAttr( vectorNode+'.outputZ', fbfMtx+'.i02' )
    cmds.connectAttr( pointOnSurfNode+'.px', fbfMtx+'.i30' )
    cmds.connectAttr( pointOnSurfNode+'.py', fbfMtx+'.i31' )
    cmds.connectAttr( pointOnSurfNode+'.pz', fbfMtx+'.i32' )
    cmds.connectAttr( pointOnSurfNode+'.nx', fbfMtx+'.i10' )
    cmds.connectAttr( pointOnSurfNode+'.ny', fbfMtx+'.i11' )
    cmds.connectAttr( pointOnSurfNode+'.nz', fbfMtx+'.i12' )
    cmds.connectAttr( pointOnSurfNode+'.position', tr+'.t' )
    cmds.connectAttr( fbfMtx+'.output', dcmp+'.imat' )
    cmds.connectAttr( dcmp+'.or', tr+'.r' )
    
    cmds.setAttr( tr+'.dh', 1 )
    cmds.setAttr( tr+'.dla', 1 )
    
    return tr


def setBindPreToJntP( sels ):
    
    for sel in sels:
        cons = cmds.listConnections( sel+'.wm', d=1, s=0, p=1, c=1, type='skinCluster' )
        selP = cmds.listRelatives( sel, p=1 )[0]
        
        inputCons = cons[1::2]
        
        for inputCon in inputCons:
            bindPreAttr = inputCon.replace( 'matrix[', 'bindPreMatrix[' )
            cmds.connectAttr( selP+'.wim', bindPreAttr )




def getMDagPathAndComponent():
    
    mSelList = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList( mSelList )
    
    returnTargets = []
    for i in range( mSelList.length() ):
        mDagPath = OpenMaya.MDagPath()
        mObject  = OpenMaya.MObject()
        
        mSelList.getDagPath( i, mDagPath, mObject )
        
        mIntArrU = OpenMaya.MIntArray()
        mIntArrV = OpenMaya.MIntArray()
        mIntArrW = OpenMaya.MIntArray()
        
        if not mObject.isNull():
            if mDagPath.apiType() == OpenMaya.MFn.kNurbsCurve:
                component = OpenMaya.MFnSingleIndexedComponent( mObject )
                component.getElements( mIntArrU )
            elif mDagPath.apiType() == OpenMaya.MFn.kNurbsSurface:
                component = OpenMaya.MFnDoubleIndexedComponent( mObject )
                component.getElements( mIntArrU, mIntArrV )
            elif mDagPath.apiType() == OpenMaya.MFn.kLattice:
                component = OpenMaya.MFnTripleIndexedComponent( mObject )
                component.getElements( mIntArrU, mIntArrV, mIntArrW )
            elif mObject.apiType() == OpenMaya.MFn.kMeshVertComponent:
                component = OpenMaya.MFnSingleIndexedComponent( mObject )
                component.getElements( mIntArrU )
            elif mObject.apiType() == OpenMaya.MFn.kMeshEdgeComponent:
                mfnMesh = OpenMaya.MFnMesh( mDagPath )
                component = OpenMaya.MFnSingleIndexedComponent( mObject )
                mIntArr = OpenMaya.MIntArray()
                component.getElements( mIntArr )
                mIntArrU.setLength( mIntArr.length() * 2 )
                util = OpenMaya.MScriptUtil()
                util.createFromList([0,0],2)
                ptrEdgeToVtxIndex = util.asInt2Ptr()
                for i in range( mIntArr.length() ):
                    mfnMesh.getEdgeVertices( mIntArr[i], ptrEdgeToVtxIndex )
                    index1 = util.getInt2ArrayItem( ptrEdgeToVtxIndex, 0, 0 )
                    index2 = util.getInt2ArrayItem( ptrEdgeToVtxIndex, 0, 1 )
                    mIntArrU[i*2  ] = index1
                    mIntArrU[i*2+1] = index2 
            elif mObject.apiType() == OpenMaya.MFn.kMeshPolygonComponent:
                mfnMesh = OpenMaya.MFnMesh( mDagPath )
                component = OpenMaya.MFnSingleIndexedComponent( mObject )
                mIntArr = OpenMaya.MIntArray()
                component.getElements( mIntArr )
                mIntArrEach = OpenMaya.MIntArray()
                for i in range( mIntArr.length() ):
                    mfnMesh.getPolygonVertices( mIntArr[i], mIntArrEach )
                    for i in range( mIntArrEach.length() ):
                        mIntArrU.append( mIntArrEach[i] )
        
        returnTargets.append( [mDagPath, mIntArrU, mIntArrV, mIntArrW] )
    
    return returnTargets





def weightHammerCurve( targets ):
    import maya.OpenMaya as om
    
    def getWeights( plug ):
        childPlug = plug.child(0)
        numElements = childPlug.numElements()
        indicesAndValues = []
        for i in range( numElements ):
            logicalIndex = childPlug[i].logicalIndex()
            value        = childPlug[i].asFloat()
            indicesAndValues.append( [ logicalIndex, value ] )
        return indicesAndValues
    
    def getMixWeights( first, second, rate ):
        
        invRate = 1.0-rate
        
        print first
        print second
        
        firstMaxIndex = first[-1][0]
        secondMaxIndex = second[-1][0]
        maxIndex = firstMaxIndex+1
        
        if firstMaxIndex < secondMaxIndex:
            maxIndex = secondMaxIndex+1
        
        firstLogicalMap  = [ False for i in range( maxIndex ) ]
        secondLogicalMap = [ False for i in range( maxIndex ) ]
        
        for index, value in first:
            firstLogicalMap[ index ] = True
            
        for index, value in second:
            secondLogicalMap[ index ] = True
        
        returnTargets = []
        
        for index, value in first:
            returnTargets.append( [index, invRate * value] )
        for index, value in second:
            if firstLogicalMap[ index ]:
                for i in range( len( returnTargets ) ):
                    wIndex = returnTargets[i][0]
                    if wIndex == index:
                        returnTargets[i][1] += rate * value
                        break
            else:
                returnTargets.append( [index, rate * value] )
        return returnTargets
    
    def clearArray( targetPlug ):
        plugChild = targetPlug.child( 0 )
        targetInstances = []
        for i in range( plugChild.numElements() ):
            targetInstances.append( plugChild[i].name() )
        targetInstances.reverse()
        for i in range( len( targetInstances ) ):
            cmds.removeMultiInstance( targetInstances[i] )
        
    
    node = targets[0].split( '.' )[0]
    
    skinClusterNodes = getNodeFromHistory( node, 'skinCluster' )
    if not skinClusterNodes: return None
    
    fnSkinCluster = OpenMaya.MFnDependencyNode( getMObject( skinClusterNodes[0] ) )
    plugWeightList = fnSkinCluster.findPlug( 'weightList' )
    
    cmds.select( targets )
    for dagPath, uArr, vArr, wArr in getMDagPathAndComponent():
        
        fnCurve = OpenMaya.MFnNurbsCurve( dagPath )
        startNum = 0
        lastNum = fnCurve.numCVs()-1
        
        if uArr[-1] == lastNum:
            pass
        elif uArr[0] == startNum:
            pass
        elif uArr[0] == startNum and uArr[-1] == lastNum:
            pass
        else:
            weightStart = getWeights( plugWeightList[ uArr[0]-1 ] )
            weightEnd   = getWeights( plugWeightList[ uArr[-1]+1 ] )
            
            length = uArr.length()
            for i in range( uArr.length() ):
                clearArray( plugWeightList[ uArr[i] ] )
                plugWeightListEmelent = plugWeightList.elementByLogicalIndex( uArr[i] )
                
                rate = float( i+1 ) / (length+2)
                weights = getMixWeights( weightStart, weightEnd, rate )
                for index, value in weights:
                    targetPlug = plugWeightListEmelent.child(0).elementByLogicalIndex( index )
                    cmds.setAttr( targetPlug.name(), value )
        cmds.skinPercent( skinClusterNodes[0], normalize=1 )



def setSkinWeightOnlyVertices( selVertices ):
    
    for dagPath, vtxIds in getSelectedVertices( selVertices ):
        fnNode = OpenMaya.MFnDagNode( dagPath )
        mesh = cmds.ls( fnNode.partialPathName() )[0]
        hists = cmds.listHistory( mesh, pdo=1 )
        
        skinNode = ''
        for hist in hists:
            if cmds.nodeType( hist ) == 'skinCluster':
                skinNode = OpenMaya.MFnDependencyNode( getMObject( hist ) )
                break
        
        if not skinNode: continue
        
        weightListPlug = skinNode.findPlug( 'weightList' )
        
        for i in range( vtxIds.length() ):
            vtxId = vtxIds[i]
            weightsPlug = weightListPlug[vtxId].child( 0 )
            
            largeInfluence = 0.0
            largeIndex = -1
            for j in range( weightsPlug.numElements() ):
                weight = weightsPlug[j].asFloat()
                if weight > largeInfluence:
                    largeInfluence = weight
                    largeIndex = j
            
            if largeIndex == -1: continue
            
            targetMatrixIndex = -1
            for j in range( weightsPlug.numElements() ):
                if j == largeIndex:
                    cmds.setAttr( weightsPlug[j].name(), 1 )
                    targetMatrixIndex = weightsPlug[j].logicalIndex()
                else:
                    cmds.setAttr( weightsPlug[j].name(), 0 )
            
            if targetMatrixIndex == -1: continue
            
            for k in range( weightListPlug.numElements() ):
                if vtxId == k: continue
                weightsPlug = weightListPlug[k].child(0)
                for m in range( weightsPlug.numElements() ):
                    if targetMatrixIndex != weightsPlug[m].logicalIndex(): continue
                    cmds.setAttr( weightsPlug[m].name(), 0 )

    cmds.refresh()
    cmds.skinPercent( skinNode.name(), normalize=1 )





class Std:
    
    base     = 'StdJnt_Base'
    root     = 'StdJnt_Root'
    back01   = 'StdJnt_Back01'
    back02   = 'StdJnt_Back02'
    chest    = 'StdJnt_Chest'
    neck     = 'StdJnt_Neck'
    head     = 'StdJnt_Head'
    headEnd  = 'StdJnt_HeadEnd'
    
    clavicle_SIDE_ = 'StdJnt_clavicle_SIDE_'
    arm_SIDE_00 = 'StdJnt_Arm_SIDE_00'
    arm_SIDE_01 = 'StdJnt_Arm_SIDE_01'
    arm_SIDE_02 = 'StdJnt_Arm_SIDE_02'
    arm_SIDE_poleV = 'StdJnt_Arm_SIDE_PoleV'
    arm_SIDE_01_Offset = 'StdJnt_Arm_SIDE_01_Offset'
    arm_SIDE_lookAt = 'LookAtStdjnt_Arm_SIDE_00'
    fingers_SIDE_ = 'StdJnt_%s_SIDE_*'
    
    leg_SIDE_00   = 'StdJnt_Leg_SIDE_00'
    leg_SIDE_01   = 'StdJnt_Leg_SIDE_01'
    leg_SIDE_02   = 'StdJnt_Leg_SIDE_02'
    leg_SIDE_poleV = 'StdJnt_Leg_SIDE_PoleV'
    leg_SIDE_01_Offset = 'StdJnt_Leg_SIDE_01_Offset'
    leg_SIDE_lookAt = 'LookAtStdJnt_Leg_SIDE_00'
    foot_SIDE_Piv = 'StdJnt_Foot_SIDE_Piv'
    foot_SIDE_ToePiv = 'StdJnt_Foot_SIDE_ToePiv'
    foot_SIDE_inside = 'StdJnt_Foot_SIDE_Inside'
    foot_SIDE_outside = 'StdJnt_Foot_SIDE_Outside'
    foot_SIDE_end = 'StdJnt_Foot_SIDE_End'
    toe_SIDE_ = 'StdJnt_Toe_SIDE_'
    toe_SIDE_end = 'StdJnt_Toe_SIDE_End'    


    @staticmethod
    def getHeadList():
        return Std.base, Std.neck, Std.head
        

    @staticmethod
    def getBodyList():
        return Std.base, Std.root, Std.back01, Std.back02, Std.chest
    
    
    @staticmethod
    def getLeftClavicleList():
        
        replaceList = ( '_SIDE_', '_L_' )
        stdClavicle = Std.clavicle_SIDE_.replace( *replaceList )
        stdArm00    = Std.arm_SIDE_00.replace( *replaceList )
        return Std.base, stdClavicle, stdArm00
    
    
    @staticmethod
    def getRightClavicleList():
        
        replaceList = ( '_SIDE_', '_R_' )
        stdClavicle = Std.clavicle_SIDE_.replace( *replaceList )
        stdArm00    = Std.arm_SIDE_00.replace( *replaceList )
        return Std.base, stdClavicle, stdArm00
    
    
    @staticmethod
    def getLeftArmList():
        
        replaceList = ( '_SIDE_', '_L_' )
        stdArm00 = Std.arm_SIDE_00.replace( *replaceList )
        stdArm01 = Std.arm_SIDE_01.replace( *replaceList )
        stdArm02 = Std.arm_SIDE_02.replace( *replaceList )
        stdArm01Offset = Std.arm_SIDE_01_Offset.replace( *replaceList )
        stdPoleV = Std.arm_SIDE_poleV.replace( *replaceList )
        stdLookAt = Std.arm_SIDE_lookAt.replace( *replaceList )
        return Std.base, stdArm00, stdArm01, stdArm02, stdArm01Offset, stdPoleV, stdLookAt
    

    @staticmethod
    def getRightArmList():
        
        replaceList = ( '_SIDE_', '_R_' )
        stdArm00 = Std.arm_SIDE_00.replace( *replaceList )
        stdArm01 = Std.arm_SIDE_01.replace( *replaceList )
        stdArm02 = Std.arm_SIDE_02.replace( *replaceList )
        stdArm01Offset = Std.arm_SIDE_01_Offset.replace( *replaceList )
        stdPoleV = Std.arm_SIDE_poleV.replace( *replaceList )
        stdLookAt = Std.arm_SIDE_lookAt.replace( *replaceList )
        return Std.base, stdArm00, stdArm01, stdArm02, stdArm01Offset, stdPoleV, stdLookAt
    
    
    @staticmethod
    def getLeftLegList():
        
        replaceList = ( '_SIDE_', '_L_' )
        stdArm00 = Std.leg_SIDE_00.replace( *replaceList )
        stdArm01 = Std.leg_SIDE_01.replace( *replaceList )
        stdArm02 = Std.leg_SIDE_02.replace( *replaceList )
        stdArm01Offset = Std.leg_SIDE_01_Offset.replace( *replaceList )
        stdPoleV = Std.leg_SIDE_poleV.replace( *replaceList )
        stdLookAt = Std.leg_SIDE_lookAt.replace( *replaceList )
        return Std.base, stdArm00, stdArm01, stdArm02, stdArm01Offset, stdPoleV, stdLookAt
    

    @staticmethod
    def getRightLegList():
        
        replaceList = ( '_SIDE_', '_R_' )
        stdArm00 = Std.leg_SIDE_00.replace( *replaceList )
        stdArm01 = Std.leg_SIDE_01.replace( *replaceList )
        stdArm02 = Std.leg_SIDE_02.replace( *replaceList )
        stdArm01Offset = Std.leg_SIDE_01_Offset.replace( *replaceList )
        stdPoleV = Std.leg_SIDE_poleV.replace( *replaceList )
        stdLookAt = Std.leg_SIDE_lookAt.replace( *replaceList )
        return Std.base, stdArm00, stdArm01, stdArm02, stdArm01Offset, stdPoleV, stdLookAt
        
    
    @staticmethod
    def getLeftIkFootList():
        
        replaceList = ( '_SIDE_', '_L_' )
        stdToe     = Std.toe_SIDE_.replace( *replaceList )
        stdToeEnd  = Std.toe_SIDE_end.replace( *replaceList )
        stdFootPiv = Std.foot_SIDE_Piv.replace( *replaceList )
        stdToePiv  = Std.foot_SIDE_ToePiv.replace( *replaceList )
        stdFootInside = Std.foot_SIDE_inside.replace( *replaceList )
        stdFootOutside = Std.foot_SIDE_outside.replace( *replaceList )
        stdFootEnd  = Std.foot_SIDE_end.replace( *replaceList )
        return stdToe, stdToeEnd, stdFootPiv, stdToePiv, stdFootInside, stdFootOutside, stdFootEnd


    @staticmethod
    def getRightIkFootList():
        
        replaceList = ( '_SIDE_', '_R_' )
        stdToe     = Std.toe_SIDE_.replace( *replaceList )
        stdToeEnd  = Std.toe_SIDE_end.replace( *replaceList )
        stdFootPiv = Std.foot_SIDE_Piv.replace( *replaceList )
        stdToePiv  = Std.foot_SIDE_ToePiv.replace( *replaceList )
        stdFootInside = Std.foot_SIDE_inside.replace( *replaceList )
        stdFootOutside = Std.foot_SIDE_outside.replace( *replaceList )
        stdFootEnd  = Std.foot_SIDE_end.replace( *replaceList )
        return stdToe, stdToeEnd, stdFootPiv, stdToePiv, stdFootInside, stdFootOutside, stdFootEnd
    
    
    @staticmethod
    def getLeftFkFootList():
        
        replaceList = ( '_SIDE_', '_L_' )
        stdToe  = Std.toe_SIDE_.replace( *replaceList )
        stdToeEnd  = Std.toe_SIDE_end.replace( *replaceList )
        return stdToe, stdToeEnd
    
    
    @staticmethod
    def getRightFkFootList():
        
        replaceList = ( '_SIDE_', '_R_' )
        stdToe  = Std.toe_SIDE_.replace( *replaceList )
        stdToeEnd  = Std.toe_SIDE_end.replace( *replaceList )
        return stdToe, stdToeEnd
    
    
    @staticmethod
    def getLeftHandList():
        
        replaceList = ( '_SIDE_', '_L_' )
        stdArm02 = Std.arm_SIDE_02.replace( *replaceList )
        fingerString = Std.fingers_SIDE_.replace( *replaceList )
        return Std.base, stdArm02, fingerString


    @staticmethod
    def getRightHandList():
        
        replaceList = ( '_SIDE_', '_R_' )
        stdArm02 = Std.arm_SIDE_02.replace( *replaceList )
        fingerString = Std.fingers_SIDE_.replace( *replaceList )
        return Std.base, stdArm02, fingerString




@convertName_dec
def aimConstraint( *args, **kwargs ):
    
    if kwargs.has_key( 'wuo' ) or kwargs.has_key( 'worldUpObject' ):
        kwargs['wuo'] = convertName( kwargs['wuo'] ) 
    
    return cmds.aimConstraint( *args, **kwargs )




class HumanRig:
    
    bodyColor = 18
    bodyRotColor = 23
    rootColor = 6
    worldColor = 22
    leftColor = 17
    rightColor = 13




class HeadRig:
    
    def __init__(self, stdBase, stdNeck, stdHead ):
        
        self.stdPrefix = 'StdJnt_'
        self.stdBase = convertSg( stdBase )
        self.stdNeck = convertSg( stdNeck )
        self.stdHead = convertSg( stdHead )
        self.controllerSize = 1
    
    
    def createAll(self, controllerSize = 1 ):
        
        self.controllerSize = controllerSize
        self.createRigBase()
        self.createController()
        self.createJoints()
        
    

    def createRigBase(self):
        
        self.rigBase = createNode( 'transform', n= 'RigBase_Head' )
        self.rigBase.xform( ws=1, matrix=self.stdNeck.wm.get() )
        dcmp = getDecomposeMatrix( getLocalMatrix( self.stdNeck, self.stdBase ) )
        dcmp.ot >> self.rigBase.t
        dcmp.outputRotate >> self.rigBase.r



    def createController(self):
        
        self.ctlNeck = makeController( sgdata.Controllers.circlePoints, self.controllerSize, n='Ctl_Neck', makeParent=1, colorIndex=23 )
        self.ctlNeck.setAttr( 'shape_ty', 0.289  )
        pCtlNeck = self.ctlNeck.parent()
        pCtlNeck.xform( ws=1, matrix= self.stdNeck.wm.get() )
        
        self.ctlHead = makeController( sgdata.Controllers.circlePoints, self.controllerSize, n='Ctl_Head', makeParent=1, colorIndex=5 )
        self.ctlHead.setAttr( 'shape_ty', 0.95  ).setAttr( 'shape_rx', 90 ).setAttr( 'shape_sx', 1.3 ).setAttr( 'shape_sy', 1.3 ).setAttr( 'shape_sz', 1.3 )
        pCtlHead = self.ctlHead.parent()
        pCtlHead.xform( ws=1, matrix= self.stdHead.wm.get() )
        pCtlHead.parentTo( self.ctlNeck )
        
        self.stdHead.t >> pCtlHead.t
        self.stdHead.r >> pCtlHead.r
        
        pCtlNeck.parentTo( self.rigBase )
        headCtlOrientObj = pCtlNeck.makeChild()
        
        self.stdHead.t >> headCtlOrientObj.t
        self.stdHead.r >> headCtlOrientObj.r
        
        constrain_rotate( headCtlOrientObj, pCtlHead )
        
        
        
    
    
    def createJoints(self):
        
        lookAtPointer01base = createNode( 'transform', n='lookAtPointerBase_neckMiddle01' )
        lookAtPointer01base.parentTo( self.ctlHead )
        lookAtPointer01base.setTransformDefault()
        
        lookAtPointer01 = lookAtPointer01base.makeChild( replaceName = ['lookAtPointerBase','lookAtPointer'] )
        multPointer01 = createNode( 'multiplyDivide' ).setAttr( 'input2', -0.25,-0.25,-0.25 )
        self.stdHead.t >> multPointer01.input1
        multPointer01.output >> lookAtPointer01.t
        
        self.stdNeck.r >> lookAtPointer01base.r
        
        lookAtHeadToNeck = createNode( 'transform', n='lookAtHeadToNeck' )
        lookAtHeadToNeck.parentTo( self.ctlHead )
        lookAtHeadToNeck.setTransformDefault()
        
        lookAtConnect( self.ctlNeck, lookAtHeadToNeck )
        
        lookAtPointer02base = createNode( 'transform', n='lookAtPointerBase_neckMiddle02' )
        lookAtPointer02base.parentTo( self.ctlNeck )
        lookAtPointer02base.setTransformDefault()
        
        lookAtConnect( self.ctlHead, lookAtPointer02base )
        
        lookAtPointer02 = lookAtPointer02base.makeChild( replaceName = ['lookAtPointerBase','lookAtPointer'] )
        multPointer02 = createNode( 'multiplyDivide' ).setAttr( 'input2', .75,.75,.75 )
        self.stdHead.t >> multPointer02.input1
        multPointer02.output >> lookAtPointer02.t

        lookAtPointer = createNode( 'transform', n='lookAtPointerBase_neckMiddle' )
        lookAtPointer.parentTo( self.ctlNeck.parent() )
        blendTwoMatrix( lookAtPointer01, lookAtPointer02, lookAtPointer, ct=1, cr=1 )
        
        select( d=1 )
        self.jntNeck = joint()
        self.jntNeckMiddle = joint()
        self.jntHead = joint()
        
        constrain_point( self.ctlNeck, self.jntNeck )
        lookAtConnect( lookAtPointer, self.jntNeck ) 
        
        dcmp = getDecomposeMatrix( getLocalMatrix( self.ctlHead, self.ctlNeck ) )
        distNode = getDistance( dcmp )
        multDist = createNode( 'multDoubleLinear' )
        distNode.distance >> multDist.input1
        multDist.input2.set( 0.5 )
        multDist.output >> self.jntNeckMiddle.ty
        multDist.output >> self.jntHead.ty
        
        constrain_rotate( self.ctlHead, self.jntHead )
        lookAtConnect( self.ctlHead, self.jntNeckMiddle )
        
        blendNode = getBlendTwoMatrixNode( lookAtPointer01base, lookAtPointer02base )
        dcmp = getDecomposeMatrix( getLocalMatrix( blendNode, lookAtPointer02) )
        
        dcmp.ory >> self.jntNeckMiddle.attr( 'rotateAxisY' )
        
        self.resultJnts = [ self.jntNeck, self.jntNeckMiddle, self.jntHead ]





class BodyRig:
    
    def __init__(self, stdBase, stdRoot, stdBackFirst, stdBackSecond, stdChest ):
        
        self.stdPrefix = 'StdJnt_'
        self.stdBase = convertSg( stdBase )
        self.stdRoot = convertSg( stdRoot )
        self.stdBackFirst = convertSg( stdBackFirst )
        self.stdBackSecond = convertSg( stdBackSecond )
        self.stdChest = convertSg( stdChest )
        
        self.controllerSize = 1
        
        
    
    def createAll(self, controllerSize = 1, numJoint=3 ):
        
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
        
        self.ctlRoot = makeController( sgdata.Controllers.movePoints, self.controllerSize, n= 'Ctl_Root', makeParent=1, colorIndex=HumanRig.rootColor )
        self.ctlPervis = makeController( sgdata.Controllers.cubePoints, self.controllerSize, n='Ctl_PervisRotator', makeParent=1, colorIndex=HumanRig.bodyRotColor )
        self.ctlBodyRotator1 = makeController( sgdata.Controllers.cubePoints, self.controllerSize, n='Ctl_BodyRotatorFirst', makeParent=1, colorIndex=HumanRig.bodyRotColor )
        self.ctlBodyRotator2 = makeController( sgdata.Controllers.cubePoints, self.controllerSize, n='Ctl_BodyRotatorSecond', makeParent=1, colorIndex=HumanRig.bodyRotColor )
        self.ctlChest = makeController( sgdata.Controllers.circlePoints, self.controllerSize, n='Ctl_Chest', makeParent=1, colorIndex=HumanRig.bodyRotColor )
        self.ctlWaist = makeController( sgdata.Controllers.circlePoints, self.controllerSize, n='Ctl_Waist', makeParent=1, colorIndex=HumanRig.bodyColor )
        self.ctlHip   = makeController( sgdata.Controllers.circlePoints, self.controllerSize, n='Ctl_Hip', makeParent=1, colorIndex=HumanRig.bodyColor )
        
        self.ctlRoot.parent().xform( ws=1, matrix= self.stdRoot.wm.get() )
        self.ctlPervis.parent().xform( ws=1, matrix= self.stdRoot.wm.get() )
        self.ctlBodyRotator1.parent().xform( ws=1, matrix= self.stdBackFirst.wm.get() )
        self.ctlBodyRotator2.parent().xform( ws=1, matrix= self.stdBackSecond.wm.get() )
        self.ctlChest.parent().xform( ws=1, matrix= self.stdChest.wm.get() )
        self.ctlWaist.parent().xform( ws=1, matrix= self.stdBackFirst.wm.get() )
        self.ctlHip.parent().xform( ws=1, matrix= self.stdRoot.wm.get() )
        
        self.ctlRoot.setAttr( 'shape_sx', 2.14 ).setAttr( 'shape_sy', 2.14 ).setAttr( 'shape_sz', 2.14 )
        self.ctlPervis.setAttr( 'shape_sx', 3.85 ).setAttr( 'shape_sy', 0.16 ).setAttr( 'shape_sz', 3.85 )
        self.ctlBodyRotator1.setAttr( 'shape_sx', 3.36 ).setAttr( 'shape_sy', 0.16 ).setAttr( 'shape_sz', 3.36 )
        self.ctlBodyRotator2.setAttr( 'shape_sx', 3.36 ).setAttr( 'shape_sy', 0.16 ).setAttr( 'shape_sz', 3.36 )
        self.ctlWaist.setAttr( 'shape_sx', 2 ).setAttr( 'shape_sy', 2 ).setAttr( 'shape_sz', 2 )
        self.ctlChest.setAttr( 'shape_sx', 2 ).setAttr( 'shape_sy', 2 ).setAttr( 'shape_sz', 2 )
        self.ctlHip.setAttr( 'shape_sx', 1.9 ).setAttr( 'shape_sy', 1.9 ).setAttr( 'shape_sz', 1.9 )
    


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
    
        pointerInHip = self.stdRoot.makeChild().rename( 'pointer_' + self.stdRoot.name() )
        multForPointerInHip = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.1, 0.1, 0.1 )
        self.stdBackFirst.t >> multForPointerInHip.input1
        multForPointerInHip.output >> pointerInHip.t
        
        pointerInBack1_grp = self.stdBackFirst.makeChild().rename( 'pointerGrp_' + self.stdBackFirst.name() )
        pointerInBack1_00 = pointerInBack1_grp.makeChild().rename( 'pointer00_' + self.stdBackFirst.name() )
        pointerInBack1_01 = pointerInBack1_grp.makeChild().rename( 'pointer01_' + self.stdBackFirst.name() )
        multForPointerInBack1_00 = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.3, 0.3, 0.3 )
        multForPointerInBack1_01 = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.3, 0.3, 0.3 )
        dcmpPointerInBack1_00 = getDecomposeMatrix( getLocalMatrix( self.stdRoot, self.stdBackFirst ) )
        dcmpPointerInBack1_00.ot >> multForPointerInBack1_00.input1
        self.stdBackSecond.t >> multForPointerInBack1_01.input1
        multForPointerInBack1_00.output >> pointerInBack1_00.t
        multForPointerInBack1_01.output >> pointerInBack1_01.t
        connectBlendTwoMatrix( self.stdRoot, self.stdBackFirst, pointerInBack1_grp, cr=1 )
        
        pointerInBack2_grp = self.stdBackSecond.makeChild().rename( 'pointerGrp_' + self.stdBackSecond.name() )
        pointerInBack2_00 = pointerInBack2_grp.makeChild().rename( 'pointer00_' + self.stdBackSecond.name() )
        pointerInBack2_01 = pointerInBack2_grp.makeChild().rename( 'pointer01_' + self.stdBackSecond.name() )
        multForPointerInBack2_00 = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.3, 0.3, 0.3 )
        multForPointerInBack2_01 = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.3, 0.3, 0.3 )
        dcmpPointerInBack2_00 = getDecomposeMatrix( getLocalMatrix( self.stdBackFirst, self.stdBackSecond ) )
        dcmpPointerInBack2_00.ot >> multForPointerInBack2_00.input1
        self.stdBackSecond.t >> multForPointerInBack2_01.input1
        multForPointerInBack2_00.output >> pointerInBack2_00.t
        multForPointerInBack2_01.output >> pointerInBack2_01.t
        connectBlendTwoMatrix( self.stdBackFirst, self.stdBackSecond, pointerInBack2_grp, cr=1 )
        
        pointerInChest = self.stdChest.makeChild().rename( 'pointer_' + self.stdChest.name() )
        multForPointerInChest = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.1, 0.1, 0.1 )
        dcmpForPointerInChest = getDecomposeMatrix( getLocalMatrix( self.stdBackSecond, self.stdChest ) )
        dcmpForPointerInChest.ot >> multForPointerInChest.input1
        multForPointerInChest.output >> pointerInChest.t
        
        dcmpCurvePointer0 = getDecomposeMatrix( getLocalMatrix( self.stdRoot, self.stdRoot ) )
        dcmpCurvePointer1 = getDecomposeMatrix( getLocalMatrix( pointerInHip, self.stdRoot ) )
        dcmpCurvePointer2 = getDecomposeMatrix( getLocalMatrix( pointerInBack1_00, self.stdRoot ) )
        dcmpCurvePointer3 = getDecomposeMatrix( getLocalMatrix( self.stdBackFirst, self.stdRoot ) )
        dcmpCurvePointer4 = getDecomposeMatrix( getLocalMatrix( pointerInBack1_01, self.stdRoot ) )
        dcmpCurvePointer5 = getDecomposeMatrix( getLocalMatrix( pointerInBack2_00, self.stdRoot ) )
        dcmpCurvePointer6 = getDecomposeMatrix( getLocalMatrix( self.stdBackSecond, self.stdRoot ) )
        dcmpCurvePointer7 = getDecomposeMatrix( getLocalMatrix( pointerInBack2_01, self.stdRoot ) )
        dcmpCurvePointer8 = getDecomposeMatrix( getLocalMatrix( pointerInChest, self.stdRoot ) )
        dcmpCurvePointer9 = getDecomposeMatrix( getLocalMatrix( self.stdChest, self.stdRoot ) )

        points = [[0,0,0] for i in range( 10 )]
        origCurve = curve( p=points, d=3 ).parentTo( self.ctlRoot ).setTransformDefault()
        origCurveShape = origCurve.shape()
        dcmpCurvePointer0.ot >> origCurveShape.attr( 'controlPoints[0]' )
        dcmpCurvePointer1.ot >> origCurveShape.attr( 'controlPoints[1]' )
        dcmpCurvePointer2.ot >> origCurveShape.attr( 'controlPoints[2]' )
        dcmpCurvePointer3.ot >> origCurveShape.attr( 'controlPoints[3]' )
        dcmpCurvePointer4.ot >> origCurveShape.attr( 'controlPoints[4]' )
        dcmpCurvePointer5.ot >> origCurveShape.attr( 'controlPoints[5]' )
        dcmpCurvePointer6.ot >> origCurveShape.attr( 'controlPoints[6]' )
        dcmpCurvePointer7.ot >> origCurveShape.attr( 'controlPoints[7]' )
        dcmpCurvePointer8.ot >> origCurveShape.attr( 'controlPoints[8]' )
        dcmpCurvePointer9.ot >> origCurveShape.attr( 'controlPoints[9]' )
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
        
        pointerInHip = self.ctlHip.makeChild().rename( 'pointer_' + self.ctlHip.name() )
        multForPointerInHip = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.1, 0.1, 0.1 )
        self.stdBackFirst.t >> multForPointerInHip.input1
        multForPointerInHip.output >> pointerInHip.t
        
        pointerInBack1_grp = pointerBody1.makeChild().rename( 'pointerGrp_' + pointerBody1.name() )
        pointerInBack1_00 = pointerInBack1_grp.makeChild().rename( 'pointer00_' + pointerBody1.name() )
        pointerInBack1_01 = pointerInBack1_grp.makeChild().rename( 'pointer01_' + pointerBody1.name() )
        multForPointerInBack1_00 = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.3, 0.3, 0.3 )
        multForPointerInBack1_01 = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.3, 0.3, 0.3 )
        dcmpPointerInBack1_00 = getDecomposeMatrix( getLocalMatrix( self.stdRoot, self.stdBackFirst ) )
        dcmpPointerInBack1_00.ot >> multForPointerInBack1_00.input1
        self.stdBackSecond.t >> multForPointerInBack1_01.input1
        multForPointerInBack1_00.output >> pointerInBack1_00.t
        multForPointerInBack1_01.output >> pointerInBack1_01.t
        connectBlendTwoMatrix( self.ctlBodyRotator1, self.ctlBodyRotator1.parent(), pointerInBack1_grp, cr=1 )
        
        pointerInBack2_grp = pointerBody2.makeChild().rename( 'pointerGrp_' + pointerBody2.name() )
        pointerInBack2_00 = pointerInBack2_grp.makeChild().rename( 'pointer00_' + pointerBody2.name() )
        pointerInBack2_01 = pointerInBack2_grp.makeChild().rename( 'pointer01_' + pointerBody2.name() )
        multForPointerInBack2_00 = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.3, 0.3, 0.3 )
        multForPointerInBack2_01 = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.3, 0.3, 0.3 )
        dcmpPointerInBack2_00 = getDecomposeMatrix( getLocalMatrix( self.stdBackFirst, self.stdBackSecond ) )
        dcmpPointerInBack2_00.ot >> multForPointerInBack2_00.input1
        self.stdBackSecond.t >> multForPointerInBack2_01.input1
        multForPointerInBack2_00.output >> pointerInBack2_00.t
        multForPointerInBack2_01.output >> pointerInBack2_01.t
        connectBlendTwoMatrix( self.ctlBodyRotator2, self.ctlBodyRotator2.parent(), pointerInBack2_grp, cr=1 )
        
        pointerInChest = self.ctlChest.makeChild().rename( 'pointer_' + self.ctlChest.name() )
        multForPointerInChest = createNode( 'multiplyDivide' ).setAttr( 'input2', 0.1, 0.1, 0.1 )
        dcmpForPointerInChest = getDecomposeMatrix( getLocalMatrix( self.stdBackSecond, self.stdChest ) )
        dcmpForPointerInChest.ot >> multForPointerInChest.input1
        multForPointerInChest.output >> pointerInChest.t
        
        dcmpCurvePointer0 = getDecomposeMatrix( getLocalMatrix( self.ctlHip, self.ctlRoot ) )
        dcmpCurvePointer1 = getDecomposeMatrix( getLocalMatrix( pointerInHip, self.ctlRoot ) )
        dcmpCurvePointer2 = getDecomposeMatrix( getLocalMatrix( pointerInBack1_00, self.ctlRoot ) )
        dcmpCurvePointer3 = getDecomposeMatrix( getLocalMatrix( pointerBody1, self.ctlRoot ) )
        dcmpCurvePointer4 = getDecomposeMatrix( getLocalMatrix( pointerInBack1_01, self.ctlRoot ) )
        dcmpCurvePointer5 = getDecomposeMatrix( getLocalMatrix( pointerInBack2_00, self.ctlRoot ) )
        dcmpCurvePointer6 = getDecomposeMatrix( getLocalMatrix( pointerBody2, self.ctlRoot ) )
        dcmpCurvePointer7 = getDecomposeMatrix( getLocalMatrix( pointerInBack2_01, self.ctlRoot ) )
        dcmpCurvePointer8 = getDecomposeMatrix( getLocalMatrix( pointerInChest, self.ctlRoot ) )
        dcmpCurvePointer9 = getDecomposeMatrix( getLocalMatrix( self.ctlChest, self.ctlRoot ) )

        bodyCurve = curve( p=[[0,0,0] for i in range( 10 )], d=7 )
        curveShape = bodyCurve.shape()
        dcmpCurvePointer0.ot >> curveShape.attr( 'controlPoints[0]' )
        dcmpCurvePointer1.ot >> curveShape.attr( 'controlPoints[1]' )
        dcmpCurvePointer2.ot >> curveShape.attr( 'controlPoints[2]' )
        dcmpCurvePointer3.ot >> curveShape.attr( 'controlPoints[3]' )
        dcmpCurvePointer4.ot >> curveShape.attr( 'controlPoints[4]' )
        dcmpCurvePointer5.ot >> curveShape.attr( 'controlPoints[5]' )
        dcmpCurvePointer6.ot >> curveShape.attr( 'controlPoints[6]' )
        dcmpCurvePointer7.ot >> curveShape.attr( 'controlPoints[7]' )
        dcmpCurvePointer8.ot >> curveShape.attr( 'controlPoints[8]' )
        dcmpCurvePointer9.ot >> curveShape.attr( 'controlPoints[9]' )
        
        bodyCurve.parentTo( self.ctlRoot ).setTransformDefault()
        self.currentCurve = bodyCurve
    

    def createResultJoints(self, numJoints = 5 ):
        
        jnts = []
        select( d=1 )
        self.rootJnt = joint()
        for i in range( numJoints + 1 ):
            jnt = joint()
            jnt.ty.set( 1.0 );
            jnts.append( jnt )
        
        self.handle, self.effector = ikHandle( sj=jnts[0], ee=jnts[-1], curve= self.currentCurve, sol='ikSplineSolver',  ccv=False, pcv=False )
        self.handle.parentTo( self.rigBase )
        self.ctlChest.addAttr( ln="attach", min=0, max=1, dv=1, k=1 )
        
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
            self.ctlChest.attach >> blendNode.attributesBlender
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
        jnts.insert( 0, self.rootJnt )
        self.resultJnts = jnts
    

    @convertSg_dec
    def createClavicleConnector(self, stdClavicleL, stdClavicleR ):
        
        chestJnt = self.resultJnts[-1]
        
        connectorClavicleL = chestJnt.makeChild().rename( stdClavicleL.replace( self.stdPrefix, 'Connector_' ) )
        connectorClavicleR = chestJnt.makeChild().rename( stdClavicleR.replace( self.stdPrefix, 'Connector_' ) )
        
        stdClavicleL.t >> connectorClavicleL.t
        stdClavicleL.r >> connectorClavicleL.r
        stdClavicleR.t >> connectorClavicleR.t
        stdClavicleR.r >> connectorClavicleR.r
        
        self.connectorClavicleL = connectorClavicleL
        self.connectorClavicleR = connectorClavicleR
    

    @convertSg_dec
    def createHipConnector(self, stdHipL, stdHipR ):
        
        rootJnt = self.rootJnt
        lookAtTarget = self.ctlRoot.makeChild().rename( self.stdRoot.replace( self.stdPrefix, 'ConnectorLookTarget_' ) )
        dcmp = getDecomposeMatrix( getLocalMatrix( self.stdChest, self.stdRoot ) )
        dcmp.oty >> lookAtTarget.ty
        
        connectorOrientBaseParent = self.ctlRoot.makeChild().rename( self.stdRoot.replace( self.stdPrefix, 'PConnectorOrientBase_' ) )
        connectorOrientBase = connectorOrientBaseParent.makeChild().rename( self.stdRoot.replace( self.stdPrefix, 'ConnectorOrientBase_' ) )
        lookAtConnect( lookAtTarget, connectorOrientBase )
        constrain_rotate( self.ctlHip, connectorOrientBaseParent )
        
        connectorOrientL = connectorOrientBase.makeChild().rename( stdHipL.replace( self.stdPrefix, 'ConnectorOrient_' ) )
        connectorOrientR = connectorOrientBase.makeChild().rename( stdHipR.replace( self.stdPrefix, 'ConnectorOrient_' ) )
        
        self.ctlHipPinL = makeController( sgdata.Controllers.pinPoints, self.controllerSize, n='Ctl_HipPos_L_', makeParent=1, colorIndex = HumanRig.leftColor )
        self.ctlHipPinR = makeController( sgdata.Controllers.pinPoints, self.controllerSize, n='Ctl_HipPos_R_', makeParent=1, colorIndex = HumanRig.rightColor )
        self.ctlHipPinR.setAttr( 'shape_rz', 180 )
        pCtlHipPinL = self.ctlHipPinL.parent()
        pCtlHipPinR = self.ctlHipPinR.parent()
        pCtlHipPinL.parentTo( self.ctlHip )
        pCtlHipPinR.parentTo( self.ctlHip )
        
        connectorL = rootJnt.makeChild().rename( stdHipL.replace( self.stdPrefix, 'Connector_' ) )
        connectorR = rootJnt.makeChild().rename( stdHipR.replace( self.stdPrefix, 'Connector_' ) )
        
        stdHipL.t >> connectorOrientL.t
        stdHipR.t >> connectorOrientR.t
        stdHipL.r >> connectorOrientL.r
        stdHipR.r >> connectorOrientR.r
        
        stdHipL.t >> pCtlHipPinL.t
        stdHipR.t >> pCtlHipPinR.t
        constrain_rotate( connectorOrientL, pCtlHipPinL )
        constrain_rotate( connectorOrientR, pCtlHipPinR )
        
        constrain_parent( self.ctlHipPinL, connectorL )
        constrain_parent( self.ctlHipPinR, connectorR )
        
        self.connectorHipL = connectorL
        self.connectorHipR = connectorR
    
    
    @convertSg_dec
    def createNeckConnector(self, stdNeck ):
        
        checkJnt = self.resultJnts[-1]
        
        connectorNeck = checkJnt.makeChild().rename( stdNeck.replace( self.stdPrefix, 'Connector_' ) )
        
        stdNeck.t >> connectorNeck.t
        stdNeck.r >> connectorNeck.r
        
        self.connectorNeck = connectorNeck
    
    
        
        
        





class ClavicleRig:
    
    def __init__(self, stdBase, stdClavicle, stdShoulder ):

        self.stdPrefix = 'StdJnt_'
        self.stdBase = convertSg( stdBase )
        self.stdClavicle = convertSg( stdClavicle )
        self.stdShoulder = convertSg( stdShoulder )
        self.controllerSize = 1
    
    
    def createAll(self, controllerSize = 1, colorIndex=0 ):
    
        self.controllerSize = controllerSize
        self.colorIndex = colorIndex
        self.createRigBase()
        self.createCtl()
        self.createJoints()
        self.createConnector()
    


    def createRigBase(self):
        
        self.rigBase = createNode( 'transform', n= self.stdClavicle.localName().replace( self.stdPrefix, 'RigBase_' ) )
        self.rigBase.xform( ws=1, matrix= self.stdClavicle.wm.get() )
        constrain_parent( self.stdClavicle, self.rigBase )
    


    def createCtl(self):
        
        self.ctlClavicle = makeController( sgdata.Controllers.pinPoints, self.controllerSize, typ='joint', n= self.stdClavicle.localName().replace( self.stdPrefix, 'Ctl_' ),
                                           makeParent=1, colorIndex= self.colorIndex )
        pCtlClavicle = self.ctlClavicle.parent()
        pCtlClavicle.parentTo( self.rigBase )
        self.stdShoulder.t >> pCtlClavicle.t
        
        if self.stdShoulder.tx.get() < 0:
            self.ctlClavicle.attr( 'shape_sx' ).set( -1 )
            self.ctlClavicle.attr( 'shape_sy' ).set( -1 )
            self.ctlClavicle.attr( 'shape_sz' ).set( -1 )
        
        pCtlClavicle.r.set( 0,0,0 )


    
    def createJoints(self):
        
        self.joints = []
        select( d=1 )
        jntFirst = joint()
        jntEnd = joint()
        jntEndOrientor = self.rigBase.makeChild().rename( self.stdClavicle.replace( self.stdPrefix, 'connectOrientor_' ) ) 
        self.stdShoulder.t >> jntEndOrientor.t
        self.stdShoulder.r >> jntEndOrientor.r
        constrain_rotate( jntEndOrientor, jntEnd )
        
        self.stdShoulder.t >> jntEnd.t
        constrain_point( self.rigBase, jntFirst )
        
        direction = [1,0,0]
        
        if self.stdShoulder.tx.get() < 0:
            direction = [-1,0,0]
        lookAtConnect( self.ctlClavicle, jntFirst, direction=direction )
        
        addOptionAttribute( self.ctlClavicle )
        self.ctlClavicle.addAttr( ln='attach', min=0, max=1, dv=0, k=1 )
        pCtlClavicle = self.ctlClavicle.parent()
        
        distBase = getDistance( pCtlClavicle )
        distCurrent = getDistance( getDecomposeMatrix(getLocalMatrix( self.ctlClavicle, self.rigBase )) )
        
        divNode = createNode( 'multiplyDivide' ).setAttr( 'op', 2 )
        distCurrent.distance >> divNode.input1X
        distBase.distance >> divNode.input2X
        
        blendNode = createNode( 'blendTwoAttr' ).setAttr( 'input[0]', 1 )
        divNode.outputX >> blendNode.input[1]
        
        self.ctlClavicle.attach >> blendNode.ab
        
        blendNode.output >> jntFirst.sx
        
        self.jntFirst = jntFirst
        self.jntEnd = jntEnd
        
        self.resultJnts = [ self.jntFirst ]
        
    
    
    def createConnector(self):
        
        self.connector = self.jntEnd
        







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
    
    
    
    def createAll(self, controllerSize=1, colorIndex=0, numJnt=3 ):
        
        self.controllerSize = controllerSize
        self.colorIndex = colorIndex
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
        self.createCurve()
        self.createSpJointsUpper(numJnt)
        self.createSpJointsLower(numJnt)
        self.createConnector()
        


    def createRigBase(self ):
        
        self.rigBase = createNode( 'transform', n= self.stdFirst.localName().replace( self.stdPrefix, 'RigBase_' ) )
        self.rigBase.xform( ws=1, matrix= self.stdFirst.wm.get() )
        constrain_parent( self.stdFirst, self.rigBase )
    

    
    def createIkController(self ):
        
        self.ctlIkEnd = makeController( sgdata.Controllers.cubePoints, self.controllerSize, typ='joint', n= self.stdEnd.localName().replace( self.stdPrefix, 'Ctl_Ik' ),
                                        makeParent=1, colorIndex = self.colorIndex )
        self.ctlIkEnd.setAttr( 'shape_sx', 0.1 )
        self.ctlIkEnd.setAttr( 'shape_sy', 1.5 )
        self.ctlIkEnd.setAttr( 'shape_sz', 1.5 )
        pCtlIkEnd = self.ctlIkEnd.parent()
        pCtlIkEnd.xform( ws=1, matrix= self.stdEnd.wm.get() )
    
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
        
        addOptionAttribute( self.ctlIkEnd, 'ikOptions')
        
        
        
    def createPoleVController(self, twistReverse=False ):
        
        self.ctlIkPoleV = makeController( sgdata.Controllers.diamondPoints, self.controllerSize, n= self.stdPoleV.localName().replace( self.stdPrefix, 'Ctl_' ),
                                          makeParent=1, colorIndex=self.colorIndex )
        self.ctlIkPoleV.setAttr( 'shape_sx', 0.23 )
        self.ctlIkPoleV.setAttr( 'shape_sy', 0.23 )
        self.ctlIkPoleV.setAttr( 'shape_sz', 0.23 )
        pIkCtlPoleV = self.ctlIkPoleV.parent()
        pIkCtlPoleV.xform( ws=1, matrix = self.stdLookAt.wm.get() )
        self.poleVTwist = makeParent( pIkCtlPoleV, n='Twist_' + self.stdPoleV.localName().replace( self.stdPrefix, '' ) )
        self.ctlIkEnd.addAttr( ln='twist', k=1, at='doubleAngle' )
        
        multNode = createNode( 'multDoubleLinear' )
        self.ctlIkEnd.twist >> multNode.input1
        multNode.output >> self.poleVTwist.rx
        
        multNode.input2.set( 1 )
        if twistReverse:
            multNode.input2.set( -1 )
        
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
        
        self.fkCtlFirst = makeController( sgdata.Controllers.rhombusPoints, self.controllerSize, n= self.stdFirst.localName().replace( self.stdPrefix, 'Ctl_Fk' ), 
                                          makeParent=1, colorIndex = self.colorIndex )
        self.fkCtlSecond = makeController( sgdata.Controllers.rhombusPoints, self.controllerSize, n= self.stdSecond.localName().replace( self.stdPrefix, 'Ctl_Fk' ),
                                          makeParent=1, colorIndex = self.colorIndex )
        self.fkCtlEnd = makeController( sgdata.Controllers.rhombusPoints, self.controllerSize, n= self.stdEnd.localName().replace( self.stdPrefix, 'Ctl_Fk' ),
                                        makeParent=1, colorIndex = self.colorIndex )
        
        self.fkCtlFirst.setAttr( 'shape_rz', 90 ).setAttr( 'shape_sx', .7 ).setAttr( 'shape_sy', .7 ).setAttr( 'shape_sz', .7 )
        self.fkCtlSecond.setAttr( 'shape_rz', 90 ).setAttr( 'shape_sx', .7 ).setAttr( 'shape_sy', .7 ).setAttr( 'shape_sz', .7 )
        self.fkCtlEnd.setAttr( 'shape_rz', 90 ).setAttr( 'shape_sx', .7 ).setAttr( 'shape_sy', .7 ).setAttr( 'shape_sz', .7 )
        
        self.fkCtlFirst.parent().xform( ws=1, matrix = self.stdFirst.wm.get() )
        self.fkCtlSecond.parent().xform( ws=1, matrix = self.stdSecond.wm.get() )
        self.fkCtlEnd.parent().xform( ws=1, matrix = self.stdEnd.wm.get() )
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
        
        self.ctlBl = makeController( sgdata.Controllers.switchPoints, self.controllerSize, n= self.stdEnd.localName().replace( self.stdPrefix, 'Ctl_Bl' ),
                                     makeParent=1, colorIndex = self.colorIndex )
        pCtlBl = self.ctlBl.parent()
        pCtlBl.xform( ws=1, matrix= self.stdEnd.wm.get() )
        
        tyValue = 0.8
        if self.stdEnd.tx.get() < 0:
            tyValue *= -1
        
        self.ctlBl.setAttr( 'shape_sx', 0.3 ).setAttr( 'shape_sy', 0.3 ).setAttr( 'shape_sz', 0.3 ).setAttr( 'shape_ty', tyValue  )
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
        
        firstPos  = self.stdFirst.xform( q=1, ws=1, matrix=1 )
        secondPos = self.stdSecond.xform( q=1, ws=1, matrix=1 )
        thirdPos  = self.stdEnd.xform( q=1, ws=1, matrix=1 )
        
        self.blJntFirst  = joint( n=self.stdFirst.replace( self.stdPrefix, 'BlJnt_' ) ).xform( ws=1, matrix=firstPos )
        self.blJntSecond = joint( n=self.stdSecond.replace( self.stdPrefix, 'BlJnt_' ) ).xform( ws=1, matrix=secondPos )
        self.blJntEnd    = joint( n=self.stdEnd.replace( self.stdPrefix, 'BlJnt_' ) ).xform( ws=1, matrix=thirdPos )
        
        offsetPos = self.stdSecondoffset.xform( q=1, ws=1, matrix=1 )
        select( self.blJntSecond )
        self.blOffset = joint( n=self.stdSecondoffset.replace( self.stdPrefix, 'BlJnt_' ) ).xform( ws=1, matrix=offsetPos )
        
        self.blJntFirst.v.set( 0 )
    


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
        self.stdSecondoffset.t >> self.blOffset.t
        


    def createCurve(self):
        
        self.curveUpper = curve( p=[[0,0,0],[0,0,0]], d=1 )
        self.curveLower = curve( p=[[0,0,0],[0,0,0]], d=1 )
        
        upperShape = self.curveUpper.shape()
        lowerShape = self.curveLower.shape()
        
        dcmpOffsetInUpper = getDecomposeMatrix( getLocalMatrix( self.stdSecondoffset, self.stdFirst ) )
        
        dcmpOffsetInUpper.ot >> upperShape.attr( 'controlPoints[1]' )
        self.blOffset.t    >> lowerShape.attr( 'controlPoints[0]' )
        self.blJntEnd.t    >> lowerShape.attr( 'controlPoints[1]' )
        
        parent( self.curveUpper, self.blJntFirst )
        parent( self.curveLower, self.blJntSecond )
        self.curveUpper.setTransformDefault()
        self.curveLower.setTransformDefault()
        
        self.curveUpper.v.set(0)
        self.curveLower.v.set(0)
        


    
    def createSpJointsUpper(self, numJnt=3 ):
        
        select( d=1 )
        self.outJntsUpper = [ joint() ]
        for i in range( numJnt ):
            self.outJntsUpper.append( joint() )
        
        self.handleUpper, effector = ikHandle( sj=self.outJntsUpper[0], ee=self.outJntsUpper[-1], sol='ikSplineSolver', ccv=False, pcv=False, curve=self.curveUpper.shape() )
        curveInfo = createNode( 'curveInfo' )
        
        self.curveUpper.shape().attr( 'local' ) >> curveInfo.inputCurve
        multNode = createNode( 'multDoubleLinear' )
        curveInfo.arcLength >> multNode.input1
        
        multValue = 1.0/numJnt
        if self.blJntSecond.tx.get() < 0:
            multValue *= -1
        
        multNode.input2.set( multValue )
        for upperJnt in self.outJntsUpper[1:]:
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
        
        for jnt in self.outJntsUpper:
            continue
        parent( self.handleUpper, self.rigBase )
        self.handleUpper.v.set( 0 )
        
        self.resultJnts = self.outJntsUpper[:-1]
        
    


    def createSpJointsLower(self, numJnt=3 ):
        
        self.outJntsUpper[-1].v.set( 0 )
        select( self.outJntsUpper[-2] )
        self.outJntsLower = [ joint() ]
        for i in range( numJnt ):
            self.outJntsLower.append( joint() )
        
        self.handleLower, effector = ikHandle( sj=self.outJntsLower[0], ee=self.outJntsLower[-1], sol='ikSplineSolver', ccv=False, pcv=False, curve=self.curveLower.shape() )
        curveInfo = createNode( 'curveInfo' )
        
        self.curveLower.shape().attr( 'local' ) >> curveInfo.inputCurve
        multNode = createNode( 'multDoubleLinear' )
        curveInfo.arcLength >> multNode.input1
        
        multValue = 1.0/numJnt
        if self.blJntSecond.tx.get() < 0:
            multValue *= -1
        
        multNode.input2.set( multValue )
        for lowerJnt in self.outJntsLower[1:]:
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
        
        for jnt in self.outJntsLower:
            continue
        
        constrain_rotate( self.blJntEnd, self.outJntsLower[-1] )
        parent( self.handleLower, self.rigBase )
        self.handleLower.v.set( 0 )
        
        self.resultJnts += self.outJntsLower[:-1]
        
    
    
    def createConnector(self):
        
        self.connector = self.outJntsLower[-1]
    
    
        



class LegRig( ArmRig ):
    
    def __init__( self, stdBase, stdFirst, stdSecond, stdEnd, stdSecondoffset, stdPoleV, stdLookAt ):
        ArmRig.__init__( self,stdBase, stdFirst, stdSecond, stdEnd, stdSecondoffset, stdPoleV, stdLookAt )
        
    
    def createAll(self, controllerSize=1, colorIndex = 0, numJnt=3 ):
        
        self.controllerSize = controllerSize
        self.colorIndex = colorIndex
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
        self.createCurve()
        self.createSpJointsUpper(numJnt)
        self.createSpJointsLower(numJnt)
        if self.stdFirst.name().find( '_L_' ) != -1:
            self.createIkFootRig( *Std.getLeftIkFootList() )
            self.createFKFootRig( *Std.getLeftFkFootList() )
        else:
            self.createIkFootRig( *Std.getRightIkFootList() )
            self.createFKFootRig( *Std.getRightFkFootList() )
        self.createBlFootRig()
    
    
    
    @convertSg_dec
    def createIkFootRig(self, stdToe, stdToeEnd, stdFootPiv, stdToePiv, stdFootInside, stdFootOutside, stdFootEnd ):
        
        self.footIkGrp = createNode( 'transform', n = self.stdEnd.localName().replace( self.stdPrefix, 'FootIkBase_' ) )
        constrain_parent( self.ctlIkEnd, self.footIkGrp )
        
        ctlFoot = makeController( sgdata.Controllers.circlePoints, self.controllerSize, n= stdFootPiv.localName().replace( self.stdPrefix, 'Ctl_FootIk' ),
                                  makeParent=1, colorIndex=self.colorIndex )
        ctlFoot.shape_rz.set( 90 )
        pCtlFoot = ctlFoot.parent()
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
        
        
        ctlToeEnd = makeController( sgdata.Controllers.spherePoints, self.controllerSize, n= stdToeEnd.localName().replace( self.stdPrefix, 'Ctl_FootIk' ),
                                    makeParent=1, colorIndex=self.colorIndex )
        ctlToeEnd.setAttr( 'shape_sx', 0.2 ).setAttr( 'shape_sy', 0.2 ).setAttr( 'shape_sz', 0.2 )
        pCtlToeEnd = ctlToeEnd.parent()
        parent( pCtlToeEnd, ctlFoot )
        constrain_parent( footEndJnt, pCtlToeEnd )
        ctlToeEnd.r >> pivToeJnt.r
        
        ctlToe = makeController( sgdata.Controllers.circlePoints, self.controllerSize, n= stdToe.localName().replace( self.stdPrefix, 'Ctl_FootIk' ),
                                 makeParent=1, colorIndex=self.colorIndex )
        if stdFootPiv.tx.get() < 0:
            ctlToe.setAttr( 'shape_sx', 0.5 ).setAttr( 'shape_sy', 0.2 ).setAttr( 'shape_sz', 0.15 ).setAttr( 'shape_ry', 15 ).setAttr( 'shape_tx', 0.3  )
        else:
            ctlToe.setAttr( 'shape_sx', -0.5 ).setAttr( 'shape_sy', -0.2 ).setAttr( 'shape_sz', -0.15 ).setAttr( 'shape_ry', 15 ).setAttr( 'shape_tx', -0.3  )
        ctlToe.setAttr( 'shape_rz', 90 )
        pCtlToe = ctlToe.parent()
        parent( pCtlToe, ctlToeEnd )
        pCtlToe.setTransformDefault()
        localDcmpToeJnt.ot >> pCtlToe.t
        ctlToe.r >> toeJnt.r
        
        select( footToAnkleJnt )
        self.ikJntFoot = joint( n= self.stdEnd.localName().replace( self.stdPrefix, 'FootIkJnt_' ) )
        self.ikJntToe  = joint( n= stdToe.localName().replace( self.stdPrefix, 'FootIkJnt_' ) )
        self.ikJntToeEnd  = joint( n= stdToeEnd.localName().replace( self.stdPrefix, 'FootIkJnt_' ) )
        
        distNode = getDistance( dcmpToeEnd )
        distMultNode = createNode( 'multDoubleLinear' )
        distNode.distance >> distMultNode.input1
        distMultNode.input2.set( 1 )
        if stdFootPiv.tx.get() < 0:
            distMultNode.input2.set( -1 )
        distMultNode.output >> self.ikJntToe.tx
        
        distNode = getDistance( localDcmpToeJnt )
        distMultNode = createNode( 'multDoubleLinear' )
        distNode.distance >> distMultNode.input1
        distMultNode.input2.set( 1 )
        if stdFootPiv.tx.get() < 0:
            distMultNode.input2.set( -1 )
        distMultNode.output >> self.ikJntToeEnd.tx
        
        direction = [1,0,0]
        if stdFootPiv.tx.get() < 0:
            direction = [-1,0,0]
        
        lookAtConnect( ctlToe, self.ikJntFoot, direction=direction )
        lookAtConnect( ctlToeEnd, self.ikJntToe, direction=direction )
        
        rCons = self.ikJntToe.r.listConnections( s=1, d=0, p=1 )
        rCons[0] // self.ikJntToe.r
        rCons[0] >> self.ikJntToe.jo
        
        self.ikJntToe.r.set( 0,0,0 )
    
        addOptionAttribute(ctlToe)
        ctlToe.addAttr( ln='toeRot', k=1 )
        ctlToe.toeRot >> self.ikJntToe.ry
        
        constrain_point( footToAnkleJnt, self.ikHandle )
        constrain_point( self.ikJntEnd, self.ikJntFoot )
        parent( self.footIkGrp, self.ikGroup )
        
        footPivJnt.v.set( 0 )



    @convertSg_dec
    def createFKFootRig(self, stdToe, stdToeEnd ):
        
        self.footFkGrp = createNode( 'transform', n = self.stdEnd.localName().replace( self.stdPrefix, 'FootFkBase_' ) )
        
        ctlFkToe = makeController( sgdata.Controllers.rhombusPoints, self.controllerSize, n= stdToe.localName().replace( self.stdPrefix, 'Ctl_FootFk' ),
                                   makeParent=1, colorIndex=self.colorIndex )
        ctlFkToe.setAttr( 'shape_sx', 0.63 ).setAttr( 'shape_sy', 0.31 ).setAttr( 'shape_sz', 0.28 ).setAttr( 'shape_rz', 90 )
        pCtlFkToe = ctlFkToe.parent()
        constrain_parent( self.fkCtlEnd, self.footFkGrp )
        parent( pCtlFkToe, self.footFkGrp )
        
        composeLocalToe    = createNode( 'composeMatrix' )
        composeLocalToeEnd = createNode( 'composeMatrix' )
        inverseToe = createNode( 'inverseMatrix' )
        
        dcmpLocalToeEnd = getDecomposeMatrix( getLocalMatrix( stdToeEnd, self.stdEnd ) )
        
        stdToe.t >> composeLocalToe.it
        dcmpLocalToeEnd.ot >> composeLocalToeEnd.it
        
        composeLocalToe.outputMatrix >> inverseToe.inputMatrix
        
        mmLocalToeEnd = createNode( 'multMatrix' )
        composeLocalToeEnd.outputMatrix >> mmLocalToeEnd.i[0]
        inverseToe.outputMatrix >> mmLocalToeEnd.i[1]
        dcmpLocalToeEndTrans = getDecomposeMatrix( mmLocalToeEnd )
        
        angleNode = createNode( 'angleBetween' )
        if self.stdEnd.tx.get() > 0:
            angleNode.vector1.set( 1,0,0 )
        else:
            angleNode.vector1.set( -1,0,0 )
        dcmpLocalToeEndTrans.ot >> angleNode.vector2
        
        stdToe.t >> pCtlFkToe.t
        angleNode.euler >> pCtlFkToe.r
        
        composeToe = createNode( 'composeMatrix' )
        stdToe.t        >> composeToe.it
        angleNode.euler >> composeToe.ir
        inverseComposeToe = createNode( 'inverseMatrix' )
        
        composeToe.outputMatrix >> inverseComposeToe.inputMatrix
        
        mmToeEndInToe = createNode( 'multMatrix' )
        composeLocalToeEnd.outputMatrix >> mmToeEndInToe.i[0]
        inverseComposeToe.outputMatrix >> mmToeEndInToe.i[1]
        dcmpToeEndInToe = getDecomposeMatrix( mmToeEndInToe )
        
        childToeEnd = makeChild( ctlFkToe )
        dcmpToeEndInToe.ot >> childToeEnd.t
        
        select( self.footFkGrp )
        self.fkJntFoot = joint( n= self.stdEnd.localName().replace( self.stdPrefix, 'FootFkJnt_' ) )
        self.fkJntToe  = joint( n= stdToe.localName().replace( self.stdPrefix, 'FootFkJnt_' ) )
        self.fkJntToeEnd  = joint( n= stdToeEnd.localName().replace( self.stdPrefix, 'FootFkJnt_' ) )
        
        direction = [1,0,0]
        if self.stdEnd.tx.get() < 0:
            direction = [-1,0,0]
        lookAtConnect( ctlFkToe, self.fkJntFoot, direction=direction )
        constrain_parent( ctlFkToe, self.fkJntToe )
        childToeEnd.t >> self.fkJntToeEnd.t
        
        parent( self.footFkGrp, self.fkGroup )
        self.fkJntFoot.v.set( 0 )

        
    @convertSg_dec
    def createBlFootRig(self):
        
        self.outJntsFoot = []
        select( self.outJntsLower[-2] )
        
        outJntFoot = joint()
        outJntToe = joint()
        outJntToeEnd = joint()
        
        self.outJntsLower[-1].t >> outJntFoot.t
        connectBlendTwoMatrix( self.ikJntFoot, self.fkJntFoot, outJntFoot, cr=1 )
        connectBlendTwoMatrix( self.ikJntToe,  self.fkJntToe,  outJntToe, ct=1, cr=1, local=1 )
        connectBlendTwoMatrix( self.ikJntToeEnd, self.fkJntToeEnd, outJntToeEnd, ct=1, local=1 )
        
        self.ctlBl.blend >> outJntFoot.blend
        self.ctlBl.blend >> outJntToe.blend
        self.ctlBl.blend >> outJntToeEnd.blend
        
        self.resultJnts += [outJntFoot,outJntToe,outJntToeEnd]
        
        pass
    
    





class HandRig:
    
    def __init__(self, stdBase, stdArm02, fingerString ):
        
        self.stdPrefix       = 'StdJnt_'
        self.stdGripPrefix   = 'StdJntGrip_'
        self.stdSpreadPrefix = 'StdJntSpread_'
        
        thumbStr = 'Thumb'
        indexStr = 'Index'
        middleStr = 'Middle'
        ringStr = 'Ring'
        pinkyStr = 'Pinky'
        add1Str = 'Add1'
        add2Str = 'Add2'
        
        thumbStds = fingerString % thumbStr
        indexStds = fingerString % indexStr
        middleStds = fingerString % middleStr
        ringStds = fingerString % ringStr
        pinkyStds = fingerString % pinkyStr
        add1Stds = fingerString % add1Str
        add2Stds = fingerString % add2Str

        self.stdBase   = convertSg( stdBase )
        self.stdArm02  = convertSg( stdArm02 )
        self.thumbStds = listNodes( thumbStds, type='transform' )
        self.indexStds = listNodes( indexStds, type='transform' )
        self.middleStds = listNodes( middleStds, type='transform' )
        self.ringStds = listNodes( ringStds, type='transform' )
        self.pinkyStds = listNodes( pinkyStds, type='transform' )
        self.add1Stds = listNodes( add1Stds, type='transform' )
        self.add2Stds = listNodes( add2Stds, type='transform' )
        self.controllerSize = 1

    
    @convertName_dec
    def getSide(self, nodeName ):
        
        if nodeName.find( '_L_' ) != -1:
            return '_L_'
        else:
            return '_R_'


    
    def createAll(self, controllerSize = 1, colorIndex=0 ):
        
        self.controllerSize = controllerSize
        self.colorIndex = colorIndex
        self.createRigBase()
        self.createControllers()
        self.createJoints()
        self.createFingerAttributeControl()
    


    def createRigBase(self):
        
        self.rigBase = createNode( 'transform', n=self.stdArm02.localName().replace( self.stdPrefix, 'RigBase_' ) )
        self.rigBase.xform( ws=1, matrix= self.stdArm02.wm.get() )
        constrain_parent( self.stdArm02, self.rigBase )



    def createControllers(self):
        
        self.thumbCtls = []
        self.indexCtls = []
        self.middleCtls = []
        self.ringCtls = []
        self.pinkyCtls = []
        
        stdLists = [ self.thumbStds, self.indexStds, self.middleStds, self.ringStds, self.pinkyStds ]
        ctlLists = [ self.thumbCtls, self.indexCtls, self.middleCtls, self.ringCtls, self.pinkyCtls ]
        
        for k in range( len( stdLists ) ):
            currentParentCtl = self.rigBase
            for i in range( len( stdLists[k] ) ):
                ctl = makeController( sgdata.Controllers.cubePoints, self.controllerSize, n= stdLists[k][i].name().replace( self.stdPrefix, 'Ctl_' ), 
                                      makeParent=1 )
                ctl.setAttr( 'shape_ty', 0.13  )
                pCtl = ctl.parent()
                stdLists[k][i].t >> pCtl.t
                stdLists[k][i].r >> pCtl.r
                ctlLists[k].append( ctl )
                parent( pCtl, currentParentCtl )
                currentParentCtl = ctl
    


    def createJoints(self):
        
        ctlLists = [ self.thumbCtls, self.indexCtls, self.middleCtls, self.ringCtls, self.pinkyCtls ]
        
        select( d=1 )
        baseJoint = joint()
        constrain_parent( self.rigBase, baseJoint )
        
        self.thumbJnts = []
        self.indexJnts = []
        self.middleJnts = []
        self.ringJnts = []
        self.pinkyJnts = []
        
        jntLists = [ self.thumbJnts, self.indexJnts, self.middleJnts, self.ringJnts, self.pinkyJnts ]
        lookAtDirection = [1,0,0]
        if self.thumbStds[0].tx.get() < 0:
            lookAtDirection = [-1,0,0]
        
        for i in range( len( ctlLists ) ):
            select( baseJoint )
            ctlParent = self.rigBase
            for j in range( len( ctlLists[i] ) ):
                newJoint = joint()
                dcmpMove = getDecomposeMatrix( getLocalMatrix( ctlLists[i][j], ctlParent) )
                dcmpOrig = getDecomposeMatrix( getLocalMatrix( ctlLists[i][j].parent(), ctlParent) )
                distanceMove = getDistance( dcmpMove )
                distanceOrig = getDistance( dcmpOrig )
                div = createNode( 'multiplyDivide' ).setAttr( 'op', 2 )
                distanceMove.distance >> div.input1X
                distanceOrig.distance >> div.input2X
                if j != 0:
                    div.outputX >> jntLists[i][j-1].sx
                    aimConstraint( ctlLists[i][j], jntLists[i][j-1], aim=lookAtDirection, u=[0,0,1], wu=[0,0,1], wut='objectrotation', wuo=ctlLists[i][j-1] )
                    dcmpOrig.ot >> newJoint.t
                else:
                    constrain_point( ctlLists[i][j], newJoint )

                jntLists[i].append( newJoint )
                select( newJoint )
                
                ctlParent = ctlLists[i][j]
        
        self.resultJnts = [baseJoint] + jntLists
        
        
    
    
    def createFingerAttributeControl(self):
        
        self.stdPrefix       = 'StdJnt_'
        self.stdGripPrefix   = 'StdJntGrip_'
        self.stdSpreadPrefix = 'StdJntSpread_'
        
        _SIDE_ = self.getSide( self.thumbStds[0] )
        self.ctlFinger = makeController( sgdata.Controllers.circlePoints, self.controllerSize, n='Ctl_Finger' + _SIDE_, 
                                         makeParent=1, colorIndex = self.colorIndex )
        transMult = 1
        if self.thumbStds[0].tx.get() < 0:
            transMult = -1
        self.ctlFinger.setAttr( 'shape_tx', 2.5 * transMult ).setAttr( 'shape_ty', 1.5 * transMult ).setAttr( 'shape_sx', 2 ).setAttr( 'shape_sy', 2 ).setAttr( 'shape_sz', 2 )
        pCtlFinger = self.ctlFinger.parent()
        pCtlFinger.parentTo( self.rigBase )
        pCtlFinger.setTransformDefault()
        
        addOptionAttribute( self.ctlFinger )
        self.ctlFinger.addAttr( ln='grip', k=1 )
        self.ctlFinger.addAttr( ln='spread', k=1 )
        
        stdLists = [ self.thumbStds, self.indexStds, self.middleStds, self.ringStds, self.pinkyStds ]
        ctlLists = [ self.thumbCtls, self.indexCtls, self.middleCtls, self.ringCtls, self.pinkyCtls ]
        
        for i in range( len( stdLists ) ):
            for j in range( len( stdLists[i] ) ):
                gripStd = convertSg( stdLists[i][j].name().replace( self.stdPrefix, self.stdGripPrefix ) )
                spreadStd = convertSg( stdLists[i][j].name().replace( self.stdPrefix, self.stdSpreadPrefix ) )
                offsetCtl = makeParent( ctlLists[i][j] ).rename( 'Offset' + ctlLists[i][j].name() )
                
                multGrip   = createNode( 'multiplyDivide' )
                multSpread = createNode( 'multiplyDivide' )
                plusNode   = createNode( 'plusMinusAverage' )
                
                gripStd.r >> multGrip.input1
                spreadStd.r >> multSpread.input1
                self.ctlFinger.grip >> multGrip.input2X
                self.ctlFinger.grip >> multGrip.input2Y
                self.ctlFinger.grip >> multGrip.input2Z
                self.ctlFinger.spread >> multSpread.input2X
                self.ctlFinger.spread >> multSpread.input2Y
                self.ctlFinger.spread >> multSpread.input2Z
                multGrip.output >> plusNode.input3D[0]
                multSpread.output >> plusNode.input3D[1]
                divNode = createNode( 'multiplyDivide' )
                plusNode.output3D >> divNode.input1
                divNode.input2.set( 0.1, 0.1, 0.1 )
                
                divNode.output >> offsetCtl.r
                
            
    






class StdControl:
    
    def __init__(self):
        pass
    

    @convertSg_dec
    def setSymmetryElement( self, sel ):
    
        matList = sel.wm.get()
        
        matList[1]  *= -1
        matList[2]  *= -1
        matList[5]  *= -1
        matList[6]  *= -1
        matList[9] *= -1
        matList[10] *= -1
        matList[12] *= -1
        sel.xform( ws=1, matrix= matList )
    
    
    
    @convertSg_dec
    def setSymmetryElement_trans(self, sel ):
        
        matList = sel.wm.get()
        
        matList[12] *= -1
        sel.xform( ws=1, matrix= matList )
        


    
    @convertSg_dec
    def setSymmetry( self, targetStd, **options ):
        
        fromSide = '_L_'
        toSide = '_R_'
        
        if options.has_key( 'from' ):
            fromSide = options['from']
        if options.has_key( 'to' ):
            toSide = options['to']
        
        symtype = 'default'
        if options.has_key( 'symtype' ):
            symtype = options['symtype']
        
        ns = targetStd.name().split( 'Std_' )[0]
        
        stds = listNodes( ns + 'Std_*', type='transform' )
        
        for std in stds:
            if std.name().find( fromSide ) == -1: continue
            if not cmds.objExists( std.name().replace( fromSide, toSide ) ): continue
            
            stdToSide = convertSg( std.name().replace( fromSide, toSide ) )
            
            if symtype == 'trans':
                origMtx = std.wm.get()
                stdToSide.xform( ws=1, t= origMtx[12:-1] )
                self.setSymmetryElement_trans( stdToSide )
            else:
                stdToSide.xform( ws=1, matrix= std.wm.get() )
                self.setSymmetryElement( stdToSide )
            





def createHumanByStd( controllerSize = 1 ):
    
    bodyRig = BodyRig( *Std.getBodyList() )
    bodyRig.createAll( controllerSize )
    cmds.refresh()
    
    bodyRig.createClavicleConnector( Std.clavicle_SIDE_.replace( '_SIDE_', '_L_'), Std.clavicle_SIDE_.replace( '_SIDE_', '_R_'))
    bodyRig.createHipConnector( Std.leg_SIDE_00.replace( '_SIDE_', '_L_'), Std.leg_SIDE_00.replace( '_SIDE_', '_R_') )
    bodyRig.createNeckConnector( Std.neck )
    cmds.refresh()
    
    headRig = HeadRig( *Std.getHeadList() )
    headRig.createAll( controllerSize )
    constrain_parent( bodyRig.connectorNeck, headRig.rigBase )
    cmds.refresh()
    
    leftClavicleRig = ClavicleRig( *Std.getLeftClavicleList() )
    leftClavicleRig.createAll(controllerSize, HumanRig.leftColor )
    constrain_parent( bodyRig.connectorClavicleL, leftClavicleRig.rigBase )
    cmds.refresh()
    
    leftArmRig = ArmRig( *Std.getLeftArmList() )
    leftArmRig.createAll( controllerSize, HumanRig.leftColor  )
    constrain_parent( leftClavicleRig.connector, leftArmRig.rigBase )
    cmds.refresh()
    
    leftLegRig = LegRig( *Std.getLeftLegList() )
    leftLegRig.createAll( controllerSize, HumanRig.leftColor  )
    constrain_parent( bodyRig.connectorHipL, leftLegRig.rigBase )
    cmds.refresh()
    
    leftHandRig = HandRig( *Std.getLeftHandList() )
    leftHandRig.createAll( controllerSize * 0.3, HumanRig.leftColor )
    constrain_parent( leftArmRig.connector, leftHandRig.rigBase )
    cmds.refresh()
    
    rightClavicleRig = ClavicleRig( *Std.getRightClavicleList() )
    rightClavicleRig.createAll(controllerSize, HumanRig.rightColor )
    constrain_parent( bodyRig.connectorClavicleR, rightClavicleRig.rigBase )
    cmds.refresh()
    
    rightArmRig = ArmRig( *Std.getRightArmList() )
    rightArmRig.createAll( controllerSize, HumanRig.rightColor )
    constrain_parent( rightClavicleRig.connector, rightArmRig.rigBase )
    cmds.refresh()
    
    rightLegRig = LegRig( *Std.getRightLegList() )
    rightLegRig.createAll( controllerSize, HumanRig.rightColor )
    constrain_parent( bodyRig.connectorHipR, rightLegRig.rigBase )
    cmds.refresh()
    
    rightHandRig = HandRig( *Std.getRightHandList() )
    rightHandRig.createAll( controllerSize * 0.3, HumanRig.rightColor )
    constrain_parent( rightArmRig.connector, rightHandRig.rigBase )
    cmds.refresh()
    
    parent( headRig.resultJnts[0], bodyRig.resultJnts[-1] ); headRig.resultJnts[0].jo.set(0,0,0)
    parent( leftClavicleRig.resultJnts[0], bodyRig.resultJnts[-1] ); leftClavicleRig.resultJnts[0].jo.set(0,0,0)
    parent( rightClavicleRig.resultJnts[0], bodyRig.resultJnts[-1] ); rightClavicleRig.resultJnts[0].jo.set(0,0,0)
    parent( leftArmRig.resultJnts[0], leftClavicleRig.resultJnts[-1] ); leftArmRig.resultJnts[0].jo.set(0,0,0)
    parent( rightArmRig.resultJnts[0], rightClavicleRig.resultJnts[-1] ); rightArmRig.resultJnts[0].jo.set(0,0,0)
    parent( leftHandRig.resultJnts[0], leftArmRig.resultJnts[-1] ); leftHandRig.resultJnts[0].jo.set(0,0,0)
    parent( rightHandRig.resultJnts[0], rightArmRig.resultJnts[-1] ); rightHandRig.resultJnts[0].jo.set(0,0,0)
    parent( leftLegRig.resultJnts[0], bodyRig.resultJnts[0] ); leftLegRig.resultJnts[0].jo.set(0,0,0)
    parent( rightLegRig.resultJnts[0], bodyRig.resultJnts[0] ); rightLegRig.resultJnts[0].jo.set(0,0,0)
    cmds.refresh()
    
    ctlsGrp = createNode( 'transform', n='ctls' )
    ctlWorld = makeController( sgdata.Controllers.circlePoints, controllerSize * 3.5, n='Ctl_World', makeParent=1, colorIndex=6 )
    pCtlWorld = ctlWorld.parent()
    ctlMove  = makeController( sgdata.Controllers.crossArrowPoints, controllerSize * 3, n='Ctl_Move', makeParent=1, colorIndex = 29 )
    pCtlMove = ctlMove.parent()
    ctlFly  = makeController( sgdata.Controllers.flyPoints, controllerSize * 2, n='Ctl_Fly', makeParent=1, colorIndex=15 )
    ctlFly.setAttr( 'shape_sy', 1.5 ).setAttr( 'shape_tz', -1 ).setAttr( 'shape_ty', 0.2 )
    pCtlFly = ctlFly.parent()
    pCtlFly.xform( ws=1, matrix= bodyRig.ctlRoot.parent().wm.get() )
    
    parent( pCtlFly, ctlMove )
    parent( pCtlMove, ctlWorld )
    parent( pCtlWorld, ctlsGrp )
    
    rootDcmp = getDecomposeMatrix( getLocalMatrix( Std.root, Std.base ) )
    rootDcmp.outputTranslate >> pCtlFly.t
    rootDcmp.outputRotate >> pCtlFly.r
    
    parent( bodyRig.rigBase, ctlFly )
    parent( headRig.rigBase, ctlFly )
    parent( leftClavicleRig.rigBase, ctlFly )
    parent( rightClavicleRig.rigBase, ctlFly )
    parent( leftArmRig.rigBase, ctlFly )
    parent( rightArmRig.rigBase, ctlFly )
    parent( leftHandRig.rigBase, ctlFly )
    parent( rightHandRig.rigBase, ctlFly )
    parent( leftLegRig.rigBase, ctlFly )
    parent( rightLegRig.rigBase, ctlFly )
    
    jntGrp = createNode( 'transform', n='jointGrp' )
    parent( bodyRig.resultJnts[0], jntGrp )
    constrain_all( ctlFly, jntGrp )
    
    rigGrp = createNode( 'transform', n='rig' )
    parent( jntGrp, ctlsGrp, rigGrp )



class FollowingIk:
    
    stdBase  = 'StdJnt_Base'
    stdRoot  = 'StdJnt_Root'
    stdShoulder_SIDE_ = 'StdJnt_Arm_SIDE_00'
    stdHip_SIDE_   = 'StdJnt_Leg_SIDE_00'
    stdWrist_SIDE_ = 'StdJnt_Arm_SIDE_02'
    stdAnkle_SIDE_ = 'StdJnt_Leg_SIDE_02'
    
    world     = 'Ctl_World'
    move     = 'Ctl_Move'
    fly      = 'Ctl_Fly'
    root     = 'Ctl_Root'
    chest    = 'Ctl_Chest'
    
    armBase_SIDE_ = 'RigBase_Arm_SIDE_00'
    legBase_SIDE_ = 'RigBase_Leg_SIDE_00'
    armIk_SIDE_ = 'Ctl_IkArm_SIDE_02'
    legIk_SIDE_ = 'Ctl_IkLeg_SIDE_02'
    
    def __init__(self, targetIk, targetBase, targetStd, targetBaseStd ):
        
        self.targetBase = pymel.core.ls( targetBase )[0]
        self.targetBaseStd = pymel.core.ls( targetBaseStd )[0]
        self.targetIk = pymel.core.ls( targetIk )[0]
        self.targetStd = pymel.core.ls( targetStd )[0]
    

    def create(self, *targets ):
        
        origPointer = pymel.core.createNode( 'transform' )
        pymel.core.parent( origPointer, self.targetBase )
        
        def getLocalDecomposeMatrix( localObj, parentObj ):
            
            localObj = pymel.core.ls( localObj )[0]
            parentObj = pymel.core.ls( parentObj )[0]
            
            mm = pymel.core.createNode( 'multMatrix' )
            dcmp = pymel.core.createNode( 'decomposeMatrix' )
            compose = pymel.core.createNode( 'composeMatrix' )
            dcmpTrans = pymel.core.createNode( 'decomposeMatrix' )
            localObj.wm >> dcmpTrans.imat
            dcmpTrans.ot >> compose.it
            compose.outputMatrix >> mm.i[0]
            parentObj.wim >> mm.i[1]
            mm.o >> dcmp.imat
            return dcmp
        
        origDcmp = getLocalDecomposeMatrix( self.targetStd, self.targetBaseStd )
        origPointer = pymel.core.createNode( 'transform' )
        origDcmp.ot >> origPointer.t
        origDcmp.outputRotate >> origPointer.r
        pymel.core.parent( origPointer, self.targetBase )

        blendMatrix = pymel.core.createNode( 'wtAddMatrix' )
        origPointer.wm >> blendMatrix.i[0].m
        
        sumWeight = pymel.core.createNode( 'plusMinusAverage' )
        rangeNode = pymel.core.createNode( 'setRange' )
        revNode   = pymel.core.createNode( 'reverse' )
        sumWeight.output1D >> rangeNode.valueX; rangeNode.maxX.set( 1 ); rangeNode.oldMaxX.set( 1 )
        rangeNode.outValueX >> revNode.inputX
        revNode.outputX >> blendMatrix.i[0].w
        
        divSumNode = pymel.core.createNode( 'condition' )
        divSumNode.secondTerm.set( 1 ); divSumNode.operation.set( 2 ); divSumNode.colorIfFalseR.set( 1 )
        sumWeight.output1D >> divSumNode.firstTerm
        sumWeight.output1D >> divSumNode.colorIfTrueR
        divSumAttr = divSumNode.outColorR

        addOptionAttribute( self.targetIk.name(), 'followOptions' )

        wIndex = 1
        for targetCtl, targetStd in targets:
            
            if not pymel.core.objExists( targetCtl ):
                print "%s is not exists" % targetCtl
                continue
            if not pymel.core.objExists( targetStd ):
                print "%s is not exists" % targetStd
                continue
            
            targetCtl = pymel.core.ls( targetCtl )[0]
            targetStd = pymel.core.ls( targetStd )[0]
            
            cuLocalDcmp = getLocalDecomposeMatrix( self.targetStd, targetStd )
            cuPointer = pymel.core.createNode( 'transform' )
            cuLocalDcmp.ot >> cuPointer.t
            cuLocalDcmp.outputRotate >> cuPointer.r
            cuPointer.rename(  'fPointer_' + self.targetIk.name() + '_in_' + targetCtl.name() )
            pymel.core.parent( cuPointer, targetCtl )
            cuPointer.wm >> blendMatrix.i[wIndex].m
            
            try:self.targetIk.addAttr( 'follow_%s' % targetCtl.name(), k=1, min=0, max=1, dv=0 )
            except:pass
            divWeight = pymel.core.createNode( 'multiplyDivide' ); divWeight.op.set( 2 )
            self.targetIk.attr( 'follow_%s' % targetCtl.name() ) >> divWeight.input1X
            divSumAttr >> divWeight.input2X
            divWeight.outputX >> blendMatrix.i[wIndex].w
            
            self.targetIk.attr( 'follow_%s' % targetCtl.name() ) >> sumWeight.input1D[ wIndex -1 ]
            
            wIndex += 1
        
        multMtx = pymel.core.createNode( 'multMatrix' )
        dcmp = pymel.core.createNode( 'decomposeMatrix' )
        blendMatrix.matrixSum >> multMtx.i[0]
        self.targetIk.getParent().pim >> multMtx.i[1]
        multMtx.matrixSum >> dcmp.imat
        
        dcmp.ot >> self.targetIk.getParent().t
        dcmp.outputRotate >> self.targetIk.getParent().r
    


    @staticmethod
    def getLeftArmList():
        
        replaceList = ( '_SIDE_', '_L_' )
        rigBase = FollowingIk.armBase_SIDE_.replace( *replaceList )
        ik = FollowingIk.armIk_SIDE_.replace( *replaceList )
        stdBase = FollowingIk.stdShoulder_SIDE_.replace( *replaceList )
        stdIk = FollowingIk.stdWrist_SIDE_.replace( *replaceList )
        return ik, rigBase, stdIk, stdBase 


    @staticmethod
    def getRightArmList():
        
        replaceList = ( '_SIDE_', '_R_' )
        rigBase = FollowingIk.armBase_SIDE_.replace( *replaceList )
        ik = FollowingIk.armIk_SIDE_.replace( *replaceList )
        stdBase = FollowingIk.stdShoulder_SIDE_.replace( *replaceList )
        stdIk = FollowingIk.stdWrist_SIDE_.replace( *replaceList )
        return ik, rigBase, stdIk, stdBase
    


    @staticmethod
    def getLeftLegList():
        
        replaceList = ( '_SIDE_', '_L_' )
        rigBase = FollowingIk.legBase_SIDE_.replace( *replaceList )
        ik = FollowingIk.legIk_SIDE_.replace( *replaceList )
        stdBase = FollowingIk.stdHip_SIDE_.replace( *replaceList )
        stdIk = FollowingIk.stdAnkle_SIDE_.replace( *replaceList )
        return ik, rigBase, stdIk, stdBase



    @staticmethod
    def getRightLegList():
        
        replaceList = ( '_SIDE_', '_R_' )
        rigBase = FollowingIk.legBase_SIDE_.replace( *replaceList )
        ik = FollowingIk.legIk_SIDE_.replace( *replaceList )
        stdBase = FollowingIk.stdHip_SIDE_.replace( *replaceList )
        stdIk = FollowingIk.stdAnkle_SIDE_.replace( *replaceList )
        return ik, rigBase, stdIk, stdBase
    


    @staticmethod
    def getFollowList():
        
        return [ [FollowingIk.root, FollowingIk.stdRoot], 
                 [FollowingIk.fly, FollowingIk.stdRoot],
                 [FollowingIk.move, FollowingIk.stdBase],
                 [FollowingIk.world, FollowingIk.stdBase]]
    
    
    @staticmethod
    def createAll():
        
        armIkLeft = FollowingIk( *FollowingIk.getLeftArmList() )
        armIkLeft.create( *FollowingIk.getFollowList() )
        armIkRight = FollowingIk( *FollowingIk.getRightArmList() )
        armIkRight.create( *FollowingIk.getFollowList() )
        
        legIkLeft = FollowingIk( *FollowingIk.getLeftLegList() )
        legIkLeft.create( *FollowingIk.getFollowList() )
        legIkRight = FollowingIk( *FollowingIk.getRightLegList() )
        legIkRight.create( *FollowingIk.getFollowList() )
        
        

    
    


@convertSg_dec
def createRigedCurve( *ctls ):
    
    firstCtl = ctls[0]
    firstCtlNext = ctls[1]
    lastCtlBefore = ctls[-2]
    lastCtl = ctls[-1]
    
    firstCtl.addAttr( ln='frontMult', cb=1, dv=0.3 )
    lastCtl.addAttr( ln='backMult', cb=1, dv=0.3 )
    
    firstPointerGrp = createNode( 'transform' )
    firstPointer1 = firstPointerGrp.makeChild()
    firstPointer2 = firstPointerGrp.makeChild()
    firstPointerGrp.parentTo( firstCtl ).setTransformDefault()
    
    lastPointerGrp = createNode( 'transform' )
    lastPointer1 = lastPointerGrp.makeChild()
    lastPointer2 = lastPointerGrp.makeChild()
    lastPointerGrp.parentTo( lastCtl ).setTransformDefault()
    
    dcmpFirst = getDecomposeMatrix( getLocalMatrix( firstCtlNext, firstCtl ) )
    distFirst = getDistance( dcmpFirst )
    dcmpLast = getDecomposeMatrix( getLocalMatrix( lastCtlBefore, lastCtl ) ) 
    distLast = getDistance( dcmpLast )
    
    firstDirIndex = getDirectionIndex( dcmpFirst.ot.get() )
    firstReverseMult = -1 if firstDirIndex >= 3 else 1
    firstTargetAttr = ['tx','ty','tz'][firstDirIndex%3]
    lastDirIndex = getDirectionIndex( dcmpLast.ot.get() )
    lastReverseMult = -1 if lastDirIndex >= 3 else 1
    lastTargetAttr  = ['tx','ty','tz'][lastDirIndex%3]
    
    multFirstPointer1 = createNode( 'multDoubleLinear' ).setAttr( 'input2',  0.05 * firstReverseMult )
    multFirstPointer2 = createNode( 'multDoubleLinear' ).setAttr( 'input2',  0.3 * firstReverseMult )
    multLastPointer1 = createNode( 'multDoubleLinear' ).setAttr( 'input2',  0.05 * lastReverseMult )
    multLastPointer2 = createNode( 'multDoubleLinear' ).setAttr( 'input2',  0.3 * lastReverseMult )
    firstCtl.frontMult >> multFirstPointer2.input2
    lastCtl.backMult >> multFirstPointer2.input2
    
    distFirst.distance >> multFirstPointer1.input1
    distFirst.distance >> multFirstPointer2.input1
    multFirstPointer1.output >> firstPointer1.attr( firstTargetAttr )
    multFirstPointer2.output >> firstPointer2.attr( lastTargetAttr )
    
    distLast.distance >> multLastPointer1.input1
    distLast.distance >> multLastPointer2.input1
    multLastPointer1.output >> lastPointer1.attr( firstTargetAttr )
    multLastPointer2.output >> lastPointer2.attr( lastTargetAttr )
    
    pointerList = [firstPointerGrp, firstPointer1, firstPointer2, lastPointer2, lastPointer1, lastPointerGrp]
    
    for i in range( 1, len( ctls )-1 ):
        beforeCtl = ctls[i-1]
        ctl = ctls[i]
        nextCtl = ctls[i+1]
        
        ctlPointerGrp = ctl.makeChild()
        ctlPointer1 = ctlPointerGrp.makeChild()
        ctlPointer2 = ctlPointerGrp.makeChild()
        
        dcmpBefore = getDecomposeMatrix( getLocalMatrix( beforeCtl, ctl ) )
        distBefore = getDistance( dcmpBefore )
        dcmpAfter  = getDecomposeMatrix( getLocalMatrix( nextCtl, ctl ) ) 
        distAfter  = getDistance( dcmpAfter )
        
        dirIndexB = getDirectionIndex( dcmpBefore.ot.get() )
        reverseMultB = -1 if dirIndexB >= 3 else 1
        targetAttrB = ['tx','ty','tz'][dirIndexB%3]
        dirindexA = getDirectionIndex( dcmpAfter.ot.get() )
        reverseMultA = -1 if dirindexA >= 3 else 1
        targetAttrA = ['tx','ty','tz'][dirindexA%3]
        
        ctl.addAttr( 'beforeMult', dv=0.3, cb=1 )
        ctl.addAttr( 'afterMult', dv=0.3, cb=1 )
        multBefore = createNode( 'multDoubleLinear' ).setAttr( 'input2', reverseMultB )
        multAfter  = createNode( 'multDoubleLinear' ).setAttr( 'input2', reverseMultA )
        ctl.beforeMult >> multBefore.input1
        ctl.afterMult  >> multAfter.input1
        
        multBeforePointer = createNode( 'multDoubleLinear' ).setAttr( 'input2',  0.3 * reverseMultB )
        multAfterPointer  = createNode( 'multDoubleLinear' ).setAttr( 'input2',  0.3 * reverseMultA )
        
        distBefore.distance >> multBeforePointer.input1
        distAfter.distance >> multAfterPointer.input1
        multBefore.output >> multBeforePointer.input2
        multAfter.output >> multAfterPointer.input2
        
        multBeforePointer.output >> ctlPointer1.attr( targetAttrB )
        multAfterPointer.output >> ctlPointer2.attr( targetAttrA )
        
        pointerList.insert( -3, ctlPointer1 )
        pointerList.insert( -3, ctlPointer2 )

    return makeCurveFromSelection( pointerList )


@convertSg_dec
def getMultDoubleLinear( node=None ):
    
    multNode = createNode( 'multDoubleLinear' )
    
    if node:
        if node.nodeType() == 'distanceBetween':
            node.distance >> multNode.input1
    
    return multNode



@convertSg_dec
def createSquashBend( *geos ):    
    if not type( geos ) in [ list, tuple ]:
        geos = [geos]
    
    allbb = OpenMaya.MBoundingBox()
    for geo in geos:
        bb = cmds.exactWorldBoundingBox( geo.name() )
        bbmin = bb[:3]
        bbmax = bb[3:]
        pointer00 = OpenMaya.MPoint( *bbmin )
        pointer01 = OpenMaya.MPoint( *bbmax )
        allbb.expand( pointer00 )
        allbb.expand( pointer01 )
    
    bbmin = allbb.min()
    bbmax = allbb.max()
    center = allbb.center()
    
    upperPoint = [ center.x, bbmax.y, center.z ]
    lowerPoint = [ center.x, bbmin.y, center.z ]
    
    dist = OpenMaya.MPoint( *upperPoint ).distanceTo( OpenMaya.MPoint( *lowerPoint ) )
    squashBase = createNode( 'transform', n='sauashBase' ).setAttr( 't', lowerPoint )
    upperCtl = makeController( sgdata.Controllers.trianglePoints, dist*0.2 )
    upperCtl.setAttr( 'shape_ty', 1 ).setAttr( 'shape_rz', 180 )
    pUpperCtl = makeParent( upperCtl )
    lowerCtl = makeController( sgdata.Controllers.trianglePoints, dist*0.2 )
    lowerCtl.setAttr( 'shape_ty', -1 )
    pLowerCtl = makeParent( lowerCtl )
    upperCtl.rename( 'Ctl_Upper' )
    lowerCtl.rename( 'Ctl_Lower' )
    pUpperCtl.t.set( *upperPoint )
    pLowerCtl.t.set( *lowerPoint )
    
    parent( pUpperCtl, squashBase )
    parent( pLowerCtl, squashBase )
    
    squashCenter = squashBase.makeChild().rename( 'squashCenter' ).setAttr( 'dh', 1 )
    blendMtxNode = getBlendTwoMatrixNode( upperCtl, lowerCtl )
    multMtx = createNode( 'multMatrix' )
    blendMtxNode.matrixSum >> multMtx.i[0]
    squashBase.attr( 'pim' ) >> multMtx.i[1]
    dcmpBlend = getDecomposeMatrix( multMtx )
    dcmpBlend.oty >> squashCenter.ty
    
    rigedCurve = createRigedCurve( upperCtl, lowerCtl )
    upperFirstChild = upperCtl.listRelatives( c=1, type='transform' )[0]
    lowerFirstChild = lowerCtl.listRelatives( c=1, type='transform' )[0]
    parent( rigedCurve, squashBase )
    
    lookAtUpper = upperCtl.makeChild().rename( 'lookAtObj_' + upperCtl.name() )
    lookAtLower = lowerCtl.makeChild().rename( 'lookAtObj_' + lowerCtl.name() )
    lookAtConnect( squashCenter, lookAtUpper )
    lookAtConnect( squashCenter, lookAtLower )
    
    multLookAtUpper = createNode( 'multiplyDivide' )
    multLookAtLower = createNode( 'multiplyDivide' )
    
    lookAtUpper.r >> multLookAtUpper.input1
    lookAtLower.r >> multLookAtLower.input1
    addOptionAttribute( upperCtl )
    addOptionAttribute( lowerCtl )
    upperCtl.addAttr( ln='autoOrient', min=0, max=1, dv=1, k=1 )
    lowerCtl.addAttr( ln='autoOrient', min=0, max=1, dv=1, k=1 )
    upperCtl.autoOrient >> multLookAtUpper.input2X
    upperCtl.autoOrient >> multLookAtUpper.input2Y
    upperCtl.autoOrient >> multLookAtUpper.input2Z
    lowerCtl.autoOrient >> multLookAtLower.input2X
    lowerCtl.autoOrient >> multLookAtLower.input2Y
    lowerCtl.autoOrient >> multLookAtLower.input2Z
    
    multLookAtUpper.output >> upperFirstChild.r
    multLookAtLower.output >> lowerFirstChild.r
    
    select( geos )
    flare, flareHandle = cmds.nonLinear( type='flare', lowBound=-1.5, highBound=1.5 )
    cmds.setAttr( flareHandle + '.v', 0 )
    flare       = convertSg( flare )
    parent( flareHandle, squashBase )
    
    select( geos )
    wireNode, curveName = cmds.wire( gw=False, en=1, ce=0.0, li=0.0, w=rigedCurve.name() )
    wireNode = convertSg( wireNode )
    wireNode.attr( 'dropoffDistance[0]' ).set( 1000000.0 )
    baseCurve = wireNode.baseWire[0].listConnections( s=1, d=0, type='nurbsCurve' )[0]
    baseCurve = convertSg( baseCurve )
    
    curveInfoMoveCurve = createNode( 'curveInfo' )
    curveInfoOrigCurve = createNode( 'curveInfo' ) 
    
    rigedCurve.shape().attr( 'local' ) >> curveInfoMoveCurve.inputCurve
    baseCurve.shape().attr( 'local' ) >> curveInfoOrigCurve.inputCurve
    
    divNode = createNode( 'multiplyDivide' ).setAttr( 'op', 2 )
    curveInfoMoveCurve.arcLength >> divNode.input2X
    curveInfoOrigCurve.arcLength  >> divNode.input1X
    addNode = createNode( 'addDoubleLinear' ).setAttr( 'input2', -1 )
    divNode.outputX >> addNode.input1
    addNode.output >> flare.curve
    
    lowerCtl.sx >> flare.startFlareX
    lowerCtl.sz >> flare.startFlareZ
    upperCtl.sx >> flare.endFlareX
    upperCtl.sz >> flare.endFlareZ
    
    pass




def makeCloneObject( target, cloneLabel= '_clone', **options  ):
    
    target = pymel.core.ls( target )[0]
    
    op_cloneAttrName = 'iscloneObj'
    op_shapeOn       = False
    op_connectionOn  = False

    targets = target.getAllParents()
    targets.reverse()
    targets.append( target )
    
    def getSourceConnection( src, trg ):
        src = pymel.core.ls( src )[0]
        trg = pymel.core.ls( trg )[0]
        cons = src.listConnections( s=1, d=0, p=1, c=1 )
    
        if not cons: return None
    
        for destCon, srcCon in cons:
            srcCon = srcCon.name()
            destCon = destCon.name().replace( src, trg )
            if cmds.nodeType( src ) == 'joint' and cmds.nodeType( trg ) =='transform':
                destCon = destCon.replace( 'jointOrient', 'rotate' )
            if not cmds.ls( destCon ): continue
            if not cmds.isConnected( srcCon, destCon ):
                cmds.connectAttr( srcCon, destCon, f=1 )

    targetCloneParent = None
    for cuTarget in targets:
        if not pymel.core.attributeQuery( op_cloneAttrName, node=cuTarget, ex=1 ):
            cuTarget.addAttr( op_cloneAttrName, at='message' )
        cloneConnection = cuTarget.attr( op_cloneAttrName ).listConnections(s=1, d=0 )
        if not cloneConnection:
            targetClone = pymel.core.createNode( 'transform', n= cuTarget.split( '|' )[-1]+cloneLabel )
            targetClone.message >> cuTarget.attr( op_cloneAttrName )
            
            if op_shapeOn:
                cuTargetShape = cuTarget.getShape()
                if cuTargetShape:
                    duObj = pymel.core.duplicate( cuTarget, n=targetClone+'_du' )[0]
                    duShape = duObj.getShape()
                    pymel.core.parent( duShape, targetClone, add=1, shape=1 )[0]
                    duShape.rename( targetClone+'Shape' )
            if op_connectionOn:
                getSourceConnection( cuTarget, targetClone )
                cuTargetShape    = cuTarget.getShape()
                targetCloneShape = targetClone.getShape()
                
                if cuTargetShape and targetCloneShape:
                    getSourceConnection( cuTargetShape, targetCloneShape )
        else:
            targetClone = cloneConnection[0]
        
        targetCloneParentExpected = targetClone.getParent()
        if targetCloneParent and targetCloneParentExpected != targetCloneParent:
            pymel.core.parent( targetClone, targetCloneParent )

        cuTargetPos = cuTarget.m.get()
        pymel.core.xform( targetClone, os=1, matrix=cuTargetPos )

        targetCloneParent = targetClone
    return targetCloneParent.name()




def copyShader( srcObj, dstObj ):
    
    srcObj = pymel.core.ls( srcObj )[0]
    dstObj = pymel.core.ls( dstObj )[0]
    
    if srcObj.type() == 'transform':
        srcObj = srcObj.getShape()
    if dstObj.type() == 'transform':
        dstObj = dstObj.getShape()
    
    shadingEngine = srcObj.listConnections( s=0, d=1, type='shadingEngine' )
    if not shadingEngine:
        cmds.warning( "%s has no shading endgine" % srcObj.name )
        return None
    cmds.sets( dstObj.name(), e=1, forceElement = shadingEngine[0].name() )




def getDestMesh( meshGrp ):
    
    meshGrp = pymel.core.ls( meshGrp )[0]
    children = meshGrp.listRelatives( c=1, ad=1, type='transform' )
    children.append( meshGrp )
    
    targetMeshs = []
    for child in children:
        childShape = child.getShape()
        if not childShape: continue
        if childShape.type() != 'mesh': continue
        targetMeshs.append( child )
    
    for targetMesh in targetMeshs:
        meshShape = targetMesh.getShape()
        clonedTransform = makeCloneObject( targetMesh )
        copyShapeToTransform( meshShape.name(), clonedTransform )
        
        clonedTransform = pymel.core.ls( clonedTransform )[0]
        clonedShape = clonedTransform.getShape()
        
        meshShape.outMesh >> clonedShape.inMesh
        
        copyShader( meshShape, clonedShape )






def createFourByFourMatrixCube( target ):
    
    cubeObj, cubeNode = pymel.core.polyCube( ch=1, o=1, cuv=4 )
    
    xVtx = cubeObj.name() + '.vtx[7]'
    yVtx = cubeObj.name() + '.vtx[4]'
    zVtx = cubeObj.name() + '.vtx[0]'
    pVtx = cubeObj.name() + '.vtx[6]'
    
    xFollicle = createFollicleOnVertex( xVtx, True, False )
    yFollicle = createFollicleOnVertex( yVtx, True, False )
    zFollicle = createFollicleOnVertex( zVtx, True, False )
    pFollicle = createFollicleOnVertex( pVtx, True, False )
    
    cubeObj.addAttr( 'size', dv=1, k=1 )
    
    cubeShape = cubeObj.getShape()
    composeOffset = pymel.core.createNode( 'composeMatrix' )
    composeScale  = pymel.core.createNode( 'composeMatrix' )
    multMatrix = pymel.core.createNode( 'multMatrix' )
    trGeo = pymel.core.createNode( 'transformGeometry' )
    composeOffset.it.set( .5, .5, .5 )
    cubeObj.size >> composeScale.isx
    cubeObj.size >> composeScale.isy
    cubeObj.size >> composeScale.isz
    composeOffset.outputMatrix >> multMatrix.i[0]
    composeScale.outputMatrix >> multMatrix.i[1]
    cubeNode.output >> trGeo.inputGeometry
    multMatrix.matrixSum >> trGeo.transform
    trGeo.outputGeometry >> cubeShape.inMesh
    
    xDcmp = getDecomposeMatrix( getLocalMatrix( xFollicle, pFollicle ) )
    yDcmp = getDecomposeMatrix( getLocalMatrix( yFollicle, pFollicle ) )
    zDcmp = getDecomposeMatrix( getLocalMatrix( zFollicle, pFollicle ) )
    
    pFollicle = pymel.core.ls( pFollicle )[0]
    cubeObj.size >> pFollicle.sx
    cubeObj.size >> pFollicle.sy
    cubeObj.size >> pFollicle.sz
    
    fbf = pymel.core.createNode( 'fourByFourMatrix' )
    xDcmp.otx >> fbf.in00
    xDcmp.oty >> fbf.in01
    xDcmp.otz >> fbf.in02
    yDcmp.otx >> fbf.in10
    yDcmp.oty >> fbf.in11
    yDcmp.otz >> fbf.in12
    zDcmp.otx >> fbf.in20
    zDcmp.oty >> fbf.in21
    zDcmp.otz >> fbf.in22
    pFollicle.tx >> fbf.in30
    pFollicle.ty >> fbf.in31
    pFollicle.tz >> fbf.in32
    
    newTr = pymel.core.createNode( 'transform' )
    newTr.attr( 'dh').set( 1 )
    newTr.attr( 'dla').set( 1 )
    dcmp = pymel.core.createNode( 'decomposeMatrix' )
    fbf.output >> dcmp.imat
    
    dcmp.outputTranslate >> newTr.t
    dcmp.outputRotate  >> newTr.r
    dcmp.outputScale  >> newTr.s
    dcmp.outputShear >> newTr.sh
    
    pymel.core.select( newTr )
    pymel.core.group( newTr, cubeObj, xFollicle, yFollicle, zFollicle, pFollicle )
    
    cmds.xform( cubeObj.name(), ws=1, matrix= cmds.getAttr( target + '.wm' ) )
    
    return newTr.name(), cubeObj.name()
    
    
    
    


