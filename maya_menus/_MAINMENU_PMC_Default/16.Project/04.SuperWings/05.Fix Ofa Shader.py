import maya.cmds as cmds

tongueShaders = cmds.ls( 'Tongue_sh', recursive=1 )
tongueMeshs = cmds.ls( 'Tongue', recursive=1 )

for tongueShader in tongueShaders:
    if tongueShader.lower().find( 'ofa' ) == -1: continue
    if tongueShader.lower().find( 'ofa_ns' ) != -1: continue
    shaderNs = tongueShader.replace( 'Tongue_sh', '' )
    shaderSg = cmds.listConnections( tongueShader + '.outColor', type='shadingEngine' )
    for tongueMesh in tongueMeshs:
        meshNs = tongueMesh.replace( 'Tongue', '' )
        if shaderNs != meshNs: continue
        cmds.sets( tongueMesh, e=1, forceElement = shaderSg[0] )


import maya.cmds as cmds

toothUp = 'Tooth_up'
toothLower = 'Tooth_under'

mouthInShader = 'Mouth_IN_shSG'
toothShader   = 'Tooth_shSG'

upFaces    = [u'Tooth_up.f[0:27]', u'Tooth_up.f[67:69]', u'Tooth_up.f[94:121]', u'Tooth_up.f[161:163]', u'Tooth_up.f[188:577]']
lowerFaces = [u'Tooth_under.f[0:10]', u'Tooth_under.f[16]', u'Tooth_under.f[42:46]', u'Tooth_under.f[89:99]', u'Tooth_under.f[105]', u'Tooth_under.f[131:135]', u'Tooth_under.f[178:567]']

cuTooths = cmds.ls( toothUp, r=1 )
ns = ''
for cuTooth in cuTooths:
    if cuTooth.lower().find( 'ofa' ) == -1: continue
    if cuTooth.lower().find( 'ofa_ns' ) != -1: continue
    ns = cuTooth.replace( toothUp, '' )

cuFaces = []
for upFace in upFaces:
    cuFaces.append( ns + upFace )
for lowerFace in lowerFaces:
    cuFaces.append( ns + lowerFace )

cmds.sets( [ns + toothUp, ns + toothLower], e=1, forceElement = ns + mouthInShader )
cmds.sets( cuFaces, e=1, forceElement = ns + toothShader )