#-*- coding: utf-8 -*-

import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import PySide.QtGui
import pymel.core
import os
from sgUIs.putObjectOnGround import Window_cmd


class Window_global:
    
    name = "sgShaderCleanup"
    title = "UI - Shader Cleanup"
    wh = [430,300]
    
    targetFolder = 'D:/PINGO_SERVER/pingo_server1/@@DEV@@/maya_tools_data/shaderCleanup'
    matAttrFile = ''
    if os.path.exists( targetFolder ):
        for root, dirs, names in os.walk( targetFolder ):
            if names:
                matAttrFile = root + '/' + names[0]
            break
    #if not matAttrFile:
    matAttrFile = os.path.dirname( __file__ ) + '/data/shaderAttributeList.txt'
    
    #print "mat attr path : ", matAttrFile
    matAttrs = {}
    
    @staticmethod
    def loadPlugins():
        
        pluginList = ['redshift4maya.mll', 'Mayatomr.mll']
        for plugin in pluginList:
            if cmds.pluginInfo( plugin, q=1, l=1 ): continue
            cmds.loadPlugin( plugin )
        
    
    @staticmethod
    def updateMatAttrs():
        
        if os.path.exists( Window_global.matAttrFile ):
            f = open( Window_global.matAttrFile, 'r' )
            data = f.read()
            f.close()
            
            lines = data.split( '\n' )
            
            shaders = map( lambda x : x.strip(), lines[0].split( '\t' ) )
            shaderAttrs = [ [] for i in range( len( shaders ) ) ]
            
            for line in lines[1:]:
                attrs = map( lambda x : x.strip(), line.split( '\t' ) )
                for i in range( len( attrs ) ):
                    shaderAttrs[i].append( attrs[i] )
            
            for i in range( len( shaders ) ):
                Window_global.matAttrs.update( {shaders[i]: shaderAttrs[i]} )


    op_shaderType = ''
    tsl_shaderList = ''
    bt_combine = ''
    watch = ''
    
    selectIndex = 0
    
    selectByUi = False
    
    nodeInfomation = {}
    
    
    
    

