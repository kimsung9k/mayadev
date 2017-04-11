from sgProject import pingo
inst = pingo.FacialLayeredTextureConnection()

sels = cmds.ls( sl=1 )
controllers = sels[0]

for sel in sels[1:]:
    inst.sliderConnection( controller + '.ty', sel, offset=0 )