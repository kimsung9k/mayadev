import maya.cmds as cmds
import maya.OpenMaya as om


def getMObject( target ):
    selList = om.MSelectionList()
    selList.add( target )
    mObj = om.MObject()
    selList.getDependNode( 0, mObj )
    return mObj


def getDependNode( target ):
    return om.MFnDependencyNode( getMObject( target ) )


def getPlugFromString( attr ):
    
    def plugAttr( plug, attrName ):
        
        try:
            origAttrName, indexSep = attrName[0].split( '[' )
            indexSep = indexSep.replace( '[', '' )
        except:
            origAttrName = attrName[0]
            indexSep = None
        
        i=0
        while ( i < plug.numChildren() ):
            childPlug = plug.child( i )

            if childPlug.name().split( '.' )[-1] == origAttrName:
                
                if not indexSep:
                    nextPlug = childPlug
                else:
                    index = int( indexSep[0] )
                    nextPlug = childPlug[ index ]
                    
                if not len( attrName ) > 1:
                    return nextPlug
                else:
                    return plugAttr( nextPlug, attrName[1:] )
            i+=1
    
    def findAttrPlug( fnNode, attrName ):

        try:
            origAttrName, indexSep = attrName[0].split( '[' )
        except:
            return fnNode.findPlug( attrName[0] )
        
        plug = fnNode.findPlug( origAttrName )
        
        index = int( indexSep.replace( ']', '' ) )
        nextPlug = plug.elementByLogicalIndex( index )
        
        if not len( attrName ) > 1:
            return nextPlug
        else:
            return plugAttr( nextPlug, attrName[1:] )
            
    splitData = attr.split( '.' )
    
    node = splitData[0]
    attrName = splitData[1:]
    
    mObj = om.MObject()
    
    selList = om.MSelectionList()
    selList.add( node )
    selList.getDependNode( 0, mObj )
    
    fnNode = om.MFnDependencyNode( mObj )
    
    return findAttrPlug( fnNode, attrName )


def clearArrayElement( targetAttr ):
    
    targetAttrPlug = getPlugFromString( targetAttr )
    
    numElements = targetAttrPlug.numElements()
    
    delIndies = []
    for i in range( numElements ):
        logicalIndex = targetAttrPlug[i].logicalIndex()
        
        if not cmds.listConnections( targetAttr+'[%d]' % logicalIndex ):
            delIndies.append( logicalIndex )
            
    for delIndex in delIndies:
        cmds.removeMultiInstance( '%s[%d]' %( targetAttr, delIndex ) )



def getLastIndex( fullAttrName ):
    
    targetAttrPlug = getPlugFromString( fullAttrName )
    return targetAttrPlug.numElements()-1



def getOriginalName( target ):
    
    fnNode = om.MFnDependencyNode( getMObject( target ) )
    return fnNode.name()



def getSourcePlug( plug ):
    
    connection = om.MPlugArray()
    plug.connectedTo( connection, True, False )
    if not connection.length(): return None
    return connection[0]



def getMatrixFromPlug( plugMatrix ):
    
    mtxData = om.MFnMatrixData( plugMatrix.asMObject() )
    return mtxData.matrix()


def getRoofLinearCurve( startInput, endInput, minValue, maxValue ):
    
    animCurve = cmds.createNode( 'animCurveUU' )
    cmds.setKeyframe( f= startInput, v=minValue )
    cmds.setKeyframe( f= endInput,   v=maxValue )
    cmds.keyTangent( itt='linear', ott='linear' )
    cmds.selectKey( animCurve )
    cmds.setInfinity( poi='cycle', pri='cycle' )
    
    return animCurve


def getRoofSineCurve( startInput, endInput, minValue, maxValue ):
    
    animCurve = cmds.createNode( 'animCurveUU' )
    cmds.setKeyframe( f= startInput, v=minValue )
    cmds.setKeyframe( f= (startInput+endInput)/2.0, v=maxValue )
    cmds.setKeyframe( f= endInput,   v=minValue )
    cmds.selectKey( animCurve )
    cmds.setInfinity( poi='cycle', pri='cycle' )
    
    return animCurve



class AnimCurveData:
    
    def __init__( self, animCurveName ):
        
        self.className = 'AnimCurveData'
        
        self.name = animCurveName
        
        self.nodeType = cmds.nodeType( animCurveName )
        self.tc = cmds.keyframe( animCurveName, q=1, tc=1 )
        self.vc = cmds.keyframe( animCurveName, q=1, vc=1 )
        self.itt = cmds.keyTangent( animCurveName, q=1, itt=1 )
        self.ott = cmds.keyTangent( animCurveName, q=1, ott=1 )
        self.lock = cmds.keyTangent( animCurveName, q=1, lock=1 )
        self.ia = cmds.keyTangent( animCurveName, q=1, inAngle=1 )
        self.oa = cmds.keyTangent( animCurveName, q=1, outAngle=1 )
        self.preInfinity = cmds.getAttr( animCurveName+'.preInfinity' )
        self.postInfinity = cmds.getAttr( animCurveName+'.postInfinity' )
    
    def createAnimCurve( self ):
        
        newAnim = cmds.createNode( self.nodeType, n=self.name )

        if not self.tc: return None
        for i in range( len( self.tc ) ):
            cmds.setKeyframe( newAnim, t=self.tc[i], v=self.vc[i] )
            cmds.keyTangent( newAnim, t=(self.tc[i],self.tc[i]), lock=self.lock[i], 
                             itt=self.itt[i], ott=self.ott[i], ia=self.ia[i], oa=self.oa[i] )
            cmds.setAttr( newAnim+'.preInfinity', self.preInfinity )
            cmds.setAttr( newAnim+'.postInfinity', self.postInfinity )
        
        return newAnim



class AnimCurveForBake:
    
    def __init__( self, fullAttrName ):
        
        self.className = 'AnimCurveForBake'
        
        nodeName, attr = fullAttrName.split( '.' )
        attrType = cmds.attributeQuery( attr, node=nodeName, attributeType=1 )
        
        self.nodeType = ''
        if attrType == 'doubleLinear':
            self.nodeType = 'animCurveTL'
        elif attrType == 'doubleAngle':
            self.nodeType = 'animCurveTA'
        else:
            self.nodeType = 'animCurveTU'

        self.attrName     = fullAttrName
        self.times  = []
        self.values = []

        self.connectionExists = True
        if not cmds.listConnections( fullAttrName, s=1, d=0 ):
            node, attr = fullAttrName.split( '.' )
            parentAttrs = cmds.attributeQuery( attr, node=node, listParent=1 )
            if parentAttrs:
                if cmds.listConnections( node+'.'+parentAttrs[0] ):pass
                else:
                    self.connectionExists = False
                    self.times.append( 1 )
                    self.values.append( cmds.getAttr( fullAttrName ) )
            else:
                self.connectionExists = False
                self.times.append( 1 )
                self.values.append( cmds.getAttr( fullAttrName ) )


    def appendKeyframeData(self):
        
        time  = cmds.currentTime( q=1 )
        value = cmds.getAttr( self.attrName )
        
        self.times.append( time )
        self.values.append( value )


    def createAnimCurve(self ):
        
        animCurveName = self.attrName.split( '|' )[-1].replace( '.', '_' )+'_BAKE'
        if cmds.ls( animCurveName ): cmds.delete( cmds.ls( animCurveName ) )
        animCurveName = cmds.createNode( self.nodeType, n=animCurveName )
        
        for i in range( len( self.times ) ):
            cmds.setKeyframe( animCurveName, t=self.times[i], v=self.values[i] )
        
        return animCurveName