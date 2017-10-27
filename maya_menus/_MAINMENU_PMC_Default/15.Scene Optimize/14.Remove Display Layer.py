import pymel.core
displayLayers = pymel.core.ls( type='displayLayer' )
for displayLayer in displayLayers:
    if not displayLayer.v.get(): continue
    if displayLayer.name() == 'defaultLayer': continue
    pymel.core.delete( displayLayer )