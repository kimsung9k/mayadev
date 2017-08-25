from sgModules import sgdata
from sgModules import sgcommands
slider     = sgcommands.makeController( sgdata.Controllers.move2Points, 0.5 )
sliderBase = sgcommands.SliderBase().create('x')
sgcommands.parent( slider, sliderBase )

cmds.transformLimits( slider.name(), tx=[0,1], etx=[1,0] )
cmds.transformLimits( slider.name(), ty=[0,1], ety=[1,0] )

keyAttrs = slider.listAttr( k=1, sn=1 )
keyAttrs += slider.listAttr( cb=1, sn=1 )

for keyAttr in keyAttrs:
    if keyAttr in ['tx'] : continue
    cmds.setAttr( slider.attr( keyAttr ).name(), e=1, lock=1, k=0 )
    cmds.setAttr( slider.attr( keyAttr ).name(), e=1, cb=0 )

sliderBaseParent = sgcommands.makeParent( sliderBase )
sgcommands.select( sliderBaseParent )