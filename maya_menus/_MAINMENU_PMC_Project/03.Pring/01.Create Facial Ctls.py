from sgMaya import sgModel, sgCmds
import pymel.core

def getXYSlider( width, height, colorIndex = None, texturePath = '' ):
    
    slider     = sgCmds.makeController( sgModel.Controller.move2Points, 0.5 )
    sliderBase = sgCmds.SliderBase().create( 'xy' )
    pymel.core.parent( slider, sliderBase )
    cmds.rename( sliderBase.name(), 'Ctl_Facial' )
    
    cmds.transformLimits( slider.name(), tx=[0,1], etx=[1,0] )
    cmds.transformLimits( slider.name(), ty=[0,1], ety=[1,0] )
    
    keyAttrs = cmds.listAttr( slider.name(), k=1, sn=1 )
    if not keyAttrs : keyAttrs = []
    chAttrs = cmds.listAttr( slider.name(), cb=1, sn=1 )
    if not chAttrs : chAttrs = []
    keyAttrs += chAttrs
    
    for keyAttr in keyAttrs:
        if keyAttr in ['tx', 'ty'] : continue
        cmds.setAttr( slider.attr( keyAttr ).name(), e=1, lock=1, k=0 )
        cmds.setAttr( slider.attr( keyAttr ).name(), e=1, cb=0 )
    
    sliderBaseParent = sgCmds.makeParent( sliderBase )
    pymel.core.select( sliderBaseParent )
    sliderBase.setAttr( 'slideSizeX', width )
    sliderBase.setAttr( 'slideSizeY', height )
    
    pPlane = cmds.polyPlane( w=1, h=1, sx=1, sy=1, ax=[0,0,1], cuv=2, ch=1 )[0]
    shape = cmds.listRelatives( pPlane, s=1, f=1 )[0]
    cmds.setAttr( shape + '.castsShadows', 0 )
    cmds.setAttr( shape + '.receiveShadows', 0 )
    cmds.setAttr( shape + '.motionBlur', 0 )
    cmds.setAttr( shape + '.primaryVisibility', 0 )
    cmds.setAttr( shape + '.smoothShading', 0 )
    cmds.setAttr( shape + '.visibleInReflections', 0 )
    cmds.setAttr( shape + '.visibleInRefractions', 0 )
    cmds.setAttr( pPlane + '.overrideEnabled', 1 )
    cmds.setAttr( pPlane + '.overrideDisplayType', 2 )
    
    av = cmds.createNode( 'plusMinusAverage' )
    md = cmds.createNode( 'multiplyDivide' )
    cmds.connectAttr( sliderBase.attr( 'slideSizeX' ).name(), av + '.input2D[0].input2Dx' )
    cmds.connectAttr( sliderBase.attr( 'slideSizeY' ).name(), av + '.input2D[0].input2Dy' )
    cmds.setAttr( av + '.input2D[1].input2Dx', 1 )
    cmds.setAttr( av + '.input2D[1].input2Dy', 1 )
    cmds.connectAttr( sliderBase.attr( 'slideSizeX' ).name(), md + '.input1X' )
    cmds.connectAttr( sliderBase.attr( 'slideSizeY' ).name(), md + '.input1Y' )
    cmds.setAttr( md + '.input2X', 0.5 )
    cmds.setAttr( md + '.input2Y', 0.5 )
    
    cmds.connectAttr( av + '.output2Dx', pPlane+'.sx' )
    cmds.connectAttr( av + '.output2Dy', pPlane+'.sy' )
    cmds.connectAttr( md + '.outputX', pPlane+'.tx' )
    cmds.connectAttr( md + '.outputY', pPlane+'.ty' )
    
    cmds.parent( pPlane, sliderBase.name() )
    
    if colorIndex:
        cmds.setAttr( slider.name() + '.overrideEnabled', 1 )
        cmds.setAttr( slider.name() + '.overrideColor', colorIndex )
        cmds.setAttr( sliderBase.name() + '.overrideEnabled', 1 )
        cmds.setAttr( sliderBase.name() + '.overrideColor', 1 )
    
    mouthShader = cmds.shadingNode( 'lambert', asShader=1 )
    mouthShaderSg = cmds.sets( renderable=True, noSurfaceShader=True, empty=1, n=mouthShader + 'SG' )
    cmds.connectAttr( mouthShader + '.outColor', mouthShaderSg + '.surfaceShader' )
    cmds.sets( pPlane, e=1, forceElement = mouthShaderSg )
    
    eyeFileNode, textureNode = sgCmds.createTextureFileNode( texturePath )
    cmds.connectAttr( eyeFileNode + '.outColor', mouthShader + '.color' )

    cmds.transformLimits( slider.name(), tx=[0,5], etx=[1,1], ty=[0,4], ety=[1,1] )
    
    return slider, sliderBaseParent
 
def createRect( width, height ):
    rect = sgCmds.makeController( sgModel.Controller.planePoints, 1, makeParent=1 )
    rect.setAttr( 'shape_sx', width )
    rect.setAttr( 'shape_sz', height )
    rect.setAttr( 'shape_rx', 90 )
    return rect.name()

try:
    scenePath = cmds.file( q=1, sceneName=1 )
    splits = scenePath.split( '/' )
    index = splits.index( 'ch' )

    mapPath = '/'.join( splits[:index+2] ) + '/map'

    eyePath = mapPath + '/' + splits[index+1] + '_eye.jpg'
    mouthPath = mapPath + '/' + splits[index+1] + '_mouth.jpg'
except:
    eyePath = ''
    mouthPath = ''


slider1, sliderBase1 = getXYSlider( 5, 4, 22, eyePath )
slider2, sliderBase2 = getXYSlider( 5, 4, 20, eyePath )
slider3, sliderBase3 = getXYSlider( 5, 4, 21, mouthPath )
rect        = createRect( 7, 6 )
rect = cmds.rename( rect, 'Ctl_Facial' )

slider1.rename( 'Ctl_Eye_R_' )
slider2.rename( 'Ctl_Eye_L_' )
slider3.rename( 'Ctl_Mouth' )


cmds.setAttr( sliderBase1 + '.tx', -1 )
cmds.setAttr( sliderBase1 + '.ty',  1 )
cmds.setAttr( sliderBase1 + '.sx', -1 )

cmds.setAttr( sliderBase2 + '.tx',  1 )
cmds.setAttr( sliderBase2 + '.ty',  1 )

cmds.setAttr( sliderBase3 + '.tx',  -2.5 )
cmds.setAttr( sliderBase3 + '.ty',  -5 ) 

pymel.core.parent( sliderBase1, sliderBase2, sliderBase3, rect )