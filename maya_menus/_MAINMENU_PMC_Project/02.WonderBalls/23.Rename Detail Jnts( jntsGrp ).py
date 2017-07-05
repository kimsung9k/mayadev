import pymel.core
sels = pymel.core.ls( sl=1 )

children = pymel.core.listRelatives( sels, c=1, ad=1, f=1, type='joint' )

for child in children:
    pChild = child.getParent()
    child.rename( pChild + '00' )