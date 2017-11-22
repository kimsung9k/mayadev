import pymel.core

sels = pymel.core.listRelatives( pymel.core.ls( sl=1 ), c=1, ad=1, type='ikHandle' )
sels += pymel.core.listRelatives( pymel.core.ls( sl=1 ), c=1, ad=1, type='ikEffector' )
pymel.core.delete( sels )