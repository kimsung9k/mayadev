#-*- coding: utf-8 -*-

import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import PySide.QtGui
import pymel.core
import os


class Window_global:
    
    name = "sgShaderCleanup"
    title = "UI - Shader Cleanup"
    wh = [430,300]
    
    matAttrFile = os.path.dirname( __file__ ) + '/data/shaderAttributeList.tsv'
    
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


    matAttrs = {'lambert' :['color', 'transparency', 'ambientColor', 'incandescence', 
                             'diffuse', 'translucence', 'translucenceDepth', 'translucenceFocus', 
                             'glowIntensity', 'matteOpacityMode', 'matteOpacity',
                             'refractions','refractiveIndex','refractionLimit', 'lightAbsorbance', 'surfaceThickness',
                             'shadowAttenuation','chromaticAberration', 
                             'normalCamera',
                             '', '', '' ],
                'blinn'   :['color', 'transparency', 'ambientColor', 'incandescence', 
                             'diffuse', 'translucence', 'translucenceDepth', 'translucenceFocus', 
                             'glowIntensity', 'matteOpacityMode', 'matteOpacity',
                             'refractions','refractiveIndex','refractionLimit', 'lightAbsorbance', 'surfaceThickness',
                             'shadowAttenuation','chromaticAberration',
                             'normalCamera',
                             'specularColor', 'reflectivity', 'reflectedColor' ],
                'phong'   :['color', 'transparency', 'ambientColor', 'incandescence', 
                             'diffuse', 'translucence', 'translucenceDepth', 'translucenceFocus', 
                             'glowIntensity', 'matteOpacityMode', 'matteOpacity',
                             'refractions','refractiveIndex','refractionLimit', 'lightAbsorbance', 'surfaceThickness',
                             'shadowAttenuation','chromaticAberration',
                             'normalCamera',
                             'specularColor', 'reflectivity', 'reflectedColor' ],
                'phongE'   :['color', 'transparency', 'ambientColor', 'incandescence', 
                             'diffuse', 'translucence', 'translucenceDepth', 'translucenceFocus', 
                             'glowIntensity', 'matteOpacityMode', 'matteOpacity',
                             'refractions','refractiveIndex','refractionLimit', 'lightAbsorbance', 'surfaceThickness',
                             'shadowAttenuation','chromaticAberration',
                             'normalCamera',
                             'specularColor', 'reflectivity', 'reflectedColor' ],
                'surfaceShader'   :['outColor', 'outTransparency', '', '', 
                             '', '', '', '', 
                             '', '', '',
                             '','','', '', '',
                             '','',
                             'normalCamera',
                             '', '', '' ],
                'mia_material_x_passes' :['diffuse', 'transparency', '', '', 
                             'diffuse_weight', '', '', '', 
                             '', '', '',
                             '','','', '', '',
                             '','',
                             'standard_bump',
                             'refl_color', 'reflectivity', 'refl_gloss', 
                             'refr_ior'
                             'diffuse_roughness',
                             'refl_gloss_samples' ],
                'mia_material_x' :['diffuse', 'transparency', '', '', 
                             'diffuse_weight', '', '', '', 
                             '', '', '',
                             '','','', '', '',
                             '','',
                             'standard_bump',
                             'refl_color', 'reflectivity', 'refl_gloss', 
                             'refr_ior', 'refr_gloss'
                             'diffuse_roughness',
                             'refl_gloss_samples' ],
                'RedshiftArchitectural'   :['diffuse', 'transparency', '', 'additional_color', 
                             'diffuse_weight', '', '', '', 
                             '', '', '',
                             '','','', '', '',
                             '','',
                             'bump_input',
                             'refl_color', 'reflectivity', 'refl_gloss', 
                             'refr_ior', 'refr_gloss'
                             'diffuse_roughness',
                             'refl_gloss_samples' ] }
    
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
    def convertTo( matType ):
        
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
                sourceSplits = sourceMatAttrs[i].split( ',' )
                targetSplits = targetMatAttrs[i].split( ',' )
                
                sourceAttr = sourceSplits[0]
                targetAttr = targetSplits[0]
                
                reverseValue = False
                if len( sourceSplits ) > 1:
                    if sourceSplits[1] == 'reverse':
                        reverseValue = not reverseValue
                if len( targetSplits ) > 1:
                    if targetSplits[1] == 'reverse':
                        reverseValue = not reverseValue
                
                if not sourceAttr or not targetAttr: continue
                if not cmds.attributeQuery( sourceAttr, node=shader, ex=1 ):continue
                sourceAttrCons = cmds.listConnections( shader + '.' + sourceAttr, s=1, p=1 )
                if sourceAttrCons:
                    cmds.connectAttr( sourceAttrCons[0], newShader + '.' + targetAttr )
                else:
                    try:cmds.setAttr( newShader + '.' + targetAttr, getReverseValue( cmds.getAttr( shader + '.' + sourceAttr ), reverseValue ) )
                    except:
                        try:cmds.setAttr( newShader + '.' + targetAttr, *getReverseValue( cmds.getAttr( shader + '.' + sourceAttr )[0], reverseValue ) )
                        except:
                            try:cmds.setAttr( newShader + '.' + targetAttr, getReverseValue( cmds.getAttr( shader + '.' + sourceAttr )[0][0], reverseValue ) )
                            except:
                                try:
                                    value = getReverseValue( cmds.getAttr( shader + '.' + sourceAttr ), reverseValue )
                                    cmds.setAttr( newShader + '.' + targetAttr, value, value, value )
                                except:
                                    pass
            
            cmds.hyperShade( objects=shader )
            selObjs = cmds.ls( sl=1 )
            
            shadingEngine = cmds.sets( renderable=1, noSurfaceShader=1, empty=1, name=shader + 'SG' )
            shaderConnect( newShader, shadingEngine )
            cmds.sets( selObjs, e=1, fe= shadingEngine )
            
            newShader = cmds.rename( newShader, shader+'_convert' )
            newShaders.append( newShader )

        materials = Window_cmds.getMaterials()
        firstMat = None
        cmds.textScrollList( Window_global.tsl_shaderList, e=1, ra=1 )
        for material in materials:
            if not firstMat: firstMat = material
            cmds.textScrollList( Window_global.tsl_shaderList, e=1, a=material )

        cmds.select( newShaders )
        
        Window_global.nodeInfomation = {}
    
    
    
    @staticmethod
    def selectShader( evt=0 ):
        
        selectedItems = cmds.textScrollList( Window_global.tsl_shaderList, q=1, si=1 )
        cmds.select( selectedItems )






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
        
        cmds.scriptJob( k=Window_global.scriptJop )
        Window_cmds.selectObjectByMaterials( selList )
        Window_global.scriptJop = cmds.scriptJob( e=['SelectionChanged', Window_cmds.selectionChanged ], parent= Window_global.name )
        
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
        Window_global.updateMatAttrs()
        
        if cmds.window( Window_global.name, ex=1 ):
            cmds.deleteUI( Window_global.name, wnd=1 )
        cmds.window( Window_global.name, title=Window_global.title )
        
        Window_global.scriptJop = cmds.scriptJob( e=['SelectionChanged', Window_cmds.selectionChanged ], parent= Window_global.name )
        
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
        
        cmds.window( Window_global.name, e=1, wh= Window_global.wh, rtf=1 )
        cmds.showWindow( Window_global.name )
        
        #Window_cmds.getAllNodeInfomation()


def show():
    Window().show()


