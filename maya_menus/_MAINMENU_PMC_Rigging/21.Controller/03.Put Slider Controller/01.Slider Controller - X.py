from sgMaya import sgCmds, sgModel
import pymel.core
from maya import cmds

slider     = sgCmds.makeController( sgModel.Controller.move2Points, 0.5 )
sliderBase = sgCmds.createSliderBase('x')
slider.setParent( sliderBase )

cmds.transformLimits( slider.name(), tx=[0,1], etx=[1,0] )
cmds.transformLimits( slider.name(), ty=[0,1], ety=[1,0] )

keyAttrs =  cmds.listAttr( slider.name(), k=1, sn=1 )
keyAttrs += cmds.listAttr( slider.name(), cb=1, sn=1 )

for keyAttr in keyAttrs:
    if keyAttr in ['tx'] : continue
    cmds.setAttr( slider.attr( keyAttr ).name(), e=1, lock=1, k=0 )
    cmds.setAttr( slider.attr( keyAttr ).name(), e=1, cb=0 )

sliderBaseParent = sgCmds.makeParent( sliderBase )
pymel.core.select( sliderBaseParent )