import pymel.core
sels = pymel.core.listRelatives( pymel.core.ls( sl=1 ), c=1, ad=1, type='joint' )
sels += pymel.core.ls( sl=1 )

for sel in sels:
    for sel in sels:
        sel.jo.set( 0,0,0 )