class Window_cmds:

    @staticmethod
    def getMaterialTypes():
        sels = cmds.ls( mat=1 )
        matTypes = []
        for sel in sels:
            matTypes.append( cmds.nodeType( sel ) )
        
        matTypes = list( set( matTypes ) )    
        matTypes.sort()
        
        return matTypes
    
    
    @staticmethod
    def getMaterials():
        
        itemList = cmds.optionMenuGrp( Window_global.op_shaderType, q=1, ils=1 )
        selIndex = cmds.optionMenuGrp( Window_global.op_shaderType, q=1, select=1)
        matType = cmds.menuItem( itemList[selIndex-1], q=1, l=1 )
        
        sels = cmds.ls( mat=1 )
        sels = list( set (sels ) )
        sels.sort()
        
        newSels = []
        for sel in sels:
            if not cmds.listConnections( sel, s=0, d=1, type='shadingEngine' ): continue
            newSels.append( sel )
        
        if matType == 'All':
            return newSels
        else:
            targetSels = []
            for sel in newSels:
                if cmds.nodeType( sel ) == matType:
                    targetSels.append( sel )
            return targetSels
    
    
    @staticmethod
    def getTextures():
        sels = cmds.ls( tex=1 )
        sels.sort()
        return sels
    
    
    @staticmethod
    def getAllNodeInfomation():
        
        nodes = cmds.ls( dep=1 )
        Window_global.nodeInfomation = {}
        
        for node in nodes:
            if cmds.attributeQuery( 'worldMatrix', node=node, ex=1 ): continue
            Window_global.nodeInfomation.update( {node:Window_cmds.getNodeInfomation(node)} )
        
    
    
    @staticmethod
    def getNodeInfomation( node ):
        
        if Window_global.nodeInfomation.has_key( node ):
            return Window_global.nodeInfomation[node]
        
        baseMatType  = cmds.nodeType( node )
        attrs = cmds.listAttr( node )
        baseAttrValues = [None for m in range( len( attrs ) ) ]
        for m in range( len( attrs ) ):
            try:
                baseAttrValue = cmds.getAttr( node + '.' + attrs[m] )
                baseAttrValues[m] = baseAttrValue
            except:
                pass
        
        Window_global.nodeInfomation.update( { node : (baseMatType, baseAttrValues) } )
        return baseMatType, baseAttrValues
    
    
    @staticmethod
    def isSame( first, second ):
        
        firstType, firstAttrValues = Window_cmds.getNodeInfomation( first )
        secondType, secondAttrValues = Window_cmds.getNodeInfomation( second )
        if firstType != secondType: return  False
        
        for i in range( len( firstAttrValues ) ):
            if firstAttrValues[i] != secondAttrValues[i]: return False
        return True
        
    
    
    
    @staticmethod
    def getSameMaterialGroups():
        
        sameGroups = []
        
        nodeList = Window_cmds.getMaterials()
        
        for i in range( len( nodeList ) ):
            
            isAppend = False
            for sameGroup in sameGroups:
                if i in sameGroup: isAppend = True
            if isAppend: continue
            
            firstHistory = pymel.core.ls( nodeList[i] )[0].history()
            if not firstHistory: firstHistory = []
            
            for j in range( i+1, len( nodeList ) ):
                
                if not Window_cmds.isSame( nodeList[i], nodeList[j] ): continue
                
                secondHistory = pymel.core.ls( nodeList[j] )[0].history()
                if not secondHistory: secondHistory = []
                if len( firstHistory ) != len( secondHistory ): continue
                
                isSame = True
                for k in range( len( firstHistory ) ):
                    if not Window_cmds.isSame( firstHistory[k].name(), secondHistory[k].name() ):
                        isSame = False
                        break
                if not isSame: continue
                
                isAppend = False
                for sameGroup in sameGroups:
                    if i in sameGroup:
                        sameGroup.append( j )
                        isAppend = True
                        break
                if not isAppend:
                    sameGroups.append( [i, j] )
        
        lenGroups = len( sameGroups )
        if not lenGroups: return None
        
        targetGroupIndices = sameGroups[ Window_global.selectIndex % lenGroups ]
        Window_global.selectIndex += 1
        return targetGroupIndices
    
    
    
    @staticmethod
    def isSameMaterials( selList ):
        
        for i in range( len( selList ) -1 ):
            if not Window_cmds.isSame( selList[i], selList[i+1] ):
                return False
        return True

    
    @staticmethod
    def combineShader( shaderList ):
        
        cmds.undoInfo( ock=1 )
        
        targetObjs = []
        for shader in shaderList:
            cmds.hyperShade( objects = shader )
            targetObjs += cmds.ls( sl=1 )
        shadingEngines = cmds.listConnections( shaderList, s=0, d=1, type='shadingEngine' )
        if not shadingEngines: return None
        shadingEngines = list( set( shadingEngines ) )
        targetShadingEngine = shadingEngines[0]
        
        cmds.sets( targetObjs, e=1, forceElement = targetShadingEngine )
        
        cmds.delete( shadingEngines[1:] )
        for shader in shaderList:
            shadingEngines = cmds.listConnections( shader, s=0, d=1, type='shadingEngine' )
            if not shadingEngines:
                cmds.delete( shader )
            elif not targetShadingEngine in shadingEngines:
                cmds.delete( shader, shadingEngines )
        
        Window_global.nodeInfomation = {}
        
        cmds.undoInfo( cck=1 )
        
    
    
    @staticmethod
    def selectObjectByMaterials( shaderList ):
        
        targetObjs = []
        for shader in shaderList:
            cmds.hyperShade( objects = shader )
            targetObjs += cmds.ls( sl=1 )
        cmds.select( targetObjs )
    
    

    @staticmethod
    def selectionChanged( evt=0 ):
        
        sels = cmds.ls( sl=1 )
        if not sels: return None
        shapes = []
        for sel in sels:
            selShapes = cmds.listRelatives( sel, s=1, f=1 )
            if selShapes:
                shapes += selShapes
        
        shadingEngines = cmds.listConnections( shapes, type='shadingEngine' )
        if not shadingEngines: return None
        materials = []
        matList = cmds.ls( mat=1 )
        for shadingEngine in shadingEngines:
            shaders = list( set( cmds.listConnections( shadingEngine, s=1, d=0 ) ) )
            for shader in shaders:
                if shader in matList:
                    materials.append( shader )
        
        if shaders:cmds.textScrollList( Window_global.tsl_shaderList, e=1, da=1, selectItem = shaders )


    @staticmethod
    def getAttrObjectFromXml( data ):
        import xml.etree.ElementTree as ET
        
        etdata = ET.fromstring( data )
        
        droot = {'src':[]}
        
        for child in etdata.getchildren():
            if child.tag == 'attr':
                droot.update( {child.tag:child.text} )
            elif child.tag == 'src':
                dsrc = {'set':[]}
                for srcChild in child.getchildren():
                    if srcChild.tag in ['node','input','output']:
                        dsrc.update( {srcChild.tag:srcChild.text} )
                    if srcChild.tag == 'set':
                        dset = {}
                        for setChild in srcChild.getchildren():
                            dset.update( {setChild.tag: setChild.text} )
                        dsrc['set'].append( dset )
                droot['src'].append( dsrc )
        return droot

    
    @staticmethod
    def getAttrFromAttrObject( xmlObject ):
        
        print "xml object : ", xmlObject
        
        attr = xmlObject['attr']
        srcs = xmlObject['src']
        
        beforeInputAttr = ''
        beforeOutputAttr = ''
        beforeNode = ''
        
        resultInput = ''
        resultOutput = ''
        
        def stringValueToValue( strValue ):
            if strValue.find( ',' ) != -1:
                splitValues = strValue.split( ',' )
                numValues = []
                for splitValue in splitValues:
                    numValues.append( float( splitValue ) )
                return numValues
            else:
                return float( strValue )
            
        
        for src in srcs:
            nodeType = src['node']
            inputAttr = src['input']
            outputAttr = src['output']
            lsets = src['set']
            
            shadingNode = cmds.shadingNode( nodeType, asUtility=1 )
            
            for lset in lsets:
                attrName = lset['attrName']
                value    = lset['value']
                try:cmds.setAttr( shadingNode + '.' + attrName,  stringValueToValue( value ) )
                except:cmds.setAttr( shadingNode + '.' + attrName,  *stringValueToValue( value ) )
            
            if beforeNode:
                cmds.connectAttr( beforeNode + '.' + beforeOutputAttr, shadingNode + '.' + inputAttr )
            else:
                resultInput = shadingNode + '.' + inputAttr
            beforeNode = shadingNode
            beforeInputAttr = inputAttr
            beforeOutputAttr = outputAttr
            resultOutput = shadingNode + '.' +  outputAttr
        
        return resultInput, resultOutput
    
    
    
    @staticmethod
    def tryConnect( srcAttr, dstAttr ):
        if not cmds.isConnected( srcAttr, dstAttr ):
            try:
                cmds.connectAttr( srcAttr, dstAttr, f=1 )
            except:
                pymelAttr = pymel.core.ls( srcAttr )[0]
                if not cmds.isConnected( pymelAttr.name(), dstAttr ):
                    try:cmds.connectAttr( pymelAttr.name(), dstAttr, f=1 )
                    except:pass
    
    
    @staticmethod
    def trySet( srcAttr, targetAttr ):
        try:cmds.setAttr( targetAttr, cmds.getAttr( srcAttr ) )
        except:
            try:cmds.setAttr( targetAttr, *cmds.getAttr( srcAttr ) )
            except:
                try:
                    attrValue = cmds.getAttr( srcAttr )
                    cmds.setAttr( targetAttr, attrValue, attrValue, attrValue )
                except:
                    pass
    
    
    @staticmethod
    def convertBump( shader ):
        
        shader = pymel.core.ls( shader )[0]
        if shader.type().find( 'Redshift' ) != -1:
            hists = shader.history()
            for hist in hists:
                if hist.type() != 'bump2d': continue
                if hist.bumpInterp.get() == 0:
                    redshiftBump = pymel.core.shadingNode( 'RedshiftBumpMap', asUtility=1 )
                    redshiftBump.out >> shader.bump_input
                    srcNode = hist.bumpValue.listConnections( s=1, d=0 )
                    if srcNode:
                        srcNode[0].outColor >> redshiftBump.input
                elif hist.bumpInterp.get() == 1:
                    redshiftBump = pymel.core.shadingNode( 'RedshiftNormalMap', asUtility=1 )
                    redshiftBump.outDisplacementVector >> shader.bump_input
                    srcNode = hist.bumpValue.listConnections( s=1, d=0, type='file' )
                    if srcNode:
                        redshiftBump.tex0.set( srcNode[0].fileTextureName.get() )
    

    @staticmethod
    def convertTo( matType ):
        
        cmds.undoInfo( ock=1 )
        def getReverseValue( value, rev ):
            if rev:
                if type( value ) in [tuple,list]:
                    return [ 1-value[0], 1-value[1], 1-value[2] ]
                else:
                    return 1-value
            else:
                return value
        
        
        def shaderConnect( shader, shadingEngine ):
            try:
                cmds.connectAttr( shader + '.outColor', shadingEngine + '.surfaceShader' )
            except:
                if cmds.nodeType( shader ).find( 'mia_material_x' ) != -1:
                    cmds.connectAttr( shader + '.message', shadingEngine + '.miMaterialShader' )
                    cmds.connectAttr( shader + '.message', shadingEngine + '.miPhotonShader' )
                    cmds.connectAttr( shader + '.message', shadingEngine + '.miShadowShader' )
        
        shaders = cmds.textScrollList( Window_global.tsl_shaderList, q=1, si=1 )
        
        targetMatAttrs = Window_global.matAttrs[ matType ]
        
        newShaders = []
        for shader in shaders:
            shaderType = cmds.nodeType( shader )
            if shaderType == matType: continue
            if not Window_global.matAttrs.has_key( shaderType ):
                cmds.warning( "'%s' type is not convert alble" % shaderType ) 
                continue
            sourceMatAttrs = Window_global.matAttrs[ shaderType ]
            
            lenAttrs = min( len( targetMatAttrs ), len( sourceMatAttrs ) )
            
            newShader = cmds.shadingNode( matType, asShader=1 )
            
            for i in range( lenAttrs ):
                sourceAttr = sourceMatAttrs[i]
                targetAttr = targetMatAttrs[i]
                
                if not sourceAttr or not targetAttr: continue
                if sourceAttr.find( '<?xml' ) != -1:
                    sourceAttr = Window_cmds.getAttrObjectFromXml(sourceAttr)['attr']
                
                if not cmds.attributeQuery( sourceAttr, node=shader, ex=1 ):continue
                
                fullSourceAttrName = shader    + '.' + sourceAttr
                fullTargetAttrName = newShader + '.' + targetAttr
                
                sourceAttrCons = cmds.listConnections( fullSourceAttrName, s=1, p=1 )
                
                if sourceAttrCons:
                    if targetAttr.find( '<?xml' ) != -1:
                        attrObject = Window_cmds.getAttrObjectFromXml(targetAttr)
                        resultInput, resultOutput = Window_cmds.getAttrFromAttrObject( attrObject )
                        if not resultOutput:
                            fullTargetAttrName = newShader + '.' + attrObject['attr']
                        else:
                            cmds.connectAttr( resultOutput, newShader + '.' + attrObject['attr'] )
                            fullTargetAttrName = resultInput
                    Window_cmds.tryConnect( sourceAttrCons[0], fullTargetAttrName )
                else:
                    if targetAttr.find( '<?xml' ) != -1:
                        attrObject = Window_cmds.getAttrObjectFromXml(targetAttr)
                        fullTargetAttrName = newShader + '.' + attrObject['attr']
                    Window_cmds.trySet( fullSourceAttrName, fullTargetAttrName )
                    
                targetAttrHists = pymel.core.ls( fullTargetAttrName )[0].history()
                for hist in targetAttrHists:
                    if hist.type() == 'file':
                        hist.colorSpace.set( 'Raw' )
            
            cmds.hyperShade( objects=shader )
            selObjs = cmds.ls( sl=1 )
            
            shadingEngine = cmds.sets( renderable=1, noSurfaceShader=1, empty=1, name=shader + 'SG' )
            shaderConnect( newShader, shadingEngine )
            cmds.sets( selObjs, e=1, fe= shadingEngine )
            
            newShader = cmds.rename( newShader, shader+'_convert' )
            newShaders.append( newShader )
            
            Window_cmds.convertBump( newShader )
            
            

        materials = Window_cmds.getMaterials()
        firstMat = None
        cmds.textScrollList( Window_global.tsl_shaderList, e=1, ra=1 )
        for material in materials:
            if not firstMat: firstMat = material
            cmds.textScrollList( Window_global.tsl_shaderList, e=1, a=material )

        cmds.select( newShaders )
        cmds.undoInfo( cck=1 )
        
        Window_global.nodeInfomation = {}
    
    
    
    @staticmethod
    def selectShader( evt=0 ):
        
        selectedItems = cmds.textScrollList( Window_global.tsl_shaderList, q=1, si=1 )
        cmds.select( selectedItems )
    
    
    @staticmethod
    def updateList( evt=0 ):
        
        materials = Window_cmds.getMaterials()
        cmds.textScrollList( Window_global.tsl_shaderList, e=1, ra=1 )
        for material in materials:
            cmds.textScrollList( Window_global.tsl_shaderList, e=1, a=material )






