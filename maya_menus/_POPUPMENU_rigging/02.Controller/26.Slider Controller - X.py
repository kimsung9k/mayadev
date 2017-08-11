from sgMaya import sgCmds, sgModel

slider     = sgCmds.makeController( sgdata.Controllers.move2Points, 0.5 )
sliderBase = sgCmds.createSliderBase('x')
pymel.core.parent( slider, sliderBase )

cmds.transformLimits( slider.name(), tx=[0,1], etx=[1,0] )
cmds.transformLimits( slider.name(), ty=[0,1], ety=[1,0] )

keyAttrs = slider.listAttr( k=1, sn=1 )
keyAttrs += slider.listAttr( cb=1, sn=1 )

for keyAttr in keyAttrs:
    if keyAttr.attrName() in ['tx'] : continue
    cmds.setAttr( keyAttr.name(), e=1, lock=1, k=0 )
    cmds.setAttr( keyAttr.name(), e=1, cb=0 )

sliderBaseParent = sgCmds.makeParent( sliderBase )
pymel.core.select( sliderBaseParent )