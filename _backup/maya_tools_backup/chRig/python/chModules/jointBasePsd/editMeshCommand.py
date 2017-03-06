import maya.cmds as cmds
import maya.OpenMaya as om
import math
import functions as fnc


def listSortCmp( value1, value2 ):
    
    if( value1[0] > value2[0] ): return -1
    elif( value1[0] == value2[0] ): return 0
    else: return 1



def selectDeltaPoints( nodeName, index, *args ):
    
    fnNode = om.MFnDependencyNode( fnc.getMObject(nodeName) )
    
    plugBlendMeshInfos = fnNode.findPlug( "blendMeshInfos" )

    if index >= plugBlendMeshInfos.numElements():
        return None
    
    plugBlendMeshInfos[ index ]



def getSameChannelExistShape( nodeName, minValue ):
    
    selList = om.MSelectionList()
    selList.add( nodeName )
    
    mObj = om.MObject()
    selList.getDependNode( 0, mObj )
    
    fnNode = om.MFnDependencyNode( mObj )
    
    driverWeightPlug = fnNode.findPlug( 'driverWeights' )
    
    valueList = []
    
    for i in range( driverWeightPlug.numElements() ):
        driverWElement = driverWeightPlug[i]
        
        connections = om.MPlugArray()
        driverWElement.connectedTo( connections, True, False )

        if connections.length() == 0:
            continue
        
        weightValue = driverWElement.asFloat()
        
        if math.fabs( weightValue ) < minValue:
            continue
        
        logicalIndex = driverWElement.logicalIndex()
        
        valueList.append( [ logicalIndex, weightValue ] )
    
    if not valueList: return None
    
    blendMeshInfoPlug = fnNode.findPlug( 'blendMeshInfos' )
    
    valueList.sort( listSortCmp )
    lenValueList = len( valueList )
    
    sameInfos = []
    
    for i in range( blendMeshInfoPlug.numElements() ):
        blendMeshInfoElement = blendMeshInfoPlug[i]
        
        targetWeightPlug = blendMeshInfoElement.child( 2 )
        
        existValueList = []
        for j in range( targetWeightPlug.numElements() ):
            targetWeightElement = targetWeightPlug[j]
            
            logicalIndex = targetWeightElement.logicalIndex()
            weightValue =  targetWeightElement.asFloat()
            
            existValueList.append( [logicalIndex,weightValue] )
            
        if len( existValueList ) != lenValueList : continue
        existValueList.sort( listSortCmp )
        
        diffExists = False
        for j in range( lenValueList ):
            if existValueList[j][0] != valueList[j][0]:
                diffExists = True
                break
            
        if not diffExists:
            blendMeshPlug = blendMeshInfoElement.child( 0 )
            
            connections = om.MPlugArray()
            blendMeshPlug.connectedTo( connections, True, False )
            
            if not connections.length(): return None
            
            fnBlendMesh = om.MFnDependencyNode( connections[0].node() )
            
            sameInfos.append( [ fnBlendMesh.name(), existValueList ] )
    
    return sameInfos


