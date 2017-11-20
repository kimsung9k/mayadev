import pymel.core
sels = pymel.core.ls( type='renderLayer' )
for sel in sels:
    if sel == 'defaultRenderLayer': continue
    pymel.core.delete( sel )