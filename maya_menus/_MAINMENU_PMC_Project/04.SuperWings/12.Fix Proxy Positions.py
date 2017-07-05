import pymel.core
from maya import mel
from sgMaya import sgCmds

sels = cmds.ls( sl=1 )

try:pymel.core.namespace( rm='bg_237_Heilala_Festival',mergeNamespaceWithParent = True )
except:pass
mel.eval( 'file -r -type "mayaBinary"  -ignoreVersion -gl -mergeNamespacesOnClash false -namespace "bg_237_Heilala_Festival" -options "v=0;" "Z:/SW_S2_Pipeline/03_Main-production/01_episode/ep237/bg/bg_237_Heilala_Festival/bg_237_Heilala_Festival.mb";' )

smallTreeProxy = pymel.core.ls( 'bg_237_Heilala_Festival:rsProxy15' )[0]
fileName = smallTreeProxy.fileName.get()
replaceName = fileName.replace( 'Small_Tree_A', 'Small_Tree_B' )
smallTreeProxy.fileName.set( replaceName )

setMatrixTargets = { 'bg_237_Heilala_Festival:polySurface582':'bg_237_Heilala_Festival_gpu2:Small_Tree_A6_gpu',
                     'bg_237_Heilala_Festival:polySurface581':'bg_237_Heilala_Festival_gpu2:Small_Tree_A5_gpu',
                     'bg_237_Heilala_Festival:polySurface583':'bg_237_Heilala_Festival_gpu2:Small_Tree_A7_gpu',
                     'bg_237_Heilala_Festival:polySurface584':'bg_237_Heilala_Festival_gpu2:Small_Tree_A8_gpu',
                     'bg_237_Heilala_Festival:tree_flower_proxy101':'bg_237_Heilala_Festival_gpu2:tree_flower_proxy106_gpu',
                     'bg_237_Heilala_Festival:polySurface578':'bg_237_Heilala_Festival_gpu2:Small_Tree_A2_gpu',
                     'bg_237_Heilala_Festival:polySurface577':'bg_237_Heilala_Festival_gpu2:Small_Tree_A1_gpu',
                     'bg_237_Heilala_Festival:palm_tree_all|bg_237_Heilala_Festival:palm_tree13|bg_237_Heilala_Festival:palm_tree13':'bg_237_Heilala_Festival_gpu2:palm_tree16_gpu',
                     'bg_237_Heilala_Festival:polySurface598':'bg_237_Heilala_Festival_gpu2:Small_Tree_A10686262_gpu',
                     'bg_237_Heilala_Festival:palm_tree_all|bg_237_Heilala_Festival:palm_tree14|bg_237_Heilala_Festival:palm_tree14':'bg_237_Heilala_Festival_gpu2:palm_tree13_gpu',
                     'bg_237_Heilala_Festival:palm_tree_all|bg_237_Heilala_Festival:palm_tree15|bg_237_Heilala_Festival:palm_tree15':'bg_237_Heilala_Festival_gpu2:palm_tree15_gpu',
                     'bg_237_Heilala_Festival:polySurface589':'bg_237_Heilala_Festival_gpu2:Small_Tree_A1064_gpu',
                     'bg_237_Heilala_Festival:polySurface590':'bg_237_Heilala_Festival_gpu2:Small_Tree_A1065_gpu',
                     'bg_237_Heilala_Festival:polySurface595':'bg_237_Heilala_Festival_gpu2:Small_Tree_A106862626262_gpu',
                     'bg_237_Heilala_Festival:polySurface596':'bg_237_Heilala_Festival_gpu2:Small_Tree_A1068626262_gpu',
                     'bg_237_Heilala_Festival:tree_flower_proxy3':'bg_237_Heilala_Festival_gpu2:tree_flower_proxy100_gpu',
                     'bg_237_Heilala_Festival:tree_flower_proxy97':'bg_237_Heilala_Festival_gpu2:tree_flower_proxy98_gpu',
                     'bg_237_Heilala_Festival:tree_flower_proxy96':'bg_237_Heilala_Festival_gpu2:tree_flower_proxy101_gpu',
                     'bg_237_Heilala_Festival:tree_flower_proxy98':'bg_237_Heilala_Festival_gpu2:tree_flower_proxy3_gpu',
                     'bg_237_Heilala_Festival:tree_flower_proxy99':'bg_237_Heilala_Festival_gpu2:tree_flower_proxy105_gpu',
                     'bg_237_Heilala_Festival:polySurface593':'bg_237_Heilala_Festival_gpu2:Small_Tree_A1068_gpu',
                     'bg_237_Heilala_Festival:polySurface592':'bg_237_Heilala_Festival_gpu2:Small_Tree_A1067_gpu',
                     'bg_237_Heilala_Festival:polySurface591':'bg_237_Heilala_Festival_gpu2:Small_Tree_A1066_gpu',
                     'bg_237_Heilala_Festival:polySurface587':'bg_237_Heilala_Festival_gpu2:Small_Tree_A1062_gpu',
                     'bg_237_Heilala_Festival:polySurface588':'bg_237_Heilala_Festival_gpu2:Small_Tree_A1063_gpu',
                     'bg_237_Heilala_Festival:polySurface580':'bg_237_Heilala_Festival_gpu2:Small_Tree_A4_gpu',
                     'bg_237_Heilala_Festival:polySurface579':'bg_237_Heilala_Festival_gpu2:Small_Tree_A3_gpu',
                     'bg_237_Heilala_Festival:sky1':'bg_237_Heilala_Festival_gpu2:sky1'}


