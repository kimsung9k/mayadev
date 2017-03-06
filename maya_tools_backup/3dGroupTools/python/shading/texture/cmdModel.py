import maya.mel as mel
import shading.texture.model

mel.eval( 'source "%s"' % shading.texture.model.OpenFileTextureManagerInfo._melScriptPath )

mc_OpenFileTextureManager ="""import maya.mel as mel
mel.eval( "FileTextureManager" )
"""