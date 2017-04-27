from maya import OpenMaya
from maya import cmds
from maya import mel
import math
import sgModules.sgdata as data
from sgModules.sgbase import *


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
        if nodeType in data.NodeType.shape:
            sgNode = SGDagNode( nodeName )
        elif nodeType in data.NodeType.transform:
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
        if self.nodeType() in data.NodeType.dag:
            attrNames += data.Attrs.dagAttrs
        if not attrNames:
            shortNames = cmds.listAttr( self.name() )
            shortNames += cmds.listAttr( self.name(), sn=1 )
            for shortName in shortNames:
                if str(shortName) in ['def','tg.try','try','global','ats.as','as','or', 'is', 'in', 'if']: continue
                attrNames.append( shortName )

        for attrName in attrNames:
            exec( "self.%s = self.attr( '%s' )" % (attrName,attrName) )


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
        if self.apiTypeStr() in data.ApiType.transform:
            return SGTransformNode( self )
        return SGTransformNode( self.parent() )


    def shape(self):
        if self.apiTypeStr() in data.ApiType.shape:
            return self
        children = cmds.listRelatives( self.name(), c=1, s=1, f=1 )
        if not children: return None
        for child in children:
            if cmds.getAttr( child + '.io' ): continue
            return SGDagNode( child )
        
        for child in children:
            return SGDagNode( child )


    def shapes(self):
        if self.apiTypeStr() in data.ApiType.shape:
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
                if cmds.nodeType( hist ) in data.NodeType.dag:
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
            if cmds.nodeType( result ) in data.NodeType.shape:
                sgresults.append( SGDagNode( result ) )
            elif cmds.nodeType( result ) in data.NodeType.transform:
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
    
    if str( nodeName.__class__ ).find( 'pymel.core' ) != -1:
        return convertSg( nodeName.name() )
    
    if not type( nodeName ) in [str, unicode]: 
        return nodeName
    
    if nodeName.find( '.' ) != -1:
        return SGAttribute( nodeName )
    nodeType = cmds.nodeType( nodeName )
    if nodeType in data.NodeType.shape:
        sgNode = SGDagNode( nodeName )
    elif nodeType in data.NodeType.transform:
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



def createNode( *args, **options ):
    
    nodeName = cmds.createNode( *args, **options )
    return convertSg( nodeName )



def shadingNode( *args, **options ):
    
    nodeName = cmds.shadingNode( *args, **options )
    return convertSg( nodeName )

    
