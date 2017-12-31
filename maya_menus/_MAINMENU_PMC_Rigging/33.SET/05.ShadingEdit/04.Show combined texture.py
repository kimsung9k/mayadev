from sgMaya import sgCmds
import pymel.core
sels = pymel.core.ls( sl=1 )
selHs = pymel.core.listRelatives( sels , c=1, ad=1, type='transform' )
selHs += sels

for sel in selHs:
    if not sel.getShape(): continue
    shaders = sgCmds.getShadersFromObject( sel )
    if not shaders: continue
    shader = shaders[0]
    meterialInfos = shader.message.listConnections( s=0, d=1, type='materialInfo' )
    if not meterialInfos: continue
    if not pymel.core.isConnected( shader.message, meterialInfos[0].attr( 'texture[0]' ) ):
        shader.message >> meterialInfos[0].attr( 'texture[0]' )
    try:shader.attr( "resolution" ).set( 128 )
    except:pass