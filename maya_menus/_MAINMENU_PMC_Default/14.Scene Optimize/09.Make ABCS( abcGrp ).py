import pymel.core
sels = pymel.core.ls( sl=1 )
sels[0].v.set( 0 )
sels[0].rename( 'abcs' )
children = pymel.core.listRelatives(sels[0], c=1, ad=1, type='transform'  )
for child in children:
    child.rename( child.nodeName().replace( ':', '_' ) )