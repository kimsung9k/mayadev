from sgMaya import sgCmds
import pymel.core
mainGrp = pymel.core.ls( sl=1 )[0]

children = pymel.core.listRelatives( mainGrp, c=1, ad=1, type='mesh' )

proxyList = []
for child in children:
    proxyNode = sgCmds.getNodeFromHistory( child, 'RedshiftProxyMesh' )
    if not proxyNode: continue
    proxyList += proxyNode

pymel.core.select( proxyList )