'''
class CheckingCmd:

    def __init__(self):
        
        self._outDriverDict = {}
    
    
    def getAngleDriverInfos( self, sameInfo ):
        
        shapeName, indexAndValueList = sameInfo
        
        blendAndFixedShape = cmds.listConnections( shapeName, type='blendAndFixedShape' )[0]
        
        for index, value in indexAndValueList:
            
            driverCons = cmds.listConnections( blendAndFixedShape+'.driverWeights[%d]' % index, s=1, d=0, c=1, p=1 )
            driverName, driverAttrName = driverCons[1].split( '.' )
            
            if not driverName in self._outDriverDict.keys():
                self._outDriverDict.update( {driverName: { driverAttrName : [value] } } )
            else:
                if not driverAttrName in self._outDriverDict[ driverName ].keys():
                    self._outDriverDict[ driverName ].update( { driverAttrName : [value] } )
                else:
                    self._outDriverDict[ driverName ][driverAttrName].append( value )



class CheckingUI:
    
    def __init__( self, driverDict ):
        
        self._winName = 'jointBasePsdCheck_ui'
        self._title   = 'Joint Base PSD Check UI'

        self._width = 400
        self._height = 100

        self._driverDict = driverDict

        self.core()
        
        
    def dictToSortedList(self, driverDict ):
        
        items = driverDict.items()
        
        items.sort( listSortCmp )
        
        return items
    
    
    
    def driverValuedInfoPopup(self, driverAttrName, scrollList ):
        
        selValues = cmds.textScrollList( driverAttrName, q=1, sii=1 )
        if not selValues:
            itemNums = cmds.textScrollList( driverAttrName, q=1, ni=1 )
            selValues = [ i+1 for i in range( itemNums ) ]
        
        def selectTargetMeshCommand():
            driver = driverAttrName.split( '.' )[0]
            cons = cmds.listConnections( driver, d=1, s=0, p=1, c=1, type='blendAndFixedShape' )
            if not cons: return None
            blendAndFixedShape, driverWeightAttr = cons[1].split( '.' )
        
        cmds.popupMenu()
        cmds.menuItem( 'Select Target Mesh' )


    def addDriverValuedInfo(self):
        
        driverItems = self.dictToSortedList( self._driverDict )
        
        uifnc.setSpace( 10 )
        cmds.separator( w=self._width )
        uifnc.setSpace( 10 )
        
        driverlist = uifnc.setWidthByPerList( [5,40,60,5], self._width-2 )
        cmds.rowColumnLayout( nc=4, cw=[(1,driverlist[0]),(2,driverlist[1]),(3,driverlist[2]),(4,driverlist[3])])
        uifnc.setSpace()
        
        for driverName, attrDict in driverItems:
            
            cmds.text( l = driverName+' : ', al='right' )
            attrItems = self.dictToSortedList( attrDict )
            
            driverList2 = uifnc.setWidthByPerList( [50,30], driverlist[2]-2 )
            cmds.rowColumnLayout( nc=2, cw=[(1,driverList2[0]), (2,driverList2[1]-2)] )
            
            for attrName, values in attrItems:

                cmds.text( l = attrName+' :    ', al='right' )
                cmds.textScrollList( a=values, h= len( values )*15 )
                uifnc.setSpace(5);uifnc.setSpace()
            
            cmds.setParent( '..' )
        
        cmds.setParent( '..' )
        
        uifnc.setSpace( 10 )
        cmds.separator( w=self._width )
        uifnc.setSpace( 10 )
                

    def core(self):

        if cmds.window( self._winName, ex=1 ):
            cmds.deleteUI( self._winName, wnd=1 )

        cmds.window( self._winName, title = self._title, rtf=1 )

        cmds.columnLayout()

        uifnc.setSpace( 10 )

        widthList = uifnc.setWidthByPerList( [5,90,5], self._width-2 )
        cmds.rowColumnLayout( nc=3, cw=[(1,widthList[0]),(2,widthList[1]),(3,widthList[2])] )
        uifnc.setSpace()
        cmds.text( "These Angle Driver's attributes\nhas values." )
        uifnc.setSpace()
        cmds.setParent( '..' )

        self.addDriverValuedInfo()

        widthList = uifnc.setWidthByPerList( [5,45,45,5], self._width-2 )
        cmds.rowColumnLayout( nc=4, cw=[(1,widthList[0]),(2,widthList[1]),(3,widthList[2]),(4,widthList[3])] )
        uifnc.setSpace()
        cmds.button( l='Edit Mesh', h=30 )
        cmds.button( l='Cencel', h=30 )
        uifnc.setSpace()
        cmds.setParent( '..' )

        uifnc.setSpace( 10 )

        cmds.setParent( '..' )

        cmds.window( self._winName, e=1, width = self._width, height = self._height )
        cmds.showWindow( self._winName )
        '''



class Main:
    
    def __init__(self, minValue, *meshs ):
        
        self._nodes = []
        self._minValue = minValue
        
        self._meshList = []
        
        for mesh in meshs:
            
            meshHists = cmds.listHistory( mesh )
            
            for hist in meshHists:
                
                if cmds.nodeType( hist ) == 'blendAndFixedShape':
                    self._meshList.append( mesh )
                    break

    
    def changeEditMeshMode(self):
        
        blinns = cmds.ls( type='blinn' )
        
        editMeshShader=None
        for blinn in blinns:
            if cmds.attributeQuery( 'isEditMeshShader', node=blinn, ex=1 ):
                editMeshShader = blinn
                
        if not editMeshShader:
            blinn = cmds.shadingNode( 'blinn', asShader=1 )
            editMeshShader = cmds.rename( blinn, 'EditMeshShader' )
            SG = cmds.sets( renderable=True, noSurfaceShader=True, empty=1, n='EditMeshSG' )
            cmds.connectAttr( editMeshShader+'.outColor', SG+'.surfaceShader' )
            cmds.setAttr( editMeshShader+'.color', .2,1,.6, type='double3' )
            cmds.setAttr( editMeshShader+'.specularColor', .2,.2,.2, type='double3' )
            
        for meshObj in self._meshList:
            
            meshShape = cmds.listRelatives( meshObj, s=1 )[0]
            
            editShape = cmds.createNode( 'mesh' )
            cmds.connectAttr( meshShape+'.outMesh', editShape+'.inMesh' )
            cmds.refresh()
            cmds.disconnectAttr( meshShape+'.outMesh', editShape+'.inMesh' )
            
            editMeshObj = cmds.listRelatives( editShape, p=1 )[0]
            
            if not cmds.attributeQuery( 'editMeshTarget', node=meshObj, ex=1 ):
                cmds.addAttr( meshObj, ln='editMeshTarget', at='message' )
                
            cons = cmds.listConnections( meshObj+'.editMeshTarget')
            
            if cons: cmds.delete( cons )
            
            cmds.connectAttr( editMeshObj+'.message', meshObj+'.editMeshTarget' )
            
            cmds.sets( editMeshObj, e=1, forceElement=SG ) 
            cmds.setAttr( meshObj+'.v', 0 )