class UI_shaderTypeLister:
    
    def __init__(self):
        pass
    
    
    def create(self):
        
        form  = cmds.formLayout()
        shaderType = cmds.optionMenuGrp( l='Shader Type : ', cw=(1,100), h=30, changeCommand = self.changeCommand )
        cmds.setParent( '..' )

        matTypes = Window_cmds.getMaterialTypes()
        
        cmds.menuItem( l='All' )
        for matType in matTypes:
            cmds.menuItem( l=matType )
        
        cmds.formLayout( form, e=1, 
                         af=[ (shaderType, 'top', 0), (shaderType, 'left', 0), (shaderType, 'right', 0) ] )
        Window_global.op_shaderType = shaderType
        
        self.om_shaderType = shaderType
        self.matTypes = matTypes
        
        Window_global.om_shaderType = shaderType
        
        return form
    
    
    def changeCommand(self, evt=0 ):
        
        materials = Window_cmds.getMaterials()
        cmds.textScrollList( Window_global.tsl_shaderList, e=1, ra=1 )
        
        selectIndex = cmds.optionMenuGrp( self.om_shaderType, q=1, select=1 ) - 2
        
        firstMat = None
        if selectIndex == -1:
            for material in materials:
                if not firstMat: firstMat = material
                cmds.textScrollList( Window_global.tsl_shaderList, e=1, a=material )
        else:
            targetMatType = self.matTypes[ selectIndex ]
            firstMat = None
            for material in materials:
                if cmds.nodeType( material ) == targetMatType:
                    if not firstMat: firstMat = material
                    cmds.textScrollList( Window_global.tsl_shaderList, e=1, a=material )
            
        cmds.swatchDisplayPort( Window_global.swatch, e=1, wh=(64,64), sn=firstMat )
        
        


