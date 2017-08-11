import pymel.core

sels = pymel.core.ls( sl=1 )

bls = sels[:-1]
target = sels[-1]

blNode = sgCmds.getNodeFromHistory( target.listRelatives( c=1 )[0], 'blendShape' )[0]
wAttrNames = [ wAttr.split( '.' )[-1] for wAttr in cmds.ls( blNode + '.w[*]' ) ]

for bl in bls:
    origName = bl.replace( '_bt', '' )
    index = wAttrNames.index( origName )
    pymel.core.blendShape( blNode, e=1, tc=0, ib=1, t=[ target, index, bl, 0.5 ] ) 