duplicateTargets = {'bg_237_Heilala_Festival:tree_flower_proxy44':['bg_237_Heilala_Festival_gpu2:tree_flower_proxy103_gpu',
                                                                    'bg_237_Heilala_Festival_gpu2:tree_flower_proxy97_gpu',
                                                                    'bg_237_Heilala_Festival_gpu2:tree_flower_proxy99_gpu',
                                                                    'bg_237_Heilala_Festival_gpu2:tree_flower_proxy102_gpu',
                                                                    'bg_237_Heilala_Festival_gpu2:tree_flower_proxy107_gpu',
                                                                    'bg_237_Heilala_Festival_gpu2:tree_flower_proxy96_gpu',
                                                                    ''],
                   'bg_237_Heilala_Festival:treeA_proxy_ori18':['bg_237_Heilala_Festival_gpu2:treeA_proxy_ori31_gpu',
                                                                'bg_237_Heilala_Festival_gpu2:treeA_proxy_ori12_gpu',
                                                                'bg_237_Heilala_Festival_gpu2:treeA_proxy_ori20_gpu',
                                                                'bg_237_Heilala_Festival_gpu2:treeA_proxy_ori32_gpu'],
                   'bg_237_Heilala_Festival:palm_tree_all|bg_237_Heilala_Festival:palm_tree13|bg_237_Heilala_Festival:palm_tree13':['bg_237_Heilala_Festival_gpu2:palm_tree14_gpu'],
                   'bg_237_Heilala_Festival:polySurface590':['bg_237_Heilala_Festival_gpu2:Small_Tree_A10686262626262_gpu'],
                   'bg_237_Heilala_Festival:pasted__rock1573065729457287':['bg_237_Heilala_Festival_gpu2:rock15737257295_gpu',
                                                                           'bg_237_Heilala_Festival_gpu2:rock1573725729557287_gpu'],
                   'bg_237_Heilala_Festival:pasted__rock15730657293':['bg_237_Heilala_Festival_gpu2:rock1573725729557289_gpu',
                                                                       'bg_237_Heilala_Festival_gpu2:rock1573725729557290_gpu']}

for src, dst in setMatrixTargets.items():
    pymel.core.xform( src, ws=1, matrix=cmds.getAttr( dst + '.wm' ) )

for src, dsts in duplicateTargets.items():
    proxyMesh = sgCmds.getNodeFromHistory( src, 'RedshiftProxyMesh' )
    for dst in dsts:
        if not dst: continue
        if proxyMesh:
            mesh = pymel.core.createNode( 'mesh' )
            meshObj = mesh.getParent()
            proxyMesh[0].outMesh >> mesh.inMesh
        else:
            meshObj = pymel.core.duplicate( src )[0]
        pymel.core.xform( meshObj, ws=1, matrix=cmds.getAttr( dst + '.wm' ) )
        srcP = cmds.listRelatives( src, p=1, f=1 )[0]
        meshObj.setParent( srcP )
        meshObj.rename( src.split( ':' )[-1] )
        if src == 'bg_237_Heilala_Festival:pasted__rock15730657293':
            print "src : ", src
            pymel.core.move( 0, -8.52, 0, meshObj, ws=1, r=1 )

mel.eval( 'rename "pasted__rock1573065729457287" "pasted__rock1";' )
mel.eval( 'rename "pasted__rock-8714123717657207257" "pasted__rock1";' )

cmds.setAttr( 'bg_237_Heilala_Festival:tree_plane_all.v', 0 )
cmds.setAttr( 'bg_237_Heilala_Festival:tree_flower_all.v', 0 )
for target in ['bg_237_Heilala_Festival:treeA5', 'bg_237_Heilala_Festival:treeB5', 'bg_237_Heilala_Festival:treeB6', 'bg_237_Heilala_Festival:treeA7', 'bg_237_Heilala_Festival:treeA8']:
    cmds.setAttr( target + '.v', 0 )

pymel.core.ls( 'bg_237_Heilala_Festival:rsProxy15' )[0].fileName.set( 'Z:/SW_S2_Pipeline/03_Main-production/05_Animation/EP237/scene/animation/EP237_animatedTrees/small_treeB/small_treeB.0091.rs' )
pymel.core.ls( 'bg_237_Heilala_Festival:rsProxy15' )[0].useFrameExtension.set( 1 )

cmds.select( sels )