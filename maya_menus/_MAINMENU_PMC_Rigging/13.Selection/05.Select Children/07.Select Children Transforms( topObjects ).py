import pymel.core
sels = pymel.core.ls( sl=1 )
selChildren = []
for sel in sels:
    selChildren += sel.listRelatives( c=1, ad=1, type='transform' )
pymel.core.select( selChildren )