class UI_shaderLister:
    
    def __init__(self):
        pass


    def create(self):
        
        form = cmds.formLayout()
        
        shaderList = cmds.textScrollList( ams=1, selectCommand = self.selectCommand )
        cmds.popupMenu()
        cmds.menuItem( l='Select Shader', c = Window_cmds.selectShader )
        materials = Window_cmds.getMaterials()
        firstMat = None
        for material in materials:
            if not firstMat: firstMat = material
            cmds.textScrollList( shaderList, e=1, a=material )
        swatch = cmds.swatchDisplayPort( wh=(64,64), bgc = [0.5, 0.5, 0.5], sn=firstMat )
        
        cmds.setParent( '..' )

        cmds.formLayout( form, e=1,
                         af=[ ( swatch, 'top', 5 ), ( swatch, 'left', 5 ),
                              ( shaderList, 'top', 5 ), ( shaderList, 'right', 5 ), ( shaderList, 'bottom', 5 ) ],
                         ac=[ ( shaderList, 'left', 3, swatch )])
        
        Window_global.swatch = swatch
        Window_global.tsl_shaderList = shaderList    
        return form
    

    def selectCommand(self, evt=0 ):
        selList = cmds.textScrollList( Window_global.tsl_shaderList, q=1, selectItem=1 )
        cmds.swatchDisplayPort( Window_global.swatch, e=1, wh=(64,64), sn=selList[0] )
        cmds.button( Window_global.bt_combine, e=1, en=0 )
        
        '''
        cmds.scriptJob( k=Window_global.scriptJob )
        Window_global.scriptJob = cmds.scriptJob( e=['SelectionChanged', Window_cmds.selectionChanged ], parent= Window_global.name )
        '''
        
        Window_cmds.selectObjectByMaterials( selList )
        
        if len( selList ) > 1 and Window_cmds.isSameMaterials( selList ):
            cmds.button( Window_global.bt_combine, e=1, en=1 )
 




