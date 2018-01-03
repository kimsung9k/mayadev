import pymel.core
from sgMaya import sgCmds

eyeCtl = pymel.core.ls( 'EyeBDCtrl' )[0]

sgCmds.addOptionAttribute( eyeCtl )
sgCmds.addAttr( eyeCtl, ln='specMode', at='enum', en=':default:twinkle', k=1 )
sgCmds.addAttr( eyeCtl, ln='twinkleIndex', at='long', k=1 )

twinkleShader = pymel.core.ls( sl=1 )[0]

texturePath = os.path.dirname( cmds.file( q=1, sceneName=1 ) ) + '/texture'
twinklePath = texturePath + '/TwinkleEye.0001.png'
twinkleSmallPath = texturePath + '/TwinkleEye_small.0001.png'

newShaders = []
def convertTwincleTexture( twinkleShader ):
    files = twinkleShader.listConnections( s=1, d=0, type='file' )
    if not files: return None
    targetFile = files[0]
    
    fileConnections = targetFile.listConnections( s=0, d=1, p=1, c=1 )
    
    lambertShaderCon = None
    rsShaderCon = None
    for origCon, dstCon in fileConnections:
        if origCon.longName() == 'outColor':
            lambertShaderCon = dstCon
        elif origCon.longName() == 'outAlpha':
            rsShaderCon = dstCon
    
    print lambertShaderCon
    print rsShaderCon
    
    if not rsShaderCon:
        rsShaderCon = pymel.core.createNode( 'lambert' ).outColor
        newShaders.append( rsShaderCon.node() )
    
    textureOutAttrs = ['outColor','outAlpha']
    
    for outAttrs, inAttr, texturePath in [ [ textureOutAttrs, lambertShaderCon, twinkleSmallPath],[ textureOutAttrs, rsShaderCon, twinklePath ] ]: 
        newFileNode    = pymel.core.createNode( 'file' )
        layeredTexture = pymel.core.createNode( 'layeredTexture' )
        layeredTexture.alphaIsLuminance.set( 1 )
        newFileNode.outColor >> layeredTexture.attr( 'inputs[0].color' ); layeredTexture.attr( 'inputs[0].blendMode' ).set( 0 )
        targetFile.outColor  >> layeredTexture.attr( 'inputs[1].color' ); layeredTexture.attr( 'inputs[1].blendMode' ).set( 0 )
        for attr in textureOutAttrs:
            try:
                layeredTexture.attr( attr ) >> inAttr
            except:continue
        eyeCtl.attr( 'specMode' ) >> layeredTexture.attr( 'inputs[0].isVisible' )
        newFileNode.fileTextureName.set( texturePath )
        

convertTwincleTexture( twinkleShader )

print eyeCtl.attr( 'twinkleIndex' ).name()
print '(' + eyeCtl.attr( 'twinkleIndex' ).name(), " + 100000) % 3 + 1"
newShaders.append( twinkleShader )
pymel.core.select( newShaders )
