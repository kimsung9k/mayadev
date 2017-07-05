from sgMaya import sgCmds
import pymel.core
mainGrp = pymel.core.ls( sl=1 )[0]

children = pymel.core.listRelatives( mainGrp, c=1, ad=1, type='mesh' )

sceneNumber = cmds.file( q=1, sceneName=1 ).split( '/' )[-1].split( '_' )[1]

animationPath = 'Z:/SW_S2_Pipeline/03_Main-production/05_Animation/EP237/scene/animation/EP237_animatedTrees'
sceneAnimationPath = animationPath.replace( 'EP237_animatedTrees', 'EP237_%s_animatedTrees' % sceneNumber )

proxyTargets = {'Small_Tree_A':'small_treeA',
                'Small_Tree_B':'small_tree',
                'rainbow_shower_proxy':'tree_flower',
                'plumeria_proxy':'plumeria',
                'palm_tree':'palm_tree',
                'hibiscus_proxy':'hibiscus',
                'small_tree_palm_proxy':'small_tree_palm',
                'treeA_proxy':'treeA',
                'bush':'bush',
                'treeB_proxy':'treeB',
                'tree_flower_proxy':'tree_tmp'}

proxyList = {}
for child in children:
    proxyNode = sgCmds.getNodeFromHistory( child, 'RedshiftProxyMesh' )
    if not proxyNode: continue
    proxyName = proxyNode[0].fileName.get().split( '/' )[-1].split( '.' )[0]
    proxyList[ proxyName ] = proxyNode[0]

for proxyName, node in proxyList.items():
    if not proxyTargets.has_key( proxyName ): continue
    proxyTarget = proxyTargets[ proxyName ]
    if os.path.exists( sceneAnimationPath + '/' + proxyTarget ):
        proxyPath = sceneAnimationPath + '/' + proxyTarget
    else:
        proxyPath = animationPath + '/' + proxyTarget
    
    print "proxyPath : ", proxyPath
    
    firstProxy = None
    for root, dirs, names in os.walk( proxyPath ):
        firstProxy = root + '/' + names[0]
        break
    if not firstProxy: continue
    node.fileName.set( firstProxy )
    node.useFrameExtension.set( 1 )