class UI_combine:
    
    def __init__(self):
        pass
    
    
    def create(self):
        
        form = cmds.formLayout()
        buttonSelectSame = cmds.button( l='Select Same', c= self.selectCommand )
        buttonCombine    = cmds.button( l='Combine', c= self.combineCommand, en=0 )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af=[(buttonSelectSame, 'top', 0), (buttonSelectSame, 'left', 0), (buttonSelectSame, 'bottom', 0),
                             (buttonCombine, 'top', 0), (buttonCombine, 'right', 0), (buttonCombine, 'bottom', 0)],
                         ap=[(buttonSelectSame, 'right', 1, 50),
                             (buttonCombine, 'left', 1, 50)])
        
        Window_global.bt_combine = buttonCombine
        
        return form
    
    
    def selectCommand(self, evt=0 ):
        cmds.textScrollList( Window_global.tsl_shaderList, e=1, ra=1 )
        materials = Window_cmds.getMaterials()
        for material in materials:
            cmds.textScrollList( Window_global.tsl_shaderList, e=1, a=material )
        groupIndices = Window_cmds.getSameMaterialGroups()
        #print "mat group indices : ", groupIndices
        
        if not groupIndices: return None
        
        groupIndices = [ i+1 for i in groupIndices ]
        cmds.textScrollList( Window_global.tsl_shaderList, e=1, sii=groupIndices )
        cmds.button( Window_global.bt_combine, e=1, en=1 )
        
        selList = cmds.textScrollList( Window_global.tsl_shaderList, q=1, selectItem=1 )
        Window_cmds.selectObjectByMaterials( selList )
    
    
    def combineCommand(self, evt=0):
        
        shaderList = cmds.textScrollList( Window_global.tsl_shaderList, q=1, selectItem=1 )
        Window_cmds.combineShader( shaderList )
        existsShader = ''
        for shader in shaderList:
            if not cmds.objExists( shader ): continue
            existsShader = shader
            break
        if not existsShader: return None
        cmds.textScrollList( Window_global.tsl_shaderList, e=1, selectItem= existsShader )
        cmds.swatchDisplayPort( Window_global.swatch, e=1, wh=(64,64), sn=existsShader )
        
        materials = Window_cmds.getMaterials()
        targetShader = None
        
        cmds.textScrollList( Window_global.tsl_shaderList, e=1, ra=1 )
        for material in materials:
            if material == existsShader: targetShader = material
            cmds.textScrollList( Window_global.tsl_shaderList, e=1, a=material )
        cmds.textScrollList( Window_global.tsl_shaderList, e=1, si=targetShader )
        Window_cmds.selectObjectByMaterials( [targetShader] )
    




class UI_convert:
    
    def __init__(self):
        pass


    def create(self):
                
        form = cmds.formLayout()
        
        buttonConvert = cmds.button( l='Convert', c= self.convertCommand )
        text = cmds.text( l='as', w=50 )
        optionMenu = cmds.optionMenu()
        for shaderType in Window_global.matAttrs.keys():
            cmds.menuItem( l=shaderType )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af = [ (buttonConvert, 'top', 0), (buttonConvert, 'left', 0), (buttonConvert, 'bottom', 0),
                                (text, 'top', 0), (text, 'bottom', 0),
                                (optionMenu, 'top', 0),(optionMenu, 'right', 0),(optionMenu, 'bottom', 0) ],
                         ap = [ (text, 'left', 0, 50 ) ],
                         ac = [ (buttonConvert, 'right', 0, text ),
                                (optionMenu, 'left', 0, text )])
        
        self.om_convert = optionMenu
        
        return form


    def convertCommand(self, evt=0 ):
        
        selectedIndex = cmds.optionMenu( self.om_convert, q=1, select=1 )
        convertType = Window_global.matAttrs.keys()[ selectedIndex-1 ]
        Window_cmds.convertTo( convertType )





class Window:
    
    def __init__(self):
        
        self._ui_shaderTypeLister = UI_shaderTypeLister()
        self._ui_shaderLister     = UI_shaderLister()
        self._ui_combine          = UI_combine()
        self._ui_convert          = UI_convert()
    
    
    def show(self, evt=0 ):
        
        Window_global.selectIndex = 0
        Window_global.loadPlugins()
        Window_global.updateMatAttrs()
        
        if cmds.window( Window_global.name, ex=1 ):
            cmds.deleteUI( Window_global.name, wnd=1 )
        cmds.window( Window_global.name, title=Window_global.title )
        
        #Window_global.scriptJob = cmds.scriptJob( e=['SelectionChanged', Window_cmds.selectionChanged ], parent= Window_global.name )
        #cmds.scriptJob( e=['Undo', Window_cmds.updateList], parent= Window_global.name )
        #cmds.scriptJob( e=['Redo', Window_cmds.updateList], parent= Window_global.name )
        
        form = cmds.formLayout()
        shaderType    = self._ui_shaderTypeLister.create()
        shader        = self._ui_shaderLister.create()
        combineShader = self._ui_combine.create()
        convert       = self._ui_convert.create()
        
        cmds.setParent('..')
        
        cmds.formLayout( form, e=1, 
                         af=[ (shaderType, 'top', 0), (shaderType, 'left', 0), (shaderType, 'right', 0),
                              (shader, 'left', 3), (shader, 'right', 3),
                              (combineShader, 'left', 3), (combineShader, 'right', 3),
                              (convert, 'left', 3), (convert, 'right', 3), (convert, 'bottom', 3 ), ],
                         ac=[ (shader, 'top', 3, shaderType ),
                              (shader, 'bottom', 3, combineShader ),
                              (combineShader, 'bottom', 3, convert ) ] )
        
        cmds.window( Window_global.name, e=1, rtf=1 )
        cmds.showWindow( Window_global.name )
        
        #Window_cmds.getAllNodeInfomation()


def show():
    Window().show()


